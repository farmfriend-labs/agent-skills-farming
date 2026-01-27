#!/bin/bash

# test.sh
# Test Plant Whisperer Assistant functionality

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
PLANT_DB_PATH="${PLANT_DB_PATH:-/opt/plant-whisperer/plants.db}"
IMAGE_STORAGE_PATH="${IMAGE_STORAGE_PATH:-/opt/plant-whisperer/images}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "=========================================="
echo "Plant Whisperer Assistant - Testing"
echo "=========================================="
echo ""

# Test suite
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

# Helper function to run test
run_test() {
    local test_name="$1"
    local test_command="$2"
    local expected_result="$3"

    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    echo -n "Test $TOTAL_TESTS: $test_name ... "

    if eval "$test_command"; then
        if [[ -n "$expected_result" ]]; then
            if eval "$expected_result"; then
                echo -e "${GREEN}PASS${NC}"
                PASSED_TESTS=$((PASSED_TESTS + 1))
            else
                echo -e "${RED}FAIL${NC}"
                FAILED_TESTS=$((FAILED_TESTS + 1))
            fi
        else
            echo -e "${GREEN}PASS${NC}"
            PASSED_TESTS=$((PASSED_TESTS + 1))
        fi
    else
        echo -e "${RED}FAIL${NC}"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
}

# Test 1: Check Python 3.8+ installation
run_test \
    "Python 3.8+ installed" \
    "python3 --version | grep -qE 'Python 3\.[89]|Python 3\.1[0-9]|Python 3\.[2-9][0-9]'"

# Test 2: Check pip3
run_test \
    "pip3 installed" \
    "command -v pip3 >/dev/null 2>&1"

# Test 3: Check OpenCV
run_test \
    "OpenCV (cv2) available" \
    "python3 -c 'import cv2'"

# Test 4: Check NumPy
run_test \
    "NumPy available" \
    "python3 -c 'import numpy'"

# Test 5: Check PIL/Pillow
run_test \
    "Pillow available" \
    "python3 -c 'import PIL'"

# Test 6: Check scikit-learn
run_test \
    "scikit-learn available" \
    "python3 -c 'import sklearn'"

# Test 7: Check requests library
run_test \
    "requests library available" \
    "python3 -c 'import requests'"

# Test 8: Check scikit-image (optional)
echo ""
echo "Testing optional dependencies..."
if python3 -c "import skimage" 2>/dev/null; then
    run_test \
        "scikit-image available" \
        "python3 -c 'import skimage'"
else
    echo -e "${YELLOW}Test 8: scikit-image not installed (optional)${NC}"
fi

# Test 9: Check TensorFlow (optional)
if python3 -c "import tensorflow" 2>/dev/null; then
    run_test \
        "TensorFlow available" \
        "python3 -c 'import tensorflow'"
else
    echo -e "${YELLOW}Test 9: TensorFlow not installed (optional for AI detection)${NC}"
fi

# Test 10: Check PyTorch (optional)
if python3 -c "import torch" 2>/dev/null; then
    run_test \
        "PyTorch available" \
        "python3 -c 'import torch'"
else
    echo -e "${YELLOW}Test 10: PyTorch not installed (optional)${NC}"
fi

# Test 11: Check directories exist
echo ""
echo "Checking directories..."
run_test \
    "scripts/ directory exists" \
    "[[ -d '$SCRIPT_DIR' ]]"

run_test \
    "Database directory exists" \
    "[[ -d '$(dirname \"$PLANT_DB_PATH\")' ]]"

# Test 12: Check image storage directory
if [[ -d "$IMAGE_STORAGE_PATH" ]]; then
    run_test \
        "Image storage directory exists" \
        "[[ -d '$IMAGE_STORAGE_PATH' ]]"
else
    echo -e "${YELLOW}Test 12: Image storage directory not found (will be created on first use)${NC}"
fi

# Test 13: Check database exists
echo ""
echo "Checking database..."
if [[ -f "$PLANT_DB_PATH" ]]; then
    run_test \
        "Database exists" \
        "[[ -f '$PLANT_DB_PATH' ]]"

    # Test 14: Check database is valid SQLite
    run_test \
        "Database is valid SQLite" \
        "sqlite3 '$PLANT_DB_PATH' 'SELECT name FROM sqlite_master LIMIT 1;' &>/dev/null"
else
    echo -e "${YELLOW}Test 13-14: Database not found at $PLANT_DB_PATH${NC}"
    echo "Run 'python3 scripts/init_database.py' to create database"
    TOTAL_TESTS=$((TOTAL_TESTS + 2))
    FAILED_TESTS=$((FAILED_TESTS + 2))
fi

# Test 15: Check required Python scripts exist
echo ""
echo "Checking Python scripts..."
run_test \
    "analyze_plant.py exists" \
    "[[ -f '$SCRIPT_DIR/analyze_plant.py' ]]"

run_test \
    "init_database.py exists" \
    "[[ -f '$SCRIPT_DIR/init_database.py' ]]"

