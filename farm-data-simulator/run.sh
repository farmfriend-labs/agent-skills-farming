#!/bin/bash

# run.sh
# Farm Data Simulator - Main entry point

set -e

# Load environment
SIMULATOR_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SIMULATOR_DIR"

# Activate virtual environment
if [[ -d "$SIMULATOR_DIR/venv" ]]; then
    source "$SIMULATOR_DIR/venv/bin/activate"
else
    echo "Error: Virtual environment not found"
    echo "Run ./setup.sh first"
    exit 1
fi

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Parse command line arguments
START_CAN_BUS=false
START_SENSORS=false
START_EQUIPMENT=false
START_MARKETS=false
START_WEATHER=false
START_IOT=false
START_ALL=true

while [[ $# -gt 0 ]]; do
    case $1 in
        --can-bus)
            START_CAN_BUS=true
            START_ALL=false
            shift
            ;;
        --sensors)
            START_SENSORS=true
            START_ALL=false
            shift
            ;;
        --equipment)
            START_EQUIPMENT=true
            START_ALL=false
            shift
            ;;
        --markets)
            START_MARKETS=true
            START_ALL=false
            shift
            ;;
        --weather)
            START_WEATHER=true
            START_ALL=false
            shift
            ;;
        --iot)
            START_IOT=true
            START_ALL=false
            shift
            ;;
        --help)
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  --can-bus      Start CAN bus simulator only"
            echo "  --sensors       Start sensor stream simulator only"
            echo "  --equipment     Start equipment telemetry simulator only"
            echo "  --markets        Start market data simulator only"
            echo "  --weather        Start weather feed simulator only"
            echo "  --iot            Start IoT device simulator only"
            echo "  --help           Show this help message"
            echo ""
            echo "If no options specified, all simulators are started"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

echo "=========================================="
echo "Farm Data Simulator - Starting"
echo "=========================================="
echo ""

# Function to start simulator in background
start_simulator() {
    local name=$1
    local script=$2
    local config=$3
    local log_file=$4

    echo "Starting $name..."
    python3 "$script" --config "$config" > "$log_file" 2>&1 &
    local pid=$!
    echo -e "${GREEN}$name started (PID: $pid)${NC}"
    echo "  Log: $log_file"
    echo "$pid" > "$SIMULATOR_DIR/pids/${name}.pid"

    # Give it time to start
    sleep 2

    # Check if still running
    if kill -0 $pid 2>/dev/null; then
        echo -e "${GREEN}$name running${NC}"
    else
        echo -e "${RED}$name failed to start${NC}"
        cat "$log_file"
        return 1
    fi
    echo ""
}

# Create PID directory
mkdir -p "$SIMULATOR_DIR/pids"

# Start requested simulators
if $START_ALL || $START_CAN_BUS; then
    start_simulator \
        "CAN Bus Simulator" \
        "$SIMULATOR_DIR/simulator/can_bus.py" \
        "$SIMULATOR_DIR/config/can-bus.json" \
        "$SIMULATOR_DIR/outputs/can-bus.log"
fi

if $START_ALL || $START_SENSORS; then
    start_simulator \
        "Sensor Stream Simulator" \
        "$SIMULATOR_DIR/simulator/sensor_stream.py" \
        "$SIMULATOR_DIR/config/sensors.json" \
        "$SIMULATOR_DIR/outputs/sensors.log"
fi

if $START_ALL || $START_EQUIPMENT; then
    start_simulator \
        "Equipment Telemetry Simulator" \
        "$SIMULATOR_DIR/simulator/equipment_telemetry.py" \
        "$SIMULATOR_DIR/config/equipment.json" \
        "$SIMULATOR_DIR/outputs/equipment.log"
fi

if $START_ALL || $START_MARKETS; then
    start_simulator \
        "Market Data Simulator" \
        "$SIMULATOR_DIR/simulator/market_data.py" \
        "$SIMULATOR_DIR/config/markets.json" \
        "$SIMULATOR_DIR/outputs/markets.log"
fi

if $START_ALL || $START_WEATHER; then
    start_simulator \
        "Weather Feed Simulator" \
        "$SIMULATOR_DIR/simulator/weather_feed.py" \
        "$SIMULATOR_DIR/config/weather.json" \
        "$SIMULATOR_DIR/outputs/weather.log"
fi

if $START_ALL || $START_IOT; then
    start_simulator \
        "IoT Device Simulator" \
        "$SIMULATOR_DIR/simulator/iot_devices.py" \
        "$SIMULATOR_DIR/config/iot.example.json" \
        "$SIMULATOR_DIR/outputs/iot.log"
fi

echo "=========================================="
echo -e "${GREEN}All simulators started${NC}"
echo "=========================================="
echo ""
echo "Monitor outputs:"
echo "  CAN traffic:      tail -f outputs/can-traffic.log"
echo "  Sensor data:      tail -f outputs/sensor-data.json"
echo "  Equipment data:    tail -f outputs/telemetry.json"
echo "  Market data:      tail -f outputs/market-data.json"
echo "  Weather data:      tail -f outputs/weather.json"
echo "  IoT messages:     tail -f outputs/iot-messages.json"
echo ""
echo "Stop all simulators:"
echo "  ./run.sh --stop"
echo ""
echo "Stop individual simulator:"
echo "  kill \$(cat pids/can-bus.pid)"
echo ""

# Trap Ctrl+C to stop all simulators
trap 'echo "Stopping all simulators..."; kill \$(cat pids/*.pid 2>/dev/null) 2>/dev/null; exit 0' INT TERM

# Wait for Ctrl+C
if $START_ALL; then
    echo "Press Ctrl+C to stop all simulators"
    wait
fi
