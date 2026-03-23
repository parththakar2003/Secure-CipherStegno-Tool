"""
Unit tests for cryptography module
"""

import unittest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.crypto import CaesarCipher, AESCipher, RSACipher


class TestCaesarCipher(unittest.TestCase):
    """Test Caesar cipher functionality"""
    
    def test_encrypt_decrypt(self):
        """Test basic encryption and decryption"""
        plaintext = "Hello World 123"
        shift = 5
        
        encrypted = CaesarCipher.encrypt(plaintext, shift)
        decrypted = CaesarCipher.decrypt(encrypted, shift)
        
        self.assertEqual(decrypted, plaintext)
    
    def test_encrypt_uppercase(self):
        """Test uppercase encryption"""
        plaintext = "ABC"
        shift = 3
        expected = "DEF"
        
        encrypted = CaesarCipher.encrypt(plaintext, shift)
        self.assertEqual(encrypted, expected)
    
    def test_encrypt_lowercase(self):
        """Test lowercase encryption"""
        plaintext = "xyz"
        shift = 3
        expected = "abc"
        
        encrypted = CaesarCipher.encrypt(plaintext, shift)
        self.assertEqual(encrypted, expected)
    
    def test_special_characters(self):
        """Test that special characters are preserved"""
        plaintext = "Hello, World!"
        shift = 5
        
        encrypted = CaesarCipher.encrypt(plaintext, shift)
        self.assertIn(',', encrypted)
        self.assertIn('!', encrypted)


class TestAESCipher(unittest.TestCase):
    """Test AES cipher functionality"""
    
    def test_encrypt_decrypt_with_password(self):
        """Test encryption and decryption with password"""
        plaintext = "This is a secret message"
        password = "strongpassword123"
        
        result = AESCipher.encrypt_with_password(plaintext, password)
        decrypted = AESCipher.decrypt_with_password(
            result['ciphertext'],
            result['iv'],
            password
        )
        
        self.assertEqual(decrypted, plaintext)
    
    def test_encrypt_decrypt_with_key_object(self):
        """Test encryption and decryption with cipher object"""
        plaintext = "Another secret message"
        password = "mypassword"
        
        cipher = AESCipher(password)
        result = cipher.encrypt(plaintext)
        decrypted = cipher.decrypt(result['ciphertext'], result['iv'])
        
        self.assertEqual(decrypted, plaintext)
    
    def test_different_passwords_fail(self):
        """Test that wrong password fails decryption"""
        plaintext = "Secret"
        password1 = "password1"
        password2 = "password2"
        
        result = AESCipher.encrypt_with_password(plaintext, password1)
        
        with self.assertRaises(Exception):
            AESCipher.decrypt_with_password(
                result['ciphertext'],
                result['iv'],
                password2
            )


class TestRSACipher(unittest.TestCase):
    """Test RSA cipher functionality"""
    
    def test_generate_key_pair(self):
        """Test RSA key pair generation"""
        cipher = RSACipher(key_size=2048)
        keys = cipher.generate_key_pair()
        
        self.assertIn('public_key', keys)
        self.assertIn('private_key', keys)
        self.assertIn('BEGIN PUBLIC KEY', keys['public_key'])
        self.assertIn('BEGIN RSA PRIVATE KEY', keys['private_key'])
    
    def test_encrypt_decrypt(self):
        """Test RSA encryption and decryption"""
        plaintext = "Short message"
        
        cipher = RSACipher(key_size=2048)
        cipher.generate_key_pair()
        
        encrypted = cipher.encrypt(plaintext)
        decrypted = cipher.decrypt(encrypted)
        
        self.assertEqual(decrypted, plaintext)
    
    def test_load_keys(self):
        """Test loading keys from PEM format"""
        cipher1 = RSACipher()
        keys = cipher1.generate_key_pair()
        
        cipher2 = RSACipher()
        cipher2.load_public_key(keys['public_key'])
        cipher2.load_private_key(keys['private_key'])
        
        plaintext = "Test message"
        encrypted = cipher2.encrypt(plaintext)
        decrypted = cipher2.decrypt(encrypted)
        
        self.assertEqual(decrypted, plaintext)


if __name__ == '__main__':
    unittest.main()
