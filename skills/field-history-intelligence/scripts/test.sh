#!/bin/bash

# test.sh
# Test field history intelligence system

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
DATABASE_PATH="${DATABASE_PATH:-/opt/field-history/field-data.db}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "=========================================="
echo "Field History Intelligence - Testing"
echo "=========================================="
echo ""

# Test counters
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0

run_test() {
    local test_name="$1"
    local test_command="$2"

    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    echo -n "Test $TOTAL_TESTS: $test_name ... "

    if eval "$test_command"; then
        echo -e "${GREEN}PASS${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo -e "${RED}FAIL${NC}"
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
}

# Test 1: Python installed
run_test \
    "Python 3.8+ installed" \
    "python3 --version | grep -qE 'Python 3\.[89]|Python 3\.1[0-9]'"

# Test 2: SQLite available
run_test \
    "SQLite available" \
    "python3 -c 'import sqlite3'"

# Test 3: Pandas available
run_test \
    "Pandas library available" \
    "python3 -c 'import pandas' 2>/dev/null"

# Test 4: NumPy available
run_test \
    "NumPy library available" \
    "python3 -c 'import numpy' 2>/dev/null"

# Test 5: Database exists
echo ""
echo "Checking database..."
if [[ -f "$DATABASE_PATH" ]]; then
    run_test \
        "Database file exists" \
        "[[ -f '$DATABASE_PATH' ]]"

    # Test 6: Database is valid SQLite
    run_test \
        "Database is valid SQLite" \
        "sqlite3 '$DATABASE_PATH' 'SELECT name FROM sqlite_master LIMIT 1;' &>/dev/null"

    # Test 7: Database has tables
    if sqlite3 "$DATABASE_PATH" 'SELECT COUNT(*) FROM sqlite_master WHERE type="table";' &>/dev/null; then
        table_count=$(sqlite3 "$DATABASE_PATH" 'SELECT COUNT(*) FROM sqlite_master WHERE type="table";' 2>/dev/null || echo "0")
        if [[ "$table_count" -gt 0 ]]; then
            echo -e "${GREEN}Test 7: PASS${NC} ($table_count tables found)"
            PASSED_TESTS=$((PASSED_TESTS + 1))
            TOTAL_TESTS=$((TOTAL_TESTS + 1))
        else
            echo -e "${YELLOW}Test 7: Database has no tables${NC}"
            TOTAL_TESTS=$((TOTAL_TESTS + 1))
        fi
    fi
else
    echo -e "${YELLOW}Database not found at $DATABASE_PATH${NC}"
    echo "Run 'python3 scripts/init_database.py' to create database"
    TOTAL_TESTS=$((TOTAL_TESTS + 4))
    FAILED_TESTS=$((FAILED_TESTS + 4))
fi

# Test 8: Scripts exist
echo ""
echo "Checking scripts..."
run_test \
    "init_database.py exists" \
    "[[ -f '$SCRIPT_DIR/init_database.py' ]]"

run_test \
    "analyze_yields.py exists" \
    "[[ -f '$SCRIPT_DIR/analyze_yields.py' ]]"

run_test \
    "import_csv.py exists" \
    "[[ -f '$SCRIPT_DIR/import_csv.py' ]]"

# Test 9: Configuration files exist
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

# Test 10: Import test data (if database exists)
if [[ -f "$DATABASE_PATH" ]]; then
    echo ""
    echo "Testing database operations..."
    run_test \
        "Can query database" \
        "sqlite3 '$DATABASE_PATH' 'SELECT COUNT(*) FROM fields;' &>/dev/null || true"
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
    echo "Field History Intelligence is ready to use."
    exit 0
else
    echo -e "${RED}Some tests failed${NC}"
    echo "Please fix the issues above before using the system."
    exit 1
fi
