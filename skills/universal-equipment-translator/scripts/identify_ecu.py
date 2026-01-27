#!/usr/bin/env python3

"""
identify_ecu.py
Identify ECU manufacturer from CAN messages.
"""

import sys
import argparse
import sqlite3
from pathlib import Path

try:
    import can
except ImportError:
    print("Error: python-can library not installed")
    print("Install with: pip3 install python-can")
    sys.exit(1)


class ECUIdentifier:
    """Identify ECU manufacturer from CAN traffic."""

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

    def identify_manufacturer(self, address: int) -> dict:
        """Identify manufacturer by source address."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT
                m.name,
                m.protocol_name,
                m.description,
                sa.start_address,
                sa.end_address,
                sa.description as address_description
            FROM source_addresses sa
            JOIN manufacturers m ON sa.manufacturer_id = m.id
            WHERE sa.start_address <= ? AND sa.end_address >= ?
            ORDER BY (sa.end_address - sa.start_address) ASC
            LIMIT 1
        """, (address, address))
        row = cursor.fetchone()

        if row:
            return {
                "name": row[0],
                "protocol": row[1],
                "description": row[2],
                "address_range": f"0x{row[3]:02X} - 0x{row[4]:02X}",
                "address_description": row[5],
            }
        return None

    def parse_can_id(self, can_id: int) -> dict:
        """Parse CAN extended ID into components."""
        if can_id > 0x7FF:
            # Extended CAN ID (29-bit)
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
            # Standard CAN ID (11-bit)
            return {
                "type": "standard",
                "id": can_id,
                "id_hex": f"0x{can_id:03X}",
            }

    def listen_and_identify(self, interface: str, timeout: int = 10):
        """Listen to CAN bus and identify ECUs."""
        print(f"Listening on {interface} for {timeout} seconds...")
        print("Press Ctrl+C to stop early")
        print("=" * 60)

        identified_ecus = {}

        try:
            # Setup CAN bus
            bus = can.Bus(interface=interface, bustype="socketcan")

            import time
            start_time = time.time()

            while time.time() - start_time < timeout:
                msg = bus.recv(timeout=1)

                if msg:
                    # Parse CAN ID
                    if msg.is_extended_id:
                        parsed = self.parse_can_id(msg.arbitration_id)

                        # Identify manufacturer
                        manufacturer = self.identify_manufacturer(parsed['source_address'])

                        if manufacturer:
                            ecu_key = f"{manufacturer['name']}@0x{parsed['source_address']:02X}"

                            if ecu_key not in identified_ecus:
                                identified_ecus[ecu_key] = {
                                    "manufacturer": manufacturer['name'],
                                    "protocol": manufacturer['protocol'],
                                    "source_address": parsed['source_address'],
                                    "pgn": parsed['pgn'],
                                    "pgn_hex": parsed['pgn_hex'],
                                    "messages_count": 1,
                                }
                                print(f"Identified: {manufacturer['name']} ({manufacturer['protocol']}) at SA 0x{parsed['source_address']:02X}")
                            else:
                                identified_ecus[ecu_key]['messages_count'] += 1

        except KeyboardInterrupt:
            print("\nInterrupted by user")
        finally:
            bus.shutdown()

        return identified_ecus

    def print_summary(self, identified_ecus: dict):
        """Print summary of identified ECUs."""
        print()
        print("=" * 60)
        print("Identified ECUs Summary")
        print("=" * 60)

        if not identified_ecus:
            print("No ECUs identified")
            print()
            print("Possible reasons:")
            print("  - No CAN traffic on bus")
            print("  - Unknown source addresses (not in database)")
            print("  - Manufacturer not in protocol database")
            return

        for ecu_key, ecu in identified_ecus.items():
            print()
            print(f"ECU: {ecu['manufacturer']}")
            print(f"  Protocol: {ecu['protocol']}")
            print(f"  Source Address: 0x{ecu['source_address']:02X}")
            print(f"  Last PGN: {ecu['pgn_hex']}")
            print(f"  Messages: {ecu['messages_count']}")


def main():
    parser = argparse.ArgumentParser(description="Identify ECU manufacturer from CAN messages")

    parser.add_argument("--interface", "-i", default="can0",
                        help="CAN interface (default: can0)")
    parser.add_argument("--timeout", "-t", type=int, default=10,
                        help="Listen timeout in seconds (default: 10)")
    parser.add_argument("--protocol-db", "-d",
                        default="/opt/equipment-translator/protocols.db",
                        help="Protocol database path")

    args = parser.parse_args()

    # Check if protocol database exists
    if not Path(args.protocol_db).exists():
        print(f"Error: Protocol database not found: {args.protocol_db}")
        print("Run 'python3 scripts/setup-database.py' to create database")
        sys.exit(1)

    # Create identifier
    identifier = ECUIdentifier(args.protocol_db)

    # Listen and identify
    identified = identifier.listen_and_identify(args.interface, args.timeout)

    # Print summary
    identifier.print_summary(identified)


if __name__ == "__main__":
    main()
