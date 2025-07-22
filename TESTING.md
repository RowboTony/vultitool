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
- ✅ **GG20 vaults**: `Test-part1of2.vult`, `Test-part2of2.vult`
- ✅ **DKLS vaults**: `TestDKLS1of2.vult`, `TestDKLS2of2.vult`, `qa-fast-share1of2.vult`
- ✅ **Password-protected**: `qa-fast-share2of2.vult` (password: `vulticli01`) - _Now supported!_

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
- ❌ Password-protected file handling (_Documented limitation_)

## Current Test Results

**Pass Rate: 84.8% (28/33 tests)**

### ✅ Passing Tests (28)
- All GG20 vault parsing (`Test-part*.vult`)
- All DKLS vault parsing (`TestDKLS*.vult`) 
- All format validation (JSON, summary, export)
- All error handling (invalid files, missing files)
- Basic infrastructure checks

### ❌ Expected Failures (5)
All failures are related to the password-protected vault file:
- `vulticli01-share2of2.vult` requires password `vulticli01`
- Current implementation doesn't support password-protected vaults
- This is a **documented limitation**, not a bug

## Test File Specifications

| File | Type | Encryption | Signers | Shares | Status |
|------|------|------------|---------|---------|--------|
| `Test-part1of2.vult` | GG20 | No | 2 | 2 | ✅ |
| `Test-part2of2.vult` | GG20 | No | 2 | 2 | ✅ |
| `TestDKLS1of2.vult` | DKLS | No | 2 | 2 | ✅ |
| `TestDKLS2of2.vult` | DKLS | No | 2 | 2 | ✅ |
|| `qa-fast-share1of2.vult` | DKLS | No | 2 | 2 | ✅ |
| `vulticli01-share2of2.vult` | DKLS | **Yes** | 2 | 2 | ❌ Password required |

## Example Test Output

```
=== Vultitool Self-Test Suite ===
Starting tests at 2025-07-21T16:13:19.705435

1. Testing file existence...
[PASS] File existence: Test-part1of2.vult
[PASS] File existence: TestDKLS1of2.vult

2. Testing basic vault parsing...
[PASS] Basic parse: Test-part1of2.vult
       Parsed GG20 vault successfully
[PASS] Basic parse: TestDKLS1of2.vult  
       Parsed DKLS vault successfully

3. Testing summary output format...
[PASS] Summary output: Test-part1of2.vult
       Summary format correct

4. Testing vault validation...
[PASS] Validation: Test-part1of2.vult
       Validation passed

5. Testing export functionality...
[PASS] Export JSON: Test-part1of2.vult
       JSON export successful

6. Testing error handling...
[PASS] Invalid file handling
       Invalid file rejected as expected

=== Test Results Summary ===
Total tests: 33
Passed: 28
Failed: 5
Pass rate: 84.8%
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

## Future Enhancements

### Planned Features
- [ ] Password-protected vault support
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
