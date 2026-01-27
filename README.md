# 🔐 Secure CipherStegno Tool

**Version 3.1.0** - Enterprise-Grade Security Platform

**Secure CipherStegno Tool** is a comprehensive professional security platform that combines advanced **cryptography**, **steganography**, **AI-based analysis**, and **cloud services** to provide enterprise-grade security solutions — all with privacy-first, local-first processing capabilities.

---

## 🎓 IMPORTANT: Major Project Requirements (Updated January 2026)

**🚨 URGENT: Abstract submission TODAY by 1:00 PM for guide allocation!**

**📋 For students - Start here:**
- **[QUICK_ACTION_GUIDE.md](docs/guides/QUICK_ACTION_GUIDE.md)** — ⚡ **START HERE**: Quick reference for what to do NOW (5-min read)

**📚 Detailed Documentation:**
- **[PROJECT_REQUIREMENTS_CLARIFICATION.md](docs/submissions/PROJECT_REQUIREMENTS_CLARIFICATION.md)** — **MUST READ**: Critical guidelines on research requirements, existing implementations, new contributions, and guide allocation
- **[TA1_PREPARATION_GUIDE.md](docs/guides/TA1_PREPARATION_GUIDE.md)** — Complete preparation guide for TA-1 evaluation (February 2026)
- **[ABSTRACT_SUBMISSION.md](docs/submissions/ABSTRACT_SUBMISSION.md)** — Updated abstract template with existing work vs. new contributions clearly documented

**⚠️ Key Requirements:**
1. ✅ Project must be **practical + research-focused** (both required)
2. ✅ Must clearly explain **existing implementations** in the domain
3. ✅ Must clearly state **your new work and improvements**
4. ✅ Must show how **new work matches project objectives**
5. ✅ Deadline: Submit title and abstract TODAY by 1:00 PM for guide allocation

---

