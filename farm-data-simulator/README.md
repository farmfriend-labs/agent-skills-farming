# Farm Data Simulator

Edge device and smart device simulator for agricultural AI skill development and testing.

## Purpose

Generate realistic farm data and telemetry for:
- Skill development and testing
- Network environment simulation
- Multi-agent testing
- Integration with FF-Terminal-Skills testing program
- Farm data visualization and analysis

## Architecture

```
farm-data-simulator/
├── README.md              # This file
├── setup.sh               # Installation and setup
├── run.sh                 # Main entry point
├── config/                # Configuration files
│   ├── can-bus.json       # CAN bus simulation config
│   ├── sensors.json       # Sensor data stream config
│   ├── markets.json      # Market data simulation config
│   ├── weather.json      # Weather data simulation config
│   └── equipment.json    # Equipment telemetry config
├── simulator/
│   ├── can_bus.py         # CAN bus traffic simulator
│   ├── sensor_stream.py   # Sensor data simulator
│   ├── equipment_telemetry.py  # Equipment telemetry simulator
│   ├── market_data.py     # Market data simulator
│   ├── weather_feed.py    # Weather data simulator
│   └── iot_devices.py    # IoT device simulator
└── outputs/               # Simulated data outputs
    ├── can-traffic.log    # CAN traffic logs
    ├── sensor-data.json   # Sensor data JSON
    ├── telemetry.json     # Equipment telemetry JSON
    ├── market-data.json   # Market data JSON
    └── weather.json      # Weather data JSON
```

## Features

### 1. CAN Bus Simulator

Generates realistic CAN bus traffic for agricultural equipment:

- ISO 11783 standard messages
- Manufacturer-specific messages (John Deere, Case IH, AGCO)
- Variable rate application data
- Guidance and steering data
- Section control messages
- Diagnostic and status messages

**Output:** `outputs/can-traffic.log`

### 2. Sensor Stream Simulator

Generates continuous sensor data streams:

- Soil moisture sensors (multiple fields)
- Temperature sensors (air, soil, equipment)
- Humidity sensors
- pH sensors (soil, water)
- Flow rate sensors (irrigation)
- Pressure sensors (hydraulics)

**Output:** `outputs/sensor-data.json` (streaming JSON)

### 3. Equipment Telemetry Simulator

Generates equipment operation data:

- Tractor status (RPM, fuel, temperature, hours)
- Planter operation (planting rate, seed usage, depth)
- Combine operation (yield, moisture, throughput)
- Sprayer operation (rate, pressure, coverage)

**Output:** `outputs/telemetry.json` (periodic updates)

### 4. Market Data Simulator

Generates agricultural market data:

- Commodity prices (corn, soybeans, wheat, cotton)
- Local cash bids and basis
- Futures prices (CBOT, KCBT)
- Premium opportunities (organic, non-GMO)
- Feed and fuel prices

**Output:** `outputs/market-data.json` (real-time updates)

### 5. Weather Feed Simulator

Generates weather data:

- Current conditions (temperature, humidity, wind, precipitation)
- Forecast data (hourly, daily, extended)
- Alerts (freeze, wind, precipitation, heat)
- Growing degree days (GDD)
- Evapotranspiration (ET) estimates

**Output:** `outputs/weather.json` (regular updates)

### 6. IoT Device Simulator

Generates smart device messages:

- Smart irrigation controllers
- Climate control systems (greenhouses)
- Livestock monitors
- Storage monitoring (grain bins, cold storage)
- Security and access control

**Output:** `outputs/iot-messages.json` (event-based)

## Installation

### Prerequisites

- Python 3.8+
- pip3 (Python package manager)
- Bash shell

### Setup

```bash
# Navigate to simulator directory
cd farm-data-simulator

# Run setup script
chmod +x setup.sh
./setup.sh

# This will:
# 1. Create virtual environment
# 2. Install Python dependencies
# 3. Create output directories
# 4. Initialize configuration files
# 5. Verify installation
```

### Dependencies

```bash
# Python dependencies installed by setup.sh
pip3 install -r requirements.txt

# Core dependencies:
# - python-can (CAN bus)
# - requests (HTTP)
# - numpy (numerical computing)
# - pandas (data analysis)
# - pyyaml (configuration)
# - schedule (task scheduling)
```

## Usage

### Start All Simulators

```bash
# Start all simulators
chmod +x run.sh
./run.sh

# Or start specific simulators:
./run.sh --can-bus
./run.sh --sensors
./run.sh --equipment
./run.sh --markets
./run.sh --weather
./run.sh --iot
```

### Start Individual Simulator

```bash
# Start CAN bus simulator only
python3 simulator/can_bus.py --config config/can-bus.json

# Start sensor stream simulator
python3 simulator/sensor_stream.py --config config/sensors.json

# Start equipment telemetry simulator
python3 simulator/equipment_telemetry.py --config config/equipment.json
```

### Output Files

All outputs written to `outputs/` directory:

