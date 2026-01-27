# Example: Setting Up Your First Field Boundary

This walkthrough demonstrates how to create a GPS-driven field boundary for precision agriculture operations.

## Prerequisites

- GPS receiver connected to your computer
- .env file configured with GPS port
- Database initialized (run `./scripts/setup.sh`)

## Step 1: Verify GPS Connection

```bash
./run.sh gps-status
```

Expected output:
```
✓ Connected to GPS on /dev/ttyUSB0
  Baudrate: 9600

Reading GPS data for 10 seconds...
Time                 Type       Sats    Fix    HDOP    Lat           Lon
14:23:45             GPGGA      12      GPS    1.2     40.712800    -74.006000
14:23:46             GPGGA      12      GPS    1.1     40.712801    -74.006001
...

================================================================================
GPS STATUS SUMMARY
================================================================================

Sentences read: 120
Fix Type: GPS (1)
Position: 40.712801, -74.006001
Altitude: 125.4 meters
HDOP: 1.1
Estimated Accuracy: 2.2m (Good (1-3 meters))

================================================================================
```

## Step 2: Create Field Boundary

For this example, we'll create a simple rectangular field. In production, you would drive the field perimeter with GPS.

Create a GeoJSON file for the boundary:

```json
{
  "type": "Polygon",
  "coordinates": [[
    [-74.006000, 40.712800],
    [-74.006000, 40.713800],
    [-74.008000, 40.713800],
    [-74.008000, 40.712800],
    [-74.006000, 40.712800]
  ]]
}
```

Save this as `north_field_boundary.json`

## Step 3: Add Field to Database

```bash
./run.sh create-field \
  --name "North Field" \
  --gps-source /dev/ttyUSB0
```

Then import the boundary:

```bash
python3 scripts/field_manager.py update \
  --field-id 1 \
  --boundary north_field_boundary.json \
  --crop-type corn \
  --soil-type silt_loam
```

Expected output:
```
✓ Field 1 updated
  Area: 25.87 acres
  Centroid: 40.713300, -74.007000
```

## Step 4: Verify Field

```bash
./run.sh list-fields
```

Expected output:
```
ID     Name                          Area (ac)    Crop           Soil            Created
----------------------------------------------------------------------------------------------------
1      North Field                    25.9         corn           silt_loam       2025-01-27 14:30:00
```

## Step 5: View Field Details

```bash
python3 scripts/field_manager.py get --field-id 1
```

Expected output:
```json
{
  "id": 1,
  "name": "North Field",
  "boundary_polygon": "{\"type\":\"Polygon\",\"coordinates\":[...]}",
  "area_acres": 25.87,
  "centroid_lat": 40.7133,
  "centroid_lon": -74.007,
  "crop_type": "corn",
  "soil_type": "silt_loam",
  "created_at": "2025-01-27 14:30:00",
  "updated_at": "2025-01-27 14:30:00"
}
```

## Common Issues

**GPS not connecting:**
- Check .env file for correct port
- Verify GPS device is powered on
- Try different USB port

**Area calculation incorrect:**
- Ensure GeoJSON coordinates are in WGS84
- Check that polygon is closed (first and last points match)
- Large fields may require more complex calculations

## Next Steps

- Set up guidance lines for the field
- Create prescription maps for variable rate application
- Monitor operations and collect data
