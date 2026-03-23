"""
Unit tests for CryptoOperations in core/operations.py
Tests Blowfish, 3DES, ChaCha20, and RSA encryption/decryption
"""

import unittest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.operations import CryptoOperations


class TestBlowfishOperations(unittest.TestCase):
    """Test Blowfish operations through CryptoOperations"""
    
    def test_encrypt_decrypt(self):
        """Test Blowfish encryption and decryption"""
        plaintext = "This is a secret message for Blowfish"
        password = "strongpassword123"
        
        # Encrypt
        encrypt_result = CryptoOperations.encrypt(plaintext, "blowfish", key=password)
        self.assertTrue(encrypt_result['success'])
        self.assertIn('ciphertext', encrypt_result)
        self.assertIn('iv', encrypt_result)
        
        # Decrypt
        decrypt_result = CryptoOperations.decrypt(
            encrypt_result['ciphertext'],
            "blowfish",
            key=password,
            iv=encrypt_result['iv']
        )
        self.assertTrue(decrypt_result['success'])
        self.assertEqual(decrypt_result['plaintext'], plaintext)
    
    def test_wrong_password(self):
        """Test that wrong password fails decryption"""
        plaintext = "Secret message"
        password1 = "password1"
        password2 = "password2"
        
        encrypt_result = CryptoOperations.encrypt(plaintext, "blowfish", key=password1)
        decrypt_result = CryptoOperations.decrypt(
            encrypt_result['ciphertext'],
            "blowfish",
            key=password2,
            iv=encrypt_result['iv']
        )
        
        # Decryption should fail with wrong password
        self.assertFalse(decrypt_result['success'])


class TestDES3Operations(unittest.TestCase):
    """Test 3DES operations through CryptoOperations"""
    
    def test_encrypt_decrypt_3des(self):
        """Test 3DES encryption with '3des' algorithm name"""
        plaintext = "This is a 3DES encrypted message"
        password = "securepassword456"
        
        # Encrypt
        encrypt_result = CryptoOperations.encrypt(plaintext, "3des", key=password)
        self.assertTrue(encrypt_result['success'])
        self.assertIn('ciphertext', encrypt_result)
        self.assertIn('iv', encrypt_result)
        
        # Decrypt
        decrypt_result = CryptoOperations.decrypt(
            encrypt_result['ciphertext'],
            "3des",
            key=password,
            iv=encrypt_result['iv']
        )
        self.assertTrue(decrypt_result['success'])
        self.assertEqual(decrypt_result['plaintext'], plaintext)
    
    def test_encrypt_decrypt_des3(self):
        """Test 3DES encryption with 'des3' algorithm name"""
        plaintext = "DES3 test message"
        password = "testpass"
        
        # Encrypt
        encrypt_result = CryptoOperations.encrypt(plaintext, "des3", key=password)
        self.assertTrue(encrypt_result['success'])
        
        # Decrypt
        decrypt_result = CryptoOperations.decrypt(
            encrypt_result['ciphertext'],
            "des3",
            key=password,
            iv=encrypt_result['iv']
        )
        self.assertTrue(decrypt_result['success'])
        self.assertEqual(decrypt_result['plaintext'], plaintext)
    
    def test_wrong_password(self):
        """Test that wrong password fails decryption"""
        plaintext = "Secret 3DES"
        password1 = "password1"
        password2 = "password2"
        
        encrypt_result = CryptoOperations.encrypt(plaintext, "3des", key=password1)
        decrypt_result = CryptoOperations.decrypt(
            encrypt_result['ciphertext'],
            "3des",
            key=password2,
            iv=encrypt_result['iv']
        )
        
        # Decryption should fail with wrong password
        self.assertFalse(decrypt_result['success'])


