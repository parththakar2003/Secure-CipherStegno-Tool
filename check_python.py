#!/usr/bin/env python
"""
Python Version Checker for Secure CipherStegno Tool

This script checks if the current Python version meets the minimum requirements
before attempting to install dependencies.

Minimum Required Version: Python 3.8
"""

import sys

MINIMUM_PYTHON_VERSION = (3, 8)
REQUIRED_VERSION_STR = "3.8"

def check_python_version():
    """Check if the current Python version meets minimum requirements."""
    current_version = sys.version_info[:2]
    
    if current_version < MINIMUM_PYTHON_VERSION:
        print("=" * 70)
        print("ERROR: Python version incompatibility detected!")
        print("=" * 70)
        print(f"\nCurrent Python version: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
        print(f"Required Python version: {REQUIRED_VERSION_STR} or higher")
        print("\nThis tool requires Python 3.8 or higher because:")
        print("  • Pillow >= 10.0.0 requires Python 3.8+")
        print("  • NumPy >= 1.24.0 requires Python 3.8+")
        print("  • Cryptography >= 41.0.0 requires Python 3.7+")
        print("  • FastAPI >= 0.104.0 requires Python 3.8+")
        print("  • Many other dependencies require modern Python versions")
        print("\nTo fix this issue:")
        print("  1. Install Python 3.8 or higher from https://www.python.org/downloads/")
        print("  2. Use a virtual environment: python3 -m venv venv && source venv/bin/activate")
        print("  3. On Ubuntu/Debian: sudo apt-get install python3.8 python3.8-venv")
        print("  4. On macOS with Homebrew: brew install python@3.8")
        print("  5. On Windows: Download from https://www.python.org/downloads/windows/")
        print("\nAfter installing Python 3.8+, use 'python3' or 'python3.8' instead of 'python'")
        print("=" * 70)
        return False
    
    print("✓ Python version check passed")
    print(f"  Using Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    return True

if __name__ == "__main__":
    if not check_python_version():
        sys.exit(1)
    sys.exit(0)
