# VultIsig .vult File Format Analysis Summary

## File Structure Overview

The `.vult` files are **base64-encoded Protocol Buffer (protobuf) data** containing cryptographic vault information.

## Analysis Results

### File Sizes and Structure
- **TestDKLS1of2.vult**: 157,476 chars → 118,106 bytes (606 protobuf fields)
- **TestDKLS2of2.vult**: 157,496 chars → 118,122 bytes (605 protobuf fields)
- **Test-part1of2.vult**: 26,644 chars → 19,982 bytes (590 protobuf fields)  
- **Test-part2of2.vult**: 26,628 chars → 19,970 bytes (604 protobuf fields)

### Key Findings

1. **Format**: Base64-encoded protobuf binary data
2. **Content Type**: Cryptographic vault data with:
   - Vault names/descriptions
   - Public keys (hex-encoded)
   - Device identifiers
   - Timestamps
   - Large JSON structures containing cryptographic parameters

### Vault Information Extracted

#### DKLS Vaults (Distributed Key Lifecycle Signature)
- **Vault Name**: "Test Fast Vault DKLS"
- **Public Key**: `0333e3d4df9cc071be24fd6c995421036074a1a88e5d3e0bc211b7ef4330078d9b`
- **Additional Hash**: `20e368bf985efdc270500c6e9dc1159102323ff6eabab56f8fa9798e4ac0e2a9`
- Device info includes: "Server-062887", "Dorian's Mac mini-ABC"

#### Private Key Vaults (Multi-part)
- **Vault Name**: "Test private key vault" 
- **Public Key**: `0267db81657a956f364167c3986a426b448a74ac0db2092f6665c4c202b37f6f1d`
- **Additional Hash**: `c6da2ad7b18728f6481d747a7335fd52a5eed82f3c3d95a51deed03399c5c0b6`
- Devices: "iPhone-EC4", "Pixel 5a-a9b"
- Contains large JSON with "ecdsa_local_data" and "PaillierSK" cryptographic parameters

## Technical Details

### Protobuf Structure
- Files start with typical protobuf field tags (`08 01 12...`)
- Contains nested length-delimited fields
- Mixed data types: varints, length-delimited strings, 32-bit and 64-bit fields
- Large embedded base64 strings containing JSON cryptographic data

### Cryptographic Elements Identified
- **ECDSA public keys** (secp256k1 format)
- **Paillier cryptosystem** parameters (homomorphic encryption)
- **Device identifiers** and timestamps
- **Multi-party computation** (MPC) data structures
- **Distributed key generation** parameters

## File Naming Conventions
- `*DKLS*.vult` - Distributed Key Lifecycle Signature vaults
- `*part*.vult` - Multi-part private key vaults (split across devices)
- Numbered parts: `1of2`, `2of2` indicate vault splitting

## Tools Developed

Created `parse_vult_enhanced.py` CLI tool that:
- Decodes base64 content
- Analyzes protobuf structure  
- Extracts readable strings
- Provides hex dumps and field analysis
- Supports verbose mode for detailed inspection

## Next Steps

The `.vult` format is now well understood as protobuf-encoded cryptographic vault data. Further analysis could focus on:
1. Creating a proper protobuf schema definition
2. Building vault reconstruction tools
3. Implementing vault validation utilities
4. Developing vault merging/splitting tools for multi-part vaults
