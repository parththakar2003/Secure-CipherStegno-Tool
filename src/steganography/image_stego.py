"""
Image Steganography Module
Implements LSB steganography for images with compression
"""

from PIL import Image
import numpy as np
import zlib
import base64


class ImageSteganography:
    """Image steganography using LSB (Least Significant Bit) technique"""
    
    DELIMITER = "<<<END_OF_MESSAGE>>>"
    
    @staticmethod
    def _text_to_binary(text):
        """Convert text to binary string"""
        return ''.join(format(ord(char), '08b') for char in text)
    
    @staticmethod
    def _binary_to_text(binary):
        """Convert binary string to text"""
        chars = []
        for i in range(0, len(binary), 8):
            byte = binary[i:i+8]
            if len(byte) == 8:
                chars.append(chr(int(byte, 2)))
        return ''.join(chars)
    
    @staticmethod
    def compress_text(text):
        """
        Compress text using zlib
        
        Args:
            text (str): Text to compress
            
        Returns:
            str: Base64 encoded compressed text
        """
        compressed = zlib.compress(text.encode('utf-8'))
        return base64.b64encode(compressed).decode('utf-8')
    
    @staticmethod
    def decompress_text(compressed_text):
        """
        Decompress text
        
        Args:
            compressed_text (str): Base64 encoded compressed text
            
        Returns:
            str: Decompressed text
        """
        compressed = base64.b64decode(compressed_text)
        return zlib.decompress(compressed).decode('utf-8')
    
    @classmethod
    def encode(cls, image_path, message, output_path, compress=True):
        """
        Encode message into image
        
        Args:
            image_path (str): Path to cover image
            message (str): Message to hide
            output_path (str): Path to save stego image
            compress (bool): Whether to compress message before encoding
            
        Returns:
            dict: Contains success status and metadata
        """
        # Load image
        image = Image.open(image_path).convert('RGB')
        pixels = np.array(image, dtype=np.int32)  # Use int32 to prevent overflow
        
        # Compress if requested
        if compress:
            message = cls.compress_text(message)
        
        # Add delimiter
        message_with_delimiter = message + cls.DELIMITER
        
        # Convert to binary
        binary_message = cls._text_to_binary(message_with_delimiter)
        
        # Check capacity
        max_bytes = pixels.size // 8
        if len(binary_message) > pixels.size:
            raise ValueError(f"Message too large. Maximum {max_bytes} bytes, got {len(binary_message)//8} bytes")
        
        # Encode message
        data_index = 0
        for row in range(pixels.shape[0]):
            for col in range(pixels.shape[1]):
                if data_index >= len(binary_message):
                    break
                
                for color_channel in range(3):  # RGB
                    if data_index < len(binary_message):
                        # Modify LSB
                        pixels[row, col, color_channel] = (pixels[row, col, color_channel] & ~1) | int(binary_message[data_index])
                        data_index += 1
            
            if data_index >= len(binary_message):
                break
        
        # Save image - ensure proper uint8 conversion
        stego_image = Image.fromarray(np.clip(pixels, 0, 255).astype(np.uint8))
        stego_image.save(output_path)
        
        return {
            'success': True,
            'message_size': len(message),
            'compressed': compress,
            'output_path': output_path
        }
    
    @classmethod
    def decode(cls, image_path, compressed=True):
        """
        Decode message from image
        
        Args:
            image_path (str): Path to stego image
            compressed (bool): Whether message was compressed
            
        Returns:
            str: Hidden message
        """
        # Load image
        image = Image.open(image_path).convert('RGB')
        pixels = np.array(image)
        
        # Extract binary data
        binary_data = ""
        for row in range(pixels.shape[0]):
            for col in range(pixels.shape[1]):
                pixel = pixels[row, col]
                for color_channel in range(3):  # RGB
                    binary_data += str(pixel[color_channel] & 1)
        
        # Convert to text
        message_with_delimiter = cls._binary_to_text(binary_data)
        
        # Find delimiter
        delimiter_index = message_with_delimiter.find(cls.DELIMITER)
        if delimiter_index == -1:
            raise ValueError("No hidden message found or message corrupted")
        
        message = message_with_delimiter[:delimiter_index]
        
        # Decompress if needed
        if compressed:
            try:
                message = cls.decompress_text(message)
            except Exception as e:
                raise ValueError(f"Failed to decompress message: {str(e)}")
        
        return message
    
    @staticmethod
    def get_capacity(image_path):
        """
        Get maximum message capacity of an image
        
        Args:
            image_path (str): Path to image
            
        Returns:
            dict: Capacity information
        """
        image = Image.open(image_path)
        width, height = image.size
        total_pixels = width * height
        max_bits = total_pixels * 3  # 3 channels (RGB)
        max_bytes = max_bits // 8
        max_chars = max_bytes  # Approximately, excluding delimiter
        
        return {
            'image_size': f"{width}x{height}",
            'total_pixels': total_pixels,
            'max_bits': max_bits,
            'max_bytes': max_bytes,
            'max_chars_approx': max_chars - len(ImageSteganography.DELIMITER)
        }


