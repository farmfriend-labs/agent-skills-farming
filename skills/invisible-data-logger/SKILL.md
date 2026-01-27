# Invisible Data Logger

Log agricultural data without expensive proprietary equipment using commodity hardware and open-source tools.

## Purpose

Capture field, equipment, and environmental data using affordable, accessible technology. Enable data collection capabilities similar to expensive farm management software subscriptions using smartphones, basic sensors, and open-source software. Farmers can log, store, and analyze their own data without paying for proprietary systems.

## Problem Solved

Farmers want data-driven decision making but face barriers:
- Proprietary farm software subscriptions cost $500-$5,000 annually
- Equipment manufacturer data capture requires expensive equipment
- Data is locked in proprietary formats unusable elsewhere
- Cloud-based systems require internet connectivity in remote areas
- Subscription software stops working when payments lapse
- Data ownership and privacy concerns with cloud platforms
- Small farms can't justify expensive precision agriculture equipment
- Mobile connectivity is unreliable in rural areas

Invisible Data Logger provides affordable, offline-capable data logging using hardware farmers already own.

## Capabilities

- **Mobile Data Collection:** Use smartphone apps for field data entry
- **Voice Logging:** Record field notes via voice-to-text
- **Photo Logging:** Capture and annotate field photos with metadata
- **GPS Tracking:** Log field boundaries, sampling points, and observation locations
- **Sensor Integration:** Connect low-cost IoT sensors for automated logging
- **Offline Mode:** Collect data without internet connectivity
- **Sync When Available:** Automatically sync data when connection restored
- **Export Capabilities:** Export data in standard formats (CSV, JSON, GeoJSON)
- **Simple Dashboard:** Basic visualization of collected data
- **Automated Reminders:** Remind users to log routine data (field walks, equipment checks)
- **Template-Based Entry:** Pre-configured forms for common data types
- **Barcode/QR Scanning:** Scan equipment tags or product labels
- **Voice Commands:** Hands-free data entry during operations
- **Local Storage:** All data stored locally on farm equipment or mobile device
- **Data Backup:** Backup to USB or network drive

## Instructions

### Usage by AI Agent

1. **Configure Data Collection Points**
   - Identify what data to collect (field observations, equipment hours, weather, inputs)
   - Create data entry templates for each data type
   - Set up automated collection points (sensors, GPS)
   - Configure voice logging for hands-free use

2. **Set Up Mobile Collection**
   - Install mobile data collection app
   - Configure offline data storage
   - Set up sync preferences (WiFi, USB, manual)
   - Create user-friendly entry forms
   - Configure voice recognition settings

3. **Integrate Sensors**
   - Connect temperature/humidity sensors to storage areas
   - Set up soil moisture probes in key fields
   - Install equipment hour meters if not present
   - Configure data collection intervals
   - Set up alerts for sensor readings outside thresholds

4. **Establish Collection Routines**
   - Schedule regular data collection tasks
   - Create reminder notifications for routine logging
   - Train farm workers on data collection methods
   - Establish backup procedures
   - Document data collection workflow

5. **Manage and Sync Data**
   - Collect data in field using mobile app
   - Use voice logging during equipment operation
   - Take photos with automatic metadata capture
   - Sync data to central storage when available
   - Create regular backups to external storage

6. **Analyze Collected Data**
   - Export data for analysis in spreadsheet or specialized tools
   - Generate basic reports and summaries
   - Identify trends and patterns
   - Correlate data types (e.g., weather vs. field observations)

## Hardware Options

### Mobile Data Collection
- **Smartphone:** Any modern smartphone with camera, GPS, and microphone
- **Tablet:** Larger screen for easier data entry
- ** ruggedized tablets:** For harsh field conditions (optional)

### Low-Cost Sensors
- **Temperature/Humidity:** $10-20 (DHT22, SHT31)
- **Soil Moisture:** $15-30 (capacitive soil moisture sensors)
- **Rain Gauge:** $25-50 (tipping bucket rain gauge)
- **Equipment Hour Meter:** $10-30 (digital hour meter)
- **GPS Module:** $20-40 (for equipment without built-in GPS)

### Storage
- **USB Drive:** Backup data storage
- **External Hard Drive:** Central data storage
- **Raspberry Pi:** Local data server (optional, $50-100)
- **NAS:** Network-attached storage for multiple users

## Data Types to Log

### Field Operations
- Field work performed (tillage, planting, spraying, harvest)
- Equipment used and hours
- Conditions during operation (weather, soil moisture)
- Issues encountered (equipment problems, field conditions)
- Yield observations during harvest

### Crop Conditions
- Stand establishment counts
- Pest pressure observations
- Disease symptoms
- Weed pressure and species identification
- Weather damage reports
- Growth stage observations

### Equipment
- Daily/weekly equipment hours
- Fuel consumption
- Maintenance performed
- Equipment issues or breakdowns
- Repair costs and parts

### Inputs
- Fertilizer applications (product, rate, date, field)
- Chemical applications (product, rate, date, field, conditions)
- Seed usage (variety, rate, date, field)
- Irrigation applications (timing, amount, method)

