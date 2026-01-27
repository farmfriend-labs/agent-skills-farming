#!/usr/bin/env python3
"""
Storage Monitor - Monitor seed storage conditions
"""

import os
import time
import json
from datetime import datetime
from pathlib import Path


# Configuration
ALERT_TEMP_MIN = float(os.environ.get('ALERT_TEMP_MIN_CELSIUS', 0))
ALERT_TEMP_MAX = float(os.environ.get('ALERT_TEMP_MAX_CELSIUS', 15))
ALERT_HUMIDITY_MIN = float(os.environ.get('ALERT_HUMIDITY_MIN_PCT', 30))
ALERT_HUMIDITY_MAX = float(os.environ.get('ALERT_HUMIDITY_MAX_PCT', 70))

MONITOR_LOG = '/var/lib/seed-sovereignty/monitor.log'


def check_conditions():
    """Check current storage conditions"""
    print("\n=== Storage Conditions Check ===\n")

    # Try to read from sensor (lm-sensors or DHT22)
    temp = read_temperature()
    humidity = read_humidity()

    if temp is None:
        print("⚠ Could not read temperature (no sensor or permission)")
        temp = float(input("Enter current temperature (°C): "))
    else:
        print(f"Temperature: {temp:.1f}°C ({temp * 9/5 + 32:.1f}°F)")

    if humidity is None:
        print("⚠ Could not read humidity (no sensor or permission)")
        humidity = float(input("Enter current humidity (%): "))
    else:
        print(f"Humidity: {humidity:.1f}%")

    # Check against thresholds
    print("\nStatus:")

    if temp < ALERT_TEMP_MIN:
        print(f"  ✗ Temperature too low (min: {ALERT_TEMP_MIN}°C)")
        print("    Action: Move seeds to warmer location")
    elif temp > ALERT_TEMP_MAX:
        print(f"  ✗ Temperature too high (max: {ALERT_TEMP_MAX}°C)")
        print("    Action: Move seeds to cooler location")
    else:
        print(f"  ✓ Temperature within acceptable range")

    if humidity < ALERT_HUMIDITY_MIN:
        print(f"  ✗ Humidity too low (min: {ALERT_HUMIDITY_MIN}%)")
        print("    Action: Add humidity pack or desiccant")
    elif humidity > ALERT_HUMIDITY_MAX:
        print(f"  ✗ Humidity too high (max: {ALERT_HUMIDITY_MAX}%)")
        print("    Action: Improve ventilation or add desiccant")
    else:
        print(f"  ✓ Humidity within acceptable range")

    # Log reading
    log_reading(temp, humidity)


def read_temperature():
    """Read temperature from sensor"""
    # Try lm-sensors
    try:
        import subprocess
        result = subprocess.run(['sensors'], capture_output=True, text=True, timeout=5)
        # Parse output (simplified)
        for line in result.stdout.split('\n'):
            if 'Core' in line or 'Tdie' in line or 'Package' in line:
                # Extract temperature
                import re
                match = re.search(r'(\d+\.\d+)', line)
                if match:
                    # Assume sensor reports °C
                    return float(match.group(1))
    except Exception:
        pass

    # Try DHT22 (requires adafruit_dht library)
    try:
        import board
        import adafruit_dht
        dht = adafruit_dht.DHT22(board.D4)
        temp = dht.temperature
        dht.exit()
        return temp
    except Exception:
        pass

    return None


def read_humidity():
    """Read humidity from sensor"""
    # Try DHT22
    try:
        import board
        import adafruit_dht
        dht = adafruit_dht.DHT22(board.D4)
        humidity = dht.humidity
        dht.exit()
        return humidity
    except Exception:
        pass

    return None


def log_reading(temp, humidity):
    """Log temperature and humidity reading"""
    log_dir = Path(MONITOR_LOG).parent
    log_dir.mkdir(parents=True, exist_ok=True)

    reading = {
        'timestamp': datetime.now().isoformat(),
        'temperature_celsius': temp,
        'humidity_percent': humidity,
        'temp_alert': temp < ALERT_TEMP_MIN or temp > ALERT_TEMP_MAX,
        'humidity_alert': humidity < ALERT_HUMIDITY_MIN or humidity > ALERT_HUMIDITY_MAX
    }

    with open(MONITOR_LOG, 'a') as f:
        f.write(json.dumps(reading) + '\n')

    print(f"\n✓ Reading logged to {MONITOR_LOG}")


def show_history():
    """Show storage conditions history"""
    if not os.path.exists(MONITOR_LOG):
        print(f"\nNo history found at {MONITOR_LOG}")
        return

    print("\n=== Storage Conditions History ===\n")

    readings = []
    with open(MONITOR_LOG, 'r') as f:
        for line in f:
            try:
                readings.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    if not readings:
        print("No readings recorded")
        return

    # Show last 20 readings
    recent = readings[-20:]

    print(f"{'Timestamp':<20} {'Temp (°C)':<12} {'Humidity (%)':<15} {'Status':<10}")
    print("-" * 60)

    for reading in recent:
        timestamp = reading['timestamp'][:19]
        temp = f"{reading['temperature_celsius']:.1f}"
        humidity = f"{reading['humidity_percent']:.1f}"

        status = "OK"
        if reading['temp_alert'] or reading['humidity_alert']:
            status = "ALERT"

        print(f"{timestamp:<20} {temp:<12} {humidity:<15} {status:<10}")


def main():
    """Main entry point"""
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == 'check':
            check_conditions()
        elif command == 'history':
            show_history()
        else:
            print(f"Unknown command: {command}")
            print("Usage: python3 storage_monitor.py [check|history]")
    else:
        check_conditions()


if __name__ == '__main__':
    main()
