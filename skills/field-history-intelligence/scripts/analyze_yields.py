#!/usr/bin/env python3
"""
Field History Intelligence - Yield Analysis Script
Analyze yield trends and patterns from historical data
"""

import sqlite3
import argparse
import sys
from datetime import datetime, timedelta

def analyze_yields(conn, field_name=None, years=None):
    """Analyze yield data from database"""
    cursor = conn.cursor()

    # Build query
    query = """
        SELECT
            f.name AS field_name,
            s.year,
            h.variety,
            h.yield,
            h.moisture,
            h.test_weight,
            p.planting_date,
            h.harvest_date
        FROM harvest h
        JOIN fields f ON h.field_id = f.id
        JOIN seasons s ON h.season_id = s.id
        LEFT JOIN planting p ON h.field_id = p.field_id AND h.season_id = p.season_id
        WHERE h.yield IS NOT NULL
    """
    params = []

    if field_name:
        query += " AND f.name = ?"
        params.append(field_name)

    if years:
        query += f" AND s.year IN ({','.join(['?'] * len(years))})"
        params.extend(years)

    query += " ORDER BY f.name, s.year DESC"

    cursor.execute(query, params)
    results = cursor.fetchall()

    if not results:
        print("No yield data found")
        return

    # Print header
    print("\n" + "="*120)
    print("YIELD ANALYSIS REPORT")
    print("="*120)
    print(f"{'Field':<20} {'Year':<6} {'Variety':<20} {'Yield':<10} {'Moisture':<10} {'Planting':<12} {'Harvest':<12}")
    print("-"*120)

    # Print results
    total_yield = 0
    total_records = 0

    for row in results:
        field_name, year, variety, yield_val, moisture, test_weight, planting_date, harvest_date = row
        print(f"{field_name:<20} {year:<6} {variety:<20} {yield_val:<10.1f} {moisture:<10.1f} {planting_date or 'N/A':<12} {harvest_date:<12}")
        total_yield += yield_val
        total_records += 1

    # Print summary
    print("-"*120)
    if total_records > 0:
        avg_yield = total_yield / total_records
        print(f"Average Yield: {avg_yield:.1f} bu/ac ({total_records} records)")
    print("="*120)

    # Analyze trends
    if field_name and total_records >= 3:
        analyze_field_trend(conn, field_name)

def analyze_field_trend(conn, field_name):
    """Analyze yield trend for a specific field"""
    cursor = conn.cursor()

    query = """
        SELECT s.year, AVG(h.yield) as avg_yield, COUNT(*) as variety_count
        FROM harvest h
        JOIN fields f ON h.field_id = f.id
        JOIN seasons s ON h.season_id = s.id
        WHERE f.name = ? AND h.yield IS NOT NULL
        GROUP BY s.year
        ORDER BY s.year DESC
        LIMIT 10
    """

    cursor.execute(query, (field_name,))
    results = cursor.fetchall()

    if len(results) >= 3:
        print(f"\n{field_name} - Yield Trend (Last 10 years):")
        print("-"*40)

        # Calculate trend
        years = [r[0] for r in reversed(results)]
        yields = [r[1] for r in reversed(results)]

        # Simple linear trend calculation
        if len(years) > 1:
            n = len(years)
            sum_x = sum(years)
            sum_y = sum(yields)
            sum_xy = sum(x * y for x, y in zip(years, yields))
            sum_x2 = sum(x**2 for x in years)

            slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x**2)
            intercept = (sum_y - slope * sum_x) / n

            print(f"Trend: {slope:.1f} bu/ac/year")

            if slope > 2:
                print("Trend: POSITIVE (improving)")
            elif slope < -2:
                print("Trend: NEGATIVE (declining)")
            else:
                print("Trend: STABLE")

        print("\nYearly breakdown:")
        for year, avg_yield, count in results:
            print(f"  {year}: {avg_yield:.1f} bu/ac ({count} varieties)")

def main():
    parser = argparse.ArgumentParser(
        description='Analyze yield trends from field history'
    )
    parser.add_argument(
        '--database',
        default='/opt/field-history/field-data.db',
        help='Path to SQLite database'
    )
    parser.add_argument(
        '--field',
        help='Field name to analyze (default: all fields)'
    )
    parser.add_argument(
        '--years',
        nargs='+',
        type=int,
        help='Years to analyze (default: all years)'
    )

    args = parser.parse_args()

    # Connect to database
    try:
        conn = sqlite3.connect(args.database)
    except Exception as e:
        print(f"Error connecting to database: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        analyze_yields(conn, args.field, args.years)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        conn.close()
        sys.exit(1)

    conn.close()

if __name__ == '__main__':
    main()
