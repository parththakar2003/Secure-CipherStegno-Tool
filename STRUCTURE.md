# Repository Structure

This document describes the organized file and folder structure of the Secure CipherStegno Tool repository.

## 📁 Root Directory Structure

```
Secure-CipherStegno-Tool/
├── 📂 apps/                    # Application entry points
│   ├── app.py                  # GUI application (Tkinter)
│   ├── cli.py                  # Command-line interface
│   ├── demo.py                 # Demo application
│   ├── interactive_cli.py      # Interactive CLI with menus
│   └── launch.py               # Unified launcher (recommended)
│
├── 📂 scripts/                 # Setup and utility scripts
│   ├── setup.py                # Python package setup configuration
│   ├── setup.sh                # Linux/macOS setup script
│   ├── setup.bat               # Windows setup script
│   ├── check_python.py         # Python version checker
│   └── create_abstract_docx.py # Document generator
│
├── 📂 src/                     # Source code modules
│   ├── ai/                     # AI and ML features
│   ├── core/                   # Core business logic
│   ├── crypto/                 # Cryptography implementations
│   ├── steganography/          # Steganography implementations
│   ├── utils/                  # Utility functions
│   └── web/                    # Web interface (FastAPI)
│
├── 📂 docs/                    # Documentation
│   ├── guides/                 # User guides and tutorials
│   │   ├── CLI_GUIDE.md
│   │   ├── CONTRIBUTING.md
│   │   ├── INTERACTIVE_CLI_QUICKSTART.md
│   │   ├── QUICKSTART.md
│   │   ├── QUICK_ACTION_GUIDE.md
│   │   └── TA1_PREPARATION_GUIDE.md
│   │
│   ├── submissions/            # Academic submission documents
│   │   ├── ABSTRACT_SUBMISSION.md
│   │   ├── ABSTRACT_SUBMISSION.docx
│   │   ├── ABSTRACT_SUBMISSION_SUMMARY.md
│   │   ├── ABSTRACT_DOCUMENT_README.md
│   │   ├── IMPLEMENTATION_SUMMARY.md
│   │   ├── INTERFACES.md
│   │   └── PROJECT_REQUIREMENTS_CLARIFICATION.md
│   │
│   └── Technical documentation
│       ├── INSTALLATION.md
│       ├── PROJECT_SUMMARY.md
│       ├── README.md
│       ├── RELEASE_v3.1.0.md
│       ├── ROADMAP.md
│       ├── SUBMISSION_CHECKLIST.md
│       ├── USAGE.md
│       └── WEB_INTERFACE_GUIDE.md
│
├── 📂 tests/                   # Unit tests
│   ├── test_crypto.py
│   ├── test_modern_crypto.py
│   ├── test_operations_crypto.py
│   └── test_utils.py
│
├── 📂 examples/                # Example files and demos
│   ├── README.md
│   └── sample_message.txt
│
├── 📂 mobile/                  # Mobile applications
│   ├── android/                # Android app
│   └── ios/                    # iOS app
│
├── 📄 README.md                # Main project README
├── 📄 CHANGELOG.md             # Version history
├── 📄 LICENSE                  # MIT License
├── 📄 requirements.txt         # Python dependencies
└── 📄 STRUCTURE.md             # This file
```

## 🚀 Quick Start

### Setup

**Linux/macOS:**
```bash
./scripts/setup.sh
source venv/bin/activate
```

**Windows:**
```cmd
scripts\setup.bat
venv\Scripts\activate.bat
```

### Running Applications

**Unified Launcher (Recommended):**
```bash
python apps/launch.py gui          # Launch GUI
python apps/launch.py web          # Launch web interface
python apps/launch.py interactive  # Launch interactive CLI
python apps/launch.py cli --help   # Launch CLI with help
```

**Direct Launch:**
```bash
python apps/app.py                 # GUI application
python apps/interactive_cli.py     # Interactive CLI
python apps/cli.py --help          # Command-line interface
```

## 📚 Documentation Locations

- **Getting Started**: `README.md` (root)
- **Usage Guide**: `docs/USAGE.md`
- **CLI Guide**: `docs/guides/CLI_GUIDE.md`
- **Web Interface**: `docs/WEB_INTERFACE_GUIDE.md`
- **Quick Actions**: `docs/guides/QUICK_ACTION_GUIDE.md`
- **Contributing**: `docs/guides/CONTRIBUTING.md`

## 🎯 Organization Benefits

### Before Organization
- 28+ files in root directory
- Mixed application code, scripts, and documentation
- Difficult to navigate and find files
- Unclear project structure

### After Organization
- Only 4 essential files in root (README, CHANGELOG, LICENSE, requirements.txt)
- Clear separation of concerns:
  - `apps/` - All user-facing applications
  - `scripts/` - Setup and utility scripts
  - `docs/` - Organized documentation
  - `src/` - Core source code (unchanged)
  - `tests/` - Unit tests (unchanged)
- Easy navigation and maintenance
- Professional structure following best practices

## 🔄 Migration Notes

If you have bookmarks or scripts referencing old paths, update them as follows:

| Old Path | New Path |
|----------|----------|
| `app.py` | `apps/app.py` |
| `cli.py` | `apps/cli.py` |
| `launch.py` | `apps/launch.py` |
| `interactive_cli.py` | `apps/interactive_cli.py` |
| `demo.py` | `apps/demo.py` |
| `setup.py` | `scripts/setup.py` |
| `setup.sh` | `scripts/setup.sh` |
| `setup.bat` | `scripts/setup.bat` |
| `check_python.py` | `scripts/check_python.py` |
| `create_abstract_docx.py` | `scripts/create_abstract_docx.py` |
| `CLI_GUIDE.md` | `docs/guides/CLI_GUIDE.md` |
| `CONTRIBUTING.md` | `docs/guides/CONTRIBUTING.md` |
| `QUICKSTART.md` | `docs/guides/QUICKSTART.md` |
| `ABSTRACT_SUBMISSION.md` | `docs/submissions/ABSTRACT_SUBMISSION.md` |

## 💡 Best Practices

1. **Always use the unified launcher** (`apps/launch.py`) for the best experience
2. **Activate virtual environment** before running any scripts
3. **Refer to `docs/`** for comprehensive guides
4. **Check `examples/`** for sample usage

## 🤝 Contributing

See `docs/guides/CONTRIBUTING.md` for contribution guidelines.

## 📝 License

This project is licensed under the MIT License - see the `LICENSE` file for details.
