"""
Command Line Interface for Secure CipherStegno Tool
Version 2.0.0
"""

import sys
import os

# Check Python version before any other imports
if sys.version_info < (3, 8):
    sys.stderr.write(
        "=" * 70 + "\n"
        "ERROR: Python 3.8 or higher is required\n"
        "=" * 70 + "\n"
        "Current Python version: {0}.{1}.{2}\n".format(
            sys.version_info.major,
            sys.version_info.minor,
            sys.version_info.micro
        ) +
        "Required Python version: 3.8 or higher\n\n"
        "This tool requires Python 3.8+ because:\n"
        "  • Pillow >= 10.0.0 requires Python 3.8+\n"
        "  • NumPy >= 1.24.0 requires Python 3.8+\n"
        "  • FastAPI >= 0.104.0 requires Python 3.8+\n"
        "  • Other dependencies require modern Python versions\n\n"
        "To fix this issue:\n"
        "  1. Install Python 3.8+ from https://www.python.org/downloads/\n"
        "  2. Use 'python3' instead of 'python' command\n"
        "  3. Run: python3 cli.py --help\n\n"
        "For detailed instructions, see:\n"
        "  https://github.com/parththakar2003/Secure-CipherStegno-Tool#installation--usage\n"
        "=" * 70 + "\n"
    )
    sys.exit(1)

import argparse
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src import __version__
from src.crypto import CaesarCipher, AESCipher, RSACipher
from src.steganography import ImageSteganography, AudioSteganography
from src.utils import Logger, PasswordValidator, calculate_file_hash


