#!/usr/bin/env python3
"""
Germination Test - Record and manage germination tests
"""

import sqlite3
import os
import sys
from datetime import datetime

# Configuration
DB_PATH = os.environ.get('SEED_DB_PATH', '/opt/seed-sovereignty/seeds.db')


def get_connection():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def list_seeds():
    """List seeds available for testing"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT id, variety_name, crop_type, year_saved, germination_pct, last_tested
        FROM seeds
        ORDER BY variety_name ASC
    ''')

    seeds = cursor.fetchall()
    conn.close()

    print("\n=== Seeds Available for Testing ===\n")
    print(f"{'ID':<5} {'Variety':<25} {'Crop':<15} {'Year':<6} {'Germ%':<7} {'Last Test':<12}")
    print("-" * 80)

    for seed in seeds:
        germ = f"{seed['germination_pct']:.0f}%" if seed['germination_pct'] else "-"
        last_test = seed['last_tested'][:10] if seed['last_tested'] else "-"

        print(f"{seed['id']:<5} {seed['variety_name']:<25} {seed['crop_type']:<15} "
              f"{seed['year_saved']:<6} {germ:<7} {last_test:<12}")

    return seeds


def record_test():
    """Record germination test results"""
    print("\n=== Record Germination Test ===\n")

    # List available seeds
    seeds = list_seeds()

    if not seeds:
        print("\nNo seeds found in inventory")
        return

    # Get seed selection
    seed_id = input("\nEnter seed ID to test: ").strip()

    try:
        seed_id = int(seed_id)
    except ValueError:
        print("Error: Invalid seed ID")
        return

    # Get test details
    seeds_tested = input("Number of seeds tested (10-25 recommended): ").strip()
    try:
        seeds_tested = int(seeds_tested)
        if seeds_tested < 1:
            print("Error: Must test at least 1 seed")
            return
    except ValueError:
        print("Error: Invalid number")
        return

    seeds_germinated = input("Number of seeds that germinated: ").strip()
    try:
        seeds_germinated = int(seeds_germinated)
        if seeds_germinated < 0 or seeds_germinated > seeds_tested:
            print(f"Error: Germinated seeds must be between 0 and {seeds_tested}")
            return
    except ValueError:
        print("Error: Invalid number")
        return

    # Calculate percentage
    germination_pct = (seeds_germinated / seeds_tested) * 100

    # Get optional details
    temp = input(f"Temperature during test (°C) [{22}]: ").strip()
    temp_celsius = float(temp) if temp else 22

    days = input(f"Days until germination counted [{10}]: ").strip()
    conditions_days = int(days) if days else 10

    notes = input("Notes (optional): ").strip() or None

    # Record test
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO germination_tests
        (seed_id, test_date, seeds_tested, seeds_germinated,
         germination_pct, conditions_temp_celsius, conditions_days, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (seed_id, datetime.now(), seeds_tested, seeds_germinated,
          germination_pct, temp_celsius, conditions_days, notes))

    # Update seed record with latest germination
    cursor.execute('''
        UPDATE seeds
        SET germination_pct = ?, last_tested = ?
        WHERE id = ?
    ''', (germination_pct, datetime.now(), seed_id))

    conn.commit()
    conn.close()

    # Display results
    print("\n=== Test Results ===\n")
    print(f"Seeds tested: {seeds_tested}")
    print(f"Seeds germinated: {seeds_germinated}")
    print(f"Germination rate: {germination_pct:.1f}%")

    # Provide recommendation
    if germination_pct >= 90:
        print("\n✓ Excellent germination - plant normally")
    elif germination_pct >= 75:
        print("\n✓ Good germination - plant normally")
    elif germination_pct >= 50:
        print("\n⚠ Fair germination - consider increasing seeding rate")
    else:
        print("\n✗ Poor germination - consider replacing seed")


def view_test_history():
    """View germination test history"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT gt.id, s.variety_name, gt.test_date, gt.seeds_tested,
               gt.seeds_germinated, gt.germination_pct, gt.conditions_temp_celsius,
               gt.conditions_days
        FROM germination_tests gt
        JOIN seeds s ON gt.seed_id = s.id
        ORDER BY gt.test_date DESC
        LIMIT 20
    ''')

    tests = cursor.fetchall()
    conn.close()

    if not tests:
        print("\nNo germination tests found")
        return

    print("\n=== Germination Test History ===\n")
    print(f"{'ID':<5} {'Variety':<25} {'Date':<12} {'Tested':<8} {'Germ':<6} "
          f"{'%':<6} {'Temp':<6} {'Days':<5}")
    print("-" * 80)

    for test in tests:
        test_date = test['test_date'][:10]
        temp = f"{test['conditions_temp_celsius']}°C" if test['conditions_temp_celsius'] else "-"

        print(f"{test['id']:<5} {test['variety_name']:<25} {test_date:<12} "
              f"{test['seeds_tested']:<8} {test['seeds_germinated']:<6} "
              f"{test['germination_pct']:<6.1f} {temp:<6} {test['conditions_days']:<5}")


def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == 'record':
            record_test()
        elif command == 'history':
            view_test_history()
        elif command == 'list':
            list_seeds()
        else:
            print(f"Unknown command: {command}")
            print("Usage: python3 germination_test.py [record|history|list]")
    else:
        print("=== Germination Test Manager ===")
        print("\nOptions:")
        print("  1. Record new test")
        print("  2. View test history")
        print("  3. List seeds")

        choice = input("\nSelect option (1-3): ").strip()

        if choice == '1':
            record_test()
        elif choice == '2':
            view_test_history()
        elif choice == '3':
            list_seeds()
        else:
            print("Invalid option")


if __name__ == '__main__':
    main()
