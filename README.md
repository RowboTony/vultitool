# vultitool

**Vultisig CLI  Ecosystem Test Suite**

A command-line tool for parsing, analyzing, and validating Vultisig `.vult` vault files. Built as a reference implementation to understand and document the Vultisig MPC wallet ecosystem.

## Quick Start

```bash
# Make vultitool executable
chmod +x ./vultitool

# Parse and display a vault file
./vultitool vault parse MyVault.vult

# Brief summary
./vultitool vault parse MyVault.vult --summary

# JSON output for automation
./vultitool vault parse MyVault.vult --json

# Validate vault format
./vultitool vault validate MyVault.vult

# Export vault metadata
./vultitool vault export MyVault.vult output.json
```

## What is Vultisig?

Vultisig is a **seedless crypto wallet** that uses Multi-Party Computation (MPC) with Threshold Signature Schemes (TSS) for transaction signing. Instead of traditional seed phrases, Vultisig uses distributed "vault parts" stored in `.vult` files.

**Key Features:**
- **No seed phrases** - Uses distributed key shares instead
- **MPC-based signing** - Supports both GG20 and DKLS protocols
- **Multi-device support** - Hot (2-of-2) and Secure (2-of-3) vaults
- **Cross-platform** - iOS, Android, Windows, Web

## Command Reference

### `vultitool vault parse <file>`

Parse and display vault contents with human-readable output.

**Options:**
- `--summary` - Brief overview only
- `--json` - Machine-readable JSON output
- `--verbose` - Show additional technical details

**Example Output:**
```
=== Vault Analysis: Test-part1of2.vult ===
File Size: 26644 chars → 19982 bytes
Container Version: 1
Encrypted: No

📁 Vault Name: 'Test private key vault'
🔐 Crypto Type: GG20
🔑 ECDSA Public Key: 0267db81657a956f364167c3986a426b448a74ac0db2092f6665c4c202b37f6f1d
🔑 EdDSA Public Key: c6da2ad7b18728f6481d747a7335fd52a5eed82f3c3d95a51deed03399c5c0b6
🆔 Local Party ID: Pixel 5a-a9b
📅 Created: 2024-10-19T07:22:50

👥 Signers (2):
  1. Pixel 5a-a9b
  2. iPhone-EC4

🗝️  Key Shares (2):
  Share 1: Public Key: 0267db81... (12953 chars)
  Share 2: Public Key: c6da2ad7... (1611 chars)
```

### `vultitool vault inspect <file>`

Detailed technical inspection of vault structure.

**Options:**
- `--show-keyshares` - Display sensitive key share data ⚠️

### `vultitool vault validate <file>`

Validate vault file format and structure.

**Options:**
- `--strict` - Enable strict validation rules

**Output:**
```
✅ Vault validation passed
```

### `vultitool vault export <file> <output>`

Export vault metadata to structured format.

**Options:**
- `--format json|yaml` - Output format (default: json)

## Supported Vault Types

| Type | Description | Protocol | Typical Use |
|------|-------------|----------|-------------|
| **GG20** | Traditional MPC protocol | ECDSA/EdDSA | General purpose |
| **DKLS** | Modern MPC protocol | ECDSA/EdDSA | Enhanced security |
| **Fast Vault** | 2-of-2 threshold | Hot signing | Daily transactions |
| **Secure Vault** | 2-of-3 threshold | Cold storage | Long-term holding |

## Understanding .vult Files

`.vult` files are **base64-encoded Protocol Buffer data** containing:

1. **VaultContainer** (outer wrapper)
   - Version info
   - Encryption status
   - Inner vault data

2. **Vault** (core data)
   - Vault name and metadata
   - Public keys (ECDSA/EdDSA)
   - Signer identities
   - Distributed key shares
   - Creation timestamp

## Installation & Setup

**Requirements:**
- Python 3.7+
- Generated protobuf bindings (from Vultisig commondata)

**Setup:**
```bash
# Clone the repository
git clone <repository-url>
cd vultitool

# Generate protobuf bindings (if needed)
# See: https://github.com/vultisig/commondata

# Make executable
chmod +x ./vultitool

# Test with sample vault
./vultitool vault parse --summary sample.vult
```

## Project Goals

This tool is part of a broader effort to:

1. **Document** the Vultisig ecosystem comprehensively
2. **Enable** better developer onboarding and testing
3. **Build** reference implementations for key workflows
4. **Establish** technical foundation for tooling and automation

## Security Notes

⚠️ **Key Share Data**: The `--show-keyshares` flag displays sensitive cryptographic material. Use only in secure environments.

⚠️ **File Handling**: `.vult` files contain cryptographic keys. Handle with appropriate security practices.

## Contributing

This project prioritizes:
- **Clarity** over complexity
- **Documentation** of all findings
- **Reproducible** results and methods
- **Cross-platform** compatibility

## License

Licensed under the Apache License, Version 2.0.

---

**Built with:** Python, Protocol Buffers, Vultisig commondata schema

**Status:** Active development - MVP parser complete, expanding functionality

For detailed technical documentation, see [spec.md](spec.md).