### Environment
- Daily weather observations
- Rainfall measurements
- Temperature readings (air and soil)
- Soil moisture readings
- Wind observations

### Financial
- Input purchases (receipts, costs)
- Equipment repairs and maintenance costs
- Fuel purchases
- Labor hours (if tracking)

## Tools

- **Python 3.8+** for data management and processing
- **SQLite** for local data storage
- **Flask/Django** for optional web interface
- **Kivy/BeeWare** for mobile app (optional)
- **Requests** for sync when connected
- **OpenCV/PIL** for image processing
- **SpeechRecognition** for voice-to-text
- **Pandas** for data analysis
- **Matplotlib** for basic visualization

## Environment Variables

```bash
# Database Configuration
DATA_DB_PATH=/opt/invisible-logger/data.db
BACKUP_PATH=/opt/invisible-logger/backups
AUTO_BACKUP_ENABLED=true
BACKUP_INTERVAL=daily

# Mobile Collection
MOBILE_APP_ENABLED=true
MOBILE_DATA_PATH=/mobile/data
SYNC_ON_WIFI=true
SYNC_INTERVAL_HOURS=1

# Voice Logging
VOICE_RECOGNITION_ENABLED=true
VOICE_LANGUAGE=en-US
VOICE_SAVE_AUDIO=false

# Sensor Integration
SENSOR_ENABLED=true
SENSOR_DATA_INTERVAL=300  # seconds
SENSOR_ALERT_ENABLED=true

# GPS Configuration
GPS_ENABLED=true
GPS_ACCURACY=10  # meters

# Export Settings
EXPORT_FORMAT=csv
EXPORT_INCLUDE_IMAGES=true
EXPORT_PATH=/opt/invisible-logger/exports

# Logging
LOG_LEVEL=info
LOG_FILE=/var/log/invisible-data-logger.log

# Notifications
REMINDER_ENABLED=true
REMINDER_TIMES=08:00,17:00
NOTIFICATION_SOUND=default

# Backup Settings
BACKUP_TO_USB=true
USB_MOUNT_POINT=/media/usb
BACKUP_RETENTION_DAYS=90
```

## Database Schema

### Observations Table
```sql
CREATE TABLE observations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  observation_type TEXT NOT NULL,  -- field, equipment, weather, input
  category TEXT,
  subcategory TEXT,
  date DATE NOT NULL,
  time TEXT,
  field_id INTEGER,
  equipment_id INTEGER,
  latitude REAL,
  longitude REAL,
  gps_accuracy REAL,
  notes TEXT,
  recorded_by TEXT,
  synced BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Observation Data Table
```sql
CREATE TABLE observation_data (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  observation_id INTEGER NOT NULL,
  data_key TEXT NOT NULL,
  data_value TEXT,
  data_value_numeric REAL,
  data_unit TEXT,
  FOREIGN KEY (observation_id) REFERENCES observations(id)
);
```

### Images Table
```sql
CREATE TABLE images (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  observation_id INTEGER,
  file_path TEXT NOT NULL,
  description TEXT,
  taken_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (observation_id) REFERENCES observations(id)
);
```

### Sensor Readings Table
```sql
CREATE TABLE sensor_readings (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  sensor_id INTEGER NOT NULL,
  sensor_type TEXT NOT NULL,
  reading_value REAL NOT NULL,
  unit TEXT,
  reading_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  location_id INTEGER,
  FOREIGN KEY (sensor_id) REFERENCES sensors(id)
);
```

### Sensors Table
```sql
CREATE TABLE sensors (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  sensor_type TEXT NOT NULL,  -- temperature, humidity, soil_moisture, rain
  location TEXT,
  field_id INTEGER,
  collection_interval INTEGER,
  alert_threshold_min REAL,
  alert_threshold_max REAL,
  active BOOLEAN DEFAULT TRUE
);
```

### Voice Logs Table
```sql
CREATE TABLE voice_logs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  audio_file_path TEXT,
  transcribed_text TEXT,
  observation_id INTEGER,
  recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  confidence_score REAL
);
```

### Reminders Table
```sql
CREATE TABLE reminders (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  reminder_type TEXT NOT NULL,
  reminder_text TEXT,
  time TEXT NOT NULL,
  days TEXT,  -- comma-separated days of week
  active BOOLEAN DEFAULT TRUE
);
```

## Data Entry Templates

### Field Observation Template
```
Date: [auto-populate]
Field: [dropdown]
Observation Type: [dropdown]
  - Crop condition
  - Pest pressure
  - Disease symptoms
  - Weather damage
  - Other

Description: [text or voice]
Severity: [Low/Medium/High]
Action Taken: [text or voice]
Follow-up Required: [Yes/No]
Photos: [camera button]
GPS Location: [auto-capture]
```

### Equipment Log Template
```
Date: [auto-populate]
Equipment: [dropdown]
Operation Type: [dropdown]
  - Routine operation
  - Maintenance performed
  - Issue observed
  - Other

