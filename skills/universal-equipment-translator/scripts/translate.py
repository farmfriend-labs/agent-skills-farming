#!/usr/bin/env python3

"""
translate.py
Translate single CAN message between protocols (for testing/debugging).
"""

import sys
import argparse
import sqlite3
from typing import Optional, Dict

try:
    import can
except ImportError:
    print("Error: python-can library not installed")
    print("Install with: pip3 install python-can")
    sys.exit(1)


def parse_can_id(can_id_str: str) -> int:
    """Parse CAN ID string to integer."""
    can_id_str = can_id_str.strip()

    # Handle hex prefix
    if can_id_str.startswith("0x") or can_id_str.startswith("0X"):
        return int(can_id_str, 16)

    # Handle decimal
    return int(can_id_str, 10)


def parse_can_data(data_str: str) -> bytes:
    """Parse CAN data string to bytes."""
    # Remove spaces and hex prefix
    data_str = data_str.strip().replace(" ", "")

    if data_str.startswith("0x") or data_str.startswith("0X"):
        data_str = data_str[2:]

    # Convert to bytes
    return bytes.fromhex(data_str)


def format_can_id(can_id: int) -> str:
    """Format CAN ID to hex string."""
    if can_id > 0x7FF:
        return f"0x{can_id:08X}"
    return f"0x{can_id:03X}"


def extract_can_components(can_id: int) -> Dict:
    """Extract CAN ID components."""
    if can_id > 0x7FF:
        # Extended ID (29-bit)
        priority = (can_id >> 26) & 0x07
        pgn = (can_id >> 8) & 0x03FFFF
        source_address = can_id & 0xFF
        return {
            "type": "extended",
            "priority": priority,
            "pgn": pgn,
            "pgn_hex": f"0x{pgn:06X}",
            "source_address": source_address,
            "source_address_hex": f"0x{source_address:02X}",
        }
    else:
        # Standard ID (11-bit)
        return {
            "type": "standard",
            "id": can_id,
            "id_hex": f"0x{can_id:03X}",
        }


class MessageTranslator:
    """Translate single message between protocols."""

    def __init__(self, protocol_db: str):
        self.protocol_db = protocol_db
        self.conn = None
        self.connect()

    def connect(self):
        """Connect to protocol database."""
        try:
            self.conn = sqlite3.connect(self.protocol_db)
            self.conn.row_factory = sqlite3.Row
        except sqlite3.Error as e:
            raise RuntimeError(f"Cannot connect to database: {e}")

    def get_manufacturer_id(self, name: str) -> Optional[int]:
        """Get manufacturer ID by name."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM manufacturers WHERE name = ?", (name,))
        row = cursor.fetchone()
        return row[0] if row else None

    def get_translation(self, source_pgn: int, source_manufacturer: str,
                     target_manufacturer: str) -> Optional[Dict]:
        """Get translation rule."""
        source_id = self.get_manufacturer_id(source_manufacturer)
        target_id = self.get_manufacturer_id(target_manufacturer)

        if not source_id or not target_id:
            return None

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

    def translate(self, can_id: int, data: bytes,
                source_protocol: str, target_protocol: str) -> Optional[Dict]:
        """Translate message."""
        # Extract CAN components
        components = extract_can_components(can_id)

        if components['type'] != 'extended':
            print("Error: Standard CAN IDs not supported for protocol translation")
            print("Only extended IDs (29-bit) are used in agricultural protocols")
            return None

        pgn = components['pgn']

        # Get translation
        translation = self.get_translation(pgn, source_protocol, target_protocol)

        if not translation:
            print(f"No translation found for PGN 0x{pgn:06X} from {source_protocol} to {target_protocol}")
            return None

        # Apply translation
        target_pgn = translation['target_pgn']
        priority = components['priority']
        source_address = components['source_address']

        # Rebuild CAN ID
        new_id = (priority << 26) | (target_pgn << 8) | source_address

        return {
            "original_id": format_can_id(can_id),
            "original_pgn": components['pgn_hex'],
            "original_data": data.hex(),
            "translated_id": format_can_id(new_id),
            "translated_pgn": f"0x{target_pgn:06X}",
            "translated_data": data.hex(),
            "translation_rule": translation['translation_rule'],
            "safety_critical": translation['safety_critical'],
            "source_protocol": source_protocol,
            "target_protocol": target_protocol,
        }


def main():
    parser = argparse.ArgumentParser(description="Translate single CAN message between protocols")

    parser.add_argument("--message", "-m", required=True,
                        help="CAN ID in hex (e.g., 0x18FF0001)")
    parser.add_argument("--data", "-d", default="",
                        help="CAN data in hex (e.g., DEADBEEF)")
    parser.add_argument("--source", "-s", default="Universal",
                        help="Source protocol (default: Universal)")
    parser.add_argument("--target", "-t", default="John Deere",
                        help="Target protocol (default: John Deere)")
    parser.add_argument("--protocol-db", "-p",
                        default="/opt/equipment-translator/protocols.db",
                        help="Protocol database path")

    args = parser.parse_args()

    # Parse message
    can_id = parse_can_id(args.message)
    data = parse_can_data(args.data)

    print(f"Input:")
    print(f"  CAN ID: {format_can_id(can_id)}")
    print(f"  Data: {data.hex()}")
    print(f"  Source Protocol: {args.source}")
    print(f"  Target Protocol: {args.target}")
    print()

    # Create translator
    translator = MessageTranslator(args.protocol_db)

    # Translate
    result = translator.translate(can_id, data, args.source, args.target)

    if result:
        print(f"Translation Result:")
        print(f"  Original: {result['original_id']} (PGN {result['original_pgn']})")
        print(f"  Translated: {result['translated_id']} (PGN {result['translated_pgn']})")
        print(f"  Rule: {result['translation_rule']}")
        print(f"  Safety Critical: {result['safety_critical']}")
    else:
        print(f"No translation available")
        sys.exit(1)


if __name__ == "__main__":
    main()
