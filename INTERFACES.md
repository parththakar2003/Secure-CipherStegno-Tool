# Available Interfaces

Secure CipherStegno Tool provides **4 different interfaces** to suit your workflow preferences:

## 🚀 Quick Start

After running `./setup.sh`, activate the virtual environment:
```bash
source venv/bin/activate
```

## 📱 1. Unified Launcher (Recommended)

The easiest way to launch any interface:

```bash
# Launch GUI
python launch.py gui

# Launch Interactive CLI
python launch.py interactive

# Launch Web Interface
python launch.py web

# Launch Command-line Interface
python launch.py cli --help
```

### Web Interface Options
```bash
# Custom port
python launch.py web --port 5000

# Custom host and port
python launch.py web --host 127.0.0.1 --port 8080
```

## 🖥️ 2. GUI Interface (Tkinter)

**Desktop application with graphical interface**

```bash
python app.py
```

**Features:**
- Modern tabbed interface
- Cryptography tab (9 algorithms: Caesar, Vigenère, Playfair, Rail Fence, AES-256, Blowfish, 3DES, ChaCha20, RSA)
- Steganography tab (Image, Audio, Video)
- Security Tools (Password generator, validator, file hash, integrity checker)
- Visual feedback and error handling

**Note:** Requires Tkinter (GUI library)
- **Windows/macOS:** Included with Python by default
- **Linux:**
  - Ubuntu/Debian: `sudo apt-get install python3-tk`
  - Fedora/RHEL: `sudo dnf install python3-tkinter`
  - Arch: `sudo pacman -S tk`
  - openSUSE: `sudo zypper install python3-tk`

## 💻 3. Command-Line Interface (CLI)

**Scriptable command-line interface for automation**

```bash
python cli.py --help
```

**Common Commands:**

```bash
# Encrypt text with AES
python cli.py encrypt --algorithm aes --input message.txt --output encrypted.bin --password mypass

# Decrypt text
python cli.py decrypt --algorithm aes --input encrypted.bin --password mypass

# Hide message in image
python cli.py stego-encode --type image --cover photo.png --message secret.txt --output stego.png

# Extract message from image
python cli.py stego-decode --type image --input stego.png

# Generate RSA keys
python cli.py generate-keys --algorithm rsa --output-dir ./keys

# Calculate file hash
python cli.py hash --file document.pdf --algorithm sha256

# Generate strong password
python cli.py generate-password --length 20

# Validate password strength
python cli.py validate-password
```

**Perfect for:**
- Batch processing
- Automation scripts
- CI/CD pipelines
- Remote servers (no GUI needed)

## ✨ 4. Interactive CLI

**Menu-driven interface with step-by-step guidance**

```bash
python interactive_cli.py
```

**Features:**
- Beautiful ASCII art interface
- Guided workflows
- Real-time feedback
- No need to remember commands
- Perfect for learning and exploration

**Menu Categories:**
1. Cryptography (Encrypt/Decrypt)
2. Steganography (Hide/Extract)
3. Security Tools
4. Key Management
5. Help & Documentation

## 🌐 5. Web Interface (FastAPI)

**Modern web-based REST API with interactive documentation**

```bash
python src/web/api.py
# or
python launch.py web
```

**Access Points:**
- Main Interface: http://localhost:8000
- API Documentation: http://localhost:8000/api/docs
- Alternative Docs: http://localhost:8000/api/redoc

**Features:**
- RESTful API endpoints
- Interactive Swagger UI documentation
- Web-based GUI
- CORS support for local development
- File upload/download support
- Token-based authentication (demo)

**API Endpoints:**
- `/api/v1/encrypt` - Text encryption
- `/api/v1/decrypt` - Text decryption
- `/api/v1/stego/encode` - Hide messages
- `/api/v1/stego/decode` - Extract messages
- `/api/v1/password/validate` - Validate passwords
- `/api/v1/password/generate` - Generate passwords
- `/api/v1/hash` - Calculate hashes

**Perfect for:**
- Web application integration
- Mobile app backends
- API consumers
- Remote access
- Microservices architecture

## 🔄 Interface Comparison

Choose the best interface for your needs:

| Interface | Best For | GUI | Automation | Learning Curve |
|-----------|----------|-----|------------|----------------|
| **GUI (app.py)** | Desktop users | ✅ | ❌ | ⭐ Easy |
| **CLI (cli.py)** | Scripts & automation | ❌ | ✅ | ⭐⭐⭐ Medium |
| **Interactive CLI** | Learning & exploration | ✅ | ❌ | ⭐ Easy |
| **Web API** | Integration & remote | ✅ | ✅ | ⭐⭐⭐ Medium |

**Note:** Use `launch.py` as a convenient launcher for any of the above interfaces.

## 🎯 Recommendations

**First-time users:** Start with `python launch.py interactive` or `python launch.py gui`

**Automation/Scripts:** Use `python cli.py` with command-line arguments

**Web developers:** Use `python launch.py web` for REST API access

**System administrators:** Use CLI for batch operations and cron jobs

**API integration:** Use Web interface for microservices and mobile apps

## 📝 Notes

- All interfaces use the same core cryptography and steganography modules
- Security features are consistent across all interfaces
- Local-only processing - no data sent to external servers
- All interfaces support the same algorithms and features

## 🆘 Troubleshooting

**GUI won't start:**
- Install Tkinter: `sudo apt-get install python3-tk` (Linux)
- Use alternative interface: `python launch.py interactive`

**Web interface port already in use:**
- Use custom port: `python launch.py web --port 8080`

**Permission errors:**
- Ensure virtual environment is activated: `source venv/bin/activate`

## 📚 More Information

- See `README.md` for full feature list
- See `QUICKSTART.md` for quick setup guide
- See `cli.py --help` for CLI command reference
- See http://localhost:8000/api/docs for API documentation (when web server is running)
