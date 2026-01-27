#!/bin/bash

# run.sh
# Main entry point for seed sovereignty guide

set -e

# Configuration
SEED_DB_PATH="${SEED_DB_PATH:-/opt/seed-sovereignty/seeds.db}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if database exists
if [ ! -f "$SEED_DB_PATH" ]; then
    echo -e "${RED}Error: Database not found at $SEED_DB_PATH${NC}"
    echo "Please run setup.sh first"
    exit 1
fi

# Display menu
echo "=========================================="
echo "Seed Sovereignty Guide"
echo "=========================================="
echo ""
echo "Select an action:"
echo ""
echo "1. Add new seeds to inventory"
echo "2. View seed inventory"
echo "3. Record germination test"
echo "4. Check seed viability"
echo "5. Lookup crop information"
echo "6. Calculate isolation requirements"
echo "7. Export inventory"
echo "8. Monitor storage conditions"
echo "9. Update seed entry"
echo "10. Remove seed entry"
echo "q. Quit"
echo ""
read -p "Enter selection (1-10 or q): " choice

case $choice in
    1)
        python3 scripts/seed_manager.py add
        ;;
    2)
        python3 scripts/seed_manager.py list
        ;;
    3)
        python3 scripts/germination_test.py
        ;;
    4)
        python3 scripts/viability_checker.py
        ;;
    5)
        python3 scripts/crop_lookup.py
        ;;
    6)
        python3 scripts/isolation_calculator.py
        ;;
    7)
        python3 scripts/export_inventory.py
        ;;
    8)
        python3 scripts/storage_monitor.py
        ;;
    9)
        python3 scripts/seed_manager.py update
        ;;
    10)
        python3 scripts/seed_manager.py remove
        ;;
    q|Q)
        echo "Goodbye!"
        exit 0
        ;;
    *)
        echo -e "${RED}Invalid selection${NC}"
        exit 1
        ;;
esac
