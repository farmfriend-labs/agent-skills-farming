#!/bin/bash

# setup.sh
# Initialize emergency diagnostics environment

set -e

# Configuration
CODE_DB_PATH="${CODE_DB_PATH:-/opt/emergency-diagnostics/codes.db}"
DIAG_LOG_FILE="${DIAG_LOG_FILE:-/var/log/emergency-diagnostics.log}"
DIAG_REPORT_DIR="${DIAG_REPORT_DIR:-/var/log/emergency-diagnostics/reports}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=========================================="
echo "Emergency Diagnostics Liberator - Setup"
echo "=========================================="
echo ""

# Check for Python 3.8+
echo "Checking Python version..."
if command -v python3 >/dev/null 2>&1; then
    PYTHON_VERSION=$(python3 --version | awk '{print $2}')
    echo "Found Python $PYTHON_VERSION"

    # Check version >= 3.8
    if python3 -c 'import sys; exit(0 if sys.version_info >= (3, 8) else 1)'; then
        echo -e "${GREEN}Python version OK (>= 3.8)${NC}"
    else
        echo -e "${RED}Error: Python 3.8 or higher required${NC}"
        exit 1
    fi
else
    echo -e "${RED}Error: Python 3 not found${NC}"
    echo "Install with: sudo apt-get install python3"
    exit 1
fi

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip3 install --user python-obd python-can pandas matplotlib reportlab 2>/dev/null || {
    echo -e "${YELLOW}Some dependencies may have failed${NC}"
    echo "Try: pip3 install python-obd python-can pandas matplotlib reportlab"
}

# Create directories
echo ""
echo "Creating directories..."

# Code DB directory
CODE_DB_DIR=$(dirname "$CODE_DB_PATH")
if [[ ! -d "$CODE_DB_DIR" ]]; then
    echo "Creating code DB directory: $CODE_DB_DIR"
    sudo mkdir -p "$CODE_DB_DIR"
    sudo chown $USER:$USER "$CODE_DB_DIR"
fi

# Log directory
LOG_DIR=$(dirname "$DIAG_LOG_FILE")
if [[ ! -d "$LOG_DIR" ]]; then
    echo "Creating log directory: $LOG_DIR"
    sudo mkdir -p "$LOG_DIR"
    sudo chown $USER:$USER "$LOG_DIR"
fi

# Report directory
if [[ ! -d "$DIAG_REPORT_DIR" ]]; then
    echo "Creating report directory: $DIAG_REPORT_DIR"
    sudo mkdir -p "$DIAG_REPORT_DIR"
    sudo chown $USER:$USER "$DIAG_REPORT_DIR"
fi

echo -e "${GREEN}Directories created${NC}"

# Initialize code database
echo ""
echo "Initializing diagnostic code database..."
python3 "$SCRIPT_DIR/setup-database.py" || {
    echo -e "${YELLOW}Warning: Database initialization may have issues${NC}"
    echo "Run manually: python3 scripts/setup-database.py"
}

# Check for CAN interface
echo ""
echo "Checking CAN interface..."
if command -v ip >/dev/null 2>&1; then
    if ip link show can0 &>/dev/null; then
        echo -e "${GREEN}CAN interface can0 found${NC}"
    else
        echo -e "${YELLOW}CAN interface can0 not found${NC}"
        echo "Create virtual interface for testing:"
        echo "  sudo ip link add dev can0 type vcan"
        echo "  sudo ip link set can0 up"
    fi
else
    echo -e "${YELLOW}ip command not found, skipping CAN check${NC}"
fi

# Check for serial ports
echo ""
echo "Checking for OBD-II serial ports..."
if ls /dev/ttyUSB* 1> /dev/null 2>&1 || ls /dev/ttyACM* 1> /dev/null 2>&1; then
    echo -e "${GREEN}Found serial ports:${NC}"
    ls /dev/ttyUSB* 2>/dev/null || ls /dev/ttyACM* 2>/dev/null
else
    echo -e "${YELLOW}No USB serial ports found${NC}"
    echo "Connect OBD-II adapter to use diagnostics"
fi

# Check udev rules for USB serial
echo ""
echo "Checking udev rules..."
if [[ -f /etc/udev/rules.d/99-obd2.rules ]]; then
    echo -e "${GREEN}OBD-II udev rules found${NC}"
else
    echo -e "${YELLOW}OBD-II udev rules not found${NC}"
    echo "Create with: sudo ./scripts/setup-udev.sh"
fi

echo ""
echo "=========================================="
echo -e "${GREEN}Setup Complete${NC}"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Connect OBD-II/CAN adapter to equipment"
echo "  2. Run 'scripts/run.sh' to start diagnostics"
echo "  3. Run 'scripts/test.sh' to verify setup"
echo ""
