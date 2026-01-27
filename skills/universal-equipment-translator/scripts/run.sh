#!/bin/bash

# run.sh
# Start equipment translator service

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
CAN_INTERFACE="${CAN_INTERFACE:-can0}"
TRANSLATION_MODE="${TRANSLATION_MODE:-iso11783}"
SAFETY_OVERRIDE_DISABLED="${SAFETY_OVERRIDE_DISABLED:-true}"
TRANSLATION_LOG_LEVEL="${TRANSLATION_LOG_LEVEL:-info}"
TRANSLATION_LOG_FILE="${TRANSLATION_LOG_FILE:-/var/log/equipment-translator.log}"
PROTOCOL_DB_PATH="${PROTOCOL_DB_PATH:-/opt/equipment-translator/protocols.db}"
OFFLINE_MODE="${OFFLINE_MODE:-true}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=========================================="
echo "Equipment Translator - Starting"
echo "=========================================="
echo ""

# Check dependencies
echo "Checking dependencies..."
missing_deps=()

command -v python3 >/dev/null 2>&1 || missing_deps+=("python3")
command -v can-utils >/dev/null 2>&1 || missing_deps+=("can-utils")

if [[ ${#missing_deps[@]} -gt 0 ]]; then
    echo -e "${RED}Error: Missing dependencies:${NC}"
    for dep in "${missing_deps[@]}"; do
        echo "  - $dep"
    done
    echo ""
    echo "Install with: sudo apt-get install ${missing_deps[*]}"
    exit 1
fi

# Check Python dependencies
echo "Checking Python dependencies..."
python3 -c "import can; import sqlite3" 2>/dev/null || {
    echo -e "${YELLOW}Warning: Python dependencies may be missing${NC}"
    echo "Install with: pip3 install python-can"
    echo "Continuing anyway..."
}

echo -e "${GREEN}Dependencies OK${NC}"
echo ""

# Create log directory
LOG_DIR=$(dirname "$TRANSLATION_LOG_FILE")
if [[ ! -d "$LOG_DIR" ]]; then
    echo "Creating log directory: $LOG_DIR"
    sudo mkdir -p "$LOG_DIR"
    sudo chown $USER:$USER "$LOG_DIR"
fi

# Check CAN interface
echo "Checking CAN interface: $CAN_INTERFACE"
if ! ip link show "$CAN_INTERFACE" &>/dev/null; then
    echo -e "${YELLOW}Warning: CAN interface $CAN_INTERFACE not found${NC}"
    echo "Run 'scripts/setup.sh' to create/configure interface"
    echo ""
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo -e "${GREEN}CAN interface found${NC}"
fi

# Check protocol database
echo "Checking protocol database: $PROTOCOL_DB_PATH"
if [[ ! -f "$PROTOCOL_DB_PATH" ]]; then
    echo -e "${YELLOW}Warning: Protocol database not found${NC}"
    echo "Run 'scripts/setup-database.py' to create database"
    echo ""
    read -p "Create database now? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        python3 "$SCRIPT_DIR/setup-database.py"
    fi
fi

# Display configuration
echo ""
echo "=========================================="
echo "Configuration"
echo "=========================================="
echo "  CAN Interface: $CAN_INTERFACE"
echo "  Translation Mode: $TRANSLATION_MODE"
echo "  Safety Override Disabled: $SAFETY_OVERRIDE_DISABLED"
echo "  Log Level: $TRANSLATION_LOG_LEVEL"
echo "  Log File: $TRANSLATION_LOG_FILE"
echo "  Protocol Database: $PROTOCOL_DB_PATH"
echo "  Offline Mode: $OFFLINE_MODE"
echo "=========================================="
echo ""

# Safety check
if [[ "$SAFETY_OVERRIDE_DISABLED" != "true" ]]; then
    echo -e "${RED}WARNING: Safety overrides are ENABLED${NC}"
    echo "This is NOT recommended for production use"
    echo ""
    read -p "Continue? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted by user"
        exit 1
    fi
fi

# Start translation service
echo "Starting translation service..."
echo "Press Ctrl+C to stop"
echo ""

# Start Python translation script
python3 "$SCRIPT_DIR/translator.py" \
    --interface "$CAN_INTERFACE" \
    --mode "$TRANSLATION_MODE" \
    --log-level "$TRANSLATION_LOG_LEVEL" \
    --log-file "$TRANSLATION_LOG_FILE" \
    --protocol-db "$PROTOCOL_DB_PATH" \
    --offline-mode "$OFFLINE_MODE" \
    --safety-override-disabled "$SAFETY_OVERRIDE_DISABLED"

# Cleanup on exit
echo ""
echo -e "${GREEN}Translator stopped${NC}"
