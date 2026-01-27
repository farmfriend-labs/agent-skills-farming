#!/bin/bash

# setup.sh
# Initialize Plant Whisperer Assistant environment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "=========================================="
echo "Plant Whisperer Assistant - Setup"
echo "=========================================="
echo ""

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
PLANT_DB_PATH="${PLANT_DB_PATH:-/opt/plant-whisperer/plants.db}"
IMAGE_STORAGE_PATH="${IMAGE_STORAGE_PATH:-/opt/plant-whisperer/images}"
LOG_FILE="${LOG_FILE:-/var/log/plant-whisperer.log}"

# Check for Python 3.8+
echo "Checking Python installation..."
if ! command -v python3 >/dev/null 2>&1; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    echo "Install with: sudo apt-get install python3 python3-pip"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo -e "${GREEN}Python version: $PYTHON_VERSION${NC}"

# Check Python version
if ! python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)" 2>/dev/null; then
    echo -e "${RED}Error: Python 3.8 or higher is required${NC}"
    echo "Current version: $PYTHON_VERSION"
    exit 1
fi

# Check for pip
echo ""
echo "Checking pip..."
if ! command -v pip3 >/dev/null 2>&1; then
    echo -e "${YELLOW}pip3 not found, installing...${NC}"
    sudo apt-get update
    sudo apt-get install -y python3-pip
fi
echo -e "${GREEN}pip3 installed${NC}"

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
echo "This may take a few minutes..."

pip3 install --upgrade pip

# Core dependencies
echo "Installing core dependencies..."
pip3 install opencv-python numpy pillow requests pyyaml

# Machine learning dependencies
echo "Installing machine learning dependencies..."
pip3 install scikit-learn scikit-image pandas matplotlib seaborn

# Optional: TensorFlow (for AI detection)
echo ""
read -p "Install TensorFlow for AI detection? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Installing TensorFlow (this may take several minutes)..."
    pip3 install tensorflow
else
    echo -e "${YELLOW}Skipping TensorFlow installation${NC}"
    echo "You can install it later with: pip3 install tensorflow"
fi

echo -e "${GREEN}Python dependencies installed${NC}"

# Create directories
echo ""
echo "Creating directories..."

# Create database directory
DB_DIR=$(dirname "$PLANT_DB_PATH")
if [[ ! -d "$DB_DIR" ]]; then
    echo "Creating database directory: $DB_DIR"
    sudo mkdir -p "$DB_DIR"
    sudo chown $USER:$USER "$DB_DIR"
fi

# Create image storage directory
if [[ ! -d "$IMAGE_STORAGE_PATH" ]]; then
    echo "Creating image storage directory: $IMAGE_STORAGE_PATH"
    sudo mkdir -p "$IMAGE_STORAGE_PATH"
    sudo chown $USER:$USER "$IMAGE_STORAGE_PATH"
fi

# Create log directory
LOG_DIR=$(dirname "$LOG_FILE")
if [[ ! -d "$LOG_DIR" ]]; then
    echo "Creating log directory: $LOG_DIR"
    sudo mkdir -p "$LOG_DIR"
    sudo chown $USER:$USER "$LOG_DIR"
fi

echo -e "${GREEN}Directories created${NC}"

# Create test data directory (optional)
if [[ "$DEBUG_MODE" == "true" ]]; then
    TEST_DATA_DIR="${TEST_DATA_DIR:-/opt/plant-whisperer/test-data}"
    if [[ ! -d "$TEST_DATA_DIR" ]]; then
        echo "Creating test data directory: $TEST_DATA_DIR"
        sudo mkdir -p "$TEST_DATA_DIR"
        sudo chown $USER:$USER "$TEST_DATA_DIR"
    fi
fi

# Initialize database
echo ""
echo "Initializing plant database..."
python3 "$SCRIPT_DIR/init_database.py"

# Copy .env.example if .env doesn't exist
if [[ ! -f "$PROJECT_ROOT/.env" ]]; then
    echo ""
    echo "Creating .env file from template..."
    cp "$PROJECT_ROOT/.env.example" "$PROJECT_ROOT/.env"
    echo -e "${GREEN}.env file created${NC}"
    echo -e "${YELLOW}Please edit .env and configure your settings${NC}"
else
    echo -e "${GREEN}.env file already exists${NC}"
fi

# Download plant disease models (optional)
echo ""
read -p "Download pre-trained AI models for disease detection? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Downloading AI models..."
    python3 "$SCRIPT_DIR/download_models.py"
else
    echo -e "${YELLOW}Skipping model download${NC}"
    echo "You can download models later by running: python3 scripts/download_models.py"
fi

# Set up logrotate (optional)
echo ""
read -p "Set up log rotation for log files? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Setting up log rotation..."
    sudo tee /etc/logrotate.d/plant-whisperer > /dev/null <<EOF
$LOG_FILE {
    daily
    rotate 5
    compress
    delaycompress
    missingok
    notifempty
    create 0644 $USER $USER
}
EOF
    echo -e "${GREEN}Log rotation configured${NC}"
else
    echo -e "${YELLOW}Skipping log rotation setup${NC}"
fi

# Create systemd service (optional)
echo ""
read -p "Create systemd service for auto-start? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Creating systemd service..."
    sudo tee /etc/systemd/system/plant-whisperer.service > /dev/null <<EOF
[Unit]
Description=Plant Whisperer Assistant
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$PROJECT_ROOT
ExecStart=/usr/bin/python3 $SCRIPT_DIR/monitor.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

    sudo systemctl daemon-reload
    sudo systemctl enable plant-whisperer.service
    echo -e "${GREEN}Systemd service created${NC}"
    echo "Start service with: sudo systemctl start plant-whisperer"
else
    echo -e "${YELLOW}Skipping systemd service creation${NC}"
fi

# Summary
echo ""
echo "=========================================="
echo -e "${GREEN}Setup Complete!${NC}"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Edit .env file with your configuration"
echo "  2. Optional: Get API keys for PlantNet, Trefle, or OpenWeatherMap"
echo "  3. Add your first plant: python3 scripts/add_plant.py"
echo "  4. Analyze a plant: python3 scripts/analyze_plant.py --image path/to/image.jpg"
echo ""
echo "For help:"
echo "  python3 scripts/analyze_plant.py --help"
echo "  See SKILL.md for documentation"
echo ""
