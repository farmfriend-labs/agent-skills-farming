# Setting Up Mobile Data Collection

This example demonstrates setting up mobile data collection for field observations using Invisible Data Logger.

## Scenario

You want to collect field observations, equipment logs, and input applications using your smartphone while in the field. Data should sync to a central database when you have WiFi connectivity.

## Setup

### 1. Install Mobile App

For the demonstration, we'll use a simple web-based mobile interface (in production, you'd use a native app):

```bash
cd /tmp/agent-skills-farming/skills/invisible-data-logger
python3 -m http.server 8080
```

Access on mobile device at: `http://your-server-ip:8080/mobile`

### 2. Configure Offline Storage

The app will store data locally when offline and sync when connected.

Configuration in `config.json`:
```json
{
  "offline_storage": true,
  "storage_path": "/sdcard/field_data",
  "sync_on_wifi": true,
  "sync_interval_minutes": 5
}
```

### 3. Create Data Entry Forms

Define mobile-friendly forms for different data types:

**Field Observation Form:**
```html
<form id="field_observation">
  <label>Field:</label>
  <select id="field_name">
    <option>North 40</option>
    <option>East 80</option>
    <option>South 25</option>
  </select>

  <label>Date:</label>
  <input type="date" id="observation_date">

  <label>Observation Type:</label>
  <select id="observation_type">
    <option>crop_condition</option>
    <option>pest_pressure</option>
    <option>disease_symptoms</option>
    <option>weather_damage</option>
    <option>other</option>
  </select>

  <label>Description:</label>
  <textarea id="description" rows="4"></textarea>
  <button type="button" id="voice_button">🎤 Speak</button>

  <label>Severity:</label>
  <select id="severity">
    <option>Low</option>
    <option>Medium</option>
    <option>High</option>
  </select>

  <label>Photos:</label>
  <input type="file" id="photos" accept="image/*" multiple>

  <label>GPS Location:</label>
  <button type="button" id="gps_button">📍 Capture Location</button>
  <div id="gps_coords"></div>

  <button type="submit">Save Observation</button>
</form>
```

### 4. Implement GPS Capture

JavaScript for automatic GPS capture:
```javascript
document.getElementById('gps_button').addEventListener('click', function() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      function(position) {
        const lat = position.coords.latitude;
        const lon = position.coords.longitude;
        const accuracy = position.coords.accuracy;

        document.getElementById('gps_coords').innerHTML =
          `Lat: ${lat.toFixed(6)}, Lon: ${lon.toFixed(6)}<br>
           Accuracy: ${accuracy.toFixed(0)}m`;

        // Store in hidden fields
        document.getElementById('latitude').value = lat;
        document.getElementById('longitude').value = lon;
        document.getElementById('gps_accuracy').value = accuracy;
      },
      function(error) {
        alert('GPS error: ' + error.message);
      },
      {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 0
      }
    );
  } else {
    alert('Geolocation not supported');
  }
});
```

### 5. Implement Voice Logging

Voice-to-text for hands-free data entry:
```javascript
document.getElementById('voice_button').addEventListener('click', function() {
  if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition ||
                            window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    recognition.lang = 'en-US';

    recognition.onresult = function(event) {
      const transcript = event.results[0][0].transcript;
      const confidence = event.results[0][0].confidence;

      document.getElementById('description').value += transcript;

      // Save voice audio
      navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
          const mediaRecorder = new MediaRecorder(stream);
          // ... save audio file
        });
    };

    recognition.start();
    document.getElementById('voice_button').textContent = '🔴 Recording...';
  } else {
    alert('Speech recognition not supported');
  }
});
```

### 6. Store Data Offline

Using IndexedDB for offline storage:
```javascript
const dbName = 'FieldDataDB';
const request = indexedDB.open(dbName, 1);

request.onupgradeneeded = function(event) {
  const db = event.target.result;
  const objectStore = db.createObjectStore('observations', {
    keyPath: 'id',
    autoIncrement: true
  });

  objectStore.createIndex('synced', 'synced', { unique: false });
};

request.onsuccess = function(event) {
  const db = event.target.result;

  // Save observation offline
  function saveOffline(observation) {
    const transaction = db.transaction(['observations'], 'readwrite');
    const objectStore = transaction.objectStore('observations');

    observation.synced = false;
    observation.created_at = new Date().toISOString();

    const request = objectStore.add(observation);

    request.onsuccess = function() {
      alert('Saved offline. Will sync when connected.');
    };
  }

  // Sync when connected
  function syncData() {
    const transaction = db.transaction(['observations'], 'readonly');
    const objectStore = transaction.objectStore('observations');
    const index = objectStore.index('synced');
    const request = index.getAll(false); // Get all unsynced

    request.onsuccess = function() {
      const observations = request.result;

      observations.forEach(observation => {
        // Send to server
        fetch('/api/observations', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(observation)
        })
        .then(response => {
          // Mark as synced
          const updateTx = db.transaction(['observations'], 'readwrite');
          const updateStore = updateTx.objectStore('observations');
          observation.synced = true;
          updateStore.put(observation);
        });
      });
    };
  }

  // Auto-sync when online
  window.addEventListener('online', syncData);
};
```

