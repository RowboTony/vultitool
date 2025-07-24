#!/usr/bin/env python3
"""
Automatic Protobuf Version Setup
Detects your protoc compiler version and installs the matching Python protobuf library
to eliminate version mismatch warnings and maintain parity with Vultisig.
"""

import subprocess
import sys
import re
import os
from pathlib import Path

def get_protoc_version():
    """Get the protoc compiler version"""
    try:
        result = subprocess.run(['protoc', '--version'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ protoc not found. Please install Protocol Buffers compiler first.")
            print("   macOS: brew install protobuf")
            print("   Ubuntu: sudo apt install protobuf-compiler")
            return None
        
        # Parse version from "libprotoc X.Y.Z" or "libprotoc X.Y"
        version_match = re.search(r'libprotoc (\d+)\.(\d+)(?:\.(\d+))?', result.stdout)
        if not version_match:
            print(f"❌ Could not parse protoc version from: {result.stdout.strip()}")
            return None
        
        major = int(version_match.group(1))
        minor = int(version_match.group(2))
        patch = int(version_match.group(3)) if version_match.group(3) else 0
        
        return (major, minor, patch)
    except FileNotFoundError:
        print("❌ protoc not found. Please install Protocol Buffers compiler first.")
        return None

def protoc_to_python_version(protoc_version):
    """Convert protoc version to corresponding Python protobuf version"""
    major, minor, patch = protoc_version
    
    # The mapping from protoc version to Python protobuf version
    # Based on protobuf release history and Vultisig compatibility
    if major >= 29:
        return f"5.29.{patch if patch > 0 else 3}"
    elif major >= 28:
        return f"5.28.{patch if patch > 0 else 0}"
    elif major >= 27:
        return f"5.27.{patch if patch > 0 else 0}"
    elif major >= 26:
        return f"5.26.{patch if patch > 0 else 0}"
    elif major >= 25:
        return f"5.25.{patch if patch > 0 else 1}"
    elif major >= 24:
        return f"4.25.{patch if patch > 0 else 8}"
    elif major >= 23:
        return f"4.24.{patch if patch > 0 else 0}"
    elif major >= 22:
        return f"4.23.{patch if patch > 0 else 0}"
    elif major >= 21:
        return f"4.22.{patch if patch > 0 else 0}"
    else:
        # For older versions, use a compatible range
        return "4.21.0"

def get_current_python_protobuf():
    """Get currently installed Python protobuf version"""
    try:
        import google.protobuf
        return google.protobuf.__version__
    except ImportError:
        return None

def install_protobuf_version(version):
    """Install specific protobuf version"""
    print(f"📦 Installing protobuf=={version}...")
    
    # Detect if we're in a virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    
    cmd = [sys.executable, '-m', 'pip', 'install', f'protobuf=={version}']
    
    if not in_venv:
        print("⚠️  Not in a virtual environment. Installing with --user flag.")
        cmd.append('--user')
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ Successfully installed protobuf=={version}")
        return True
    else:
        print(f"❌ Failed to install protobuf=={version}")
        print(f"Error: {result.stderr}")
        return False

def main():
    print("🔧 vultitool Protobuf Version Setup")
    print("=" * 40)
    
    # Get protoc version
    protoc_version = get_protoc_version()
    if not protoc_version:
        sys.exit(1)
    
    major, minor, patch = protoc_version
    print(f"📋 Detected protoc version: {major}.{minor}.{patch}")
    
    # Calculate matching Python version
    target_python_version = protoc_to_python_version(protoc_version)
    print(f"🎯 Target Python protobuf version: {target_python_version}")
    
    # Check current Python version
    current_version = get_current_python_protobuf()
    if current_version:
        print(f"📦 Current Python protobuf version: {current_version}")
        
        if current_version == target_python_version:
            print("✅ Versions already match! No action needed.")
            return
        else:
            print(f"⚠️  Version mismatch detected:")
            print(f"   protoc generates: {target_python_version}")
            print(f"   Python runtime:   {current_version}")
            print(f"   This causes protobuf warnings that we'll fix.")
    else:
        print("📦 Python protobuf not installed")
    
    # Ask user for confirmation
    response = input(f"\nInstall protobuf=={target_python_version} to match your protoc? [Y/n]: ").strip().lower()
    if response in ['', 'y', 'yes']:
        if install_protobuf_version(target_python_version):
            print("\n🎉 Setup complete! Protobuf versions now match.")
            print("💡 Next steps:")
            print("   1. Regenerate protobuf files: make protobuf-python")
            print("   2. Test with: python3 -c 'from vultisig.vault.v1.vault_pb2 import Vault; print(\"✅ No warnings!\")'")
        else:
            print("\n❌ Setup failed. Please install manually:")
            print(f"   pip install protobuf=={target_python_version}")
            sys.exit(1)
    else:
        print("⏭️  Skipping installation. You can install manually:")
        print(f"   pip install protobuf=={target_python_version}")
        print("Note: You may see protobuf version warnings until versions match.")

if __name__ == "__main__":
    main()
