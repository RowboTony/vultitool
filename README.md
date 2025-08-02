> **⚠️ ARCHIVED: This project is no longer maintained. Please use [`vultool`](https://github.com/RowboTony/vultool) instead.**

---

# vultitool-poc-py (ARCHIVED, NO LONGER MAINTAINED)

> **⚠️ This repository is a proof-of-concept and is no longer maintained.  
> Development has moved to the next-generation CLI tool: [`vultool`](https://github.com/RowboTony/vultool).  
> Please use [vultool](https://github.com/RowboTony/vultool) for all current and future Vultisig CLI workflows.  
> This repo remains for historical reference only.**

---

## Legacy Project Description

A command-line tool for parsing, analyzing, and validating Vultisig `.vult` vault files.  
**Note:** This proof-of-concept Python codebase (`vultitool-poc-py`) has been superseded by [`vultool`](https://github.com/RowboTony/vultool), which is actively developed and production-focused.

---

## Why Was This Project Archived?

- This repo was an early R&D effort to understand `.vult` files and document the Vultisig ecosystem.
- All lessons learned, design improvements, and new features are now in [`vultool`](https://github.com/RowboTony/vultool).
- `vultool` is faster, more robust, has better test coverage, and follows modern CLI conventions.

---

## Where To Go Now

- **For all active development and usage:**  
  → [https://github.com/RowboTony/vultool](https://github.com/RowboTony/vultool)
- **For historical reference or Python PoC:**  
  → Feel free to browse this repo, but note it will not receive updates or bugfixes.

---

Thank you for supporting open-source research and tool development for the Vultisig ecosystem!

---
---

# README.md (archived)

---

**Vultisig CLI Ecosystem Tool Suite**

A command-line tool for parsing, analyzing, and validating Vultisig `.vult` vault files. Built as a reference implementation to understand and document the Vultisig MPC wallet ecosystem.

## Official Vultisig Integration

**`vultitool` uses the canonical Vultisig sources for maximum compatibility and accuracy:**

- **Protobuf Schemas**: Direct integration with [github.com/vultisig/commondata](https://github.com/vultisig/commondata) - the official protobuf definitions used by all Vultisig applications
- **Cryptographic Libraries**: Aligned with [github.com/vultisig/mobile-tss-lib](https://github.com/vultisig/mobile-tss-lib) for decryption and vault handling
- **Version Parity**: Matches dependency versions from [github.com/vultisig/vultisig-go](https://github.com/vultisig/vultisig-go) for protocol compatibility
- **No Local Copies**: All protobuf definitions are sourced directly from official Vultisig repositories via Go modules

**This ensures 100% compatibility with official Vultisig applications** and serves as the definitive technical reference for the Vultisig ecosystem.

## Installation & Setup

**Prerequisites:** Python 3.8+, Go 1.24+, Protocol Buffers Compiler (protoc), Git

### Ubuntu/Debian Installation

```bash
# Install system dependencies
sudo apt update && sudo apt install python3 python3-pip golang-go protobuf-compiler git rsync

# Clone and setup
git clone https://github.com/vultisig/vultitool
cd vultitool

# One-command setup (installs dependencies + builds protobuf + builds tools)
make setup && make build

# Verify installation
./vultitool doctor health
```

### macOS Installation (Quick Start)

```bash
# One-command bootstrap (installs everything)
git clone https://github.com/vultisig/vultitool
cd vultitool
./bootstrap-macos.sh
```

### macOS Installation (Manual)

```bash
# Install dependencies via Homebrew
brew install python go protobuf git

# Clone and setup
git clone https://github.com/vultisig/vultitool
cd vultitool

# One-command setup (installs dependencies + builds protobuf + builds tools)
make setup && make build

# Verify installation
./vultitool doctor health
```

**Manual setup:** See [detailed instructions](#detailed-setup) below.

## Usage Examples

```bash
# Get help on available commands
./vultitool help

# Parse and display a vault file
./vultitool vault parse MyVault.vult

# Brief summary
./vultitool vault parse MyVault.vult --summary

# JSON output for automation
./vultitool vault parse MyVault.vult --json

# Parse encrypted vault with password
./vultitool vault parse MyVault.vult --password mypassword

# Validate vault format
./vultitool vault validate MyVault.vult

# Export vault metadata
./vultitool vault export MyVault.vult output.json

# Test with included samples
./vultitool vault parse tests/fixtures/testGG20-part1of2.vult --summary
```

## What is Vultisig?

Vultisig is a **seedless crypto wallet** that uses Multi-Party Computation (MPC) with Threshold Signature Schemes (TSS) for transaction signing. Instead of traditional seed phrases, Vultisig uses distributed "vault parts" stored in `.vult` files.

**Key Features:**
- **No seed phrases** - Uses distributed key shares instead
- **MPC-based signing** - Supports both GG20 and DKLS protocols
- **Multi-device support** - Hot (2-of-2) and Secure (2-of-3) vaults
- **Cross-platform** - Android, iOS, macOS, Web, Windows

### Official Vultisig Resources

- **Website**: [https://vultisig.com/](https://vultisig.com/) - Download the app and learn more
- **Documentation**: [https://docs.vultisig.com/](https://docs.vultisig.com/) - Complete user and developer guides
- **Source Code**: [https://github.com/vultisig/](https://github.com/vultisig/) - Official repositories and development

## Decryption Method Consistency

`vultitool` uses **exactly the same decryption methods** as the official [mobile-tss-lib](https://github.com/vultisig/mobile-tss-lib) Go implementation. This ensures 100% compatibility with encrypted `.vult` files.

### Technical Details

**Algorithm**: AES-GCM with SHA256 password hashing  
**Implementation**: Direct Python port of the Go `DecryptVault` function  
**Source**: `mobile-tss-lib/cmd/recovery-cli/main.go` lines 522-555  

**Process:**
1. Hash password using SHA256: `hash := sha256.Sum256([]byte(password))`
2. Create AES cipher with 256-bit key from hash
3. Use GCM mode with 12-byte nonce (standard size)
4. Extract nonce from beginning of encrypted data
5. Decrypt using `gcm.Open` equivalent with automatic tag verification

This approach eliminates any guesswork and ensures `vultitool` can decrypt any `.vult` file that the official Vultisig tools can handle.

## Self-Test System

`vultitool` includes a comprehensive self-test system to ensure reliability and serve as a "truth machine" for Vultisig vault analysis.

### Quick Self-Test

```bash
# Quick health check
./vultitool doctor health

# Full comprehensive test suite
./vultitool doctor selftest

# Environment and dependency check
./vultitool doctor env
```

### Test Coverage

**Current Status: 100% pass rate (48/48 tests)**

- **GG20 vault parsing**: `testGG20-part1of2.vult`, `testGG20-part2of2.vult`
- **DKLS vault parsing**: `testDKLS-1of2.vult`, `testDKLS-2of2.vult`

**Test File Attribution**: The `testGG20` and `testDKLS` files were sourced from [SxMShaDoW/Vultisig-Share-Decoder](https://github.com/SxMShaDoW/Vultisig-Share-Decoder) with appreciation for the contribution to the Vultisig testing ecosystem.
- **Fast Vault (2-of-2)**: `qa-fast-share1of2.vult`, `qa-fast-share2of2.vult`
- **Secure Vault (3-of-3)**: `qa-secure-share1of3.vult`, `qa-secure-share2of3.vult`, `qa-secure-share3of3.vult`
- **Encrypted vault support**: Password-protected vaults with authentication
- **Password security validation**: Tests correct/incorrect/empty/blank password handling
- **Output format validation**: JSON, summary, export functionality
- **Error handling**: Invalid files, missing files
- **Automated testing**: Fully automated selftest with no manual intervention required

### Example Test Output

```
[PASS] Basic parse: tests/fixtures/testGG20-part1of2.vult
       Parsed GG20 vault successfully
[PASS] Basic parse: tests/fixtures/qa-fast-share2of2.vult 
       Parsed DKLS vault successfully
[PASS] Encrypted vault test
       Password security works correctly
[PASS] Export JSON: tests/fixtures/testDKLS-1of2.vult
       JSON export successful

=== Test Results Summary ===
Total tests: 48
Passed: 48
Failed: 0
Pass rate: 100.0%
```

See [`TESTING.md`](TESTING.md) for complete testing documentation.

## Developer Workflow & CI/CD

vultitool includes comprehensive CI/CD-ready infrastructure for professional development workflows:

### Pre-Commit Validation System

**Quick Validation (5-10 seconds)**
```bash
# Run fast pre-commit checks before every commit
./scripts/pre-commit-check.sh quick

# Install as git pre-commit hook (runs automatically on git commit)
./scripts/pre-commit-check.sh setup  
```

**Full Clean-Slate Validation (2-3 minutes)**
```bash
# Full validation: rebuilds everything from scratch
./scripts/pre-commit-check.sh

# Alternative: use Makefile target
make test-clean
```

### What Gets Validated

✅ **Version consistency** across VERSION file, CHANGELOG.md, and CLI output  
✅ **Naming conventions** (vultitool lowercase, Vultisig title case)  
✅ **No protobuf warnings** from version mismatches  
✅ **Self-tests pass** (48/48 test suite)  
✅ **Clean environment** builds and works properly  
✅ **Dependency integrity** ensures reproducible builds  

### Developer Commands

```bash
# Essential developer workflow
./scripts/pre-commit-check.sh quick  # Before every commit
git add .
# Craft commit message manually

# For releases or major PRs
./scripts/pre-commit-check.sh         # Full validation

# Build system helpers  
make status                           # Check current build state
make check-deps                      # Verify all tools installed
make clean && make build             # Fresh rebuild
```

### Why This Infrastructure Matters

- **Prevents "works on my machine" issues** - Clean-slate testing catches environment dependencies
- **Eliminates dependency hell** - Version pinning and validation prevents protobuf warnings
- **Maintains code quality** - Automated checks enforce naming conventions and standards
- **Enables CI/CD integration** - Scripts designed for automated testing environments
- **Professional development** - Matches enterprise-grade development practices

## Command Reference

### Getting Help

```bash
# Show main help and available commands
./vultitool help
./vultitool --help
./vultitool -h

# Show help for specific commands
./vultitool vault --help
./vultitool doctor --help
```

### `vultitool vault parse <file>`

Parse and display vault contents with flexible output formatting.

**Options:**
- `--summary` - Brief overview only
- `--json` - Machine-readable JSON output
- `--verbose` - Show additional technical details
- `--password` - Vault password for encrypted vaults

**Use Cases:**
- Quick vault overview with `--summary`
- Automation and scripting with `--json`
- Flexible detail level control

**Example Output:**
```
=== Vault Analysis: testGG20-part1of2.vult ===
File Size: 26644 chars → 19982 bytes
Container Version: 1
Encrypted: No

Vault Name: 'Test private key vault'
Crypto Type: GG20
ECDSA Public Key: 0267db81657a956f364167c3986a426b448a74ac0db2092f6665c4c202b37f6f1d
EdDSA Public Key: c6da2ad7b18728f6481d747a7335fd52a5eed82f3c3d95a51deed03399c5c0b6
Local Party ID: Pixel 5a-a9b
Created: 2024-10-19T07:22:50

Signers (2):
  1. Pixel 5a-a9b
  2. iPhone-EC4

Key Shares (2):
  Share 1: Public Key: 0267db81... (12953 chars)
  Share 2: Public Key: c6da2ad7... (1611 chars)
```

### `vultitool vault inspect <file>`

Deep technical analysis of vault structure (always detailed/verbose output).

**Options:**
- `--show-keyshares` - Display sensitive key share data (WARNING: sensitive)
- `--password` - Vault password for encrypted vaults

**Use Cases:**
- Security auditing and forensic analysis
- Debugging vault issues
- Accessing sensitive key share data when needed

**Key Differences from `parse`:**
- Always shows detailed output (equivalent to `parse --verbose`)
- No JSON or summary output options
- Can display actual key share data with `--show-keyshares`
- Designed for technical inspection rather than general parsing

### `vultitool vault validate <file>`

Validate vault file format and structure.

**Options:**
- `--strict` - Enable strict validation rules
- `--password` - Vault password for encrypted vaults

**Output:**
```
Vault validation passed
```

### `vultitool vault export <file> <output>`

Export vault metadata to structured format.

**Options:**
- `--format json|yaml` - Output format (default: json)
- `--password` - Vault password for encrypted vaults

## Command Comparison

| Feature | `parse` | `inspect` |
|---------|---------|----------|
| **Output Formats** | Human-readable, JSON, Summary | Human-readable only (always detailed) |
| **Detail Level** | Configurable (`--verbose`) | Always verbose |
| **Automation Friendly** | Yes (`--json`, `--summary`) | No |
| **Key Share Data** | Never shown | Optional with `--show-keyshares` |
| **Primary Use Case** | General parsing, automation | Security analysis, debugging |

**Quick Decision Guide:**
- Need JSON output or brief summary? → Use `parse`
- Need to see actual key share data? → Use `inspect`
- General vault analysis? → Use `parse` 
- Security audit or debugging? → Use `inspect`

## Supported Vault Types

| Type | Description | Protocol | Typical Use |
|------|-------------|----------|-------------|
| **GG20** | Traditional MPC protocol | ECDSA/EdDSA | General purpose |
| **DKLS** | Modern MPC protocol | ECDSA/EdDSA | Enhanced security |
| **Fast Vault** | 2-of-2 threshold | Hot signing | Daily transactions |
| **Secure Vault** | 2-of-3 threshold | Cold storage | Long-term holding |
| **Encrypted Vault** | Password-protected | Any protocol | Extra security layer |

## Understanding .vult Files

`.vult` files are **base64-encoded Protocol Buffer data** containing:

1. **VaultContainer** (outer wrapper)
   - Version info
   - Encryption status (supports password protection)
   - Inner vault data

2. **Vault** (core data)
   - Vault name and metadata
   - Public keys (ECDSA/EdDSA)
   - Signer identities
   - Distributed key shares
   - Creation timestamp

## Detailed Setup {#detailed-setup}

### Manual Setup (Step-by-Step)

If automated setup fails or you prefer manual control:

```bash
# 1. Install system dependencies
# Ubuntu/Debian: sudo apt install python3 python3-pip golang-go protobuf-compiler git rsync
# macOS: brew install python go protobuf git

# 2. Install Python dependencies
pip3 install -r requirements.txt

# 3. Download Go dependencies
go mod download

# 4. Update protobuf definitions from official Vultisig sources
./scripts/update-proto.sh

# 5. Generate protobuf bindings
make protobuf

# 6. Build components
make build

# 7. Verify everything works
./vultitool doctor health
```

### Build System Reference

```bash
make help           # Show all available commands
make status         # Check current build status  
make check-deps     # Verify all required tools are installed
make clean          # Clean all build artifacts
```

### macOS Bootstrap Guide

For a fresh macOS system, here's the complete bootstrap process from first clone:

**Option 1: Automated Bootstrap Script**

```bash
git clone https://github.com/vultisig/vultitool
cd vultitool
./bootstrap-macos.sh
```

**Option 2: Manual Step-by-Step**

```bash
# 1. Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Install required dependencies
brew install python go protobuf git

# 3. Clone the repository
git clone https://github.com/vultisig/vultitool
cd vultitool

# 4. Bootstrap the entire project
make check-deps     # Verify all tools are installed
make setup          # Install Python deps + generate protobuf
make build          # Build both Python and Go components

# 5. Verify everything works
./vultitool doctor health
./vultitool doctor selftest

# 6. Test with sample vault file
./vultitool vault parse tests/fixtures/testGG20-part1of2.vult --summary
```

**Expected Output:**
```
✅ All required dependencies found
✅ Setup complete!
✅ Python component ready
✅ Go binary built: vultitool-go

=== Health Check Results ===
✅ vultitool binary: OK
✅ Protobuf bindings: 14 files found
✅ Test files: 9 .vult files available
✅ All health checks passed!

=== Test Results Summary ===
Total tests: 48
Passed: 48
Failed: 0
Pass rate: 100.0%

📁 Vault: Test private key vault
🔐 Type: GG20
👥 Signers: 2
🗝️  Shares: 2
📅 Created: 2024-10-19T07:22:50
```

### macOS-Specific Notes

- **Virtual Environment**: macOS setup automatically creates a Python virtual environment (`venv/`) to avoid conflicts with system Python
- **Protobuf Warnings**: You may see compatibility warnings about protobuf versions - these can be safely ignored
- **Homebrew Path**: Ensure `/opt/homebrew/bin` is in your PATH for Apple Silicon Macs
- **Dependencies**: All dependencies are managed via Homebrew for consistent installation

## Project Goals

This tool is part of a broader effort to:

1. **Document** the Vultisig ecosystem comprehensively
2. **Enable** better developer onboarding and testing
3. **Build** reference implementations for key workflows
4. **Establish** technical foundation for tooling and automation

## Security Notes

**WARNING - Key Share Data**: The `--show-keyshares` flag displays sensitive cryptographic material. Use only in secure environments.

**WARNING - File Handling**: `.vult` files contain cryptographic keys. Handle with appropriate security practices.

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

**Status:** Archived – Development has moved to [`vultool`](https://github.com/RowboTony/vultool)

For detailed technical documentation, see [spec.md](spec.md).
