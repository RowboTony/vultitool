"""
Doctor command implementation for vultitool
Provides health checks, self-tests, and diagnostic capabilities
"""

import sys
import subprocess
from pathlib import Path
from datetime import datetime


class DoctorCommands:
    @staticmethod
    def setup_parser(parser):
        """Setup doctor command parser with subcommands"""
        subparsers = parser.add_subparsers(dest='doctor_action', help='Doctor operations')
        
        # Self-test command
        selftest_parser = subparsers.add_parser('selftest', help='Run comprehensive self-tests')
        selftest_parser.add_argument('--report', help='Generate detailed JSON report', metavar='FILE')
        selftest_parser.add_argument('--quick', action='store_true', help='Run only basic tests')
        
        # Health check command
        health_parser = subparsers.add_parser('health', help='Quick health check')
        
        # Environment check command
        env_parser = subparsers.add_parser('env', help='Check environment and dependencies')
    
    @staticmethod
    def handle(args):
        """Route doctor commands to appropriate handlers"""
        if args.doctor_action == 'selftest':
            return DoctorCommands.selftest(args)
        elif args.doctor_action == 'health':
            return DoctorCommands.health(args)
        elif args.doctor_action == 'env':
            return DoctorCommands.environment_check(args)
        else:
            print("No doctor action specified. Use --help for usage.")
            return 1
    
    @staticmethod
    def selftest(args):
        """Run comprehensive self-tests"""
        print("🔍 Running Vultitool Self-Tests...")
        print()
        
        # Import and run our test suite
        try:
            test_script = Path(__file__).parent.parent / "tests" / "test_vultitool.py"
            if not test_script.exists():
                print("❌ Test suite not found!")
                return 1
            
            cmd = ["python3", str(test_script)]
            if args.report:
                cmd.extend(["--report", args.report])
                
            # Run from project root so tests can access parent modules
            result = subprocess.run(cmd, cwd=test_script.parent.parent)
            return result.returncode
            
        except Exception as e:
            print(f"❌ Failed to run self-tests: {e}")
            return 1
    
    @staticmethod
    def health(args):
        """Quick health check"""
        # Get version from VERSION file
        try:
            version_file = Path(__file__).parent.parent / "VERSION"
            if version_file.exists():
                version = version_file.read_text().strip()
            else:
                version = "unknown"
        except Exception:
            version = "unknown"
            
        print(":: Vultitool Health Check 🩺 👀 ")
        print(f":: Version: vultitool {version} ")
        print(f":: Timestamp: {datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z')} ")
        print()
        
        issues = []
        
        # Check if vultitool is executable
        vultitool_path = Path("./vultitool")
        if not vultitool_path.exists():
            issues.append("vultitool binary not found")
        elif not vultitool_path.is_file():
            issues.append("vultitool is not a file")
        elif not vultitool_path.stat().st_mode & 0o111:
            issues.append("vultitool is not executable")
        else:
            print("✅ vultitool binary: OK")
        
        # Check for protobuf bindings
        generated_path = Path("generated")
        if not generated_path.exists():
            issues.append("Generated protobuf bindings not found")
        else:
            proto_files = list(generated_path.glob("**/*.py"))
            if len(proto_files) == 0:
                issues.append("No protobuf Python files found in generated/")
            else:
                print(f"✅ Protobuf bindings: {len(proto_files)} files found")
        
        # Check for test files - look for all .vult files in tests/fixtures
        test_fixtures_path = Path("tests/fixtures")
        if test_fixtures_path.exists():
            vult_files = list(test_fixtures_path.glob("*.vult"))
            if len(vult_files) == 0:
                issues.append("No test .vult files found in tests/fixtures/")
            else:
                print(f"✅ Test files: {len(vult_files)} .vult files available")
        else:
            issues.append("tests/fixtures/ directory not found")
        
        # Check Python dependencies
        try:
            import base64
            import json
            print("✅ Python standard library: OK")
        except ImportError as e:
            issues.append(f"Missing Python dependency: {e}")
        
        # Check Go binary functionality
        go_binary_path = Path("./vultitool-go")
        if not go_binary_path.exists():
            issues.append("vultitool-go binary not found - run 'make build-go'")
        elif not go_binary_path.is_file():
            issues.append("vultitool-go is not a file")
        elif not go_binary_path.stat().st_mode & 0o111:
            issues.append("vultitool-go is not executable")
        else:
            # Test basic Go functionality
            try:
                result = subprocess.run(
                    ["./vultitool-go", "--help"], 
                    capture_output=True, 
                    text=True, 
                    timeout=5
                )
                if result.returncode == 0 and "vultitool" in result.stdout and "Commands:" in result.stdout:
                    print("✅ Go binary functionality: OK")
                else:
                    issues.append("vultitool-go --help failed or returned unexpected output")
            except subprocess.TimeoutExpired:
                issues.append("vultitool-go command timed out")
            except Exception as e:
                issues.append(f"Failed to execute vultitool-go: {e}")
        
        # Check Go module integrity
        go_mod_path = Path("go.mod")
        go_sum_path = Path("go.sum")
        if go_mod_path.exists() and go_sum_path.exists():
            print("✅ Go modules: OK")
        elif go_mod_path.exists() and not go_sum_path.exists():
            issues.append("go.sum missing - run 'go mod download' or 'make build-go'")
        else:
            issues.append("Go module files missing - project may not be properly initialized")
        
        # Try a basic command
        try:
            result = subprocess.run(
                ["./vultitool", "--version"], 
                capture_output=True, 
                text=True, 
                timeout=5
            )
            if result.returncode == 0:
                print("✅ Basic command execution: OK")
            else:
                issues.append("vultitool --version failed")
        except subprocess.TimeoutExpired:
            issues.append("vultitool command timed out")
        except Exception as e:
            issues.append(f"Failed to execute vultitool: {e}")
        
        print()
        
        if issues:
            print("❌ Health Check Failed!")
            print("Issues found:")
            for issue in issues:
                print(f"  - {issue}")
            return 1
        else:
            print("✅ All health checks passed!")
            print()
            print("💡 Next steps:")
            print("  - Run 'vultitool doctor selftest' for comprehensive testing")
            print("  - Try parsing a .vult file with 'vultitool vault parse <file>'")
            return 0
    
    @staticmethod
    def environment_check(args):
        """Check environment and dependencies"""
        print("🌍 Environment Check")
        print(f"Timestamp: {datetime.now().isoformat()}")
        print()
        
        # Python version
        print(f"Python version: {sys.version}")
        
        # Working directory
        cwd = Path.cwd()
        print(f"Working directory: {cwd}")
        
        # File structure
        print("\nProject structure:")
        important_paths = [
            "./vultitool",
            "./commands/",
            "./generated/",
            "./tests/",
            "./README.md",
            "./spec.md"
        ]
        
        for path_str in important_paths:
            path = Path(path_str)
            if path.exists():
                if path.is_file():
                    size = path.stat().st_size
                    print(f"  ✅ {path_str} (file, {size} bytes)")
                else:
                    items = len(list(path.iterdir())) if path.is_dir() else 0
                    print(f"  ✅ {path_str} (directory, {items} items)")
            else:
                print(f"  ❌ {path_str} (missing)")
        
        # Available .vult files (check both root and fixtures)
        vult_files = list(Path(".").glob("*.vult")) + list(Path("tests/fixtures").glob("*.vult")) if Path("tests/fixtures").exists() else list(Path(".").glob("*.vult"))
        print(f"\n.vult files found: {len(vult_files)}")
        for vult_file in sorted(vult_files):
            size = vult_file.stat().st_size
            print(f"  - {vult_file} ({size:,} bytes)")
        
        # Protobuf files
        if Path("generated").exists():
            pb_files = list(Path("generated").glob("**/*_pb2.py"))
            print(f"\nProtobuf bindings: {len(pb_files)} files")
            for pb_file in sorted(pb_files)[:5]:  # Show first 5
                rel_path = pb_file.relative_to("generated")
                print(f"  - {rel_path}")
            if len(pb_files) > 5:
                print(f"  ... and {len(pb_files) - 5} more")
        
        print(f"\nEnvironment check completed at {datetime.now().isoformat()}")
        return 0
