#!/usr/bin/env python3
"""
Emergency Diagnostics Liberator - Code Database Setup

Creates and initializes the diagnostic trouble code database
with manufacturer-specific codes and generic OBD-II/J1939 codes.
"""

import sqlite3
import os
import sys
from pathlib import Path

# Database path
CODE_DB_PATH = os.environ.get('CODE_DB_PATH', '/opt/emergency-diagnostics/codes.db')

def create_database():
    """Create the code database and initialize tables."""
    db_dir = os.path.dirname(CODE_DB_PATH)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)

    conn = sqlite3.connect(CODE_DB_PATH)
    cursor = conn.cursor()

    # Create manufacturers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS manufacturers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            code TEXT NOT NULL,
            description TEXT
        )
    ''')

    # Create codes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            spn INTEGER NOT NULL,
            fmi INTEGER NOT NULL,
            manufacturer_id INTEGER,
            description TEXT NOT NULL,
            severity TEXT NOT NULL,
            common_causes TEXT,
            suggested_tests TEXT,
            repair_complexity TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (manufacturer_id) REFERENCES manufacturers(id),
            UNIQUE(spn, fmi, manufacturer_id)
        )
    ''')

    # Create code_categories table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS code_categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            spn_range_start INTEGER,
            spn_range_end INTEGER
        )
    ''')

    # Create diagnostic_sessions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS diagnostic_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            equipment_type TEXT,
            equipment_make TEXT,
            equipment_model TEXT,
            vin TEXT,
            interface_type TEXT,
            protocol TEXT,
            total_codes INTEGER,
            critical_codes INTEGER
        )
    ''')

    # Create session_codes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS session_codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            spn INTEGER NOT NULL,
            fmi INTEGER NOT NULL,
            description TEXT,
            severity TEXT,
            ecu TEXT,
            status TEXT,
            FOREIGN KEY (session_id) REFERENCES diagnostic_sessions(id)
        )
    ''')

    # Create sensor_data table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER NOT NULL,
            spn INTEGER NOT NULL,
            parameter_name TEXT,
            value REAL,
            unit TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES diagnostic_sessions(id)
        )
    ''')

    conn.commit()
    print("Database structure created successfully")
    return conn, cursor

def populate_manufacturers(cursor):
    """Populate manufacturers table with major agricultural equipment manufacturers."""
    manufacturers = [
        ('Universal', 'GEN', 'Generic OBD-II/J1939 codes applicable to all equipment'),
        ('John Deere', 'JD', 'John Deere proprietary codes'),
        ('Case IH', 'CI', 'Case IH AFS codes'),
        ('AGCO', 'AG', 'AGCO codes (Challenger, Massey Ferguson, Fendt)'),
        ('Kubota', 'KU', 'Kubota codes'),
        ('New Holland', 'NH', 'New Holland codes'),
        ('Claas', 'CL', 'Claas codes'),
    ]

    for name, code, description in manufacturers:
        try:
            cursor.execute('''
                INSERT INTO manufacturers (name, code, description)
                VALUES (?, ?, ?)
            ''', (name, code, description))
            print(f"  Added manufacturer: {name}")
        except sqlite3.IntegrityError:
            print(f"  Manufacturer {name} already exists")

def populate_categories(cursor):
    """Populate code categories."""
    categories = [
        ('Engine System', 'Engine-related codes including sensors, actuators, and controls', 91, 250),
        ('Transmission', 'Transmission and drivetrain codes', 500, 650),
        ('Hydraulics', 'Hydraulic system codes', 1000, 1200),
        ('Electrical', 'Electrical system codes', 1500, 1700),
        ('Brakes', 'Brake system codes', 597, 599),
        ('PTO', 'Power Take-Off codes', 960, 980),
        ('Emissions', 'Emissions control codes', 244, 247),
        ('Aftertreatment', 'Diesel aftertreatment codes', 3220, 3230),
    ]

    for name, description, start, end in categories:
        try:
            cursor.execute('''
                INSERT INTO code_categories (name, description, spn_range_start, spn_range_end)
                VALUES (?, ?, ?, ?)
            ''', (name, description, start, end))
            print(f"  Added category: {name}")
        except sqlite3.IntegrityError:
            print(f"  Category {name} already exists")

