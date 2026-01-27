#!/usr/bin/env python3
"""
Field History Intelligence - Database Initialization Script
Initializes SQLite database with schema for field history tracking
"""

import sqlite3
import argparse
import sys
import os
from pathlib import Path

def create_schema(conn):
    """Create all database tables and indexes"""
    cursor = conn.cursor()

    # Fields table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fields (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            farm_name TEXT,
            acres REAL,
            soil_type TEXT,
            drainage_rating TEXT,
            gps_boundary TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Seasons table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS seasons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            year INTEGER NOT NULL,
            crop_type TEXT,
            planting_date DATE,
            harvest_date DATE,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Planting table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS planting (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            field_id INTEGER NOT NULL,
            season_id INTEGER NOT NULL,
            variety TEXT NOT NULL,
            planting_date DATE NOT NULL,
            seeding_rate REAL,
            population REAL,
            row_spacing REAL,
            depth REAL,
            method TEXT,
            FOREIGN KEY (field_id) REFERENCES fields(id),
            FOREIGN KEY (season_id) REFERENCES seasons(id)
        )
    """)

    # Harvest table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS harvest (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            field_id INTEGER NOT NULL,
            season_id INTEGER NOT NULL,
            variety TEXT,
            harvest_date DATE NOT NULL,
            yield REAL,
            moisture REAL,
            test_weight REAL,
            gross_yield REAL,
            dockage REAL,
            quality_notes TEXT,
            FOREIGN KEY (field_id) REFERENCES fields(id),
            FOREIGN KEY (season_id) REFERENCES seasons(id)
        )
    """)

    # Inputs table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inputs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            field_id INTEGER NOT NULL,
            season_id INTEGER NOT NULL,
            application_date DATE NOT NULL,
            input_type TEXT NOT NULL,
            product_name TEXT,
            rate REAL,
            rate_unit TEXT,
            method TEXT,
            total_quantity REAL,
            cost_per_unit REAL,
            total_cost REAL,
            equipment_id INTEGER,
            weather_conditions TEXT,
            notes TEXT,
            FOREIGN KEY (field_id) REFERENCES fields(id),
            FOREIGN KEY (season_id) REFERENCES seasons(id)
        )
    """)

    # Soil tests table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS soil_tests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            field_id INTEGER NOT NULL,
            test_date DATE NOT NULL,
            lab_name TEXT,
            sample_depth TEXT,
            ph REAL,
            organic_matter REAL,
            nitrogen REAL,
            phosphorus REAL,
            potassium REAL,
            calcium REAL,
            magnesium REAL,
            sulfur REAL,
            boron REAL,
            zinc REAL,
            iron REAL,
            manganese REAL,
            copper REAL,
            cec REAL,
            textural_class TEXT,
            notes TEXT,
            FOREIGN KEY (field_id) REFERENCES fields(id)
        )
    """)

    # Weather table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            field_id INTEGER NOT NULL,
            date DATE NOT NULL,
            precipitation REAL,
            max_temp REAL,
            min_temp REAL,
            avg_temp REAL,
            humidity REAL,
            wind_speed REAL,
            soil_temp_2in REAL,
            soil_temp_4in REAL,
            growing_degree_days REAL,
            notes TEXT,
            FOREIGN KEY (field_id) REFERENCES fields(id)
        )
    """)

    # Equipment table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS equipment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            make TEXT,
            model TEXT,
            year INTEGER,
            purchase_date DATE
        )
    """)

    # Equipment usage table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS equipment_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            equipment_id INTEGER NOT NULL,
            field_id INTEGER NOT NULL,
            season_id INTEGER NOT NULL,
            operation_date DATE NOT NULL,
            operation_type TEXT,
            hours REAL,
            acres_covered REAL,
            fuel_used REAL,
            efficiency REAL,
            notes TEXT,
            FOREIGN KEY (equipment_id) REFERENCES equipment(id),
            FOREIGN KEY (field_id) REFERENCES fields(id),
            FOREIGN KEY (season_id) REFERENCES seasons(id)
        )
    """)

    # Observations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS observations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            field_id INTEGER NOT NULL,
            season_id INTEGER,
            observation_date DATE NOT NULL,
            category TEXT,
            severity TEXT,
            description TEXT NOT NULL,
            location_in_field TEXT,
            photos TEXT,
            action_taken TEXT,
            resolved BOOLEAN DEFAULT FALSE,
            resolution_date DATE,
            created_by TEXT,
            FOREIGN KEY (field_id) REFERENCES fields(id),
            FOREIGN KEY (season_id) REFERENCES seasons(id)
        )
    """)

    # Financial records table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS financial_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            field_id INTEGER NOT NULL,
            season_id INTEGER NOT NULL,
            record_date DATE NOT NULL,
            category TEXT,
            description TEXT,
            amount REAL,
            unit TEXT,
            payment_method TEXT,
            receipt_image TEXT,
            notes TEXT,
            FOREIGN KEY (field_id) REFERENCES fields(id),
            FOREIGN KEY (season_id) REFERENCES seasons(id)
        )
    """)

    # Create indexes for performance
    indexes = [
        "CREATE INDEX IF NOT EXISTS idx_fields_name ON fields(name)",
        "CREATE INDEX IF NOT EXISTS idx_seasons_year ON seasons(year)",
        "CREATE INDEX IF NOT EXISTS idx_planting_field ON planting(field_id)",
        "CREATE INDEX IF NOT EXISTS idx_planting_season ON planting(season_id)",
        "CREATE INDEX IF NOT EXISTS idx_harvest_field ON harvest(field_id)",
        "CREATE INDEX IF NOT EXISTS idx_harvest_season ON harvest(season_id)",
        "CREATE INDEX IF NOT EXISTS idx_inputs_field ON inputs(field_id)",
        "CREATE INDEX IF NOT EXISTS idx_inputs_season ON inputs(season_id)",
        "CREATE INDEX IF NOT EXISTS idx_soil_tests_field ON soil_tests(field_id)",
        "CREATE INDEX IF NOT EXISTS idx_weather_field ON weather(field_id)",
        "CREATE INDEX IF NOT EXISTS idx_weather_date ON weather(date)",
        "CREATE INDEX IF NOT EXISTS idx_observation_field ON observations(field_id)",
    ]

    for index_sql in indexes:
        cursor.execute(index_sql)

    conn.commit()
    print("Database schema created successfully")

def insert_sample_data(conn, sample=False):
    """Insert sample data for testing"""
    if not sample:
        return

    cursor = conn.cursor()

    # Sample field
    cursor.execute("""
        INSERT INTO fields (name, farm_name, acres, soil_type, drainage_rating)
        VALUES ('North 40', 'Miller Farms', 40.5, 'Silt Loam', 'Good')
    """)

    # Sample season
    cursor.execute("""
        INSERT INTO seasons (name, year, crop_type, planting_date, harvest_date)
        VALUES ('2024 Corn', 2024, 'corn', '2024-04-15', '2024-10-15')
    """)

    conn.commit()
    print("Sample data inserted successfully")

def main():
    parser = argparse.ArgumentParser(
        description='Initialize Field History Intelligence database'
    )
    parser.add_argument(
        '--database',
        default='/opt/field-history/field-data.db',
        help='Path to SQLite database file'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Overwrite existing database'
    )
    parser.add_argument(
        '--sample',
        action='store_true',
        help='Insert sample data'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Verbose output'
    )

    args = parser.parse_args()

    # Create database directory if needed
    db_dir = os.path.dirname(args.database)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)
        print(f"Created directory: {db_dir}")

    # Check if database exists
    if os.path.exists(args.database) and not args.force:
        print(f"Database already exists: {args.database}")
        print("Use --force to overwrite")
        sys.exit(1)

    # Connect to database
    conn = sqlite3.connect(args.database)
    if args.verbose:
        print(f"Connected to database: {args.database}")

    try:
        create_schema(conn)
        insert_sample_data(conn, args.sample)

        # Print summary
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"\nCreated {len(tables)} tables:")
        for table in tables:
            print(f"  - {table[0]}")

        print(f"\nDatabase initialized successfully: {args.database}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        conn.close()
        sys.exit(1)

    conn.close()

if __name__ == '__main__':
    main()
