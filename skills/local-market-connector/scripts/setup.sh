#!/bin/bash

# setup.sh - Local Market Connector Setup

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DATABASE_PATH="${BUYER_DB_PATH:-/opt/local-market/buyers.db}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=========================================="
echo "Local Market Connector - Setup"
echo "=========================================="
echo ""

# Check Python
echo "Checking dependencies..."
if ! command -v python3 >/dev/null 2>&1; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    exit 1
fi
echo -e "${GREEN}Python 3 found${NC}"

# Install Python packages
echo ""
echo "Installing Python packages..."
pip3 install requests beautifulsoup4 pandas geopy -q 2>/dev/null
echo -e "${GREEN}Packages installed${NC}"

# Create directories
echo ""
echo "Creating directories..."
sudo mkdir -p /opt/local-market/{buyers,backups}
sudo chown $USER:$USER /opt/local-market -R
echo -e "${GREEN}Directories created${NC}"

# Create .env
if [[ ! -f "$PROJECT_ROOT/.env" ]]; then
    cp "$PROJECT_ROOT/.env.example" "$PROJECT_ROOT/.env"
    echo -e "${GREEN}.env created from .env.example${NC}"
fi

# Initialize database
echo ""
echo "Initializing database..."
python3 scripts/init_database.py --database "$DATABASE_PATH"

echo ""
echo -e "${GREEN}Setup complete!${NC}"
echo "Next: Edit .env and add buyers to database"