### 7. Configure Automatic Sync

Server-side sync script:
```python
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

@app.route('/api/observations', methods=['POST'])
def sync_observation():
    data = request.json

    conn = sqlite3.connect('/opt/invisible-logger/data.db')
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO observations (
            observation_type, category, date, time,
            field_id, latitude, longitude, gps_accuracy,
            notes, recorded_by, synced
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get('observation_type'),
        data.get('category'),
        data.get('date'),
        data.get('time'),
        data.get('field_id'),
        data.get('latitude'),
        data.get('longitude'),
        data.get('gps_accuracy'),
        data.get('description'),
        data.get('recorded_by'),
        True  # Mark as synced
    ))

    conn.commit()
    conn.close()

    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

## Usage Example

### In the Field - Crop Observation

1. Open mobile app: `http://server-ip:8080/mobile`
2. Select field: "North 40"
3. Select type: "pest_pressure"
4. Tap voice button: "Aphids detected in 30% of plants mostly on leaves"
5. Select severity: "Medium"
6. Tap GPS button: Captures location (41.8781, -87.6298, 8m accuracy)
7. Take 2 photos of aphids
8. Tap "Save Observation"

Data is stored locally (no connectivity needed).

### Back at Farm - Automatic Sync

1. Connect to WiFi
2. App automatically detects connection
3. All offline observations sync to central database
4. App confirms: "Synced 3 observations"

### Review Synced Data

Check what was collected:
```sql
SELECT
  date,
  observation_type,
  category,
  notes,
  severity,
  latitude,
  longitude
FROM observations
WHERE date >= DATE('now', '-1 day')
ORDER BY date DESC;
```

Output:
```
date         | observation_type  | category        | notes                                | severity
-------------|------------------|-----------------|--------------------------------------|----------
2024-06-15   | pest_pressure     | crop_condition   | Aphids detected in 30% of plants      | Medium
2024-06-15   | crop_condition    | stand           | Good stand, uniform emergence         | Low
2024-06-14   | equipment_log     | maintenance     | Changed oil in combine               | Low
```

## Advanced Features

### Photo Metadata

Automatically capture metadata when taking photos:
- GPS location
- Timestamp
- Camera orientation
- Device information

### Barcode Scanning

Scan product labels for input application logging:
```javascript
// Scan barcode for fertilizer bag
document.getElementById('scan_button').addEventListener('click', function() {
  Quagga.init({
    inputStream: { name: "Live", type: "LiveStream", target: document.querySelector('#scanner') },
    decoder: { readers: ["ean_reader", "code_128_reader"] }
  }, function(err) {
    if (err) {
      console.log(err);
      return;
    }
    Quagga.start();
  });

  Quagga.onDetected(function(data) {
    const code = data.codeResult.code;
    document.getElementById('product_barcode').value = code;

    // Look up product info
    lookupProduct(code);
  });
});
```

### Field Maps with Observations

Display all observations on field map:
```javascript
// Load field boundary and observations
const fieldBoundary = loadFieldBoundary('North 40');
const observations = loadObservations('North 40');

// Create map with Leaflet
const map = L.map('map').setView([fieldBoundary.center.lat,
                                   fieldBoundary.center.lon], 16);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

// Add field boundary
L.geoJSON(fieldBoundary, {
  style: { color: '#2563eb', weight: 3 }
}).addTo(map);

// Add observation markers
observations.forEach(obs => {
  const marker = L.marker([obs.latitude, obs.longitude]).addTo(map);

  // Color by severity
  const colors = { 'Low': 'green', 'Medium': 'orange', 'High': 'red' };
  marker.bindPopup(`
    <b>${obs.observation_type}</b><br>
    ${obs.notes}<br>
    Severity: ${obs.severity}
  `);
});
```

## Best Practices

**Data Collection:**
- Collect data while it's fresh in memory
- Use voice logging when driving or operating equipment
- Take photos to document observations
- Capture GPS location for precise tracking

**Sync Strategy:**
- Sync automatically when on WiFi
- Manual sync option for urgent data
- Regular backups to prevent data loss
- Verify sync status regularly

**Mobile Usage:**
- Keep app shortcuts on home screen
- Pre-fill common data (field, user)
- Use offline mode in remote areas
- Test app before relying on it in field

**Data Quality:**
- Validate data when possible
- Use consistent terminology
- Include enough detail for future reference
- Review data weekly for completeness

## References

- SKILL.md - Full documentation
- examples/sensor-setup.md - Sensor integration guide
- examples/voice-logging.md - Advanced voice logging
