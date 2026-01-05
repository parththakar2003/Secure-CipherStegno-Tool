# Quick Start Guide - v3.2.0

## Welcome to Secure CipherStegno Tool! 🔐

This guide will help you get started with the new features in version 3.2.0.

## What's New in v3.2.0?

### 🎨 Beautiful Interactive CLI
We've completely redesigned the command-line experience with:
- Colorful ANSI art banners
- Animated progress indicators
- Easy-to-use menu navigation
- Visual feedback and effects

### 🔐 New Encryption Algorithms
Three powerful new encryption options:
- **Blowfish**: Fast symmetric encryption
- **3DES**: Legacy compatibility
- **ChaCha20**: Modern stream cipher

### 🎬 Video Steganography
Hide messages in video files (MP4, AVI)

### 🛠️ Advanced Security Tools
- Encryption analyzer
- Token generator
- Port scanner
- Data sanitizer
- Hash chains

## Getting Started

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/parththakar2003/Secure-CipherStegno-Tool.git
cd Secure-CipherStegno-Tool

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/macOS
# OR
venv\Scripts\activate.bat  # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Demo

See all the new features in action:

```bash
python3 demo.py
```

This will showcase:
- ASCII art banners
- Dynamic animations
- Menu systems
- New algorithms
- Security tools

### 3. Try the Interactive CLI

The easiest way to use the tool:

```bash
python3 interactive_cli.py
```

Navigate through beautiful menus to:
- Encrypt/decrypt messages
- Hide data in images/audio/video
- Generate secure passwords
- Analyze algorithm strengths
- And much more!

### 4. Use the GUI (Traditional)

For a graphical interface:

```bash
python3 app.py
```

### 5. Use the Command-Line (Advanced)

For scripting and automation:

```bash
python3 cli.py --help
```

## Quick Examples

### Example 1: Encrypt with ChaCha20

```bash
# Using interactive CLI
python3 interactive_cli.py
# Select: Cryptography > Encrypt > ChaCha20
```

### Example 2: Generate a Strong Password

```bash
# Using interactive CLI
python3 interactive_cli.py
# Select: Security Tools > Generate Strong Password
```

### Example 3: Compare Algorithms

```bash
# Using interactive CLI
python3 interactive_cli.py
# Select: Cryptography > Compare Algorithms
```

### Example 4: Hide Message in Image

```bash
# Using traditional CLI
python3 cli.py stego-encode --type image --cover photo.png --message secret.txt --output stego.png
```

## Feature Highlights

### Cryptography Menu
- **Classical Ciphers**: Caesar, Vigenère, Playfair, Rail Fence
- **Symmetric**: AES-256, Blowfish, 3DES, ChaCha20
- **Asymmetric**: RSA-2048/4096
- **Hybrid**: AES + RSA

### Steganography Menu
- **Image**: PNG, BMP, JPEG
- **Audio**: WAV files
- **Video**: MP4, AVI (requires ffmpeg)

### Security Tools Menu
- Password generator and validator
- File hash calculator
- Network port scanner
- Encryption analyzer
- Token generator
- Data sanitizer

## Tips & Tricks

1. **First Time?** Start with the interactive CLI - it's the easiest!

2. **Want Speed?** Use ChaCha20 or Blowfish for fast encryption

3. **Need Security?** AES-256 is the industry standard

4. **Large Files?** Use steganography with compression enabled

5. **Automation?** Use the traditional CLI with command-line arguments

## Troubleshooting

### Dependencies Not Installed?
```bash
pip install -r requirements.txt
```

### Video Steganography Not Working?
Install ffmpeg:
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Download from https://ffmpeg.org/
```

### CLI Not Colorful?
Make sure you're using a terminal that supports ANSI colors:
- Linux: Most terminals support it
- macOS: Terminal.app or iTerm2
- Windows: Windows Terminal or PowerShell

## Need Help?

- 📖 Check `docs/USAGE.md` for detailed instructions
- 🐛 Report issues on GitHub
- 💡 See `CHANGELOG.md` for all changes
- 📧 Contact: See GitHub profile

## What's Next?

Explore all the features:
1. Try different encryption algorithms
2. Hide messages in different media types
3. Generate secure tokens
4. Analyze your passwords
5. Compare algorithm strengths

**Have fun and stay secure!** 🔐✨

---

© 2025 Parth Thakar | MIT License
