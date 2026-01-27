# ISO 11783 / ISOBUS Standard Reference

## Overview

ISO 11783 (commonly called ISOBUS) is the international standard for agricultural electronics. It standardizes communication between tractors, implements, and other agricultural equipment.

## Key Components

### 1. Virtual Terminal (VT)
- Operator interface display
- Standardized buttons and controls
- Implements connect to any VT-compliant display
- Eliminates need for brand-specific displays

### 2. Task Controller (TC)
- Controls implement operations
- Prescription-based operation
- As-applied data logging
- Section control

### 3. Auxiliary Control (AUX)
- Additional functions
- Custom controls
- Non-standard implement features

### 4. Basic Tractor ECU (BTE)
- Tractor control interface
- Speed, PTO, hitch control
- Implements can request tractor functions

### 5. Implement ECU (IE)
- Implement control unit
- Implements connect to tractor via ISOBUS
- Universal compatibility

## CAN Bus Layers

### Physical Layer
- CAN High / CAN Low wires
- Twisted pair, 120 ohm termination
- 250 Kbps or 500 Kbps baud rate

### Data Link Layer
- CAN 2.0B (29-bit identifiers)
- Standard and extended frames
- Error detection and handling

### Network Layer
- Address claim process
- Priority-based arbitration
- Source and destination addressing

## Common PGNs (Parameter Group Numbers)

### Addressing and Management
- 0x00F804: Address Claim
- 0x00FE00: Request PGN
- 0x00FF00: Transport Protocol
- 0x00FF84: Transport Protocol Connection Management

### Virtual Terminal
- 0x01FF00: VT to ECU
- 0x01FF84: ECU to VT

### Task Controller
- 0x00CF004: TC Process Data
- 0x00CF005: TC Device Descriptor

### Implement Control
- 0x00EFE00: Implement Control
- 0x00EFE01: Implement Status

## CAN Identifier Format (29-bit)

```
Bits 28-26: Priority (0-7, lower is higher priority)
Bits 25-8:  Parameter Group Number (PGN)
Bits 7-0:   Source Address (SA)
```

## Example Messages

### Address Claim
```
CAN ID: 0x18EEFFF1
Data: 03 01 00 01 00 00 00 00
```

### VT Message
```
CAN ID: 0x18FF0002
Data: [VT message data]
```

## Implementation Tips

1. **Always terminate the bus** - 120 ohm resistors at both ends
2. **Check baud rate** - 250K or 500K, must match all devices
3. **Verify ground connections** - Common ground essential
4. **Test with known equipment** - Validate with ISOBUS-certified implements

## Manufacturer ISOBUS Compliance

- **John Deere**: Good compliance, some proprietary extensions
- **Case IH**: Excellent compliance, universal terminal support
- **AGCO**: Good compliance, Fuse integration
- **Kubota**: Growing ISOBUS support

## Resources

- ISO 11783 Standard (11 parts)
- AEF (Agricultural Electronics Foundation) certification
- Manufacturer ISOBUS implementation guides
- Open-source ISOBUS libraries

## Testing

Use ISOBUS test tools:
- CANoe with ISOBUS license
- ISOBUS diagnostic tools
- Manufacturer test implements
- Open-source ISOBUS simulators
