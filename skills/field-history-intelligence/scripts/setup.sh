#!/bin/bash

# setup.sh
# Initialize field history intelligence system

set -e

# Configuration
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DATABASE_PATH="${DATABASE_PATH:-/opt/field-history/field-data.db}"
BACKUP_PATH="${BACKUP_PATH:-/opt/field-history/backups}"
IMPORT_DIR="${IMPORT_DIR:-/opt/field-history/imports}"
LOG_FILE="${LOG_FILE:-/var/log/field-history-intelligence.log}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "=========================================="
echo "Field History Intelligence - Setup"
echo "=========================================="
echo ""

# Check for Python
echo "Checking dependencies..."
if ! command -v python3 >/dev/null 2>&1; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    echo "Install with: sudo apt-get install python3 python3-pip"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo -e "${GREEN}Python $PYTHON_VERSION found${NC}"

# Check for pip
if ! command -v pip3 >/dev/null 2>&1; then
    echo -e "${YELLOW}Warning: pip3 not found${NC}"
    echo "Install with: sudo apt-get install python3-pip"
fi

# Install Python dependencies
echo ""
echo "Installing Python packages..."
PACKAGES=(
    "pandas>=1.3"
    "numpy>=1.21"
    "matplotlib>=3.4"
    "Pillow>=8.3"
    "pytesseract>=0.3.8"
    "tabula-py>=2.3"
    "requests>=2.26"
    "reportlab>=3.6"
    "fiona>=1.8"
)

for package in "${PACKAGES[@]}"; do
    echo -n "  Installing $package ... "
    if pip3 install "$package" -q 2>/dev/null; then
        echo -e "${GREEN}OK${NC}"
    else
        echo -e "${YELLOW}SKIPPED (may already be installed)${NC}"
    fi
done

# Check for SQLite
echo ""
echo "Checking SQLite..."
if python3 -c "import sqlite3" 2>/dev/null; then
    echo -e "${GREEN}SQLite available${NC}"
else
    echo -e "${YELLOW}Warning: SQLite may not be available${NC}"
fi

# Check for Tesseract OCR (optional)
echo ""
echo "Checking OCR capabilities..."
if command -v tesseract >/dev/null 2>&1; then
    echo -e "${GREEN}Tesseract OCR found${NC}"
else
    echo -e "${YELLOW}Tesseract OCR not found (optional for image import)${NC}"
    echo "Install with: sudo apt-get install tesseract-ocr"
fi

# Create directory structure
echo ""
echo "Creating directory structure..."
directories=(
    "$DATABASE_PATH"
    "$BACKUP_PATH"
    "$IMPORT_DIR"
    "$(dirname "$LOG_FILE")"
)

for dir in "${directories[@]}"; do
    dir_path=$(dirname "$dir")
    if [[ ! -d "$dir_path" ]]; then
        echo -n "  Creating $dir_path ... "
        sudo mkdir -p "$dir_path"
        sudo chown $USER:$USER "$dir_path"
        echo -e "${GREEN}OK${NC}"
    fi
done

# Initialize database
echo ""
echo "Initializing database..."
if python3 scripts/init_database.py --database "$DATABASE_PATH"; then
    echo -e "${GREEN}Database initialized${NC}"
else
    echo -e "${YELLOW}Database may already exist or initialization failed${NC}"
fi

# Create sample configuration
echo ""
echo "Creating configuration files..."
if [[ ! -f "$PROJECT_ROOT/.env" ]]; then
    echo -n "  Creating .env from .env.example ... "
    cp "$PROJECT_ROOT/.env.example" "$PROJECT_ROOT/.env"
    echo -e "${GREEN}OK${NC}"
    echo -e "${YELLOW}Please edit .env and configure your settings${NC}"
else
    echo -e "${YELLOW}.env already exists${NC}"
fi

# Set permissions
echo ""
echo "Setting permissions..."
chmod +x "$PROJECT_ROOT/scripts"/*.sh 2>/dev/null || true

# Display summary
echo ""
echo "=========================================="
echo -e "${GREEN}Setup Complete${NC}"
echo "=========================================="
echo ""
echo "Configuration:"
echo "  Database: $DATABASE_PATH"
echo "  Backups: $BACKUP_PATH"
echo "  Imports: $IMPORT_DIR"
echo "  Log: $LOG_FILE"
echo ""
echo "Next steps:"
echo "  1. Edit .env to configure your settings"
echo "  2. Import historical data using scripts/import_*.py"
echo "  3. Run analysis with scripts/analyze_*.py"
echo "  4. Generate reports with scripts/generate_report.py"
echo ""
echo "For help: python3 scripts/init_database.py --help"
echo ""
