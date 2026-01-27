#!/usr/bin/env python3
"""
GPS Status Checker for Plug-and-Play Precision Agriculture
Checks GPS receiver status, accuracy, and fix type
"""

import sys
import argparse
import serial
import time
from datetime import datetime


class GPSStatusChecker:
    """Check and report GPS receiver status"""

    def __init__(self, port='/dev/ttyUSB0', baudrate=9600, timeout=10):
        """Initialize GPS checker

        Args:
            port: Serial port for GPS receiver
            baudrate: Serial communication baud rate
            timeout: Timeout in seconds
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_conn = None

        # GPS data
        self.satellites = []
        self.fix_type = None
        self.latitude = None
        self.longitude = None
        self.altitude = None
        self.hdop = None  # Horizontal dilution of precision
        self.vdop = None  # Vertical dilution of precision
        self.pdop = None  # Position dilution of precision

    def connect(self):
        """Connect to GPS receiver via serial port

        Returns:
            bool: True if connection successful
        """
        try:
            self.serial_conn = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=1
            )
            print(f"✓ Connected to GPS on {self.port}")
            print(f"  Baudrate: {self.baudrate}")
            return True
        except serial.SerialException as e:
            print(f"✗ Failed to connect to GPS: {e}")
            return False

    def disconnect(self):
        """Disconnect from GPS receiver"""
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
            print("✓ Disconnected from GPS")

    def parse_nmea_sentence(self, sentence):
        """Parse NMEA sentence

        Args:
            sentence: NMEA sentence string

        Returns:
            tuple: (sentence_type, data) or (None, None)
        """
        if not sentence.startswith('$'):
            return None, None

        parts = sentence.split('*')[0].split(',')
        sentence_type = parts[0][1:5]  # Get GPRMC, GPGGA, etc.

        return sentence_type, parts

    def process_gpgga(self, parts):
        """Process GPGGA sentence (Global Positioning System Fix Data)

        Args:
            parts: NMEA sentence parts
        """
        if len(parts) < 15:
            return

        # Parse fix type (field 6)
        # 0 = Invalid, 1 = GPS fix, 2 = DGPS fix
        try:
            self.fix_type = int(parts[6])
        except (ValueError, IndexError):
            self.fix_type = 0

        # Parse satellites (field 7)
        try:
            num_sats = int(parts[7])
        except (ValueError, IndexError):
            num_sats = 0

        # Parse HDOP (field 8)
        try:
            self.hdop = float(parts[8])
        except (ValueError, IndexError):
            self.hdop = None

        # Parse altitude (field 9)
        try:
            self.altitude = float(parts[9])
        except (ValueError, IndexError):
            self.altitude = None

        # Parse latitude (field 2) and longitude (field 4)
        try:
            lat_deg = float(parts[2][:2])
            lat_min = float(parts[2][2:]) / 60.0
            lat_dir = parts[3]
            self.latitude = lat_deg + lat_min
            if lat_dir == 'S':
                self.latitude = -self.latitude

            lon_deg = float(parts[4][:3])
            lon_min = float(parts[4][3:]) / 60.0
            lon_dir = parts[5]
            self.longitude = lon_deg + lon_min
            if lon_dir == 'W':
                self.longitude = -self.longitude
        except (ValueError, IndexError):
            pass

        return num_sats

    def process_gprmc(self, parts):
        """Process GPRMC sentence (Recommended Minimum sentence)

        Args:
            parts: NMEA sentence parts
        """
        # RMC provides date and time, and fix status
        if len(parts) < 12:
            return

        # Fix status (field 2): A = valid, V = invalid
        fix_status = parts[2]
        if fix_status == 'A':
            return True
        return False

    def read_nmea_sentences(self, duration=10):
        """Read and process NMEA sentences

        Args:
            duration: Duration to read in seconds
        """
        print(f"\nReading GPS data for {duration} seconds...")
        print(f"{'Time':<20} {'Type':<10} {'Sats':<6} {'Fix':<6} {'HDOP':<8} {'Lat':<12} {'Lon':<13}")

        start_time = time.time()
        num_sats = 0
        sentences_read = 0

        while (time.time() - start_time) < duration:
            if not self.serial_conn or not self.serial_conn.is_open:
                break

            try:
                line = self.serial_conn.readline().decode('ascii', errors='ignore').strip()
                if not line:
                    continue

                sentence_type, parts = self.parse_nmea_sentence(line)
                if not sentence_type:
                    continue

                sentences_read += 1

                if sentence_type == 'GPGGA':
                    sats = self.process_gpgga(parts)
                    if sats is not None:
                        num_sats = sats

                    # Print status line
                    timestamp = datetime.now().strftime('%H:%M:%S')
                    fix_text = self.get_fix_type_text()
                    hdop_text = f"{self.hdop:.1f}" if self.hdop else "N/A"
                    lat_text = f"{self.latitude:.6f}" if self.latitude else "N/A"
                    lon_text = f"{self.longitude:.6f}" if self.longitude else "N/A"

                    print(f"{timestamp:<20} {sentence_type:<10} {num_sats:<6} {fix_text:<6} {hdop_text:<8} {lat_text:<12} {lon_text:<13}")

                elif sentence_type == 'GPRMC':
                    self.process_gprmc(parts)

            except Exception as e:
                print(f"Error parsing NMEA sentence: {e}")
                continue

        return sentences_read

    def get_fix_type_text(self):
        """Get human-readable fix type

        Returns:
            str: Fix type description
        """
        fix_types = {
            0: "No Fix",
            1: "GPS",
            2: "DGPS",
            3: "PPS",
            4: "RTK",
            5: "Float RTK",
            6: "Estimated"
        }
        return fix_types.get(self.fix_type, "Unknown")

    def estimate_accuracy(self):
        """Estimate position accuracy based on HDOP

        Returns:
            tuple: (accuracy_estimate, accuracy_description)
        """
        if not self.hdop:
            return None, "Unknown"

        # Accuracy estimate based on HDOP (rough approximation)
        accuracy_m = self.hdop * 2.0  # Rough conversion

        if accuracy_m < 1.0:
            description = "Excellent (sub-meter)"
        elif accuracy_m < 3.0:
            description = "Good (1-3 meters)"
        elif accuracy_m < 5.0:
            description = "Fair (3-5 meters)"
        elif accuracy_m < 10.0:
            description = "Poor (5-10 meters)"
        else:
            description = "Very Poor (>10 meters)"

        return accuracy_m, description

    def print_summary(self, sentences_read):
        """Print summary of GPS status

        Args:
            sentences_read: Number of NMEA sentences read
        """
        print("\n" + "=" * 80)
        print("GPS STATUS SUMMARY")
        print("=" * 80)

        print(f"\nSentences read: {sentences_read}")

        if self.fix_type is not None:
            print(f"Fix Type: {self.get_fix_type_text()} ({self.fix_type})")
        else:
            print("Fix Type: Unknown")

        if self.latitude is not None and self.longitude is not None:
            print(f"Position: {self.latitude:.6f}, {self.longitude:.6f}")
        else:
            print("Position: Not acquired")

        if self.altitude is not None:
            print(f"Altitude: {self.altitude:.1f} meters")
        else:
            print("Altitude: Not available")

        if self.hdop is not None:
            accuracy, description = self.estimate_accuracy()
            print(f"HDOP: {self.hdop:.1f}")
            print(f"Estimated Accuracy: {accuracy:.1f}m ({description})")
        else:
            print("HDOP: Not available")

        print("\n" + "=" * 80)

    def run(self, duration=10):
        """Run GPS status check

        Args:
            duration: Duration to check GPS in seconds
        """
        if not self.connect():
            return False

        try:
            sentences_read = self.read_nmea_sentences(duration)
            self.print_summary(sentences_read)
            return True
        finally:
            self.disconnect()


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Check GPS receiver status for precision agriculture'
    )
    parser.add_argument(
        '--port',
        default='/dev/ttyUSB0',
        help='Serial port for GPS receiver (default: /dev/ttyUSB0)'
    )
    parser.add_argument(
        '--baudrate',
        type=int,
        default=9600,
        help='Serial baud rate (default: 9600)'
    )
    parser.add_argument(
        '--duration',
        type=int,
        default=10,
        help='Duration to check GPS in seconds (default: 10)'
    )

    args = parser.parse_args()

    checker = GPSStatusChecker(
        port=args.port,
        baudrate=args.baudrate,
        timeout=args.duration
    )

    success = checker.run(duration=args.duration)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
