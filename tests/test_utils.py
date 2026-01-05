"""
Unit tests for utility functions
"""

import unittest
import sys
import os
import tempfile

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.utils import (
    calculate_string_hash,
    PasswordValidator,
    generate_random_key,
    format_file_size
)


class TestHashFunctions(unittest.TestCase):
    """Test hash calculation functions"""
    
    def test_calculate_string_hash_sha256(self):
        """Test SHA-256 hash calculation"""
        text = "Hello World"
        hash_result = calculate_string_hash(text, 'sha256')
        
        # Known SHA-256 hash of "Hello World"
        expected = "a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e"
        self.assertEqual(hash_result, expected)
    
    def test_calculate_string_hash_md5(self):
        """Test MD5 hash calculation"""
        text = "Test"
        hash_result = calculate_string_hash(text, 'md5')
        self.assertEqual(len(hash_result), 32)  # MD5 produces 32 hex chars


class TestPasswordValidator(unittest.TestCase):
    """Test password validation"""
    
    def test_weak_password(self):
        """Test weak password detection"""
        result = PasswordValidator.validate_strength("abc")
        self.assertEqual(result['strength'], 'Weak')
        self.assertFalse(result['valid'])
    
    def test_medium_password(self):
        """Test medium password detection"""
        result = PasswordValidator.validate_strength("Password123")
        self.assertIn(result['strength'], ['Medium', 'Strong'])
    
    def test_strong_password(self):
        """Test strong password detection"""
        result = PasswordValidator.validate_strength("P@ssw0rd!2024")
        self.assertEqual(result['strength'], 'Strong')
        self.assertTrue(result['valid'])
    
    def test_common_pattern_detection(self):
        """Test detection of common patterns"""
        result = PasswordValidator.validate_strength("password123")
        self.assertIn('Avoid common patterns', result['feedback'])
    
    def test_generate_strong_password(self):
        """Test password generation"""
        password = PasswordValidator.generate_strong_password(16)
        
        self.assertEqual(len(password), 16)
        
        # Validate it's strong
        result = PasswordValidator.validate_strength(password)
        self.assertIn(result['strength'], ['Medium', 'Strong'])


class TestRandomKey(unittest.TestCase):
    """Test random key generation"""
    
    def test_generate_random_key(self):
        """Test random key generation"""
        key = generate_random_key(32)
        
        self.assertEqual(len(key), 32)
        self.assertIsInstance(key, bytes)
    
    def test_keys_are_different(self):
        """Test that generated keys are unique"""
        key1 = generate_random_key(32)
        key2 = generate_random_key(32)
        
        self.assertNotEqual(key1, key2)


class TestFormatFileSize(unittest.TestCase):
    """Test file size formatting"""
    
    def test_bytes(self):
        """Test bytes formatting"""
        result = format_file_size(500)
        self.assertIn('B', result)
    
    def test_kilobytes(self):
        """Test kilobytes formatting"""
        result = format_file_size(1024)
        self.assertIn('KB', result)
    
    def test_megabytes(self):
        """Test megabytes formatting"""
        result = format_file_size(1024 * 1024)
        self.assertIn('MB', result)
    
    def test_gigabytes(self):
        """Test gigabytes formatting"""
        result = format_file_size(1024 * 1024 * 1024)
        self.assertIn('GB', result)


if __name__ == '__main__':
    unittest.main()
