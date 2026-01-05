"""
Advanced Security Tools
Includes encryption strength analyzer, secure communications, and more
"""

import socket
import hashlib
import re
from datetime import datetime
import secrets


class EncryptionAnalyzer:
    """Analyze encryption strength and provide recommendations"""
    
    @staticmethod
    def analyze_algorithm(algorithm_name):
        """
        Analyze encryption algorithm strength
        
        Args:
            algorithm_name (str): Name of algorithm
            
        Returns:
            dict: Analysis results
        """
        algorithm_data = {
            'aes': {
                'name': 'AES-256',
                'strength': 'Very Strong',
                'security_level': 256,
                'type': 'Symmetric',
                'recommended': True,
                'notes': 'Industry standard, widely adopted, NSA approved for TOP SECRET'
            },
            'rsa': {
                'name': 'RSA-2048/4096',
                'strength': 'Strong',
                'security_level': 112,  # 2048-bit RSA ~ 112-bit security
                'type': 'Asymmetric',
                'recommended': True,
                'notes': 'Suitable for key exchange and digital signatures'
            },
            'blowfish': {
                'name': 'Blowfish',
                'strength': 'Strong',
                'security_level': 128,
                'type': 'Symmetric',
                'recommended': True,
                'notes': 'Fast and secure, but consider using AES for new applications'
            },
            '3des': {
                'name': 'Triple DES',
                'strength': 'Medium',
                'security_level': 112,
                'type': 'Symmetric',
                'recommended': False,
                'notes': 'Legacy algorithm, being phased out. Use AES instead.'
            },
            'des': {
                'name': 'DES',
                'strength': 'Weak',
                'security_level': 56,
                'type': 'Symmetric',
                'recommended': False,
                'notes': 'Deprecated. Vulnerable to brute force attacks. Do not use.'
            },
            'chacha20': {
                'name': 'ChaCha20',
                'strength': 'Very Strong',
                'security_level': 256,
                'type': 'Stream Cipher',
                'recommended': True,
                'notes': 'Modern, fast, and secure. Good alternative to AES.'
            },
            'caesar': {
                'name': 'Caesar Cipher',
                'strength': 'Very Weak',
                'security_level': 4,
                'type': 'Classical',
                'recommended': False,
                'notes': 'Educational only. Easily broken. Not for real security.'
            },
            'vigenere': {
                'name': 'Vigenère Cipher',
                'strength': 'Weak',
                'security_level': 20,
                'type': 'Classical',
                'recommended': False,
                'notes': 'Historical cipher. Vulnerable to frequency analysis.'
            }
        }
        
        algo_key = algorithm_name.lower().replace('-', '').replace('_', '')
        
        if algo_key in algorithm_data:
            return algorithm_data[algo_key]
        else:
            return {
                'name': algorithm_name,
                'strength': 'Unknown',
                'security_level': 0,
                'type': 'Unknown',
                'recommended': False,
                'notes': 'Algorithm not in database. Research before using.'
            }
    
    @staticmethod
    def compare_algorithms(algorithms):
        """
        Compare multiple encryption algorithms
        
        Args:
            algorithms (list): List of algorithm names
            
        Returns:
            dict: Comparison results
        """
        results = []
        for algo in algorithms:
            results.append(EncryptionAnalyzer.analyze_algorithm(algo))
        
        # Sort by security level
        results.sort(key=lambda x: x['security_level'], reverse=True)
        
        return {
            'algorithms': results,
            'strongest': results[0]['name'] if results else None,
            'weakest': results[-1]['name'] if results else None
        }


