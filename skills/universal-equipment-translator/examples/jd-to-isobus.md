# John Deere to ISOBUS Translation

This example demonstrates translating John Deere proprietary messages to ISO 11783 ISOBUS standard.

## Background

John Deere equipment uses JDLink protocol, which is an extension of ISO 11783 with proprietary PGNs and data formats. For interoperability with other brands, these messages must be translated to ISO 11783 standard.

## John Deere Protocol Characteristics

### CAN ID Format

John Deere uses extended 29-bit CAN IDs with specific PGN ranges:

| PGN Range | Description |
|-----------|-------------|
| 0x0CFExxxx | JDLink proprietary messages |
| 0x18FFxxxx | ISOBUS-compatible messages |
| 0x00FExxxx | Proprietary diagnostic messages |

### Source Address Ranges

John Deere equipment typically uses:
- 0x10-0x1F: Tractors
- 0x20-0x2F: Implements
- 0x30-0x3F: Displays/terminals

### Common John Deere PGNs

| PGN (Hex) | Name | Description |
|------------|------|-------------|
| 0x0CFE0010 | Tractor ECU | Tractor control unit |
| 0x0CFE0020 | Implement ECU | Implement control unit |
| 0x0CFE0030 | AutoTrac | GPS guidance system |
| 0x18FF0001 | VT to ECU | Virtual terminal messages |

## Translation Example

### Scenario

John Deere 8R tractor sending control messages to Case IH 2000 planter.

**Original John Deere Message:**
```
CAN ID: 0x0CFE0010
Data: 01 02 03 04 05 06 07 08
```

**Extracted Components:**
- Priority: 3
- PGN: 0x00FE00
- Source Address: 0x10

**Translated to ISO 11783:**
```
CAN ID: 0x0CFE0010
Data: 01 02 03 04 05 06 07 08
```

In this case, the PGN 0x00FE00 (Proprietary A) may need mapping to ISO 11783 equivalent or pass-through if no standard equivalent exists.

## Implementation

### Step 1: Add John Deere PGN to Database

```sql
-- Add John Deere proprietary PGN
INSERT INTO pgns (pgn, name, description, manufacturer_id)
VALUES (
  0x0CFE0010,
  'Tractor ECU',
  'John Deere tractor control unit messages',
  (SELECT id FROM manufacturers WHERE name = 'John Deere')
);
```

### Step 2: Create Translation Rule

```sql
-- Map to ISO 11783 equivalent or pass-through
INSERT INTO message_mappings (source_pgn, source_manufacturer_id, target_pgn, target_manufacturer_id, translation_rule, safety_critical)
VALUES (
  0x0CFE0010,
  (SELECT id FROM manufacturers WHERE name = 'John Deere'),
  0x0CFE0010,
  (SELECT id FROM manufacturers WHERE name = 'Universal'),
  'identity',
  FALSE
);
```

### Step 3: Test Translation

```bash
python3 scripts/translate.py \
  --message 0x0CFE0010 \
  --data "0102030405060708" \
  --source "John Deere" \
  --target "Universal"
```

## Common Translation Scenarios

### 1. AutoTrac Guidance

**John Deere:** Proprietary AutoTrac PGN (0x0CFE0030)

**Translation:**
- If compatible ISOBUS guidance PGN exists (0x0CFFxxxx), map to that
- Otherwise, pass-through as proprietary

```bash
# Test AutoTrac translation
python3 scripts/translate.py \
  --message 0x0CFE0030 \
  --data "GUIDANCE_DATA_HERE" \
  --source "John Deere" \
  --target "Universal"
```

### 2. Section Control

**John Deere:** Proprietary section control messages

**Translation:**
- Map to ISOBUS Task Controller (TC) messages if available
- Maintain section states (on/off) across translation

```bash
# Test section control translation
python3 scripts/translate.py \
  --message "SECTION_CONTROL_PGN" \
  --data "SECTION_STATES" \
  --source "John Deere" \
  --target "Universal"
```

