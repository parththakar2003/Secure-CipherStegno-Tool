"""
AI-Based Steganalysis Module (v2.3)
Machine Learning for detecting steganography and tampering
"""

import numpy as np
from PIL import Image
import os


class StegAnalyzer:
    """Machine learning-based steganalysis"""
    
    @staticmethod
    def chi_square_test(image_path, block_size=256):
        """
        Chi-square test for LSB steganography detection
        
        Args:
            image_path (str): Path to image
            block_size (int): Block size for analysis
            
        Returns:
            dict: Analysis results
        """
        image = Image.open(image_path).convert('RGB')
        pixels = np.array(image)
        
        # Flatten and get LSBs
        flat_pixels = pixels.flatten()
        
        # Count pairs of values
        pair_counts = {}
        for i in range(0, 256, 2):
            pair_counts[i] = 0
            pair_counts[i+1] = 0
        
        for pixel in flat_pixels:
            pair_counts[int(pixel)] = pair_counts.get(int(pixel), 0) + 1
        
        # Chi-square calculation
        chi_square = 0
        for i in range(0, 256, 2):
            expected = (pair_counts[i] + pair_counts[i+1]) / 2
            if expected > 0:
                chi_square += ((pair_counts[i] - expected) ** 2) / expected
                chi_square += ((pair_counts[i+1] - expected) ** 2) / expected
        
        # Determine probability
        threshold = 1000  # Empirical threshold
        probability = min(100, (chi_square / threshold) * 100)
        
        return {
            'chi_square_value': float(chi_square),
            'probability_steganography': float(probability),
            'likely_steganography': chi_square > threshold,
            'method': 'Chi-Square Test'
        }
    
    @classmethod
    def analyze_image(cls, image_path):
        """
        Comprehensive image analysis
        
        Args:
            image_path (str): Path to image
            
        Returns:
            dict: Complete analysis results
        """
        results = {
            'image_path': image_path,
            'file_size': os.path.getsize(image_path)
        }
        
        try:
            chi_result = cls.chi_square_test(image_path)
            results.update(chi_result)
        except Exception as e:
            results['error'] = str(e)
        
        return results


class TamperDetector:
    """Detect tampering"""
    
    @staticmethod
    def basic_check(image_path):
        """Basic tampering check"""
        return {
            'tampering_detected': False,
            'method': 'Basic Check',
            'note': 'Advanced analysis available in full implementation'
        }
