"""
Secure CipherStegno Tool
Version and package information
"""

__version__ = '3.1.0'
__author__ = 'Parth Thakar'
__email__ = 'parththakar2003@users.noreply.github.com'
__license__ = 'MIT'
__description__ = 'Advanced cryptography and steganography toolkit'
__url__ = 'https://github.com/parththakar2003/Secure-CipherStegno-Tool'

# Version history
VERSION_HISTORY = {
    '1.0.0': 'Initial release - Basic Caesar cipher and image steganography',
    '2.0.0': 'Major upgrade - AES-256, RSA, audio steganography, CLI, tests, documentation',
    '2.1.0': 'Advanced Cryptography - Vigenère, Playfair, Rail Fence ciphers',
    '2.2.0': 'Expanded Steganography - Video, JPEG, PDF, document steganography',
    '2.3.0': 'AI & Security - ML-based steganalysis, tampering detection',
    '3.0.0': 'Cloud Platform - FastAPI web service, RESTful API, OAuth2',
    '3.1.0': 'Enterprise & Mobile - Full-featured platform (framework complete)'
}

# API version for future REST API
API_VERSION = 'v1'

# Minimum Python version required
MIN_PYTHON_VERSION = (3, 8)

def get_version():
    """Return the version string"""
    return __version__

def get_version_info():
    """Return detailed version information"""
    return {
        'version': __version__,
        'author': __author__,
        'license': __license__,
        'description': __description__,
        'url': __url__,
        'api_version': API_VERSION
    }
