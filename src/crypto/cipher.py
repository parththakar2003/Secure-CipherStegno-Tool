"""
Advanced Cryptography Module
Implements AES-256, RSA, and Caesar cipher encryption/decryption
"""

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64
import hashlib
import os


class CaesarCipher:
    """Caesar cipher implementation"""
    
    @staticmethod
    def encrypt(text, shift):
        """
        Encrypt text using Caesar cipher
        
        Args:
            text (str): Text to encrypt
            shift (int): Shift value
            
        Returns:
            str: Encrypted text
        """
        result = ""
        for char in text:
            if char.isalpha():
                shift_base = 65 if char.isupper() else 97
                result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
            elif char.isdigit():
                result += str((int(char) + shift) % 10)
            else:
                result += char
        return result
    
    @staticmethod
    def decrypt(text, shift):
        """
        Decrypt text using Caesar cipher
        
        Args:
            text (str): Text to decrypt
            shift (int): Shift value
            
        Returns:
            str: Decrypted text
        """
        result = ""
        for char in text:
            if char.isalpha():
                shift_base = 65 if char.isupper() else 97
                result += chr((ord(char) - shift_base - shift) % 26 + shift_base)
            elif char.isdigit():
                result += str((int(char) - shift) % 10)
            else:
                result += char
        return result


class AESCipher:
    """AES-256 encryption/decryption"""
    
    def __init__(self, key=None):
        """
        Initialize AES cipher
        
        Args:
            key (bytes, optional): 32-byte key for AES-256. Generated if not provided.
        """
        if key is None:
            self.key = get_random_bytes(32)
        elif isinstance(key, str):
            # Derive key from password using SHA-256
            self.key = hashlib.sha256(key.encode()).digest()
        else:
            if len(key) != 32:
                raise ValueError("Key must be 32 bytes for AES-256")
            self.key = key
    
    def encrypt(self, plaintext):
        """
        Encrypt plaintext using AES-256 in CBC mode
        
        Args:
            plaintext (str or bytes): Data to encrypt
            
        Returns:
            dict: Contains 'ciphertext', 'iv', and 'key'
        """
        if isinstance(plaintext, str):
            plaintext = plaintext.encode('utf-8')
        
        cipher = AES.new(self.key, AES.MODE_CBC)
        ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
        
        return {
            'ciphertext': base64.b64encode(ciphertext).decode('utf-8'),
            'iv': base64.b64encode(cipher.iv).decode('utf-8'),
            'key': base64.b64encode(self.key).decode('utf-8')
        }
    
    def decrypt(self, ciphertext_b64, iv_b64):
        """
        Decrypt ciphertext using AES-256
        
        Args:
            ciphertext_b64 (str): Base64 encoded ciphertext
            iv_b64 (str): Base64 encoded initialization vector
            
        Returns:
            str: Decrypted plaintext
        """
        ciphertext = base64.b64decode(ciphertext_b64)
        iv = base64.b64decode(iv_b64)
        
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
        
        return plaintext.decode('utf-8')
    
    @staticmethod
    def encrypt_with_password(plaintext, password):
        """
        Convenience method to encrypt with password
        
        Args:
            plaintext (str): Text to encrypt
            password (str): Password to derive key from
            
        Returns:
            dict: Encrypted data with IV
        """
        cipher = AESCipher(password)
        return cipher.encrypt(plaintext)
    
    @staticmethod
    def decrypt_with_password(ciphertext_b64, iv_b64, password):
        """
        Convenience method to decrypt with password
        
        Args:
            ciphertext_b64 (str): Base64 encoded ciphertext
            iv_b64 (str): Base64 encoded IV
            password (str): Password to derive key from
            
        Returns:
            str: Decrypted text
        """
        cipher = AESCipher(password)
        return cipher.decrypt(ciphertext_b64, iv_b64)


