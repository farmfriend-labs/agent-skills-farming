#!/usr/bin/env python3
"""
Initialization script for precision agriculture database
Creates database schema and initial tables
"""

import sqlite3
import os
from pathlib import Path


def init_database(db_path='/var/lib/precision-ag/precision-ag.db'):
    """Initialize database with schema

    Args:
        db_path: Path to database file
    """

    # Ensure database directory exists
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    print(f"Initializing database at: {db_path}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Enable foreign keys
    cursor.execute('PRAGMA foreign_keys = ON')

    # Create fields table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fields (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            boundary_polygon TEXT NOT NULL,
            area_acres REAL,
            centroid_lat REAL,
            centroid_lon REAL,
            crop_type TEXT,
            soil_type TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    print("✓ Created 'fields' table")

    # Create guidance_lines table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS guidance_lines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            field_id INTEGER NOT NULL,
            guidance_type TEXT NOT NULL,
            spacing REAL NOT NULL,
            orientation REAL,
            lines_data TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (field_id) REFERENCES fields(id) ON DELETE CASCADE
        )
    ''')
    print("✓ Created 'guidance_lines' table")

    # Create prescriptions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prescriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            field_id INTEGER NOT NULL,
            prescription_name TEXT NOT NULL,
            input_type TEXT NOT NULL,
            zones_data TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (field_id) REFERENCES fields(id) ON DELETE CASCADE
        )
    ''')
    print("✓ Created 'prescriptions' table")

    # Create operations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS operations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            field_id INTEGER NOT NULL,
            operation_type TEXT NOT NULL,
            start_date TIMESTAMP,
            end_date TIMESTAMP,
            product TEXT,
            rate REAL,
            acres_treated REAL,
            notes TEXT,
            FOREIGN KEY (field_id) REFERENCES fields(id) ON DELETE CASCADE
        )
    ''')
    print("✓ Created 'operations' table")

    # Create yield_data table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS yield_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            field_id INTEGER NOT NULL,
            harvest_date TIMESTAMP NOT NULL,
            crop TEXT NOT NULL,
            moisture REAL,
            total_yield REAL,
            yield_data_json TEXT,
            as_applied_map TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (field_id) REFERENCES fields(id) ON DELETE CASCADE
        )
    ''')
    print("✓ Created 'yield_data' table")

    # Create weather_data table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            field_id INTEGER,
            timestamp TIMESTAMP NOT NULL,
            temperature REAL,
            humidity REAL,
            precipitation REAL,
            wind_speed REAL,
            wind_direction REAL,
            data_source TEXT,
            UNIQUE(field_id, timestamp),
            FOREIGN KEY (field_id) REFERENCES fields(id) ON DELETE CASCADE
        )
    ''')
    print("✓ Created 'weather_data' table")

    # Create implements table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS implements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            manufacturer TEXT,
            model TEXT,
            type TEXT,
            width REAL,
            sections INTEGER,
            isobus_compatible BOOLEAN DEFAULT 1,
            can_address INTEGER,
            configuration_json TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    print("✓ Created 'implements' table")

    # Create operation_logs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS operation_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            field_id INTEGER,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            log_type TEXT NOT NULL,
            message TEXT,
            data_json TEXT,
            FOREIGN KEY (field_id) REFERENCES fields(id) ON DELETE CASCADE
        )
    ''')
    print("✓ Created 'operation_logs' table")

    # Create indexes for performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_operations_field ON operations(field_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_yield_data_field ON yield_data(field_id)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_weather_field_time ON weather_data(field_id, timestamp)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_operation_logs_field_time ON operation_logs(field_id, timestamp)')
    print("✓ Created indexes")

    # Commit changes
    conn.commit()
    conn.close()

    print("\n✓ Database initialization complete")


if __name__ == '__main__':
    import os

    # Get database path from environment or use default
    db_path = os.getenv('DB_PATH', '/var/lib/precision-ag/precision-ag.db')

    init_database(db_path)
