#!/usr/bin/env python3
"""
equipment_telemetry.py - Equipment Telemetry Simulator
Generates realistic equipment operation data.
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
logger = logging.getLogger('EquipmentTelemetrySimulator')


@dataclass
class EquipmentReading:
    """Represents equipment telemetry reading."""
    equipment_id: str
    equipment_type: str
    equipment_name: str
    sensor: str
    value: float
    unit: str
    status: str
    timestamp: str


class EquipmentTelemetrySimulator:
    """Simulates equipment telemetry for agricultural operations."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.output_file = None
        self.tractors = config.get('tractors', [])
        self.planters = config.get('planters', [])
        self.sprayers = config.get('sprayers', [])
        self.combines = config.get('combines', [])

        self.telemetry_interval = 5  # Default 5 seconds

        # Setup output
        self.setup_output()

    def setup_output(self):
        """Setup output file."""
        output_dir = Path(__file__).parent.parent / "outputs"
        output_dir.mkdir(exist_ok=True)

        self.output_file = output_dir / "telemetry.json"
        logger.info(f"Output file: {self.output_file}")

    def generate_sensor_value(self, sensor_def: Dict) -> tuple:
        """Generate sensor value with status."""
        sensor_type = sensor_def.get('type', 'generic')

        if 'range' in sensor_def:
            min_val, max_val = sensor_def['range']
            value = random.uniform(min_val, max_val)
            status = 'normal'
        elif 'values' in sensor_def:
            value = random.choice(sensor_def['values'])
            status = value
        else:
            value = random.uniform(0, 100)
            status = 'unknown'

        unit = sensor_def.get('unit', '')

        return round(value, 2), unit, status

    def generate_equipment_telemetry(self, equip: Dict) -> List[EquipmentReading]:
        """Generate telemetry for a piece of equipment."""
        readings = []

        for sensor_name, sensor_def in equip.get('sensors', {}).items():
            value, unit, status = self.generate_sensor_value(sensor_def)

            reading = EquipmentReading(
                equipment_id=equip['id'],
                equipment_type=equip.get('type', 'unknown'),
                equipment_name=equip.get('name', 'Unknown'),
                sensor=sensor_name,
                value=value,
                unit=unit,
                status=status,
                timestamp=datetime.utcnow().isoformat()
            )

            readings.append(reading)

        return readings

    def generate_all_telemetry(self) -> Dict[str, Any]:
        """Generate telemetry for all equipment."""
        all_telemetry = {
            'timestamp': datetime.utcnow().isoformat(),
            'equipment': []
        }

        # Generate tractor telemetry
        for tractor in self.tractors:
            tractor_data = {
                'equipment_id': tractor['id'],
                'equipment_name': tractor['name'],
                'manufacturer': tractor.get('manufacturer', 'Unknown'),
                'model': tractor.get('model', 'Unknown'),
                'year': tractor.get('year', 0),
                'sensors': []
            }

            readings = self.generate_equipment_telemetry(tractor)
            for reading in readings:
                tractor_data['sensors'].append(asdict(reading))

            all_telemetry['equipment'].append(tractor_data)

        # Generate planter telemetry
        for planter in self.planters:
            planter_data = {
                'equipment_id': planter['id'],
                'equipment_name': planter['name'],
                'manufacturer': planter.get('manufacturer', 'Unknown'),
                'model': planter.get('model', 'Unknown'),
                'year': planter.get('year', 0),
                'sensors': []
            }

            readings = self.generate_equipment_telemetry(planter)
            for reading in readings:
                planter_data['sensors'].append(asdict(reading))

            all_telemetry['equipment'].append(planter_data)

        # Generate sprayer telemetry
        for sprayer in self.sprayers:
            sprayer_data = {
                'equipment_id': sprayer['id'],
                'equipment_name': sprayer['name'],
                'manufacturer': sprayer.get('manufacturer', 'Unknown'),
                'model': sprayer.get('model', 'Unknown'),
                'year': sprayer.get('year', 0),
                'sensors': []
            }

            readings = self.generate_equipment_telemetry(sprayer)
            for reading in readings:
                sprayer_data['sensors'].append(asdict(reading))

            all_telemetry['equipment'].append(sprayer_data)

        # Generate combine telemetry
        for combine in self.combines:
            combine_data = {
                'equipment_id': combine['id'],
                'equipment_name': combine['name'],
                'manufacturer': combine.get('manufacturer', 'Unknown'),
                'model': combine.get('model', 'Unknown'),
                'year': combine.get('year', 0),
                'sensors': []
            }

            readings = self.generate_equipment_telemetry(combine)
            for reading in readings:
                combine_data['sensors'].append(asdict(reading))

            all_telemetry['equipment'].append(combine_data)

        return all_telemetry

    def write_output(self, data: Dict):
        """Write telemetry to output file."""
        with open(self.output_file, 'w') as f:
            json.dump(data, f, indent=2)

    def run(self, duration_seconds: int = None):
        """Run equipment telemetry simulator."""
        logger.info("Starting equipment telemetry simulator...")
        logger.info(f"Tractors: {len(self.tractors)}")
        logger.info(f"Planters: {len(self.planters)}")
        logger.info(f"Sprayers: {len(self.sprayers)}")
        logger.info(f"Combines: {len(self.combines)}")
        logger.info(f"Update interval: {self.telemetry_interval}s")

        start_time = time.time()
        update_count = 0

        try:
            while duration_seconds is None or time.time() - start_time < duration_seconds:
                # Generate telemetry
                data = self.generate_all_telemetry()

                # Write output
                self.write_output(data)
                update_count += 1

                logger.debug(f"Update {update_count}: {len(data['equipment'])} equipment")

                # Sleep for update interval
                time.sleep(self.telemetry_interval)

        except KeyboardInterrupt:
            logger.info("Interrupted by user")
        finally:
            logger.info(f"Sent {update_count} updates")
            logger.info(f"Output written to: {self.output_file}")

    def get_stats(self) -> Dict:
        """Get simulator statistics."""
        return {
            "tractors": len(self.tractors),
            "planters": len(self.planters),
            "sprayers": len(self.sprayers),
            "combines": len(self.combines),
            "total_equipment": len(self.tractors) + len(self.planters) + len(self.sprayers) + len(self.combines),
            "telemetry_interval": self.telemetry_interval,
        }


def main():
    parser = argparse.ArgumentParser(description="Equipment Telemetry Simulator")

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
    simulator = EquipmentTelemetrySimulator(config)

    # Print stats and exit
    if args.stats:
        stats = simulator.get_stats()
        print(json.dumps(stats, indent=2))
        return

    # Run simulator
    simulator.run(duration_seconds=args.duration)


if __name__ == "__main__":
    main()
