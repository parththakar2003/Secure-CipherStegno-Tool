"""
FastAPI Web Application (v3.0)
RESTful API for Secure CipherStegno Tool
"""

try:
    from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends, status
    from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel
    import uvicorn
except ImportError:
    raise ImportError("FastAPI dependencies required. Install with: pip install fastapi uvicorn python-multipart")

import sys
import os
from typing import Optional, List
import tempfile
import shutil

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from src.crypto import CaesarCipher, AESCipher, RSACipher, VigenereCipher
from src.steganography import ImageSteganography, AudioSteganography
from src.utils import PasswordValidator, calculate_file_hash
from src import __version__

# Initialize FastAPI app
app = FastAPI(
    title="Secure CipherStegno API",
    description="RESTful API for cryptography and steganography operations",
    version=__version__,
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OAuth2 scheme (placeholder)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Pydantic models
class EncryptRequest(BaseModel):
    text: str
    algorithm: str
    key: Optional[str] = None
    shift: Optional[int] = 3

class EncryptResponse(BaseModel):
    success: bool
    ciphertext: str
    algorithm: str
    iv: Optional[str] = None

class DecryptRequest(BaseModel):
    ciphertext: str
    algorithm: str
    key: Optional[str] = None
    shift: Optional[int] = 3
    iv: Optional[str] = None

class PasswordValidationRequest(BaseModel):
    password: str

class PasswordGenerationRequest(BaseModel):
    length: int = 16

class HashRequest(BaseModel):
    algorithm: str = "sha256"

class User(BaseModel):
    username: str
    email: Optional[str] = None

# Root endpoint
@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "name": "Secure CipherStegno API",
        "version": __version__,
        "status": "operational",
        "endpoints": {
            "docs": "/api/docs",
            "health": "/api/health",
            "encrypt": "/api/v1/encrypt",
            "decrypt": "/api/v1/decrypt",
            "stego": "/api/v1/stego",
            "tools": "/api/v1/tools"
        }
    }

# Health check
@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": __version__
    }

