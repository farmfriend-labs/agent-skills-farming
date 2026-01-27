#!/usr/bin/env python3
"""
Data Synthesis Dashboard - Main Application
"""

import sqlite3
import os
import json
import argparse
from datetime import datetime
from pathlib import Path

try:
    import dash
    from dash import dcc, html
    import plotly.graph_objs as go
    import pandas as pd
    DASH_AVAILABLE = True
except ImportError:
    DASH_AVAILABLE = False

class DataSynthesisDashboard:
    """Main dashboard class for data synthesis and visualization."""

    def __init__(self, config):
        self.config = config
        self.db_path = config.get('database_path', '/var/data-synthesis-dashboard/dashboard.db')
        self.conn = None

    def initialize_database(self):
        """Initialize the dashboard database."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()

        # Equipment table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS equipment (
                id INTEGER PRIMARY KEY,
                name TEXT,
                type TEXT,
                manufacturer TEXT,
                status TEXT,
                location_lat REAL,
                location_lon REAL,
                fuel_level REAL,
                engine_hours REAL,
                last_update TIMESTAMP
            )
        ''')

        # Weather table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weather (
                id INTEGER PRIMARY KEY,
                location TEXT,
                temperature REAL,
                humidity REAL,
                wind_speed REAL,
                precipitation REAL,
                forecast TEXT,
                last_update TIMESTAMP
            )
        ''')

        # Operations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS operations (
                id INTEGER PRIMARY KEY,
                field_name TEXT,
                operation_type TEXT,
                acres_completed REAL,
                acres_total REAL,
                equipment_id INTEGER,
                start_time TIMESTAMP,
                end_time TIMESTAMP,
                status TEXT
            )
        ''')

        # Alerts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY,
                severity TEXT,
                message TEXT,
                equipment_id INTEGER,
                created_at TIMESTAMP,
                acknowledged BOOLEAN DEFAULT FALSE
            )
        ''')

        self.conn.commit()
        print("Database initialized")

    def run_dashboard(self, port=5000):
        """Run the dashboard web interface."""
        if not DASH_AVAILABLE:
            print("Dash not available, running in CLI mode")
            self.cli_mode()
            return

        app = dash.Dash(__name__)

        app.layout = html.Div([
            html.H1('Data Synthesis Dashboard'),
            dcc.Graph(id='equipment-status'),
            dcc.Interval(
                id='interval-component',
                interval=30*1000,  # Update every 30 seconds
                n_intervals=0
            )
        ])

        print(f"Dashboard running at http://localhost:{port}")
        app.run_server(debug=False, host='0.0.0.0', port=port)

    def cli_mode(self):
        """Run in command-line mode."""
        print("\nData Synthesis Dashboard - CLI Mode")
        print("Commands: status, weather, operations, alerts, quit\n")

        while True:
            try:
                cmd = input("dashboard> ").strip().lower()
                if cmd == 'quit':
                    break
                elif cmd == 'status':
                    self.show_equipment_status()
                elif cmd == 'weather':
                    self.show_weather()
                elif cmd == 'operations':
                    self.show_operations()
                elif cmd == 'alerts':
                    self.show_alerts()
                elif cmd == 'help':
                    print("Available commands: status, weather, operations, alerts, quit")
                else:
                    print(f"Unknown command: {cmd}")
            except (EOFError, KeyboardInterrupt):
                break

    def show_equipment_status(self):
        """Display equipment status."""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM equipment')
        equipment = cursor.fetchall()

        print("\nEquipment Status:")
        print("-" * 60)
        for eq in equipment:
            print(f"  {eq[1]} ({eq[2]}): {eq[4]}")

    def show_weather(self):
        """Display weather information."""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM weather ORDER BY last_update DESC LIMIT 1')
        weather = cursor.fetchone()

        if weather:
            print(f"\nWeather for {weather[1]}:")
            print(f"  Temperature: {weather[2]}°F")
            print(f"  Humidity: {weather[3]}%")
            print(f"  Wind: {weather[4]} mph")
            print(f"  Precipitation: {weather[5]} inches")

    def show_operations(self):
        """Display operational status."""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM operations WHERE status != "completed"')
        ops = cursor.fetchall()

        print("\nActive Operations:")
        print("-" * 60)
        for op in ops:
            progress = (op[3] / op[4] * 100) if op[4] > 0 else 0
            print(f"  {op[1]} - {op[2]}: {progress:.1f}% complete")

    def show_alerts(self):
        """Display active alerts."""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM alerts WHERE acknowledged = FALSE')
        alerts = cursor.fetchall()

        print("\nActive Alerts:")
        print("-" * 60)
        for alert in alerts:
            print(f"  [{alert[1].upper()}] {alert[2]}")

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()

def main():
    parser = argparse.ArgumentParser(description='Data Synthesis Dashboard')
    parser.add_argument('--port', type=int, default=5000, help='Dashboard port')
    parser.add_argument('--database', default='/var/data-synthesis-dashboard/dashboard.db', help='Database path')

    args = parser.parse_args()

    config = {
        'database_path': args.database
    }

    dashboard = DataSynthesisDashboard(config)
    dashboard.initialize_database()

    try:
        dashboard.run_dashboard(port=args.port)
    finally:
        dashboard.close()

if __name__ == '__main__':
    main()
