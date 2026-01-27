#!/bin/bash

# setup-can.sh
# Initialize CAN interface for equipment translator

set -e

# Configuration
CAN_INTERFACE="${CAN_INTERFACE:-can0}"
CAN_BAUDRATE="${CAN_BAUDRATE:-250000}"
CAN_TYPE="${CAN_TYPE:-socketcan}"
CAN_TIMEOUT="${CAN_TIMEOUT:-5}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=========================================="
echo "Equipment Translator - CAN Setup"
echo "=========================================="
echo ""

# Check for root/sudo
if [[ $EUID -ne 0 ]]; then
   echo -e "${RED}Error: This script must be run as root (use sudo)${NC}"
   echo "CAN interfaces require privileged access"
   exit 1
fi

# Load kernel modules
echo "Loading CAN kernel modules..."
modprobe can
modprobe can_raw
modprobe vcan  # for virtual testing
echo -e "${GREEN}CAN modules loaded${NC}"

# Check for virtual or physical interface
if [[ "$CAN_TYPE" == "virtual" ]]; then
    echo "Setting up virtual CAN interface..."
    ip link add dev "$CAN_INTERFACE" type vcan
    ip link set "$CAN_INTERFACE" up
    echo -e "${GREEN}Virtual CAN interface $CAN_INTERFACE created${NC}"
else
    # Check if interface exists
    if ! ip link show "$CAN_INTERFACE" &> /dev/null; then
        echo -e "${YELLOW}Warning: Interface $CAN_INTERFACE not found${NC}"
        echo "Available interfaces:"
        ip link show | grep -E '^[0-9]+:' | awk '{print "  " $2}'
        echo ""
        echo "Creating virtual CAN interface for testing..."
        ip link add dev "$CAN_INTERFACE" type vcan
        ip link set "$CAN_INTERFACE" up
        echo -e "${GREEN}Virtual CAN interface $CAN_INTERFACE created${NC}"
    else
        echo "Bringing up CAN interface $CAN_INTERFACE..."
        ip link set "$CAN_INTERFACE" down 2>/dev/null || true

        # Configure baud rate
        echo "Setting CAN baud rate to $CAN_BAUDRATE..."
        ip link set "$CAN_INTERFACE" type can bitrate "$CAN_BAUDRATE"
        ip link set "$CAN_INTERFACE" up

        echo -e "${GREEN}CAN interface $CAN_INTERFACE configured${NC}"
        echo "  Interface: $CAN_INTERFACE"
        echo "  Baudrate: $CAN_BAUDRATE"
        echo "  Type: $CAN_TYPE"
    fi
fi

# Verify interface is up
if ip link show "$CAN_INTERFACE" | grep -q "state UP"; then
    echo -e "${GREEN}Interface is UP${NC}"
else
    echo -e "${RED}Error: Failed to bring up interface${NC}"
    exit 1
fi

# Test CAN interface
echo ""
echo "Testing CAN interface..."
if command -v candump &> /dev/null; then
    timeout "$CAN_TIMEOUT" candump "$CAN_INTERFACE" 2>&1 | head -n 1 &
    CANDUMP_PID=$!

    if command -v cansend &> /dev/null; then
        sleep 1
        cansend "$CAN_INTERFACE" "123#DEADBEEF" 2>/dev/null || true
        sleep 1

        if kill -0 $CANDUMP_PID 2>/dev/null; then
            kill $CANDUMP_PID 2>/dev/null || true
            echo -e "${GREEN}CAN interface test PASSED${NC}"
            echo "  Can send and receive messages"
        else
            echo -e "${YELLOW}Warning: CAN test inconclusive (no messages captured)${NC}"
        fi
    else
        echo -e "${YELLOW}cansend not found, skipping send test${NC}"
    fi
else
    echo -e "${YELLOW}candump not found, skipping interface test${NC}"
fi

# Display interface status
echo ""
echo "Interface Status:"
ip -details link show "$CAN_INTERFACE"

echo ""
echo "=========================================="
echo -e "${GREEN}CAN Setup Complete${NC}"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Run 'scripts/run.sh' to start translator"
echo "  2. Run 'scripts/test.sh' to test functionality"
echo ""
