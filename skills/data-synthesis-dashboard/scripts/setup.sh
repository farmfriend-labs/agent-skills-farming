#!/bin/bash
# setup.sh - Initialize data synthesis dashboard environment

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=========================================="
echo "Data Synthesis Dashboard - Setup"
echo "=========================================="

# Check Python
if ! command -v python3 >/dev/null 2>&1; then
    echo -e "${RED}Error: Python 3 not found${NC}"
    exit 1
fi

# Install dependencies
echo "Installing Python dependencies..."
pip3 install --user flask dash plotly pandas sqlalchemy requests 2>/dev/null || {
    echo -e "${YELLOW}Some dependencies may have failed${NC}"
}

# Create directories
mkdir -p /var/data-synthesis-dashboard/data
mkdir -p /var/data-synthesis-dashboard/logs
mkdir -p /var/data-synthesis-dashboard/cache

echo -e "${GREEN}Setup Complete${NC}"
echo "Next: Run 'scripts/run.sh' to start dashboard"
