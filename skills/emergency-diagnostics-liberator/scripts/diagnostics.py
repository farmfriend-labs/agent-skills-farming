#!/usr/bin/env python3
"""
Emergency Diagnostics Liberator - Main Diagnostics Script

Provides interactive diagnostic capabilities for agricultural equipment.
Reads codes, interprets them, and provides repair guidance.
"""

import argparse
import sqlite3
import sys
import time
from datetime import datetime
from pathlib import Path
import os

try:
    import obd
    OBD_AVAILABLE = True
except ImportError:
    OBD_AVAILABLE = False

try:
    import can
    CAN_AVAILABLE = True
except ImportError:
    CAN_AVAILABLE = False

class EmergencyDiagnostics:
    """Main diagnostics class for emergency equipment diagnostics."""

    def __init__(self, config):
        """Initialize diagnostics with configuration."""
        self.config = config
        self.connection = None
        self.db_conn = None
        self.session_id = None

    def connect(self):
        """Connect to equipment diagnostic interface."""
        interface_type = self.config['interface_type']

        if interface_type == 'obd2':
            return self._connect_obd2()
        elif interface_type == 'can':
            return self._connect_can()
        else:
            print(f"Error: Unknown interface type: {interface_type}")
            return False

    def _connect_obd2(self):
        """Connect via OBD-II adapter."""
        if not OBD_AVAILABLE:
            print("Error: python-obd library not available")
            print("Install with: pip3 install python-obd")
            return False

        port = self.config['port']
        print(f"Connecting to OBD-II adapter on {port}...")

        try:
            self.connection = obd.OBD(portstr=port, baudrate=115200)
            if self.connection.is_connected():
                print(f"Connected to {self.connection.port_name()}")
                print(f"Protocol: {self.connection.protocol_name()}")
                return True
            else:
                print("Failed to connect to OBD-II adapter")
                return False
        except Exception as e:
            print(f"Error connecting: {e}")
            return False

    def _connect_can(self):
        """Connect via CAN interface."""
        if not CAN_AVAILABLE:
            print("Error: python-can library not available")
            print("Install with: pip3 install python-can")
            return False

        interface = self.config['can_interface']
        print(f"Connecting to CAN interface {interface}...")

        try:
            self.connection = can.interface.Bus(channel=interface,
                                                  bustype='socketcan')
            print(f"Connected to {interface}")
            return True
        except Exception as e:
            print(f"Error connecting: {e}")
            return False

    def open_database(self):
        """Open code database."""
        db_path = self.config['code_db']

        if not os.path.exists(db_path):
            print(f"Error: Database not found at {db_path}")
            return False

        try:
            self.db_conn = sqlite3.connect(db_path)
            return True
        except Exception as e:
            print(f"Error opening database: {e}")
            return False

    def read_codes(self):
        """Read diagnostic trouble codes from equipment."""
        interface_type = self.config['interface_type']

        if interface_type == 'obd2':
            return self._read_codes_obd2()
        elif interface_type == 'can':
            return self._read_codes_can()
        else:
            print(f"Unknown interface type: {interface_type}")
            return []

    def _read_codes_obd2(self):
        """Read codes via OBD-II."""
        if not self.connection or not self.connection.is_connected():
            print("Not connected to equipment")
            return []

        print("Reading codes from OBD-II...")

        codes = []
        dtc = self.connection.query(obd.commands.GET_DTC)

        if dtc is not None:
            raw_codes = dtc.value
            print(f"Found {len(raw_codes)} code(s)")

            for code in raw_codes:
                codes.append(str(code))

        return codes

    def _read_codes_can(self):
        """Read codes via CAN bus (J1939)."""
        print("Reading codes via CAN bus...")
        # Simplified - real implementation would parse J1939 DM1 messages
        # This is a placeholder for CAN-based code reading
        print("Note: Full J1939 code reading requires additional implementation")
        return []

    def interpret_code(self, code):
        """Interpret a diagnostic code using database."""
        if not self.db_conn:
            return None

        # Parse code (simplified - real implementation would handle OBD-II and J1939 formats)
        # For now, assume J1939 format: SPN_FMI
        if '_' in code:
            parts = code.split('_')
            spn = int(parts[0])
            fmi = int(parts[1])
        else:
            # Try OBD-II format (P-code)
            print(f"OBD-II code interpretation not fully implemented: {code}")
            return None

        # Query database
        cursor = self.db_conn.cursor()
        cursor.execute('''
            SELECT c.description, c.severity, c.common_causes, c.suggested_tests, c.repair_complexity,
                   m.name as manufacturer
            FROM codes c
            LEFT JOIN manufacturers m ON c.manufacturer_id = m.id
            WHERE c.spn = ? AND c.fmi = ?
            ORDER BY c.manufacturer_id DESC
            LIMIT 1
        ''', (spn, fmi))

        result = cursor.fetchone()

        if result:
            return {
                'spn': spn,
                'fmi': fmi,
                'description': result[0],
                'severity': result[1],
                'causes': result[2],
                'tests': result[3],
                'complexity': result[4],
                'manufacturer': result[5]
            }
        else:
            return {
                'spn': spn,
                'fmi': fmi,
                'description': 'Code not found in database',
                'severity': 'Unknown',
                'causes': 'Unknown',
                'tests': 'Consult manufacturer documentation',
                'complexity': 'Unknown',
                'manufacturer': 'Unknown'
            }

    def display_code(self, interpretation):
        """Display code interpretation in human-readable format."""
        if not interpretation:
            return

        print("")
        print("=" * 60)
        print(f"SPN {interpretation['spn']} FMI {interpretation['fmi']}")
        print("=" * 60)

        # Color severity
        severity = interpretation['severity'].upper()
        if severity == 'CRITICAL':
            print(f"Severity: {severity} [STOP OPERATION IMMEDIATELY]")
        elif severity == 'WARNING':
            print(f"Severity: {severity} [ADDRESS SOON]")
        elif severity == 'ADVISORY':
            print(f"Severity: {severity} [MONITOR]")
        else:
            print(f"Severity: {severity}")

        print("")
        print(f"Description: {interpretation['description']}")
        print("")

        if interpretation['manufacturer'] != 'Unknown':
            print(f"Manufacturer: {interpretation['manufacturer']}")

        print("")
        print("Common Causes:")
        if interpretation['causes']:
            for cause in interpretation['causes'].split(','):
                print(f"  - {cause.strip()}")
        else:
            print("  Unknown")

        print("")
        print("Suggested Tests:")
        if interpretation['tests']:
            for test in interpretation['tests'].split(','):
                print(f"  - {test.strip()}")
        else:
            print("  Consult service manual")

        print("")
        print(f"Repair Complexity: {interpretation['complexity']}")
        print("=" * 60)
        print("")

    def start_session(self, equipment_info):
        """Start a new diagnostic session."""
        if not self.db_conn:
            return

        cursor = self.db_conn.cursor()
        cursor.execute('''
            INSERT INTO diagnostic_sessions (equipment_type, equipment_make, equipment_model, vin, interface_type, protocol)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            equipment_info.get('type', 'Unknown'),
            equipment_info.get('make', 'Unknown'),
            equipment_info.get('model', 'Unknown'),
            equipment_info.get('vin', 'Unknown'),
            self.config['interface_type'],
            self.config['protocol']
        ))

        self.db_conn.commit()
        self.session_id = cursor.lastrowid
        print(f"Session started: ID {self.session_id}")

    def log_codes(self, codes):
        """Log codes from current session."""
        if not self.db_conn or not self.session_id:
            return

        cursor = self.db_conn.cursor()
        for code in codes:
            interpretation = self.interpret_code(code)
            if interpretation:
                cursor.execute('''
                    INSERT INTO session_codes (session_id, spn, fmi, description, severity, status)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    self.session_id,
                    interpretation['spn'],
                    interpretation['fmi'],
                    interpretation['description'],
                    interpretation['severity'],
                    'Active'
                ))

        self.db_conn.commit()
        print(f"Logged {len(codes)} codes to session")

    def generate_report(self):
        """Generate diagnostic report for current session."""
        if not self.db_conn or not self.session_id:
            print("No active session")
            return

        cursor = self.db_conn.cursor()
        cursor.execute('''
            SELECT spn, fmi, description, severity, status
            FROM session_codes
            WHERE session_id = ?
        ''', (self.session_id,))

        codes = cursor.fetchall()

        print("")
        print("=" * 60)
        print("DIAGNOSTIC REPORT")
        print("=" * 60)
        print(f"Session ID: {self.session_id}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("")
        print("Codes Found:")
        for code in codes:
            print(f"  SPN {code[0]} FMI {code[1]}: {code[2]} [{code[3]}]")
        print("")
        print("=" * 60)
        print("")

    def close(self):
        """Close connections."""
        if self.connection:
            if self.config['interface_type'] == 'obd2':
                self.connection.close()
            elif self.config['interface_type'] == 'can':
                self.connection.shutdown()

        if self.db_conn:
            self.db_conn.close()

def interactive_mode(diagnostics):
    """Interactive command-line mode."""
    print("")
    print("Emergency Diagnostics Liberator - Interactive Mode")
    print("Type 'help' for commands, 'quit' to exit")
    print("")

    while True:
        try:
            cmd = input("diag> ").strip().lower()

            if cmd == 'quit' or cmd == 'exit':
                print("Exiting...")
                break

            elif cmd == 'help':
                print("Available commands:")
                print("  read    - Read diagnostic codes")
                print("  clear   - Clear codes (with confirmation)")
                print("  info    - Show connection info")
                print("  report  - Generate diagnostic report")
                print("  quit    - Exit")

            elif cmd == 'read':
                codes = diagnostics.read_codes()
                if codes:
                    for code in codes:
                        interpretation = diagnostics.interpret_code(code)
                        diagnostics.display_code(interpretation)
                    diagnostics.log_codes(codes)
                else:
                    print("No codes found")

            elif cmd == 'clear':
                if diagnostics.config['warn_before_clear']:
                    confirm = input("Are you sure you want to clear codes? (yes/no): ")
                    if confirm.lower() == 'yes':
                        print("Clear codes not yet implemented")
                        print("Note: Only clear after repairs are complete")
                else:
                    print("Clear codes not yet implemented")

            elif cmd == 'info':
                if diagnostics.config['interface_type'] == 'obd2':
                    if diagnostics.connection and diagnostics.connection.is_connected():
                        print(f"Connected to: {diagnostics.connection.port_name()}")
                        print(f"Protocol: {diagnostics.connection.protocol_name()}")
                        print(f"ELM Version: {diagnostics.connection.elm_version()}")
                    else:
                        print("Not connected")
                else:
                    print(f"CAN interface: {diagnostics.config['can_interface']}")

            elif cmd == 'report':
                diagnostics.generate_report()

            elif cmd == '':
                continue

            else:
                print(f"Unknown command: {cmd}")
                print("Type 'help' for available commands")

        except KeyboardInterrupt:
            print("\nUse 'quit' to exit")
        except EOFError:
            break

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Emergency Diagnostics Liberator - Equipment Diagnostics'
    )

    parser.add_argument('--interface-type', default='obd2',
                       choices=['obd2', 'can'],
                       help='Diagnostic interface type')
    parser.add_argument('--port', default='/dev/ttyUSB0',
                       help='OBD-II serial port')
    parser.add_argument('--can-interface', default='can0',
                       help='CAN interface name')
    parser.add_argument('--baudrate', type=int, default=250000,
                       help='CAN baud rate')
    parser.add_argument('--protocol', default='auto',
                       help='Diagnostic protocol')
    parser.add_argument('--manufacturer', default='auto',
                       help='Manufacturer (johndeere, caseih, agco, etc.)')
    parser.add_argument('--code-db', default='/opt/emergency-diagnostics/codes.db',
                       help='Path to code database')
    parser.add_argument('--offline-mode', default='true',
                       help='Offline mode')
    parser.add_argument('--log-level', default='info',
                       help='Log level')
    parser.add_argument('--log-file', default='/var/log/emergency-diagnostics.log',
                       help='Log file path')
    parser.add_argument('--report-dir', default='/var/log/emergency-diagnostics/reports',
                       help='Report directory')
    parser.add_argument('--safety-override-disabled', default='true',
                       help='Disable safety overrides')
    parser.add_argument('--require-confirmation', default='true',
                       help='Require confirmation for actions')
    parser.add_argument('--warn-before-clear', default='true',
                       help='Warn before clearing codes')

    args = parser.parse_args()

    config = {
        'interface_type': args.interface_type,
        'port': args.port,
        'can_interface': args.can_interface,
        'baudrate': args.baudrate,
        'protocol': args.protocol,
        'manufacturer': args.manufacturer,
        'code_db': args.code_db,
        'offline_mode': args.offline_mode,
        'log_level': args.log_level,
        'log_file': args.log_file,
        'report_dir': args.report_dir,
        'safety_override_disabled': args.safety_override_disabled,
        'require_confirmation': args.require_confirmation,
        'warn_before_clear': args.warn_before_clear,
    }

    # Initialize diagnostics
    diagnostics = EmergencyDiagnostics(config)

    # Open code database
    if not diagnostics.open_database():
        sys.exit(1)

    # Connect to equipment
    if not diagnostics.connect():
        sys.exit(1)

    # Start session
    diagnostics.start_session({
        'type': 'Unknown',
        'make': config['manufacturer'],
        'model': 'Unknown',
        'vin': 'Unknown'
    })

    # Enter interactive mode
    try:
        interactive_mode(diagnostics)
    finally:
        diagnostics.close()

if __name__ == '__main__':
    main()