run_test \
    "monitor.py exists" \
    "[[ -f '$SCRIPT_DIR/monitor.py' ]]"

# Test 16: Check configuration files
echo ""
echo "Checking configuration files..."
run_test \
    ".env.example exists" \
    "[[ -f '$PROJECT_ROOT/.env.example' ]]"

run_test \
    "SKILL.md exists" \
    "[[ -f '$PROJECT_ROOT/SKILL.md' ]]"

run_test \
    "tools.json exists" \
    "[[ -f '$PROJECT_ROOT/tools.json' ]]"

# Test 17: Test image processing capability
echo ""
echo "Testing image processing..."
if python3 -c "import cv2, numpy; img = numpy.zeros((100, 100, 3), dtype='uint8')" 2>/dev/null; then
    run_test \
        "Can create test image" \
        "python3 -c \"import cv2, numpy; img = numpy.zeros((100, 100, 3), dtype='uint8')\""
else
    echo -e "${RED}Test 17: Image processing test FAILED${NC}"
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi

# Test 18: Test color analysis
if python3 -c "import cv2, numpy; img = numpy.zeros((100, 100, 3), dtype='uint8'); hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)" 2>/dev/null; then
    run_test \
        "Color space conversion works" \
        "python3 -c \"import cv2, numpy; img = numpy.zeros((100, 100, 3), dtype='uint8'); hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)\""
else
    echo -e "${RED}Test 18: Color space conversion test FAILED${NC}"
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi

# Test 19: Test feature extraction
echo ""
echo "Testing analysis capabilities..."
if python3 -c "import cv2, numpy; img = numpy.zeros((100, 100, 3), dtype='uint8'); hist = cv2.calcHist([img], [0], None, [256], [0, 256])" 2>/dev/null; then
    run_test \
        "Can extract color histogram" \
        "python3 -c \"import cv2, numpy; img = numpy.zeros((100, 100, 3), dtype='uint8'); hist = cv2.calcHist([img], [0], None, [256], [0, 256])\""
else
    echo -e "${RED}Test 19: Color histogram test FAILED${NC}"
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    FAILED_TESTS=$((FAILED_TESTS + 1))
fi

# Test 20: Test database operations
echo ""
echo "Testing database operations..."
if [[ -f "$PLANT_DB_PATH" ]]; then
    if python3 -c "import sqlite3; conn = sqlite3.connect('$PLANT_DB_PATH'); cursor = conn.cursor(); cursor.execute('SELECT COUNT(*) FROM plants'); conn.close()" 2>/dev/null; then
        run_test \
            "Can query plant database" \
            "python3 -c \"import sqlite3; conn = sqlite3.connect('$PLANT_DB_PATH'); cursor = conn.cursor(); cursor.execute('SELECT COUNT(*) FROM plants'); conn.close()\""
    else
        echo -e "${RED}Test 20: Database query test FAILED${NC}"
        TOTAL_TESTS=$((TOTAL_TESTS + 1))
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
else
    echo -e "${YELLOW}Test 20: Database test skipped (database not found)${NC}"
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
fi

# Test 21: Test API configuration
echo ""
echo "Testing API configuration..."
API_CONFIGURED=false

if [[ -n "$PLANTNET_API_KEY" ]]; then
    echo -e "${GREEN}PlantNet API key configured${NC}"
    API_CONFIGURED=true
else
    echo -e "${YELLOW}PlantNet API key not configured (optional)${NC}"
fi

if [[ -n "$TREFLE_API_KEY" ]]; then
    echo -e "${GREEN}Trefle API key configured${NC}"
    API_CONFIGURED=true
else
    echo -e "${YELLOW}Trefle API key not configured (optional)${NC}"
fi

if [[ -n "$OPENWEATHER_API_KEY" ]]; then
    echo -e "${GREEN}OpenWeatherMap API key configured${NC}"
    API_CONFIGURED=true
else
    echo -e "${YELLOW}OpenWeatherMap API key not configured (optional)${NC}"
fi

if [[ "$API_CONFIGURED" == "true" ]]; then
    run_test \
        "At least one API key configured" \
        "true"
else
    echo -e "${YELLOW}Test 21: No API keys configured (all optional)${NC}"
fi

# Summary
echo ""
echo "=========================================="
echo "Test Summary"
echo "=========================================="
echo "Total Tests: $TOTAL_TESTS"
echo -e "Passed: ${GREEN}$PASSED_TESTS${NC}"
if [[ $FAILED_TESTS -gt 0 ]]; then
    echo -e "Failed: ${RED}$FAILED_TESTS${NC}"
else
    echo -e "Failed: ${FAILED_TESTS}${NC}"
fi
echo "=========================================="

if [[ $FAILED_TESTS -eq 0 ]]; then
    echo -e "${GREEN}All tests passed!${NC}"
    echo "Plant Whisperer Assistant is ready to use."
    exit 0
else
    echo -e "${RED}Some tests failed${NC}"
    echo "Please fix the issues above before using the assistant."
    exit 1
fi
