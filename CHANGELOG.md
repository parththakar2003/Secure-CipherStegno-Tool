# Changelog

All notable changes to the Secure CipherStegno Tool project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.0] - 2025-01-05

### Added
- **Vigenère Cipher**: Polyalphabetic substitution cipher with key strength analysis
- **Playfair Cipher**: Digraph substitution cipher implementation
- **Rail Fence Cipher**: Transposition cipher with configurable rails
- Version management system (`src/__init__.py`)
- Setup.py for proper package installation
- Comprehensive version tracking across all modules

### Fixed
- Image steganography pixel manipulation bug (int32 handling)
- NumPy array overflow issues in LSB encoding

### Changed
- Updated CLI to display version number
- Improved error handling in steganography modules

## [2.0.0] - 2025-01-05

### Added
- **Advanced Cryptography**:
  - AES-256 encryption/decryption with password derivation
  - RSA-2048 public key cryptography
  - Hybrid encryption (AES + RSA)
  - Key generation and management system
  
- **Audio Steganography**:
  - LSB steganography for WAV files
  - Capacity analysis for audio files
  - Audio file validation

- **Enhanced Image Steganography**:
  - Message compression support (zlib)
  - Advanced multi-bit LSB encoding
  - Capacity analysis

- **Security Tools**:
  - Password strength validator with detailed feedback
  - Secure password generator (cryptographically random)
  - File hash calculator (MD5, SHA-1, SHA-256, SHA-512)
  - File integrity verification
  - Secure file deletion with multiple overwrite passes
  - Comprehensive logging system

- **User Interfaces**:
  - Modern GUI application (`app.py`) with tabbed interface
  - Full-featured Command-Line Interface (`cli.py`)
  - Interactive password validation
  - Real-time encryption/decryption

- **Project Infrastructure**:
  - Organized project structure (`src/`, `tests/`, `docs/`, `examples/`)
  - Unit tests for cryptography and utilities
  - requirements.txt with all dependencies
  - .gitignore for Python projects
  - CONTRIBUTING.md guidelines

- **Documentation**:
  - Comprehensive USAGE.md guide
  - Detailed ROADMAP.md for future development
  - README.md with badges and examples
  - Code examples and sample files

### Changed
- Restructured codebase into modular architecture
- Improved error handling throughout
- Enhanced Caesar cipher to handle digits
- Updated README with new features and examples

### Deprecated
- `index.py` (legacy GUI) - kept for backwards compatibility

## [1.0.0] - 2025-01-04

### Added
- Initial release
- Basic Caesar cipher encryption/decryption
- Simple LSB image steganography (PNG/BMP)
- Basic Tkinter GUI interface
- MIT License

---

## Upcoming Releases

### [2.2.0] - Planned
- Video steganography (MP4, AVI, MKV)
- MP3 audio steganography
- JPEG steganography (DCT coefficients)
- Document steganography (PDF, DOCX)
- Batch processing capabilities

### [2.3.0] - Planned
- Machine learning-based steganalysis
- Tampering detection system
- Neural network steganography
- Statistical analysis tools
- Anomaly detection

### [3.0.0] - Planned
- Web-based interface (React + FastAPI)
- Cloud deployment
- Multi-user authentication
- RESTful API with OAuth2
- End-to-end encryption for cloud storage
- Real-time collaboration features

### [3.1.0] - Planned
- Mobile applications (iOS/Android)
- Hardware Security Module (HSM) integration
- Enterprise features (LDAP, SSO, SAML)
- Compliance tools (GDPR, HIPAA)
- Advanced audit and monitoring

---

## Version Numbering

This project uses [Semantic Versioning](https://semver.org/):
- MAJOR version for incompatible API changes
- MINOR version for backwards-compatible functionality additions
- PATCH version for backwards-compatible bug fixes

## Links

- [GitHub Repository](https://github.com/parththakar2003/Secure-CipherStegno-Tool)
- [Issue Tracker](https://github.com/parththakar2003/Secure-CipherStegno-Tool/issues)
- [Documentation](https://github.com/parththakar2003/Secure-CipherStegno-Tool/blob/main/docs/USAGE.md)