Hours Today: [number]
Total Hours: [auto-calculate]
Description: [text or voice]
Photos: [camera button]
```

### Input Application Template
```
Date: [auto-populate]
Field: [dropdown]
Input Type: [dropdown]
  - Fertilizer
  - Chemical
  - Seed
  - Irrigation
  - Other

Product: [text or scan barcode]
Rate: [number]
Unit: [dropdown]
Method: [dropdown]
Total Quantity: [auto-calculate]
Cost: [number]
Conditions: [text]
GPS: [auto-capture field boundary]
```

## Voice Commands

Enable hands-free data entry with voice commands:

**Field Observation:**
"Log field observation North 40 crop condition standing water in low areas severity medium"

**Equipment Log:**
"Log equipment combine operation 4.5 hours today total 245 hours"

**Input Application:**
"Log input application North 40 fertilizer 28-0-0 rate 30 gallons per acre total 1215 gallons"

**Weather:**
"Log weather observation 0.5 inches rain temperature 78 degrees"

**General Note:**
"Take note remember to check planter calibration before next planting"

## Sensor Setup Examples

### Soil Moisture Sensor (Arduino/ESP32)
```python
import sqlite3
import time
import board
import adafruit_dht

# Initialize sensor
dht = adafruit_dht.DHT22(board.D4)

# Database connection
conn = sqlite3.connect('/opt/invisible-logger/data.db')

while True:
    try:
        # Read sensor
        temperature = dht.temperature
        humidity = dht.humidity

        # Store reading
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO sensor_readings
            (sensor_id, sensor_type, reading_value, unit)
            VALUES (?, ?, ?, ?)
        """, (1, 'humidity', humidity, '%'))
        conn.commit()

        # Check thresholds
        if humidity < 30 or humidity > 90:
            # Trigger alert
            print(f"ALERT: Humidity {humidity}% outside range")

        time.sleep(300)  # Wait 5 minutes

    except Exception as e:
        print(f"Error: {e}")
        time.sleep(60)
```

### Temperature/Humidity Sensor (Storage Monitoring)
Monitor grain bin temperature to detect spoilage risk.

### Equipment Hour Meter
Connect to equipment ignition circuit or use vibration sensor to log equipment usage.

## Export Formats

### CSV Export
```csv
observation_id,date,time,observation_type,field,category,notes,latitude,longitude
1,2024-01-15,08:30,field_observation,North 40,crop_condition,Standing water in low areas due to recent rain,41.8781,-87.6298
2,2024-01-15,14:45,equipment_log,combine,maintenance,Changed oil and filters,,,
```

### GeoJSON Export
For mapping field observations and sample points:
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [-87.6298, 41.8781]
      },
      "properties": {
        "observation_type": "field_observation",
        "date": "2024-01-15",
        "category": "pest_pressure",
        "notes": "Aphids detected in 50% of plants"
      }
    }
  ]
}
```

## Examples

See examples/ directory for:
- Setting up mobile data collection
- Installing soil moisture sensors
- Voice logging setup
- Data export and analysis

## References

### Hardware Resources
- **Arduino:** Platform for sensor integration
- **Raspberry Pi:** Local data server option
- **Adafruit:** Sensor components and tutorials

### Software Resources
- **OpenDataKit:** Open-source mobile data collection
- **KODI:** Field data collection platform
- **OpenFarm:** Open-source farm management

### Technical References
See references/technical-docs.md for:
- Sensor integration guides
- API documentation
- Database schema details
- Integration with other tools

## Troubleshooting

### Mobile App Issues

**App not syncing:**
- Check WiFi connection
- Verify sync settings
- Try manual sync
- Check for app updates

**GPS not capturing:**
- Enable location services
- Check GPS accuracy
- Verify location permissions
- Try outdoor location

### Sensor Issues

**Sensor not reading:**
- Check connections
- Verify power supply
- Test sensor individually
- Check data logs for errors

**Readings seem wrong:**
- Verify sensor calibration
- Check for interference
- Compare to manual readings
- Replace sensor if needed

### Data Issues

**Missing data entries:**
- Check sync status
- Look for unsaved records
- Review backup files
- Check application logs

**Export fails:**
- Check export path permissions
- Verify disk space
- Check file size limits
- Try different export format

## Testing

1. **Unit Testing**
   - Test database operations
   - Verify sensor data capture
   - Test export functionality
   - Check backup procedures

2. **Integration Testing**
   - Test mobile app sync
   - Verify voice recognition
   - Test sensor integration
   - Check data export to analysis tools

3. **Field Testing**
   - Test data collection in field conditions
   - Verify offline functionality
   - Test sensor durability
   - Check battery life for mobile devices

## Version History

- **1.0.0** - Initial release with mobile collection and sensor integration

## License

MIT License - Open source, free to use, modify, and distribute.

## Support

For issues, questions, or contributions:
- GitHub Issues: https://github.com/farmfriend-labs/agent-skills-farming/issues
- Email: farmfriend.labs@gmail.com
