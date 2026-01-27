#!/usr/bin/env python3
"""
Crop Lookup - Get crop-specific seed saving information
"""

import sqlite3
import os

# Configuration
DB_PATH = os.environ.get('SEED_DB_PATH', '/opt/seed-sovereignty/seeds.db')

# Crop information database
CROP_INFO = {
    'tomato': {
        'pollination_type': 'Self-pollinating',
        'isolation_distance': '25 feet (most varieties), 100+ feet for potato-leaf types',
        'min_population': '6-12 plants',
        'biennial': False,
        'processing_method': 'Fermentation method',
        'processing_steps': [
            'Scoop seeds into container with some pulp',
            'Add small amount of water, cover loosely',
            'Let ferment 2-3 days at room temperature',
            'Stir daily to release seeds from gel coating',
            'When good seeds sink and bad float, pour off top',
            'Rinse thoroughly, spread to dry on paper towels'
        ],
        'drying_time': '7-14 days',
        'viability_years': 4,
        'notes': 'Most tomatoes rarely cross-pollinate. Potato-leaf varieties are more prone to crossing.'
    },
    'beans': {
        'pollination_type': 'Self-pollinating',
        'isolation_distance': '10-20 feet',
        'min_population': '20-40 plants',
        'biennial': False,
        'processing_method': 'Threshing',
        'processing_steps': [
            'Allow pods to dry completely on the vine',
            'Harvest when pods are crispy and rattle',
            'Thresh by stomping or crushing pods in bag',
            'Winnow to remove pods and debris',
            'Dry thoroughly in well-ventilated area'
        ],
        'drying_time': '7-14 days',
        'viability_years': 3,
        'notes': 'Beans rarely cross-pollinate. Occasional bee activity may cause crossing.'
    },
    'peas': {
        'pollination_type': 'Self-pollinating',
        'isolation_distance': '50 feet',
        'min_population': '20-40 plants',
        'biennial': False,
        'processing_method': 'Threshing',
        'processing_steps': [
            'Allow pods to dry completely on the vine',
            'Harvest when pods are dry and brittle',
            'Thresh by threshing or crushing pods',
            'Winnow to remove pods',
            'Dry thoroughly'
        ],
        'drying_time': '7-14 days',
        'viability_years': 3,
        'notes': 'Occasional bee pollination can occur. Keep some distance from other pea varieties.'
    },
    'lettuce': {
        'pollination_type': 'Self-pollinating',
        'isolation_distance': '20 feet',
        'min_population': '12-20 plants',
        'biennial': False,
        'processing_method': 'Rubbing and winnowing',
        'processing_steps': [
            'Allow seedheads to fully fluff and dry on plant',
            'Harvest when seedheads are completely dry',
            'Rub seedheads to release seeds',
            'Winnow carefully to remove chaff',
            'Dry seeds thoroughly'
        ],
        'drying_time': '7-10 days',
        'viability_years': 2,
        'notes': 'Seeds are very small and light. Winnow gently to avoid losing seeds.'
    },
    'corn': {
        'pollination_type': 'Cross-pollinating',
        'isolation_distance': '1/4 mile minimum',
        'min_population': '100-200 plants',
        'biennial': False,
        'processing_method': 'Drying',
        'processing_steps': [
            'Allow ears to dry completely on the stalk',
            'Harvest when husks are dry and kernels are hard',
            'Remove kernels from cob by hand or mechanical means',
            'Dry thoroughly to 10-12% moisture',
            'Store in cool, dry conditions'
        ],
        'drying_time': '14-21 days',
        'viability_years': 1,
        'notes': 'Corn has very short viability (1-2 years). Plant fresh seed each season for best results.'
    },
    'squash': {
        'pollination_type': 'Cross-pollinating',
        'isolation_distance': '1/2 mile',
        'min_population': '6-12 plants',
        'biennial': False,
        'processing_method': 'Fermentation',
        'processing_steps': [
            'Cut open fully ripe fruit',
            'Scoop seeds into container',
            'Add water, let ferment 2-3 days',
            'Stir daily to separate seeds from pulp',
            'Rinse thoroughly when good seeds sink',
            'Dry completely'
        ],
        'drying_time': '7-14 days',
        'viability_years': 4,
        'notes': 'Summer squash (C. pepo) crosses with zucchini and pumpkins. Different species do not cross.'
    },
    'cucumber': {
        'pollination_type': 'Cross-pollinating',
        'isolation_distance': '1/2 mile',
        'min_population': '12-20 plants',
        'biennial': False,
        'processing_method': 'Fermentation',
        'processing_steps': [
            'Allow fruit to yellow and soften',
            'Cut open and scoop seeds',
            'Ferment for 2-3 days',
            'Rinse and dry completely',
            'Remove membrane from seeds'
        ],
        'drying_time': '7-14 days',
        'viability_years': 5,
        'notes': 'Cucumbers have excellent longevity. Properly stored seeds can last 5-10 years.'
    },
    'pepper': {
        'pollination_type': 'Cross-pollinating',
        'isolation_distance': '500 feet',
        'min_population': '6-10 plants',
        'biennial': False,
        'processing_method': 'Rinsing',
        'processing_steps': [
            'Allow fruits to fully ripen on plant',
            'Cut open ripe fruit',
            'Scrape out seeds',
            'Rinse to remove membrane',
            'Dry on paper towels',
            'Turn seeds daily to prevent mold'
        ],
        'drying_time': '7-10 days',
        'viability_years': 2,
        'notes': 'Peppers readily cross-pollinate. Isolate different varieties or bag flowers.'
    },
    'eggplant': {
        'pollination_type': 'Cross-pollinating',
        'isolation_distance': '500 feet',
        'min_population': '6-10 plants',
        'biennial': False,
        'processing_method': 'Rinsing',
        'processing_steps': [
            'Allow fruits to overripen past eating stage',
            'Cut open and scoop seeds',
            'Rub to remove pulp and membrane',
            'Rinse thoroughly',
            'Dry completely'
        ],
        'drying_time': '7-10 days',
        'viability_years': 4,
        'notes': 'Similar to peppers. Good longevity when properly stored.'
    },
    'beets': {
        'pollination_type': 'Biennial',
        'isolation_distance': '1 mile',
        'min_population': '16-32 plants',
        'biennial': True,
        'processing_method': 'Rubbing and winnowing',
        'processing_steps': [
            'Harvest roots in fall, select best specimens',
            'Store roots over winter in cool, dark location',
            'Replant roots in spring',
            'Allow seed stalks to mature second year',
            'Rub seedheads to release seeds',
            'Winnow and dry'
        ],
        'drying_time': '14-21 days',
        'viability_years': 4,
        'notes': 'Two-year cycle. Keep at least 16 roots for genetic diversity.'
    },
    'carrots': {
        'pollination_type': 'Biennial',
        'isolation_distance': '1 mile',
        'min_population': '32-64 plants',
        'biennial': True,
        'processing_method': 'Rubbing and winnowing',
        'processing_steps': [
            'Harvest roots in fall, select best specimens',
            'Store roots over winter',
            'Replant in spring',
            'Allow umbels to dry on plant',
            'Rub umbels to release seeds',
            'Winnow carefully (seeds are small)'
        ],
        'drying_time': '14-21 days',
        'viability_years': 3,
        'notes': 'Queen Anne\'s Lace is wild carrot and will cross. Keep well isolated.'
    },
    'onions': {
        'pollination_type': 'Biennial',
        'isolation_distance': '1 mile',
        'min_population': '20-50 plants',
        'biennial': True,
        'processing_method': 'Rubbing umbels',
        'processing_steps': [
            'Select best bulbs for seed saving',
            'Overwinter bulbs',
            'Replant in spring',
            'Allow seed heads to mature and dry',
            'Rub umbels to release black seeds',
            'Winnow and dry thoroughly'
        ],
        'drying_time': '14-21 days',
        'viability_years': 1,
        'notes': 'Onion seeds have short viability (1-2 years). Save fresh seed annually.'
    },
    'cabbage': {
        'pollination_type': 'Biennial',
        'isolation_distance': '1 mile',
        'min_population': '20-50 plants',
        'biennial': True,
        'processing_method': 'Threshing',
        'processing_steps': [
            'Harvest heads in fall',
            'Store roots/crowns over winter',
            'Replant in spring',
            'Allow seed pods to mature on plant',
            'Thresh pods to release seeds',
            'Winnow and dry'
        ],
        'drying_time': '14-21 days',
        'viability_years': 4,
        'notes': 'All brassicas cross readily. Isolate from other cabbage, broccoli, kale, etc.'
    },
    'broccoli': {
        'pollination_type': 'Biennial',
        'isolation_distance': '1 mile',
        'min_population': '20-50 plants',
        'biennial': True,
        'processing_method': 'Threshing',
        'processing_steps': [
            'Harvest main heads',
            'Allow side shoots to go to seed',
            'Let seed pods dry on plant',
            'Thresh pods to release seeds',
            'Winnow and dry'
        ],
        'drying_time': '14-21 days',
        'viability_years': 4,
        'notes': 'Crosses with all other brassicas. Requires strict isolation.'
    }
}