# Encryption endpoint
@app.post("/api/v1/encrypt", response_model=EncryptResponse)
async def encrypt_text(request: EncryptRequest):
    """Encrypt text using specified algorithm"""
    try:
        if request.algorithm == "caesar":
            ciphertext = CaesarCipher.encrypt(request.text, request.shift or 3)
            return EncryptResponse(
                success=True,
                ciphertext=ciphertext,
                algorithm="caesar"
            )
        
        elif request.algorithm == "vigenere":
            if not request.key:
                raise HTTPException(status_code=400, detail="Key required for Vigenère cipher")
            ciphertext = VigenereCipher.encrypt(request.text, request.key)
            return EncryptResponse(
                success=True,
                ciphertext=ciphertext,
                algorithm="vigenere"
            )
        
        elif request.algorithm == "aes":
            if not request.key:
                raise HTTPException(status_code=400, detail="Password required for AES")
            result = AESCipher.encrypt_with_password(request.text, request.key)
            return EncryptResponse(
                success=True,
                ciphertext=result['ciphertext'],
                algorithm="aes",
                iv=result['iv']
            )
        
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported algorithm: {request.algorithm}")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Decryption endpoint
@app.post("/api/v1/decrypt")
async def decrypt_text(request: DecryptRequest):
    """Decrypt text using specified algorithm"""
    try:
        if request.algorithm == "caesar":
            plaintext = CaesarCipher.decrypt(request.ciphertext, request.shift or 3)
            return {
                "success": True,
                "plaintext": plaintext,
                "algorithm": "caesar"
            }
        
        elif request.algorithm == "vigenere":
            if not request.key:
                raise HTTPException(status_code=400, detail="Key required")
            plaintext = VigenereCipher.decrypt(request.ciphertext, request.key)
            return {
                "success": True,
                "plaintext": plaintext,
                "algorithm": "vigenere"
            }
        
        elif request.algorithm == "aes":
            if not request.key or not request.iv:
                raise HTTPException(status_code=400, detail="Password and IV required")
            plaintext = AESCipher.decrypt_with_password(
                request.ciphertext,
                request.iv,
                request.key
            )
            return {
                "success": True,
                "plaintext": plaintext,
                "algorithm": "aes"
            }
        
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported algorithm: {request.algorithm}")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Password validation endpoint
@app.post("/api/v1/tools/validate-password")
async def validate_password(request: PasswordValidationRequest):
    """Validate password strength"""
    try:
        result = PasswordValidator.validate_strength(request.password)
        return {
            "success": True,
            "validation": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Password generation endpoint
@app.post("/api/v1/tools/generate-password")
async def generate_password(request: PasswordGenerationRequest):
    """Generate strong password"""
    try:
        password = PasswordValidator.generate_strong_password(request.length)
        validation = PasswordValidator.validate_strength(password)
        return {
            "success": True,
            "password": password,
            "strength": validation['strength'],
            "score": validation['score']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# File hash endpoint
@app.post("/api/v1/tools/hash")
async def hash_file(file: UploadFile = File(...), algorithm: str = Form("sha256")):
    """Calculate file hash"""
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            temp_path = temp_file.name
        
        # Calculate hash
        file_hash = calculate_file_hash(temp_path, algorithm)
        
        # Cleanup
        os.unlink(temp_path)
        
        return {
            "success": True,
            "filename": file.filename,
            "algorithm": algorithm,
            "hash": file_hash
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Steganography encode endpoint
@app.post("/api/v1/stego/encode")
async def stego_encode(
    cover: UploadFile = File(...),
    message: str = Form(...),
    compress: bool = Form(True)
):
    """Hide message in cover file"""
    try:
        # Save cover file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(cover.filename)[1]) as temp_cover:
            shutil.copyfileobj(cover.file, temp_cover)
            cover_path = temp_cover.name
        
        # Create output file
        output_path = tempfile.mktemp(suffix=os.path.splitext(cover.filename)[1])
        
        # Encode based on file type
        if cover.filename.lower().endswith(('.png', '.bmp')):
            result = ImageSteganography.encode(cover_path, message, output_path, compress)
        elif cover.filename.lower().endswith('.wav'):
            result = AudioSteganography.encode(cover_path, message, output_path)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
        
        # Read result file
        with open(output_path, 'rb') as f:
            content = f.read()
        
        # Cleanup
        os.unlink(cover_path)
        os.unlink(output_path)
        
        import base64
        return {
            "success": True,
            "message_size": result['message_size'],
            "output": base64.b64encode(content).decode(),
            "format": os.path.splitext(cover.filename)[1][1:]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Steganography decode endpoint
@app.post("/api/v1/stego/decode")
async def stego_decode(
    stego_file: UploadFile = File(...),
    compressed: bool = Form(True)
):
    """Extract message from stego file"""
    try:
        # Save stego file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(stego_file.filename)[1]) as temp_stego:
            shutil.copyfileobj(stego_file.file, temp_stego)
            stego_path = temp_stego.name
        
        # Decode based on file type
        if stego_file.filename.lower().endswith(('.png', '.bmp')):
            message = ImageSteganography.decode(stego_path, compressed)
        elif stego_file.filename.lower().endswith('.wav'):
            message = AudioSteganography.decode(stego_path)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
        
        # Cleanup
        os.unlink(stego_path)
        
        return {
            "success": True,
            "message": message
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# OAuth2 token endpoint (placeholder)
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """OAuth2 login endpoint (placeholder)"""
    # In production, validate credentials against database
    if form_data.username == "demo" and form_data.password == "demo123":
        return {
            "access_token": "demo_token_12345",
            "token_type": "bearer"
        }
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password"
    )

# Protected endpoint example
@app.get("/api/v1/user/profile")
async def get_profile(token: str = Depends(oauth2_scheme)):
    """Get user profile (protected endpoint)"""
    # In production, validate token and get user from database
    return {
        "username": "demo_user",
        "email": "demo@example.com",
        "subscription": "pro"
    }

def run_server(host="0.0.0.0", port=8000):
    """Run the FastAPI server"""
    print(f"Starting Secure CipherStegno API v{__version__}")
    print(f"Server: http://{host}:{port}")
    print(f"Documentation: http://{host}:{port}/api/docs")
    
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    run_server()
