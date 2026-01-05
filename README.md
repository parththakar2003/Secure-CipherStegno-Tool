# 🔐 Secure CipherStegno Tool

**Secure CipherStegno Tool** is an advanced privacy-focused application that combines **cryptography** and **steganography** to securely encrypt and embed sensitive information into images or audio files — all processed **locally** to ensure maximum security and data integrity .

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


---

## 📌 Features

### Cryptography
- 🔐 **Caesar Cipher** — Simple substitution cipher for basic encryption
- 🔒 **AES-256** — Industry-standard symmetric encryption
- 🔑 **RSA** — Public key cryptography (2048/4096 bit)
- 🔐 **Hybrid Encryption** — Combine AES and RSA for optimal security
- 🔑 **Key Management** — Generate, store, and manage cryptographic keys

### Steganography
- 🖼️ **Image Steganography** — Hide messages in PNG/BMP images using LSB technique
- 🎵 **Audio Steganography** — Embed secrets in WAV audio files
- 🗜️ **Compression Support** — Compress messages before hiding for larger capacity
- 📊 **Capacity Analysis** — Check how much data can be hidden in cover files
- 🔧 **Advanced LSB** — Configurable bits-per-channel for balance between capacity and quality

### Security Tools
- ✅ **Password Validator** — Analyze password strength with detailed feedback
- 🔄 **Password Generator** — Create cryptographically secure passwords
- #️⃣ **Hash Calculator** — MD5, SHA-1, SHA-256, SHA-512 support
- 🔍 **File Integrity Verification** — Verify files haven't been tampered with
- 🗑️ **Secure File Deletion** — Overwrite files before deletion

### User Interface
- 🖥️ **Modern GUI** — Intuitive Tkinter interface with professional design
- ⌨️ **CLI Support** — Full-featured command-line interface
- 📖 **Comprehensive Documentation** — Usage guides and examples
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
```
Secure-CipherStegno-Tool/
├── src/
│   ├── crypto/          # Cryptography modules
│   ├── steganography/   # Steganography implementations
│   └── utils/           # Security and file utilities
├── tests/               # Unit tests
├── docs/                # Documentation
├── examples/            # Sample files and usage examples
├── app.py              # Enhanced GUI application
├── cli.py              # Command-line interface
├── index.py            # Original simple GUI (legacy)
└── requirements.txt    # Python dependencies
```

---

## 📷 Screenshots


---

## 🧪 Installation & Usage

### Quick Start

```bash
# Clone the repository
git clone https://github.com/parththakar2003/Secure-CipherStegno-Tool.git
cd Secure-CipherStegno-Tool

# Install dependencies
pip install -r requirements.txt

# Run the enhanced GUI application
python app.py

# Or use the command-line interface
python cli.py --help
```

### GUI Application

The enhanced GUI provides a modern, user-friendly interface with three main tabs:

1. **Cryptography** — Caesar, AES-256, and RSA encryption/decryption
2. **Steganography** — Image and audio steganography
3. **Security Tools** — Password tools, hash calculator, file verification

```bash
python app.py
```

### CLI Usage Examples

#### Encrypt with AES
```bash
python cli.py encrypt --algorithm aes --input message.txt --output encrypted.json --password "strongpassword"
```

#### Hide message in image
```bash
python cli.py stego-encode --type image --cover photo.png --message secret.txt --output stego.png --compress
```

#### Generate RSA keys
```bash
python cli.py generate-keys --algorithm rsa --output-dir ./keys
```

#### Calculate file hash
```bash
python cli.py hash --input document.pdf --algorithm sha256
```

For detailed usage instructions, see [docs/USAGE.md](docs/USAGE.md)

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_crypto.py

# Or use unittest
python -m unittest discover tests/
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

