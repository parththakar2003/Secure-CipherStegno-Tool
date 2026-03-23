# Web Interface Quick Start Guide

## 🌐 Secure CipherStegno Tool - Web Interface

The web interface provides a modern, browser-based UI for all cryptography, steganography, and security operations.

## 🚀 Starting the Web Interface

### Method 1: Using the Unified Launcher (Recommended)

```bash
# Start web server on default port (8000)
python apps/launch.py web

# Start on custom port
python apps/launch.py web --port 5000

# Start on specific host
python apps/launch.py web --host 127.0.0.1 --port 8080
```

### Method 2: Using Uvicorn Directly

```bash
# Start with default settings
python -m uvicorn src.web.api:app --host 0.0.0.0 --port 8000

# Start with auto-reload (for development)
python -m uvicorn src.web.api:app --host 0.0.0.0 --port 8000 --reload
```

### Accessing the Interface

Once started, open your web browser and navigate to:
- **Web Interface**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/docs
- **Alternative API Docs**: http://localhost:8000/api/redoc

## 📱 Features

### 1. Cryptography Operations
- **Encrypt/Decrypt** text using multiple algorithms
- **Supported Algorithms**:
  - Classical: Caesar, Vigenère, Playfair, Rail Fence
  - Modern: AES-256, Blowfish, 3DES, ChaCha20, RSA
- **Dynamic Forms**: Fields adjust based on selected algorithm
- **Copy Results**: One-click copying to clipboard

### 2. Steganography Operations
- **Encode**: Hide messages in PNG, BMP, or WAV files
- **Decode**: Extract hidden messages from stego files
- **Compression**: Optional message compression
- **Download**: Direct download of stego files

### 3. Security Tools
- **Password Validator**: Check password strength with detailed feedback
- **Password Generator**: Generate cryptographically secure passwords
- **Hash Calculator**: Calculate MD5, SHA-1, SHA-256, SHA-512 hashes

### 4. About
- Project information
- Supported algorithms
- Feature overview

## 🎯 Usage Examples

### Encrypting Text

1. Navigate to **Cryptography** tab
2. Click **Encrypt** button
3. Enter your plain text
4. Select an algorithm (e.g., AES-256)
5. Enter a key/password
6. Click **🔒 Encrypt**
7. Copy the result

### Hiding Messages in Images

1. Navigate to **Steganography** tab
2. Click **Encode (Hide)** button
3. Select a cover file (PNG, BMP, or WAV)
4. Enter your secret message
5. Check "Compress message" if needed
6. Click **🔒 Hide Message**
7. Download the stego file

### Validating Password Strength

1. Navigate to **Security Tools** tab
2. Find the **Password Validator** card
3. Enter a password
4. Click **Check Strength**
5. View strength rating and feedback

## 🔄 Synchronization with Other Interfaces

The web interface uses the same core operations module (`src/core/operations.py`) as the GUI and CLI interfaces, ensuring:
- ✅ Consistent behavior across all interfaces
- ✅ Same encryption algorithms and parameters
- ✅ Same steganography operations
- ✅ Same security tools

## 🛡️ Security Notes

- All operations are performed **server-side** on your local machine
- No data is sent to external servers
- No tracking or analytics
- Privacy-first design
- Use HTTPS in production environments

## 🔧 Configuration

### Port Configuration
Default port is 8000. To change:
```bash
python apps/launch.py web --port YOUR_PORT
```

### Host Configuration
Default host is 0.0.0.0 (all interfaces). To restrict:
```bash
python apps/launch.py web --host 127.0.0.1  # Localhost only
```

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Use a different port
python apps/launch.py web --port 8888
```

### Module Not Found Errors
```bash
# Install all dependencies
pip install -r requirements.txt
```

### Browser Not Opening Automatically
Manually open your browser and navigate to `http://localhost:8000`

## 📊 API Access

The web interface also provides a RESTful API for programmatic access:

### API Endpoints

- `POST /api/v1/encrypt` - Encrypt text
- `POST /api/v1/decrypt` - Decrypt text
- `POST /api/v1/stego/encode` - Hide message in file
- `POST /api/v1/stego/decode` - Extract message from file
- `POST /api/v1/tools/validate-password` - Validate password
- `POST /api/v1/tools/generate-password` - Generate password
- `POST /api/v1/tools/hash` - Calculate file hash

### Interactive API Documentation

Visit `http://localhost:8000/api/docs` for interactive Swagger UI documentation where you can:
- View all available endpoints
- See request/response schemas
- Test endpoints directly in the browser

## 🎨 Browser Compatibility

Tested and working on:
- ✅ Chrome/Chromium 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

## 📝 Notes

- The web interface is designed for **local use** by default
- For production deployment, consider:
  - Using HTTPS (SSL/TLS)
  - Setting up proper authentication
  - Configuring CORS appropriately
  - Using a production ASGI server (e.g., Gunicorn with Uvicorn workers)

## 🆘 Support

For issues or questions:
- Check the main [README.md](../README.md)
- Visit the [GitHub repository](https://github.com/parththakar2003/Secure-CipherStegno-Tool)
- Open an issue on GitHub
