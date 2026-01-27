#!/usr/bin/env python3

"""
translator.py
Main translation engine for agricultural equipment protocols.
Translates between manufacturer-specific protocols and ISO 11783 standard.
"""

import sys
import argparse
import logging
import json
import sqlite3
from pathlib import Path
from typing import Optional, Dict, Any, Tuple
import time
from dataclasses import dataclass

try:
    import can
except ImportError:
    print("Error: python-can library not installed")
    print("Install with: pip3 install python-can")
    sys.exit(1)


@dataclass
class CANMessage:
    """Represents a CAN message."""
    interface: str
    arbitration_id: int
    data: bytes
    timestamp: float
    channel: Optional[str] = None

    @property
    def extended_id(self) -> bool:
        """Check if using extended CAN ID (29-bit)."""
        return self.arbitration_id > 0x7FF

    @property
    def priority(self) -> int:
        """Extract priority from CAN extended ID."""
        return (self.arbitration_id >> 26) & 0x07

    @property
    def pgn(self) -> int:
        """Extract PGN from CAN extended ID."""
        return (self.arbitration_id >> 8) & 0x03FFFF

    @property
    def source_address(self) -> int:
        """Extract source address from CAN extended ID."""
        return self.arbitration_id & 0xFF

    def __repr__(self):
        return f"CANMessage(id=0x{self.arbitration_id:08X}, len={len(self.data)}, data={self.data.hex()})"


