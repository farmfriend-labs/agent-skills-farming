# Universal Equipment Translator

Enables mixed-fleet equipment interoperability by translating between proprietary agricultural equipment protocols.

## Purpose

Break down vendor lock-in by translating between equipment manufacturers' proprietary communication protocols, allowing any tractor to work with any implement regardless of brand. Eliminates forced equipment purchases based on software compatibility rather than need.

## Problem Solved

Farmers are forced to buy equipment from a single manufacturer because their tractors won't recognize implements from other brands. This artificial software restriction costs farmers $50K-$200K in unnecessary equipment purchases and limits their ability to choose the best tool for each job.

## Capabilities

- Translates between ISO 11783/ISOBUS standard protocols
- Interprets CAN bus messages from major manufacturers
- Converts manufacturer-specific data formats
- Creates compatibility layers for mixed-brand fleets
- Bypasses artificial software interoperability restrictions
- Maintains safety-critical functions
- Supports bidirectional communication
- Works offline with cached protocol definitions

## Instructions

### Usage by AI Agent

1. **Identify Equipment Brands**
   - Determine tractor brand and model
   - Determine implement brand and model
   - Check supported protocols for each

2. **Select Translation Profile**
   - Load ISO 11783/ISOBUS base definitions
   - Apply manufacturer-specific extensions
   - Use references/manufacturer-protocols.md for specific mappings

3. **Configure Communication Layer**
   - Set up CAN bus interface
   - Configure baud rate and message IDs
   - Load protocol translation rules
   - Test basic communication before operation

4. **Monitor Operation**
   - Translate messages in real-time
   - Log protocol errors for troubleshooting
   - Maintain safety-critical signal integrity
   - Track successful/failed message translations

5. **Fallback Handling**
   - If translation fails, revert to safe mode
   - Alert operator of compatibility issues
   - Log failures for protocol database improvement

### Safety Considerations

- Never override safety-critical functions
- Maintain ISO 11783 compliance for safety messages
- Do not modify emergency stop or shutdown sequences
- Preserve manufacturer-recommended operating parameters
- Test in controlled environment before field use
- Always allow manual override

## Tools

- **Python 3.8+** for protocol parsing and translation
- **CAN interface hardware** (SocketCAN, Vector, PEAK, etc.)
- **CAN utils** (candump, cansend from can-utils)
- **Serial communication** for ISOBUS (ISO 11783)
- **SQLite** for protocol database caching
- **Log monitoring** (journalctl, syslog)

## Environment Variables

```bash
# CAN Interface Configuration
CAN_INTERFACE=can0
CAN_BAUDRATE=250000

# Translation Settings
TRANSLATION_MODE=iso11783  # iso11783 | raw | hybrid
SAFETY_OVERRIDE_DISABLED=true

# Logging
TRANSLATION_LOG_LEVEL=info
TRANSLATION_LOG_FILE=/var/log/equipment-translator.log

# Protocol Database
PROTOCOL_DB_PATH=/opt/equipment-translator/protocols.db
OFFLINE_MODE=true
```

## Manufacturer Protocols

### John Deere

**Protocol:** JDLink / ISO 11783 with proprietary extensions

**CAN IDs:** 0x18FFxxxx series for control messages

**Key Characteristics:**
- Uses CANopen profile for implement control
- Proprietary diagnostic codes
- GPS and guidance integration
- AutoTrac compatibility layer

**Compatibility Notes:**
- Supports ISO 11783 PGNs (Parameter Group Numbers)
- Requires JD-specific handshake for implements
- Works with third-party implements via universal terminal

### Case IH

**Protocol:** AFS (Advanced Farming Systems) / ISO 11783

**CAN IDs:** 0x0CFExxxx series for standard ISOBUS

**Key Characteristics:**
- AFS Pro terminal interface
- ISOBUS virtual terminal support
- ACCU GUIDE integration
- Proprietary section control

**Compatibility Notes:**
- Excellent ISO 11783 support
- Works with most ISOBUS-compliant implements
- Less proprietary than John Deere

### AGCO

**Protocol:** AGCOMMAND / ISO 11783

**CAN IDs:** Mixed ISOBUS and proprietary ranges

**Key Characteristics:**
- C1000 terminal support
- ISO 11783 VT implementation
- AgroMap compatibility
- Fuse integration

**Compatibility Notes:**
- Good ISOBUS compliance
- Variable rate application via ISO 11783
- Task controller support

### ISOBUS (ISO 11783) Standard

**Standard:** ISO 11783 (International Standard for Agricultural and Forestry)

**Key Components:**
- Virtual Terminal (VT) - Operator interface
- Task Controller (TC) - Operation control
- Auxiliary Control (AUX) - Additional functions
- Basic Tractor ECU (BTE) - Tractor control
- Implement ECU (IE) - Implement control

**Common PGNs (Parameter Group Numbers):**
- 0x00F804: Address Claim
- 0x00FE00: Request PGN
- 0x00FF00: Transport Protocol
- 0x00FF84: Transport Protocol Connection Management
- 0x01FF00: Virtual Terminal to ECU
- 0x01FF84: ECU to Virtual Terminal

