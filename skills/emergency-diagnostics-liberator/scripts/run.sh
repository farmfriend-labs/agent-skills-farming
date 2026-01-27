#!/bin/bash

# run.sh
# Start emergency diagnostics session

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
DIAG_INTERFACE_TYPE="${DIAG_INTERFACE_TYPE:-obd2}"
DIAG_INTERFACE_PORT="${DIAG_INTERFACE_PORT:-/dev/ttyUSB0}"
DIAG_CAN_INTERFACE="${DIAG_CAN_INTERFACE:-can0}"
DIAG_BAUDRATE="${DIAG_BAUDRATE:-250000}"
DIAG_PROTOCOL="${DIAG_PROTOCOL:-auto}"
DIAG_MANUFACTURER="${DIAG_MANUFACTURER:-auto}"
CODE_DB_PATH="${CODE_DB_PATH:-/opt/emergency-diagnostics/codes.db}"
OFFLINE_MODE="${OFFLINE_MODE:-true}"
DIAG_LOG_LEVEL="${DIAG_LOG_LEVEL:-info}"
DIAG_LOG_FILE="${DIAG_LOG_FILE:-/var/log/emergency-diagnostics.log}"
DIAG_REPORT_DIR="${DIAG_REPORT_DIR:-/var/log/emergency-diagnostics/reports}"
SAFETY_OVERRIDE_DISABLED="${SAFETY_OVERRIDE_DISABLED:-true}"
REQUIRE_CONFIRMATION="${REQUIRE_CONFIRMATION:-true}"
WARN_BEFORE_CLEAR="${WARN_BEFORE_CLEAR:-true}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=========================================="
echo "Emergency Diagnostics Liberator"
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
    echo "Install with: sudo apt-get install ${missing_deps[*]}"
    exit 1
fi

# Check Python dependencies
echo "Checking Python dependencies..."
python3 -c "import obd; import can; import sqlite3; import pandas" 2>/dev/null || {
    echo -e "${YELLOW}Warning: Python dependencies may be missing${NC}"
    echo "Install with: pip3 install python-obd python-can pandas"
    echo "Continuing anyway..."
}

echo -e "${GREEN}Dependencies OK${NC}"
echo ""

# Check code database
echo "Checking code database: $CODE_DB_PATH"
if [[ ! -f "$CODE_DB_PATH" ]]; then
    echo -e "${YELLOW}Warning: Code database not found${NC}"
    echo "Run 'python3 scripts/setup-database.py' to create database"
    echo ""
    read -p "Create database now? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        python3 "$SCRIPT_DIR/setup-database.py"
    else
        echo "Cannot continue without code database"
        exit 1
    fi
else
    echo -e "${GREEN}Code database found${NC}"
fi

# Check interface based on type
if [[ "$DIAG_INTERFACE_TYPE" == "obd2" ]]; then
    echo "Checking OBD-II port: $DIAG_INTERFACE_PORT"
    if [[ ! -e "$DIAG_INTERFACE_PORT" ]]; then
        echo -e "${RED}Error: OBD-II port not found${NC}"
        echo "Available ports:"
        ls /dev/ttyUSB* 2>/dev/null || ls /dev/ttyACM* 2>/dev/null || echo "  None found"
        echo ""
        echo "Connect OBD-II adapter and update DIAG_INTERFACE_PORT in .env"
        exit 1
    else
        echo -e "${GREEN}OBD-II port found${NC}"
    fi
elif [[ "$DIAG_INTERFACE_TYPE" == "can" ]]; then
    echo "Checking CAN interface: $DIAG_CAN_INTERFACE"
    if ! ip link show "$DIAG_CAN_INTERFACE" &>/dev/null; then
        echo -e "${RED}Error: CAN interface not found${NC}"
        echo "Available interfaces:"
        ip link show | grep -E '^[0-9]+:' | awk '{print "  " $2}' | sed 's/:$//'
        echo ""
        echo "Create CAN interface or update DIAG_CAN_INTERFACE in .env"
        exit 1
    else
        echo -e "${GREEN}CAN interface found${NC}"
    fi
fi

# Display configuration
echo ""
echo "=========================================="
echo "Configuration"
echo "=========================================="
echo "  Interface Type: $DIAG_INTERFACE_TYPE"
if [[ "$DIAG_INTERFACE_TYPE" == "obd2" ]]; then
    echo "  OBD-II Port: $DIAG_INTERFACE_PORT"
elif [[ "$DIAG_INTERFACE_TYPE" == "can" ]]; then
    echo "  CAN Interface: $DIAG_CAN_INTERFACE"
    echo "  CAN Baudrate: $DIAG_BAUDRATE"
fi
echo "  Protocol: $DIAG_PROTOCOL"
echo "  Manufacturer: $DIAG_MANUFACTURER"
echo "  Code Database: $CODE_DB_PATH"
echo "  Offline Mode: $OFFLINE_MODE"
echo "  Log Level: $DIAG_LOG_LEVEL"
echo "  Log File: $DIAG_LOG_FILE"
echo "  Report Dir: $DIAG_REPORT_DIR"
echo "  Safety Override Disabled: $SAFETY_OVERRIDE_DISABLED"
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

# Create log directory if needed
LOG_DIR=$(dirname "$DIAG_LOG_FILE")
if [[ ! -d "$LOG_DIR" ]]; then
    sudo mkdir -p "$LOG_DIR"
    sudo chown $USER:$USER "$LOG_DIR"
fi

# Start diagnostics
echo "Starting diagnostic session..."
echo "Type 'help' for available commands"
echo "Type 'quit' or Ctrl+C to exit"
echo ""

# Run Python diagnostics script
python3 "$SCRIPT_DIR/diagnostics.py" \
    --interface-type "$DIAG_INTERFACE_TYPE" \
    --port "$DIAG_INTERFACE_PORT" \
    --can-interface "$DIAG_CAN_INTERFACE" \
    --baudrate "$DIAG_BAUDRATE" \
    --protocol "$DIAG_PROTOCOL" \
    --manufacturer "$DIAG_MANUFACTURER" \
    --code-db "$CODE_DB_PATH" \
    --offline-mode "$OFFLINE_MODE" \
    --log-level "$DIAG_LOG_LEVEL" \
    --log-file "$DIAG_LOG_FILE" \
    --report-dir "$DIAG_REPORT_DIR" \
    --safety-override-disabled "$SAFETY_OVERRIDE_DISABLED" \
    --require-confirmation "$REQUIRE_CONFIRMATION" \
    --warn-before-clear "$WARN_BEFORE_CLEAR"

# Cleanup on exit
echo ""
echo -e "${GREEN}Diagnostic session ended${NC}"
