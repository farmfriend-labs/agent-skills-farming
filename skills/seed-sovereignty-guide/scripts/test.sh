#!/bin/bash

# test.sh
# Comprehensive test suite for seed sovereignty guide

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=========================================="
echo "Seed Sovereignty Guide - Test Suite"
echo "=========================================="
echo ""

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Test function
run_test() {
    local test_name="$1"
    local test_command="$2"

    echo "Testing: $test_name"

    if eval "$test_command" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ PASSED${NC}: $test_name"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}✗ FAILED${NC}: $test_name"
        ((TESTS_FAILED++))
    fi
    echo ""
}

# Check Python installation
echo "=== Environment Checks ==="
run_test "Python 3 installed" "command -v python3"
run_test "Python 3 version >= 3.8" "python3 -c 'import sys; exit(0 if sys.version_info >= (3, 8) else 1)'"

# Check database
echo "=== Database Tests ==="
if [ -f "${SEED_DB_PATH:-/opt/seed-sovereignty/seeds.db}" ]; then
    run_test "Database file exists" "true"
    run_test "Database readable" "sqlite3 ${SEED_DB_PATH:-/opt/seed-sovereignty/seeds.db} 'SELECT 1' > /dev/null 2>&1"
else
    echo -e "${YELLOW}⚠ Database not found - run setup.sh first${NC}"
    echo ""
fi

# Test Python scripts (if database exists)
if [ -f "${SEED_DB_PATH:-/opt/seed-sovereignty/seeds.db}" ]; then
    echo "=== Script Tests ==="
    run_test "seed_manager.py import" "python3 -c 'import scripts.seed_manager'"
    run_test "germination_test.py import" "python3 -c 'import scripts.germination_test'"
    run_test "viability_checker.py import" "python3 -c 'import scripts.viability_checker'"
    run_test "crop_lookup.py import" "python3 -c 'import scripts.crop_lookup'"
    run_test "isolation_calculator.py import" "python3 -c 'import scripts.isolation_calculator'"
    run_test "storage_monitor.py import" "python3 -c 'import scripts.storage_monitor'"
    run_test "export_inventory.py import" "python3 -c 'import scripts.export_inventory'"

    echo "=== Database Operations Tests ==="
    # Test database queries (read-only)
    run_test "Query seeds table" "sqlite3 ${SEED_DB_PATH:-/opt/seed-sovereignty/seeds.db} 'SELECT COUNT(*) FROM seeds' > /dev/null 2>&1"
    run_test "Query germination_tests table" "sqlite3 ${SEED_DB_PATH:-/opt/seed-sovereignty/seeds.db} 'SELECT COUNT(*) FROM germination_tests' > /dev/null 2>&1"
    run_test "Query variety_characteristics table" "sqlite3 ${SEED_DB_PATH:-/opt/seed-sovereignty/seeds.db} 'SELECT COUNT(*) FROM variety_characteristics' > /dev/null 2>&1"
fi

# Test optional dependencies
echo "=== Optional Dependencies ==="
run_test "lm-sensors installed" "command -v sensors"
run_test "python-requests available" "python3 -c 'import requests' 2> /dev/null"

# Test script permissions
echo "=== Script Permissions ==="
run_test "setup.sh executable" "test -x scripts/setup.sh"
run_test "run.sh executable" "test -x scripts/run.sh"
run_test "test.sh executable" "test -x scripts/test.sh"
run_test "Python scripts executable" "test -x scripts/seed_manager.py"

# Test export directory
echo "=== Export Directory Tests ==="
EXPORT_DIR="${EXPORT_PATH:-/var/lib/seed-sovereignty/exports}"
if [ -d "$EXPORT_DIR" ] || mkdir -p "$EXPORT_DIR" 2>/dev/null; then
    run_test "Export directory writable" "touch $EXPORT_DIR/test_write.tmp && rm $EXPORT_DIR/test_write.tmp"
else
    echo -e "${YELLOW}⚠ Cannot create export directory${NC}"
    echo ""
fi

# Test example functionality
echo "=== Crop Lookup Tests ==="
run_test "Lookup tomato" "python3 scripts/crop_lookup.py tomato | grep -q 'Self-pollinating'"
run_test "Lookup corn" "python3 scripts/crop_lookup.py corn | grep -q 'Cross-pollinating'"
run_test "List all crops" "python3 scripts/crop_lookup.py list | grep -q 'tomato'"

# Summary
echo "=========================================="
echo "Test Summary"
echo "=========================================="
echo -e "${GREEN}Passed: $TESTS_PASSED${NC}"
if [ $TESTS_FAILED -gt 0 ]; then
    echo -e "${RED}Failed: $TESTS_FAILED${NC}"
else
    echo "Failed: 0"
fi
echo "Total: $((TESTS_PASSED + TESTS_FAILED))"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed. Check the output above for details.${NC}"
    exit 1
fi
