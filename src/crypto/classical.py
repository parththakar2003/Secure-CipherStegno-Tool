"""
Classical Cipher Implementations
Includes Vigenère, Playfair, and other classical ciphers
"""


class VigenereCipher:
    """Vigenère cipher - polyalphabetic substitution cipher"""
    
    @staticmethod
    def _prepare_key(text, key):
        """
        Prepare key by repeating it to match text length
        
        Args:
            text (str): Plaintext
            key (str): Encryption key
            
        Returns:
            str: Extended key
        """
        key = key.upper()
        extended_key = []
        key_index = 0
        
        for char in text:
            if char.isalpha():
                extended_key.append(key[key_index % len(key)])
                key_index += 1
            else:
                extended_key.append(char)
        
        return ''.join(extended_key)
    
    @classmethod
    def encrypt(cls, plaintext, key):
        """
        Encrypt text using Vigenère cipher
        
        Args:
            plaintext (str): Text to encrypt
            key (str): Encryption key (alphabetic)
            
        Returns:
            str: Encrypted text
        """
        if not key or not key.isalpha():
            raise ValueError("Key must contain only alphabetic characters")
        
        extended_key = cls._prepare_key(plaintext, key)
        ciphertext = []
        
        for i, char in enumerate(plaintext):
            if char.isalpha():
                # Determine if uppercase or lowercase
                shift_base = 65 if char.isupper() else 97
                key_char = extended_key[i]
                
                # Calculate shift from key character
                shift = ord(key_char) - 65
                
                # Encrypt character
                encrypted_char = chr((ord(char) - shift_base + shift) % 26 + shift_base)
                ciphertext.append(encrypted_char)
            else:
                ciphertext.append(char)
        
        return ''.join(ciphertext)
    
    @classmethod
    def decrypt(cls, ciphertext, key):
        """
        Decrypt text using Vigenère cipher
        
        Args:
            ciphertext (str): Text to decrypt
            key (str): Decryption key (alphabetic)
            
        Returns:
            str: Decrypted text
        """
        if not key or not key.isalpha():
            raise ValueError("Key must contain only alphabetic characters")
        
        extended_key = cls._prepare_key(ciphertext, key)
        plaintext = []
        
        for i, char in enumerate(ciphertext):
            if char.isalpha():
                # Determine if uppercase or lowercase
                shift_base = 65 if char.isupper() else 97
                key_char = extended_key[i]
                
                # Calculate shift from key character
                shift = ord(key_char) - 65
                
                # Decrypt character
                decrypted_char = chr((ord(char) - shift_base - shift) % 26 + shift_base)
                plaintext.append(decrypted_char)
            else:
                plaintext.append(char)
        
        return ''.join(plaintext)
    
    @staticmethod
    def analyze_key_strength(key):
        """
        Analyze Vigenère key strength
        
        Args:
            key (str): Encryption key
            
        Returns:
            dict: Analysis results
        """
        if not key:
            return {
                'strength': 'Invalid',
                'score': 0,
                'recommendations': ['Key cannot be empty']
            }
        
        score = 0
        recommendations = []
        
        # Length check
        key_length = len(key)
        if key_length < 5:
            recommendations.append('Use a key of at least 5 characters')
        elif key_length >= 10:
            score += 3
        elif key_length >= 7:
            score += 2
        else:
            score += 1
        
        # Character diversity
        unique_chars = len(set(key.upper()))
        if unique_chars < 5:
            recommendations.append('Use more diverse characters in key')
        elif unique_chars >= 15:
            score += 2
        elif unique_chars >= 10:
            score += 1
        
        # Pattern check
        if key.lower() in ['abcd', 'password', 'qwerty', 'key', 'secret']:
            score -= 2
            recommendations.append('Avoid common words as keys')
        
        # Repeated characters
        max_repeat = max((key.count(c) for c in set(key)), default=0)
        if max_repeat > len(key) // 2:
            recommendations.append('Avoid excessive character repetition')
            score -= 1
        
        # Determine strength
        if score >= 4:
            strength = 'Strong'
        elif score >= 2:
            strength = 'Medium'
        else:
            strength = 'Weak'
        
        return {
            'strength': strength,
            'score': max(0, score),
            'key_length': key_length,
            'unique_characters': unique_chars,
            'recommendations': recommendations if recommendations else ['Good key strength']
        }


