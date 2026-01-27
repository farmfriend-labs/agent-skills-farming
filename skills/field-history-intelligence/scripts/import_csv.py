#!/usr/bin/env python3
"""
Field History Intelligence - Data Import Script (CSV)
Import field data from CSV files
"""

import sqlite3
import csv
import argparse
import sys
from datetime import datetime

def import_csv(conn, csv_file, data_type, season=None):
    """Import data from CSV file"""
    cursor = conn.cursor()

    # Map data types to tables
    data_type_map = {
        'planting': {
            'table': 'planting',
            'columns': ['field_name', 'season', 'variety', 'planting_date', 'seeding_rate', 'row_spacing', 'depth', 'method']
        },
        'harvest': {
            'table': 'harvest',
            'columns': ['field_name', 'season', 'harvest_date', 'variety', 'yield', 'moisture', 'test_weight']
        },
        'inputs': {
            'table': 'inputs',
            'columns': ['field_name', 'season', 'application_date', 'input_type', 'product_name', 'rate', 'rate_unit', 'method', 'total_cost']
        },
    }

    if data_type not in data_type_map:
        print(f"Unknown data type: {data_type}")
        print(f"Supported types: {', '.join(data_type_map.keys())}")
        return False

    table_info = data_type_map[data_type]
    table = table_info['table']
    expected_columns = table_info['columns']

    # Read CSV file
    try:
        with open(csv_file, 'r', newline='') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return False

    # Validate columns
    actual_columns = list(rows[0].keys()) if rows else []
    missing_columns = set(expected_columns) - set(actual_columns)

    if missing_columns:
        print(f"Missing columns in CSV: {missing_columns}")
        print(f"Expected: {expected_columns}")
        print(f"Found: {actual_columns}")
        return False

    # Import data
    imported = 0
    errors = 0

    for row in rows:
        try:
            # Get field_id
            field_name = row.get('field_name')
            cursor.execute("SELECT id FROM fields WHERE name = ?", (field_name,))
            field_result = cursor.fetchone()

            if not field_result:
                print(f"Field not found: {field_name}")
                errors += 1
                continue

            field_id = field_result[0]

            # Get season_id
            season_name = row.get('season')
            cursor.execute("SELECT id FROM seasons WHERE name = ?", (season_name,))
            season_result = cursor.fetchone()

            if not season_result:
                print(f"Season not found: {season_name}")
                errors += 1
                continue

            season_id = season_result[0]

            # Build insert based on data type
            if data_type == 'planting':
                cursor.execute("""
                    INSERT INTO planting (
                        field_id, season_id, variety, planting_date,
                        seeding_rate, row_spacing, depth, method
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    field_id, season_id,
                    row.get('variety'),
                    row.get('planting_date'),
                    float(row.get('seeding_rate', 0)) if row.get('seeding_rate') else None,
                    float(row.get('row_spacing', 0)) if row.get('row_spacing') else None,
                    float(row.get('depth', 0)) if row.get('depth') else None,
                    row.get('method')
                ))

            elif data_type == 'harvest':
                cursor.execute("""
                    INSERT INTO harvest (
                        field_id, season_id, harvest_date, variety,
                        yield, moisture, test_weight
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    field_id, season_id,
                    row.get('harvest_date'),
                    row.get('variety'),
                    float(row.get('yield', 0)) if row.get('yield') else None,
                    float(row.get('moisture', 0)) if row.get('moisture') else None,
                    float(row.get('test_weight', 0)) if row.get('test_weight') else None,
                ))

            elif data_type == 'inputs':
                cursor.execute("""
                    INSERT INTO inputs (
                        field_id, season_id, application_date,
                        input_type, product_name, rate, rate_unit,
                        method, total_cost
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    field_id, season_id,
                    row.get('application_date'),
                    row.get('input_type'),
                    row.get('product_name'),
                    float(row.get('rate', 0)) if row.get('rate') else None,
                    row.get('rate_unit'),
                    row.get('method'),
                    float(row.get('total_cost', 0)) if row.get('total_cost') else None,
                ))

            imported += 1

        except Exception as e:
            print(f"Error importing row: {e}")
            errors += 1

    conn.commit()

    print(f"\nImport Summary:")
    print(f"  Imported: {imported} records")
    print(f"  Errors: {errors}")
    print(f"  Total: {len(rows)} rows")

    return True

def main():
    parser = argparse.ArgumentParser(
        description='Import field data from CSV files'
    )
    parser.add_argument(
        '--database',
        default='/opt/field-history/field-data.db',
        help='Path to SQLite database'
    )
    parser.add_argument(
        'csv_file',
        help='Path to CSV file'
    )
    parser.add_argument(
        'data_type',
        choices=['planting', 'harvest', 'inputs'],
        help='Type of data to import'
    )

    args = parser.parse_args()

    # Connect to database
    try:
        conn = sqlite3.connect(args.database)
    except Exception as e:
        print(f"Error connecting to database: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        success = import_csv(conn, args.csv_file, args.data_type)
        if not success:
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        conn.close()
        sys.exit(1)

    conn.close()

if __name__ == '__main__':
    main()
