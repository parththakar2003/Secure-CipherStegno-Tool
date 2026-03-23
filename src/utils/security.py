"""
Utility functions for security operations
"""

import hashlib
import os
import re
from datetime import datetime


def calculate_file_hash(file_path, algorithm='sha256'):
    """
    Calculate hash of a file
    
    Args:
        file_path (str): Path to file
        algorithm (str): Hash algorithm (md5, sha1, sha256, sha512)
        
    Returns:
        str: Hex digest of file hash
    """
    if algorithm not in ['md5', 'sha1', 'sha256', 'sha512']:
        raise ValueError(f"Unsupported algorithm: {algorithm}")
    
    hash_obj = hashlib.new(algorithm)
    
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_obj.update(chunk)
    
    return hash_obj.hexdigest()


def calculate_string_hash(data, algorithm='sha256'):
    """
    Calculate hash of a string
    
    Args:
        data (str): String to hash
        algorithm (str): Hash algorithm
        
    Returns:
        str: Hex digest of hash
    """
    if algorithm not in ['md5', 'sha1', 'sha256', 'sha512']:
        raise ValueError(f"Unsupported algorithm: {algorithm}")
    
    hash_obj = hashlib.new(algorithm)
    hash_obj.update(data.encode('utf-8'))
    
    return hash_obj.hexdigest()


def verify_file_integrity(file_path, expected_hash, algorithm='sha256'):
    """
    Verify file integrity by comparing hash
    
    Args:
        file_path (str): Path to file
        expected_hash (str): Expected hash value
        algorithm (str): Hash algorithm used
        
    Returns:
        bool: True if hashes match
    """
    actual_hash = calculate_file_hash(file_path, algorithm)
    return actual_hash.lower() == expected_hash.lower()


class PasswordValidator:
    """Password strength validator"""
    
    @staticmethod
    def validate_strength(password):
        """
        Validate password strength
        
        Args:
            password (str): Password to validate
            
        Returns:
            dict: Validation result with score and feedback
        """
        score = 0
        feedback = []
        
        # Length check
        if len(password) < 8:
            feedback.append("Password should be at least 8 characters long")
        elif len(password) >= 12:
            score += 2
            feedback.append("Good length")
        else:
            score += 1
        
        # Uppercase check
        if re.search(r'[A-Z]', password):
            score += 1
        else:
            feedback.append("Add uppercase letters")
        
        # Lowercase check
        if re.search(r'[a-z]', password):
            score += 1
        else:
            feedback.append("Add lowercase letters")
        
        # Digit check
        if re.search(r'\d', password):
            score += 1
        else:
            feedback.append("Add numbers")
        
        # Special character check
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            score += 2
        else:
            feedback.append("Add special characters")
        
        # Common patterns check
        common_patterns = ['123', 'password', 'qwerty', 'abc']
        if any(pattern in password.lower() for pattern in common_patterns):
            score -= 2
            feedback.append("Avoid common patterns")
        
        # Determine strength
        if score >= 7:
            strength = "Strong"
        elif score >= 5:
            strength = "Medium"
        else:
            strength = "Weak"
        
        return {
            'strength': strength,
            'score': max(0, score),
            'feedback': feedback,
            'valid': score >= 5
        }
    
    @staticmethod
    def generate_strong_password(length=16):
        """
        Generate a strong random password
        
        Args:
            length (int): Length of password
            
        Returns:
            str: Generated password
        """
        import string
        import secrets
        
        # Define character sets
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        special = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        # Ensure at least one from each category
        password = [
            secrets.choice(lowercase),
            secrets.choice(uppercase),
            secrets.choice(digits),
            secrets.choice(special)
        ]
        
        # Fill the rest
        all_chars = lowercase + uppercase + digits + special
        password.extend(secrets.choice(all_chars) for _ in range(length - 4))
        
        # Shuffle
        password_list = list(password)
        secrets.SystemRandom().shuffle(password_list)
        
        return ''.join(password_list)


def generate_random_key(length=32):
    """
    Generate cryptographically secure random key
    
    Args:
        length (int): Length of key in bytes
        
    Returns:
        bytes: Random key
    """
    return os.urandom(length)


def secure_delete_file(file_path, passes=3):
    """
    Securely delete a file by overwriting before deletion
    
    Args:
        file_path (str): Path to file to delete
        passes (int): Number of overwrite passes
        
    Returns:
        bool: Success status
    """
    if not os.path.exists(file_path):
        return False
    
    try:
        file_size = os.path.getsize(file_path)
        
        with open(file_path, 'ba+') as f:
            for _ in range(passes):
                f.seek(0)
                f.write(os.urandom(file_size))
                f.flush()
                os.fsync(f.fileno())
        
        os.remove(file_path)
        return True
        
    except Exception as e:
        print(f"Error securely deleting file: {e}")
        return False


class Logger:
    """Simple logging utility"""
    
    def __init__(self, log_file=None):
        """
        Initialize logger
        
        Args:
            log_file (str, optional): Path to log file
        """
        self.log_file = log_file
        self.enabled = True
    
    def _write_log(self, level, message):
        """Write log entry"""
        if not self.enabled:
            return
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] [{level}] {message}"
        
        print(log_entry)
        
        if self.log_file:
            try:
                with open(self.log_file, 'a') as f:
                    f.write(log_entry + '\n')
            except Exception as e:
                print(f"Failed to write to log file: {e}")
    
    def info(self, message):
        """Log info message"""
        self._write_log('INFO', message)
    
    def warning(self, message):
        """Log warning message"""
        self._write_log('WARNING', message)
    
    def error(self, message):
        """Log error message"""
        self._write_log('ERROR', message)
    
    def success(self, message):
        """Log success message"""
        self._write_log('SUCCESS', message)
    
    def disable(self):
        """Disable logging"""
        self.enabled = False
    
    def enable(self):
        """Enable logging"""
        self.enabled = True


def format_file_size(size_bytes):
    """
    Format file size in human-readable format
    
    Args:
        size_bytes (int): Size in bytes
        
    Returns:
        str: Formatted size string
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"
