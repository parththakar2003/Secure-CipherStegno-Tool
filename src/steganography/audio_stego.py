"""
Audio Steganography Module
Implements LSB steganography for WAV audio files
"""

import wave
import struct
import os


class AudioSteganography:
    """Audio steganography using LSB technique for WAV files"""
    
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
    
    @classmethod
    def encode(cls, audio_path, message, output_path):
        """
        Encode message into WAV audio file
        
        Args:
            audio_path (str): Path to cover audio file (WAV)
            message (str): Message to hide
            output_path (str): Path to save stego audio
            
        Returns:
            dict: Encoding result
        """
        # Open audio file
        audio = wave.open(audio_path, 'rb')
        
        # Get audio parameters
        params = audio.getparams()
        n_channels = params.nchannels
        sample_width = params.sampwidth
        frame_rate = params.framerate
        n_frames = params.nframes
        
        # Read frames
        frames = audio.readframes(n_frames)
        audio.close()
        
        # Convert to list of samples
        samples = list(struct.unpack(f'{n_frames * n_channels}h', frames))
        
        # Prepare message
        message_with_delimiter = message + cls.DELIMITER
        binary_message = cls._text_to_binary(message_with_delimiter)
        
        # Check capacity
        if len(binary_message) > len(samples):
            raise ValueError(f"Message too large. Maximum {len(samples)//8} bytes, got {len(binary_message)//8} bytes")
        
        # Encode message in LSB
        for i in range(len(binary_message)):
            # Modify LSB of sample
            samples[i] = (samples[i] & ~1) | int(binary_message[i])
        
        # Convert back to bytes
        modified_frames = struct.pack(f'{len(samples)}h', *samples)
        
        # Write to output file
        output_audio = wave.open(output_path, 'wb')
        output_audio.setparams(params)
        output_audio.writeframes(modified_frames)
        output_audio.close()
        
        return {
            'success': True,
            'message_size': len(message),
            'audio_duration': n_frames / frame_rate,
            'output_path': output_path
        }
    
    @classmethod
    def decode(cls, audio_path):
        """
        Decode message from WAV audio file
        
        Args:
            audio_path (str): Path to stego audio file
            
        Returns:
            str: Hidden message
        """
        # Open audio file
        audio = wave.open(audio_path, 'rb')
        
        # Get audio parameters
        params = audio.getparams()
        n_channels = params.nchannels
        n_frames = params.nframes
        
        # Read frames
        frames = audio.readframes(n_frames)
        audio.close()
        
        # Convert to list of samples
        samples = list(struct.unpack(f'{n_frames * n_channels}h', frames))
        
        # Extract binary data from LSB
        binary_data = ""
        for sample in samples:
            binary_data += str(sample & 1)
        
        # Convert to text
        message_with_delimiter = cls._binary_to_text(binary_data)
        
        # Find delimiter
        delimiter_index = message_with_delimiter.find(cls.DELIMITER)
        if delimiter_index == -1:
            raise ValueError("No hidden message found or message corrupted")
        
        message = message_with_delimiter[:delimiter_index]
        
        return message
    
    @staticmethod
    def get_capacity(audio_path):
        """
        Get maximum message capacity of an audio file
        
        Args:
            audio_path (str): Path to audio file
            
        Returns:
            dict: Capacity information
        """
        audio = wave.open(audio_path, 'rb')
        params = audio.getparams()
        n_channels = params.nchannels
        n_frames = params.nframes
        frame_rate = params.framerate
        audio.close()
        
        total_samples = n_frames * n_channels
        max_bits = total_samples
        max_bytes = max_bits // 8
        duration = n_frames / frame_rate
        
        return {
            'channels': n_channels,
            'frame_rate': frame_rate,
            'n_frames': n_frames,
            'duration_seconds': duration,
            'total_samples': total_samples,
            'max_bits': max_bits,
            'max_bytes': max_bytes,
            'max_chars_approx': max_bytes - len(AudioSteganography.DELIMITER)
        }
    
    @staticmethod
    def validate_audio_file(audio_path):
        """
        Validate if audio file is suitable for steganography
        
        Args:
            audio_path (str): Path to audio file
            
        Returns:
            dict: Validation result
        """
        if not os.path.exists(audio_path):
            return {
                'valid': False,
                'error': 'File does not exist'
            }
        
        if not audio_path.lower().endswith('.wav'):
            return {
                'valid': False,
                'error': 'Only WAV files are supported'
            }
        
        try:
            audio = wave.open(audio_path, 'rb')
            params = audio.getparams()
            
            # Check if 16-bit audio
            if params.sampwidth != 2:
                audio.close()
                return {
                    'valid': False,
                    'error': 'Only 16-bit audio is supported'
                }
            
            audio.close()
            
            return {
                'valid': True,
                'channels': params.nchannels,
                'sample_rate': params.framerate,
                'sample_width': params.sampwidth
            }
            
        except Exception as e:
            return {
                'valid': False,
                'error': str(e)
            }
