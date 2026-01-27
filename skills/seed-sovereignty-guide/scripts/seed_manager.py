#!/usr/bin/env python3
"""
Seed Manager - Manage seed inventory
"""

import sqlite3
import os
import sys
from datetime import datetime
from pathlib import Path

# Configuration
DB_PATH = os.environ.get('SEED_DB_PATH', '/opt/seed-sovereignty/seeds.db')


def get_connection():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def add_seed():
    """Add new seed entry to database"""
    print("\n=== Add New Seed Entry ===\n")

    variety = input("Variety name: ").strip()
    if not variety:
        print("Error: Variety name is required")
        return

    crop_type = input("Crop type (tomato, beans, corn, etc.): ").strip().lower()
    year_saved = input("Year saved (e.g., 2025): ").strip()
    source = input("Source (your garden, exchange, purchased): ").strip() or None
    quantity = input("Quantity (grams): ").strip() or None
    location = input("Storage location (e.g., refrigerator, freezer): ").strip() or None
    container = input("Container type (jar, bag, envelope): ").strip() or None
    notes = input("Notes (drought resistant, early maturity, etc.): ").strip() or None

    try:
        year_saved = int(year_saved)
    except ValueError:
        print("Error: Invalid year")
        return

    if quantity:
        try:
            quantity = float(quantity)
        except ValueError:
            print("Error: Invalid quantity")
            return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO seeds
        (variety_name, crop_type, year_saved, source, quantity_grams,
         location_stored, container_type, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (variety, crop_type, year_saved, source, quantity, location, container, notes))

    seed_id = cursor.lastrowid
    conn.commit()
    conn.close()

    print(f"\n✓ Seed added successfully (ID: {seed_id})")
    print(f"  Variety: {variety}")
    print(f"  Crop: {crop_type}")
    print(f"  Year: {year_saved}")


def list_seeds():
    """List all seeds in inventory"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id, variety_name, crop_type, year_saved, source,
               quantity_grams, germination_pct, location_stored, last_tested
        FROM seeds
        ORDER BY year_saved DESC, variety_name ASC
    ''')

    seeds = cursor.fetchall()
    conn.close()

    if not seeds:
        print("\nNo seeds found in inventory")
        return

    print("\n=== Seed Inventory ===\n")
    print(f"{'ID':<5} {'Variety':<25} {'Crop':<15} {'Year':<6} {'Qty':<8} {'Germ%':<7} {'Last Test':<12}")
    print("-" * 80)

    for seed in seeds:
        qty = f"{seed['quantity_grams']:.1f}g" if seed['quantity_grams'] else "-"
        germ = f"{seed['germination_pct']:.0f}%" if seed['germination_pct'] else "-"
        last_test = seed['last_tested'][:10] if seed['last_tested'] else "-"

        print(f"{seed['id']:<5} {seed['variety_name']:<25} {seed['crop_type']:<15} "
              f"{seed['year_saved']:<6} {qty:<8} {germ:<7} {last_test:<12}")

    print(f"\nTotal seeds: {len(seeds)}")


def update_seed():
    """Update existing seed entry"""
    print("\n=== Update Seed Entry ===\n")

    seed_id = input("Enter seed ID to update: ").strip()

    try:
        seed_id = int(seed_id)
    except ValueError:
        print("Error: Invalid seed ID")
        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM seeds WHERE id = ?', (seed_id,))
    seed = cursor.fetchone()

    if not seed:
        print(f"Error: Seed with ID {seed_id} not found")
        conn.close()
        return

    print(f"\nCurrent values:")
    print(f"  Variety: {seed['variety_name']}")
    print(f"  Crop type: {seed['crop_type']}")
    print(f"  Year saved: {seed['year_saved']}")
    print(f"  Source: {seed['source']}")
    print(f"  Quantity: {seed['quantity_grams']}g" if seed['quantity_grams'] else "  Quantity: -")
    print(f"  Location: {seed['location_stored']}")
    print(f"  Container: {seed['container_type']}")
    print(f"  Notes: {seed['notes']}")
    print(f"  Germination: {seed['germination_pct']}%" if seed['germination_pct'] else "  Germination: -")

    print("\nEnter new values (press Enter to keep current):")

    variety = input(f"Variety [{seed['variety_name']}]: ").strip() or seed['variety_name']
    crop_type = input(f"Crop type [{seed['crop_type']}]: ").strip().lower() or seed['crop_type']
    year_input = input(f"Year saved [{seed['year_saved']}]: ").strip()
    year_saved = int(year_input) if year_input else seed['year_saved']
    source = input(f"Source [{seed['source'] or '-'}]: ").strip() or seed['source']
    qty_input = input(f"Quantity [{seed['quantity_grams'] or '-'}]: ").strip()
    quantity = float(qty_input) if qty_input else seed['quantity_grams']
    location = input(f"Location [{seed['location_stored'] or '-'}]: ").strip() or seed['location_stored']
    container = input(f"Container [{seed['container_type'] or '-'}]: ").strip() or seed['container_type']
    notes = input(f"Notes [{seed['notes'] or '-'}]: ").strip() or seed['notes']

    cursor.execute('''
        UPDATE seeds
        SET variety_name = ?, crop_type = ?, year_saved = ?, source = ?,
            quantity_grams = ?, location_stored = ?, container_type = ?, notes = ?
        WHERE id = ?
    ''', (variety, crop_type, year_saved, source, quantity, location, container, notes, seed_id))

    conn.commit()
    conn.close()

    print(f"\n✓ Seed {seed_id} updated successfully")


def remove_seed():
    """Remove seed entry from database"""
    print("\n=== Remove Seed Entry ===\n")

    seed_id = input("Enter seed ID to remove: ").strip()

    try:
        seed_id = int(seed_id)
    except ValueError:
        print("Error: Invalid seed ID")
        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT variety_name, crop_type FROM seeds WHERE id = ?', (seed_id,))
    seed = cursor.fetchone()

    if not seed:
        print(f"Error: Seed with ID {seed_id} not found")
        conn.close()
        return

    print(f"\nSeed to remove:")
    print(f"  Variety: {seed['variety_name']}")
    print(f"  Crop: {seed['crop_type']}")

    confirm = input("\nConfirm removal? (y/N): ").strip().lower()
    if confirm != 'y':
        print("Removal cancelled")
        conn.close()
        return

    cursor.execute('DELETE FROM seeds WHERE id = ?', (seed_id,))
    conn.commit()
    conn.close()

    print(f"\n✓ Seed {seed_id} removed successfully")


def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == 'add':
            add_seed()
        elif command == 'list':
            list_seeds()
        elif command == 'update':
            update_seed()
        elif command == 'remove':
            remove_seed()
        else:
            print(f"Unknown command: {command}")
            print("Usage: python3 seed_manager.py [add|list|update|remove]")
    else:
        print("Usage: python3 seed_manager.py [add|list|update|remove]")


if __name__ == '__main__':
    main()
