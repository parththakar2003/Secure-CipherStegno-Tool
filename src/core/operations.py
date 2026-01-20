"""
Core operations module
Unified business logic for cryptography, steganography, and security operations
Used by all interfaces: GUI (Tkinter), CLI, and Web
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from src.crypto import (CaesarCipher, AESCipher, RSACipher, VigenereCipher,
                        PlayfairCipher, RailFenceCipher, BlowfishCipher,
                        DES3Cipher, ChaCha20Cipher)
from src.steganography import ImageSteganography, AudioSteganography, VideoSteganography
from src.utils import PasswordValidator, calculate_file_hash, Logger


class CryptoOperations:
    """Unified cryptography operations"""
    
    @staticmethod
    def encrypt(text, algorithm, key=None, shift=3):
        """
        Encrypt text using specified algorithm
        
        Args:
            text: Plain text to encrypt
            algorithm: Algorithm name (caesar, vigenere, aes, rsa, etc.)
            key: Encryption key (required for most algorithms)
            shift: Shift value (for Caesar cipher)
            
        Returns:
            dict: {
                'success': bool,
                'ciphertext': str,
                'algorithm': str,
                'iv': str (optional, for AES),
                'public_key': str (optional, for RSA),
                'error': str (optional)
            }
        """
        try:
            algorithm = algorithm.lower()
            
            if algorithm == "caesar":
                ciphertext = CaesarCipher.encrypt(text, shift)
                return {
                    'success': True,
                    'ciphertext': ciphertext,
                    'algorithm': 'caesar'
                }
            
            elif algorithm == "vigenere":
                if not key:
                    return {'success': False, 'error': 'Key required for Vigenère cipher'}
                ciphertext = VigenereCipher.encrypt(text, key)
                return {
                    'success': True,
                    'ciphertext': ciphertext,
                    'algorithm': 'vigenere'
                }
            
            elif algorithm == "playfair":
                if not key:
                    return {'success': False, 'error': 'Key required for Playfair cipher'}
                ciphertext = PlayfairCipher.encrypt(text, key)
                return {
                    'success': True,
                    'ciphertext': ciphertext,
                    'algorithm': 'playfair'
                }
            
            elif algorithm == "railfence":
                if not key:
                    key = "3"  # default rails
                rails = int(key)
                ciphertext = RailFenceCipher.encrypt(text, rails)
                return {
                    'success': True,
                    'ciphertext': ciphertext,
                    'algorithm': 'railfence',
                    'rails': rails
                }
            
            elif algorithm == "aes":
                if not key:
                    return {'success': False, 'error': 'Password required for AES'}
                result = AESCipher.encrypt_with_password(text, key)
                return {
                    'success': True,
                    'ciphertext': result['ciphertext'],
                    'iv': result['iv'],
                    'algorithm': 'aes'
                }
            
            elif algorithm == "blowfish":
                if not key:
                    return {'success': False, 'error': 'Key required for Blowfish'}
                result = BlowfishCipher.encrypt(text, key)
                return {
                    'success': True,
                    'ciphertext': result['ciphertext'],
                    'iv': result['iv'],
                    'algorithm': 'blowfish'
                }
            
            elif algorithm == "des3" or algorithm == "3des":
                if not key:
                    return {'success': False, 'error': 'Key required for 3DES'}
                result = DES3Cipher.encrypt(text, key)
                return {
                    'success': True,
                    'ciphertext': result['ciphertext'],
                    'iv': result['iv'],
                    'algorithm': 'des3'
                }
            
            elif algorithm == "chacha20":
                if not key:
                    return {'success': False, 'error': 'Key required for ChaCha20'}
                result = ChaCha20Cipher.encrypt(text, key)
                return {
                    'success': True,
                    'ciphertext': result['ciphertext'],
                    'nonce': result['nonce'],
                    'algorithm': 'chacha20'
                }
            
            elif algorithm == "rsa":
                result = RSACipher.encrypt(text)
                return {
                    'success': True,
                    'ciphertext': result['ciphertext'],
                    'public_key': result['public_key'],
                    'private_key': result['private_key'],
                    'algorithm': 'rsa'
                }
            
            else:
                return {'success': False, 'error': f'Unsupported algorithm: {algorithm}'}
        
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def decrypt(ciphertext, algorithm, key=None, shift=3, iv=None, nonce=None, private_key=None):
        """
        Decrypt ciphertext using specified algorithm
        
        Args:
            ciphertext: Encrypted text
            algorithm: Algorithm name
            key: Decryption key
            shift: Shift value (for Caesar)
            iv: Initialization vector (for AES, Blowfish, 3DES)
            nonce: Nonce (for ChaCha20)
            private_key: Private key (for RSA)
            
        Returns:
            dict: {
                'success': bool,
                'plaintext': str,
                'algorithm': str,
                'error': str (optional)
            }
        """
        try:
            algorithm = algorithm.lower()
            
            if algorithm == "caesar":
                plaintext = CaesarCipher.decrypt(ciphertext, shift)
                return {
                    'success': True,
                    'plaintext': plaintext,
                    'algorithm': 'caesar'
                }
            
            elif algorithm == "vigenere":
                if not key:
                    return {'success': False, 'error': 'Key required'}
                plaintext = VigenereCipher.decrypt(ciphertext, key)
                return {
                    'success': True,
                    'plaintext': plaintext,
                    'algorithm': 'vigenere'
                }
            
            elif algorithm == "playfair":
                if not key:
                    return {'success': False, 'error': 'Key required'}
                plaintext = PlayfairCipher.decrypt(ciphertext, key)
                return {
                    'success': True,
                    'plaintext': plaintext,
                    'algorithm': 'playfair'
                }
            
            elif algorithm == "railfence":
                if not key:
                    key = "3"  # default rails
                rails = int(key)
                plaintext = RailFenceCipher.decrypt(ciphertext, rails)
                return {
                    'success': True,
                    'plaintext': plaintext,
                    'algorithm': 'railfence'
                }
            
            elif algorithm == "aes":
                if not key or not iv:
                    return {'success': False, 'error': 'Password and IV required'}
                plaintext = AESCipher.decrypt_with_password(ciphertext, iv, key)
                return {
                    'success': True,
                    'plaintext': plaintext,
                    'algorithm': 'aes'
                }
            
            elif algorithm == "blowfish":
                if not key or not iv:
                    return {'success': False, 'error': 'Key and IV required'}
                plaintext = BlowfishCipher.decrypt(ciphertext, key, iv)
                return {
                    'success': True,
                    'plaintext': plaintext,
                    'algorithm': 'blowfish'
                }
            
            elif algorithm == "des3" or algorithm == "3des":
                if not key or not iv:
                    return {'success': False, 'error': 'Key and IV required'}
                plaintext = DES3Cipher.decrypt(ciphertext, key, iv)
                return {
                    'success': True,
                    'plaintext': plaintext,
                    'algorithm': 'des3'
                }
            
            elif algorithm == "chacha20":
                if not key or not nonce:
                    return {'success': False, 'error': 'Key and nonce required'}
                plaintext = ChaCha20Cipher.decrypt(ciphertext, key, nonce)
                return {
                    'success': True,
                    'plaintext': plaintext,
                    'algorithm': 'chacha20'
                }
            
            elif algorithm == "rsa":
                if not private_key:
                    return {'success': False, 'error': 'Private key required'}
                plaintext = RSACipher.decrypt(ciphertext, private_key)
                return {
                    'success': True,
                    'plaintext': plaintext,
                    'algorithm': 'rsa'
                }
            
            else:
                return {'success': False, 'error': f'Unsupported algorithm: {algorithm}'}
        
        except Exception as e:
            return {'success': False, 'error': str(e)}


class SteganographyOperations:
    """Unified steganography operations"""
    
    @staticmethod
    def encode(cover_path, message, output_path, file_type='image', compress=True):
        """
        Hide message in cover file
        
        Args:
            cover_path: Path to cover file
            message: Message to hide
            output_path: Path to save stego file
            file_type: Type of file (image, audio, video)
            compress: Whether to compress message
            
        Returns:
            dict: {
                'success': bool,
                'output_path': str,
                'message_size': int,
                'capacity': int (optional),
                'error': str (optional)
            }
        """
        try:
            if file_type == 'image':
                result = ImageSteganography.encode(cover_path, message, output_path, compress)
                return {
                    'success': True,
                    'output_path': output_path,
                    'message_size': result['message_size'],
                    'capacity': result.get('capacity')
                }
            
            elif file_type == 'audio':
                result = AudioSteganography.encode(cover_path, message, output_path)
                return {
                    'success': True,
                    'output_path': output_path,
                    'message_size': result['message_size']
                }
            
            elif file_type == 'video':
                result = VideoSteganography.encode(cover_path, message, output_path)
                return {
                    'success': True,
                    'output_path': output_path,
                    'message_size': result['message_size']
                }
            
            else:
                return {'success': False, 'error': f'Unsupported file type: {file_type}'}
        
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def decode(stego_path, file_type='image', compressed=True):
        """
        Extract message from stego file
        
        Args:
            stego_path: Path to stego file
            file_type: Type of file (image, audio, video)
            compressed: Whether message is compressed
            
        Returns:
            dict: {
                'success': bool,
                'message': str,
                'error': str (optional)
            }
        """
        try:
            if file_type == 'image':
                message = ImageSteganography.decode(stego_path, compressed)
                return {
                    'success': True,
                    'message': message
                }
            
            elif file_type == 'audio':
                message = AudioSteganography.decode(stego_path)
                return {
                    'success': True,
                    'message': message
                }
            
            elif file_type == 'video':
                message = VideoSteganography.decode(stego_path)
                return {
                    'success': True,
                    'message': message
                }
            
            else:
                return {'success': False, 'error': f'Unsupported file type: {file_type}'}
        
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def check_capacity(cover_path, file_type='image'):
        """
        Check how much data can be hidden in cover file
        
        Args:
            cover_path: Path to cover file
            file_type: Type of file
            
        Returns:
            dict: {
                'success': bool,
                'capacity_bytes': int,
                'capacity_chars': int,
                'error': str (optional)
            }
        """
        try:
            if file_type == 'image':
                capacity = ImageSteganography.check_capacity(cover_path)
                return {
                    'success': True,
                    'capacity_bytes': capacity,
                    'capacity_chars': capacity
                }
            
            elif file_type == 'audio':
                capacity = AudioSteganography.check_capacity(cover_path)
                return {
                    'success': True,
                    'capacity_bytes': capacity,
                    'capacity_chars': capacity
                }
            
            else:
                return {'success': False, 'error': f'Capacity check not supported for: {file_type}'}
        
        except Exception as e:
            return {'success': False, 'error': str(e)}


class SecurityOperations:
    """Unified security operations"""
    
    @staticmethod
    def validate_password(password):
        """
        Validate password strength
        
        Returns:
            dict: {
                'success': bool,
                'strength': str,
                'score': int,
                'feedback': list,
                'requirements_met': dict
            }
        """
        try:
            result = PasswordValidator.validate_strength(password)
            return {
                'success': True,
                **result
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def generate_password(length=16):
        """
        Generate strong password
        
        Returns:
            dict: {
                'success': bool,
                'password': str,
                'strength': str,
                'score': int
            }
        """
        try:
            password = PasswordValidator.generate_strong_password(length)
            validation = PasswordValidator.validate_strength(password)
            return {
                'success': True,
                'password': password,
                'strength': validation['strength'],
                'score': validation['score']
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def calculate_hash(file_path, algorithm='sha256'):
        """
        Calculate file hash
        
        Returns:
            dict: {
                'success': bool,
                'hash': str,
                'algorithm': str,
                'file_size': int
            }
        """
        try:
            file_hash = calculate_file_hash(file_path, algorithm)
            file_size = os.path.getsize(file_path)
            return {
                'success': True,
                'hash': file_hash,
                'algorithm': algorithm,
                'file_size': file_size
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