### 3. Implement Control

**John Deere:** Proprietary implement control

**Translation:**
- Map to ISOBUS Auxiliary Control (AUX) messages
- Translate control commands to standard format

```bash
# Test implement control translation
python3 scripts/translate.py \
  --message "IMPLEMENT_CONTROL_PGN" \
  --data "CONTROL_DATA" \
  --source "John Deere" \
  --target "Universal"
```

## Advanced: Data Field Mapping

For more complex translations requiring data field remapping:

### Step 1: Define Data Fields

```sql
-- Add data fields for John Deere PGN
INSERT INTO data_fields (pgn_id, field_name, byte_offset, bit_offset, bit_length, data_type, units, scale, offset, description)
VALUES (
  (SELECT id FROM pgns WHERE pgn = 0x0CFE0010),
  'speed',
  0,
  0,
  16,
  'uint16',
  'km/h',
  0.01,
  0,
  'Tractor forward speed'
);

INSERT INTO data_fields (pgn_id, field_name, byte_offset, bit_offset, bit_length, data_type, units, scale, offset, description)
VALUES (
  (SELECT id FROM pgns WHERE pgn = 0x0CFE0010),
  'pto_rpm',
  2,
  0,
  16,
  'uint16',
  'rpm',
  1.0,
  0,
  'PTO revolutions per minute'
);
```

### Step 2: Create Complex Translation Rule

This requires custom translation logic in the translation engine. For now, use identity mapping for basic PGN translation.

## Limitations

1. **Proprietary PGNs**: Some John Deere PGNs have no ISO 11783 equivalent and must pass through as proprietary
2. **Data Structure**: Different data structures may require field-level mapping
3. **Authentication**: Some John Deere features require JDLink authentication (not supported by translation layer)
4. **Encrypted Messages**: Encrypted JDLink messages cannot be translated

## Troubleshooting

### Messages Not Translating

1. Check if PGN is in database:
   ```sql
   SELECT * FROM pgns WHERE pgn = 0x0CFE0010;
   ```

2. Check if translation rule exists:
   ```sql
   SELECT * FROM message_mappings
   WHERE source_pgn = 0x0CFE0010
   AND source_manufacturer_id = (SELECT id FROM manufacturers WHERE name = 'John Deere');
   ```

3. Check logs for errors:
   ```bash
   tail -f /var/log/equipment-translator.log
   ```

### Safety Messages Blocked

If safety-critical messages are not being translated, verify the setting in .env:

```
# Check this is set to true
SAFETY_OVERRIDE_DISABLED=true
```

### Incompatible Implement

If implement still not recognized after translation:

1. Verify ISOBUS support on implement
2. Check for manufacturer-specific handshake requirements
3. Consult implement manual for protocol requirements

## Testing with Real Equipment

### Test Setup

1. Connect John Deere tractor to CAN bus
2. Connect Case IH implement to same bus
3. Start translation service:
   ```bash
   cd scripts
   sudo ./run.sh
   ```

4. Monitor CAN traffic:
   ```bash
   candump can0
   ```

### Expected Behavior

- John Deere messages received on CAN bus
- Messages parsed and manufacturer identified
- Translation applied (identity or ISO 11783 mapping)
- Translated messages sent to CAN bus
- Case IH implement receives translated messages

### Verify Implementation Recognition

Check if Case IH implement is recognized by John Deere terminal:

1. Power on implement
2. Power on tractor
3. Check tractor display for implement detection
4. If not detected, check CAN traffic and translation logs

## References

- John Deere CAN Bus Specification (proprietary, requires dealer access)
- ISO 11783 Standard Parts 1-11
- SAE J1939 Standard (CAN protocol foundation)
- J1939-71 (Application Layer for Agricultural Equipment)

## Further Reading

- examples/basic-translation.md - Basic translation workflow
- references/manufacturer-protocols.md - Detailed protocol information
- SKILL.md - Complete skill documentation
