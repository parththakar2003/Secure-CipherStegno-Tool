"""
Legacy GUI Entry Point
This file is deprecated but kept for backwards compatibility.
It now redirects to the enhanced GUI application (app.py).

For new users, please use: python app.py
"""

import sys
import os

# Add the current directory to path
sys.path.insert(0, os.path.dirname(__file__))

if __name__ == '__main__':
    print("=" * 70)
    print("NOTICE: index.py is deprecated")
    print("=" * 70)
    print("This file is kept for backwards compatibility only.")
    print("Redirecting to the enhanced GUI application (app.py)...")
    print()
    print("For future use, please run: python app.py")
    print("=" * 70)
    print()
    
    # Import and run the enhanced GUI
    try:
        from app import main
        main()
    except Exception as e:
        print(f"Error launching enhanced GUI: {e}")
        print()
        print("Please ensure all dependencies are installed:")
        print("  pip install -r requirements.txt")
        print()
        print("Then run: python app.py")
        sys.exit(1)