class TestChaCha20Operations(unittest.TestCase):
    """Test ChaCha20 operations through CryptoOperations"""
    
    def test_encrypt_decrypt(self):
        """Test ChaCha20 encryption and decryption"""
        plaintext = "ChaCha20 is a modern stream cipher"
        password = "chacha20password"
        
        # Encrypt
        encrypt_result = CryptoOperations.encrypt(plaintext, "chacha20", key=password)
        self.assertTrue(encrypt_result['success'])
        self.assertIn('ciphertext', encrypt_result)
        self.assertIn('nonce', encrypt_result)
        
        # Decrypt
        decrypt_result = CryptoOperations.decrypt(
            encrypt_result['ciphertext'],
            "chacha20",
            key=password,
            nonce=encrypt_result['nonce']
        )
        self.assertTrue(decrypt_result['success'])
        self.assertEqual(decrypt_result['plaintext'], plaintext)
    
    def test_long_message(self):
        """Test encryption of longer messages"""
        plaintext = "A" * 1000  # 1000 character message
        password = "longmessagetest"
        
        encrypt_result = CryptoOperations.encrypt(plaintext, "chacha20", key=password)
        self.assertTrue(encrypt_result['success'])
        
        decrypt_result = CryptoOperations.decrypt(
            encrypt_result['ciphertext'],
            "chacha20",
            key=password,
            nonce=encrypt_result['nonce']
        )
        self.assertTrue(decrypt_result['success'])
        self.assertEqual(decrypt_result['plaintext'], plaintext)
    
    def test_wrong_password(self):
        """Test that wrong password fails decryption"""
        plaintext = "Secret ChaCha20"
        password1 = "password1"
        password2 = "password2"
        
        encrypt_result = CryptoOperations.encrypt(plaintext, "chacha20", key=password1)
        decrypt_result = CryptoOperations.decrypt(
            encrypt_result['ciphertext'],
            "chacha20",
            key=password2,
            nonce=encrypt_result['nonce']
        )
        
        # Decryption should fail with wrong password
        self.assertFalse(decrypt_result['success'])


class TestRSAOperations(unittest.TestCase):
    """Test RSA operations through CryptoOperations"""
    
    def test_encrypt_decrypt(self):
        """Test RSA encryption and decryption"""
        plaintext = "RSA test message"
        
        # Encrypt (generates keys automatically)
        encrypt_result = CryptoOperations.encrypt(plaintext, "rsa")
        self.assertTrue(encrypt_result['success'])
        self.assertIn('ciphertext', encrypt_result)
        self.assertIn('public_key', encrypt_result)
        self.assertIn('private_key', encrypt_result)
        
        # Decrypt
        decrypt_result = CryptoOperations.decrypt(
            encrypt_result['ciphertext'],
            "rsa",
            private_key=encrypt_result['private_key']
        )
        self.assertTrue(decrypt_result['success'])
        self.assertEqual(decrypt_result['plaintext'], plaintext)
    
    def test_short_message(self):
        """Test RSA with short message"""
        plaintext = "Hi"
        
        encrypt_result = CryptoOperations.encrypt(plaintext, "rsa")
        self.assertTrue(encrypt_result['success'])
        
        decrypt_result = CryptoOperations.decrypt(
            encrypt_result['ciphertext'],
            "rsa",
            private_key=encrypt_result['private_key']
        )
        self.assertTrue(decrypt_result['success'])
        self.assertEqual(decrypt_result['plaintext'], plaintext)
    
    def test_wrong_key(self):
        """Test that wrong private key fails decryption"""
        plaintext = "Secret RSA"
        
        # First encryption
        encrypt_result1 = CryptoOperations.encrypt(plaintext, "rsa")
        
        # Second encryption (generates different keys)
        encrypt_result2 = CryptoOperations.encrypt(plaintext, "rsa")
        
        # Try to decrypt first ciphertext with second private key
        decrypt_result = CryptoOperations.decrypt(
            encrypt_result1['ciphertext'],
            "rsa",
            private_key=encrypt_result2['private_key']
        )
        
        # Decryption should fail with wrong key
        self.assertFalse(decrypt_result['success'])


if __name__ == '__main__':
    unittest.main()
