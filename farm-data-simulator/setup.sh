#!/bin/bash

# setup.sh
# Farm Data Simulator - Setup and installation

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

SIMULATOR_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=========================================="
echo "Farm Data Simulator - Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
PYTHON_VERSION=$(python3 --version | awk '{print $2}')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [[ $PYTHON_MAJOR -lt 3 ]] || [[ $PYTHON_MAJOR -eq 3 && $PYTHON_MINOR -lt 8 ]]; then
    echo -e "${RED}Error: Python 3.8+ required${NC}"
    echo "Found: Python $PYTHON_VERSION"
    exit 1
fi

echo -e "${GREEN}Python $PYTHON_VERSION OK${NC}"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [[ ! -d "$SIMULATOR_DIR/venv" ]]; then
    python3 -m venv "$SIMULATOR_DIR/venv"
    echo -e "${GREEN}Virtual environment created${NC}"
else
    echo -e "${YELLOW}Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source "$SIMULATOR_DIR/venv/bin/activate"

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing Python dependencies..."
pip install -r "$SIMULATOR_DIR/requirements.txt"

echo -e "${GREEN}Dependencies installed${NC}"
echo ""

# Create output directories
echo "Creating output directories..."
mkdir -p "$SIMULATOR_DIR/outputs"
echo -e "${GREEN}Output directories created${NC}"
echo ""

# Create configuration files
echo "Initializing configuration files..."
if [[ ! -f "$SIMULATOR_DIR/config/can-bus.json" ]]; then
    cp "$SIMULATOR_DIR/config/can-bus.example.json" "$SIMULATOR_DIR/config/can-bus.json"
    echo "Created config/can-bus.json"
fi

if [[ ! -f "$SIMULATOR_DIR/config/sensors.json" ]]; then
    cp "$SIMULATOR_DIR/config/sensors.example.json" "$SIMULATOR_DIR/config/sensors.json"
    echo "Created config/sensors.json"
fi

if [[ ! -f "$SIMULATOR_DIR/config/markets.json" ]]; then
    cp "$SIMULATOR_DIR/config/markets.example.json" "$SIMULATOR_DIR/config/markets.json"
    echo "Created config/markets.json"
fi

if [[ ! -f "$SIMULATOR_DIR/config/weather.json" ]]; then
    cp "$SIMULATOR_DIR/config/weather.example.json" "$SIMULATOR_DIR/config/weather.json"
    echo "Created config/weather.json"
fi

if [[ ! -f "$SIMULATOR_DIR/config/equipment.json" ]]; then
    cp "$SIMULATOR_DIR/config/equipment.example.json" "$SIMULATOR_DIR/config/equipment.json"
    echo "Created config/equipment.json"
fi

echo -e "${GREEN}Configuration files initialized${NC}"
echo ""

# Make scripts executable
echo "Making scripts executable..."
chmod +x "$SIMULATOR_DIR/run.sh"
chmod +x "$SIMULATOR_DIR/simulator/"*.py 2>/dev/null || true
echo -e "${GREEN}Scripts executable${NC}"
echo ""

# Verify installation
echo "Verifying installation..."

# Check Python dependencies
python3 -c "import sys; sys.path.insert(0, 'venv/lib/python3.X/site-packages'); import can, requests, numpy, pandas, yaml" 2>/dev/null || {
    echo -e "${RED}Error: Some Python dependencies failed to import${NC}"
    echo "Please check requirements.txt and reinstall"
    exit 1
}

echo -e "${GREEN}Python dependencies OK${NC}"

# Check configuration files
CONFIG_OK=true
for config_file in can-bus.json sensors.json markets.json weather.json equipment.json; do
    if [[ ! -f "$SIMULATOR_DIR/config/$config_file" ]]; then
        echo -e "${RED}Error: Missing config/$config_file${NC}"
        CONFIG_OK=false
    fi
done

if $CONFIG_OK; then
    echo -e "${GREEN}Configuration files OK${NC}"
else
    echo -e "${YELLOW}Some configuration files missing${NC}"
    echo "Please run setup again"
    exit 1
fi

# Check output directory
if [[ -d "$SIMULATOR_DIR/outputs" ]]; then
    echo -e "${GREEN}Output directory OK${NC}"
else
    echo -e "${RED}Error: Output directory missing${NC}"
    exit 1
fi

echo ""
echo "=========================================="
echo -e "${GREEN}Setup Complete${NC}"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Edit configuration files in config/"
echo "  3. Run simulator: ./run.sh"
echo ""
echo "To run individual simulators:"
echo "  python3 simulator/can_bus.py --config config/can-bus.json"
echo "  python3 simulator/sensor_stream.py --config config/sensors.json"
echo "  python3 simulator/equipment_telemetry.py --config config/equipment.json"
echo ""