class PlayfairCipher:
    """Playfair cipher - digraph substitution cipher"""
    
    @staticmethod
    def _create_matrix(key):
        """
        Create 5x5 Playfair matrix from key
        
        Args:
            key (str): Encryption key
            
        Returns:
            list: 5x5 matrix
        """
        # Remove duplicates and non-alphabetic characters
        key = ''.join(dict.fromkeys(key.upper().replace('J', 'I')))
        key = ''.join(c for c in key if c.isalpha())
        
        # Add remaining letters
        alphabet = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'  # I/J combined
        for char in alphabet:
            if char not in key:
                key += char
        
        # Create 5x5 matrix
        matrix = []
        for i in range(0, 25, 5):
            matrix.append(list(key[i:i+5]))
        
        return matrix
    
    @staticmethod
    def _find_position(matrix, char):
        """Find position of character in matrix"""
        for i, row in enumerate(matrix):
            if char in row:
                return i, row.index(char)
        return None
    
    @staticmethod
    def _prepare_text(text):
        """
        Prepare text for Playfair encryption
        
        Args:
            text (str): Input text
            
        Returns:
            list: List of digraphs
        """
        # Convert to uppercase, replace J with I, remove non-alphabetic
        text = text.upper().replace('J', 'I')
        text = ''.join(c for c in text if c.isalpha())
        
        # Create digraphs
        digraphs = []
        i = 0
        while i < len(text):
            if i == len(text) - 1:
                # Odd length, add X
                digraphs.append(text[i] + 'X')
                i += 1
            elif text[i] == text[i+1]:
                # Same letters, insert X
                digraphs.append(text[i] + 'X')
                i += 1
            else:
                digraphs.append(text[i:i+2])
                i += 2
        
        return digraphs
    
    @classmethod
    def encrypt(cls, plaintext, key):
        """
        Encrypt text using Playfair cipher
        
        Args:
            plaintext (str): Text to encrypt
            key (str): Encryption key
            
        Returns:
            str: Encrypted text
        """
        matrix = cls._create_matrix(key)
        digraphs = cls._prepare_text(plaintext)
        ciphertext = []
        
        for digraph in digraphs:
            row1, col1 = cls._find_position(matrix, digraph[0])
            row2, col2 = cls._find_position(matrix, digraph[1])
            
            if row1 == row2:
                # Same row - shift right
                ciphertext.append(matrix[row1][(col1 + 1) % 5])
                ciphertext.append(matrix[row2][(col2 + 1) % 5])
            elif col1 == col2:
                # Same column - shift down
                ciphertext.append(matrix[(row1 + 1) % 5][col1])
                ciphertext.append(matrix[(row2 + 1) % 5][col2])
            else:
                # Rectangle - swap columns
                ciphertext.append(matrix[row1][col2])
                ciphertext.append(matrix[row2][col1])
        
        return ''.join(ciphertext)
    
    @classmethod
    def decrypt(cls, ciphertext, key):
        """
        Decrypt text using Playfair cipher
        
        Args:
            ciphertext (str): Text to decrypt
            key (str): Decryption key
            
        Returns:
            str: Decrypted text
        """
        matrix = cls._create_matrix(key)
        
        # Prepare ciphertext into digraphs
        ciphertext = ciphertext.upper().replace('J', 'I')
        ciphertext = ''.join(c for c in ciphertext if c.isalpha())
        digraphs = [ciphertext[i:i+2] for i in range(0, len(ciphertext), 2)]
        
        plaintext = []
        
        for digraph in digraphs:
            if len(digraph) < 2:
                continue
            
            row1, col1 = cls._find_position(matrix, digraph[0])
            row2, col2 = cls._find_position(matrix, digraph[1])
            
            if row1 == row2:
                # Same row - shift left
                plaintext.append(matrix[row1][(col1 - 1) % 5])
                plaintext.append(matrix[row2][(col2 - 1) % 5])
            elif col1 == col2:
                # Same column - shift up
                plaintext.append(matrix[(row1 - 1) % 5][col1])
                plaintext.append(matrix[(row2 - 1) % 5][col2])
            else:
                # Rectangle - swap columns
                plaintext.append(matrix[row1][col2])
                plaintext.append(matrix[row2][col1])
        
        return ''.join(plaintext)


class RailFenceCipher:
    """Rail Fence cipher - transposition cipher"""
    
    @staticmethod
    def encrypt(plaintext, rails):
        """
        Encrypt text using Rail Fence cipher
        
        Args:
            plaintext (str): Text to encrypt
            rails (int): Number of rails
            
        Returns:
            str: Encrypted text
        """
        if rails < 2:
            raise ValueError("Number of rails must be at least 2")
        
        # Create fence
        fence = [[] for _ in range(rails)]
        rail = 0
        direction = 1  # 1 for down, -1 for up
        
        for char in plaintext:
            fence[rail].append(char)
            rail += direction
            
            # Change direction at top or bottom
            if rail == 0 or rail == rails - 1:
                direction = -direction
        
        # Read off the fence
        ciphertext = ''.join([''.join(rail) for rail in fence])
        return ciphertext
    
    @staticmethod
    def decrypt(ciphertext, rails):
        """
        Decrypt text using Rail Fence cipher
        
        Args:
            ciphertext (str): Text to decrypt
            rails (int): Number of rails
            
        Returns:
            str: Decrypted text
        """
        if rails < 2:
            raise ValueError("Number of rails must be at least 2")
        
        # Create fence pattern
        fence = [[None for _ in range(len(ciphertext))] for _ in range(rails)]
        rail = 0
        direction = 1
        
        # Mark positions
        for i in range(len(ciphertext)):
            fence[rail][i] = '*'
            rail += direction
            if rail == 0 or rail == rails - 1:
                direction = -direction
        
        # Fill fence with ciphertext
        index = 0
        for i in range(rails):
            for j in range(len(ciphertext)):
                if fence[i][j] == '*':
                    fence[i][j] = ciphertext[index]
                    index += 1
        
        # Read off in zigzag pattern
        plaintext = []
        rail = 0
        direction = 1
        
        for i in range(len(ciphertext)):
            plaintext.append(fence[rail][i])
            rail += direction
            if rail == 0 or rail == rails - 1:
                direction = -direction
        
        return ''.join(plaintext)
