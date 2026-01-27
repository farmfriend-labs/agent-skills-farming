#!/usr/bin/env python3
"""
Isolation Calculator - Calculate isolation requirements for varieties
"""

import sys


ISOLATION_DISTANCES = {
    'tomato': {
        'standard': 25,
        'high_risk': 100,
        'note': 'Potato-leaf varieties are more prone to crossing'
    },
    'pepper': {
        'standard': 500,
        'high_risk': 1000,
        'note': 'Readily cross-pollinates via insects'
    },
    'eggplant': {
        'standard': 500,
        'high_risk': 1000,
        'note': 'Similar to peppers for crossing risk'
    },
    'beans': {
        'standard': 20,
        'high_risk': 50,
        'note': 'Rarely crosses, but occasional bee activity'
    },
    'peas': {
        'standard': 50,
        'high_risk': 100,
        'note': 'Occasional bee pollination possible'
    },
    'lettuce': {
        'standard': 20,
        'high_risk': 50,
        'note': 'Mostly self-pollinating'
    },
    'corn': {
        'standard': 1320,
        'high_risk': 2640,
        'note': '1/4 mile minimum standard, 1/2 mile for high purity'
    },
    'squash': {
        'standard': 1320,
        'high_risk': 2640,
        'note': '1/2 mile minimum. Different species do not cross'
    },
    'cucumber': {
        'standard': 1320,
        'high_risk': 2640,
        'note': 'Similar to squash'
    },
    'melon': {
        'standard': 1320,
        'high_risk': 2640,
        'note': 'Similar to squash'
    },
    'beets': {
        'standard': 5280,
        'high_risk': 10560,
        'note': '1 mile minimum (biennial)'
    },
    'carrots': {
        'standard': 5280,
        'high_risk': 10560,
        'note': '1 mile minimum. Wild carrot (Queen Anne\'s Lace) crosses'
    },
    'onions': {
        'standard': 5280,
        'high_risk': 10560,
        'note': '1 mile minimum (biennial)'
    },
    'cabbage': {
        'standard': 5280,
        'high_risk': 10560,
        'note': '1 mile minimum. All brassicas cross'
    },
    'broccoli': {
        'standard': 5280,
        'high_risk': 10560,
        'note': '1 mile minimum. All brassicas cross'
    },
    'kale': {
        'standard': 5280,
        'high_risk': 10560,
        'note': '1 mile minimum. All brassicas cross'
    }
}


def calculate_isolation(crop_type, num_varieties, garden_size_sqft=None):
    """Calculate isolation requirements"""
    crop_type = crop_type.lower().strip()

    if crop_type not in ISOLATION_DISTANCES:
        print(f"\nSorry, no isolation data for '{crop_type}'")
        print(f"\nAvailable crops: {', '.join(sorted(ISOLATION_DISTANCES.keys()))}")
        return

    data = ISOLATION_DISTANCES[crop_type]

    print(f"\n=== Isolation Requirements: {crop_type.title()} ===\n")
    print(f"Standard isolation: {data['standard']} feet ({data['standard'] / 5280:.2f} miles)")
    print(f"High-purity isolation: {data['high_risk']} feet ({data['high_risk'] / 5280:.2f} miles)")
    print(f"\nNote: {data['note']}")

    if num_varieties > 1:
        print(f"\nWith {num_varieties} varieties:")
        print("  Option 1: Space varieties at required isolation distance")
        print("  Option 2: Use bagging or hand pollination for each variety")
        print("  Option 3: Grow only one variety per season")

    if garden_size_sqft:
        print(f"\nFor a {garden_size_sqft:,} sqft garden:")
        side_length = (garden_size_sqft ** 0.5)

        if data['standard'] > side_length:
            needed = data['standard'] - side_length
            print(f"  ⚠ Garden is too small for full isolation")
            print(f"    Need additional {needed:.0f} feet on each side")
            print(f"    Recommendation: Use bagging or grow one variety")
        else:
            print(f"  ✓ Garden is large enough for standard isolation")
            print(f"    Available spacing: {side_length - data['standard']:.0f} feet beyond required")


def main():
    """Main entry point"""
    print("=== Seed Isolation Calculator ===\n")

    crop_type = input("Enter crop type: ").strip().lower()

    if crop_type not in ISOLATION_DISTANCES:
        print(f"\nAvailable crops: {', '.join(sorted(ISOLATION_DISTANCES.keys()))}")
        return

    num_varieties = input("Number of varieties to grow (default 1): ").strip()
    num_varieties = int(num_varieties) if num_varieties else 1

    garden_size = input("Garden size in sqft (optional): ").strip()
    garden_size = int(garden_size) if garden_size else None

    calculate_isolation(crop_type, num_varieties, garden_size)


if __name__ == '__main__':
    main()
