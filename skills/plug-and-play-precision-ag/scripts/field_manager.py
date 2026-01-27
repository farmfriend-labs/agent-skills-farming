#!/usr/bin/env python3
"""
Field Manager for Plug-and-Play Precision Agriculture
Create, list, and manage field boundaries
"""

import sys
import argparse
import sqlite3
import json
from datetime import datetime
from pathlib import Path


class FieldManager:
    """Manage field boundaries and properties"""

    def __init__(self, db_path='/var/lib/precision-ag/precision-ag.db'):
        """Initialize field manager

        Args:
            db_path: Path to SQLite database
        """
        self.db_path = db_path
        self.conn = None

    def connect(self):
        """Connect to database

        Returns:
            bool: True if connection successful
        """
        try:
            # Ensure database directory exists
            Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            return True
        except sqlite3.Error as e:
            print(f"✗ Failed to connect to database: {e}")
            return False

    def disconnect(self):
        """Disconnect from database"""
        if self.conn:
            self.conn.close()

    def initialize_database(self):
        """Initialize database schema"""
        cursor = self.conn.cursor()

        # Create fields table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fields (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                boundary_polygon TEXT NOT NULL,
                area_acres REAL,
                centroid_lat REAL,
                centroid_lon REAL,
                crop_type TEXT,
                soil_type TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Create operations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS operations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                field_id INTEGER NOT NULL,
                operation_type TEXT NOT NULL,
                start_date TIMESTAMP,
                end_date TIMESTAMP,
                product TEXT,
                rate REAL,
                acres_treated REAL,
                notes TEXT,
                FOREIGN KEY (field_id) REFERENCES fields(id)
            )
        ''')

        self.conn.commit()
        print("✓ Database initialized")

    def create_field(self, name, boundary_polygon, crop_type=None, soil_type=None):
        """Create a new field

        Args:
            name: Field name
            boundary_polygon: GeoJSON polygon coordinates
            crop_type: Primary crop type
            soil_type: Primary soil type

        Returns:
            int: Field ID if successful, None otherwise
        """
        cursor = self.conn.cursor()

        try:
            # Calculate area and centroid
            area_acres = self._calculate_area_acres(boundary_polygon)
            centroid = self._calculate_centroid(boundary_polygon)

            # Insert field
            cursor.execute('''
                INSERT INTO fields (name, boundary_polygon, area_acres, centroid_lat, centroid_lon, crop_type, soil_type)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                name,
                json.dumps(boundary_polygon),
                area_acres,
                centroid[0] if centroid else None,
                centroid[1] if centroid else None,
                crop_type,
                soil_type
            ))

            field_id = cursor.lastrowid
            self.conn.commit()

            print(f"✓ Field created: {name} (ID: {field_id})")
            print(f"  Area: {area_acres:.2f} acres")
            if centroid:
                print(f"  Centroid: {centroid[0]:.6f}, {centroid[1]:.6f}")

            return field_id

        except sqlite3.IntegrityError:
            print(f"✗ Field '{name}' already exists")
            return None
        except Exception as e:
            print(f"✗ Failed to create field: {e}")
            return None

    def list_fields(self):
        """List all fields

        Returns:
            list: List of field dictionaries
        """
        cursor = self.conn.cursor()

        cursor.execute('''
            SELECT id, name, area_acres, centroid_lat, centroid_lon,
                   crop_type, soil_type, created_at
            FROM fields
            ORDER BY name
        ''')

        fields = cursor.fetchall()

        if not fields:
            print("No fields found")
            return []

        print(f"\n{'ID':<6} {'Name':<30} {'Area (ac)':<12} {'Crop':<15} {'Soil':<15} {'Created':<20}")
        print("-" * 108)

        for field in fields:
            print(f"{field['id']:<6} {field['name']:<30} {field['area_acres'] or 0:<12.1f} "
                  f"{field['crop_type'] or 'N/A':<15} {field['soil_type'] or 'N/A':<15} "
                  f"{field['created_at']:<20}")

        return [dict(field) for field in fields]

    def get_field(self, field_id):
        """Get field details

        Args:
            field_id: Field ID

        Returns:
            dict: Field details or None
        """
        cursor = self.conn.cursor()

        cursor.execute('''
            SELECT * FROM fields WHERE id = ?
        ''', (field_id,))

        field = cursor.fetchone()

        if not field:
            print(f"✗ Field {field_id} not found")
            return None

        return dict(field)

    def update_field(self, field_id, name=None, boundary_polygon=None, crop_type=None, soil_type=None):
        """Update field

        Args:
            field_id: Field ID
            name: New name
            boundary_polygon: New boundary polygon
            crop_type: New crop type
            soil_type: New soil type

        Returns:
            bool: True if successful
        """
        cursor = self.conn.cursor()

        updates = []
        params = []

        if name:
            updates.append("name = ?")
            params.append(name)

        if boundary_polygon:
            updates.append("boundary_polygon = ?")
            params.append(json.dumps(boundary_polygon))

            # Recalculate area and centroid
            area_acres = self._calculate_area_acres(boundary_polygon)
            centroid = self._calculate_centroid(boundary_polygon)

            updates.append("area_acres = ?")
            params.append(area_acres)

            if centroid:
                updates.append("centroid_lat = ?")
                params.append(centroid[0])
                updates.append("centroid_lon = ?")
                params.append(centroid[1])

        if crop_type:
            updates.append("crop_type = ?")
            params.append(crop_type)

        if soil_type:
            updates.append("soil_type = ?")
            params.append(soil_type)

        if not updates:
            print("No updates specified")
            return False

        updates.append("updated_at = CURRENT_TIMESTAMP")
        params.append(field_id)

        cursor.execute(f'''
            UPDATE fields SET {', '.join(updates)} WHERE id = ?
        ''', params)

        if cursor.rowcount > 0:
            self.conn.commit()
            print(f"✓ Field {field_id} updated")
            return True
        else:
            print(f"✗ Field {field_id} not found")
            return False

    def delete_field(self, field_id):
        """Delete field

        Args:
            field_id: Field ID

        Returns:
            bool: True if successful
        """
        cursor = self.conn.cursor()

        cursor.execute('DELETE FROM fields WHERE id = ?', (field_id,))

        if cursor.rowcount > 0:
            self.conn.commit()
            print(f"✓ Field {field_id} deleted")
            return True
        else:
            print(f"✗ Field {field_id} not found")
            return False

    def _calculate_area_acres(self, boundary_polygon):
        """Calculate area in acres from polygon

        Args:
            boundary_polygon: GeoJSON polygon coordinates

        Returns:
            float: Area in acres
        """
        # Simplified area calculation using shoelace formula
        # For production use, consider using shapely for accurate calculations

        try:
            coords = boundary_polygon['coordinates'][0]  # Exterior ring

            # Remove closing point (duplicate of first)
            if coords[0] == coords[-1]:
                coords = coords[:-1]

            # Convert to meters (rough approximation for small areas)
            # Assumes WGS84 coordinates
            lat_avg = sum(c[1] for c in coords) / len(coords)
            meters_per_degree_lat = 111320.0
            meters_per_degree_lon = 111320.0 * abs(0.0000001 / (1 / 3600.0))

            # Apply shoelace formula
            area_m2 = 0.0
            n = len(coords)
            for i in range(n):
                j = (i + 1) % n
                area_m2 += coords[i][0] * coords[j][1]
                area_m2 -= coords[j][0] * coords[i][1]

            area_m2 = abs(area_m2) * meters_per_degree_lat * meters_per_degree_lon / 2.0

            # Convert to acres
            area_acres = area_m2 / 4046.86

            return area_acres

        except Exception as e:
            print(f"Warning: Could not calculate area: {e}")
            return 0.0

    def _calculate_centroid(self, boundary_polygon):
        """Calculate centroid of polygon

        Args:
            boundary_polygon: GeoJSON polygon coordinates

        Returns:
            tuple: (latitude, longitude) or None
        """
        try:
            coords = boundary_polygon['coordinates'][0]

            # Remove closing point
            if coords[0] == coords[-1]:
                coords = coords[:-1]

            # Simple average (not accurate for complex polygons)
            avg_lat = sum(c[1] for c in coords) / len(coords)
            avg_lon = sum(c[0] for c in coords) / len(coords)

            return (avg_lat, avg_lon)

        except Exception:
            return None


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Manage field boundaries for precision agriculture'
    )
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # Create command
    create_parser = subparsers.add_parser('create', help='Create a new field')
    create_parser.add_argument('--name', required=True, help='Field name')
    create_parser.add_argument('--boundary', help='GeoJSON boundary file')
    create_parser.add_argument('--crop-type', help='Crop type')
    create_parser.add_argument('--soil-type', help='Soil type')

    # List command
    subparsers.add_parser('list', help='List all fields')

    # Get command
    get_parser = subparsers.add_parser('get', help='Get field details')
    get_parser.add_argument('--field-id', required=True, type=int, help='Field ID')

    # Update command
    update_parser = subparsers.add_parser('update', help='Update a field')
    update_parser.add_argument('--field-id', required=True, type=int, help='Field ID')
    update_parser.add_argument('--name', help='New field name')
    update_parser.add_argument('--boundary', help='New GeoJSON boundary file')
    update_parser.add_argument('--crop-type', help='New crop type')
    update_parser.add_argument('--soil-type', help='New soil type')

    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a field')
    delete_parser.add_argument('--field-id', required=True, type=int, help='Field ID')

    # Init command
    subparsers.add_parser('init', help='Initialize database')

    args = parser.parse_args()

    # Get database path from environment or use default
    import os
    db_path = os.getenv('DB_PATH', '/var/lib/precision-ag/precision-ag.db')

    manager = FieldManager(db_path=db_path)

    if not manager.connect():
        sys.exit(1)

    try:
        if args.command == 'init':
            manager.initialize_database()
        elif args.command == 'create':
            # Load boundary from file or create example
            if args.boundary:
                with open(args.boundary, 'r') as f:
                    boundary = json.load(f)
            else:
                print("Error: --boundary required")
                sys.exit(1)

            manager.create_field(
                args.name,
                boundary,
                args.crop_type,
                args.soil_type
            )
        elif args.command == 'list':
            manager.list_fields()
        elif args.command == 'get':
            field = manager.get_field(args.field_id)
            if field:
                print(json.dumps(field, indent=2))
        elif args.command == 'update':
            boundary = None
            if args.boundary:
                with open(args.boundary, 'r') as f:
                    boundary = json.load(f)

            manager.update_field(
                args.field_id,
                args.name,
                boundary,
                args.crop_type,
                args.soil_type
            )
        elif args.command == 'delete':
            manager.delete_field(args.field_id)
        else:
            parser.print_help()
    finally:
        manager.disconnect()


if __name__ == '__main__':
    main()
