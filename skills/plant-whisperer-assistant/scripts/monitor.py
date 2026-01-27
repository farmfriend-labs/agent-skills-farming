#!/usr/bin/env python3
"""
monitor.py - Plant health monitoring service
Monitors plant health and generates alerts
"""

import argparse
import sys
import os
import time
import logging
from datetime import datetime, timedelta
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

try:
    import sqlite3
    import yaml
except ImportError as e:
    print(f"Error: Required library not installed: {e}")
    sys.exit(1)

# Load configuration
def load_config():
    """Load configuration from .env file"""
    config = {}

    defaults = {
        'ANALYSIS_MODE': 'standard',
        'LOG_LEVEL': 'info',
        'LOG_FILE': '/var/log/plant-whisperer.log',
        'PLANT_DB_PATH': '/opt/plant-whisperer/plants.db',
        'IMAGE_STORAGE_PATH': '/opt/plant-whisperer/images',
        'ALERT_EMAIL_ENABLED': 'false',
        'ALERT_EMAIL': '',
        'ALERT_SEVERITY_THRESHOLD': 'warning',
        'MONITOR_INTERVAL': '3600',  # 1 hour
    }

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    env_file = os.path.join(project_root, '.env')

    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    config[key] = value

    for key, value in defaults.items():
        if key not in config:
            config[key] = value

    return config

def setup_logging(config):
    """Setup logging configuration"""
    log_level = getattr(logging, config['LOG_LEVEL'].upper(), logging.INFO)
    log_file = config['LOG_FILE']

    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )

    return logging.getLogger('plant_monitor')

class ImageHandler(FileSystemEventHandler):
    """Handle new image events"""

    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.analyze = __import__('analyze_plant', fromlist=['comprehensive_analysis'])

    def on_created(self, event):
        """Handle new image file creation"""
        if event.is_directory:
            return

        # Check if it's an image file
        file_path = event.src_path
        if file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
            self.logger.info(f"New image detected: {file_path}")

            # Extract plant ID from path (e.g., /path/images/plant_123/image.jpg)
            plant_id = self.extract_plant_id(file_path)

            if plant_id:
                try:
                    # Run analysis
                    results = self.analyze.comprehensive_analysis(
                        file_path, plant_id, self.config, self.logger
                    )
                    self.logger.info(f"Analysis completed for plant {plant_id}")
                except Exception as e:
                    self.logger.error(f"Analysis failed: {str(e)}")

    def extract_plant_id(self, file_path):
        """Extract plant ID from file path"""
        # Try to extract from directory name (e.g., plant_123)
        parent_dir = os.path.basename(os.path.dirname(file_path))
        if parent_dir.startswith('plant_'):
            try:
                return int(parent_dir.split('_')[1])
            except ValueError:
                pass

        # Try to extract from filename (e.g., plant123_image.jpg)
        filename = os.path.basename(file_path)
        if filename.startswith('plant'):
            try:
                # Extract number after 'plant'
                import re
                match = re.search(r'plant(\d+)', filename)
                if match:
                    return int(match.group(1))
            except ValueError:
                pass

        return None

def check_alerts(config, logger):
    """Check for plants that need attention and create alerts"""
    db_path = config['PLANT_DB_PATH']

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Find plants with recent analyses below health threshold
        threshold = 70  # Health score threshold
        days_ago = (datetime.now() - timedelta(days=7)).isoformat()

        cursor.execute("""
        SELECT DISTINCT p.id, p.name, p.species, MAX(a.analysis_date) as last_analysis,
               MAX(a.overall_health_score) as latest_score
        FROM plants p
        JOIN analyses a ON p.id = a.plant_id
        WHERE a.analysis_date > ? AND a.overall_health_score < ?
        GROUP BY p.id
        """, (days_ago, threshold))

        low_health_plants = cursor.fetchall()

        for plant_id, name, species, last_analysis, score in low_health_plants:
            # Check if alert already exists
            cursor.execute("""
            SELECT COUNT(*) FROM alerts
            WHERE plant_id = ? AND acknowledged = 0 AND created_at > ?
            """, (plant_id, days_ago))

            if cursor.fetchone()[0] == 0:
                # Create new alert
                severity = 'critical' if score < 50 else 'warning'
                message = f"Plant '{name}' (ID: {plant_id}) health score is {score}/100. Recent issues detected."

                cursor.execute("""
                INSERT INTO alerts (plant_id, alert_type, severity, message)
                VALUES (?, 'health_check', ?, ?)
                """, (plant_id, severity, message))

                logger.warning(f"Alert created for plant {plant_id} ({name}): {message}")

        conn.commit()
        conn.close()

    except sqlite3.Error as e:
        logger.error(f"Database error checking alerts: {str(e)}")