class CLI:
    """Command Line Interface handler"""
    
    def __init__(self):
        self.logger = Logger()
        self.parser = self._create_parser()
    
    def _create_parser(self):
        """Create argument parser"""
        parser = argparse.ArgumentParser(
            description=f'Secure CipherStegno Tool v{__version__} - Advanced Cryptography and Steganography',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Encrypt text with AES
  python cli.py encrypt --algorithm aes --input message.txt --output encrypted.bin --password mypass
  
  # Hide encrypted message in image
  python cli.py stego-encode --type image --cover photo.png --message secret.txt --output stego.png
  
  # Extract message from image
  python cli.py stego-decode --type image --input stego.png
  
  # Generate RSA key pair
  python cli.py generate-keys --algorithm rsa --output-dir ./keys
            """
        )
        
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # Encrypt command
        encrypt_parser = subparsers.add_parser('encrypt', help='Encrypt data')
        encrypt_parser.add_argument('--algorithm', choices=['caesar', 'aes', 'rsa'], required=True,
                                   help='Encryption algorithm')
        encrypt_parser.add_argument('--input', required=True, help='Input file or text')
        encrypt_parser.add_argument('--output', required=True, help='Output file')
        encrypt_parser.add_argument('--password', help='Password for encryption')
        encrypt_parser.add_argument('--key', help='Key file for RSA')
        encrypt_parser.add_argument('--shift', type=int, default=3, help='Shift value for Caesar cipher')
        
        # Decrypt command
        decrypt_parser = subparsers.add_parser('decrypt', help='Decrypt data')
        decrypt_parser.add_argument('--algorithm', choices=['caesar', 'aes', 'rsa'], required=True,
                                   help='Decryption algorithm')
        decrypt_parser.add_argument('--input', required=True, help='Input encrypted file')
        decrypt_parser.add_argument('--output', required=True, help='Output file')
        decrypt_parser.add_argument('--password', help='Password for decryption')
        decrypt_parser.add_argument('--key', help='Key file for RSA')
        decrypt_parser.add_argument('--shift', type=int, default=3, help='Shift value for Caesar cipher')
        
        # Steganography encode
        stego_encode_parser = subparsers.add_parser('stego-encode', help='Hide message in cover file')
        stego_encode_parser.add_argument('--type', choices=['image', 'audio'], required=True,
                                        help='Steganography type')
        stego_encode_parser.add_argument('--cover', required=True, help='Cover file (image or audio)')
        stego_encode_parser.add_argument('--message', required=True, help='Message file to hide')
        stego_encode_parser.add_argument('--output', required=True, help='Output stego file')
        stego_encode_parser.add_argument('--compress', action='store_true', help='Compress message')
        
        # Steganography decode
        stego_decode_parser = subparsers.add_parser('stego-decode', help='Extract message from stego file')
        stego_decode_parser.add_argument('--type', choices=['image', 'audio'], required=True,
                                        help='Steganography type')
        stego_decode_parser.add_argument('--input', required=True, help='Stego file')
        stego_decode_parser.add_argument('--output', help='Output file for extracted message')
        stego_decode_parser.add_argument('--compressed', action='store_true', help='Message was compressed')
        
        # Generate keys
        keygen_parser = subparsers.add_parser('generate-keys', help='Generate cryptographic keys')
        keygen_parser.add_argument('--algorithm', choices=['rsa', 'aes'], required=True,
                                  help='Key type to generate')
        keygen_parser.add_argument('--output-dir', default='.', help='Output directory for keys')
        keygen_parser.add_argument('--key-size', type=int, help='Key size (RSA: 2048/4096, AES: 256)')
        
        # Hash file
        hash_parser = subparsers.add_parser('hash', help='Calculate file hash')
        hash_parser.add_argument('--input', required=True, help='Input file')
        hash_parser.add_argument('--algorithm', choices=['md5', 'sha1', 'sha256', 'sha512'],
                                default='sha256', help='Hash algorithm')
        
        # Password validation
        pwd_parser = subparsers.add_parser('validate-password', help='Validate password strength')
        pwd_parser.add_argument('--password', help='Password to validate (or use stdin)')
        
        # Generate password
        genpwd_parser = subparsers.add_parser('generate-password', help='Generate strong password')
        genpwd_parser.add_argument('--length', type=int, default=16, help='Password length')
        
        return parser
    
    def run(self, args=None):
        """Run CLI with arguments"""
        args = self.parser.parse_args(args)
        
        if not args.command:
            self.parser.print_help()
            return
        
        try:
            if args.command == 'encrypt':
                self._handle_encrypt(args)
            elif args.command == 'decrypt':
                self._handle_decrypt(args)
            elif args.command == 'stego-encode':
                self._handle_stego_encode(args)
            elif args.command == 'stego-decode':
                self._handle_stego_decode(args)
            elif args.command == 'generate-keys':
                self._handle_generate_keys(args)
            elif args.command == 'hash':
                self._handle_hash(args)
            elif args.command == 'validate-password':
                self._handle_validate_password(args)
            elif args.command == 'generate-password':
                self._handle_generate_password(args)
        except Exception as e:
            print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
            sys.exit(1)
    
    def _handle_encrypt(self, args):
        """Handle encryption command"""
        # Read input
        if os.path.exists(args.input):
            with open(args.input, 'r') as f:
                plaintext = f.read()
        else:
            plaintext = args.input
        
        if args.algorithm == 'caesar':
            result = CaesarCipher.encrypt(plaintext, args.shift)
            with open(args.output, 'w') as f:
                f.write(result)
            print(f"{Fore.GREEN}✓ Text encrypted with Caesar cipher (shift={args.shift})")
        
        elif args.algorithm == 'aes':
            if not args.password:
                raise ValueError("Password required for AES encryption")
            
            cipher = AESCipher(args.password)
            result = cipher.encrypt(plaintext)
            
            # Save to file
            import json
            with open(args.output, 'w') as f:
                json.dump(result, f)
            
            print(f"{Fore.GREEN}✓ Text encrypted with AES-256")
            print(f"Output: {args.output}")
        
        elif args.algorithm == 'rsa':
            if not args.key:
                raise ValueError("Public key file required for RSA encryption")
            
            with open(args.key, 'r') as f:
                public_key = f.read()
            
            cipher = RSACipher()
            cipher.load_public_key(public_key)
            result = cipher.encrypt(plaintext)
            
            with open(args.output, 'w') as f:
                f.write(result)
            
            print(f"{Fore.GREEN}✓ Text encrypted with RSA")
    
    def _handle_decrypt(self, args):
        """Handle decryption command"""
        if args.algorithm == 'caesar':
            with open(args.input, 'r') as f:
                ciphertext = f.read()
            
            result = CaesarCipher.decrypt(ciphertext, args.shift)
            with open(args.output, 'w') as f:
                f.write(result)
            
            print(f"{Fore.GREEN}✓ Text decrypted with Caesar cipher")
        
        elif args.algorithm == 'aes':
            if not args.password:
                raise ValueError("Password required for AES decryption")
            
            import json
            with open(args.input, 'r') as f:
                encrypted_data = json.load(f)
            
            cipher = AESCipher(args.password)
            result = cipher.decrypt(encrypted_data['ciphertext'], encrypted_data['iv'])
            
            with open(args.output, 'w') as f:
                f.write(result)
            
            print(f"{Fore.GREEN}✓ Text decrypted with AES-256")
        
        elif args.algorithm == 'rsa':
            if not args.key:
                raise ValueError("Private key file required for RSA decryption")
            
            with open(args.key, 'r') as f:
                private_key = f.read()
            
            with open(args.input, 'r') as f:
                ciphertext = f.read()
            
            cipher = RSACipher()
            cipher.load_private_key(private_key)
            result = cipher.decrypt(ciphertext)
            
            with open(args.output, 'w') as f:
                f.write(result)
            
            print(f"{Fore.GREEN}✓ Text decrypted with RSA")
    
    def _handle_stego_encode(self, args):
        """Handle steganography encoding"""
        # Read message
        with open(args.message, 'r') as f:
            message = f.read()
        
        if args.type == 'image':
            result = ImageSteganography.encode(args.cover, message, args.output, args.compress)
            print(f"{Fore.GREEN}✓ Message hidden in image")
            print(f"Output: {result['output_path']}")
            print(f"Message size: {result['message_size']} bytes")
        
        elif args.type == 'audio':
            result = AudioSteganography.encode(args.cover, message, args.output)
            print(f"{Fore.GREEN}✓ Message hidden in audio")
            print(f"Output: {result['output_path']}")
            print(f"Audio duration: {result['audio_duration']:.2f} seconds")
    
    def _handle_stego_decode(self, args):
        """Handle steganography decoding"""
        if args.type == 'image':
            message = ImageSteganography.decode(args.input, args.compressed)
        elif args.type == 'audio':
            message = AudioSteganography.decode(args.input)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(message)
            print(f"{Fore.GREEN}✓ Message extracted and saved to {args.output}")
        else:
            print(f"{Fore.GREEN}✓ Extracted message:")
            print(f"{Fore.CYAN}{message}{Style.RESET_ALL}")
    
    def _handle_generate_keys(self, args):
        """Handle key generation"""
        os.makedirs(args.output_dir, exist_ok=True)
        
        if args.algorithm == 'rsa':
            key_size = args.key_size or 2048
            cipher = RSACipher(key_size)
            keys = cipher.generate_key_pair()
            
            public_key_path = os.path.join(args.output_dir, 'public_key.pem')
            private_key_path = os.path.join(args.output_dir, 'private_key.pem')
            
            with open(public_key_path, 'w') as f:
                f.write(keys['public_key'])
            with open(private_key_path, 'w') as f:
                f.write(keys['private_key'])
            
            print(f"{Fore.GREEN}✓ RSA key pair generated ({key_size} bits)")
            print(f"Public key: {public_key_path}")
            print(f"Private key: {private_key_path}")
        
        elif args.algorithm == 'aes':
            from src.utils import generate_random_key
            import base64
            
            key = generate_random_key(32)
            key_path = os.path.join(args.output_dir, 'aes_key.bin')
            
            with open(key_path, 'wb') as f:
                f.write(key)
            
            print(f"{Fore.GREEN}✓ AES-256 key generated")
            print(f"Key file: {key_path}")
            print(f"Key (base64): {base64.b64encode(key).decode()}")
    
    def _handle_hash(self, args):
        """Handle file hashing"""
        file_hash = calculate_file_hash(args.input, args.algorithm)
        print(f"{Fore.GREEN}✓ {args.algorithm.upper()} hash calculated")
        print(f"File: {args.input}")
        print(f"Hash: {Fore.CYAN}{file_hash}{Style.RESET_ALL}")
    
    def _handle_validate_password(self, args):
        """Handle password validation"""
        if args.password:
            password = args.password
        else:
            import getpass
            password = getpass.getpass("Enter password to validate: ")
        
        result = PasswordValidator.validate_strength(password)
        
        print(f"\n{Fore.CYAN}Password Strength Analysis:")
        print(f"{Style.RESET_ALL}{'=' * 40}")
        
        # Color based on strength
        if result['strength'] == 'Strong':
            strength_color = Fore.GREEN
        elif result['strength'] == 'Medium':
            strength_color = Fore.YELLOW
        else:
            strength_color = Fore.RED
        
        print(f"Strength: {strength_color}{result['strength']}{Style.RESET_ALL}")
        print(f"Score: {result['score']}/8")
        
        if result['feedback']:
            print(f"\nRecommendations:")
            for feedback in result['feedback']:
                print(f"  • {feedback}")
    
    def _handle_generate_password(self, args):
        """Handle password generation"""
        password = PasswordValidator.generate_strong_password(args.length)
        print(f"{Fore.GREEN}✓ Strong password generated:")
        print(f"{Fore.CYAN}{password}{Style.RESET_ALL}")
        
        # Validate it
        result = PasswordValidator.validate_strength(password)
        print(f"\nStrength: {Fore.GREEN}{result['strength']}{Style.RESET_ALL}")


def main():
    """Main entry point"""
    cli = CLI()
    cli.run()


if __name__ == '__main__':
    main()
