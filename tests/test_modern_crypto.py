"""
Unit tests for modern cipher implementations
"""

import unittest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.crypto.modern import BlowfishCipher, DES3Cipher, ChaCha20Cipher


class TestBlowfishCipher(unittest.TestCase):
    """Test Blowfish cipher functionality"""
    
    def test_encrypt_decrypt_with_password(self):
        """Test encryption and decryption with password"""
        plaintext = "This is a secret message for Blowfish"
        password = "strongpassword123"
        
        result = BlowfishCipher.encrypt_with_password(plaintext, password)
        decrypted = BlowfishCipher.decrypt_with_password(
            result['ciphertext'],
            result['iv'],
            password
        )
        
        self.assertEqual(decrypted, plaintext)
    
    def test_different_passwords_fail(self):
        """Test that wrong password fails decryption"""
        plaintext = "Secret"
        password1 = "password1"
        password2 = "password2"
        
        result = BlowfishCipher.encrypt_with_password(plaintext, password1)
        
        with self.assertRaises(Exception):
            BlowfishCipher.decrypt_with_password(
                result['ciphertext'],
                result['iv'],
                password2
            )
    
    def test_encrypt_decrypt_with_object(self):
        """Test encryption with cipher object"""
        plaintext = "Another test message"
        password = "mypassword"
        
        cipher = BlowfishCipher(password)
        result = cipher.encrypt(plaintext)
        decrypted = cipher.decrypt(result['ciphertext'], result['iv'])
        
        self.assertEqual(decrypted, plaintext)


class TestDES3Cipher(unittest.TestCase):
    """Test 3DES cipher functionality"""
    
    def test_encrypt_decrypt_with_password(self):
        """Test encryption and decryption with password"""
        plaintext = "This is a 3DES encrypted message"
        password = "securepassword456"
        
        result = DES3Cipher.encrypt_with_password(plaintext, password)
        decrypted = DES3Cipher.decrypt_with_password(
            result['ciphertext'],
            result['iv'],
            password
        )
        
        self.assertEqual(decrypted, plaintext)
    
    def test_encrypt_decrypt_with_object(self):
        """Test encryption with cipher object"""
        plaintext = "3DES test message"
        password = "testpass"
        
        cipher = DES3Cipher(password)
        result = cipher.encrypt(plaintext)
        decrypted = cipher.decrypt(result['ciphertext'], result['iv'])
        
        self.assertEqual(decrypted, plaintext)
    
    def test_different_passwords_fail(self):
        """Test that wrong password fails decryption"""
        plaintext = "Secret 3DES"
        password1 = "password1"
        password2 = "password2"
        
        result = DES3Cipher.encrypt_with_password(plaintext, password1)
        
        with self.assertRaises(Exception):
            DES3Cipher.decrypt_with_password(
                result['ciphertext'],
                result['iv'],
                password2
            )


class TestChaCha20Cipher(unittest.TestCase):
    """Test ChaCha20 cipher functionality"""
    
    def test_encrypt_decrypt_with_password(self):
        """Test encryption and decryption with password"""
        plaintext = "ChaCha20 is a modern stream cipher"
        password = "chacha20password"
        
        result = ChaCha20Cipher.encrypt_with_password(plaintext, password)
        decrypted = ChaCha20Cipher.decrypt_with_password(
            result['ciphertext'],
            result['nonce'],
            password
        )
        
        self.assertEqual(decrypted, plaintext)
    
    def test_encrypt_decrypt_with_object(self):
        """Test encryption with cipher object"""
        plaintext = "ChaCha20 test message"
        password = "testpass123"
        
        cipher = ChaCha20Cipher(password)
        result = cipher.encrypt(plaintext)
        decrypted = cipher.decrypt(result['ciphertext'], result['nonce'])
        
        self.assertEqual(decrypted, plaintext)
    
    def test_different_passwords_fail(self):
        """Test that wrong password fails decryption"""
        plaintext = "Secret ChaCha20"
        password1 = "password1"
        password2 = "password2"
        
        result = ChaCha20Cipher.encrypt_with_password(plaintext, password1)
        
        with self.assertRaises(Exception):
            ChaCha20Cipher.decrypt_with_password(
                result['ciphertext'],
                result['nonce'],
                password2
            )
    
    def test_long_message(self):
        """Test encryption of longer messages"""
        plaintext = "A" * 1000  # 1000 character message
        password = "longmessagetest"
        
        result = ChaCha20Cipher.encrypt_with_password(plaintext, password)
        decrypted = ChaCha20Cipher.decrypt_with_password(
            result['ciphertext'],
            result['nonce'],
            password
        )
        
        self.assertEqual(decrypted, plaintext)


class TestClassicalCiphers(unittest.TestCase):
    """Test classical cipher implementations"""
    
    def test_vigenere_encrypt_decrypt(self):
        """Test Vigenère cipher"""
        from src.crypto.classical import VigenereCipher
        
        plaintext = "HELLO WORLD"
        key = "KEY"
        
        encrypted = VigenereCipher.encrypt(plaintext, key)
        decrypted = VigenereCipher.decrypt(encrypted, key)
        
        self.assertEqual(decrypted.upper(), plaintext.upper())
    
    def test_playfair_encrypt_decrypt(self):
        """Test Playfair cipher"""
        from src.crypto.classical import PlayfairCipher
        
        plaintext = "HELLO WORLD"
        key = "KEYWORD"
        
        encrypted = PlayfairCipher.encrypt(plaintext, key)
        decrypted = PlayfairCipher.decrypt(encrypted, key)
        
        # Playfair may add padding, so check if original is in result
        self.assertIn("HELLO", decrypted.upper())
    
    def test_railfence_encrypt_decrypt(self):
        """Test Rail Fence cipher"""
        from src.crypto.classical import RailFenceCipher
        
        plaintext = "HELLO WORLD"
        rails = 3
        
        encrypted = RailFenceCipher.encrypt(plaintext, rails)
        decrypted = RailFenceCipher.decrypt(encrypted, rails)
        
        self.assertEqual(decrypted, plaintext)


if __name__ == '__main__':
    unittest.main()
