"""
Document Steganography Module
Hide data in PDF and text documents
"""

import os
import tempfile


class PDFSteganography:
    """PDF steganography using metadata and whitespace"""
    
    @staticmethod
    def encode_metadata(pdf_path, message, output_path):
        """
        Encode message in PDF metadata (requires PyPDF2)
        
        Args:
            pdf_path (str): Input PDF path
            message (str): Message to hide
            output_path (str): Output PDF path
            
        Returns:
            dict: Encoding result
        """
        try:
            from PyPDF2 import PdfReader, PdfWriter
        except ImportError:
            raise ImportError("PyPDF2 is required for PDF steganography. Install with: pip install PyPDF2")
        
        reader = PdfReader(pdf_path)
        writer = PdfWriter()
        
        # Copy all pages
        for page in reader.pages:
            writer.add_page(page)
        
        # Encode message in custom metadata
        import base64
        encoded_message = base64.b64encode(message.encode()).decode()
        
        writer.add_metadata({
            '/Author': encoded_message[:100],  # Limited length
            '/Subject': encoded_message[100:200] if len(encoded_message) > 100 else '',
            '/Keywords': encoded_message[200:] if len(encoded_message) > 200 else ''
        })
        
        # Write output
        with open(output_path, 'wb') as f:
            writer.write(f)
        
        return {
            'success': True,
            'message_size': len(message),
            'encoded_size': len(encoded_message),
            'output_path': output_path,
            'note': 'Message stored in PDF metadata (limited to ~300 chars base64)'
        }
    
    @staticmethod
    def decode_metadata(pdf_path):
        """
        Decode message from PDF metadata
        
        Args:
            pdf_path (str): PDF path
            
        Returns:
            str: Hidden message
        """
        try:
            from PyPDF2 import PdfReader
        except ImportError:
            raise ImportError("PyPDF2 is required. Install with: pip install PyPDF2")
        
        reader = PdfReader(pdf_path)
        metadata = reader.metadata
        
        if not metadata:
            raise ValueError("No metadata found in PDF")
        
        # Extract from metadata fields
        import base64
        encoded_parts = []
        
        if '/Author' in metadata:
            encoded_parts.append(metadata['/Author'])
        if '/Subject' in metadata:
            encoded_parts.append(metadata['/Subject'])
        if '/Keywords' in metadata:
            encoded_parts.append(metadata['/Keywords'])
        
        encoded_message = ''.join(encoded_parts)
        
        try:
            message = base64.b64decode(encoded_message).decode()
            return message
        except Exception as e:
            raise ValueError(f"Failed to decode message: {str(e)}")


class TextSteganography:
    """Text steganography using Unicode and whitespace"""
    
    @staticmethod
    def encode_whitespace(text, message):
        """
        Encode message using whitespace
        
        Args:
            text (str): Cover text
            message (str): Message to hide
            
        Returns:
            str: Stego text
        """
        # Convert message to binary
        binary = ''.join(format(ord(c), '08b') for c in message)
        binary += '11111111'  # End marker
        
        # Split text into lines
        lines = text.split('\n')
        
        if len(binary) > len(lines):
            raise ValueError("Message too long for cover text")
        
        # Encode in trailing whitespace (space=0, tab=1)
        stego_lines = []
        for i, line in enumerate(lines):
            if i < len(binary):
                # Add space or tab at end
                if binary[i] == '0':
                    stego_lines.append(line + ' ')
                else:
                    stego_lines.append(line + '\t')
            else:
                stego_lines.append(line)
        
        return '\n'.join(stego_lines)
    
    @staticmethod
    def decode_whitespace(stego_text):
        """
        Decode message from whitespace
        
        Args:
            stego_text (str): Stego text
            
        Returns:
            str: Hidden message
        """
        lines = stego_text.split('\n')
        
        # Extract binary from trailing whitespace
        binary = ''
        for line in lines:
            if line.endswith('\t'):
                binary += '1'
            elif line.endswith(' '):
                binary += '0'
            else:
                break  # No more encoded data
        
        # Find end marker
        end_marker = '11111111'
        if end_marker in binary:
            binary = binary[:binary.index(end_marker)]
        
        # Convert to text
        message = ''
        for i in range(0, len(binary), 8):
            byte = binary[i:i+8]
            if len(byte) == 8:
                message += chr(int(byte, 2))
        
        return message
    
    @staticmethod
    def encode_unicode(text, message):
        """
        Encode message using zero-width Unicode characters
        
        Args:
            text (str): Cover text
            message (str): Message to hide
            
        Returns:
            str: Stego text
        """
        # Zero-width characters
        ZERO_WIDTH_SPACE = '\u200B'      # 0
        ZERO_WIDTH_NON_JOINER = '\u200C'  # 1
        
        # Convert message to binary
        binary = ''.join(format(ord(c), '08b') for c in message)
        binary += '11111111'  # End marker
        
        if len(binary) > len(text):
            raise ValueError("Message too long for cover text")
        
        # Insert zero-width characters
        stego_text = ''
        for i, char in enumerate(text):
            stego_text += char
            if i < len(binary):
                if binary[i] == '0':
                    stego_text += ZERO_WIDTH_SPACE
                else:
                    stego_text += ZERO_WIDTH_NON_JOINER
        
        return stego_text
    
    @staticmethod
    def decode_unicode(stego_text):
        """
        Decode message from zero-width Unicode characters
        
        Args:
            stego_text (str): Stego text
            
        Returns:
            str: Hidden message
        """
        ZERO_WIDTH_SPACE = '\u200B'
        ZERO_WIDTH_NON_JOINER = '\u200C'
        
        # Extract binary
        binary = ''
        for char in stego_text:
            if char == ZERO_WIDTH_SPACE:
                binary += '0'
            elif char == ZERO_WIDTH_NON_JOINER:
                binary += '1'
        
        # Find end marker
        end_marker = '11111111'
        if end_marker in binary:
            binary = binary[:binary.index(end_marker)]
        
        # Convert to text
        message = ''
        for i in range(0, len(binary), 8):
            byte = binary[i:i+8]
            if len(byte) == 8:
                message += chr(int(byte, 2))
        
        return message
