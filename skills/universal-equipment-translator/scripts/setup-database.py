#!/usr/bin/env python3

"""
setup-database.py
Create and initialize the protocol database for equipment translator.
"""

import sqlite3
import os
import json
from pathlib import Path

# Database schema
SCHEMA_SQL = """
-- Manufacturers table
CREATE TABLE IF NOT EXISTS manufacturers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    protocol_name TEXT NOT NULL,
    description TEXT,
    standard BOOLEAN DEFAULT FALSE
);

-- PGN (Parameter Group Number) definitions
CREATE TABLE IF NOT EXISTS pgns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pgn INTEGER NOT NULL UNIQUE,
    name TEXT NOT NULL,
    description TEXT,
    manufacturer_id INTEGER,
    FOREIGN KEY (manufacturer_id) REFERENCES manufacturers(id)
);

-- Message mappings between protocols
CREATE TABLE IF NOT EXISTS message_mappings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_pgn INTEGER NOT NULL,
    source_manufacturer_id INTEGER,
    target_pgn INTEGER NOT NULL,
    target_manufacturer_id INTEGER,
    translation_rule TEXT,
    safety_critical BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (source_manufacturer_id) REFERENCES manufacturers(id),
    FOREIGN KEY (target_manufacturer_id) REFERENCES manufacturers(id)
);

-- Data field definitions
CREATE TABLE IF NOT EXISTS data_fields (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pgn_id INTEGER NOT NULL,
    field_name TEXT NOT NULL,
    byte_offset INTEGER NOT NULL,
    bit_offset INTEGER DEFAULT 0,
    bit_length INTEGER NOT NULL,
    data_type TEXT NOT NULL,
    units TEXT,
    scale REAL DEFAULT 1.0,
    offset REAL DEFAULT 0.0,
    description TEXT,
    FOREIGN KEY (pgn_id) REFERENCES pgns(id)
);

-- Source address ranges
CREATE TABLE IF NOT EXISTS source_addresses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    manufacturer_id INTEGER NOT NULL,
    start_address INTEGER NOT NULL,
    end_address INTEGER NOT NULL,
    description TEXT,
    FOREIGN KEY (manufacturer_id) REFERENCES manufacturers(id)
);

-- CAN message templates
CREATE TABLE IF NOT EXISTS message_templates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    template_json TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Translation logs (for debugging)
CREATE TABLE IF NOT EXISTS translation_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source_can_id TEXT NOT NULL,
    target_can_id TEXT NOT NULL,
    source_manufacturer TEXT,
    target_manufacturer TEXT,
    success BOOLEAN,
    error_message TEXT
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_pgn_source ON message_mappings(source_pgn);
CREATE INDEX IF NOT EXISTS idx_pgn_target ON message_mappings(target_pgn);
CREATE INDEX IF NOT EXISTS idx_sa_manufacturer ON source_addresses(manufacturer_id, start_address, end_address);
"""

# ISO 11783 standard PGNs
ISO_11783_PGNS = [
    (0x00F804, "Address Claim", "ECU claiming its address on the bus"),
    (0x00FE00, "Request PGN", "Request specific PGN from an ECU"),
    (0x00FF00, "Transport Protocol", "Transport protocol for messages > 8 bytes"),
    (0x00FF84, "Transport Protocol Connection Management", "TP.CM messages"),
    (0x01FF00, "VT to ECU", "Virtual Terminal to ECU message"),
    (0x01FF84, "ECU to VT", "ECU to Virtual Terminal message"),
    (0x00FEF8, "Proprietary A", "Manufacturer-specific PGN (0x00FEF8)"),
    (0x00FEFF, "Proprietary B", "Manufacturer-specific PGN (0x00FEFF)"),
]

# Manufacturer protocols
MANUFACTURERS = [
    ("Universal", "ISO 11783", "Standard ISO 11783 protocol", True),
    ("John Deere", "JDLink", "John Deere proprietary extension of ISO 11783", False),
    ("Case IH", "AFS", "Case IH Advanced Farming Systems", False),
    ("AGCO", "AGCOMMAND", "AGCO command and control protocol", False),
    ("Kubota", "K-Communicator", "Kubota protocol", False),
    ("CNH", "IPL", "CNH Industrial protocol", False),
]

# Source address ranges (approximate)
SOURCE_ADDRESS_RANGES = [
    ("Universal", 0, 0xFE, "Reserved standard addresses"),
    ("John Deere", 0x10, 0x1F, "John Deere equipment range"),
    ("Case IH", 0x20, 0x2F, "Case IH equipment range"),
    ("AGCO", 0x30, 0x3F, "AGCO equipment range"),
]