```bash
# Monitor CAN traffic
tail -f outputs/can-traffic.log

# Monitor sensor data
watch -n 1 cat outputs/sensor-data.json

# Monitor equipment telemetry
watch -n 5 cat outputs/telemetry.json

# Monitor market data
watch -n 60 cat outputs/market-data.json
```

## Configuration

### CAN Bus Configuration

`config/can-bus.json`:

```json
{
  "interface": "vcan0",
  "baudrate": 250000,
  "manufacturers": ["Universal", "John Deere", "Case IH", "AGCO"],
  "message_rate": 10,
  "include_standard": true,
  "include_proprietary": true
}
```

### Sensor Configuration

`config/sensors.json`:

```json
{
  "fields": [
    {
      "id": "field-1",
      "name": "North Field",
      "soil_moisture_sensors": 4,
      "temperature_sensors": 2,
      "ph_sensors": 1
    },
    {
      "id": "field-2",
      "name": "South Field",
      "soil_moisture_sensors": 3,
      "temperature_sensors": 2,
      "ph_sensors": 1
    }
  ],
  "update_interval_seconds": 30
}
```

### Market Configuration

`config/markets.json`:

```json
{
  "commodities": ["corn", "soybeans", "wheat", "cotton"],
  "update_interval_minutes": 15,
  "include_futures": true,
  "include_local_bids": true,
  "location": "Cedar Creek, TX"
}
```

### Weather Configuration

`config/weather.json`:

```json
{
  "location": "Cedar Creek, TX",
  "update_interval_minutes": 15,
  "include_forecast": true,
  "include_alerts": true,
  "gdd_base_temp": 50
}
```

## Integration with Skills

### Connect Skills to Simulator

Skills can read simulator outputs for testing:

```bash
# Example: Read sensor data
cat outputs/sensor-data.json | jq '.fields[] | select(.id == "field-1")'

# Example: Read equipment telemetry
cat outputs/telemetry.json | jq '.equipment[] | select(.type == "tractor")'

# Example: Monitor CAN traffic
candump can0 -l | tee -a outputs/can-traffic.log
```

### FF-Terminal-Skills Testing

Simulator designed to work with FF-Terminal-Skills testing program:

1. Start simulator
2. Configure skill to read from simulator outputs
3. Run skill tests against realistic data
4. Validate skill responses

### Multi-Agent Testing

Multiple agents can connect to simulator outputs simultaneously:

```bash
# Agent 1: Read CAN traffic
tail -f outputs/can-traffic.log | agent-1-process

# Agent 2: Read sensor data
tail -f outputs/sensor-data.json | agent-2-process

# Agent 3: Read market data
tail -f outputs/market-data.json | agent-3-process
```

## Real-World Data Sources

### Weather Data

- **Primary:** wttr.in (free, no API key)
- **Alternative:** OpenWeatherMap (free tier)
- **Alternative:** NOAA (US only, free)

### Market Data

- **Primary:** Real-time simulation (for development)
- **Production:** USDA AMS Market News
- **Production:** CBOT/KCBT futures APIs (paid)
- **Production:** Local elevator APIs

### Equipment Data

- **Primary:** CAN bus traffic from real equipment
- **Simulation:** Manufacturer specifications and real-world patterns
- **Validation:** Field testing with actual equipment

## Advanced Usage

### Custom Sensor Types

Add custom sensor types to configuration:

```json
{
  "sensors": [
    {
      "type": "custom_soil_sensor",
      "id": "sensor-001",
      "field": "field-1",
      "parameters": {
        "range_min": 0,
        "range_max": 100,
        "update_interval": 60,
        "units": "mV"
      }
    }
  ]
}
```

### Data Export

Export simulated data for analysis:

```bash
# Export to CSV
python3 simulator/export_data.py --format csv --output data.csv

# Export to database
python3 simulator/export_data.py --format sqlite --output data.db
```

### Playback Mode

Replay previously recorded data:

```bash
# Replay CAN traffic
python3 simulator/can_bus.py --mode replay --file outputs/can-traffic.log

# Replay sensor data
python3 simulator/sensor_stream.py --mode replay --file outputs/sensor-data.json
```

## Troubleshooting

### CAN Interface Issues

If CAN interface fails to start:

```bash
# Check for vcan module
lsmod | grep vcan

# Load vcan module
sudo modprobe vcan

# Create virtual CAN interface
sudo ip link add dev vcan0 type vcan
sudo ip link set vcan0 up
```

### Sensor Data Not Updating

Check configuration and update interval:

```bash
# Verify configuration
cat config/sensors.json | jq '.update_interval_seconds'

# Restart sensor simulator
pkill -f sensor_stream.py
python3 simulator/sensor_stream.py --config config/sensors.json
```

### Output Files Not Created

Check output directory permissions:

```bash
# Check directory
ls -la outputs/

# Fix permissions if needed
chmod 755 outputs/
```

## License

MIT License - Free to use, modify, and distribute.

## Support

For issues, questions, or contributions:
- GitHub Issues: https://github.com/farmfriend-labs/agent-skills-farming/issues
- Email: farmfriend.labs@gmail.com
