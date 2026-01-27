#!/bin/bash
# test.sh - Plug-and-Play Precision Agriculture Test Suite

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
TESTS_TOTAL=0
TESTS_PASSED=0
TESTS_FAILED=0

# Function to print test header
print_test_header() {
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}Testing: $1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

# Function to print success
print_success() {
    echo -e "${GREEN}[PASS]${NC} $1"
    ((TESTS_PASSED++))
}

# Function to print failure
print_failure() {
    echo -e "${RED}[FAIL]${NC} $1"
    ((TESTS_FAILED++))
}

# Function to print info
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

# Function to run a test
run_test() {
    ((TESTS_TOTAL++))
    local test_name="$1"
    local test_command="$2"

    print_info "Running: $test_name"
    if eval "$test_command" > /dev/null 2>&1; then
        print_success "$test_name"
        return 0
    else
        print_failure "$test_name"
        return 1
    fi
}

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

echo "========================================"
echo "Plug-and-Play Precision Ag Test Suite"
echo "========================================"
echo ""

# Test 1: Python version
print_test_header "Python Environment"
if python3 --version | grep -q "Python 3\.[89]\|Python 3\.[1-9][0-9]"; then
    print_success "Python 3.8+ installed"
else
    print_failure "Python 3.8+ required"
fi

# Test 2: Required Python packages
print_test_header "Python Packages"

REQUIRED_PACKAGES=(
    "pyserial"
    "pyproj"
    "shapely"
    "geopandas"
    "requests"
    "pandas"
    "numpy"
    "matplotlib"
)

for package in "${REQUIRED_PACKAGES[@]}"; do
    run_test "$package installed" "python3 -c 'import $package'"
done

# Test 3: System dependencies
print_test_header "System Dependencies"

if command -v sqlite3 &> /dev/null; then
    print_success "sqlite3 installed"
else
    print_failure "sqlite3 not found"
fi

if command -v gdal-config &> /dev/null; then
    print_success "GDAL installed"
else
    print_failure "GDAL not found"
fi

# Test 4: Directory structure
print_test_header "Directory Structure"

DIRECTORIES=(
    "/var/lib/precision-ag/fields"
    "/var/lib/precision-ag/implements"
    "/var/lib/precision-ag/prescriptions"
    "/var/lib/precision-ag/yield_data"
    "/var/lib/precision-ag/weather"
    "/var/log/precision-ag"
    "/var/backups/precision-ag"
)

for dir in "${DIRECTORIES[@]}"; do
    run_test "Directory exists: $dir" "test -d '$dir'"
done

# Test 5: Database
print_test_header "Database"

DB_PATH="${DB_PATH:-/var/lib/precision-ag/precision-ag.db}"

if [ -f "$DB_PATH" ]; then
    print_success "Database file exists"
    run_test "Database is readable" "test -r '$DB_PATH'"
    run_test "Database is writable" "test -w '$DB_PATH'"

    # Test database schema
    print_info "Testing database schema..."
    if python3 -c "import sqlite3; conn = sqlite3.connect('$DB_PATH'); cursor = conn.cursor(); cursor.execute('SELECT name FROM sqlite_master WHERE type=\"table\"'); tables = [t[0] for t in cursor.fetchall()]; required = ['fields', 'operations', 'prescriptions', 'yield_data']; all_exist = all(t in tables for t in required); conn.close(); exit(0 if all_exist else 1)"; then
        print_success "Database schema correct"
    else
        print_failure "Database schema incorrect"
    fi
else
    print_warning "Database file not found. Run setup.sh first."
fi

# Test 6: GPS device (optional)
print_test_header "GPS Device"

GPS_PORT="${GPS_PORT:-/dev/ttyUSB0}"

if [ -e "$GPS_PORT" ]; then
    print_success "GPS device found: $GPS_PORT"
    run_test "GPS device is readable" "test -r '$GPS_PORT'"
    run_test "GPS device is writable" "test -w '$GPS_PORT'"

    # Test GPS communication
    print_info "Testing GPS communication (this may take 10 seconds)..."
    if timeout 10 python3 scripts/gps_status.py --port "$GPS_PORT" --baudrate "${GPS_BAUDRATE:-9600}" > /dev/null 2>&1; then
        print_success "GPS communication successful"
    else
        print_warning "Could not communicate with GPS. Device may not be connected."
    fi
else
    print_warning "GPS device not found: $GPS_PORT"
