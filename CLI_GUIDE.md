# 🖥️ Command Line Interface Guide

## Overview

The **Secure CipherStegno Tool** provides a powerful command-line interface (CLI) through `cli.py` for automation, scripting, and advanced usage. This guide covers all available commands and their usage.

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Encryption Commands](#encryption-commands)
3. [Decryption Commands](#decryption-commands)
4. [Steganography Commands](#steganography-commands)
5. [Key Generation](#key-generation)
6. [Security Tools](#security-tools)
7. [Examples & Use Cases](#examples--use-cases)
8. [Troubleshooting](#troubleshooting)

---

## Getting Started

### Installation

First, ensure all dependencies are installed:

```bash
pip install -r requirements.txt
```

### Basic Usage

```bash
python cli.py [command] [options]
```

To see all available commands:

```bash
python cli.py --help
```

To see help for a specific command:

```bash
python cli.py encrypt --help
python cli.py stego-encode --help
```

---

## Encryption Commands

### Caesar Cipher

**Simple substitution cipher** - Shifts each letter by a specified number of positions.

#### Encrypt

```bash
python cli.py encrypt --algorithm caesar --input "Hello World" --output encrypted.txt --shift 5
```

Or encrypt from a file:

```bash
python cli.py encrypt --algorithm caesar --input message.txt --output encrypted.txt --shift 3
```

#### Decrypt

```bash
python cli.py decrypt --algorithm caesar --input encrypted.txt --output decrypted.txt --shift 5
```

**Parameters:**
- `--algorithm`: Must be `caesar`
- `--input`: Input text or file path
- `--output`: Output file path
- `--shift`: Number of positions to shift (default: 3)

---

### AES-256 Encryption

**Industry-standard symmetric encryption** - Recommended for most use cases.

#### Encrypt

```bash
python cli.py encrypt --algorithm aes --input message.txt --output encrypted.json --password "your-strong-password"
```

#### Decrypt

```bash
python cli.py decrypt --algorithm aes --input encrypted.json --output decrypted.txt --password "your-strong-password"
```

**Parameters:**
- `--algorithm`: Must be `aes`
- `--input`: Input file path or text
- `--output`: Output JSON file (contains ciphertext and IV)
- `--password`: Encryption/decryption password (required)

**Important Notes:**
- AES output is saved as JSON containing both `ciphertext` and `iv` (initialization vector)
- Keep the password safe - it's required for decryption
- Use strong passwords (12+ characters with mixed case, numbers, symbols)

---

### RSA Encryption

**Public-key cryptography** - Uses key pairs for encryption/decryption.

#### Generate Key Pair

```bash
python cli.py generate-keys --algorithm rsa --output-dir ./keys --key-size 2048
```

Available key sizes:
- `2048` - Standard security (faster)
- `4096` - High security (slower)

#### Encrypt with Public Key

```bash
python cli.py encrypt --algorithm rsa --input message.txt --output encrypted.txt --key ./keys/public_key.pem
```

#### Decrypt with Private Key

```bash
python cli.py decrypt --algorithm rsa --input encrypted.txt --output decrypted.txt --key ./keys/private_key.pem
```

**Parameters:**
- `--algorithm`: Must be `rsa`
- `--input`: Input file path or text
- `--output`: Output file path
- `--key`: Path to public key (encrypt) or private key (decrypt)

**Security Notes:**
- **Never share your private key**
- Store private keys in a secure location
- Use RSA for key exchange or small data
- For large data, use hybrid encryption (AES + RSA)

---

## Decryption Commands

All decryption commands follow the same pattern as encryption but use the `decrypt` subcommand:

```bash
python cli.py decrypt --algorithm [caesar|aes|rsa] --input [encrypted-file] --output [output-file] [algorithm-specific-options]
```

See [Encryption Commands](#encryption-commands) for algorithm-specific examples.

---

## Steganography Commands

### Image Steganography

**Hide messages in images** using LSB (Least Significant Bit) technique.

#### Hide Message in Image

```bash
python cli.py stego-encode --type image --cover photo.png --message secret.txt --output stego.png
```

With compression (recommended for larger messages):

```bash
python cli.py stego-encode --type image --cover photo.png --message secret.txt --output stego.png --compress
```

#### Extract Message from Image

```bash
python cli.py stego-decode --type image --input stego.png --output extracted.txt
```

If message was compressed:

```bash
python cli.py stego-decode --type image --input stego.png --output extracted.txt --compressed
```

**Parameters:**
- `--type`: Must be `image`
- `--cover`: Cover image path (PNG, BMP, JPEG)
- `--message`: Message file to hide
- `--output`: Output stego image or extracted message
- `--compress`: Enable compression (encode only)
- `--compressed`: Message was compressed (decode only)

**Supported Formats:**
- PNG (recommended - lossless)
- BMP (lossless)
- JPEG (lossy - not recommended for steganography)

---

### Audio Steganography

**Hide messages in audio files** using LSB technique.

#### Hide Message in Audio

```bash
python cli.py stego-encode --type audio --cover music.wav --message secret.txt --output stego.wav
```

#### Extract Message from Audio

```bash
python cli.py stego-decode --type audio --input stego.wav --output extracted.txt
```

**Parameters:**
- `--type`: Must be `audio`
- `--cover`: Cover audio path (WAV format)
- `--message`: Message file to hide
- `--output`: Output stego audio or extracted message

**Requirements:**
- Audio files must be in WAV format
- Larger audio files can hide more data

---

## Key Generation

Generate cryptographic keys for various algorithms.

### RSA Key Pair

```bash
# Standard 2048-bit keys
python cli.py generate-keys --algorithm rsa --output-dir ./keys

# High-security 4096-bit keys
python cli.py generate-keys --algorithm rsa --output-dir ./keys --key-size 4096
```

**Output:**
- `public_key.pem` - Share this for encryption
- `private_key.pem` - Keep this secret for decryption

### AES Key

```bash
python cli.py generate-keys --algorithm aes --output-dir ./keys
```

**Output:**
- `aes_key.bin` - 256-bit AES key
- Key is also displayed in base64 format

---

## Security Tools

### File Hashing

Calculate cryptographic hash of any file for integrity verification.

```bash
# SHA-256 (recommended)
python cli.py hash --input document.pdf --algorithm sha256

# Other algorithms
python cli.py hash --input file.txt --algorithm md5
python cli.py hash --input file.txt --algorithm sha1
python cli.py hash --input file.txt --algorithm sha512
```

**Available Algorithms:**
- `md5` - Fast but not secure (legacy)
- `sha1` - Deprecated for security
- `sha256` - Recommended (default)
- `sha512` - High security

**Use Cases:**
- Verify file integrity
- Detect file tampering
- Compare file versions

---

### Password Generation

Generate cryptographically secure random passwords.

```bash
# Generate 16-character password (default)
python cli.py generate-password

# Custom length
python cli.py generate-password --length 24
```

**Features:**
- Cryptographically secure random generation
- Mix of uppercase, lowercase, numbers, and symbols
- Automatic strength validation

---

### Password Validation

Check password strength and get improvement recommendations.

```bash
# With password argument
python cli.py validate-password --password "MyP@ssw0rd"

# Interactive (secure, doesn't show password)
python cli.py validate-password
```

**Output:**
- Strength rating (Weak/Medium/Strong)
- Score (0-8)
- Specific recommendations for improvement

**Password Requirements:**
- Minimum 8 characters
- Mix of uppercase and lowercase letters
- At least one number
- At least one special character
- Avoid common passwords

---

## Examples & Use Cases

### Use Case 1: Secure File Transfer

Send an encrypted file to someone with their RSA public key:

```bash
# Encrypt file with recipient's public key
python cli.py encrypt --algorithm rsa --input confidential.pdf --output encrypted.bin --key recipient_public.pem

# Recipient decrypts with their private key
python cli.py decrypt --algorithm rsa --input encrypted.bin --output confidential.pdf --key my_private.pem
```

---

### Use Case 2: Hide Secret Message in Photo

```bash
# 1. Encrypt the message first
python cli.py encrypt --algorithm aes --input secret.txt --output encrypted.json --password "mypassword"

# 2. Hide encrypted message in image
python cli.py stego-encode --type image --cover vacation.png --message encrypted.json --output photo.png --compress

# 3. Extract and decrypt
python cli.py stego-decode --type image --input photo.png --output encrypted.json --compressed
python cli.py decrypt --algorithm aes --input encrypted.json --output secret.txt --password "mypassword"
```

---

### Use Case 3: Verify File Integrity

```bash
# Before sending
python cli.py hash --input document.pdf --algorithm sha256
# Output: abc123def456...

# After receiving, verify hash matches
python cli.py hash --input document.pdf --algorithm sha256
# Compare with original hash
```

---

### Use Case 4: Batch Processing with Shell Scripts

Create a script to encrypt multiple files:

```bash
#!/bin/bash
for file in *.txt; do
    python cli.py encrypt --algorithm aes --input "$file" --output "${file}.enc" --password "batchpass"
done
```

---

### Use Case 5: Automated Security Audit

```bash
#!/bin/bash
# Generate report of file hashes
echo "File Integrity Report - $(date)" > report.txt
for file in important/*; do
    hash=$(python cli.py hash --input "$file" --algorithm sha256 | tail -1)
    echo "$file: $hash" >> report.txt
done
```

---

## Troubleshooting

### Common Issues

#### 1. "Message too large for image"

**Problem:** The message is larger than the cover image capacity.

**Solutions:**
- Use a larger cover image
- Enable compression: `--compress`
- Split message into multiple images

#### 2. "No hidden message found"

**Problem:** Cannot extract message from stego file.

**Solutions:**
- Ensure file hasn't been modified (avoid JPEG if possible)
- Check if message was compressed, use `--compressed` flag
- Verify you're using the correct stego file

#### 3. "Password required for AES encryption"

**Problem:** No password provided for AES operation.

**Solution:**
```bash
# Add --password flag
python cli.py encrypt --algorithm aes --input file.txt --output enc.json --password "yourpassword"
```

#### 4. "Only WAV files are supported for audio steganography"

**Problem:** Trying to use non-WAV audio file.

**Solutions:**
- Convert audio to WAV format using ffmpeg:
  ```bash
  ffmpeg -i music.mp3 music.wav
  ```
- Use image steganography instead

#### 5. "Key file required for RSA"

**Problem:** No key file specified for RSA operation.

**Solution:**
```bash
# First generate keys
python cli.py generate-keys --algorithm rsa --output-dir ./keys

# Then use them
python cli.py encrypt --algorithm rsa --input msg.txt --output enc.txt --key ./keys/public_key.pem
```

#### 6. "Module not found" errors

**Problem:** Dependencies not installed.

**Solution:**
```bash
pip install -r requirements.txt
```

#### 7. Python version error

**Problem:** Using Python < 3.8

**Solution:**
- Install Python 3.8 or higher
- Use `python3` command instead of `python`

---

### Performance Tips

1. **Large Files:**
   - Use AES instead of RSA for large files
   - Enable compression for steganography
   - Consider splitting very large files

2. **Batch Operations:**
   - Write shell scripts for batch processing
   - Use consistent passwords/keys for automation

3. **Security Best Practices:**
   - Generate unique keys for different recipients
   - Use strong passwords (12+ characters)
   - Store private keys securely
   - Verify file hashes after transfer
   - Use SHA-256 or SHA-512 for hashing

---

## Advanced Topics

### Combining Encryption and Steganography

For maximum security, encrypt data before hiding it:

```bash
# Encrypt
python cli.py encrypt --algorithm aes --input message.txt --output encrypted.json --password "pass"

# Hide encrypted data
python cli.py stego-encode --type image --cover photo.png --message encrypted.json --output stego.png

# Extract
python cli.py stego-decode --type image --input stego.png --output encrypted.json

# Decrypt
python cli.py decrypt --algorithm aes --input encrypted.json --output message.txt --password "pass"
```

### Scripting Examples

**Python script using CLI:**

```python
import subprocess
import sys

def encrypt_file(input_file, output_file, password):
    """Encrypt file using CLI"""
    result = subprocess.run([
        sys.executable, 'cli.py', 'encrypt',
        '--algorithm', 'aes',
        '--input', input_file,
        '--output', output_file,
        '--password', password
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✓ Encrypted: {output_file}")
    else:
        print(f"✗ Error: {result.stderr}")

# Usage
encrypt_file('document.txt', 'document.enc', 'mypassword')
```

---

## Getting Help

- **General Help:** `python cli.py --help`
- **Command Help:** `python cli.py [command] --help`
- **Documentation:** See `README.md` and `docs/` directory
- **Issues:** Report at [GitHub Issues](https://github.com/parththakar2003/Secure-CipherStegno-Tool/issues)

---

## Quick Reference

### Common Commands Cheat Sheet

```bash
# Encrypt with AES
python cli.py encrypt --algorithm aes --input file.txt --output enc.json --password "pass"

# Decrypt with AES
python cli.py decrypt --algorithm aes --input enc.json --output file.txt --password "pass"

# Generate RSA keys
python cli.py generate-keys --algorithm rsa --output-dir ./keys

# Hide in image
python cli.py stego-encode --type image --cover photo.png --message secret.txt --output stego.png

# Extract from image
python cli.py stego-decode --type image --input stego.png --output secret.txt

# Hash file
python cli.py hash --input file.pdf --algorithm sha256

# Generate password
python cli.py generate-password --length 20

# Validate password
python cli.py validate-password --password "Test@123"
```

---

**Version:** 3.1.0  
**Last Updated:** January 2026  
**License:** MIT

For the interactive menu-based interface, see `interactive_cli.py` - no commands to type!
