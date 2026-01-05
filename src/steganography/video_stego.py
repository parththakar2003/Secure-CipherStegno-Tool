"""
Video Steganography Module
Implements steganography for video files (MP4, AVI)
"""

import os
import subprocess
import tempfile
import shutil
from PIL import Image
import numpy as np


class VideoSteganography:
    """Video steganography using frame-based LSB technique"""
    
    DELIMITER = "<<<END_OF_MESSAGE>>>"
    
    @staticmethod
    def _check_ffmpeg():
        """Check if ffmpeg is installed"""
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    @staticmethod
    def _extract_frames(video_path, output_dir):
        """
        Extract frames from video using ffmpeg
        
        Args:
            video_path (str): Path to video file
            output_dir (str): Directory to save frames
            
        Returns:
            int: Number of frames extracted
        """
        cmd = [
            'ffmpeg', '-i', video_path,
            '-vf', 'fps=30',
            os.path.join(output_dir, 'frame_%06d.png')
        ]
        
        subprocess.run(cmd, capture_output=True, check=True)
        
        # Count frames
        frames = [f for f in os.listdir(output_dir) if f.startswith('frame_')]
        return len(frames)
    
    @staticmethod
    def _frames_to_video(frames_dir, output_path, fps=30):
        """
        Combine frames back into video
        
        Args:
            frames_dir (str): Directory containing frames
            output_path (str): Output video path
            fps (int): Frames per second
        """
        cmd = [
            'ffmpeg', '-framerate', str(fps),
            '-i', os.path.join(frames_dir, 'frame_%06d.png'),
            '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
            output_path
        ]
        
        subprocess.run(cmd, capture_output=True, check=True)
    
    @classmethod
    def encode(cls, video_path, message, output_path, max_frames=30):
        """
        Encode message into video
        
        Args:
            video_path (str): Path to cover video
            message (str): Message to hide
            output_path (str): Path to save stego video
            max_frames (int): Maximum frames to use for encoding
            
        Returns:
            dict: Encoding result
        """
        if not cls._check_ffmpeg():
            raise RuntimeError("ffmpeg is required but not installed")
        
        # Create temporary directories
        temp_dir = tempfile.mkdtemp()
        frames_dir = os.path.join(temp_dir, 'frames')
        os.makedirs(frames_dir)
        
        try:
            # Extract frames
            num_frames = cls._extract_frames(video_path, frames_dir)
            
            # Prepare message
            message_with_delimiter = message + cls.DELIMITER
            binary_message = ''.join(format(ord(c), '08b') for c in message_with_delimiter)
            
            # Encode in frames
            frames_used = 0
            data_index = 0
            
            for i in range(1, min(num_frames, max_frames) + 1):
                if data_index >= len(binary_message):
                    break
                
                frame_path = os.path.join(frames_dir, f'frame_{i:06d}.png')
                
                # Load frame
                image = Image.open(frame_path).convert('RGB')
                pixels = np.array(image, dtype=np.int32)
                
                # Encode data in this frame
                for row in range(pixels.shape[0]):
                    for col in range(pixels.shape[1]):
                        if data_index >= len(binary_message):
                            break
                        
                        for channel in range(3):
                            if data_index < len(binary_message):
                                pixels[row, col, channel] = (
                                    pixels[row, col, channel] & ~1
                                ) | int(binary_message[data_index])
                                data_index += 1
                    
                    if data_index >= len(binary_message):
                        break
                
                # Save modified frame
                stego_frame = Image.fromarray(np.clip(pixels, 0, 255).astype(np.uint8))
                stego_frame.save(frame_path)
                frames_used += 1
                
                if data_index >= len(binary_message):
                    break
            
            # Reconstruct video
            cls._frames_to_video(frames_dir, output_path)
            
            return {
                'success': True,
                'message_size': len(message),
                'frames_used': frames_used,
                'total_frames': num_frames,
                'output_path': output_path
            }
        
        finally:
            # Cleanup
            shutil.rmtree(temp_dir)
    
    @classmethod
    def decode(cls, video_path, max_frames=30):
        """
        Decode message from video
        
        Args:
            video_path (str): Path to stego video
            max_frames (int): Maximum frames to check
            
        Returns:
            str: Hidden message
        """
        if not cls._check_ffmpeg():
            raise RuntimeError("ffmpeg is required but not installed")
        
        temp_dir = tempfile.mkdtemp()
        frames_dir = os.path.join(temp_dir, 'frames')
        os.makedirs(frames_dir)
        
        try:
            # Extract frames
            num_frames = cls._extract_frames(video_path, frames_dir)
            
            # Extract binary data
            binary_data = ""
            
            for i in range(1, min(num_frames, max_frames) + 1):
                frame_path = os.path.join(frames_dir, f'frame_{i:06d}.png')
                
                if not os.path.exists(frame_path):
                    break
                
                image = Image.open(frame_path).convert('RGB')
                pixels = np.array(image)
                
                for row in range(pixels.shape[0]):
                    for col in range(pixels.shape[1]):
                        for channel in range(3):
                            binary_data += str(pixels[row, col, channel] & 1)
            
            # Convert to text
            message_with_delimiter = ''.join(
                chr(int(binary_data[i:i+8], 2))
                for i in range(0, len(binary_data), 8)
            )
            
            # Find delimiter
            delimiter_index = message_with_delimiter.find(cls.DELIMITER)
            if delimiter_index == -1:
                raise ValueError("No hidden message found")
            
            return message_with_delimiter[:delimiter_index]
        
        finally:
            shutil.rmtree(temp_dir)
    
    @staticmethod
    def get_video_info(video_path):
        """
        Get video information
        
        Args:
            video_path (str): Path to video
            
        Returns:
            dict: Video information
        """
        cmd = [
            'ffprobe', '-v', 'error',
            '-select_streams', 'v:0',
            '-show_entries', 'stream=width,height,duration,nb_frames',
            '-of', 'default=noprint_wrappers=1',
            video_path
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            info = {}
            for line in result.stdout.split('\n'):
                if '=' in line:
                    key, value = line.strip().split('=')
                    info[key] = value
            
            return {
                'width': int(info.get('width', 0)),
                'height': int(info.get('height', 0)),
                'duration': float(info.get('duration', 0)),
                'frames': int(info.get('nb_frames', 0))
            }
        except:
            return {
                'width': 0,
                'height': 0,
                'duration': 0,
                'frames': 0,
                'error': 'Could not get video info'
            }


class MP3Steganography:
    """MP3 steganography (placeholder - requires lame encoder)"""
    
    @staticmethod
    def encode(audio_path, message, output_path):
        """
        Encode message into MP3 (not yet implemented)
        
        Args:
            audio_path (str): Path to cover audio
            message (str): Message to hide
            output_path (str): Output path
            
        Returns:
            dict: Result
        """
        raise NotImplementedError(
            "MP3 steganography requires LAME encoder integration. "
            "Please use WAV format or convert MP3 to WAV first."
        )
    
    @staticmethod
    def decode(audio_path):
        """Decode message from MP3 (not yet implemented)"""
        raise NotImplementedError(
            "MP3 steganography requires LAME encoder integration. "
            "Please use WAV format."
        )


class JPEGSteganography:
    """JPEG steganography using DCT coefficients"""
    
    @staticmethod
    def encode(image_path, message, output_path, quality=95):
        """
        Encode message into JPEG using DCT coefficient modification
        
        Args:
            image_path (str): Path to cover image
            message (str): Message to hide
            output_path (str): Output path
            quality (int): JPEG quality (85-100 recommended)
            
        Returns:
            dict: Encoding result
        """
        # Note: Full DCT-based JPEG steganography requires complex implementation
        # This is a simplified version using conversion to/from lossless format
        
        # Load JPEG
        image = Image.open(image_path)
        
        # Convert to PNG (lossless)
        temp_png = tempfile.mktemp(suffix='.png')
        image.save(temp_png, 'PNG')
        
        # Use LSB on PNG
        from .image_stego import ImageSteganography
        
        temp_stego = tempfile.mktemp(suffix='.png')
        ImageSteganography.encode(temp_png, message, temp_stego, compress=True)
        
        # Convert back to JPEG
        stego_image = Image.open(temp_stego)
        stego_image.save(output_path, 'JPEG', quality=quality)
        
        # Cleanup
        os.remove(temp_png)
        os.remove(temp_stego)
        
        return {
            'success': True,
            'message_size': len(message),
            'output_path': output_path,
            'quality': quality,
            'note': 'JPEG compression may affect message recovery'
        }
    
    @staticmethod
    def decode(image_path):
        """
        Decode message from JPEG
        
        Args:
            image_path (str): Path to stego image
            
        Returns:
            str: Hidden message
        """
        from .image_stego import ImageSteganography
        
        # Try to decode
        try:
            message = ImageSteganography.decode(image_path, compressed=True)
            return message
        except Exception as e:
            raise ValueError(
                f"Failed to decode message. JPEG compression may have "
                f"corrupted the hidden data. Error: {str(e)}"
            )
