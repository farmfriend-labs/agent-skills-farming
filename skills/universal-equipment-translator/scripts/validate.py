#!/usr/bin/env python3

"""
validate.py
Validate CAN message against ISO 11783 standard and protocol specifications.
"""

import sys
import argparse
from typing import Dict, List, Optional
import json


def parse_can_id(can_id_str: str) -> int:
    """Parse CAN ID string to integer."""
    can_id_str = can_id_str.strip()

    if can_id_str.startswith("0x") or can_id_str.startswith("0X"):
        return int(can_id_str, 16)

    return int(can_id_str, 10)


def extract_can_components(can_id: int) -> Dict:
    """Extract CAN ID components."""
    if can_id > 0x7FF:
        # Extended ID (29-bit)
        priority = (can_id >> 26) & 0x07
        pgn = (can_id >> 8) & 0x03FFFF
        source_address = can_id & 0xFF
        return {
            "type": "extended",
            "priority": priority,
            "pgn": pgn,
            "pgn_hex": f"0x{pgn:06X}",
            "source_address": source_address,
            "source_address_hex": f"0x{source_address:02X}",
        }
    else:
        # Standard ID (11-bit)
        return {
            "type": "standard",
            "id": can_id,
            "id_hex": f"0x{can_id:03X}",
        }


def parse_can_data(data_str: str) -> bytes:
    """Parse CAN data string to bytes."""
    data_str = data_str.strip().replace(" ", "")

    if data_str.startswith("0x") or data_str.startswith("0X"):
        data_str = data_str[2:]

    return bytes.fromhex(data_str)


# ISO 11783 standard PGNs and their constraints
ISO_11783_PGNS = {
    0x00F804: {
        "name": "Address Claim",
        "data_length": 8,
        "description": "ECU claims its address on the bus",
        "safety_critical": False,
    },
    0x00FE00: {
        "name": "Request PGN",
        "data_length": 3,
        "description": "Request specific PGN from an ECU",
        "safety_critical": False,
    },
    0x00FF00: {
        "name": "Transport Protocol",
        "data_length": 8,
        "description": "Transport protocol for messages > 8 bytes",
        "safety_critical": False,
    },
    0x00FF84: {
        "name": "Transport Protocol Connection Management",
        "data_length": 8,
        "description": "TP.CM messages",
        "safety_critical": False,
    },
    0x01FF00: {
        "name": "VT to ECU",
        "data_length": 8,
        "description": "Virtual Terminal to ECU message",
        "safety_critical": False,
    },
    0x01FF84: {
        "name": "ECU to VT",
        "data_length": 8,
        "data_length": 8,
        "description": "ECU to Virtual Terminal message",
        "safety_critical": False,
    },
    0x00FEF8: {
        "name": "Proprietary A",
        "data_length": 8,
        "description": "Manufacturer-specific PGN",
        "safety_critical": False,
    },
    0x00FEFF: {
        "name": "Proprietary B",
        "data_length": 8,
        "description": "Manufacturer-specific PGN",
        "safety_critical": False,
    },
}

# Safety-critical message types (not to be modified)
SAFETY_CRITICAL_PGN_RANGES = [
    (0x00FE00, 0x00FEFF),  # Proprietary safety messages
]


def is_safety_critical(pgn: int) -> bool:
    """Check if PGN is safety-critical."""
    for start, end in SAFETY_CRITICAL_PGN_RANGES:
        if start <= pgn <= end:
            return True
    return False


def check_pgn_format(can_id: int) -> Dict:
    """Validate PGN format according to ISO 11783."""
    components = extract_can_components(can_id)

    if components['type'] != 'extended':
        return {
            "valid": False,
            "error": "Standard CAN IDs not supported - use extended IDs (29-bit)",
        }

    pgn = components['pgn']
    errors = []
    warnings = []

    # Check PGN is within valid range
    if pgn > 0x03FFFF:
        errors.append("PGN exceeds maximum value (0x03FFFF)")

    # Check source address
    sa = components['source_address']
    if sa == 0x00:
        warnings.append("Source address 0x00 is reserved")
    if sa == 0xFF:
        warnings.append("Source address 0xFF is global address")

    # Check if PGN is defined in ISO 11783
    if pgn in ISO_11783_PGNS:
        pgn_info = ISO_11783_PGNS[pgn]
        if 'data_length' in pgn_info:
            warnings.append(f"PGN {pgn_info['name']}: {pgn_info['description']}")
    else:
        # Check if in proprietary range
        if 0x00FEF8 <= pgn <= 0x00FEFF:
            warnings.append("Proprietary PGN - manufacturer-specific")
        else:
            warnings.append(f"Unknown PGN - may be manufacturer-specific")

    # Check safety-critical status
    if is_safety_critical(pgn):
        warnings.append("Safety-critical PGN - should not be modified in translation")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "pgn_info": ISO_11783_PGNS.get(pgn),
    }