class ProtocolDatabase:
    """Interface to protocol SQLite database."""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = None
        self.connect()

    def connect(self):
        """Connect to database."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
        except sqlite3.Error as e:
            raise RuntimeError(f"Cannot connect to database: {e}")

    def get_manufacturer_by_address(self, address: int) -> Optional[str]:
        """Identify manufacturer by source address."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT m.name
            FROM source_addresses sa
            JOIN manufacturers m ON sa.manufacturer_id = m.id
            WHERE sa.start_address <= ? AND sa.end_address >= ?
            LIMIT 1
        """, (address, address))
        row = cursor.fetchone()
        return row[0] if row else None

    def get_translation(self, source_pgn: int, source_manufacturer: str,
                     target_manufacturer: str) -> Optional[Dict]:
        """Get translation rule for message."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT
                mm.target_pgn,
                mm.translation_rule,
                mm.safety_critical,
                sm.name as source_man,
                tm.name as target_man
            FROM message_mappings mm
            JOIN manufacturers sm ON mm.source_manufacturer_id = sm.id
            JOIN manufacturers tm ON mm.target_manufacturer_id = tm.id
            WHERE mm.source_pgn = ? AND sm.name = ? AND tm.name = ?
        """, (source_pgn, source_manufacturer, target_manufacturer))
        row = cursor.fetchone()
        if row:
            return {
                "target_pgn": row[0],
                "translation_rule": row[1],
                "safety_critical": row[2],
                "source_manufacturer": row[3],
                "target_manufacturer": row[4],
            }
        return None

    def get_pgn_name(self, pgn: int, manufacturer: str) -> Optional[str]:
        """Get PGN name."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT p.name
            FROM pgns p
            JOIN manufacturers m ON p.manufacturer_id = m.id
            WHERE p.pgn = ? AND m.name = ?
        """, (pgn, manufacturer))
        row = cursor.fetchone()
        return row[0] if row else None

    def log_translation(self, source_id: str, target_id: str,
                      source_man: str, target_man: str,
                      success: bool, error: str = ""):
        """Log translation for debugging."""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO translation_logs
            (source_can_id, target_can_id, source_manufacturer, target_manufacturer, success, error_message)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (source_id, target_id, source_man, target_man, success, error))
        self.conn.commit()


class EquipmentTranslator:
    """Main translation engine."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.setup_logging()

        # Load protocol database
        self.log.info(f"Loading protocol database: {config['protocol_db']}")
        self.protocol_db = ProtocolDatabase(config['protocol_db'])

        # Setup CAN bus
        self.log.info(f"Setting up CAN interface: {config['interface']}")
        self.setup_can_bus()

        # Statistics
        self.stats = {
            "messages_processed": 0,
            "messages_translated": 0,
            "translation_errors": 0,
            "safety_violations_prevented": 0,
        }

        self.log.info("Translator initialized successfully")

    def setup_logging(self):
        """Configure logging."""
        log_level = getattr(logging, self.config['log_level'].upper(), logging.INFO)

        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.config['log_file']),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.log = logging.getLogger('EquipmentTranslator')

    def setup_can_bus(self):
        """Setup CAN bus interface."""
        try:
            # Create bus configuration
            bus_config = {
                "interface": "socketcan",
                "channel": self.config['interface'],
            }

            # Add bitrate if specified
            if 'baudrate' in self.config:
                bus_config['bitrate'] = self.config['baudrate']

            self.bus = can.Bus(**bus_config)
            self.log.info("CAN bus connected successfully")

        except Exception as e:
            raise RuntimeError(f"Failed to connect to CAN bus: {e}")

    def identify_manufacturer(self, msg: CANMessage) -> str:
        """Identify manufacturer from message."""
        manufacturer = self.protocol_db.get_manufacturer_by_address(msg.source_address)
        return manufacturer or "Universal"

    def parse_message(self, msg: CANMessage) -> Dict[str, Any]:
        """Parse CAN message."""
        manufacturer = self.identify_manufacturer(msg)
        pgn_name = self.protocol_db.get_pgn_name(msg.pgn, manufacturer)

        return {
            "manufacturer": manufacturer,
            "pgn": msg.pgn,
            "pgn_name": pgn_name,
            "priority": msg.priority,
            "source_address": msg.source_address,
            "data": msg.data,
            "data_hex": msg.data.hex(),
            "original_id": f"0x{msg.arbitration_id:08X}",
        }

    def translate_message(self, parsed: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Translate message between protocols."""
        mode = self.config['translation_mode']

        # ISO 11783 mode - enforce standard
        if mode == "iso11783":
            # Skip translation if already standard
            if parsed['manufacturer'] == "Universal":
                return None

            # Translate to ISO 11783
            translation = self.protocol_db.get_translation(
                parsed['pgn'],
                parsed['manufacturer'],
                "Universal"
            )

            if translation:
                return self.apply_translation(parsed, translation)

        # Raw mode - no translation
        elif mode == "raw":
            return None

        # Hybrid mode - translate if possible
        elif mode == "hybrid":
            translation = self.protocol_db.get_translation(
                parsed['pgn'],
                parsed['manufacturer'],
                "Universal"
            )
            if translation:
                return self.apply_translation(parsed, translation)
            return None

        return None

    def apply_translation(self, parsed: Dict[str, Any],
                         translation: Dict[str, Any]) -> Dict[str, Any]:
        """Apply translation rule to message."""
        target_pgn = translation['target_pgn']
        rule = translation['translation_rule']
        safety_critical = translation['safety_critical']

        # Safety check
        if safety_critical and self.config['safety_override_disabled']:
            self.log.warning(f"Blocking safety-critical message translation: PGN 0x{parsed['pgn']:08X}")
            self.stats['safety_violations_prevented'] += 1
            return None

        # Apply translation rule
        if rule == "identity":
            # No change to data, just new PGN
            new_id = self.rebuild_can_id(
                parsed['priority'],
                target_pgn,
                parsed['source_address']
            )
        else:
            # More complex translation would go here
            # For now, assume identity mapping
            new_id = self.rebuild_can_id(
                parsed['priority'],
                target_pgn,
                parsed['source_address']
            )

        return {
            "arbitration_id": new_id,
            "data": parsed['data'],
            "translation_rule": rule,
            "original_manufacturer": translation['source_manufacturer'],
            "target_manufacturer": translation['target_manufacturer'],
        }

    def rebuild_can_id(self, priority: int, pgn: int, source_address: int) -> int:
        """Rebuild 29-bit CAN ID from components."""
        return (priority << 26) | (pgn << 8) | source_address

    def send_message(self, translated: Dict[str, Any]):
        """Send translated message to CAN bus."""
        try:
            msg = can.Message(
                arbitration_id=translated['arbitration_id'],
                data=translated['data'],
                is_extended_id=True
            )
            self.bus.send(msg)
            self.log.debug(f"Sent: 0x{translated['arbitration_id']:08X}")
        except Exception as e:
            self.log.error(f"Failed to send message: {e}")

    def process_message(self, msg: CANMessage):
        """Process incoming CAN message."""
        self.stats['messages_processed'] += 1

        try:
            # Parse message
            parsed = self.parse_message(msg)

            self.log.debug(f"Received: {parsed['original_id']} from {parsed['manufacturer']}")

            # Translate message
            translated = self.translate_message(parsed)

            if translated:
                # Send translated message
                self.send_message(translated)
                self.stats['messages_translated'] += 1

                # Log translation
                self.protocol_db.log_translation(
                    parsed['original_id'],
                    f"0x{translated['arbitration_id']:08X}",
                    parsed['manufacturer'],
                    translated['target_manufacturer'],
                    True
                )
            else:
                # Pass through without translation
                pass

        except Exception as e:
            self.log.error(f"Error processing message: {e}")
            self.stats['translation_errors'] += 1

    def run(self):
        """Main translation loop."""
        self.log.info("Starting translation loop...")
        self.log.info(f"Mode: {self.config['translation_mode']}")
        self.log.info(f"Safety override disabled: {self.config['safety_override_disabled']}")

        try:
            while True:
                msg = self.bus.recv()
                can_msg = CANMessage(
                    interface=self.config['interface'],
                    arbitration_id=msg.arbitration_id,
                    data=msg.data,
                    timestamp=msg.timestamp,
                    channel=msg.channel
                )
                self.process_message(can_msg)

                # Print stats every 100 messages
                if self.stats['messages_processed'] % 100 == 0:
                    self.log.info(f"Stats: {self.stats}")

        except KeyboardInterrupt:
            self.log.info("Shutting down...")
            self.log.info(f"Final stats: {self.stats}")
        finally:
            if self.bus:
                self.bus.shutdown()


def main():
    parser = argparse.ArgumentParser(description="Equipment Protocol Translator")

    parser.add_argument("--interface", "-i", default="can0",
                        help="CAN interface (default: can0)")
    parser.add_argument("--baudrate", "-b", type=int, default=250000,
                        help="CAN baud rate (default: 250000)")
    parser.add_argument("--mode", "-m", default="iso11783",
                        choices=["iso11783", "raw", "hybrid"],
                        help="Translation mode (default: iso11783)")
    parser.add_argument("--log-level", "-l", default="info",
                        choices=["debug", "info", "warn", "error"],
                        help="Log level (default: info)")
    parser.add_argument("--log-file", "-f",
                        default="/var/log/equipment-translator.log",
                        help="Log file path")
    parser.add_argument("--protocol-db", "-d",
                        default="/opt/equipment-translator/protocols.db",
                        help="Protocol database path")
    parser.add_argument("--offline-mode", "-o", action="store_true",
                        help="Offline mode (no external API calls)")
    parser.add_argument("--safety-override-disabled", action="store_true",
                        help="Disable safety overrides (default: enabled)")

    args = parser.parse_args()

    # Build config
    config = {
        "interface": args.interface,
        "baudrate": args.baudrate,
        "translation_mode": args.mode,
        "log_level": args.log_level,
        "log_file": args.log_file,
        "protocol_db": args.protocol_db,
        "offline_mode": args.offline_mode,
        "safety_override_disabled": args.safety_override_disabled,
    }

    # Create and run translator
    translator = EquipmentTranslator(config)
    translator.run()


if __name__ == "__main__":
    main()