def lookup_crop(crop_name):
    """Look up crop information"""
    crop_name = crop_name.lower().strip()

    if crop_name not in CROP_INFO:
        print(f"\nSorry, no information available for '{crop_name}'")
        print("\nAvailable crops:")
        for crop in sorted(CROP_INFO.keys()):
            print(f"  • {crop}")
        return

    info = CROP_INFO[crop_name]

    print(f"\n=== Seed Saving Information: {crop_name.title()} ===\n")
    print(f"Pollination Type: {info['pollination_type']}")
    print(f"Isolation Distance: {info['isolation_distance']}")
    print(f"Minimum Population: {info['min_population']}")
    print(f"Biennial: {'Yes' if info['biennial'] else 'No'}")
    print(f"Processing Method: {info['processing_method']}")
    print(f"Viability: {info['viability_years']} years")
    print(f"\nProcessing Steps:")
    for i, step in enumerate(info['processing_steps'], 1):
        print(f"  {i}. {step}")
    print(f"\nNotes: {info['notes']}")


def list_all_crops():
    """List all available crops"""
    print("\n=== Available Crops ===\n")
    print("Self-pollinating:")
    for crop, info in sorted(CROP_INFO.items()):
        if not info['biennial'] and 'Self' in info['pollination_type']:
            print(f"  • {crop.title()}")

    print("\nCross-pollinating (annual):")
    for crop, info in sorted(CROP_INFO.items()):
        if not info['biennial'] and 'Cross' in info['pollination_type']:
            print(f"  • {crop.title()}")

    print("\nBiennial (two-year cycle):")
    for crop, info in sorted(CROP_INFO.items()):
        if info['biennial']:
            print(f"  • {crop.title()}")


def main():
    """Main entry point"""
    import sys

    if len(sys.argv) > 1:
        crop_name = ' '.join(sys.argv[1:])
        lookup_crop(crop_name)
    else:
        print("=== Crop Lookup ===")
        crop_name = input("\nEnter crop name (or 'list' to see all crops): ").strip()

        if crop_name.lower() == 'list':
            list_all_crops()
        else:
            lookup_crop(crop_name)


if __name__ == '__main__':
    main()
