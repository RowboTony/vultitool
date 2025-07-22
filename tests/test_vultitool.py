#!/usr/bin/env python3
"""
Vultitool Self-Test Suite
Comprehensive testing for .vult file parsing and vultitool functionality
"""

import sys
import json
import subprocess
import tempfile
import base64
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class VultitoolTester:
    def __init__(self):
        self.passed_tests = 0
        self.failed_tests = 0
        self.test_results = []
        
        # Known test files and their expected properties
        self.test_files = {
            "tests/fixtures/testGG20-part1of2.vult": {
                "type": "GG20",
                "vault_name": "Test private key vault",
                "encrypted": False,
                "expected_signers": 2,
                "expected_shares": 2,
                "public_key_ecdsa": "0267db81657a956f364167c3986a426b448a74ac0db2092f6665c4c202b37f6f1d"
            },
            "tests/fixtures/testGG20-part2of2.vult": {
                "type": "GG20", 
                "vault_name": "Test private key vault",
                "encrypted": False,
                "expected_signers": 2,
                "expected_shares": 2,
                "public_key_ecdsa": "0267db81657a956f364167c3986a426b448a74ac0db2092f6665c4c202b37f6f1d"
            },
            "tests/fixtures/testDKLS-1of2.vult": {
                "type": "DKLS",
                "vault_name": "Test Fast Vault DKLS",
                "encrypted": False,
                "expected_signers": 2,
                "expected_shares": 2,
                "public_key_ecdsa": "0333e3d4df9cc071be24fd6c995421036074a1a88e5d3e0bc211b7ef4330078d9b"
            },
            "tests/fixtures/testDKLS-2of2.vult": {
                "type": "DKLS",
                "vault_name": "Test Fast Vault DKLS", 
                "encrypted": False,
                "expected_signers": 2,
                "expected_shares": 2,
                "public_key_ecdsa": "0333e3d4df9cc071be24fd6c995421036074a1a88e5d3e0bc211b7ef4330078d9b"
            },
            "tests/fixtures/qa-fast-share1of2.vult": {
                "type": "DKLS",
                "encrypted": False,
                "expected_signers": 2,
                "expected_shares": 2
            },
            "tests/fixtures/qa-fast-share2of2.vult": {
                "type": "DKLS",
                "encrypted": True,  # This one requires password
                "password": "vulticli01",
                "expected_signers": 2,
                "expected_shares": 2
            }
        }
        
    def log_result(self, test_name: str, passed: bool, message: str = "", details: str = ""):
        """Log test result"""
        status = "PASS" if passed else "FAIL"
        self.test_results.append({
            "test": test_name,
            "status": status,
            "message": message,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })
        
        if passed:
            self.passed_tests += 1
            print(f"[PASS] {test_name}")
            if message:
                print(f"       {message}")
        else:
            self.failed_tests += 1
            print(f"[FAIL] {test_name}")
            if message:
                print(f"       {message}")
            if details:
                print(f"       Details: {details}")
    
    def run_vultitool_command(self, args: List[str]) -> Tuple[int, str, str]:
        """Run vultitool command and return (exit_code, stdout, stderr)"""
        try:
            cmd = ["./vultitool"] + args
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", "Command timed out"
        except Exception as e:
            return -1, "", str(e)
    
    def test_file_exists(self, filename: str) -> bool:
        """Test if test file exists"""
        file_path = Path(filename)
        exists = file_path.exists()
        self.log_result(
            f"File existence: {filename}",
            exists,
            f"File {'found' if exists else 'missing'}: {file_path.absolute()}"
        )
        return exists
    
    def test_basic_parse(self, filename: str, expected: Dict) -> bool:
        """Test basic parsing of vault file"""
        # Build command with password if required
        cmd = ["vault", "parse", filename, "--json"]
        if expected.get("encrypted", False) and "password" in expected:
            cmd.extend(["--password", expected["password"]])
            
        exit_code, stdout, stderr = self.run_vultitool_command(cmd)
        
        if exit_code != 0:
            self.log_result(
                f"Basic parse: {filename}",
                False,
                f"Command failed with exit code {exit_code}",
                f"stderr: {stderr}"
            )
            return False
        
        try:
            data = json.loads(stdout)
            vault = data.get("vault", {})
            
            # Check expected fields
            checks = []
            
            # Vault name check (if expected)
            if "vault_name" in expected:
                actual_name = vault.get("name", "")
                name_match = actual_name == expected["vault_name"]
                checks.append(("vault_name", name_match, f"Expected: '{expected['vault_name']}', Got: '{actual_name}'"))
            
            # Lib type check
            actual_type = vault.get("lib_type", "")
            type_match = actual_type == expected["type"]
            checks.append(("lib_type", type_match, f"Expected: '{expected['type']}', Got: '{actual_type}'"))
            
            # Public key check (if expected)
            if "public_key_ecdsa" in expected:
                actual_key = vault.get("public_key_ecdsa", "")
                key_match = actual_key == expected["public_key_ecdsa"]
                checks.append(("public_key", key_match, f"Expected: '{expected['public_key_ecdsa']}', Got: '{actual_key}'"))
            
            # Signers count
            actual_signers = len(vault.get("signers", []))
            signers_match = actual_signers == expected["expected_signers"]
            checks.append(("signers_count", signers_match, f"Expected: {expected['expected_signers']}, Got: {actual_signers}"))
            
            # Key shares count
            actual_shares = len(vault.get("key_shares", []))
            shares_match = actual_shares == expected["expected_shares"]
            checks.append(("shares_count", shares_match, f"Expected: {expected['expected_shares']}, Got: {actual_shares}"))
            
            # Check if all validations passed
            all_passed = all(check[1] for check in checks)
            failed_checks = [check for check in checks if not check[1]]
            
            self.log_result(
                f"Basic parse: {filename}",
                all_passed,
                f"Parsed {expected['type']} vault successfully" if all_passed else f"Field validation failed",
                "; ".join([f"{check[0]}: {check[2]}" for check in failed_checks]) if failed_checks else ""
            )
            
            return all_passed
            
        except json.JSONDecodeError as e:
            self.log_result(
                f"Basic parse: {filename}",
                False,
                "Failed to parse JSON output",
                f"JSON error: {str(e)}"
            )
            return False
    
    def test_summary_output(self, filename: str, expected: Dict = None) -> bool:
        """Test summary output format"""
        # Build command with password if required
        cmd = ["vault", "parse", filename, "--summary"]
        if expected and expected.get("encrypted", False) and "password" in expected:
            cmd.extend(["--password", expected["password"]])
            
        exit_code, stdout, stderr = self.run_vultitool_command(cmd)
        
        if exit_code != 0:
            self.log_result(
                f"Summary output: {filename}",
                False,
                f"Command failed with exit code {exit_code}",
                stderr
            )
            return False
        
        # Check for expected summary elements
        required_elements = ["📁 Vault:", "🔐 Type:", "👥 Signers:", "🗝️  Shares:"]
        missing_elements = [elem for elem in required_elements if elem not in stdout]
        
        success = len(missing_elements) == 0
        self.log_result(
            f"Summary output: {filename}",
            success,
            "Summary format correct" if success else f"Missing elements: {', '.join(missing_elements)}"
        )
        return success
    
    def test_validation(self, filename: str, expected: Dict = None) -> bool:
        """Test vault validation"""
        # Build command with password if required
        cmd = ["vault", "validate", filename]
        if expected and expected.get("encrypted", False) and "password" in expected:
            cmd.extend(["--password", expected["password"]])
            
        exit_code, stdout, stderr = self.run_vultitool_command(cmd)
        
        # For valid test files, validation should pass
        success = exit_code == 0 and "✅ Vault validation passed" in stdout
        self.log_result(
            f"Validation: {filename}",
            success,
            "Validation passed" if success else f"Validation failed (exit: {exit_code})",
            stdout if not success else ""
        )
        return success
    
    def test_export_functionality(self, filename: str, expected: Dict = None) -> bool:
        """Test vault export functionality"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp_file:
            tmp_path = tmp_file.name
        
        try:
            # Test JSON export with password if required
            cmd = ["vault", "export", filename, tmp_path]
            if expected and expected.get("encrypted", False) and "password" in expected:
                cmd.extend(["--password", expected["password"]])
                
            exit_code, stdout, stderr = self.run_vultitool_command(cmd)
            
            if exit_code != 0:
                self.log_result(
                    f"Export JSON: {filename}",
                    False,
                    f"Export command failed (exit: {exit_code})",
                    stderr
                )
                return False
            
            # Verify exported file exists and is valid JSON
            try:
                with open(tmp_path, 'r') as f:
                    exported_data = json.load(f)
                
                # Basic structure checks
                has_file_info = "file_info" in exported_data
                has_container = "container" in exported_data
                has_vault = "vault" in exported_data
                
                success = has_file_info and has_container and has_vault
                self.log_result(
                    f"Export JSON: {filename}",
                    success,
                    "JSON export successful" if success else "Exported JSON missing required sections"
                )
                return success
                
            except json.JSONDecodeError as e:
                self.log_result(
                    f"Export JSON: {filename}",
                    False,
                    "Exported file is not valid JSON",
                    str(e)
                )
                return False
                
        finally:
            # Cleanup
            try:
                Path(tmp_path).unlink()
            except:
                pass
    
    def test_encrypted_vault(self) -> bool:
        """Test handling of encrypted vaults with passwords"""
        encrypted_file = "tests/fixtures/qa-fast-share2of2.vult"
        correct_password = "vulticli01"
        
        if not Path(encrypted_file).exists():
            self.log_result(
                "Encrypted vault test",
                True,
                "No encrypted test file available - skipping"
            )
            return True
        
        test_results = []
        
        # Test 1: With correct password should succeed
        exit_code, stdout, stderr = self.run_vultitool_command(["vault", "parse", encrypted_file, "--json", "--password", correct_password])
        correct_password_works = exit_code == 0
        test_results.append(("correct_password", correct_password_works))
        
        # Test 2: With wrong password should fail (PASS means it properly rejects)
        exit_code, stdout, stderr = self.run_vultitool_command(["vault", "parse", encrypted_file, "--json", "--password", "wrongpassword"])
        wrong_password_rejected = exit_code != 0  # PASS if command fails (security working)
        test_results.append(("wrong_password_rejected", wrong_password_rejected))
        
        # Test 3: With empty password should fail (PASS means it properly rejects)
        exit_code, stdout, stderr = self.run_vultitool_command(["vault", "parse", encrypted_file, "--json", "--password", ""])
        empty_password_rejected = exit_code != 0  # PASS if command fails (security working)
        test_results.append(("empty_password_rejected", empty_password_rejected))
        
        # Test 4: With blank/space password should fail (PASS means it properly rejects)
        exit_code, stdout, stderr = self.run_vultitool_command(["vault", "parse", encrypted_file, "--json", "--password", "   "])
        blank_password_rejected = exit_code != 0  # PASS if command fails (security working)
        test_results.append(("blank_password_rejected", blank_password_rejected))
        
        # Overall success if all password security tests work correctly
        all_tests_passed = all(result[1] for result in test_results)
        failed_tests = [result[0] for result in test_results if not result[1]]
        
        self.log_result(
            "Encrypted vault test",
            all_tests_passed,
            f"Password security works correctly" if all_tests_passed else f"Password security issues: {', '.join(failed_tests)}",
            "; ".join([f"{test}: {'✓' if passed else '✗'}" for test, passed in test_results])
        )
        
        return all_tests_passed
    
    def test_invalid_file_handling(self) -> bool:
        """Test handling of invalid/corrupted files"""
        # Create a temporary invalid file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.vult', delete=False) as tmp_file:
            tmp_file.write("invalid_base64_content_not_a_vault")
            tmp_path = tmp_file.name
        
        try:
            exit_code, stdout, stderr = self.run_vultitool_command(["vault", "parse", tmp_path])
            
            # Should fail gracefully with non-zero exit code
            success = exit_code != 0
            self.log_result(
                "Invalid file handling",
                success,
                "Invalid file rejected as expected" if success else "Invalid file was accepted (unexpected)",
                f"exit_code: {exit_code}, stderr: {stderr[:200]}..."
            )
            return success
            
        finally:
            try:
                Path(tmp_path).unlink()
            except:
                pass
    
    def test_missing_file_handling(self) -> bool:
        """Test handling of missing files"""
        nonexistent_file = "nonexistent_file.vult"
        exit_code, stdout, stderr = self.run_vultitool_command(["vault", "parse", nonexistent_file])
        
        # Should fail gracefully
        success = exit_code != 0
        self.log_result(
            "Missing file handling",
            success,
            "Missing file handled as expected" if success else "Missing file not handled properly"
        )
        return success
    
    def run_all_tests(self) -> bool:
        """Run all self-tests"""
        print("=== Vultitool Self-Test Suite ===")
        print(f"Starting tests at {datetime.now().isoformat()}")
        print()
        
        # Test 1: File existence
        print("1. Testing file existence...")
        for filename in self.test_files.keys():
            if not self.test_file_exists(filename):
                print(f"   Warning: {filename} not found - skipping related tests")
        print()
        
        # Test 2: Basic parsing for each available file
        print("2. Testing basic vault parsing...")
        for filename, expected in self.test_files.items():
            if Path(filename).exists():
                self.test_basic_parse(filename, expected)
        print()
        
        # Test 3: Summary output
        print("3. Testing summary output format...")
        for filename, expected in self.test_files.items():
            if Path(filename).exists():
                self.test_summary_output(filename, expected)
        print()
        
        # Test 4: Validation
        print("4. Testing vault validation...")
        for filename, expected in self.test_files.items():
            if Path(filename).exists():
                self.test_validation(filename, expected)
        print()
        
        # Test 5: Export functionality
        print("5. Testing export functionality...")
        for filename, expected in self.test_files.items():
            if Path(filename).exists():
                self.test_export_functionality(filename, expected)
        print()
        
        # Test 6: Error handling
        print("6. Testing error handling...")
        self.test_encrypted_vault()
        self.test_invalid_file_handling()
        self.test_missing_file_handling()
        print()
        
        # Summary
        total_tests = self.passed_tests + self.failed_tests
        pass_rate = (self.passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print("=== Test Results Summary ===")
        print(f"Total tests: {total_tests}")
        print(f"Passed: {self.passed_tests}")
        print(f"Failed: {self.failed_tests}")
        print(f"Pass rate: {pass_rate:.1f}%")
        
        if self.failed_tests > 0:
            print("\nFailed tests:")
            for result in self.test_results:
                if result["status"] == "FAIL":
                    print(f"  - {result['test']}: {result['message']}")
        
        print(f"\nTest completed at {datetime.now().isoformat()}")
        
        return self.failed_tests == 0
    
    def generate_report(self, output_file: str = "test_report.json"):
        """Generate detailed test report"""
        report = {
            "test_run": {
                "timestamp": datetime.now().isoformat(),
                "total_tests": self.passed_tests + self.failed_tests,
                "passed": self.passed_tests,
                "failed": self.failed_tests,
                "pass_rate": (self.passed_tests / (self.passed_tests + self.failed_tests) * 100) if (self.passed_tests + self.failed_tests) > 0 else 0
            },
            "test_files": self.test_files,
            "results": self.test_results
        }
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"Detailed test report saved to: {output_file}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Vultitool Self-Test Suite")
    parser.add_argument("--report", help="Generate detailed JSON report", metavar="FILE")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    tester = VultitoolTester()
    success = tester.run_all_tests()
    
    if args.report:
        tester.generate_report(args.report)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
