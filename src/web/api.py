"""
FastAPI Web Application (v3.1)
RESTful API and Web Interface for Secure CipherStegno Tool
"""

try:
    from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends, status, Request
    from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.staticfiles import StaticFiles
    from fastapi.templating import Jinja2Templates
    from fastapi.responses import HTMLResponse, FileResponse
    from pydantic import BaseModel
    import uvicorn
except ImportError:
    raise ImportError("FastAPI dependencies required. Install with: pip install fastapi uvicorn python-multipart jinja2")

import sys
import os
from typing import Optional, List
import tempfile
import shutil
import base64

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from src.crypto import CaesarCipher, AESCipher, RSACipher, VigenereCipher
from src.steganography import ImageSteganography, AudioSteganography
from src.utils import PasswordValidator, calculate_file_hash
from src import __version__
from src.core import CryptoOperations, SteganographyOperations, SecurityOperations

# Initialize FastAPI app
app = FastAPI(
    title="Secure CipherStegno API",
    description="RESTful API and Web Interface for cryptography and steganography operations",
    version=__version__,
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Mount static files and templates
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# CORS middleware - Environment-aware configuration
# For production, set ALLOWED_ORIGINS environment variable
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:8000,http://127.0.0.1:8000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
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
    public_key: Optional[str] = None
    private_key: Optional[str] = None
    nonce: Optional[str] = None

class DecryptRequest(BaseModel):
    ciphertext: str
    algorithm: str
    key: Optional[str] = None
    shift: Optional[int] = 3
    iv: Optional[str] = None
    nonce: Optional[str] = None
    private_key: Optional[str] = None

class PasswordValidationRequest(BaseModel):
    password: str

class PasswordGenerationRequest(BaseModel):
    length: int = 16

class HashRequest(BaseModel):
    algorithm: str = "sha256"

class User(BaseModel):
    username: str
    email: Optional[str] = None

# Web Interface Root
@app.get("/", response_class=HTMLResponse)
async def web_interface(request: Request):
    """Serve the web interface"""
    return templates.TemplateResponse("index.html", {"request": request, "version": __version__})

# API Root endpoint
@app.get("/api")
async def api_root():
    """API root endpoint"""
    return {
        "name": "Secure CipherStegno API",
        "version": __version__,
        "status": "operational",
        "endpoints": {
            "web": "/",
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
        result = CryptoOperations.encrypt(
            text=request.text,
            algorithm=request.algorithm,
            key=request.key,
            shift=request.shift or 3
        )
        
        if not result['success']:
            raise HTTPException(status_code=400, detail=result.get('error', 'Encryption failed'))
        
        return EncryptResponse(
            success=True,
            ciphertext=result['ciphertext'],
            algorithm=result['algorithm'],
            iv=result.get('iv'),
            public_key=result.get('public_key'),
            private_key=result.get('private_key'),
            nonce=result.get('nonce')
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Decryption endpoint
@app.post("/api/v1/decrypt")
async def decrypt_text(request: DecryptRequest):
    """Decrypt text using specified algorithm"""
    try:
        result = CryptoOperations.decrypt(
            ciphertext=request.ciphertext,
            algorithm=request.algorithm,
            key=request.key,
            shift=request.shift or 3,
            iv=request.iv,
            nonce=request.nonce,
            private_key=request.private_key
        )
        
        if not result['success']:
            raise HTTPException(status_code=400, detail=result.get('error', 'Decryption failed'))
        
        return {
            "success": True,
            "plaintext": result['plaintext'],
            "algorithm": result['algorithm']
        }
    
    except HTTPException:
        raise
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

# OAuth2 token endpoint (DEVELOPMENT ONLY - NOT FOR PRODUCTION)
# WARNING: This is a placeholder for development/testing purposes only
# In production, implement proper authentication with secure credential storage
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    OAuth2 login endpoint (DEVELOPMENT PLACEHOLDER)
    
    ⚠️ WARNING: This endpoint uses hardcoded credentials and is NOT secure!
    DO NOT use in production. Implement proper authentication system.
    """
    # DEVELOPMENT ONLY: These credentials are for testing purposes
    # In production: validate against secure database, use password hashing, etc.
    if form_data.username == "demo" and form_data.password == "demo123":
        return {
            "access_token": "demo_token_12345",  # Not a real JWT token
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