**Message Structure:**
- 29-bit CAN identifier
- Priority (3 bits)
- PGN (18 bits)
- Source Address (8 bits)

## CAN Bus Fundamentals

### Message Types

**Data Frame:**
- Standard 11-bit identifier (CAN 2.0A)
- Extended 29-bit identifier (CAN 2.0B) - Used in agriculture

**CAN Extended ID Format (29-bit):**
```
Bits 28-26: Priority (0-7, lower is higher priority)
Bits 25-8:  Parameter Group Number (PGN)
Bits 7-0:   Source Address (SA)
```

### Agricultural CAN Layers

1. **Physical Layer:** CAN High/Low wiring, 250K or 500K baud
2. **Data Link Layer:** CAN 2.0B with extended IDs
3. **Network Layer:** ISO 11783 PGN addressing
4. **Application Layer:** J1939/ISO 11783 messages
5. **Session Layer:** ISO 11783 transport protocol
6. **Presentation Layer:** Data conversion
7. **Application Layer:** Control, monitoring, task control

## Translation Strategy

### ISO 11783 to Manufacturer-Specific

1. **Parse incoming message**
   - Extract CAN ID (29-bit)
   - Decode priority, PGN, source address
   - Parse data payload

2. **Identify manufacturer**
   - Check source address in PGN database
   - Look up manufacturer protocol profile
   - Load translation rules

3. **Convert to standard format**
   - Extract meaningful values (speed, depth, rate)
   - Map manufacturer-specific IDs to ISO PGNs
   - Preserve units and data types

4. **Translate to target protocol**
   - Apply target manufacturer format rules
   - Reconstruct CAN ID with target parameters
   - Validate message structure

5. **Forward to destination**
   - Send translated message to CAN bus
   - Log translation for debugging
   - Handle translation errors gracefully

### Manufacturer to ISO 11783

Reverse of above process. Translate proprietary messages to ISO 11783 standard for universal compatibility.

## Legal Considerations

### DMCA Exemptions

**Section 1201 Circumvention Exemption (2018-2022):**

Authorized circumvention allowed for:
- Diagnosis, repair, or maintenance of lawfully acquired devices
- Tractors, agricultural vehicles, and implements
- Interoperability with independently created software

**Requirements:**
- Device must be lawfully owned
- Circumvention must be for repair/maintenance
- No violation of copyright
- No creation of infringing derivatives

### Warranty Considerations

- Translation layer does not modify ECU firmware
- OEM warranty may still apply to hardware
- Document all modifications for compliance
- Check local laws regarding equipment modification

### Liability

- Operator assumes responsibility for translated operation
- Maintain original manufacturer safety systems
- Do not override safety-critical functions
- Document testing procedures and results

## Examples

See examples/ directory for:
- Basic ISO 11783 message translation
- John Deere to ISOBUS translation
- CAN bus setup and configuration
- Error handling and recovery

## References

### Standards

- **ISO 11783:** International standard for agricultural bus systems
  - Part 1: General standard and definitions
  - Part 2: Physical layer
  - Part 3: Data link layer
  - Part 4: Network layer
  - Part 5: Network management
  - Part 6: Virtual terminal
  - Part 7: Implement messages application layer
  - Part 9: Tractor ECU applications
  - Part 10: Task controller and management

- **SAE J1939:** CAN protocol for heavy vehicles
  - Foundation for ISO 11783

### Manufacturer Documentation

See references/manufacturer-protocols.md for:
- John Deere CAN bus specifications
- Case IH AFS protocol details
- AGCO AGCOMMAND specifications
- ISO 11783 implementation guides

### Research and Standards

- ISO 11783 Working Group documentation
- Agricultural Electronics Standards (AESA)
- OpenAg consortium interoperability papers
- SAE International technical papers

## Troubleshooting

### Common Issues

**No communication between tractor and implement:**
- Check CAN bus termination (120 ohm resistors)
- Verify baud rate matches (250K vs 500K)
- Check ground connections
- Verify power to implement ECU
- Test with known-good equipment

**Translation errors:**
- Check protocol database version
- Verify manufacturer protocol profile loaded
- Update translation rules if PGNs changed
- Check CAN bus for error frames

**Inconsistent behavior:**
- Log CAN traffic for analysis
- Check for duplicate source addresses
- Verify priority settings
- Test with different translation modes

**Safety systems triggering:**
- Verify safety-critical PGNs not modified
- Check for message reordering
- Verify CAN bus error handling
- Test with manufacturer diagnostic tools

## Testing

1. **Unit Testing**
   - Test message parsing and translation
   - Verify CAN ID construction
   - Validate data type conversions

2. **Integration Testing**
   - Connect compatible equipment first
   - Test known-good translations
   - Verify bidirectional communication

3. **Field Testing**
   - Test in controlled environment
   - Monitor CAN traffic and errors
   - Verify equipment operates correctly
   - Document any issues

## Version History

- **1.0.0** - Initial release with ISO 11783 and major manufacturer support

## License

MIT License - Open source, free to use, modify, and distribute.

## Support

For issues, questions, or contributions:
- GitHub Issues: https://github.com/farmfriend-labs/agent-skills-farming/issues
- Email: farmfriend.labs@gmail.com
