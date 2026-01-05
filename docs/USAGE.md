# Example Usage Guide

## Installation

```bash
pip install -r requirements.txt
```

## GUI Application

Run the graphical interface:
```bash
python index.py
```

## Command Line Interface

### Basic Cryptography

#### Caesar Cipher
```bash
# Encrypt
python cli.py encrypt --algorithm caesar --input "Hello World" --output encrypted.txt --shift 5

# Decrypt
python cli.py decrypt --algorithm caesar --input encrypted.txt --output decrypted.txt --shift 5
```

#### AES-256 Encryption
```bash
# Encrypt a file
python cli.py encrypt --algorithm aes --input message.txt --output encrypted.json --password "strongpassword"

# Decrypt
python cli.py decrypt --algorithm aes --input encrypted.json --output decrypted.txt --password "strongpassword"
```

#### RSA Encryption
```bash
# Generate key pair
python cli.py generate-keys --algorithm rsa --output-dir ./keys

# Encrypt
python cli.py encrypt --algorithm rsa --input message.txt --output encrypted.txt --key ./keys/public_key.pem

# Decrypt
python cli.py decrypt --algorithm rsa --input encrypted.txt --output decrypted.txt --key ./keys/private_key.pem
```

### Steganography

#### Image Steganography
```bash
# Hide message in image
python cli.py stego-encode --type image --cover photo.png --message secret.txt --output stego.png --compress

# Extract message
python cli.py stego-decode --type image --input stego.png --output extracted.txt --compressed
```

#### Audio Steganography
```bash
# Hide message in audio
python cli.py stego-encode --type audio --cover music.wav --message secret.txt --output stego.wav

# Extract message
python cli.py stego-decode --type audio --input stego.wav --output extracted.txt
```

### Utility Commands

#### File Hashing
```bash
python cli.py hash --input document.pdf --algorithm sha256
```

#### Password Tools
```bash
# Generate strong password
python cli.py generate-password --length 20

# Validate password strength
python cli.py validate-password --password "MyP@ssw0rd"
```

## Python API Examples

### Cryptography

```python
from src.crypto import CaesarCipher, AESCipher, RSACipher

# Caesar Cipher
encrypted = CaesarCipher.encrypt("Hello", 5)
decrypted = CaesarCipher.decrypt(encrypted, 5)

# AES Encryption
result = AESCipher.encrypt_with_password("Secret message", "password")
decrypted = AESCipher.decrypt_with_password(
    result['ciphertext'], 
    result['iv'], 
    "password"
)

# RSA
cipher = RSACipher()
keys = cipher.generate_key_pair()
encrypted = cipher.encrypt("Message")
decrypted = cipher.decrypt(encrypted)
```

### Steganography

```python
from src.steganography import ImageSteganography, AudioSteganography

# Image Steganography
ImageSteganography.encode(
    image_path="cover.png",
    message="Secret message",
    output_path="stego.png",
    compress=True
)

message = ImageSteganography.decode("stego.png", compressed=True)

# Audio Steganography
AudioSteganography.encode(
    audio_path="cover.wav",
    message="Hidden message",
    output_path="stego.wav"
)

message = AudioSteganography.decode("stego.wav")
```

### Utilities

```python
from src.utils import (
    PasswordValidator, 
    calculate_file_hash,
    Logger
)

# Password validation
result = PasswordValidator.validate_strength("P@ssw0rd123")
print(f"Strength: {result['strength']}")

# Generate password
password = PasswordValidator.generate_strong_password(16)

# File hashing
hash_value = calculate_file_hash("document.pdf", "sha256")

# Logging
logger = Logger("app.log")
logger.info("Operation started")
logger.success("Operation completed")
```

## Advanced Usage

### Hybrid Encryption (AES + RSA)

```python
from src.crypto import hybrid_encrypt, hybrid_decrypt, RSACipher

# Generate RSA keys
cipher = RSACipher()
keys = cipher.generate_key_pair()

# Encrypt large message
encrypted = hybrid_encrypt(
    plaintext="Large secret message",
    recipient_public_key_pem=keys['public_key']
)

# Decrypt
decrypted = hybrid_decrypt(
    encrypted_data=encrypted['encrypted_data'],
    iv=encrypted['iv'],
    encrypted_key=encrypted['encrypted_key'],
    private_key_pem=keys['private_key']
)
```

### Advanced Image Steganography

```python
from src.steganography import AdvancedImageSteganography

# Use more LSBs for higher capacity
stego = AdvancedImageSteganography(bits_per_channel=2)
stego.encode("cover.png", "Secret message", "stego.png")
message = stego.decode("stego.png")
```

## Security Best Practices

1. **Use strong passwords**: At least 12 characters with mix of uppercase, lowercase, numbers, and special characters
2. **Keep private keys secure**: Never share RSA private keys
3. **Use AES for large data**: RSA is slow for large amounts of data
4. **Verify file integrity**: Use hash functions to verify file hasn't been tampered with
5. **Secure deletion**: Use secure_delete_file() for sensitive data
6. **Compress before encrypting**: Reduces data size for steganography

## Troubleshooting

### Common Issues

**Issue**: "Message too large for image"
- **Solution**: Use a larger cover image or compress the message

**Issue**: "No hidden message found"
- **Solution**: Ensure you're using the correct decompression flag

**Issue**: "Only WAV files are supported"
- **Solution**: Convert audio files to WAV format first

**Issue**: "Password validation fails"
- **Solution**: Ensure password meets minimum strength requirements
