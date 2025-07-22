# Test Fixtures

This directory contains Vultisig `.vult` vault files used for testing and validation.

## Test Files

### GG20 Vaults (Traditional MPC Protocol)
- **`testGG20-part1of2.vult`** - Part 1 of 2-of-2 GG20 vault ("Test private key vault")
- **`testGG20-part2of2.vult`** - Part 2 of 2-of-2 GG20 vault ("Test private key vault")

### DKLS Vaults (Modern MPC Protocol)  
- **`TestDKLS1of2.vult`** - Part 1 of 2-of-2 DKLS vault ("Test Fast Vault DKLS")
- **`TestDKLS2of2.vult`** - Part 2 of 2-of-2 DKLS vault ("Test Fast Vault DKLS")

### Additional Test Cases
- **`qa-fast-share1of2.vult`** - DKLS vault share 1 (unencrypted)
- **`qa-fast-share2of2.vult`** - DKLS vault share 2 (password-protected: `vulticli01`)

## Vault Specifications

| File | Type | Encryption | Signers | Shares | Public Key (ECDSA) |
|------|------|------------|---------|---------|-------------------|
| `Test-part1of2.vult` | GG20 | No | 2 | 2 | `0267db81...` |
|| `testGG20-part1of2.vult` | GG20 | No | 2 | 2 | `0267db81...` |
| `TestDKLS1of2.vult` | DKLS | No | 2 | 2 | `0333e3d4...` |
| `TestDKLS2of2.vult` | DKLS | No | 2 | 2 | `0333e3d4...` |
|| `qa-fast-share1of2.vult` | DKLS | No | 2 | 2 | - |
| `vulticli01-share2of2.vult` | DKLS | **Yes** | 2 | 2 | - |

## Usage in Tests

These files are used by `test_vultitool.py` to verify:
- Basic vault parsing functionality
- GG20 vs DKLS protocol support
- Output format validation (JSON, summary)
- Export functionality 
- Error handling (password-protected vaults)

## Security Note

⚠️ **These are test files only** - they contain sample cryptographic data for validation purposes and should not be used for actual value storage.

The password-protected file (`qa-fast-share2of2.vult`) uses password: `vulticli01`
