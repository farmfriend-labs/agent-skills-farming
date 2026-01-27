#!/bin/bash

# setup.sh
# Initialize seed sovereignty guide database and dependencies

set -e

# Configuration
SEED_DB_PATH="${SEED_DB_PATH:-/opt/seed-sovereignty/seeds.db}"
GERMINATION_LOG_PATH="${GERMINATION_LOG_PATH:-/opt/seed-sovereignty/germination.log}"
INSTALL_DIR="/opt/seed-sovereignty"
PYTHON_VERSION="python3"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=========================================="
echo "Seed Sovereignty Guide - Setup"
echo "=========================================="
echo ""

# Check for Python 3
echo "Checking for Python 3..."
if ! command -v $PYTHON_VERSION &> /dev/null; then
    echo -e "${RED}Error: Python 3 not found${NC}"
    echo "Please install Python 3.8 or later"
    exit 1
fi

PYTHON_VER=$($PYTHON_VERSION --version | awk '{print $2}')
echo -e "${GREEN}Found Python $PYTHON_VER${NC}"

# Create installation directory
echo ""
echo "Creating installation directory..."
sudo mkdir -p "$INSTALL_DIR"
sudo chown $USER:$USER "$INSTALL_DIR"
echo -e "${GREEN}Directory created: $INSTALL_DIR${NC}"

# Create database
echo ""
echo "Initializing seed database..."
if [ -f "$SEED_DB_PATH" ]; then
    echo -e "${YELLOW}Database already exists at $SEED_DB_PATH${NC}"
    read -p "Overwrite existing database? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm "$SEED_DB_PATH"
        echo "Old database removed"
    else
        echo "Keeping existing database"
    fi
fi

# Create database schema
$PYTHON_VERSION - <<EOF
import sqlite3
import os

db_path = os.environ.get('SEED_DB_PATH', '/opt/seed-sovereignty/seeds.db')
os.makedirs(os.path.dirname(db_path), exist_ok=True)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Seeds table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS seeds (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        variety_name TEXT NOT NULL,
        crop_type TEXT NOT NULL,
        year_saved INTEGER NOT NULL,
        source TEXT,
        germination_pct REAL,
        quantity_grams REAL,
        location_stored TEXT,
        container_type TEXT,
        date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_tested TIMESTAMP,
        notes TEXT
    )
''')

# Germination tests table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS germination_tests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        seed_id INTEGER NOT NULL,
        test_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        seeds_tested INTEGER NOT NULL,
        seeds_germinated INTEGER NOT NULL,
        germination_pct REAL NOT NULL,
        conditions_temp_celsius REAL,
        conditions_days INTEGER,
        notes TEXT,
        FOREIGN KEY (seed_id) REFERENCES seeds(id)
    )
''')

# Variety characteristics table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS variety_characteristics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        variety_name TEXT NOT NULL,
        crop_type TEXT NOT NULL,
        pollination_type TEXT NOT NULL,
        isolation_distance_feet INTEGER,
        min_population INTEGER,
        biennial BOOLEAN DEFAULT 0,
        processing_method TEXT,
        viability_years INTEGER
    )
''')

# Create indexes
cursor.execute('CREATE INDEX IF NOT EXISTS idx_seeds_variety ON seeds(variety_name)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_seeds_crop ON seeds(crop_type)')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_seeds_year ON seeds(year_saved)')

# Insert default variety characteristics
default_varieties = [
    ('Cherokee Purple', 'tomato', 'self-pollinating', 25, 12, 0, 'fermentation', 4),
    ('Kentucky Wonder', 'beans', 'self-pollinating', 20, 40, 0, 'threshing', 3),
    ('Golden Bantam', 'corn', 'cross-pollinating', 1320, 150, 0, 'drying', 1),
    ('Waltham Butternut', 'squash', 'cross-pollinating', 2640, 12, 0, 'fermentation', 4),
    ('Boston Pickling', 'cucumber', 'cross-pollinating', 2640, 20, 0, 'fermentation', 5),
    ('Red Salad Bowl', 'lettuce', 'self-pollinating', 20, 20, 0, 'rubbing', 2),
    ('California Wonder', 'pepper', 'cross-pollinating', 500, 10, 0, 'rinsing', 3),
    ('Black Beauty', 'eggplant', 'cross-pollinating', 500, 10, 0, 'rinsing', 4),
    ('Detroit Dark Red', 'beets', 'biennial', 5280, 32, 1, 'rubbing', 4),
    ('Danvers 126', 'carrots', 'biennial', 5280, 64, 1, 'rubbing', 3),
]

cursor.executemany('''
    INSERT OR IGNORE INTO variety_characteristics
    (variety_name, crop_type, pollination_type, isolation_distance_feet,
     min_population, biennial, processing_method, viability_years)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
''', default_varieties)

conn.commit()
conn.close()

print(f"Database created: {db_path}")
print(f"Inserted {len(default_varieties)} default varieties")
EOF

echo -e "${GREEN}Database initialized${NC}"

# Create log file
echo ""
echo "Creating log file..."
sudo touch "$GERMINATION_LOG_PATH"
sudo chown $USER:$USER "$GERMINATION_LOG_PATH"
echo -e "${GREEN}Log file created: $GERMINATION_LOG_PATH${NC}"

# Check for optional dependencies
echo ""
echo "Checking optional dependencies..."

if command -v sensors &> /dev/null; then
    echo -e "${GREEN}lm-sensors installed (temperature monitoring)${NC}"
else
    echo -e "${YELLOW}lm-sensors not found (temperature monitoring not available)${NC}"
fi

if $PYTHON_VERSION -c "import requests" 2>/dev/null; then
    echo -e "${GREEN}python-requests installed (seed exchange API)${NC}"
else
    echo -e "${YELLOW}python-requests not found (seed exchange API not available)${NC}"
fi

# Display summary
echo ""
echo "=========================================="
echo -e "${GREEN}Setup Complete${NC}"
echo "=========================================="
echo ""
echo "Configuration:"
echo "  Database: $SEED_DB_PATH"
echo "  Log file: $GERMINATION_LOG_PATH"
echo "  Install dir: $INSTALL_DIR"
echo ""
echo "Next steps:"
echo "  1. Add seeds to database: python3 scripts/seed_manager.py add"
echo "  2. Record germination tests: python3 scripts/germination_test.py"
echo "  3. Check viability: python3 scripts/viability_checker.py"
echo ""