class NetworkScanner:
    """Basic network security scanner"""
    
    @staticmethod
    def scan_port(host, port, timeout=1):
        """
        Check if a port is open
        
        Args:
            host (str): Target host
            port (int): Port number
            timeout (int): Connection timeout
            
        Returns:
            dict: Scan result
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            
            return {
                'port': port,
                'status': 'open' if result == 0 else 'closed',
                'open': result == 0
            }
        except Exception as e:
            return {
                'port': port,
                'status': 'error',
                'open': False,
                'error': str(e)
            }
    
    @staticmethod
    def scan_common_ports(host, timeout=1):
        """
        Scan common ports on a host
        
        Args:
            host (str): Target host
            timeout (int): Connection timeout
            
        Returns:
            dict: Scan results
        """
        common_ports = {
            21: 'FTP',
            22: 'SSH',
            23: 'Telnet',
            25: 'SMTP',
            53: 'DNS',
            80: 'HTTP',
            110: 'POP3',
            143: 'IMAP',
            443: 'HTTPS',
            445: 'SMB',
            3306: 'MySQL',
            3389: 'RDP',
            5432: 'PostgreSQL',
            8080: 'HTTP-Alt'
        }
        
        results = []
        for port, service in common_ports.items():
            scan_result = NetworkScanner.scan_port(host, port, timeout)
            scan_result['service'] = service
            if scan_result['open']:
                results.append(scan_result)
        
        return {
            'host': host,
            'open_ports': results,
            'total_open': len(results),
            'scan_time': datetime.now().isoformat()
        }


class SecureTokenGenerator:
    """Generate secure tokens for various purposes"""
    
    @staticmethod
    def generate_token(length=32, url_safe=True):
        """
        Generate a secure random token
        
        Args:
            length (int): Length of token in bytes
            url_safe (bool): Whether token should be URL-safe
            
        Returns:
            str: Generated token
        """
        if url_safe:
            return secrets.token_urlsafe(length)
        else:
            return secrets.token_hex(length)
    
    @staticmethod
    def generate_api_key():
        """
        Generate an API key
        
        Returns:
            str: API key
        """
        prefix = "sk"
        random_part = secrets.token_urlsafe(32)
        return f"{prefix}_{random_part}"
    
    @staticmethod
    def generate_session_token():
        """
        Generate a session token
        
        Returns:
            dict: Session token with metadata
        """
        token = secrets.token_urlsafe(48)
        return {
            'token': token,
            'created_at': datetime.now().isoformat(),
            'expires_in': 3600  # 1 hour
        }


class DataSanitizer:
    """Sanitize data to prevent security vulnerabilities"""
    
    @staticmethod
    def sanitize_filename(filename):
        """
        Sanitize filename to prevent path traversal
        
        Args:
            filename (str): Filename to sanitize
            
        Returns:
            str: Sanitized filename
        """
        # Remove path separators
        filename = filename.replace('/', '_').replace('\\', '_')
        
        # Remove potentially dangerous characters
        filename = re.sub(r'[^\w\s\-\.]', '', filename)
        
        # Limit length
        if len(filename) > 255:
            name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
            filename = name[:250] + ('.' + ext if ext else '')
        
        return filename
    
    @staticmethod
    def sanitize_input(text, max_length=1000):
        """
        Sanitize user input
        
        Args:
            text (str): Text to sanitize
            max_length (int): Maximum allowed length
            
        Returns:
            str: Sanitized text
        """
        # Limit length
        text = text[:max_length]
        
        # Remove null bytes
        text = text.replace('\x00', '')
        
        # Remove other control characters except newline and tab
        text = ''.join(char for char in text if char >= ' ' or char in '\n\t')
        
        return text
    
    @staticmethod
    def validate_email(email):
        """
        Validate email address format
        
        Args:
            email (str): Email to validate
            
        Returns:
            bool: True if valid
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))


class CryptographicHashChain:
    """Create and verify hash chains for data integrity"""
    
    def __init__(self, algorithm='sha256'):
        """
        Initialize hash chain
        
        Args:
            algorithm (str): Hash algorithm to use
        """
        self.algorithm = algorithm
        self.chain = []
    
    def add_block(self, data):
        """
        Add data block to chain
        
        Args:
            data (str): Data to add
            
        Returns:
            str: Block hash
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        # Get previous hash
        previous_hash = self.chain[-1]['hash'] if self.chain else '0' * 64
        
        # Create block
        block = {
            'index': len(self.chain),
            'data': data.decode('utf-8') if isinstance(data, bytes) else data,
            'previous_hash': previous_hash,
            'timestamp': datetime.now().isoformat()
        }
        
        # Calculate block hash
        block_string = f"{block['index']}{block['data']}{block['previous_hash']}{block['timestamp']}"
        block_hash = hashlib.new(self.algorithm, block_string.encode()).hexdigest()
        block['hash'] = block_hash
        
        self.chain.append(block)
        return block_hash
    
    def verify_chain(self):
        """
        Verify integrity of the entire chain
        
        Returns:
            bool: True if chain is valid
        """
        for i, block in enumerate(self.chain):
            # Verify block hash
            block_string = f"{block['index']}{block['data']}{block['previous_hash']}{block['timestamp']}"
            expected_hash = hashlib.new(self.algorithm, block_string.encode()).hexdigest()
            
            if block['hash'] != expected_hash:
                return False
            
            # Verify link to previous block
            if i > 0:
                if block['previous_hash'] != self.chain[i-1]['hash']:
                    return False
        
        return True
    
    def get_chain(self):
        """Get the entire chain"""
        return self.chain
