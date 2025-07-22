# Test Fixtures

This directory contains Vultisig `.vult` vault files used for testing and validation.

## Test Files

### GG20 Vaults (Traditional MPC Protocol)
- **`testGG20-part1of2.vult`** - Part 1 of 2-of-2 GG20 vault ("Test private key vault")
- **`testGG20-part2of2.vult`** - Part 2 of 2-of-2 GG20 vault ("Test private key vault")

### DKLS Vaults (Modern MPC Protocol)  
- **`testDKLS-1of2.vult`** - Part 1 of 2-of-2 DKLS vault ("Test Fast Vault DKLS")
- **`testDKLS-2of2.vult`** - Part 2 of 2-of-2 DKLS vault ("Test Fast Vault DKLS")

### Additional Test Cases
- **`qa-fast-share1of2.vult`** - DKLS vault share 1 (unencrypted)
- **`qa-fast-share2of2.vult`** - DKLS vault share 2 (password-protected: `vulticli01`)

### Secure Vault (3-Part DKLS)
- **`qa-secure-share1of3.vult`** - Part 1 of 3-of-3 DKLS "Secure Vault" ("QA Secure Vault 01")
- **`qa-secure-share2of3.vult`** - Part 2 of 3-of-3 DKLS "Secure Vault" ("QA Secure Vault 01")
- **`qa-secure-share3of3.vult`** - Part 3 of 3-of-3 DKLS "Secure Vault" ("QA Secure Vault 01")

## Vault Specifications

| File | Type | Encryption | Signers | Shares |
|------|------|------------|---------|--------|
| `testGG20-part1of2.vult` | GG20 | No | 2 | 2 |
| `testGG20-part2of2.vult` | GG20 | No | 2 | 2 |
| `testDKLS-1of2.vult` | DKLS | No | 2 | 2 |
| `testDKLS-2of2.vult` | DKLS | No | 2 | 2 |
| `qa-fast-share1of2.vult` | DKLS | No | 2 | 2 |
| `qa-fast-share2of2.vult` | DKLS | **Yes** | 2 | 2 |
| `qa-secure-share1of3.vult` | DKLS | No | 3 | 2 |
| `qa-secure-share2of3.vult` | DKLS | No | 3 | 2 |
| `qa-secure-share3of3.vult` | DKLS | No | 3 | 2 |

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
