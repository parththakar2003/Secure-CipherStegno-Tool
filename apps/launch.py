#!/usr/bin/env python3
"""
Unified Launcher for Secure CipherStegno Tool
Launch GUI or CLI interface
"""

import sys
import os
import argparse

# Check Python version
if sys.version_info < (3, 8):
    sys.stderr.write("ERROR: Python 3.8 or higher is required\n")
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description='Secure CipherStegno Tool - Unified Launcher',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Interface Options:
  gui         Launch graphical user interface (Tkinter)
  cli         Launch command-line interface with arguments
  interactive Launch interactive CLI with menus

Examples:
  python launch.py gui                    # Start GUI
  python launch.py interactive            # Start interactive CLI
  python launch.py cli --help             # Show CLI options
        """
    )

    parser.add_argument(
        'interface',
        choices=['gui', 'cli', 'interactive'],
        help='Interface to launch'
    )

    # Parse known args to allow passing through to subcommands
    args, remaining = parser.parse_known_args()

    # Get the repository root directory (parent of apps/)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    os.chdir(repo_root)

    # Add apps directory to path for imports
    sys.path.insert(0, os.path.join(repo_root, 'apps'))

    if args.interface == 'gui':
        print("🖥️  Launching GUI interface...")
        import app
        app.main()

    elif args.interface == 'cli':
        print("💻 Launching CLI interface...")
        sys.argv = ['cli.py'] + remaining
        import cli
        cli.main()

    elif args.interface == 'interactive':
        print("✨ Launching Interactive CLI...")
        import interactive_cli
        interactive_cli.main()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
