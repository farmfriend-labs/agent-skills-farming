#!/usr/bin/env python3
"""
sensor_stream.py - Sensor Data Stream Simulator
Generates realistic sensor data for field monitoring.
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
logger = logging.getLogger('SensorStreamSimulator')


@dataclass
class SensorReading:
    """Represents a single sensor reading."""
    sensor_id: str
    sensor_type: str
    value: float
    unit: str
    timestamp: str
    field_id: str
    location: str


class SensorStreamSimulator:
    """Simulates sensor data streams for agricultural monitoring."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.output_file = None
        self.fields = config.get('fields', [])
        self.equipment = config.get('equipment', [])
        self.infrastructure = config.get('infrastructure', [])
        self.update_interval = config.get('update_interval_seconds', 30)
        self.data_format = config.get('data_format', 'json')
        self.include_timestamp = config.get('include_timestamp', True)

        # Setup output
        self.setup_output()

    def setup_output(self):
        """Setup output file."""
        output_dir = Path(__file__).parent.parent / "outputs"
        output_dir.mkdir(exist_ok=True)

        if self.data_format == 'json':
            self.output_file = output_dir / "sensor-data.json"
        else:
            self.output_file = output_dir / "sensor-data.log"

        logger.info(f"Output file: {self.output_file}")

    def generate_sensor_reading(self, sensor_def: Dict, field_id: str) -> SensorReading:
        """Generate a single sensor reading."""
        sensor_type = sensor_def['type']
        sensor_id = f"{sensor_type}_{random.randint(1000, 9999)}"

        # Generate value based on sensor type
        if sensor_type == 'soil_moisture':
            value = random.uniform(10, 40)
            unit = '%'
        elif sensor_type == 'temperature':
            value = random.uniform(45, 95)
            unit = 'F'
        elif sensor_type == 'ph':
            value = random.uniform(5.5, 7.5)
            unit = 'pH'
        elif sensor_type == 'humidity':
            value = random.uniform(30, 80)
            unit = '%'
        elif sensor_type == 'flow_rate':
            value = random.uniform(5, 45)
            unit = 'gpm'
        elif sensor_type == 'pressure':
            value = random.uniform(15, 75)
            unit = 'PSI'
        else:
            value = random.uniform(0, 100)
            unit = 'units'

        return SensorReading(
            sensor_id=sensor_id,
            sensor_type=sensor_type,
            value=round(value, 2),
            unit=unit,
            timestamp=datetime.utcnow().isoformat(),
            field_id=field_id,
            location=random.choice(['north', 'south', 'east', 'west', 'center'])
        )

    def generate_field_sensors(self, field: Dict) -> List[SensorReading]:
        """Generate sensor readings for a field."""
        readings = []

        # Generate soil moisture readings
        for i in range(field.get('soil_moisture_sensors', 0)):
            sensor_def = {'type': 'soil_moisture'}
            readings.append(self.generate_sensor_reading(sensor_def, field['id']))

        # Generate temperature readings
        for i in range(field.get('temperature_sensors', 0)):
            sensor_def = {'type': 'temperature'}
            readings.append(self.generate_sensor_reading(sensor_def, field['id']))

        # Generate pH readings
        for i in range(field.get('ph_sensors', 0)):
            sensor_def = {'type': 'ph'}
            readings.append(self.generate_sensor_reading(sensor_def, field['id']))

        return readings

    def generate_equipment_sensors(self, equip: Dict) -> List[SensorReading]:
        """Generate sensor readings for equipment."""
        readings = []

        for sensor_type in equip.get('sensors', []):
            sensor_def = {'type': sensor_type}
            # Use equipment ID instead of field ID
            reading = self.generate_sensor_reading(sensor_def, equip['id'])
            # Modify to include equipment info
            reading.field_id = f"equip-{equip['id']}"
            reading.location = f"{equip['type']}-{equip['name']}"

            readings.append(reading)

        return readings

    def generate_infrastructure_sensors(self, infra: Dict) -> List[SensorReading]:
        """Generate sensor readings for infrastructure."""
        readings = []

        for sensor_type in infra.get('sensors', []):
            sensor_def = {'type': sensor_type}
            reading = self.generate_sensor_reading(sensor_def, infra['id'])
            reading.field_id = f"infra-{infra['id']}"
            reading.location = f"{infra['type']}-{infra['name']}"

            readings.append(reading)

        return readings

    def generate_all_sensors(self) -> Dict[str, Any]:
        """Generate sensor readings for all sensors."""
        all_readings = {
            'timestamp': datetime.utcnow().isoformat(),
            'fields': [],
            'equipment': [],
            'infrastructure': []
        }

        # Generate field sensors
        for field in self.fields:
            field_data = {
                'field_id': field['id'],
                'field_name': field['name'],
                'sensors': []
            }

            readings = self.generate_field_sensors(field)
            for reading in readings:
                field_data['sensors'].append(asdict(reading))

            all_readings['fields'].append(field_data)

        # Generate equipment sensors
        for equip in self.equipment:
            equip_data = {
                'equipment_id': equip['id'],
                'equipment_name': equip['name'],
                'equipment_type': equip['type'],
                'sensors': []
            }

            readings = self.generate_equipment_sensors(equip)
            for reading in readings:
                equip_data['sensors'].append(asdict(reading))

            all_readings['equipment'].append(equip_data)

        # Generate infrastructure sensors
        for infra in self.infrastructure:
            infra_data = {
                'infrastructure_id': infra['id'],
                'infrastructure_name': infra['name'],
                'infrastructure_type': infra['type'],
                'sensors': []
            }

            readings = self.generate_infrastructure_sensors(infra)
            for reading in readings:
                infra_data['sensors'].append(asdict(reading))

            all_readings['infrastructure'].append(infra_data)

        return all_readings

    def write_output(self, data: Dict):
        """Write sensor data to output file."""
        if self.data_format == 'json':
            with open(self.output_file, 'w') as f:
                json.dump(data, f, indent=2)
        else:
            with open(self.output_file, 'a') as f:
                f.write(json.dumps(data) + '\n')

    def run(self, duration_seconds: int = None):
        """Run sensor stream simulator."""
        logger.info("Starting sensor stream simulator...")
        logger.info(f"Fields: {len(self.fields)}")
        logger.info(f"Equipment: {len(self.equipment)}")
        logger.info(f"Infrastructure: {len(self.infrastructure)}")
        logger.info(f"Update interval: {self.update_interval}s")

        start_time = time.time()
        update_count = 0

        try:
            while duration_seconds is None or time.time() - start_time < duration_seconds:
                # Generate sensor data
                data = self.generate_all_sensors()

                # Write output
                self.write_output(data)
                update_count += 1

                logger.debug(f"Update {update_count}: {len(data['fields'])} fields, "
                           f"{len(data['equipment'])} equipment, "
                           f"{len(data['infrastructure'])} infrastructure")

                # Sleep for update interval
                time.sleep(self.update_interval)

        except KeyboardInterrupt:
            logger.info("Interrupted by user")
        finally:
            logger.info(f"Sent {update_count} updates")
            logger.info(f"Output written to: {self.output_file}")

    def get_stats(self) -> Dict:
        """Get simulator statistics."""
        total_sensors = 0

        for field in self.fields:
            total_sensors += field.get('soil_moisture_sensors', 0)
            total_sensors += field.get('temperature_sensors', 0)
            total_sensors += field.get('ph_sensors', 0)

        for equip in self.equipment:
            total_sensors += len(equip.get('sensors', []))

        for infra in self.infrastructure:
            total_sensors += len(infra.get('sensors', []))

        return {
            "fields": len(self.fields),
            "equipment": len(self.equipment),
            "infrastructure": len(self.infrastructure),
            "total_sensors": total_sensors,
            "update_interval": self.update_interval,
            "data_format": self.data_format,
        }


def main():
    parser = argparse.ArgumentParser(description="Sensor Data Stream Simulator")

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
    simulator = SensorStreamSimulator(config)

    # Print stats and exit
    if args.stats:
        stats = simulator.get_stats()
        print(json.dumps(stats, indent=2))
        return

    # Run simulator
    simulator.run(duration_seconds=args.duration)


if __name__ == "__main__":
    main()
