#!/bin/bash
# setup.sh - Plug-and-Play Precision Agriculture Setup Script
# This script installs dependencies and configures the environment

set -e

echo "========================================"
echo "Plug-and-Play Precision Ag Setup"
echo "========================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    print_warning "Some operations may require sudo privileges"
fi

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
    DISTRO=$(lsb_release -si 2>/dev/null || echo "unknown")
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
else
    print_error "Unsupported operating system: $OSTYPE"
    exit 1
fi

print_success "Detected OS: $OS"

# Check Python version
echo ""
echo "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
    print_success "Python $PYTHON_VERSION found"
else
    print_error "Python 3 is not installed"
    exit 1
fi

# Create necessary directories
echo ""
echo "Creating directory structure..."
mkdir -p /var/lib/precision-ag/fields
mkdir -p /var/lib/precision-ag/implements
mkdir -p /var/lib/precision-ag/prescriptions
mkdir -p /var/lib/precision-ag/yield_data
mkdir -p /var/lib/precision-ag/weather
mkdir -p /var/log/precision-ag
mkdir -p /var/backups/precision-ag
print_success "Directory structure created"

# Install system dependencies
echo ""
echo "Installing system dependencies..."

if [ "$OS" == "linux" ]; then
    if command -v apt-get &> /dev/null; then
        echo "Using apt-get package manager..."
        apt-get update
        apt-get install -y \
            python3-pip \
            python3-venv \
            sqlite3 \
            gdal-bin \
            python3-gdal \
            gpsbabel \
            qgis \
            can-utils \
            python3-serial
    elif command -v yum &> /dev/null; then
        echo "Using yum package manager..."
        yum install -y \
            python3-pip \
            sqlite \
            gdal \
            python3-gdal \
            gpsbabel \
            qgis \
            can-utils \
            python3-pyserial
    else
        print_warning "Unknown package manager. Please install dependencies manually."
    fi
elif [ "$OS" == "macos" ]; then
    if command -v brew &> /dev/null; then
        echo "Using Homebrew package manager..."
        brew install \
            python3 \
            gdal \
            gpsbabel \
            qgis \
            can-utils
    else
        print_warning "Homebrew not found. Please install Homebrew first."
    fi
fi

print_success "System dependencies installed"

# Install Python packages
echo ""
echo "Installing Python packages..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install required packages
pip install pyserial>=3.5
pip install pyproj>=3.2
pip install shapely>=1.8
pip install geopandas>=0.10
pip install requests>=2.26
pip install pandas>=1.3
pip install numpy>=1.21
pip install matplotlib>=3.4
pip install can>=4.0

print_success "Python packages installed"

# Initialize database
echo ""
echo "Initializing database..."
python3 scripts/init_db.py

print_success "Database initialized"

# Copy example environment file
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file from example..."
    cp .env.example .env
    print_success ".env file created. Please edit with your configuration."
fi

# Check for GPS device
echo ""
echo "Checking for GPS devices..."
GPS_FOUND=false
for device in /dev/ttyUSB* /dev/ttyACM*; do
    if [ -e "$device" ]; then
        print_success "Found potential GPS device: $device"
        GPS_FOUND=true
    fi
done

if [ "$GPS_FOUND" = false ]; then
    print_warning "No GPS devices found. Please connect your GPS receiver."
fi

# Check for CAN interface
echo ""
echo "Checking for CAN interface..."
if ip link show can0 &> /dev/null; then
    print_success "CAN interface can0 found"
else
    print_warning "CAN interface not found. Configure with: sudo ip link add can0 type can"
fi

# Set permissions
echo ""
echo "Setting up permissions..."
if [ -f /dev/ttyUSB0 ]; then
    sudo chmod 666 /dev/ttyUSB0 2>/dev/null || print_warning "Could not set permissions for /dev/ttyUSB0"
fi
if [ -f /dev/ttyACM0 ]; then
    sudo chmod 666 /dev/ttyACM0 2>/dev/null || print_warning "Could not set permissions for /dev/ttyACM0"
fi

print_success "Permissions configured"

# Create systemd service (Linux only)
if [ "$OS" == "linux" ] && [ "$DISTRO" == "Ubuntu" ] || [ "$DISTRO" == "Debian" ]; then
    echo ""
    read -p "Install systemd service for auto-start? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Creating systemd service..."
        cat > /etc/systemd/system/precision-ag.service << EOF
[Unit]
Description=Plug-and-Play Precision Agriculture Service
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
ExecStart=$(pwd)/scripts/run.sh
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
        print_success "Systemd service created"
        print_warning "Enable with: sudo systemctl enable precision-ag"
        print_warning "Start with: sudo systemctl start precision-ag"
    fi
fi

# Summary
echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your configuration"
echo "2. Connect your GPS receiver"
echo "3. Test GPS connection: python3 scripts/test_gps.py"
echo "4. Create your first field: python3 scripts/field_manager.py create"
echo ""
echo "For help: python3 scripts/run.sh --help"
echo ""
