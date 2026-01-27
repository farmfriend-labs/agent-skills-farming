#!/usr/bin/env python3
"""
Viability Checker - Check seed viability and recommend replacement
"""

import sqlite3
import os
from datetime import datetime, timedelta

# Configuration
DB_PATH = os.environ.get('SEED_DB_PATH', '/opt/seed-sovereignty/seeds.db')
MINIMUM_GERMINATION_PCT = float(os.environ.get('MINIMUM_GERMINATION_PCT', 70))
RECOMMEND_REPLACEMENT_YEARS = int(os.environ.get('RECOMMEND_REPLACEMENT_YEARS', 4))


def get_connection():
    """Get database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_variety_characteristics(conn, crop_type):
    """Get default viability years for crop type"""
    cursor = conn.cursor()

    # Default viability years by crop
    viability_map = {
        'tomato': 4,
        'beans': 3,
        'peas': 3,
        'lettuce': 2,
        'corn': 1,
        'squash': 4,
        'cucumber': 5,
        'melon': 5,
        'pepper': 3,
        'eggplant': 4,
        'beets': 4,
        'carrots': 3,
        'onions': 1,
        'cabbage': 4,
        'broccoli': 4,
        'kale': 4,
    }

    return viability_map.get(crop_type, 3)


def check_viability():
    """Check all seeds for viability"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM seeds ORDER BY variety_name ASC')
    seeds = cursor.fetchall()

    if not seeds:
        print("\nNo seeds found in inventory")
        conn.close()
        return

    print("\n=== Seed Viability Check ===\n")

    current_year = datetime.now().year
    issues = []

    for seed in seeds:
        age = current_year - seed['year_saved']
        viability_years = get_variety_characteristics(conn, seed['crop_type'])

        # Check if seed is too old
        if age > viability_years:
            issues.append({
                'seed': seed,
                'issue': 'age',
                'severity': 'high',
                'message': f"Seed is {age} years old (max viability: {viability_years} years)"
            })
        elif age >= viability_years:
            issues.append({
                'seed': seed,
                'issue': 'age',
                'severity': 'medium',
                'message': f"Seed is {age} years old (approaching end of viability)"
            })

        # Check germination percentage
        if seed['germination_pct'] is not None:
            if seed['germination_pct'] < 50:
                issues.append({
                    'seed': seed,
                    'issue': 'germination',
                    'severity': 'high',
                    'message': f"Low germination rate: {seed['germination_pct']:.0f}%"
                })
            elif seed['germination_pct'] < MINIMUM_GERMINATION_PCT:
                issues.append({
                    'seed': seed,
                    'issue': 'germination',
                    'severity': 'medium',
                    'message': f"Marginal germination rate: {seed['germination_pct']:.0f}%"
                })

        # Check if recently tested
        if seed['last_tested']:
            last_test_date = datetime.fromisoformat(seed['last_tested'])
            days_since_test = (datetime.now() - last_test_date).days
            if days_since_test > 365:
                issues.append({
                    'seed': seed,
                    'issue': 'testing',
                    'severity': 'low',
                    'message': f"Last tested {days_since_test} days ago"
                })

    conn.close()

    # Display results
    if not issues:
        print("✓ All seeds appear to be viable and healthy\n")
        return

    print(f"Found {len(issues)} potential issues:\n")

    for issue in issues:
        seed = issue['seed']
        severity_icon = '✗' if issue['severity'] == 'high' else '⚠' if issue['severity'] == 'medium' else 'ℹ'

        print(f"{severity_icon} {seed['variety_name']} ({seed['crop_type']})")
        print(f"   Year: {seed['year_saved']} | "
              f"Germination: {seed['germination_pct']:.0f}%" if seed['germination_pct'] else f"   Year: {seed['year_saved']} | Germination: Not tested")
        print(f"   Issue: {issue['message']}")
        print()

    # Summary
    high_severity = sum(1 for i in issues if i['severity'] == 'high')
    medium_severity = sum(1 for i in issues if i['severity'] == 'medium')
    low_severity = sum(1 for i in issues if i['severity'] == 'low')

    print(f"Summary: {high_severity} high priority, {medium_severity} medium priority, {low_severity} low priority")

    # Recommendations
    if high_severity > 0:
        print("\nRecommendations:")
        print("  • Test germination for all high-priority seeds")
        print("  • Consider replacing seeds with low germination rates")
        print("  • Plan to save fresh seeds this season")


def get_replacement_recommendations():
    """Get seeds that should be replaced"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM seeds ORDER BY variety_name ASC')
    seeds = cursor.fetchall()

    current_year = datetime.now().year
    recommendations = []

    for seed in seeds:
        age = current_year - seed['year_saved']
        viability_years = get_variety_characteristics(conn, seed['crop_type'])

        # Recommend replacement if old or low germination
        if age > viability_years:
            recommendations.append({
                'seed': seed,
                'reason': f"Exceeded viable lifespan ({age}/{viability_years} years)",
                'priority': 'high'
            })
        elif seed['germination_pct'] and seed['germination_pct'] < MINIMUM_GERMINATION_PCT:
            recommendations.append({
                'seed': seed,
                'reason': f"Low germination rate ({seed['germination_pct']:.0f}%)",
                'priority': 'high'
            })

    conn.close()

    if not recommendations:
        print("\nNo replacement recommendations at this time\n")
        return

    print("\n=== Replacement Recommendations ===\n")

    for rec in recommendations:
        seed = rec['seed']
        priority_icon = '✗' if rec['priority'] == 'high' else '⚠'

        print(f"{priority_icon} {seed['variety_name']} ({seed['crop_type']})")
        print(f"   Reason: {rec['reason']}")
        print(f"   Source: {seed['source'] if seed['source'] else 'Not specified'}")
        print(f"   Quantity: {seed['quantity_grams']}g" if seed['quantity_grams'] else "   Quantity: Not specified")
        print()


def main():
    """Main entry point"""
    if len(__name__.split('.')) > 1:
        # Being imported
        return

    print("=== Seed Viability Checker ===")
    print("\nOptions:")
    print("  1. Check all seeds for viability")
    print("  2. Get replacement recommendations")

    choice = input("\nSelect option (1-2): ").strip()

    if choice == '1':
        check_viability()
    elif choice == '2':
        get_replacement_recommendations()
    else:
        print("Invalid option")


if __name__ == '__main__':
    main()
