"""
Modern Cipher Implementations
Includes Blowfish, DES, 3DES encryption algorithms
"""

from Crypto.Cipher import Blowfish, DES3
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import hashlib
import base64


class BlowfishCipher:
    """Blowfish cipher - fast block cipher designed by Bruce Schneier"""
    
    def __init__(self, key=None):
        """
        Initialize Blowfish cipher
        
        Args:
            key (bytes or str): Key for Blowfish (4-56 bytes, default 16)
        """
        if key is None:
            self.key = get_random_bytes(16)
        elif isinstance(key, str):
            # Derive key from password using SHA-256, truncate to 32 bytes
            derived = hashlib.sha256(key.encode()).digest()
            self.key = derived[:32]  # Blowfish supports up to 56 bytes, we use 32
        else:
            if len(key) < 4 or len(key) > 56:
                raise ValueError("Blowfish key must be between 4 and 56 bytes")
            self.key = key
    
    def encrypt(self, plaintext):
        """
        Encrypt plaintext using Blowfish in CBC mode
        
        Args:
            plaintext (str or bytes): Data to encrypt
            
        Returns:
            dict: Contains 'ciphertext', 'iv', and 'key'
        """
        if isinstance(plaintext, str):
            plaintext = plaintext.encode('utf-8')
        
        cipher = Blowfish.new(self.key, Blowfish.MODE_CBC)
        ciphertext = cipher.encrypt(pad(plaintext, Blowfish.block_size))
        
        return {
            'ciphertext': base64.b64encode(ciphertext).decode('utf-8'),
            'iv': base64.b64encode(cipher.iv).decode('utf-8'),
            'key': base64.b64encode(self.key).decode('utf-8')
        }
    
    def decrypt(self, ciphertext_b64, iv_b64):
        """
        Decrypt ciphertext using Blowfish
        
        Args:
            ciphertext_b64 (str): Base64 encoded ciphertext
            iv_b64 (str): Base64 encoded initialization vector
            
        Returns:
            str: Decrypted plaintext
        """
        ciphertext = base64.b64decode(ciphertext_b64)
        iv = base64.b64decode(iv_b64)
        
        cipher = Blowfish.new(self.key, Blowfish.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext), Blowfish.block_size)
        
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
        cipher = BlowfishCipher(password)
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
        cipher = BlowfishCipher(password)
        return cipher.decrypt(ciphertext_b64, iv_b64)


class DES3Cipher:
    """Triple DES cipher - applies DES three times for enhanced security"""
    
    def __init__(self, key=None):
        """
        Initialize 3DES cipher
        
        Args:
            key (bytes or str): Key for 3DES (must be 16 or 24 bytes)
        """
        if key is None:
            self.key = DES3.adjust_key_parity(get_random_bytes(24))
        elif isinstance(key, str):
            # Derive key from password using SHA-256
            derived = hashlib.sha256(key.encode()).digest()
            # Take first 24 bytes and adjust parity
            self.key = DES3.adjust_key_parity(derived[:24])
        else:
            if len(key) not in [16, 24]:
                raise ValueError("3DES key must be 16 or 24 bytes")
            self.key = DES3.adjust_key_parity(key)
    
    def encrypt(self, plaintext):
        """
        Encrypt plaintext using 3DES in CBC mode
        
        Args:
            plaintext (str or bytes): Data to encrypt
            
        Returns:
            dict: Contains 'ciphertext', 'iv', and 'key'
        """
        if isinstance(plaintext, str):
            plaintext = plaintext.encode('utf-8')
        
        cipher = DES3.new(self.key, DES3.MODE_CBC)
        ciphertext = cipher.encrypt(pad(plaintext, DES3.block_size))
        
        return {
            'ciphertext': base64.b64encode(ciphertext).decode('utf-8'),
            'iv': base64.b64encode(cipher.iv).decode('utf-8'),
            'key': base64.b64encode(self.key).decode('utf-8')
        }
    
    def decrypt(self, ciphertext_b64, iv_b64):
        """
        Decrypt ciphertext using 3DES
        
        Args:
            ciphertext_b64 (str): Base64 encoded ciphertext
            iv_b64 (str): Base64 encoded initialization vector
            
        Returns:
            str: Decrypted plaintext
        """
        ciphertext = base64.b64decode(ciphertext_b64)
        iv = base64.b64decode(iv_b64)
        
        cipher = DES3.new(self.key, DES3.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext), DES3.block_size)
        
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
        cipher = DES3Cipher(password)
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
        cipher = DES3Cipher(password)
        return cipher.decrypt(ciphertext_b64, iv_b64)


class ChaCha20Cipher:
    """ChaCha20 stream cipher - modern, fast, and secure"""
    
    def __init__(self, key=None):
        """
        Initialize ChaCha20 cipher
        
        Args:
            key (bytes or str): Key for ChaCha20 (must be 32 bytes)
        """
        if key is None:
            self.key = get_random_bytes(32)
        elif isinstance(key, str):
            # Derive key from password using SHA-256
            self.key = hashlib.sha256(key.encode()).digest()
        else:
            if len(key) != 32:
                raise ValueError("ChaCha20 key must be 32 bytes")
            self.key = key
    
    def encrypt(self, plaintext):
        """
        Encrypt plaintext using ChaCha20
        
        Args:
            plaintext (str or bytes): Data to encrypt
            
        Returns:
            dict: Contains 'ciphertext', 'nonce', and 'key'
        """
        from Crypto.Cipher import ChaCha20
        
        if isinstance(plaintext, str):
            plaintext = plaintext.encode('utf-8')
        
        cipher = ChaCha20.new(key=self.key)
        ciphertext = cipher.encrypt(plaintext)
        
        return {
            'ciphertext': base64.b64encode(ciphertext).decode('utf-8'),
            'nonce': base64.b64encode(cipher.nonce).decode('utf-8'),
            'key': base64.b64encode(self.key).decode('utf-8')
        }
    
    def decrypt(self, ciphertext_b64, nonce_b64):
        """
        Decrypt ciphertext using ChaCha20
        
        Args:
            ciphertext_b64 (str): Base64 encoded ciphertext
            nonce_b64 (str): Base64 encoded nonce
            
        Returns:
            str: Decrypted plaintext
        """
        from Crypto.Cipher import ChaCha20
        
        ciphertext = base64.b64decode(ciphertext_b64)
        nonce = base64.b64decode(nonce_b64)
        
        cipher = ChaCha20.new(key=self.key, nonce=nonce)
        plaintext = cipher.decrypt(ciphertext)
        
        return plaintext.decode('utf-8')
    
    @staticmethod
    def encrypt_with_password(plaintext, password):
        """
        Convenience method to encrypt with password
        
        Args:
            plaintext (str): Text to encrypt
            password (str): Password to derive key from
            
        Returns:
            dict: Encrypted data with nonce
        """
        cipher = ChaCha20Cipher(password)
        return cipher.encrypt(plaintext)
    
    @staticmethod
    def decrypt_with_password(ciphertext_b64, nonce_b64, password):
        """
        Convenience method to decrypt with password
        
        Args:
            ciphertext_b64 (str): Base64 encoded ciphertext
            nonce_b64 (str): Base64 encoded nonce
            password (str): Password to derive key from
            
        Returns:
            str: Decrypted text
        """
        cipher = ChaCha20Cipher(password)
        return cipher.decrypt(ciphertext_b64, nonce_b64)
