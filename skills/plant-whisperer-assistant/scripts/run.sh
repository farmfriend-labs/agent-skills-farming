#!/bin/bash

# run.sh
# Start Plant Whisperer Assistant service

set -e

# Load environment variables
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Source .env if it exists
if [[ -f "$PROJECT_ROOT/.env" ]]; then
    set -a
    source "$PROJECT_ROOT/.env"
    set +a
fi

# Configuration with defaults
ANALYSIS_MODE="${ANALYSIS_MODE:-standard}"
LOG_LEVEL="${LOG_LEVEL:-info}"
LOG_FILE="${LOG_FILE:-/var/log/plant-whisperer.log}"
PLANT_DB_PATH="${PLANT_DB_PATH:-/opt/plant-whisperer/plants.db}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=========================================="
echo "Plant Whisperer Assistant - Starting"
echo "=========================================="
echo ""

# Check dependencies
echo "Checking dependencies..."
missing_deps=()

command -v python3 >/dev/null 2>&1 || missing_deps+=("python3")

if [[ ${#missing_deps[@]} -gt 0 ]]; then
    echo -e "${RED}Error: Missing dependencies:${NC}"
    for dep in "${missing_deps[@]}"; do
        echo "  - $dep"
    done
    echo ""
    echo "Run 'scripts/setup.sh' to install dependencies"
    exit 1
fi

# Check Python dependencies
echo "Checking Python dependencies..."
python3 -c "import cv2, numpy, PIL, requests, yaml" 2>/dev/null || {
    echo -e "${RED}Error: Python dependencies missing${NC}"
    echo "Run 'scripts/setup.sh' to install dependencies"
    exit 1
}

echo -e "${GREEN}Dependencies OK${NC}"
echo ""

# Check database
echo "Checking plant database: $PLANT_DB_PATH"
if [[ ! -f "$PLANT_DB_PATH" ]]; then
    echo -e "${YELLOW}Warning: Database not found${NC}"
    echo "Run 'python3 scripts/init_database.py' to create database"
    exit 1
fi
echo -e "${GREEN}Database found${NC}"

# Create log directory if needed
LOG_DIR=$(dirname "$LOG_FILE")
if [[ ! -d "$LOG_DIR" ]]; then
    echo "Creating log directory: $LOG_DIR"
    sudo mkdir -p "$LOG_DIR"
    sudo chown $USER:$USER "$LOG_DIR"
fi

# Display configuration
echo ""
echo "=========================================="
echo "Configuration"
echo "=========================================="
echo "  Analysis Mode: $ANALYSIS_MODE"
echo "  Log Level: $LOG_LEVEL"
echo "  Log File: $LOG_FILE"
echo "  Database: $PLANT_DB_PATH"
echo "=========================================="
echo ""

# Start service
echo "Starting Plant Whisperer Assistant..."
echo "Press Ctrl+C to stop"
echo ""

# Start Python monitoring script
python3 "$SCRIPT_DIR/monitor.py" \
    --mode "$ANALYSIS_MODE" \
    --log-level "$LOG_LEVEL" \
    --log-file "$LOG_FILE" \
    --database "$PLANT_DB_PATH"

echo ""
echo -e "${GREEN}Service stopped${NC}"