class AdvancedImageSteganography:
    """Advanced image steganography with multiple bits per pixel"""
    
    def __init__(self, bits_per_channel=2):
        """
        Initialize with configurable bits per channel
        
        Args:
            bits_per_channel (int): Number of LSBs to use (1-4)
        """
        if bits_per_channel < 1 or bits_per_channel > 4:
            raise ValueError("bits_per_channel must be between 1 and 4")
        
        self.bits_per_channel = bits_per_channel
        self.mask = (1 << bits_per_channel) - 1
    
    def encode(self, image_path, message, output_path):
        """
        Encode message using multiple LSBs
        
        Args:
            image_path (str): Path to cover image
            message (str): Message to hide
            output_path (str): Path to save stego image
            
        Returns:
            dict: Encoding result
        """
        image = Image.open(image_path).convert('RGB')
        pixels = np.array(image)
        
        # Prepare message
        binary_message = ''.join(format(ord(c), '08b') for c in message)
        binary_message += '1' * 16  # End marker
        
        # Check capacity
        max_bits = pixels.size * self.bits_per_channel
        if len(binary_message) > max_bits:
            raise ValueError("Message too large for this image and bit configuration")
        
        # Encode
        bit_index = 0
        for row in range(pixels.shape[0]):
            for col in range(pixels.shape[1]):
                if bit_index >= len(binary_message):
                    break
                
                pixel = list(pixels[row, col])
                for channel in range(3):
                    if bit_index < len(binary_message):
                        # Clear LSBs and set new value
                        bits_to_embed = binary_message[bit_index:bit_index + self.bits_per_channel]
                        bits_to_embed = bits_to_embed.ljust(self.bits_per_channel, '0')
                        value = int(bits_to_embed, 2)
                        
                        pixel[channel] = (pixel[channel] & ~self.mask) | value
                        bit_index += self.bits_per_channel
                
                pixels[row, col] = tuple(pixel)
            
            if bit_index >= len(binary_message):
                break
        
        stego_image = Image.fromarray(pixels.astype(np.uint8))
        stego_image.save(output_path)
        
        return {
            'success': True,
            'bits_per_channel': self.bits_per_channel,
            'message_size': len(message)
        }
    
    def decode(self, image_path):
        """
        Decode message from image
        
        Args:
            image_path (str): Path to stego image
            
        Returns:
            str: Hidden message
        """
        image = Image.open(image_path).convert('RGB')
        pixels = np.array(image)
        
        # Extract bits
        binary_data = ""
        for row in range(pixels.shape[0]):
            for col in range(pixels.shape[1]):
                pixel = pixels[row, col]
                for channel in range(3):
                    bits = format(pixel[channel] & self.mask, f'0{self.bits_per_channel}b')
                    binary_data += bits
        
        # Find end marker
        end_marker = '1' * 16
        marker_index = binary_data.find(end_marker)
        if marker_index == -1:
            raise ValueError("No hidden message found")
        
        binary_data = binary_data[:marker_index]
        
        # Convert to text
        message = ''.join(chr(int(binary_data[i:i+8], 2)) for i in range(0, len(binary_data), 8))
        
        return message