def check_message_structure(can_id: int, data: bytes) -> Dict:
    """Validate message structure."""
    errors = []
    warnings = []

    # Check CAN ID format
    components = extract_can_id(can_id)

    if components['type'] == 'standard':
        errors.append("Standard CAN IDs not used in agricultural protocols")

    # Check data length
    if len(data) > 8:
        errors.append(f"Data length {len(data)} exceeds CAN max (8 bytes)")

    if len(data) == 0:
        warnings.append("Zero-length data frame")

    # Check PGN constraints
    pgn = components['pgn']
    if pgn in ISO_11783_PGNS:
        pgn_info = ISO_11783_PGNS[pgn]
        if 'data_length' in pgn_info:
            expected_length = pgn_info['data_length']
            if len(data) != expected_length:
                errors.append(f"Data length mismatch for PGN {pgn_info['name']}: "
                           f"expected {expected_length}, got {len(data)}")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
    }


def validate_message(can_id: int, data: bytes,
                   protocol_spec: Optional[str] = None) -> Dict:
    """Validate CAN message against ISO 11783."""
    results = {
        "can_id": can_id,
        "can_id_hex": f"0x{can_id:08X}",
        "data": data.hex(),
        "data_length": len(data),
        "protocol_spec": protocol_spec or "ISO 11783",
        "valid": True,
        "errors": [],
        "warnings": [],
    }

    # Extract CAN components
    try:
        components = extract_can_id(can_id)
    except Exception as e:
        results['valid'] = False
        results['errors'].append(f"Failed to parse CAN ID: {e}")
        return results

    results['components'] = components

    # Check PGN format
    pgn_result = check_pgn_format(can_id)
    results['pgn_validation'] = pgn_result
    results['errors'].extend(pgn_result['errors'])
    results['warnings'].extend(pgn_result['warnings'])

    # Check message structure
    structure_result = check_message_structure(can_id, data)
    results['structure_validation'] = structure_result
    results['errors'].extend(structure_result['errors'])
    results['warnings'].extend(structure_result['warnings'])

    # Final validity
    results['valid'] = len(results['errors']) == 0

    return results


def print_validation_report(results: Dict):
    """Print validation report."""
    print("=" * 60)
    print("CAN Message Validation Report")
    print("=" * 60)
    print()
    print(f"CAN ID: {results['can_id_hex']}")
    print(f"Data: {results['data']}")
    print(f"Length: {results['data_length']} bytes")
    print(f"Protocol: {results['protocol_spec']}")
    print()

    if results['valid']:
        print("Status: VALID")
    else:
        print("Status: INVALID")

    print()

    # Print components
    if 'components' in results:
        print("CAN ID Components:")
        c = results['components']
        print(f"  Type: {c['type']}")
        if c['type'] == 'extended':
            print(f"  Priority: {c['priority']}")
            print(f"  PGN: {c['pgn_hex']}")
            print(f"  Source Address: {c['source_address_hex']}")
        print()

    # Print errors
    if results['errors']:
        print("ERRORS:")
        for i, error in enumerate(results['errors'], 1):
            print(f"  {i}. {error}")
        print()

    # Print warnings
    if results['warnings']:
        print("WARNINGS:")
        for i, warning in enumerate(results['warnings'], 1):
            print(f"  {i}. {warning}")
        print()

    # Print PGN info
    if 'pgn_validation' in results:
        pgn_info = results['pgn_validation'].get('pgn_info')
        if pgn_info:
            print("PGN Information:")
            print(f"  Name: {pgn_info['name']}")
            print(f"  Description: {pgn_info['description']}")
            if pgn_info.get('safety_critical'):
                print(f"  Safety Critical: YES")
            print()

    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="Validate CAN message against ISO 11783")

    parser.add_argument("--message", "-m", required=True,
                        help="CAN ID in hex (e.g., 0x18FF0001)")
    parser.add_argument("--data", "-d", default="",
                        help="CAN data in hex (e.g., DEADBEEF)")
    parser.add_argument("--protocol-spec", "-p",
                        help="Protocol specification (default: ISO 11783)")
    parser.add_argument("--json", "-j", action="store_true",
                        help="Output in JSON format")

    args = parser.parse_args()

    # Parse message
    can_id = parse_can_id(args.message)
    data = parse_can_data(args.data)

    # Validate
    results = validate_message(can_id, data, args.protocol_spec)

    # Print report
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print_validation_report(results)

    # Exit code
    sys.exit(0 if results['valid'] else 1)


if __name__ == "__main__":
    main()