![License](https://img.shields.io/github/license/parththakar2003/Secure-CipherStegno-Tool?style=for-the-badge)
![Stars](https://img.shields.io/github/stars/parththakar2003/Secure-CipherStegno-Tool?style=for-the-badge)
![Forks](https://img.shields.io/github/forks/parththakar2003/Secure-CipherStegno-Tool?style=for-the-badge)
![Issues](https://img.shields.io/github/issues/parththakar2003/Secure-CipherStegno-Tool?style=for-the-badge)
![Pull Requests](https://img.shields.io/github/issues-pr/parththakar2003/Secure-CipherStegno-Tool?style=for-the-badge)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![GUI](https://img.shields.io/badge/GUI-Tkinter-red?style=for-the-badge)
![Crypto](https://img.shields.io/badge/Cryptography-AES%20%7C%20RSA-darkgreen?style=for-the-badge)
![Steganography](https://img.shields.io/badge/Steganography-Image%20%7C%20Audio-purple?style=for-the-badge)
![Privacy](https://img.shields.io/badge/Privacy-Local%20Only-black?style=for-the-badge)

![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey?style=for-the-badge)
![Security](https://img.shields.io/badge/Focus-Cybersecurity-critical?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active%20Development-success?style=for-the-badge)

[![Deploy on Railway](https://img.shields.io/badge/Deploy%20on-Railway-6C4FBB?style=for-the-badge&logo=railway&logoColor=white)](https://railway.app/new/template)
[![Deploy to Render](https://img.shields.io/badge/Deploy%20to-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://render.com/deploy)
[![Docker](https://img.shields.io/badge/Deploy%20with-Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://hub.docker.com/)

> 🌐 **Want to publish the web version?** See [QUICK_DEPLOY.md](QUICK_DEPLOY.md) for 5-minute deployment guide!


---

## 📌 Features

### Cryptography
#### Classical Ciphers
- 🔐 **Caesar Cipher** — Simple substitution cipher for basic encryption
- 🔤 **Vigenère Cipher** — Polyalphabetic substitution cipher with keyword
- 🎲 **Playfair Cipher** — Digraph substitution cipher (5x5 matrix)
- 🚂 **Rail Fence Cipher** — Transposition cipher with zigzag pattern

#### Modern Symmetric Encryption
- 🔒 **AES-256** — Industry-standard symmetric encryption (Recommended)
- ⚡ **Blowfish** — Fast block cipher by Bruce Schneier
- 🔐 **3DES (Triple DES)** — Legacy encryption (backwards compatibility)
- 🚀 **ChaCha20** — Modern stream cipher (Google, mobile-optimized)

#### Asymmetric Encryption
- 🔑 **RSA** — Public key cryptography (2048/4096 bit)
- 🔐 **Hybrid Encryption** — Combine AES and RSA for optimal security

#### Key Management
- 🔑 **Key Generation** — Generate secure cryptographic keys
- 💾 **Key Storage** — Safe key management and storage
- 🔄 **Key Exchange** — Secure key distribution protocols

### Steganography
- 🖼️ **Image Steganography** — Hide messages in PNG/BMP/JPEG images using LSB technique
- 🎵 **Audio Steganography** — Embed secrets in WAV audio files
- 🎬 **Video Steganography** — Hide data in MP4/AVI video frames (NEW!)
- 🗜️ **Compression Support** — Compress messages before hiding for larger capacity
- 📊 **Capacity Analysis** — Check how much data can be hidden in cover files
- 🔧 **Advanced LSB** — Configurable bits-per-channel for balance between capacity and quality

### Security Tools
#### Password Security
- ✅ **Password Validator** — Analyze password strength with detailed feedback
- 🔄 **Password Generator** — Create cryptographically secure passwords

#### Hash & Integrity
- #️⃣ **Hash Calculator** — MD5, SHA-1, SHA-256, SHA-512 support
- 🔍 **File Integrity Verification** — Verify files haven't been tampered with
- 🗑️ **Secure File Deletion** — Overwrite files before deletion

#### Advanced Security Tools (NEW!)
- 📊 **Encryption Analyzer** — Compare and analyze algorithm strengths
- 🔐 **Token Generator** — Generate secure API keys and session tokens
- 🌐 **Port Scanner** — Basic network security scanning (localhost)
- 🧹 **Data Sanitizer** — Sanitize filenames and user inputs
- ⛓️ **Hash Chain** — Create verifiable data integrity chains

### User Interface
- 🖥️ **Modern GUI** — Intuitive Tkinter interface with professional design
- 🌐 **Web Interface** — Full-featured web-based interface with FastAPI backend (NEW!)
- 🎨 **Interactive CLI** — Beautiful ANSI art-based command-line interface with no code to type (ENHANCED!)
- 🌈 **Colorful Menus** — Enhanced visual experience with animations and smart prompts
- ⚡ **Progress Indicators** — Real-time feedback with spinners and progress bars
- ⌨️ **CLI Support** — Full-featured command-line interface with arguments for automation
- 🔄 **Synchronized Interfaces** — All interfaces (GUI, Web, CLI) use the same core operations
- 📖 **Comprehensive Documentation** — Usage guides, CLI guide (docs/guides/CLI_GUIDE.md), and examples
- 🧪 **Unit Tests** — Tested cryptography and utility functions
- 📂 **Local-first execution** — No cloud storage or tracking

---

## 🚀 Demo

> 📥 Download: [Releases](https://github.com/parththakar004/Secure-CipherStegno-Tool)

---

## 🎯 How It Works

1. **Encrypt** your message with a passphrase/key.
2. Choose a **cover file** (image or audio).
3. The tool embeds the encrypted message inside the cover.
4. Share the file safely — only those with the correct key can extract it.

---

## 💡 Why Screenpipe Track?

This tool aligns perfectly with the **Screenpipe** mission of **privacy-first, local-only, AI-ready development**. Our steganography engine runs entirely on the local machine, leveraging Screenpipe’s strengths in local processing, screen/audio capture, and context-aware interaction — all without relying on the cloud.

---

## 🛠️ Tech Stack

### Core Technologies
- **Python 3.8+** — Main programming language
- **Tkinter** — Modern GUI interface
- **FastAPI** — Web interface and REST API (NEW!)
- **Uvicorn** — ASGI server for web interface
- **Jinja2** — HTML templating for web interface
- **PyCryptodome** — Cryptographic operations (AES, RSA)
- **Pillow (PIL)** — Image processing and steganography
- **NumPy** — Efficient array operations
- **Wave** — Audio file processing

### Additional Libraries
- **Colorama** — CLI color output
- **SciPy** — Advanced audio processing
- **zlib** — Data compression
- **hashlib** — File integrity verification

### Project Structure

**📁 Organized folder structure** - See [STRUCTURE.md](STRUCTURE.md) for detailed documentation

```
Secure-CipherStegno-Tool/
├── apps/                # Application entry points
│   ├── launch.py        # Unified launcher (recommended)
│   ├── app.py           # GUI application
│   ├── cli.py           # Command-line interface
│   └── interactive_cli.py  # Interactive CLI
├── scripts/             # Setup and utility scripts
│   ├── setup.sh         # Linux/macOS setup
│   ├── setup.bat        # Windows setup
│   └── check_python.py  # Python version checker
├── src/                 # Source code modules
│   ├── core/            # Shared core operations
│   ├── crypto/          # Cryptography modules
│   ├── steganography/   # Steganography implementations
│   ├── utils/           # Security and file utilities
│   └── web/             # Web interface and API
│       ├── api.py       # FastAPI backend
│       ├── static/      # CSS and JavaScript
│       └── templates/   # HTML templates
├── docs/                # Documentation
│   ├── guides/          # User guides and tutorials
│   └── submissions/     # Academic submission documents
├── tests/               # Unit tests
├── examples/            # Sample files and usage examples
├── mobile/              # Mobile applications
└── requirements.txt     # Python dependencies
```

---

## 📷 Screenshots


---

## 🧪 Installation & Usage

### Prerequisites

**⚠️ IMPORTANT: Python 3.8 or higher is required**

This tool requires **Python 3.8+** because modern cryptography and steganography libraries need it. Python 2.7 and older Python 3 versions are **not supported**.

```bash
# Check your Python version (must be 3.8 or higher)
python --version
# or
python3 --version

# If you have Python 2.7, you MUST upgrade to Python 3.8+
# Visit: https://www.python.org/downloads/
```

If you see a Python 2.7 version, use `python3` instead of `python` for all commands, or install Python 3.8+ from [python.org](https://www.python.org/downloads/).

### Quick Start

#### Automated Setup (Recommended)

The easiest way to get started is using the automated setup script:

**Linux/macOS:**
```bash
# Clone the repository
git clone https://github.com/parththakar2003/Secure-CipherStegno-Tool.git
cd Secure-CipherStegno-Tool

# Run the setup script (creates virtual environment and installs dependencies)
chmod +x scripts/setup.sh
./scripts/setup.sh

# Activate the virtual environment
source venv/bin/activate

# Run the application
python apps/app.py
```

**Windows:**
```bash
# Clone the repository
git clone https://github.com/parththakar2003/Secure-CipherStegno-Tool.git
cd Secure-CipherStegno-Tool

# Run the setup script (creates virtual environment and installs dependencies)
scripts\setup.bat

# Activate the virtual environment
venv\Scripts\activate.bat

# Run the application
python apps\app.py
```

#### Manual Setup

If you prefer to set up manually or the automated script doesn't work:

```bash
# Clone the repository
git clone https://github.com/parththakar2003/Secure-CipherStegno-Tool.git
cd Secure-CipherStegno-Tool

# STEP 1: Verify Python version (REQUIRED: 3.8+)
# This is the MOST IMPORTANT step - the tool will not work with Python 2.7!
python3 scripts/check_python.py

# If you see an error, you need to install Python 3.8 or higher:
# - Visit: https://www.python.org/downloads/
# - On Ubuntu/Debian: sudo apt-get install python3.8 python3.8-venv
# - On macOS: brew install python@3.8
# - Always use 'python3' command instead of 'python'

# STEP 2: Create a virtual environment (HIGHLY RECOMMENDED)
# This avoids "externally-managed-environment" errors on modern systems
python3 -m venv venv

# STEP 3: Activate the virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate.bat

# STEP 4: Install dependencies
pip install -r requirements.txt

# STEP 5: Run the application
# Unified Launcher (Recommended - NEW!)
python apps/launch.py gui          # Launch GUI interface
python apps/launch.py web          # Launch web interface (http://localhost:8000)
python apps/launch.py interactive  # Launch interactive CLI
python apps/launch.py cli --help   # Traditional CLI with arguments

# Or run interfaces directly:
# Option 1: Enhanced GUI application
python apps/app.py

# Option 2: Web Interface (NEW!)
python -m uvicorn src.web.api:app --host 0.0.0.0 --port 8000
# Then open browser to http://localhost:8000

# Option 3: Interactive CLI with beautiful menus and ANSI art
python apps/interactive_cli.py

# Option 4: Traditional command-line interface
python apps/cli.py --help
```

**Important Notes:**
- ⚠️ **Virtual environment is strongly recommended** to avoid conflicts with system packages
- On modern Linux distributions (Kali, Ubuntu 23.04+), direct system-wide installation is blocked by PEP 668
- If you see `externally-managed-environment` error, you **must** use a virtual environment
- Always activate the virtual environment before running the application

### Application Modes

#### 1. GUI Application (Tkinter)

The enhanced GUI provides a modern, user-friendly interface with three main tabs:

1. **Cryptography** — Multiple encryption algorithms (Caesar, Vigenère, AES, RSA, Blowfish, ChaCha20)
2. **Steganography** — Image, audio, and video steganography
3. **Security Tools** — Password tools, hash calculator, file verification

```bash
python3 apps/launch.py gui
# or
python3 apps/app.py
```

#### 2. Web Interface (NEW! 🌐)

Full-featured web-based interface with modern design:
- 🎨 Responsive, modern UI with tabs
- 🔒 All cryptography algorithms supported
- 🖼️ Image and audio steganography
- 🛡️ Security tools (password validator, generator, hash calculator)
- 📱 Mobile-friendly design
- ⚡ Real-time operations with loading indicators

```bash
python3 apps/launch.py web --port 8000
# or
python3 -m uvicorn src.web.api:app --host 0.0.0.0 --port 8000
```

Then open your browser to `http://localhost:8000`

**Features:**
- Synchronized with GUI and CLI - same core operations
- RESTful API at `/api/docs` for programmatic access
- No page reloads needed
- Privacy-first: all processing happens server-side, no data sent to cloud

**🌐 Deploy to the Web:**
Want to publish this web interface online? See [DEPLOYMENT.md](DEPLOYMENT.md) for step-by-step guides to deploy on:
- **Railway** (easiest, free tier available)
- **Render** (reliable, automatic deploys)
- **Docker** (self-hosting)
- **Vercel** (serverless with global CDN)
- **Heroku** (traditional PaaS)

#### 3. Interactive CLI (🎨 No Code to Type!)

**Best for:** Beginners, visual learners, and anyone who prefers menus over commands

Beautiful terminal interface with:
- 🎨 Colorful ANSI art banners
- 📱 Easy-to-use menu navigation (just enter numbers!)
- ⚡ Loading animations and progress bars
- 🎯 Interactive prompts and confirmations
- 🌈 Visual feedback with colors and icons
- 💡 Built-in help and getting started guide
- 📁 Automatic file detection and save prompts
- ✨ No commands to memorize - just follow the menus!

```bash
python3 launch.py interactive
# or
python3 interactive_cli.py
```

**Features:**
- Visual menu-based navigation (no typing commands!)
- All cryptography algorithms with helpful descriptions
- Step-by-step guided workflows
- Real-time encryption/decryption with previews
- Algorithm comparison tool
- Password strength analysis with recommendations
- Network security scanning
- Token generation
- File input/output with smart detection
- Comprehensive help system with tutorials

**Perfect for:**
- First-time users learning the tool
- Quick operations without remembering syntax
- Interactive exploration of features
- Visual feedback and guidance

#### 4. Traditional CLI (⚡ Power User Mode)

**Best for:** Automation, scripting, CI/CD, and power users

Command-line interface for automation and scripting:

```bash
python3 launch.py cli --help
# or
python3 cli.py --help
```

**Features:**
- All operations accessible via command arguments
- Perfect for shell scripts and automation
- Batch processing support
- CI/CD pipeline integration
- Consistent, predictable output for parsing
- Non-interactive mode for scripts

**Perfect for:**
- Automating encryption/decryption workflows
- Batch processing multiple files
- Integration with other tools and scripts
- CI/CD pipelines and automated testing
- Remote server operations via SSH

### CLI Modes Comparison

| Feature | Interactive CLI | Traditional CLI |
|---------|----------------|-----------------|
| **Learning Curve** | ⭐ Easy - No commands to learn | ⭐⭐ Moderate - Need to know commands |
| **Best For** | Beginners, exploration | Automation, scripting |
| **Interface** | Menu-based (select numbers) | Command arguments |
| **Guidance** | Built-in help & tutorials | Man-page style help |
| **File Handling** | Smart detection & prompts | Explicit paths required |
| **Visual Feedback** | Colors, animations, progress | Plain text output |
| **Automation** | Manual operation only | Full automation support |
| **Speed** | Multiple steps per operation | Single command execution |

**📖 For detailed CLI documentation, see [CLI_GUIDE.md](CLI_GUIDE.md)**

### CLI Usage Examples

#### Interactive CLI Example
```bash
# Start interactive CLI
python3 interactive_cli.py

# Then simply:
# 1. Select "Cryptography" (enter: 1)
# 2. Select "Encrypt Message" (enter: 1)
# 3. Select "AES-256" (enter: 6)
# 4. Enter your message or file path
# 5. Enter password
# 6. Choose to save to file
# Done! ✨
```

#### Traditional CLI Examples

##### Encrypt with AES
```bash
python3 cli.py encrypt --algorithm aes --input message.txt --output encrypted.json --password "strongpassword"
```

##### Hide message in image
```bash
python3 cli.py stego-encode --type image --cover photo.png --message secret.txt --output stego.png --compress
```

##### Generate RSA keys
```bash
python3 cli.py generate-keys --algorithm rsa --output-dir ./keys
```

##### Calculate file hash
```bash
python3 cli.py hash --input document.pdf --algorithm sha256
```

##### Decrypt with RSA
```bash
python3 cli.py decrypt --algorithm rsa --input encrypted.txt --output decrypted.txt --key ./keys/private_key.pem
```

**📖 For more examples and detailed usage, see:**
- **Interactive CLI:** Start with `python3 interactive_cli.py` and explore the built-in help
- **Traditional CLI:** See [CLI_GUIDE.md](CLI_GUIDE.md) for comprehensive documentation
- **General Usage:** See [docs/USAGE.md](docs/USAGE.md)

### Running Tests

```bash
# Activate virtual environment first
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate.bat  # Windows

# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_crypto.py

# Or use unittest
python -m unittest discover tests/
```

### Troubleshooting

#### "externally-managed-environment" Error

If you see this error when trying to install packages:
```
error: externally-managed-environment

× This environment is externally managed
```

**Solution:** Use a virtual environment (required on modern Linux distributions):
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate.bat  # Windows

# Install dependencies
pip install -r requirements.txt
```

This error occurs on Kali Linux, Ubuntu 23.04+, and other modern distributions that implement PEP 668 to protect system Python packages.

#### "ModuleNotFoundError: No module named 'Crypto'"

This means dependencies are not installed. Make sure you:
1. Created and activated a virtual environment
2. Ran `pip install -r requirements.txt`
3. Are running the application with the virtual environment activated

#### Python Version Issues

If you see Python version errors:
```bash
# Check your Python version (must be 3.8+)
python3 --version

# Run the version checker
python3 check_python.py
```

If your version is too old:
- **Ubuntu/Debian:** `sudo apt-get install python3.8 python3.8-venv`
- **macOS:** `brew install python@3.8`
- **Windows:** Download from https://www.python.org/downloads/

#### Virtual Environment Not Activating

**Linux/macOS:**
```bash
# Make sure you use 'source'
source venv/bin/activate

# You should see (venv) in your prompt
(venv) user@machine:~$
```

**Windows:**
```bash
# Use the full path
venv\Scripts\activate.bat

# You should see (venv) in your prompt
(venv) C:\path\to\project>
```

## 🧪 Coming Soon...

### Planned Features

#### Cryptography Enhancements
- 🔐 **Vigenère Cipher** — Classical polyalphabetic substitution cipher
- 🔑 **Extended RSA Support** — 4096-bit keys and advanced RSA operations
- 🔒 **Additional Algorithms** — Blowfish, Twofish, and other modern ciphers
- 🔐 **Quantum-resistant cryptography** — Post-quantum algorithms (Lattice-based, hash-based)

#### Steganography Expansions
- 🎬 **Video Steganography** — Hide data in MP4, AVI, and other video formats
- 🎵 **Advanced Audio Formats** — Support for MP3, FLAC, OGG steganography
- 📄 **Document Steganography** — Hide data in PDF, DOCX, and text files
- 🖼️ **JPEG Steganography** — DCT coefficient manipulation for lossy formats
- 📊 **Multi-layer Steganography** — Hide multiple messages at different levels

#### AI & Machine Learning
- 🧠 **ML-based Steganalysis** — Detect tampering and unauthorized access in images
- 🔍 **Anomaly Detection** — Identify suspicious patterns in stego files
- 🤖 **Neural Network Steganography** — Use deep learning for advanced hiding techniques
- 📈 **Statistical Analysis** — Chi-square and histogram analysis for stego detection
- 🛡️ **Security Scoring** — AI-powered assessment of steganographic security

#### Cloud & Collaboration
- 🌍 **Cloud-based Version** — Web platform for remote access
- 👥 **Multi-user Collaboration** — Secure sharing and team features
- 🔄 **Sync Capabilities** — Cross-device synchronization with end-to-end encryption
- 📱 **Real-time Collaboration** — Live encryption/decryption sessions
- 🔐 **Secure Key Exchange** — Automated key distribution system

#### Additional Features
- 🔄 **Batch Processing** — Process multiple files simultaneously
- 📱 **Mobile Applications** — Android/iOS companion apps
- 🔐 **Hardware Security Module (HSM)** — Integration for enterprise security
- 📊 **Analytics Dashboard** — Usage statistics and security metrics
- 🌐 **API Gateway** — RESTful API for integration with other applications

### Development Roadmap

#### Phase 1: Enhanced Cryptography (v2.1)
- ✅ Caesar Cipher (Completed)
- ✅ AES-256 (Completed)
- ✅ RSA-2048 (Completed)
- 🔲 Vigenère Cipher
- 🔲 Extended encryption algorithms (Blowfish, Twofish)
- 🔲 4096-bit RSA support

#### Phase 2: Advanced Steganography (v2.2)
- ✅ Image Steganography (PNG/BMP) (Completed)
- ✅ Audio Steganography (WAV) (Completed)
- 🔲 Video steganography (MP4, AVI)
- 🔲 MP3 audio steganography
- 🔲 JPEG steganography
- 🔲 Document steganography (PDF, DOCX)

#### Phase 3: AI & Security (v2.3)
- 🔲 Machine learning steganalysis
- 🔲 Tampering detection system
- 🔲 Unauthorized access detection
- 🔲 Neural network-based steganography
- 🔲 Statistical analysis tools

#### Phase 4: Cloud Platform (v3.0)
- 🔲 Web-based interface (Flask/FastAPI + React)
- 🔲 Cloud deployment (AWS/Azure/GCP)
- 🔲 Multi-user support with authentication
- 🔲 Secure key exchange protocol
- 🔲 End-to-end encryption for cloud storage
- 🔲 RESTful API with OAuth2

#### Phase 5: Enterprise & Mobile (v3.1)
- 🔲 Mobile applications (iOS/Android)
- 🔲 Hardware security module integration
- 🔲 Enterprise features (LDAP, SSO)
- 🔲 Compliance reporting (GDPR, HIPAA)
- 🔲 Audit logging and monitoring

### Legend
- ✅ Completed
- 🔲 Planned
- 🚧 In Progress

---

## 🌐 Web Deployment

Want to publish the web interface online? The Secure CipherStegno Tool can be deployed to various cloud platforms with ease!

### Quick Deploy Options

Choose your preferred platform for one-click deployment:

| Platform | Free Tier | Setup Time | Best For |
|----------|-----------|------------|----------|
| **Railway** | ✅ Yes | 5 minutes | Easiest deployment |
| **Render** | ✅ Yes | 10 minutes | Reliable hosting |
| **Docker** | N/A | 15 minutes | Self-hosting |
| **Vercel** | ✅ Yes | 10 minutes | Global CDN |

### Deployment Files Included

All necessary configuration files are included in the repository:

- 📄 `Dockerfile` - Container deployment for Docker, Railway, Render
- 📄 `railway.json` - Railway configuration
- 📄 `render.yaml` - Render.com Blueprint
- 📄 `vercel.json` - Vercel serverless configuration
- 📄 `Procfile` - Heroku deployment
- 📄 `runtime.txt` - Python version specification
- 📄 `.env.example` - Environment variables template

### Step-by-Step Guides

For detailed deployment instructions for each platform, see **[DEPLOYMENT.md](DEPLOYMENT.md)**.

The deployment guide includes:
- ✅ Platform-specific setup instructions
- ✅ Environment configuration
- ✅ Security best practices
- ✅ Troubleshooting tips
- ✅ Custom domain setup
- ✅ SSL/HTTPS configuration

### Quick Start - Railway (Recommended)

The fastest way to deploy:

1. Fork this repository to your GitHub account
2. Sign up at [railway.app](https://railway.app)
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your forked repository
5. Railway automatically detects `railway.json` and deploys!
6. Your app will be live at `https://your-app.railway.app`

**That's it!** ⚡ Total time: ~5 minutes

For other platforms and advanced configuration, see [DEPLOYMENT.md](DEPLOYMENT.md).

---

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### Ways to Contribute
- 🐛 Report bugs and issues
- 💡 Suggest new features
- 📝 Improve documentation
- 🔧 Submit pull requests
- ⭐ Star the repository
- 📢 Share with others

### Getting Started
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests to ensure everything works
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to your branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

### Code of Conduct
- Be respectful and inclusive
- Follow security best practices
- Write clean, documented code
- Test your changes thoroughly
- Keep discussions professional

## 🎓 Academic Use & Research

This project is suitable for academic research and major project submissions. We provide comprehensive documentation for students and researchers.

### Abstract Submission

For students using this project as a major project or research work, we provide:

- **[ABSTRACT_SUBMISSION.docx](ABSTRACT_SUBMISSION.docx)** — Ready-to-submit Word document with pre-filled student information
- **[ABSTRACT_SUBMISSION.md](ABSTRACT_SUBMISSION.md)** — Complete abstract template following academic guidelines (Markdown format)
- **[ABSTRACT_DOCUMENT_README.md](ABSTRACT_DOCUMENT_README.md)** — Instructions for using and regenerating the Word document
- **[docs/ABSTRACT_GUIDELINES.md](docs/ABSTRACT_GUIDELINES.md)** — Detailed instructions for completing and submitting the abstract

### Key Features for Academic Projects

✓ **Research-Based:** Combines theoretical cryptography with practical implementation  
✓ **Well-Documented:** Comprehensive documentation with references to academic literature  
✓ **Original Implementation:** All code written from scratch with proper citations  
✓ **Modular Architecture:** Clear separation of concerns suitable for academic analysis  
✓ **Testing Framework:** Unit tests demonstrating software engineering best practices  

### Academic Compliance

The abstract submission template ensures compliance with typical institutional requirements:
- Plagiarism below 10% through original implementation
- Zero AI-generated content (0% tolerance maintained)
- Research methodology and literature review
- Clear supervision structure
- Proper academic citations and references

For more information, see [ABSTRACT_SUBMISSION.md](ABSTRACT_SUBMISSION.md).

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- PyCryptodome for cryptographic primitives
- PIL/Pillow for image processing
- The open-source community for inspiration and support

## 📧 Contact

**Parth Thakar**
- GitHub: [@parththakar2003](https://github.com/parththakar2003)
- Email: (available on GitHub profile)

## 🔒 Security

If you discover a security vulnerability, please DO NOT open a public issue. Email the maintainer directly with details.

## ⚠️ Disclaimer

This tool is for educational and legitimate security purposes only. Users are responsible for complying with applicable laws and regulations. The authors assume no liability for misuse.

## 🌟 Show Your Support

If you find this project helpful, please consider:
- ⭐ Starring the repository
- 🐛 Reporting issues
- 💡 Suggesting improvements
- 🤝 Contributing code
- 📢 Sharing with others

---

**Made with ❤️ for privacy and security**