def create_database(db_path):
    """Create protocol database with schema and initial data."""
    # Create directory if it doesn't exist
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
        print(f"Created directory: {db_dir}")

    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Create schema
        print("Creating database schema...")
        cursor.executescript(SCHEMA_SQL)
        conn.commit()

        # Insert manufacturers
        print("Inserting manufacturers...")
        for name, protocol, description, standard in MANUFACTURERS:
            cursor.execute(
                "INSERT OR IGNORE INTO manufacturers (name, protocol_name, description, standard) VALUES (?, ?, ?, ?)",
                (name, protocol, description, standard)
            )
        conn.commit()

        # Get manufacturer IDs
        manufacturer_ids = {}
        cursor.execute("SELECT id, name FROM manufacturers")
        for row in cursor.fetchall():
            manufacturer_ids[row[1]] = row[0]

        # Insert ISO 11783 PGNs
        print("Inserting ISO 11783 PGNs...")
        for pgn, name, description in ISO_11783_PGNS:
            cursor.execute(
                "INSERT OR IGNORE INTO pgns (pgn, name, description, manufacturer_id) VALUES (?, ?, ?, ?)",
                (pgn, name, description, manufacturer_ids["Universal"])
            )
        conn.commit()

        # Insert source address ranges
        print("Inserting source address ranges...")
        for name, start, end, description in SOURCE_ADDRESS_RANGES:
            if name in manufacturer_ids:
                cursor.execute(
                    "INSERT OR IGNORE INTO source_addresses (manufacturer_id, start_address, end_address, description) VALUES (?, ?, ?, ?)",
                    (manufacturer_ids[name], start, end, description)
                )
        conn.commit()

        # Insert basic message mappings
        print("Creating basic message mappings...")
        insert_basic_mappings(cursor, manufacturer_ids)
        conn.commit()

        # Create indexes for performance
        print("Creating indexes...")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_pgn_source ON message_mappings(source_pgn)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_pgn_target ON message_mappings(target_pgn)")
        conn.commit()

        # Statistics
        print("\nDatabase Statistics:")
        cursor.execute("SELECT COUNT(*) FROM manufacturers")
        print(f"  Manufacturers: {cursor.fetchone()[0]}")

        cursor.execute("SELECT COUNT(*) FROM pgns")
        print(f"  PGNs defined: {cursor.fetchone()[0]}")

        cursor.execute("SELECT COUNT(*) FROM message_mappings")
        print(f"  Message mappings: {cursor.fetchone()[0]}")

        cursor.execute("SELECT COUNT(*) FROM source_addresses")
        print(f"  Source address ranges: {cursor.fetchone()[0]}")

        print(f"\nDatabase created successfully at: {db_path}")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()


def insert_basic_mappings(cursor, manufacturer_ids):
    """Insert basic message mappings between protocols."""

    # Identity mappings (same protocol)
    for name in manufacturer_ids:
        for pgn, _, _ in ISO_11783_PGNS:
            cursor.execute(
                "INSERT OR IGNORE INTO message_mappings (source_pgn, source_manufacturer_id, target_pgn, target_manufacturer_id, translation_rule, safety_critical) VALUES (?, ?, ?, ?, ?, ?)",
                (pgn, manufacturer_ids[name], pgn, manufacturer_ids[name], "identity", False)
            )

    # ISO 11783 to manufacturer mappings (placeholder - needs real protocols)
    # These would be filled in from actual protocol documentation
    for manufacturer in ["John Deere", "Case IH", "AGCO"]:
        if manufacturer in manufacturer_ids:
            for pgn, _, _ in ISO_11783_PGNS:
                # Map ISO PGNs to manufacturer equivalent
                cursor.execute(
                    "INSERT OR IGNORE INTO message_mappings (source_pgn, source_manufacturer_id, target_pgn, target_manufacturer_id, translation_rule, safety_critical) VALUES (?, ?, ?, ?, ?, ?)",
                    (pgn, manufacturer_ids["Universal"], pgn, manufacturer_ids[manufacturer], "iso_to_manufacturer", False)
                )


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Setup protocol database for equipment translator")
    parser.add_argument("--db-path", "-d", default="/opt/equipment-translator/protocols.db",
                        help="Path to database file (default: /opt/equipment-translator/protocols.db)")
    parser.add_argument("--force", "-f", action="store_true",
                        help="Force overwrite existing database")

    args = parser.parse_args()

    # Check if database exists
    if os.path.exists(args.db_path) and not args.force:
        print(f"Database already exists at: {args.db_path}")
        response = input("Overwrite? (yes/no): ")
        if response.lower() not in ["yes", "y"]:
            print("Aborted")
            return

    # Create database
    create_database(args.db_path)

    print("\nNext steps:")
    print("  1. Edit .env to set PROTOCOL_DB_PATH=" + args.db_path)
    print("  2. Run 'scripts/setup.sh' to configure CAN interface")
    print("  3. Run 'scripts/run.sh' to start translator")


if __name__ == "__main__":
    main()
