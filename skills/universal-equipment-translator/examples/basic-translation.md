# Basic ISO 11783 Message Translation

This example demonstrates basic ISO 11783 message translation using the equipment translator.

## Scenario

You have a John Deere tractor (source) and a Case IH planter (target). You need to translate messages between them so the planter is recognized by the tractor.

## Prerequisites

- CAN interface configured (run `scripts/setup.sh`)
- Protocol database created (run `python3 scripts/setup-database.py`)
- John Deere tractor with JDLink protocol
- Case IH planter with ISOBUS support

## Setup

1. Configure CAN interface:
   ```bash
   cd scripts
   sudo ./setup.sh
   ```

2. Create protocol database:
   ```bash
   python3 scripts/setup-database.py
   ```

3. Configure .env file:
   ```bash
   cp .env.example .env
   nano .env
   ```

   Set:
   ```
   CAN_INTERFACE=can0
   CAN_BAUDRATE=250000
   TRANSLATION_MODE=iso11783
   SAFETY_OVERRIDE_DISABLED=true
   PROTOCOL_DB_PATH=/opt/equipment-translator/protocols.db
   ```

## Identify Equipment

Before translating, identify the ECUs on the bus:

```bash
python3 scripts/identify_ecu.py --interface can0 --timeout 10
```

Example output:
```
Identified: John Deere (JDLink) at SA 0x10
Identified: Case IH (AFS) at SA 0x20
```

## Single Message Translation

Test translation with a single message:

```bash
python3 scripts/translate.py \
  --message 0x18FF0001 \
  --data "DEADBEEF" \
  --source "John Deere" \
  --target "Universal"
```

Output:
```
Input:
  CAN ID: 0x18FF0001
  Data: deadbeef
  Source Protocol: John Deere
  Target Protocol: Universal

Translation Result:
  Original: 0x18FF0001 (PGN 0x00FF00)
  Translated: 0x18FF0001 (PGN 0x00FF00)
  Rule: identity
  Safety Critical: False
```

## Run Full Translation Service

Start the translation service:

```bash
cd scripts
sudo ./run.sh
```

The translator will:
- Listen to CAN traffic on `can0`
- Parse each message and identify manufacturer
- Translate manufacturer-specific messages to ISO 11783 standard
- Forward translated messages to CAN bus
- Log all translations to file

## Validate Messages

Validate a message before translation:

```bash
python3 scripts/validate.py \
  --message 0x18FF0001 \
  --data "DEADBEEF"
```

Output:
```
==============================================================
CAN Message Validation Report
==============================================================

CAN ID: 0x18FF0001
Data: deadbeef
Length: 4 bytes
Protocol: ISO 11783

Status: VALID

CAN ID Components:
  Type: extended
  Priority: 3
  PGN: 0x00FF00
  Source Address: 0x01

PGN Information:
  Name: Transport Protocol
  Description: Transport protocol for messages > 8 bytes

==============================================================
```

## Monitor CAN Traffic

Monitor CAN traffic to see translated messages:

```bash
# Terminal 1: Start translator
cd scripts
sudo ./run.sh

# Terminal 2: Monitor CAN bus
candump can0
```

Example output:
```
can0  18FF0001  [8]  DE AD BE EF 00 00 00 00
can0  18FF0002  [8]  01 02 03 04 05 06 07 08
```

## Troubleshooting

### No Communication

If no messages appear:

1. Check CAN interface is up:
   ```bash
   ip link show can0
   ```

2. Check CAN bus termination:
   ```bash
   # Should have 120 ohm resistors at both ends
   # Use multimeter to measure between CAN_H and CAN_L
   ```

3. Verify baud rate matches equipment:
   ```bash
   # Common agricultural baud rates: 250K or 500K
   # Set in .env: CAN_BAUDRATE=250000
   ```

### Translation Errors

If translations fail:

1. Check protocol database:
   ```bash
   sqlite3 /opt/equipment-translator/protocols.db "SELECT * FROM pgns LIMIT 5;"
   ```

2. Check logs:
   ```bash
   tail -f /var/log/equipment-translator.log
   ```

3. Enable debug logging in .env:
   ```
   TRANSLATION_LOG_LEVEL=debug
   ```

### Safety Messages Blocked

If safety-critical messages are not being translated:

This is expected behavior. Safety-critical PGNs should not be modified to ensure equipment safety.

To verify, check the log:
```bash
grep "safety-critical" /var/log/equipment-translator.log
```

## Advanced: Custom Translation Rules

For custom manufacturer protocols, add translation rules to the database:

```sql
-- Add new PGN
INSERT INTO pgns (pgn, name, description, manufacturer_id)
VALUES (0x0CFF00, 'Custom PGN', 'Manufacturer-specific PGN',
  (SELECT id FROM manufacturers WHERE name = 'John Deere'));

-- Add translation mapping
INSERT INTO message_mappings (source_pgn, source_manufacturer_id, target_pgn, target_manufacturer_id, translation_rule, safety_critical)
VALUES (0x0CFF00,
  (SELECT id FROM manufacturers WHERE name = 'John Deere'),
  0x0CFF00,
  (SELECT id FROM manufacturers WHERE name = 'Universal'),
  'identity',
  FALSE);
```

## Next Steps

- Test with actual equipment
- Monitor translation logs for errors
- Add custom protocol mappings as needed
- Review translation statistics

## References

- SKILL.md - Complete skill documentation
- references/manufacturer-protocols.md - Detailed manufacturer protocols
- references/iso11783-reference.md - ISO 11783 standard reference
