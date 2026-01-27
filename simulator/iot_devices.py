#!/usr/bin/env python3
"""
iot_devices.py - IoT Device Simulator
Generates realistic IoT device messages for smart farm devices.
"""

import sys
import json
import time
import argparse
import logging
import random
from typing import Dict, List, Any
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('IoTDeviceSimulator')


@dataclass
class IoTMessage:
    """Represents an IoT device message."""
    device_id: str
    device_type: str
    device_name: str
    location_id: str
    message_type: str
    data: Dict[str, Any]
    timestamp: str
    status: str


class IoTDeviceSimulator:
    """Simulates IoT device messages for smart farm devices."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.output_file = None
        self.devices = config.get('devices', [])

        # Device state tracking
        self.device_states = {}

        # Setup output
        self.setup_output()

    def setup_output(self):
        """Setup output file."""
        output_dir = Path(__file__).parent.parent / "outputs"
        output_dir.mkdir(exist_ok=True)

        self.output_file = output_dir / "iot-messages.json"
        logger.info(f"Output file: {self.output_file}")

    def initialize_device_state(self, device: Dict):
        """Initialize device state."""
        device_id = device['id']
        self.device_states[device_id] = {
            'last_message_time': time.time(),
            'message_count': 0,
            'status': 'online',
            'sensor_values': {},
            'action_states': {}
        }

        # Initialize sensor values
        for sensor_name, sensor_def in device.get('sensors', {}).items():
            if 'range' in sensor_def:
                min_val, max_val = sensor_def['range']
                self.device_states[device_id]['sensor_values'][sensor_name] = random.uniform(min_val, max_val)
            elif 'values' in sensor_def:
                self.device_states[device_id]['sensor_values'][sensor_name] = random.choice(sensor_def['values'])

    def update_device_state(self, device: Dict, device_id: str):
        """Update device state based on configuration."""
        state = self.device_states[device_id]

        # Update sensor values
        for sensor_name, sensor_def in device.get('sensors', {}).items():
            # Only update some sensors periodically
            if random.random() < 0.3:
                if 'range' in sensor_def:
                    min_val, max_val = sensor_def['range']
                    change = random.uniform(-max_val*0.1, max_val*0.1)
                    current = state['sensor_values'].get(sensor_name, 0)
                    new_value = max(min_val, min(max_val, current + change))
                    state['sensor_values'][sensor_name] = new_value
                elif 'values' in sensor_def:
                    state['sensor_values'][sensor_name] = random.choice(sensor_def['values'])

        # Update action states
        for action_name, action_def in device.get('actions', {}).items():
            if 'values' in action_def:
                # Randomly trigger actions occasionally
                if random.random() < 0.05:
                    state['action_states'][action_name] = random.choice(action_def['values'])

        state['last_message_time'] = time.time()
        state['message_count'] += 1

    def generate_device_message(self, device: Dict) -> IoTMessage:
        """Generate a message from a device."""
        device_id = device['id']
        device_type = device['type']
        device_name = device['name']
        location_id = device.get('location_id', 'unknown')

        # Update device state
        if device_id not in self.device_states:
            self.initialize_device_state(device)

        self.update_device_state(device, device_id)

        state = self.device_states[device_id]

        # Determine message type based on device type
        message_type = 'status_update'
        if device_type == 'irrigation_controller':
            message_type = random.choice(['status_update', 'valve_change', 'pressure_change'])
        elif device_type == 'climate_controller':
            message_type = random.choice(['status_update', 'temperature_change', 'humidity_change'])
        elif device_type == 'livestock_monitor':
            message_type = random.choice(['status_update', 'animal_count_change', 'feed_level_alert'])
        elif device_type == 'storage_monitor':
            message_type = random.choice(['status_update', 'temperature_alert', 'moisture_alert'])
        elif device_type == 'gate_controller':
            message_type = random.choice(['status_update', 'gate_open', 'gate_close', 'vehicle_detected'])

        # Build message data
        message_data = {
            'sensor_values': state['sensor_values'],
            'action_states': state['action_states'],
            'device_status': state['status']
        }

        # Add device-specific data
        if device_type == 'irrigation_controller':
            message_data['zones'] = device.get('zones', 0)
            message_data['valve_positions'] = state['sensor_values'].get('valve_status', 'unknown')
        elif device_type == 'climate_controller':
            message_data['vent_position'] = state['sensor_values'].get('vent_position', 0)
            message_data['co2_level'] = state['sensor_values'].get('co2_level', 400)
        elif device_type == 'livestock_monitor':
            message_data['animal_count'] = state['sensor_values'].get('animal_count', 0)
        elif device_type == 'storage_monitor':
            message_data['grain_level'] = state['sensor_values'].get('level', 0)
            message_data['aeration_status'] = state['sensor_values'].get('aeration_status', 'off')
        elif device_type == 'gate_controller':
            message_data['gate_position'] = state['sensor_values'].get('gate_status', 'closed')
            message_data['battery_level'] = state['sensor_values'].get('battery_level', 100)

        # Determine status
        status = 'normal'
        if random.random() < 0.02:
            status = 'warning'
        elif random.random() < 0.01:
            status = 'alert'

        message = IoTMessage(
            device_id=device_id,
            device_type=device_type,
            device_name=device_name,
            location_id=location_id,
            message_type=message_type,
            data=message_data,
            timestamp=datetime.utcnow().isoformat(),
            status=status
        )

        return message

    def generate_all_messages(self) -> Dict:
        """Generate messages from all devices."""
        all_messages = {
            'timestamp': datetime.utcnow().isoformat(),
            'device_count': len(self.devices),
            'messages': []
        }

        for device in self.devices:
            message = self.generate_device_message(device)
            all_messages['messages'].append(asdict(message))

        return all_messages

    def write_output(self, data: Dict):
        """Write IoT messages to output file."""
        with open(self.output_file, 'w') as f:
            json.dump(data, f, indent=2)

    def run(self, duration_seconds: int = None):
        """Run IoT device simulator."""
        logger.info("Starting IoT device simulator...")
        logger.info(f"Devices: {len(self.devices)}")

        device_types = {}
        for device in self.devices:
            device_type = device.get('type', 'unknown')
            device_types[device_type] = device_types.get(device_type, 0) + 1

        for device_type, count in device_types.items():
            logger.info(f"  {device_type}: {count}")

        start_time = time.time()
        update_count = 0

        try:
            while duration_seconds is None or time.time() - start_time < duration_seconds:
                # Generate device messages
                data = self.generate_all_messages()

                # Write output
                self.write_output(data)
                update_count += 1

                logger.debug(f"Update {update_count}: {len(data['messages'])} device messages")

                # Find minimum message interval
                min_interval = 30  # Default 30 seconds
                for device in self.devices:
                    interval = device.get('message_interval', 30)
                    if interval < min_interval:
                        min_interval = interval

                # Sleep for minimum interval
                time.sleep(min_interval)

        except KeyboardInterrupt:
            logger.info("Interrupted by user")
        finally:
            logger.info(f"Sent {update_count} updates")
            logger.info(f"Output written to: {self.output_file}")

    def get_stats(self) -> Dict:
        """Get simulator statistics."""
        device_types = {}
        for device in self.devices:
            device_type = device.get('type', 'unknown')
            device_types[device_type] = device_types.get(device_type, 0) + 1

        return {
            "devices": len(self.devices),
            "device_types": device_types,
            "device_states": len(self.device_states),
        }


def main():
    parser = argparse.ArgumentParser(description="IoT Device Simulator")

    parser.add_argument("--config", "-c", required=True,
                        help="Configuration file (JSON)")
    parser.add_argument("--duration", "-d", type=int,
                        help="Duration in seconds (default: run forever)")
    parser.add_argument("--stats", "-s", action="store_true",
                        help="Print statistics and exit")

    args = parser.parse_args()

    # Load configuration
    try:
        with open(args.config, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {args.config}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in configuration: {e}")
        sys.exit(1)

    # Create simulator
    simulator = IoTDeviceSimulator(config)

    # Print stats and exit
    if args.stats:
        stats = simulator.get_stats()
        print(json.dumps(stats, indent=2))
        return

    # Run simulator
    simulator.run(duration_seconds=args.duration)


if __name__ == "__main__":
    main()
