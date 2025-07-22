#!/usr/bin/env python3
"""
Vultitool - A CLI parser for .vult files

This script parses and displays the contents of .vult files from the Vultisig ecosystem.
Supports base64 decoding and basic protocol buffer inspection.
"""

import sys
import base64
import argparse
from pathlib import Path


def analyze_protobuf_structure(data):
    """Basic analysis of protobuf structure without full parsing."""
    analysis = {
        'total_bytes': len(data),
        'fields_found': [],
        'probable_strings': [],
        'first_bytes_hex': data[:50].hex() if len(data) >= 50 else data.hex()
    }
    
    # Simple field detection - look for protobuf field tags
    i = 0
    while i < min(len(data), 1000):  # Analyze first 1KB only
        if i + 1 < len(data):
            # Basic protobuf wire type detection
            byte_val = data[i]
            if byte_val & 0x07 in [0, 1, 2, 5]:  # Valid wire types
                field_num = byte_val >> 3
                wire_type = byte_val & 0x07
                if field_num > 0 and field_num < 100:  # Reasonable field numbers
                    analysis['fields_found'].append({
                        'field_number': field_num,
                        'wire_type': wire_type,
                        'offset': i
                    })
        i += 1
    
    # Look for potential string content (printable ASCII sequences)
    current_string = ""
    for i, byte_val in enumerate(data[:1000]):
        if 32 <= byte_val <= 126:  # Printable ASCII range
            current_string += chr(byte_val)
        else:
            if len(current_string) > 4:  # Strings of 4+ chars might be meaningful
                analysis['probable_strings'].append(current_string)
            current_string = ""
    
    if len(current_string) > 4:
        analysis['probable_strings'].append(current_string)
    
    return analysis


def parse_vult_file(file_path, verbose=False):
    """Parse a .vult file and return its contents."""
    try:
        with open(file_path, 'r') as f:
            content = f.read().strip()
        
        print(f"File: {file_path}")
        print(f"Raw content length: {len(content)} characters")
        
        # Try to decode as base64
        try:
            decoded_data = base64.b64decode(content)
            print(f"Base64 decoded length: {len(decoded_data)} bytes")
            
            # Analyze the binary structure
            print("\n=== Binary Analysis ===")
            if len(decoded_data) >= 2:
                first_bytes = decoded_data[:10]
                print(f"First 10 bytes (hex): {first_bytes.hex()}")
                print(f"First 10 bytes (decimal): {[b for b in first_bytes]}")
                
                # Check if this looks like protobuf
                if decoded_data[0] in [0x08, 0x0A, 0x10, 0x12, 0x18, 0x1A, 0x20, 0x22]:
                    print("✓ Data appears to be Protocol Buffer format")
                    
                    # Basic protobuf analysis
                    analysis = analyze_protobuf_structure(decoded_data)
                    print(f"\n=== Protocol Buffer Analysis ===")
                    print(f"Total bytes: {analysis['total_bytes']}")
                    print(f"Fields detected: {len(analysis['fields_found'])}")
                    
                    if verbose and analysis['fields_found']:
                        print("\nField details (first 10):")
                        for field in analysis['fields_found'][:10]:
                            wire_types = {0: 'varint', 1: '64-bit', 2: 'length-delimited', 5: '32-bit'}
                            wire_desc = wire_types.get(field['wire_type'], f"unknown({field['wire_type']})")
                            print(f"  Field {field['field_number']}: {wire_desc} at offset {field['offset']}")
                    
                    if analysis['probable_strings']:
                        print(f"\nProbable text strings found: {len(analysis['probable_strings'])}")
                        for i, s in enumerate(analysis['probable_strings'][:5]):
                            print(f"  {i+1}: '{s}'")
                        if len(analysis['probable_strings']) > 5:
                            print(f"  ... and {len(analysis['probable_strings']) - 5} more")
                else:
                    print("? Data format unknown - not standard protobuf")
                    
                if verbose:
                    print(f"\nFirst 200 bytes (hex):\n{decoded_data[:200].hex()}")
            else:
                print("Error: Decoded data is too short")
                
        except Exception as e:
            print(f"Base64 decoding failed: {e}")
            print(f"Raw content (first 200 chars): {content[:200]}")
            
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
        return False
    except Exception as e:
        print(f"Error reading file: {e}")
        return False
    
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Parse and display .vult file contents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python parse_vult_enhanced.py testDKLS-2of2.vult
  python parse_vult_enhanced.py --verbose testGG20-part1of2.vult
        """
    )
    
    parser.add_argument('file', help='Path to the .vult file to parse')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Enable verbose output with detailed binary analysis')
    
    args = parser.parse_args()
    
    # Validate file exists and has .vult extension
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Error: File '{file_path}' does not exist")
        sys.exit(1)
    
    if file_path.suffix.lower() != '.vult':
        print(f"Warning: File '{file_path}' does not have .vult extension")
    
    success = parse_vult_file(file_path, verbose=args.verbose)
    
    if not success:
        sys.exit(1)


if __name__ == '__main__':
    main()
