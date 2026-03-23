"""
File operations utility module
"""

import os
import json
import shutil


class FileManager:
    """File management utilities"""
    
    @staticmethod
    def ensure_directory(directory_path):
        """
        Ensure directory exists, create if not
        
        Args:
            directory_path (str): Path to directory
        """
        os.makedirs(directory_path, exist_ok=True)
    
    @staticmethod
    def validate_file_exists(file_path):
        """
        Validate that file exists
        
        Args:
            file_path (str): Path to file
            
        Returns:
            bool: True if file exists
        """
        return os.path.exists(file_path) and os.path.isfile(file_path)
    
    @staticmethod
    def get_file_extension(file_path):
        """
        Get file extension
        
        Args:
            file_path (str): Path to file
            
        Returns:
            str: File extension (lowercase, without dot)
        """
        _, ext = os.path.splitext(file_path)
        return ext.lower().lstrip('.')
    
    @staticmethod
    def is_image_file(file_path):
        """
        Check if file is an image
        
        Args:
            file_path (str): Path to file
            
        Returns:
            bool: True if image file
        """
        image_extensions = ['png', 'jpg', 'jpeg', 'bmp', 'gif', 'tiff']
        return FileManager.get_file_extension(file_path) in image_extensions
    
    @staticmethod
    def is_audio_file(file_path):
        """
        Check if file is an audio file
        
        Args:
            file_path (str): Path to file
            
        Returns:
            bool: True if audio file
        """
        audio_extensions = ['wav', 'mp3', 'ogg', 'flac']
        return FileManager.get_file_extension(file_path) in audio_extensions
    
    @staticmethod
    def backup_file(file_path, backup_dir=None):
        """
        Create backup of a file
        
        Args:
            file_path (str): Path to file
            backup_dir (str, optional): Directory for backup
            
        Returns:
            str: Path to backup file
        """
        if not FileManager.validate_file_exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if backup_dir is None:
            backup_dir = os.path.dirname(file_path)
        
        FileManager.ensure_directory(backup_dir)
        
        filename = os.path.basename(file_path)
        name, ext = os.path.splitext(filename)
        backup_filename = f"{name}_backup{ext}"
        backup_path = os.path.join(backup_dir, backup_filename)
        
        # If backup already exists, add number
        counter = 1
        while os.path.exists(backup_path):
            backup_filename = f"{name}_backup_{counter}{ext}"
            backup_path = os.path.join(backup_dir, backup_filename)
            counter += 1
        
        shutil.copy2(file_path, backup_path)
        return backup_path
    
    @staticmethod
    def read_file_binary(file_path):
        """
        Read file in binary mode
        
        Args:
            file_path (str): Path to file
            
        Returns:
            bytes: File content
        """
        with open(file_path, 'rb') as f:
            return f.read()
    
    @staticmethod
    def write_file_binary(file_path, data):
        """
        Write data to file in binary mode
        
        Args:
            file_path (str): Path to file
            data (bytes): Data to write
        """
        with open(file_path, 'wb') as f:
            f.write(data)
    
    @staticmethod
    def read_json(file_path):
        """
        Read JSON file
        
        Args:
            file_path (str): Path to JSON file
            
        Returns:
            dict: Parsed JSON data
        """
        with open(file_path, 'r') as f:
            return json.load(f)
    
    @staticmethod
    def write_json(file_path, data, indent=2):
        """
        Write data to JSON file
        
        Args:
            file_path (str): Path to JSON file
            data (dict): Data to write
            indent (int): JSON indentation
        """
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=indent)


class ConfigManager:
    """Configuration management"""
    
    def __init__(self, config_file='config.json'):
        """
        Initialize config manager
        
        Args:
            config_file (str): Path to config file
        """
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self):
        """Load configuration from file"""
        if os.path.exists(self.config_file):
            try:
                return FileManager.read_json(self.config_file)
            except Exception:
                return self._default_config()
        else:
            return self._default_config()
    
    def _default_config(self):
        """Get default configuration"""
        return {
            'crypto': {
                'default_algorithm': 'aes',
                'key_size': 256,
                'rsa_key_size': 2048
            },
            'steganography': {
                'compression_enabled': True,
                'default_format': 'png'
            },
            'security': {
                'min_password_length': 8,
                'hash_algorithm': 'sha256',
                'secure_delete_passes': 3
            },
            'ui': {
                'theme': 'light',
                'auto_backup': True
            }
        }
    
    def save_config(self):
        """Save configuration to file"""
        FileManager.write_json(self.config_file, self.config)
    
    def get(self, key, default=None):
        """
        Get configuration value
        
        Args:
            key (str): Configuration key (supports dot notation)
            default: Default value if key not found
            
        Returns:
            Configuration value or default
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key, value):
        """
        Set configuration value
        
        Args:
            key (str): Configuration key (supports dot notation)
            value: Value to set
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        self.save_config()
