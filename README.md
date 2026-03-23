# Secure CipherStegno Tool

**Version 3.2.0** — Enterprise-Grade Security Platform

**Secure CipherStegno Tool** is a comprehensive professional security platform that combines advanced **cryptography**, **steganography**, **AI-based analysis**, and **cloud services** to provide enterprise-grade security solutions — all with privacy-first, local-first processing capabilities.

---

![License](https://img.shields.io/github/license/parththakar2003/Secure-CipherStegno-Tool?style=for-the-badge)
![Stars](https://img.shields.io/github/stars/parththakar2003/Secure-CipherStegno-Tool?style=for-the-badge)
![Forks](https://img.shields.io/github/forks/parththakar2003/Secure-CipherStegno-Tool?style=for-the-badge)
![Issues](https://img.shields.io/github/issues/parththakar2003/Secure-CipherStegno-Tool?style=for-the-badge)
![Pull Requests](https://img.shields.io/github/issues-pr/parththakar2003/Secure-CipherStegno-Tool?style=for-the-badge)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![GUI](https://img.shields.io/badge/GUI-Tkinter-red?style=for-the-badge)
![Crypto](https://img.shields.io/badge/Cryptography-AES%20%7C%20RSA-darkgreen?style=for-the-badge)
![Steganography](https://img.shields.io/badge/Steganography-Image%20%7C%20Audio%20%7C%20Video-purple?style=for-the-badge)
![Privacy](https://img.shields.io/badge/Privacy-Local%20Only-black?style=for-the-badge)

![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey?style=for-the-badge)
![Security](https://img.shields.io/badge/Focus-Cybersecurity-critical?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active%20Development-success?style=for-the-badge)

---

## Features

### Cryptography

#### Classical Ciphers
- **Caesar Cipher** — Simple substitution cipher for basic encryption
- **Vigenère Cipher** — Polyalphabetic substitution cipher with keyword
- **Playfair Cipher** — Digraph substitution cipher (5x5 matrix)
- **Rail Fence Cipher** — Transposition cipher with zigzag pattern

#### Modern Symmetric Encryption
- **AES-256** — Industry-standard symmetric encryption (Recommended)
- **Blowfish** — Fast block cipher by Bruce Schneier
- **3DES (Triple DES)** — Legacy encryption for backwards compatibility
- **ChaCha20** — Modern stream cipher, mobile-optimized

#### Asymmetric Encryption
- **RSA** — Public key cryptography (2048/4096 bit)
- **Hybrid Encryption** — Combine AES and RSA for optimal security

#### Key Management
- **Key Generation** — Generate secure cryptographic keys
- **Key Storage** — Safe key management and storage
- **Key Exchange** — Secure key distribution protocols

### Steganography
- **Image Steganography** — Hide messages in PNG/BMP/JPEG images using LSB technique
- **Audio Steganography** — Embed secrets in WAV audio files
- **Video Steganography** — Hide data in MP4/AVI video frames
- **Document Steganography** — Hide data in PDF/DOCX and text files
- **Compression Support** — Compress messages before hiding for larger capacity
- **Capacity Analysis** — Check how much data can be hidden in cover files
- **Advanced LSB** — Configurable bits-per-channel for balance between capacity and quality

### Security Tools

#### Password Security
- **Password Validator** — Analyze password strength with detailed feedback
- **Password Generator** — Create cryptographically secure passwords

#### Hash & Integrity
- **Hash Calculator** — MD5, SHA-1, SHA-256, SHA-512 support
- **File Integrity Verification** — Verify files haven't been tampered with
- **Secure File Deletion** — Overwrite files before deletion

#### Advanced Security Tools
- **Encryption Analyzer** — Compare and analyze algorithm strengths
- **Token Generator** — Generate secure API keys and session tokens
- **Port Scanner** — Basic network security scanning (localhost)
- **Data Sanitizer** — Sanitize filenames and user inputs
- **Hash Chain** — Create verifiable data integrity chains

### User Interfaces
- **Modern GUI** — Intuitive Tkinter interface with professional design
- **Web Interface** — Full-featured web-based interface with FastAPI backend
- **Interactive CLI** — Beautiful ANSI art-based command-line interface with menu navigation
- **Traditional CLI** — Full-featured command-line interface with arguments for automation
- **Synchronized Interfaces** — All interfaces (GUI, Web, CLI) use the same core operations

---

## How It Works

1. **Encrypt** your message with a passphrase/key.
2. Choose a **cover file** (image, audio, or video).
3. The tool embeds the encrypted message inside the cover.
4. Share the file safely — only those with the correct key can extract it.

---

## Tech Stack

### Core Technologies
- **Python 3.8+** — Main programming language
- **Tkinter** — GUI interface
- **FastAPI** — Web interface and REST API
- **Uvicorn** — ASGI server for web interface
- **Jinja2** — HTML templating for web interface
- **PyCryptodome** — Cryptographic operations (AES, RSA, Blowfish, 3DES)
- **Pillow (PIL)** — Image processing and steganography
- **NumPy** — Efficient array operations
- **Wave** — Audio file processing
- **PyPDF2** — Document steganography

### Additional Libraries
- **Colorama** — CLI color output
- **SciPy** — Advanced audio processing
- **zlib** — Data compression
- **hashlib** — File integrity verification

---

## Project Structure

See [STRUCTURE.md](STRUCTURE.md) for detailed documentation.

```
Secure-CipherStegno-Tool/
├── apps/                # Application entry points
│   ├── launch.py        # Unified launcher (recommended)
│   ├── app.py           # GUI application
│   ├── cli.py           # Command-line interface
│   ├── interactive_cli.py  # Interactive CLI with menus
│   └── demo.py          # Demo application
├── scripts/             # Setup and utility scripts
│   ├── setup.sh         # Linux/macOS setup
│   ├── setup.bat        # Windows setup
│   └── check_python.py  # Python version checker
├── src/                 # Source code modules
│   ├── core/            # Shared core operations
│   ├── crypto/          # Cryptography modules
│   ├── steganography/   # Steganography implementations
│   ├── ai/              # AI/ML steganalysis
│   ├── utils/           # Security and file utilities
│   └── web/             # Web interface and API
├── docs/                # Documentation
│   ├── guides/          # User guides and tutorials
│   └── submissions/     # Academic submission documents
├── tests/               # Unit tests
├── examples/            # Sample files and usage examples
└── requirements.txt     # Python dependencies
```

---

## Installation & Usage

### Prerequisites

**Python 3.8 or higher is required.**

```bash
# Check your Python version
python --version
# or
python3 --version
```

If your version is below 3.8, download Python 3.8+ from [python.org](https://www.python.org/downloads/).

### Quick Start

#### Automated Setup (Recommended)

**Linux/macOS:**
```bash
git clone https://github.com/parththakar2003/Secure-CipherStegno-Tool.git
cd Secure-CipherStegno-Tool

chmod +x scripts/setup.sh
./scripts/setup.sh

source venv/bin/activate
python apps/app.py
```

**Windows:**
```bash
git clone https://github.com/parththakar2003/Secure-CipherStegno-Tool.git
cd Secure-CipherStegno-Tool

scripts\setup.bat

venv\Scripts\activate.bat
python apps\app.py
```

#### Manual Setup

```bash
git clone https://github.com/parththakar2003/Secure-CipherStegno-Tool.git
cd Secure-CipherStegno-Tool

# Verify Python version (must be 3.8+)
python3 scripts/check_python.py

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# or: venv\Scripts\activate.bat  (Windows)

# Install dependencies
pip install -r requirements.txt

# Launch the application
python apps/launch.py gui          # GUI interface
python apps/launch.py web          # Web interface (http://localhost:8000)
python apps/launch.py interactive  # Interactive CLI
python apps/launch.py cli --help   # Traditional CLI
```

**Note:** Virtual environment is strongly recommended to avoid conflicts with system packages. On modern Linux distributions (Ubuntu 23.04+, Kali), direct system-wide installation is blocked by PEP 668.

---

### Application Modes

#### 1. GUI Application (Tkinter)

Three main tabs: Cryptography, Steganography, Security Tools.

```bash
python3 apps/launch.py gui
# or
python3 apps/app.py
```

#### 2. Web Interface

Full-featured, mobile-friendly web UI with a FastAPI backend.

```bash
python3 apps/launch.py web --port 8000
# or
python3 -m uvicorn src.web.api:app --host 0.0.0.0 --port 8000
```

Open your browser to `http://localhost:8000`. REST API docs at `/api/docs`.

#### 3. Interactive CLI

Menu-based terminal interface with ANSI art — no commands to memorize.

```bash
python3 apps/launch.py interactive
# or
python3 apps/interactive_cli.py
```

#### 4. Traditional CLI

Command-line interface for automation, scripting, and CI/CD.

```bash
python3 apps/launch.py cli --help
# or
python3 apps/cli.py --help
```

### CLI Modes Comparison

| Feature | Interactive CLI | Traditional CLI |
|---------|----------------|-----------------|
| **Learning Curve** | Easy — no commands to learn | Moderate — need to know commands |
| **Best For** | Beginners, exploration | Automation, scripting |
| **Interface** | Menu-based (select numbers) | Command arguments |
| **Visual Feedback** | Colors, animations, progress | Plain text output |
| **Automation** | Manual operation only | Full automation support |

For detailed CLI documentation, see [docs/guides/CLI_GUIDE.md](docs/guides/CLI_GUIDE.md).

---

### CLI Usage Examples

#### Encrypt with AES
```bash
python3 apps/cli.py encrypt --algorithm aes --input message.txt --output encrypted.json --password "strongpassword"
```

#### Hide message in image
```bash
python3 apps/cli.py stego-encode --type image --cover photo.png --message secret.txt --output stego.png --compress
```

#### Generate RSA keys
```bash
python3 apps/cli.py generate-keys --algorithm rsa --output-dir ./keys
```

#### Calculate file hash
```bash
python3 apps/cli.py hash --input document.pdf --algorithm sha256
```

#### Decrypt with RSA
```bash
python3 apps/cli.py decrypt --algorithm rsa --input encrypted.txt --output decrypted.txt --key ./keys/private_key.pem
```

---

### Running Tests

```bash
source venv/bin/activate  # Linux/macOS
# or: venv\Scripts\activate.bat  (Windows)

python -m pytest tests/
# or
python -m unittest discover tests/
```

---

### Troubleshooting

#### `externally-managed-environment` Error

Use a virtual environment (required on modern Linux distributions):
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
```

#### `ModuleNotFoundError: No module named 'Crypto'`

Ensure you created and activated the virtual environment, then ran `pip install -r requirements.txt`.

#### Python Version Issues

```bash
python3 --version  # Must be 3.8+
python3 scripts/check_python.py
```

---

## Roadmap

### Completed
- ✅ Classical Ciphers (Caesar, Vigenère, Playfair, Rail Fence)
- ✅ AES-256, RSA-2048 encryption
- ✅ Blowfish, 3DES, ChaCha20 ciphers
- ✅ Image Steganography (PNG/BMP/JPEG)
- ✅ Audio Steganography (WAV)
- ✅ Video Steganography (MP4/AVI)
- ✅ Document Steganography (PDF/DOCX)
- ✅ Advanced Security Tools (Analyzer, Token Generator, Port Scanner, Hash Chain)
- ✅ Interactive CLI with ANSI art
- ✅ Web Interface (FastAPI)
- ✅ AI-based steganalysis module

### Planned
- 🔲 Quantum-resistant cryptography (Post-quantum algorithms)
- 🔲 MP3/FLAC/OGG audio steganography
- 🔲 Multi-layer steganography
- 🔲 Neural network-based steganography
- 🔲 ML steganalysis improvements
- 🔲 Mobile applications (Android/iOS)
- 🔲 Hardware Security Module (HSM) integration
- 🔲 Enterprise features (LDAP, SSO, audit logging)
- 🔲 Compliance reporting (GDPR, HIPAA)

---

## Contributing

### Ways to Contribute
- Report bugs and issues
- Suggest new features
- Improve documentation
- Submit pull requests

### Getting Started
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Run tests: `python -m pytest tests/`
5. Commit: `git commit -m 'Add amazing feature'`
6. Push: `git push origin feature/amazing-feature`
7. Open a Pull Request

See [docs/guides/CONTRIBUTING.md](docs/guides/CONTRIBUTING.md) for detailed guidelines.

---

## Academic Use

This project is suitable for academic research and major project submissions. Documentation for students:

- [docs/submissions/ABSTRACT_SUBMISSION.md](docs/submissions/ABSTRACT_SUBMISSION.md) — Abstract template
- [docs/ABSTRACT_GUIDELINES.md](docs/ABSTRACT_GUIDELINES.md) — Submission instructions
- [docs/SUBMISSION_CHECKLIST.md](docs/SUBMISSION_CHECKLIST.md) — Pre-submission checklist

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## Contact

**Parth Thakar**
- GitHub: [@parththakar2003](https://github.com/parththakar2003)

## Security

If you discover a security vulnerability, please **do not** open a public issue. Email the maintainer directly with details.

## Disclaimer

This tool is for educational and legitimate security purposes only. Users are responsible for complying with applicable laws and regulations. The authors assume no liability for misuse.

---

*Made with care for privacy and security*
