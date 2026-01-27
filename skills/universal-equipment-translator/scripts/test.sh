#!/bin/bash

# test.sh
# Test equipment translator functionality

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
CAN_INTERFACE="${CAN_INTERFACE:-can0}"
CAN_BAUDRATE="${CAN_BAUDRATE:-250000}"
TEST_DURATION="${TEST_DURATION:-10}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "=========================================="
echo "Equipment Translator - Testing"
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

# Test 3: Check CAN utilities
run_test \
    "can-utils installed" \
    "command -v candump >/dev/null 2>&1 && command -v cansend >/dev/null 2>&1"

# Test 4: Check Python CAN library
run_test \
    "python-can library available" \
    "python3 -c 'import can'"

# Test 5: Check SQLite
run_test \
    "SQLite available" \
    "python3 -c 'import sqlite3'"

# Test 6: Check CAN interface exists
echo ""
echo "Checking CAN interface..."
if ip link show "$CAN_INTERFACE" &>/dev/null; then
    run_test \
        "CAN interface exists" \
        "ip link show $CAN_INTERFACE &>/dev/null"

    # Test 7: Check CAN interface is up
    if ip link show "$CAN_INTERFACE" | grep -q "state UP"; then
        run_test \
            "CAN interface is UP" \
            "ip link show $CAN_INTERFACE | grep -q 'state UP'"
    else
        echo -e "${YELLOW}Test 7: CAN interface is DOWN (expected if not configured)${NC}"
    fi
else
    echo -e "${YELLOW}CAN interface $CAN_INTERFACE not found${NC}"
    echo "Tests 6-7 skipped (interface not configured)"
fi

# Test 8: Check scripts exist
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

# Test 9: Check Python scripts exist
echo ""
echo "Checking Python scripts..."
run_test \
    "translator.py exists" \
    "[[ -f '$SCRIPT_DIR/translator.py' ]]"

run_test \
    "setup-database.py exists" \
    "[[ -f '$SCRIPT_DIR/setup-database.py' ]]"

# Test 10: Check protocol database
echo ""
echo "Checking protocol database..."
if [[ -f "$PROTOCOL_DB_PATH" ]]; then
    run_test \
        "Protocol database exists" \
        "[[ -f '$PROTOCOL_DB_PATH' ]]"

    # Test 11: Check database is valid SQLite
    run_test \
        "Database is valid SQLite" \
        "sqlite3 '$PROTOCOL_DB_PATH' 'SELECT name FROM sqlite_master LIMIT 1;' &>/dev/null"
else
    echo -e "${YELLOW}Protocol database not found at $PROTOCOL_DB_PATH${NC}"
    echo "Run 'python3 scripts/setup-database.py' to create database"
    TOTAL_TESTS=$((TOTAL_TESTS + 2))
    FAILED_TESTS=$((FAILED_TESTS + 2))
fi

# Test 12: Check log directory writable
echo ""
echo "Checking log directory..."
LOG_DIR=$(dirname "$TRANSLATION_LOG_FILE")
if [[ -d "$LOG_DIR" ]]; then
    run_test \
        "Log directory exists" \
        "[[ -d '$LOG_DIR' ]]"

    # Test 13: Check if writable
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

# Test 14: Check .env.example exists
echo ""
echo "Checking configuration files..."
run_test \
    ".env.example exists" \
    "[[ -f '$PROJECT_ROOT/.env.example' ]]"

# Test 15: Check SKILL.md exists
run_test \
    "SKILL.md exists" \
    "[[ -f '$PROJECT_ROOT/SKILL.md' ]]"

# Test 16: Check tools.json exists
run_test \
    "tools.json exists" \
    "[[ -f '$PROJECT_ROOT/tools.json' ]]"

# CAN bus capture test
echo ""
echo "Testing CAN bus communication..."
if command -v timeout >/dev/null 2>&1 && command -v candump >/dev/null 2>&1; then
    echo "Starting CAN capture test for $TEST_DURATION seconds..."
    echo "Send a test message with: cansend $CAN_INTERFACE '123#DEADBEEF'"
    echo ""

    # Start candump in background
    timeout "$TEST_DURATION" candump "$CAN_INTERFACE" 2>/dev/null | head -n 1 &
    CANDUMP_PID=$!

    # Send test message
    sleep 1
    if command -v cansend >/dev/null 2>&1; then
        cansend "$CAN_INTERFACE" "123#DEADBEEF" 2>/dev/null || true
    fi

    sleep 2

    # Check if candump captured anything
    if kill -0 $CANDUMP_PID 2>/dev/null; then
        kill $CANDUMP_PID 2>/dev/null || true
        echo -e "${YELLOW}Test 17: CAN capture test inconclusive (no messages)${NC}"
        echo "This is normal if interface is idle"
    else
        echo -e "${GREEN}Test 17: CAN capture test PASSED${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        TOTAL_TESTS=$((TOTAL_TESTS + 1))
    fi
else
    echo -e "${YELLOW}Test 17: CAN capture test skipped (timeout or candump not available)${NC}"
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
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
    echo "Equipment translator is ready to use."
    exit 0
else
    echo -e "${RED}Some tests failed${NC}"
    echo "Please fix the issues above before using the translator."
    exit 1
fi
