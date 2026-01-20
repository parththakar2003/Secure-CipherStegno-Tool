#!/usr/bin/env python3
"""
Unified Launcher for Secure CipherStegno Tool
Launch GUI, CLI, or Web interface
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
  web         Launch web interface (FastAPI server)

Examples:
  python launch.py gui                    # Start GUI
  python launch.py interactive            # Start interactive CLI
  python launch.py web                    # Start web server on http://localhost:8000
  python launch.py web --port 5000        # Start web server on custom port
  python launch.py cli --help             # Show CLI options
        """
    )
    
    parser.add_argument(
        'interface',
        choices=['gui', 'cli', 'interactive', 'web'],
        help='Interface to launch'
    )
    
    # Web-specific options
    parser.add_argument(
        '--host',
        default='0.0.0.0',
        help='Host for web server (default: 0.0.0.0)'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=8000,
        help='Port for web server (default: 8000)'
    )
    
    # Parse known args to allow passing through to subcommands
    args, remaining = parser.parse_known_args()
    
    # Change to script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    if args.interface == 'gui':
        print("🖥️  Launching GUI interface...")
        import app
        sys.exit(0)
    
    elif args.interface == 'cli':
        print("💻 Launching CLI interface...")
        sys.argv = ['cli.py'] + remaining
        import cli
        sys.exit(0)
    
    elif args.interface == 'interactive':
        print("✨ Launching Interactive CLI...")
        import interactive_cli
        sys.exit(0)
    
    elif args.interface == 'web':
        print(f"🌐 Launching Web interface...")
        print(f"   Server: http://{args.host}:{args.port}")
        print(f"   Documentation: http://{args.host}:{args.port}/api/docs")
        print(f"   Press Ctrl+C to stop")
        
        from src.web.api import run_server
        run_server(host=args.host, port=args.port)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
