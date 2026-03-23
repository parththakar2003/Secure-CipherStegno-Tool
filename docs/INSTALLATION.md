# Installation Guide

Complete installation guide for Secure CipherStegno Tool.

## Prerequisites

### Required Software
- **Python 3.8 or higher** (Python 3.12+ recommended)
- **pip** (Python package manager)
- **git** (for cloning the repository)

### Check Your Python Version

```bash
python3 --version
```

If you see a version lower than 3.8, you need to upgrade Python.

## Quick Start (Recommended)

The easiest way to install and run the tool is using the automated setup script.

### Linux/macOS

```bash
# 1. Clone the repository
git clone https://github.com/parththakar2003/Secure-CipherStegno-Tool.git
cd Secure-CipherStegno-Tool

# 2. Run the automated setup
chmod +x setup.sh
./setup.sh

# 3. Activate the virtual environment
source venv/bin/activate

# 4. Run the application
python app.py
```

### Windows

```bash
# 1. Clone the repository
git clone https://github.com/parththakar2003/Secure-CipherStegno-Tool.git
cd Secure-CipherStegno-Tool

# 2. Run the automated setup
setup.bat

# 3. Activate the virtual environment
venv\Scripts\activate.bat

# 4. Run the application
python app.py
```

## Manual Installation

If you prefer to install manually or need more control:

### Step 1: Clone the Repository

```bash
git clone https://github.com/parththakar2003/Secure-CipherStegno-Tool.git
cd Secure-CipherStegno-Tool
```

### Step 2: Verify Python Version

```bash
python3 check_python.py
```

This will check if your Python version meets the minimum requirements.

### Step 3: Create Virtual Environment

**Why use a virtual environment?**
- Isolates project dependencies from system packages
- Required on modern Linux distributions (Kali, Ubuntu 23.04+, etc.)
- Prevents `externally-managed-environment` errors
- Makes dependency management easier

**Create the virtual environment:**

```bash
# Linux/macOS
python3 -m venv venv

# Windows
python -m venv venv
```

### Step 4: Activate Virtual Environment

**Linux/macOS:**
```bash
source venv/bin/activate
```

**Windows (Command Prompt):**
```bash
venv\Scripts\activate.bat
```

**Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

After activation, you should see `(venv)` at the beginning of your command prompt.

### Step 5: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install all required packages:
- Pillow (image processing)
- NumPy (numerical operations)
- PyCryptodome (cryptography)
- Cryptography (additional crypto support)
- SciPy (scientific computing)
- FastAPI & Uvicorn (web API)
- And more...

### Step 6: Verify Installation

```bash
# Test imports
python -c "from src.crypto import CaesarCipher, AESCipher, RSACipher; print('✓ Installation successful')"

# Run the CLI help
python cli.py --help
```

## Running the Application

### GUI Application

```bash
# Make sure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate.bat on Windows

# Run the GUI
python app.py
```

### Command-Line Interface

```bash
# Make sure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate.bat on Windows

# Show help
python cli.py --help

# Example: Encrypt a message
python cli.py encrypt --algorithm aes --input message.txt --output encrypted.bin --password mypassword
```

### Legacy GUI (Simple Interface)

```bash
python index.py
```

## Troubleshooting

### Error: "externally-managed-environment"

**Problem:** Modern Linux distributions (Kali, Ubuntu 23.04+, Fedora 38+) implement PEP 668 which blocks system-wide pip installations.

**Solution:** Use a virtual environment (see Step 3 above).

**Why this happens:**
- Prevents system Python packages from being modified
- Protects system stability
- Recommended best practice for Python development

### Error: "ModuleNotFoundError: No module named 'Crypto'"

**Problem:** Dependencies are not installed or virtual environment is not activated.

**Solutions:**
1. Make sure virtual environment is activated (you should see `(venv)` in your prompt)
2. Install dependencies: `pip install -r requirements.txt`
3. If still failing, recreate the virtual environment:
   ```bash
   rm -rf venv
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

### Error: "Python version too old"

**Problem:** Python version is below 3.8.

**Solutions:**

**Ubuntu/Debian:**
```bash
sudo apt-get update
# Install Python 3.8 or newer (e.g., python3.10, python3.11, python3.12)
sudo apt-get install python3.10 python3.10-venv python3-pip
```

**macOS (with Homebrew):**
```bash
# Install latest Python 3
brew install python3
```

**Windows:**
Download and install Python 3.8 or higher from https://www.python.org/downloads/

### Virtual Environment Not Activating (Linux/macOS)

**Problem:** `activate` command not working.

**Solution:** Use `source` command:
```bash
source venv/bin/activate
```

### Virtual Environment Not Activating (Windows PowerShell)

**Problem:** PowerShell execution policy blocks activation.

**Solution:** Change execution policy (run as Administrator):
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate:
```powershell
venv\Scripts\Activate.ps1
```

### Permission Denied (setup.sh)

**Problem:** Setup script is not executable.

**Solution:**
```bash
chmod +x setup.sh
./setup.sh
```

### Import Errors After Installation

**Problem:** Python can't find the modules.

**Solutions:**
1. Verify you're in the correct directory
2. Make sure virtual environment is activated
3. Reinstall dependencies:
   ```bash
   pip install --force-reinstall -r requirements.txt
   ```

## Deactivating Virtual Environment

When you're done using the tool:

```bash
deactivate
```

This returns you to the system Python environment.

## Updating the Tool

To update to the latest version:

```bash
# Make sure you're in the project directory
cd Secure-CipherStegno-Tool

# Deactivate virtual environment if active
deactivate

# Pull latest changes
git pull origin main

# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate.bat on Windows

# Update dependencies
pip install --upgrade -r requirements.txt
```

## Development Installation

If you want to contribute or modify the tool:

```bash
# Install with development dependencies
pip install -e .
pip install -r requirements.txt
pip install pytest pytest-cov black flake8

# Run tests
python -m pytest tests/

# Run linting
flake8 src/
black --check src/
```

## Platform-Specific Notes

### Kali Linux

Kali Linux enforces PEP 668 strictly. **Always use a virtual environment.**

```bash
# Install python3-venv if not already installed
sudo apt-get install python3-venv

# Create and use virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Ubuntu 23.04+

Same as Kali Linux - virtual environment is required.

### Windows 11

No special requirements. Virtual environment is still recommended for isolation.

### macOS

Works out of the box. Virtual environment is recommended.

## Getting Help

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section above
2. Read the [README.md](../README.md) for overview
3. Check [USAGE.md](USAGE.md) for usage examples
4. Open an issue on GitHub: https://github.com/parththakar2003/Secure-CipherStegno-Tool/issues

## Security Note

- Never install system-wide with `--break-system-packages` flag (this can break system Python dependencies and cause system instability)
- Always use virtual environments for Python projects to isolate dependencies
- Keep dependencies up to date for security patches
- Review code before running if you're concerned about security

## License

This project is licensed under the MIT License - see [LICENSE](../LICENSE) file for details.
