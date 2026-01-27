#!/bin/bash

# test.sh
# Test emergency diagnostics functionality

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
CODE_DB_PATH="${CODE_DB_PATH:-/opt/emergency-diagnostics/codes.db}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=========================================="
echo "Emergency Diagnostics Liberator - Testing"
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

# Test 1: Check Python installation
run_test \
    "Python 3.8+ installed" \
    "command -v python3 >/dev/null 2>&1"

# Test 2: Check Python version
run_test \
    "Python version >= 3.8" \
    "python3 --version | grep -qE 'Python 3\.[89]|Python 3\.1[0-9]|Python 3\.[2-9][0-9]'"

# Test 3: Check python-obd library
run_test \
    "python-obd library available" \
    "python3 -c 'import obd'"

# Test 4: Check python-can library
run_test \
    "python-can library available" \
    "python3 -c 'import can'"

# Test 5: Check SQLite
run_test \
    "SQLite available" \
    "python3 -c 'import sqlite3'"

# Test 6: Check pandas
run_test \
    "pandas available" \
    "python3 -c 'import pandas'"

# Test 7: Check matplotlib
run_test \
    "matplotlib available" \
    "python3 -c 'import matplotlib'"

# Test 8: Check code database
echo ""
echo "Checking code database..."
if [[ -f "$CODE_DB_PATH" ]]; then
    run_test \
        "Code database exists" \
        "[[ -f '$CODE_DB_PATH' ]]"

    # Test 9: Check database is valid SQLite
    run_test \
        "Database is valid SQLite" \
        "sqlite3 '$CODE_DB_PATH' 'SELECT name FROM sqlite_master LIMIT 1;' &>/dev/null"

    # Test 10: Check database has data
    CODE_COUNT=$(sqlite3 "$CODE_DB_PATH" "SELECT COUNT(*) FROM codes;" 2>/dev/null || echo "0")
    if [[ "$CODE_COUNT" -gt 0 ]]; then
        run_test \
            "Database has code entries" \
            "[[ $CODE_COUNT -gt 0 ]]"
    else
        echo -e "${YELLOW}Test 10: Database is empty${NC}"
        TOTAL_TESTS=$((TOTAL_TESTS + 1))
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
else
    echo -e "${YELLOW}Code database not found at $CODE_DB_PATH${NC}"
    echo "Run 'python3 scripts/setup-database.py' to create database"
    TOTAL_TESTS=$((TOTAL_TESTS + 3))
    FAILED_TESTS=$((FAILED_TESTS + 3))
fi

# Test 11: Check scripts exist
echo ""
echo "Checking required scripts..."
run_test \
    "setup.sh exists" \
    "[[ -f '$SCRIPT_DIR/setup.sh' ]]"

run_test \
    "run.sh exists" \
    "[[ -f '$SCRIPT_DIR/run.sh' ]]"

run_test \
    "test.sh exists" \
    "[[ -f '$SCRIPT_DIR/test.sh' ]]"

# Test 12: Check Python scripts exist
echo ""
echo "Checking Python scripts..."
run_test \
    "diagnostics.py exists" \
    "[[ -f '$SCRIPT_DIR/diagnostics.py' ]]"

run_test \
    "setup-database.py exists" \
    "[[ -f '$SCRIPT_DIR/setup-database.py' ]]"

# Test 13: Check log directory
echo ""
echo "Checking log directory..."
LOG_DIR=$(dirname "$DIAG_LOG_FILE")
if [[ -d "$LOG_DIR" ]]; then
    run_test \
        "Log directory exists" \
        "[[ -d '$LOG_DIR' ]]"

    # Test 14: Check if writable
    if [[ -w "$LOG_DIR" ]]; then
        run_test \
            "Log directory is writable" \
            "[[ -w '$LOG_DIR' ]]"
    else
        echo -e "${YELLOW}Log directory is not writable${NC}"
        TOTAL_TESTS=$((TOTAL_TESTS + 1))
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
else
    echo -e "${YELLOW}Log directory not found${NC}"
    TOTAL_TESTS=$((TOTAL_TESTS + 2))
    FAILED_TESTS=$((FAILED_TESTS + 2))
fi

# Test 15: Check .env.example exists
echo ""
echo "Checking configuration files..."
run_test \
    ".env.example exists" \
    "[[ -f '$PROJECT_ROOT/.env.example' ]]"

# Test 16: Check SKILL.md exists
run_test \
    "SKILL.md exists" \
    "[[ -f '$PROJECT_ROOT/SKILL.md' ]]"

# Test 17: Check tools.json exists
run_test \
    "tools.json exists" \
    "[[ -f '$PROJECT_ROOT/tools.json' ]]"

# Test 18: Check code database query
echo ""
echo "Testing database functionality..."
if [[ -f "$CODE_DB_PATH" ]]; then
    # Test query for common engine code
    ENGINE_CODES=$(sqlite3 "$CODE_DB_PATH" "SELECT COUNT(*) FROM codes WHERE spn >= 91 AND spn <= 250;" 2>/dev/null || echo "0")
    if [[ "$ENGINE_CODES" -gt 0 ]]; then
        run_test \
            "Database has engine codes" \
            "[[ $ENGINE_CODES -gt 0 ]]"
    else
        echo -e "${YELLOW}Test 18: No engine codes found in database${NC}"
        TOTAL_TESTS=$((TOTAL_TESTS + 1))
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi

    # Test code lookup
    CODE_DESC=$(sqlite3 "$CODE_DB_PATH" "SELECT description FROM codes WHERE spn = 91 AND fmi = 0;" 2>/dev/null | head -n 1)
    if [[ -n "$CODE_DESC" ]]; then
        run_test \
            "Can look up code descriptions" \
            "[[ -n '$CODE_DESC' ]]"
    else
        echo -e "${YELLOW}Test 19: Code lookup returned no results${NC}"
        TOTAL_TESTS=$((TOTAL_TESTS + 1))
        FAILED_TESTS=$((FAILED_TESTS + 1))
    fi
fi

# Test 20: Check CAN interface (optional)
echo ""
echo "Checking CAN interface (optional)..."
if ip link show can0 &>/dev/null; then
    run_test \
        "CAN interface can0 exists" \
        "ip link show can0 &>/dev/null"
else
    echo -e "${YELLOW}CAN interface can0 not found (optional for CAN-based diagnostics)${NC}"
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
    echo "Emergency diagnostics is ready to use."
    exit 0
else
    echo -e "${RED}Some tests failed${NC}"
    echo "Please fix the issues above before using the diagnostics."
    exit 1
fi