def populate_generic_codes(cursor):
    """Populate database with generic J1939/OBD-II codes."""
    # Get universal manufacturer ID
    cursor.execute("SELECT id FROM manufacturers WHERE name = 'Universal'")
    result = cursor.fetchone()
    if not result:
        print("  Warning: Universal manufacturer not found")
        return

    manufacturer_id = result[0]

    # Common engine codes
    codes = [
        # SPN 91 - Engine Coolant Temperature
        (91, 0, 'Engine Coolant Temperature Above Normal - Severe Overheat', 'Critical',
         'Thermostat failure, coolant leak, water pump failure, radiator blockage',
         'Check coolant level, inspect for leaks, check thermostat operation',
         'Medium'),
        (91, 1, 'Engine Coolant Temperature Below Normal', 'Warning',
         'Thermostat stuck open, sensor failure',
         'Check thermostat, verify sensor reading with manual temperature gauge',
         'Low'),
        (91, 3, 'Engine Coolant Temperature Voltage Above Normal or Open', 'Warning',
         'Sensor circuit high, sensor failure, wiring issue',
         'Check sensor wiring, test sensor resistance',
         'Medium'),
        (91, 4, 'Engine Coolant Temperature Voltage Below Normal or Open', 'Warning',
         'Sensor circuit low, sensor failure, short circuit',
         'Check sensor wiring, test sensor resistance',
         'Medium'),

        # SPN 100 - Engine Oil Pressure
        (100, 0, 'Engine Oil Pressure Above Normal', 'Warning',
         'Pressure regulator failure, wrong oil viscosity',
         'Check oil viscosity, inspect pressure relief valve',
         'Medium'),
        (100, 1, 'Engine Oil Pressure Below Normal', 'Critical',
         'Oil pump failure, low oil level, bearing wear, oil filter bypass',
         'Check oil level immediately, inspect for leaks, verify oil pump operation',
         'High'),
        (100, 3, 'Engine Oil Pressure Sensor Voltage Above Normal', 'Warning',
         'Sensor circuit high, sensor failure',
         'Check sensor wiring, test sensor',
         'Low'),
        (100, 4, 'Engine Oil Pressure Sensor Voltage Below Normal', 'Warning',
         'Sensor circuit low, sensor failure',
         'Check sensor wiring, test sensor',
         'Low'),

        # SPN 105 - Engine Speed
        (105, 2, 'Engine Speed Erratic', 'Critical',
         'Fuel delivery problem, sensor failure, wiring issue',
         'Check fuel system, inspect crankshaft position sensor and wiring',
         'High'),
        (105, 8, 'Engine Speed Signal Abnormal', 'Critical',
         'Sensor failure, wiring issue, ECU problem',
         'Inspect sensor and wiring, check ECU connections',
         'Medium'),

        # SPN 111 - Fuel Pressure
        (111, 0, 'Fuel Pressure Above Normal', 'Warning',
         'Pressure regulator failure, fuel return blockage',
         'Check fuel pressure regulator, inspect return lines',
         'Medium'),
        (111, 1, 'Fuel Pressure Below Normal', 'Critical',
         'Fuel filter blockage, fuel pump failure, air in fuel system',
         'Replace fuel filters, prime fuel system, check fuel pump',
         'Medium'),
        (111, 3, 'Fuel Pressure Sensor Voltage Above Normal', 'Warning',
         'Sensor circuit high, sensor failure',
         'Check sensor wiring, test sensor',
         'Low'),
        (111, 4, 'Fuel Pressure Sensor Voltage Below Normal', 'Warning',
         'Sensor circuit low, sensor failure',
         'Check sensor wiring, test sensor',
         'Low'),

        # SPN 1572 - Battery Voltage
        (1572, 0, 'Battery Voltage Above Normal - Overcharging', 'Warning',
         'Alternator voltage regulator failure',
         'Check alternator, test voltage regulator',
         'Medium'),
        (1572, 1, 'Battery Voltage Below Normal', 'Advisory',
         'Battery weak, alternator not charging, excessive load',
         'Check battery condition, test alternator output, reduce electrical load',
         'Low'),
        (1572, 3, 'Battery Voltage Sensor Circuit High', 'Warning',
         'Sensor circuit high, sensor failure',
         'Check sensor wiring, test sensor',
         'Low'),
        (1572, 4, 'Battery Voltage Sensor Circuit Low', 'Warning',
         'Sensor circuit low, sensor failure',
         'Check sensor wiring, test sensor',
         'Low'),

        # SPN 597 - Brake Pressure
        (597, 0, 'Brake Pressure Above Normal', 'Critical',
         'Brake system failure, valve failure',
         'Stop operation immediately, inspect brake system',
         'High'),
        (597, 1, 'Brake Pressure Below Normal', 'Critical',
         'Brake system failure, low brake fluid, leak',
         'Stop operation immediately, check brake fluid, inspect for leaks',
         'High'),

        # SPN 245 - DPF Differential Pressure
        (245, 1, 'DPF Differential Pressure Elevated', 'Warning',
         'DPF requiring regeneration, soot accumulation',
         'Perform DPF regeneration, check for operating conditions preventing regeneration',
         'Medium'),
        (245, 0, 'DPF Differential Pressure Critically High', 'Critical',
         'DPF blockage, regeneration failure',
         'Stop operation, perform immediate regeneration or DPF cleaning',
         'High'),

        # SPN 3226 - DEF Quality/Level
        (3226, 1, 'DEF Level Low', 'Advisory',
         'DEF tank low on fluid',
         'Refill DEF tank',
         'Low'),
        (3226, 3, 'DEF Quality Poor or Unknown', 'Warning',
         'Contaminated DEF, wrong fluid in tank',
         'Drain DEF tank, refill with proper DEF fluid',
         'Medium'),

        # SPN 949 - Hydraulic Oil Temperature
        (949, 0, 'Hydraulic Oil Temperature Above Normal - Severe', 'Critical',
         'Hydraulic system overload, cooling system failure',
         'Reduce hydraulic load, check hydraulic oil cooler',
         'Medium'),
        (949, 1, 'Hydraulic Oil Temperature Elevated', 'Warning',
         'Heavy load, high ambient temperature, cooler partially blocked',
         'Reduce load if possible, check cooler for debris',
         'Low'),

        # SPN 172 - Exhaust Gas Temperature
        (172, 0, 'Exhaust Gas Temperature Above Normal - Critical', 'Critical',
         'Engine overheat, fueling problem, turbocharger failure',
         'Stop operation, check engine coolant, inspect fuel system',
         'High'),
        (172, 1, 'Exhaust Gas Temperature Elevated', 'Warning',
         'High load, elevated ambient temperature',
         'Reduce load, check for air restrictions',
         'Low'),
    ]

    for spn, fmi, description, severity, causes, tests, complexity in codes:
        try:
            cursor.execute('''
                INSERT INTO codes (spn, fmi, manufacturer_id, description, severity, common_causes, suggested_tests, repair_complexity)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (spn, fmi, manufacturer_id, description, severity, causes, tests, complexity))
        except sqlite3.IntegrityError:
            # Code already exists, skip
            pass

    print(f"  Added {len(codes)} generic J1939 codes")

def main():
    """Main database setup function."""
    print(f"Setting up code database at: {CODE_DB_PATH}")
    print("")

    # Create database
    conn, cursor = create_database()
    print("")

    # Populate tables
    print("Populating manufacturers...")
    populate_manufacturers(cursor)
    print("")

    print("Populating code categories...")
    populate_categories(cursor)
    print("")

    print("Populating generic J1939 codes...")
    populate_generic_codes(cursor)
    print("")

    # Commit and close
    conn.commit()
    conn.close()

    print("==========================================")
    print("Database setup complete!")
    print("==========================================")
    print("")
    print(f"Database location: {CODE_DB_PATH}")
    print("Total codes available: TODO")  # Add count query
    print("")
    print("Next steps:")
    print("  1. Connect to equipment")
    print("  2. Run 'python3 scripts/diagnostics.py'")
    print("  3. Read and interpret diagnostic codes")
    print("")

if __name__ == '__main__':
    main()
