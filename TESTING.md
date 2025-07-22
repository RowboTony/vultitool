# Vultitool Self-Test System

## Overview

Vultitool includes a comprehensive self-test system to ensure the program works correctly and serves as a "truth machine" for Vultisig vault analysis.

## Quick Start

```bash
# Quick health check
./vultitool doctor health

# Full self-test suite  
./vultitool doctor selftest

# Environment diagnostics
./vultitool doctor env

# Generate detailed test report
./vultitool doctor selftest --report test_results.json
```

## Test Coverage

### 1. File Existence Tests
- ✅ Verifies all expected test files are present
- ✅ Checks for required `.vult` files used in testing

### 2. Basic Parsing Tests  
- ✅ **GG20 vaults**: `testGG20-part1of2.vult`, `testGG20-part2of2.vult`
- ✅ **DKLS vaults**: `testDKLS-1of2.vult`, `testDKLS-2of2.vult`
- ✅ **Fast Vault (2-of-2)**: `qa-fast-share1of2.vult`, `qa-fast-share2of2.vult`
- ✅ **Secure Vault (3-of-3)**: `qa-secure-share1of3.vult`, `qa-secure-share2of3.vult`, `qa-secure-share3of3.vult`
- ✅ **Password-protected**: Encrypted vault support with password authentication

### 3. Output Format Tests
- ✅ JSON output format validation
- ✅ Summary output format validation  
- ✅ Required fields presence check

### 4. Validation Tests
- ✅ Vault structure validation
- ✅ Field completeness checks
- ✅ Cryptographic key format validation

### 5. Export Functionality Tests
- ✅ JSON export format validation
- ✅ File creation and structure verification
- ✅ Data integrity checks

### 6. Error Handling Tests
- ✅ Invalid file rejection
- ✅ Missing file handling
- ✅ Password-protected file handling with correct/incorrect passwords

## Current Test Results

**Pass Rate: 100% (48/48 tests)** ✨

### ✅ Passing Tests (48)
- All GG20 vault parsing (`testGG20-part*.vult`)
- All DKLS vault parsing (`testDKLS-*.vult`) 
- All Fast Vault parsing (`qa-fast-share*.vult`)
- All Secure Vault parsing (`qa-secure-share*.vult`)
- All format validation (JSON, summary, export)
- All error handling (invalid files, missing files)
- Password security validation (correct/incorrect/empty passwords)
- Basic infrastructure checks

### ❌ Expected Failures (0)
**All tests now pass!** Password-protected vault support has been implemented with full compatibility with the official Vultisig mobile-tss-lib decryption methods.

## Test File Specifications

| File | Type | Encryption | Signers | Shares | Status |
|------|------|------------|---------|---------|--------|
| `testGG20-part1of2.vult` | GG20 | No | 2 | 2 | ✅ |
| `testGG20-part2of2.vult` | GG20 | No | 2 | 2 | ✅ |
| `testDKLS-1of2.vult` | DKLS | No | 2 | 2 | ✅ |
| `testDKLS-2of2.vult` | DKLS | No | 2 | 2 | ✅ |
| `qa-fast-share1of2.vult` | DKLS | No | 2 | 2 | ✅ |
| `qa-fast-share2of2.vult` | DKLS | **Yes** | 2 | 2 | ✅ |
| `qa-secure-share1of3.vult` | DKLS | No | 3 | 2 | ✅ |
| `qa-secure-share2of3.vult` | DKLS | No | 3 | 2 | ✅ |
| `qa-secure-share3of3.vult` | DKLS | No | 3 | 2 | ✅ |

## Example Test Output

```
=== Vultitool Self-Test Suite ===
Starting tests at 2025-07-21T21:50:17.631807

1. Testing file existence...
[PASS] File existence: tests/fixtures/testGG20-part1of2.vult
[PASS] File existence: tests/fixtures/qa-secure-share1of3.vult

2. Testing basic vault parsing...
[PASS] Basic parse: tests/fixtures/testGG20-part1of2.vult
       Parsed GG20 vault successfully
[PASS] Basic parse: tests/fixtures/qa-secure-share1of3.vult  
       Parsed DKLS vault successfully

3. Testing summary output format...
[PASS] Summary output: tests/fixtures/testGG20-part1of2.vult
       Summary format correct

4. Testing vault validation...
[PASS] Validation: tests/fixtures/testGG20-part1of2.vult
       Validation passed

5. Testing export functionality...
[PASS] Export JSON: tests/fixtures/testGG20-part1of2.vult
       JSON export successful

6. Testing error handling...
[PASS] Encrypted vault test
       Password security works correctly
[PASS] Invalid file handling
       Invalid file rejected as expected

=== Test Results Summary ===
Total tests: 48
Passed: 48
Failed: 0
Pass rate: 100.0%
```

## Health Check Features

### Quick Health Check
```bash
./vultitool doctor health
```
- ✅ Binary executable check
- ✅ Protobuf bindings verification
- ✅ Test file availability
- ✅ Python dependencies
- ✅ Basic command execution

### Environment Check
```bash
./vultitool doctor env
```
- Python version and environment
- Project structure verification
- Available `.vult` files inventory
- Protobuf bindings listing

## Integration

The self-test system integrates seamlessly with vultitool:

1. **Built-in Commands**: Access via `vultitool doctor` subcommands
2. **Standalone Script**: Run directly with `python3 test_vultitool.py`
3. **CI/CD Ready**: Returns proper exit codes (0=success, 1=failure)
4. **Reporting**: Generate JSON reports for automated analysis

## Possible Future Enhancements

### Planned Features
- [x] Password-protected vault support
- [ ] Additional edge case testing  
- [ ] Performance benchmarking
- [ ] Cross-platform compatibility tests
- [ ] Integration with CI/CD pipelines

### Test Coverage Expansion
- [ ] Multi-part vault reconstruction testing
- [ ] Vault compatibility verification
- [ ] Stress testing with large vault files
- [ ] Network dependency testing (for future features)

## Usage in Development

**Before commits:**
```bash
./vultitool doctor selftest
```

**For troubleshooting:**
```bash
./vultitool doctor health
./vultitool doctor env
```

**For documentation:**
```bash
./vultitool doctor selftest --report results.json
```

This self-test system ensures vultitool remains reliable and provides confidence in its analysis of Vultisig vault files.