fi

# Test 7: CAN interface (optional)
print_test_header "CAN Interface"

CAN_INTERFACE="${CAN_INTERFACE:-can0}"

if ip link show "$CAN_INTERFACE" &> /dev/null; then
    print_success "CAN interface found: $CAN_INTERFACE"
else
    print_warning "CAN interface not found: $CAN_INTERFACE"
fi

# Test 8: Script functionality
print_test_header "Script Functionality"

# Test GPS status script
if [ -x scripts/gps_status.py ]; then
    run_test "GPS status script is executable" "true"
    print_info "GPS status script: scripts/gps_status.py"
else
    print_warning "GPS status script not executable"
fi

# Test field manager script
if [ -x scripts/field_manager.py ]; then
    run_test "Field manager script is executable" "true"
else
    print_warning "Field manager script not executable"
fi

# Test 9: Data export/import
print_test_header "Data Operations"

# Create test data
TEST_DIR="/tmp/precision-ag-test"
mkdir -p "$TEST_DIR"

print_info "Creating test data..."
echo "field_id,latitude,longitude,value" > "$TEST_DIR/test_data.csv"
echo "1,40.7128,-74.0060,100" >> "$TEST_DIR/test_data.csv"
echo "1,40.7129,-74.0061,105" >> "$TEST_DIR/test_data.csv"
echo "1,40.7130,-74.0062,95" >> "$TEST_DIR/test_data.csv"

run_test "CSV file created" "test -f '$TEST_DIR/test_data.csv'"

# Test Python can read CSV
if python3 -c "import pandas; df = pandas.read_csv('$TEST_DIR/test_data.csv'); exit(0 if len(df) > 0 else 1)"; then
    print_success "Python can read test CSV"
else
    print_failure "Python cannot read test CSV"
fi

# Clean up test data
rm -rf "$TEST_DIR"

# Test 10: Configuration
print_test_header "Configuration"

if [ -f .env ]; then
    print_success ".env file exists"

    # Check for required variables
    if grep -q "GPS_PORT=" .env; then
        print_success "GPS_PORT configured"
    else
        print_failure "GPS_PORT not configured"
    fi

    if grep -q "FIELD_DATA_PATH=" .env; then
        print_success "FIELD_DATA_PATH configured"
    else
        print_failure "FIELD_DATA_PATH not configured"
    fi

    if grep -q "DB_PATH=" .env; then
        print_success "DB_PATH configured"
    else
        print_failure "DB_PATH not configured"
    fi
else
    print_warning ".env file not found. Copy from .env.example."
fi

# Test 11: API connectivity (if not offline)
print_test_header "API Connectivity"

if [ "${OFFLINE_MODE:-true}" = "false" ]; then
    # Test weather API
    print_info "Testing weather API connectivity..."
    if python3 -c "import requests; r = requests.get('${OPENMETEO_API_URL:-https://api.open-meteo.com/v1}', timeout=5); exit(0 if r.status_code == 200 else 1)"; then
        print_success "Weather API accessible"
    else
        print_warning "Weather API not accessible"
    fi
else
    print_info "Offline mode enabled, skipping API tests"
fi

# Test 12: Log files
print_test_header "Logging"

LOG_FILE="${LOG_FILE:-/var/log/precision-ag.log}"

if [ -f "$LOG_FILE" ]; then
    print_success "Log file exists"
    run_test "Log file is readable" "test -r '$LOG_FILE'"

    if [ -r "$LOG_FILE" ]; then
        LOG_SIZE=$(stat -f%z "$LOG_FILE" 2>/dev/null || stat -c%s "$LOG_FILE" 2>/dev/null || echo "0")
        print_info "Log file size: $LOG_SIZE bytes"
    fi
else
    print_warning "Log file not found. Will be created on first run."
fi

# Test summary
echo ""
echo "========================================"
echo "Test Summary"
echo "========================================"
echo -e "Total Tests: $TESTS_TOTAL"
echo -e "${GREEN}Passed: $TESTS_PASSED${NC}"
echo -e "${RED}Failed: $TESTS_FAILED${NC}"

if [ $TESTS_FAILED -eq 0 ]; then
    echo ""
    echo -e "${GREEN}All tests passed!${NC}"
    exit 0
else
    echo ""
    echo -e "${RED}Some tests failed. Please review the output above.${NC}"
    exit 1
fi
