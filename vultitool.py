#!/usr/bin/env python3
"""
VultiTool - Command-line tools for working with VultiSig vault files
"""

import sys
import argparse
from pathlib import Path

# Add the commands directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "commands"))

from vault import VaultCommands
from doctor import DoctorCommands

def main():
    """Main entry point for vultitool"""
    parser = argparse.ArgumentParser(
        description="VultiTool - Command-line tools for VultiSig vault files",
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
