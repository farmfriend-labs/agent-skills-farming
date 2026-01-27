#!/usr/bin/env python3
"""
Export Inventory - Export seed inventory to file
"""

import sqlite3
import os
import json
import csv
from datetime import datetime

# Configuration
DB_PATH = os.environ.get('SEED_DB_PATH', '/opt/seed-sovereignty/seeds.db')
EXPORT_PATH = os.environ.get('EXPORT_PATH', '/var/lib/seed-sovereignty/exports')
EXPORT_FORMAT = os.environ.get('EXPORT_FORMAT', 'json')


def get_connection():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def export_json():
    """Export inventory to JSON format"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM seeds ORDER BY variety_name ASC')
    seeds = cursor.fetchall()

    conn.close()

    # Convert to list of dicts
    seeds_data = []
    for seed in seeds:
        seed_dict = dict(seed)
        # Convert timestamp to string
        if seed_dict['date_added']:
            seed_dict['date_added'] = seed_dict['date_added']
        if seed_dict['last_tested']:
            seed_dict['last_tested'] = seed_dict['last_tested']
        seeds_data.append(seed_dict)

    # Create export directory
    export_dir = Path(EXPORT_PATH)
    export_dir.mkdir(parents=True, exist_ok=True)

    # Write JSON file
    filename = export_dir / f"seed_inventory_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(seeds_data, f, indent=2, default=str)

    print(f"\n✓ Exported {len(seeds_data)} seeds to {filename}")
    return filename


def export_csv():
    """Export inventory to CSV format"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM seeds ORDER BY variety_name ASC')
    seeds = cursor.fetchall()

    conn.close()

    # Create export directory
    export_dir = Path(EXPORT_PATH)
    export_dir.mkdir(parents=True, exist_ok=True)

    # Write CSV file
    filename = export_dir / f"seed_inventory_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(filename, 'w', newline='') as f:
        if seeds:
            writer = csv.DictWriter(f, fieldnames=seeds[0].keys())
            writer.writeheader()
            for seed in seeds:
                writer.writerow(dict(seed))

    print(f"\n✓ Exported {len(seeds)} seeds to {filename}")
    return filename


def export_text():
    """Export inventory to human-readable text format"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id, variety_name, crop_type, year_saved, source,
               quantity_grams, germination_pct, location_stored,
               container_type, last_tested, notes
        FROM seeds
        ORDER BY year_saved DESC, variety_name ASC
    ''')
    seeds = cursor.fetchall()

    conn.close()

    # Create export directory
    export_dir = Path(EXPORT_PATH)
    export_dir.mkdir(parents=True, exist_ok=True)

    # Write text file
    filename = export_dir / f"seed_inventory_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("Seed Inventory\n")
        f.write(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total seeds: {len(seeds)}\n")
        f.write("=" * 80 + "\n\n")

        for seed in seeds:
            f.write(f"ID: {seed['id']}\n")
            f.write(f"Variety: {seed['variety_name']}\n")
            f.write(f"Crop Type: {seed['crop_type']}\n")
            f.write(f"Year Saved: {seed['year_saved']}\n")
            f.write(f"Source: {seed['source'] or 'Not specified'}\n")

            if seed['quantity_grams']:
                f.write(f"Quantity: {seed['quantity_grams']}g\n")

            if seed['germination_pct']:
                f.write(f"Germination: {seed['germination_pct']:.0f}%\n")

            if seed['location_stored']:
                f.write(f"Location: {seed['location_stored']}\n")

            if seed['container_type']:
                f.write(f"Container: {seed['container_type']}\n")

            if seed['last_tested']:
                f.write(f"Last Tested: {seed['last_tested'][:10]}\n")

            if seed['notes']:
                f.write(f"Notes: {seed['notes']}\n")

            f.write("\n" + "-" * 80 + "\n\n")

    print(f"\n✓ Exported {len(seeds)} seeds to {filename}")
    return filename


def main():
    """Main entry point"""
    import sys

    format_type = EXPORT_FORMAT

    if len(sys.argv) > 1:
        format_type = sys.argv[1].lower()

    print("=== Export Seed Inventory ===\n")

    if format_type == 'json':
        export_json()
    elif format_type == 'csv':
        export_csv()
    elif format_type == 'txt' or format_type == 'text':
        export_text()
    else:
        print(f"Unknown format: {format_type}")
        print("Available formats: json, csv, txt")
        return

    print(f"\nExport location: {EXPORT_PATH}")


if __name__ == '__main__':
    main()
