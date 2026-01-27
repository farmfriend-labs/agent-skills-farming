#!/usr/bin/env python3
"""
can_bus.py - CAN Bus Traffic Simulator
Generates realistic CAN bus traffic for agricultural equipment.
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

try:
    import can
except ImportError:
    print("Error: python-can library not installed")
    print("Install with: pip install python-can")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('CANBusSimulator')


@dataclass
class CANMessage:
    """Represents a CAN message."""
    arbitration_id: int
    data: bytes
    timestamp: float
    channel: str = "can0"

    def to_hex_string(self) -> str:
        """Convert to hex string for logging."""
        return f"0x{self.arbitration_id:08X} [{len(self.data)}] {' '.join(f'{b:02X}' for b in self.data)}"


class CANBusSimulator:
    """Simulates CAN bus traffic for agricultural equipment."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.interface = config.get('interface', 'vcan0')
        self.baudrate = config.get('baudrate', 250000)
        self.manufacturers = config.get('manufacturers', ['Universal'])
        self.message_rate = config.get('message_rate', 10)
        self.include_standard = config.get('include_standard', True)
        self.include_proprietary = config.get('include_proprietary', True)

        # Load PGN profiles
        self.standard_pgns = []
        self.proprietary_pgns = []
        self.load_pgn_profiles()

        # Initialize CAN bus
        self.bus = None
        self.setup_can_bus()

    def load_pgn_profiles(self):
        """Load PGN profiles from configuration."""
        pgn_profiles = self.config.get('pgn_profiles', {})

        if 'standard' in pgn_profiles:
            self.standard_pgns = pgn_profiles['standard']

        if 'proprietary' in pgn_profiles:
            self.proprietary_pgns = pgn_profiles['proprietary']

        logger.info(f"Loaded {len(self.standard_pgns)} standard PGNs")
        logger.info(f"Loaded {len(self.proprietary_pgns)} proprietary PGNs")

    def setup_can_bus(self):
        """Setup CAN bus interface."""
        try:
            # Try to create virtual CAN interface if it doesn't exist
            self.bus = can.Bus(
                interface='socketcan',
                channel=self.interface,
                bitrate=self.baudrate,
                receive_own_messages=False
            )
            logger.info(f"CAN bus connected: {self.interface} @ {self.baudrate} bps")
        except Exception as e:
            logger.warning(f"Failed to connect to CAN bus: {e}")
            logger.info("Running in simulation mode (no actual CAN output)")
            self.bus = None

    def generate_can_id(self, manufacturer: str, pgn: int, source_address: int) -> int:
        """Generate 29-bit CAN ID from components."""
        # Priority: 0-7 (lower is higher priority)
        priority = random.randint(1, 5)

        # Build CAN ID: Priority (3 bits) | PGN (18 bits) | Source Address (8 bits)
        can_id = (priority << 26) | (pgn << 8) | source_address
        return can_id

    def generate_source_address(self, manufacturer: str) -> int:
        """Generate source address for manufacturer."""
        ranges = self.config.get('source_address_ranges', {})

        if manufacturer in ranges:
            start, end = ranges[manufacturer]
            return random.randint(start, end)
        else:
            return random.randint(0, 0xFE)

    def generate_data(self, data_length: int) -> bytes:
        """Generate random CAN data."""
        return bytes([random.randint(0, 255) for _ in range(data_length)])

    def generate_standard_message(self) -> CANMessage:
        """Generate ISO 11783 standard message."""
        if not self.standard_pgns:
            return None

        manufacturer = "Universal"
        pgn_info = random.choice(self.standard_pgns)
        pgn = pgn_info['pgn']
        data_length = pgn_info.get('data_length', 8)
        source_address = random.randint(0, 0xFE)

        can_id = self.generate_can_id(manufacturer, pgn, source_address)
        data = self.generate_data(data_length)

        return CANMessage(
            arbitration_id=can_id,
            data=data,
            timestamp=time.time(),
            channel=self.interface
        )

    def generate_proprietary_message(self) -> CANMessage:
        """Generate manufacturer-specific message."""
        if not self.proprietary_pgns or not self.manufacturers:
            return None

        # Select random manufacturer (excluding Universal)
        available_manufacturers = [m for m in self.manufacturers if m != "Universal"]
        if not available_manufacturers:
            return None

        manufacturer = random.choice(available_manufacturers)
        pgn_info = random.choice(self.proprietary_pgns)
        pgn = pgn_info['pgn']
        data_length = pgn_info.get('data_length', 8)
        source_address = self.generate_source_address(manufacturer)

        can_id = self.generate_can_id(manufacturer, pgn, source_address)
        data = self.generate_data(data_length)

        return CANMessage(
            arbitration_id=can_id,
            data=data,
            timestamp=time.time(),
            channel=self.interface
        )

    def send_message(self, msg: CANMessage):
        """Send message to CAN bus."""
        if self.bus:
            try:
                can_msg = can.Message(
                    arbitration_id=msg.arbitration_id,
                    data=msg.data,
                    is_extended_id=msg.arbitration_id > 0x7FF,
                    timestamp=msg.timestamp
                )
                self.bus.send(can_msg)
            except Exception as e:
                logger.error(f"Failed to send CAN message: {e}")

        # Log message
        hex_str = msg.to_hex_string()
        timestamp = datetime.fromtimestamp(msg.timestamp).isoformat()

        # Extract components for logging
        manufacturer = self.identify_manufacturer_from_id(msg.arbitration_id)

        print(f"{timestamp} {self.interface} {hex_str}")

    def identify_manufacturer_from_id(self, can_id: int) -> str:
        """Identify manufacturer from CAN ID."""
        source_address = can_id & 0xFF
        ranges = self.config.get('source_address_ranges', {})

        for manufacturer, (start, end) in ranges.items():
            if start <= source_address <= end:
                return manufacturer

        return "Unknown"

    def run(self, duration_seconds: int = None):
        """Run CAN bus simulator."""
        logger.info("Starting CAN bus simulator...")
        logger.info(f"Message rate: {self.message_rate} messages/second")

        start_time = time.time()
        message_count = 0

        try:
            while duration_seconds is None or time.time() - start_time < duration_seconds:
                # Generate message
                msg = None

                # Mix of standard and proprietary messages
                if self.include_standard and self.include_proprietary:
                    if random.random() < 0.7:
                        msg = self.generate_standard_message()
                    else:
                        msg = self.generate_proprietary_message()
                elif self.include_standard:
                    msg = self.generate_standard_message()
                elif self.include_proprietary:
                    msg = self.generate_proprietary_message()

                if msg:
                    self.send_message(msg)
                    message_count += 1

                # Sleep to maintain message rate
                time.sleep(1.0 / self.message_rate)

        except KeyboardInterrupt:
            logger.info("Interrupted by user")
        finally:
            logger.info(f"Sent {message_count} messages")
            if self.bus:
                self.bus.shutdown()

    def get_stats(self) -> Dict:
        """Get simulator statistics."""
        return {
            "interface": self.interface,
            "baudrate": self.baudrate,
            "message_rate": self.message_rate,
            "manufacturers": self.manufacturers,
            "standard_pgns": len(self.standard_pgns),
            "proprietary_pgns": len(self.proprietary_pgns),
        }


def main():
    parser = argparse.ArgumentParser(description="CAN Bus Traffic Simulator")

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
    simulator = CANBusSimulator(config)

    # Print stats and exit
    if args.stats:
        stats = simulator.get_stats()
        print(json.dumps(stats, indent=2))
        return

    # Run simulator
    simulator.run(duration_seconds=args.duration)


if __name__ == "__main__":
    main()