class RSACipher:
    """RSA encryption/decryption"""
    
    def __init__(self, key_size=2048):
        """
        Initialize RSA cipher
        
        Args:
            key_size (int): Size of RSA key (default 2048)
        """
        self.key_size = key_size
        self.key_pair = None
        self.public_key = None
        self.private_key = None
    
    def generate_key_pair(self):
        """Generate RSA key pair"""
        self.key_pair = RSA.generate(self.key_size)
        self.public_key = self.key_pair.publickey()
        self.private_key = self.key_pair
        
        return {
            'public_key': self.public_key.export_key().decode('utf-8'),
            'private_key': self.private_key.export_key().decode('utf-8')
        }
    
    def load_public_key(self, public_key_pem):
        """
        Load public key from PEM format
        
        Args:
            public_key_pem (str): PEM formatted public key
        """
        self.public_key = RSA.import_key(public_key_pem)
    
    def load_private_key(self, private_key_pem):
        """
        Load private key from PEM format
        
        Args:
            private_key_pem (str): PEM formatted private key
        """
        self.private_key = RSA.import_key(private_key_pem)
    
    def encrypt(self, plaintext):
        """
        Encrypt plaintext using RSA public key
        
        Args:
            plaintext (str or bytes): Data to encrypt
            
        Returns:
            str: Base64 encoded ciphertext
        """
        if self.public_key is None:
            raise ValueError("Public key not loaded")
        
        if isinstance(plaintext, str):
            plaintext = plaintext.encode('utf-8')
        
        cipher = PKCS1_OAEP.new(self.public_key)
        ciphertext = cipher.encrypt(plaintext)
        
        return base64.b64encode(ciphertext).decode('utf-8')
    
    def decrypt(self, ciphertext_b64):
        """
        Decrypt ciphertext using RSA private key
        
        Args:
            ciphertext_b64 (str): Base64 encoded ciphertext
            
        Returns:
            str: Decrypted plaintext
        """
        if self.private_key is None:
            raise ValueError("Private key not loaded")
        
        ciphertext = base64.b64decode(ciphertext_b64)
        cipher = PKCS1_OAEP.new(self.private_key)
        plaintext = cipher.decrypt(ciphertext)
        
        return plaintext.decode('utf-8')
    
    def save_keys(self, public_key_path, private_key_path):
        """
        Save keys to files
        
        Args:
            public_key_path (str): Path to save public key
            private_key_path (str): Path to save private key
        """
        if self.public_key is None or self.private_key is None:
            raise ValueError("Keys not generated")
        
        with open(public_key_path, 'wb') as f:
            f.write(self.public_key.export_key())
        
        with open(private_key_path, 'wb') as f:
            f.write(self.private_key.export_key())
    
    def load_keys_from_files(self, public_key_path=None, private_key_path=None):
        """
        Load keys from files
        
        Args:
            public_key_path (str, optional): Path to public key file
            private_key_path (str, optional): Path to private key file
        """
        if public_key_path and os.path.exists(public_key_path):
            with open(public_key_path, 'rb') as f:
                self.public_key = RSA.import_key(f.read())
        
        if private_key_path and os.path.exists(private_key_path):
            with open(private_key_path, 'rb') as f:
                self.private_key = RSA.import_key(f.read())


def hybrid_encrypt(plaintext, recipient_public_key_pem):
    """
    Hybrid encryption: Use AES for data, RSA for AES key
    
    Args:
        plaintext (str): Text to encrypt
        recipient_public_key_pem (str): Recipient's RSA public key
        
    Returns:
        dict: Contains encrypted data and encrypted AES key
    """
    # Encrypt data with AES
    aes_cipher = AESCipher()
    encrypted_data = aes_cipher.encrypt(plaintext)
    
    # Encrypt AES key with RSA
    rsa_cipher = RSACipher()
    rsa_cipher.load_public_key(recipient_public_key_pem)
    encrypted_key = rsa_cipher.encrypt(aes_cipher.key)
    
    return {
        'encrypted_data': encrypted_data['ciphertext'],
        'iv': encrypted_data['iv'],
        'encrypted_key': encrypted_key
    }


def hybrid_decrypt(encrypted_data, iv, encrypted_key, private_key_pem):
    """
    Hybrid decryption: Decrypt AES key with RSA, then decrypt data with AES
    
    Args:
        encrypted_data (str): Base64 encoded encrypted data
        iv (str): Base64 encoded IV
        encrypted_key (str): Base64 encoded encrypted AES key
        private_key_pem (str): Private RSA key
        
    Returns:
        str: Decrypted plaintext
    """
    # Decrypt AES key with RSA
    rsa_cipher = RSACipher()
    rsa_cipher.load_private_key(private_key_pem)
    aes_key = base64.b64decode(rsa_cipher.decrypt(encrypted_key))
    
    # Decrypt data with AES
    aes_cipher = AESCipher(aes_key)
    plaintext = aes_cipher.decrypt(encrypted_data, iv)
    
    return plaintext