def print_status(config, logger):
    """Print current monitoring status"""
    db_path = config['PLANT_DB_PATH']

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Count plants
        cursor.execute("SELECT COUNT(*) FROM plants")
        plant_count = cursor.fetchone()[0]

        # Count recent analyses
        days_ago = (datetime.now() - timedelta(days=7)).isoformat()
        cursor.execute("SELECT COUNT(*) FROM analyses WHERE analysis_date > ?", (days_ago,))
        analysis_count = cursor.fetchone()[0]

        # Count unacknowledged alerts
        cursor.execute("SELECT COUNT(*) FROM alerts WHERE acknowledged = 0")
        alert_count = cursor.fetchone()[0]

        # Calculate average health score
        cursor.execute("""
        SELECT AVG(overall_health_score) FROM analyses
        WHERE analysis_date > ?
        """, (days_ago,))

        avg_score = cursor.fetchone()[0]

        print("\n" + "="*60)
        print("PLANT MONITOR STATUS")
        print("="*60)
        print(f"Plants tracked: {plant_count}")
        print(f"Analyses (last 7 days): {analysis_count}")
        print(f"Unacknowledged alerts: {alert_count}")
        if avg_score:
            print(f"Average health score: {avg_score:.1f}/100")
        print("="*60 + "\n")

        conn.close()

    except sqlite3.Error as e:
        logger.error(f"Database error checking status: {str(e)}")

def run_service(config, logger):
    """Run the monitoring service"""
    logger.info("Starting Plant Whisperer monitoring service")
    logger.info(f"Image storage path: {config['IMAGE_STORAGE_PATH']}")
    logger.info(f"Database: {config['PLANT_DB_PATH']}")

    # Setup file watcher if image directory exists
    observer = None
    if os.path.exists(config['IMAGE_STORAGE_PATH']):
        event_handler = ImageHandler(config, logger)
        observer = Observer()
        observer.schedule(event_handler, config['IMAGE_STORAGE_PATH'], recursive=True)
        observer.start()
        logger.info("File watcher started")
    else:
        logger.warning(f"Image storage directory not found: {config['IMAGE_STORAGE_PATH']}")
        logger.info("File watching disabled")

    try:
        monitor_interval = int(config.get('MONITOR_INTERVAL', '3600'))
        logger.info(f"Monitor interval: {monitor_interval} seconds")

        while True:
            # Print status
            print_status(config, logger)

            # Check for alerts
            check_alerts(config, logger)

            # Wait for next cycle
            logger.info(f"Sleeping for {monitor_interval} seconds...")
            time.sleep(monitor_interval)

    except KeyboardInterrupt:
        logger.info("Shutting down monitoring service...")
    finally:
        if observer:
            observer.stop()
            observer.join()
        logger.info("Monitoring service stopped")

def main():
    parser = argparse.ArgumentParser(description='Plant health monitoring service')
    parser.add_argument('--mode', '-m', help='Analysis mode')
    parser.add_argument('--database', '-d', help='Database path')
    parser.add_argument('--log-level', '-l', help='Log level')
    parser.add_argument('--log-file', '-f', help='Log file path')
    parser.add_argument('--status', '-s', action='store_true', help='Print status and exit')

    args = parser.parse_args()

    # Load configuration
    config = load_config()

    # Override with command line arguments
    if args.mode:
        config['ANALYSIS_MODE'] = args.mode
    if args.database:
        config['PLANT_DB_PATH'] = args.database
    if args.log_level:
        config['LOG_LEVEL'] = args.log_level
    if args.log_file:
        config['LOG_FILE'] = args.log_file

    # Setup logging
    logger = setup_logging(config)

    try:
        # If status only, print and exit
        if args.status:
            print_status(config, logger)
            return 0

        # Run monitoring service
        run_service(config, logger)
        return 0

    except Exception as e:
        logger.error(f"Service error: {str(e)}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
