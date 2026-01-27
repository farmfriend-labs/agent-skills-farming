#!/usr/bin/env python3
"""
ROI Calculator for Precision Agriculture
Calculate return on investment for precision practices
"""

import sys
import argparse
import sqlite3
import json
from datetime import datetime


def calculate_roi(db_path, season=None, fields=None):
    """Calculate ROI for precision practices

    Args:
        db_path: Path to database
        season: Year/season
        fields: Comma-separated list of field IDs

    Returns:
        dict: ROI results
    """

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Get input savings from variable rate application
    cursor.execute('''
        SELECT SUM((traditional_rate - precision_rate) * acres_treated * cost_per_unit) as savings
        FROM operations
        WHERE operation_type = 'application' AND precision_rate IS NOT NULL
    ''')

    input_savings = cursor.fetchone()['savings'] or 0

    # Get yield improvement
    cursor.execute('''
        SELECT AVG(precision_yield - traditional_yield) as avg_improvement
        FROM yield_data
        WHERE harvest_year = ?
    ''', (season,))

    yield_improvement = cursor.fetchone()['avg_improvement'] or 0

    # Get fuel savings from reduced overlap
    fuel_savings = 500  # Placeholder

    total_benefit = input_savings + yield_improvement + fuel_savings
    initial_investment = 10000  # Example: $10,000 total investment
    roi_percentage = (total_benefit / initial_investment) * 100

    results = {
        'season': season,
        'input_savings': input_savings,
        'yield_improvement': yield_improvement,
        'fuel_savings': fuel_savings,
        'total_benefit': total_benefit,
        'initial_investment': initial_investment,
        'roi_percentage': roi_percentage
    }

    return results


def print_roi_results(results):
    """Print ROI results

    Args:
        results: ROI calculation results
    """

    print("\n" + "=" * 60)
    print(f"PRECISION AGRICULTURE ROI - {results['season']}")
    print("=" * 60)

    print(f"\nSavings:")
    print(f"  Input savings:     ${results['input_savings']:,.2f}")
    print(f"  Yield improvement: ${results['yield_improvement']:,.2f}")
    print(f"  Fuel savings:      ${results['fuel_savings']:,.2f}")

    print(f"\nTotal Benefit:      ${results['total_benefit']:,.2f}")
    print(f"Initial Investment: ${results['initial_investment']:,.2f}")
    print(f"ROI:                {results['roi_percentage']:.1f}%")

    if results['total_benefit'] > results['initial_investment']:
        print(f"\nPayback achieved in {results['initial_investment'] / (results['total_benefit'] / 12):.1f} months")

    print("=" * 60)


def main():
    """Main function"""
    import os

    parser = argparse.ArgumentParser(
        description='Calculate ROI for precision agriculture'
    )
    parser.add_argument(
        '--season',
        default=str(datetime.now().year),
        help='Season/year for calculation'
    )
    parser.add_argument(
        '--fields',
        default='all',
        help='Comma-separated list of field IDs'
    )

    args = parser.parse_args()

    db_path = os.getenv('DB_PATH', '/var/lib/precision-ag/precision-ag.db')

    results = calculate_roi(
        db_path,
        season=args.season,
        fields=args.fields.split(',') if args.fields != 'all' else None
    )

    print_roi_results(results)

    # Export to JSON
    output_file = f"/var/lib/precision-ag/roi_{args.season}.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n✓ Results saved to {output_file}")


if __name__ == '__main__':
    main()
