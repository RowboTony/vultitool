#!/usr/bin/env python3
"""
vultitool - Command-line tools for working with Vultisig vault files
"""

import sys
import argparse
from pathlib import Path

# Add the commands directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "commands"))

from vault import VaultCommands
from doctor import DoctorCommands


def get_version():
    """Get version from VERSION file"""
    try:
        version_file = Path(__file__).parent / "VERSION"
        if version_file.exists():
            return version_file.read_text().strip()
        else:
            return "unknown"
    except Exception:
        return "unknown"

def main():
    """Main entry point for vultitool"""
    parser = argparse.ArgumentParser(
        description="vultitool - Command-line tools for Vultisig vault files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  vultitool vault parse my-vault.vult --summary
  vultitool vault inspect my-vault.vult --show-keyshares
  vultitool vault validate my-vault.vult --strict
  vultitool vault export my-vault.vult output.json --format json
  vultitool doctor check
        """
    )
    
    # Add version flag
    parser.add_argument('--version', '-v', action='version', 
                       version=f'vultitool {get_version()}')
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Vault commands
    vault_parser = subparsers.add_parser('vault', help='Vault file operations')
    VaultCommands.setup_parser(vault_parser)
    
    # Doctor commands
    doctor_parser = subparsers.add_parser('doctor', help='System diagnostics')
    DoctorCommands.setup_parser(doctor_parser)
    
    # Parse arguments
    args = parser.parse_args()
    
    # Route to appropriate command handler
    if args.command == 'vault':
        return VaultCommands.handle(args)
    elif args.command == 'doctor':
        return DoctorCommands.handle(args)
    else:
        parser.print_help()
        return 1

if __name__ == '__main__':
    sys.exit(main())
