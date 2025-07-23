#!/usr/bin/env python3
"""
VultiTool Wrapper Script
Automatically uses the virtual environment if available, otherwise falls back to system Python.
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    # Get the directory containing this script
    script_dir = Path(__file__).parent.absolute()
    
    # Check if virtual environment exists
    venv_python = script_dir / "venv" / "bin" / "python3"
    main_script = script_dir / "vultitool.py"
    
    if venv_python.exists() and main_script.exists():
        # Use virtual environment Python
        cmd = [str(venv_python), str(main_script)] + sys.argv[1:]
    else:
        # Fall back to system Python
        cmd = [sys.executable, str(main_script)] + sys.argv[1:]
    
    # Execute the main script
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)
    except FileNotFoundError:
        print(f"Error: Could not find vultitool.py in {script_dir}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
