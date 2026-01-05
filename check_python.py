#!/usr/bin/env python
"""
Python Version Checker for Secure CipherStegno Tool

This script checks if the current Python version meets the minimum requirements
before attempting to install dependencies.

Minimum Required Version: Python 3.8
"""

import sys
import os

MINIMUM_PYTHON_VERSION = (3, 8)
REQUIRED_VERSION_STR = "3.8"

def is_virtual_environment():
    """Check if we're running inside a virtual environment."""
    return (hasattr(sys, 'real_prefix') or
            (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))

def check_python_version():
    """Check if the current Python version meets minimum requirements."""
    current_version = sys.version_info[:2]
    
    if current_version < MINIMUM_PYTHON_VERSION:
        print("=" * 70)
        print("ERROR: Python version incompatibility detected!")
        print("=" * 70)
        print("\nCurrent Python version: {0}.{1}.{2}".format(
            sys.version_info[0], sys.version_info[1], sys.version_info[2]))
        print("Required Python version: {0} or higher".format(REQUIRED_VERSION_STR))
        print("\nThis tool requires Python 3.8 or higher because:")
        print("  • Pillow >= 10.0.0 requires Python 3.8+")
        print("  • NumPy >= 1.24.0 requires Python 3.8+")
        print("  • Cryptography >= 41.0.0 requires Python 3.7+")
        print("  • FastAPI >= 0.104.0 requires Python 3.8+")
        print("  • Many other dependencies require modern Python versions")
        print("\nTo fix this issue:")
        print("  1. Install Python 3.8 or higher from https://www.python.org/downloads/")
        print("  2. On Ubuntu/Debian: sudo apt-get install python3.8 python3.8-venv")
        print("  3. On macOS with Homebrew: brew install python@3.8")
        print("  4. On Windows: Download from https://www.python.org/downloads/windows/")
        print("\nAfter installing Python 3.8+:")
        print("  • Use 'python3' or 'python3.8' instead of 'python'")
        print("  • Create a virtual environment: python3 -m venv venv")
        print("  • Activate it: source venv/bin/activate (Linux/macOS) or venv\\Scripts\\activate.bat (Windows)")
        print("  • Install dependencies: pip install -r requirements.txt")
        print("=" * 70)
        return False
    
    print("✓ Python version check passed")
    print("  Using Python {0}.{1}.{2}".format(
        sys.version_info[0], sys.version_info[1], sys.version_info[2]))
    
    # Check if in virtual environment
    if is_virtual_environment():
        print("✓ Running inside virtual environment")
    else:
        print("\n⚠️  WARNING: Not running in a virtual environment")
        print("  Modern systems (Kali Linux, Ubuntu 23.04+) block system-wide pip installs.")
        print("  It is HIGHLY RECOMMENDED to use a virtual environment:")
        print("    1. Create: python3 -m venv venv")
        print("    2. Activate: source venv/bin/activate (Linux/macOS)")
        print("                 venv\\Scripts\\activate.bat (Windows)")
        print("    3. Install: pip install -r requirements.txt")
    
    return True

if __name__ == "__main__":
    if not check_python_version():
        sys.exit(1)
    sys.exit(0)

