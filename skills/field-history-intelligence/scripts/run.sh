#!/bin/bash

# run.sh
# Main entry point for field history intelligence

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Source .env if it exists
if [[ -f "$PROJECT_ROOT/.env" ]]; then
    set -a
    source "$PROJECT_ROOT/.env"
    set +a
fi

# Configuration with defaults
DATABASE_PATH="${DATABASE_PATH:-/opt/field-history/field-data.db}"
BACKUP_PATH="${BACKUP_PATH:-/opt/field-history/backups}"
LOG_LEVEL="${LOG_LEVEL:-info}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "=========================================="
echo "Field History Intelligence"
echo "=========================================="
echo ""

# Check database
if [[ ! -f "$DATABASE_PATH" ]]; then
    echo -e "${RED}Error: Database not found${NC}"
    echo "Run 'python3 scripts/init_database.py' to create database"
    exit 1
fi

echo "Database: $DATABASE_PATH"
echo "Log Level: $LOG_LEVEL"
echo ""

# Show menu
echo "Available commands:"
echo ""
echo "  1. Analyze yields"
echo "  2. Analyze inputs"
echo "  3. Compare varieties"
echo "  4. Import data"
echo "  5. Generate report"
echo "  6. Visualize data"
echo "  7. Search records"
echo "  8. Backup database"
echo "  9. Interactive mode"
echo "  0. Exit"
echo ""

read -p "Select option (0-9): " choice

case $choice in
    1)
        read -p "Field name (leave blank for all): " field
        read -p "Years (space-separated, leave blank for all): " years
        python3 "$SCRIPT_DIR/analyze_yields.py" \
            --database "$DATABASE_PATH" \
            ${field:+--field "$field"} \
            ${years:+--years $years}
        ;;
    2)
        echo "Input analysis not yet implemented"
        echo "Use: python3 scripts/analyze_inputs.py"
        ;;
    3)
        echo "Variety comparison not yet implemented"
        echo "Use: python3 scripts/compare_varieties.py"
        ;;
    4)
        read -p "CSV file path: " csv_file
        read -p "Data type (planting, harvest, inputs): " data_type
        python3 "$SCRIPT_DIR/import_csv.py" \
            --database "$DATABASE_PATH" \
            "$csv_file" "$data_type"
        ;;
    5)
        echo "Report generation not yet implemented"
        echo "Use: python3 scripts/generate_report.py"
        ;;
    6)
        echo "Visualization not yet implemented"
        echo "Use: python3 scripts/visualize.py"
        ;;
    7)
        echo "Search not yet implemented"
        echo "Use: python3 scripts/search.py"
        ;;
    8)
        echo "Creating backup..."
        backup_file="$BACKUP_PATH/field-data-$(date +%Y%m%d-%H%M%S).db"
        mkdir -p "$BACKUP_PATH"
        cp "$DATABASE_PATH" "$backup_file"
        echo -e "${GREEN}Backup created: $backup_file${NC}"
        ;;
    9)
        echo "Interactive mode not yet implemented"
        ;;
    0)
        echo "Goodbye!"
        exit 0
        ;;
    *)
        echo -e "${RED}Invalid option${NC}"
        exit 1
        ;;
esac

echo ""
echo "Done!"
