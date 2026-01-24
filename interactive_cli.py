"""
Enhanced Interactive CLI for Secure CipherStegno Tool
Beautiful, user-friendly command-line interface with menus and animations
No code to type - just select from menus!
"""

import sys
import os

# Check Python version before any other imports
if sys.version_info < (3, 8):
    sys.stderr.write("ERROR: Python 3.8 or higher is required\n")
    sys.exit(1)

# Add src to path
sys.path.insert(0, os.path.dirname(__file__))

from colorama import init, Fore, Style
import time
import json

# Initialize colorama
init(autoreset=True)

from src.crypto import (CaesarCipher, AESCipher, RSACipher, VigenereCipher, 
                         PlayfairCipher, RailFenceCipher, BlowfishCipher, 
                         DES3Cipher, ChaCha20Cipher)
from src.steganography import ImageSteganography, AudioSteganography, VideoSteganography
from src.utils import PasswordValidator, calculate_file_hash, Logger
from src.utils.cli_art import (ASCIIArt, Animations, MenuFormatter, InputHelper, 
                                clear_screen, print_header)
from src.utils.advanced_security import (EncryptionAnalyzer, SecureTokenGenerator,
                                          DataSanitizer, NetworkScanner)


class InteractiveCLI:
    """Enhanced interactive command-line interface"""
    
    def __init__(self):
        self.logger = Logger()
        self.running = True
    
    def run(self):
        """Run the interactive CLI"""
        print_header()
        
        while self.running:
            try:
                self._show_main_menu()
            except KeyboardInterrupt:
                print(f"\n\n{Fore.YELLOW}  Exiting gracefully...{Style.RESET_ALL}")
                break
            except Exception as e:
                MenuFormatter.print_info_box(
                    "Error Occurred",
                    [str(e), "Please try again or report this issue."],
                    "error"
                )
                input(f"{Fore.YELLOW}  Press Enter to continue...{Style.RESET_ALL}")
        
        self._exit_animation()
    
    def _show_main_menu(self):
        """Display main menu"""
        clear_screen()
        print(ASCIIArt.MAIN_BANNER)
        
        MenuFormatter.print_menu(
            "🔐 MAIN MENU",
            [
                "🔐 Cryptography - Encrypt & Decrypt",
                "🖼️  Steganography - Hide & Extract Messages",
                "🛠️  Security Tools - Password, Hash, Analysis",
                "ℹ️  Help & Information",
                "❌ Exit"
            ]
        )
        
        choice = InputHelper.get_choice("Select an option", range(1, 6))
        
        if choice == 0:
            self._cryptography_menu()
        elif choice == 1:
            self._steganography_menu()
        elif choice == 2:
            self._security_tools_menu()
        elif choice == 3:
            self._help_menu()
        elif choice == 4:
            self.running = False
    
    def _cryptography_menu(self):
        """Cryptography submenu"""
        while True:
            clear_screen()
            print(ASCIIArt.CRYPTO_ICON)
            
            MenuFormatter.print_menu(
                "🔐 CRYPTOGRAPHY",
                [
                    "🔒 Encrypt Message",
                    "🔓 Decrypt Message",
                    "🔑 Generate Keys",
                    "📊 Compare Algorithms",
                    "⬅️  Back to Main Menu"
                ]
            )
            
            choice = InputHelper.get_choice("Select an option", range(1, 6))
            
            if choice == 0:
                self._encrypt_menu()
            elif choice == 1:
                self._decrypt_menu()
            elif choice == 2:
                self._generate_keys_menu()
            elif choice == 3:
                self._compare_algorithms()
            elif choice == 4:
                break
    
    def _encrypt_menu(self):
        """Encryption menu"""
        clear_screen()
        MenuFormatter.print_section("🔒 ENCRYPTION", "🔐")
        
        # Select algorithm
        algorithms = [
            "Caesar Cipher (Simple)",
            "Vigenère Cipher (Classical)",
            "Playfair Cipher (Digraph)",
            "Rail Fence Cipher (Transposition)",
            "---",
            "AES-256 (Recommended)",
            "Blowfish (Fast)",
            "3DES (Legacy)",
            "ChaCha20 (Modern)",
            "---",
            "RSA (Public Key)",
            "---",
            "⬅️  Back to Previous Menu"
        ]
        
        MenuFormatter.print_menu("Select Encryption Algorithm", algorithms, show_header=False)
        algo_choice = InputHelper.get_choice("Algorithm", range(1, len(algorithms) + 1))
        
        if algo_choice is None or algo_choice == 11:  # Back option
            return
        
        # Get message
        print(f"\n{Fore.CYAN}{'─' * 70}{Style.RESET_ALL}")
        MenuFormatter.print_info_box(
            "Message Input",
            [
                "You can either:",
                "  1. Type your message directly",
                "  2. Enter the path to a text file (e.g., message.txt)",
                "",
                "The tool will automatically detect if it's a file path."
            ],
            "info"
        )
        
        message_input = InputHelper.get_input("Enter message or file path")
        
        if not message_input:
            print(f"{Fore.RED}  ✗ No message provided{Style.RESET_ALL}")
            input(f"{Fore.YELLOW}  Press Enter to continue...{Style.RESET_ALL}")
            return
        
        # Check if it's a file
        message = message_input
        if os.path.exists(message_input):
            try:
                with open(message_input, 'r') as f:
                    message = f.read()
                print(f"{Fore.GREEN}  ✓ Message loaded from file{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.YELLOW}  ⚠ Could not read as file, using as text: {e}{Style.RESET_ALL}")
                message = message_input
        
        # Encrypt based on algorithm
        Animations.encrypt_animation("Encrypting")
        
        try:
            result = None
            
            if algo_choice == 0:  # Caesar
                print(f"\n{Fore.CYAN}  Caesar Cipher shifts each letter by a fixed number.{Style.RESET_ALL}")
                shift = int(InputHelper.get_input("Enter shift value (1-25)", "3"))
                result = CaesarCipher.encrypt(message, shift)
                self._show_result("Encrypted Text", result, "success")
                
                # Ask to save
                if InputHelper.confirm("Save encrypted text to file?", default=True):
                    filename = InputHelper.get_input("Enter filename", "encrypted_caesar.txt")
                    with open(filename, 'w') as f:
                        f.write(result)
                    print(f"{Fore.GREEN}  ✓ Saved to {filename}{Style.RESET_ALL}")
            
            elif algo_choice == 1:  # Vigenere
                print(f"\n{Fore.CYAN}  Vigenère uses a keyword for polyalphabetic substitution.{Style.RESET_ALL}")
                key = InputHelper.get_input("Enter encryption key (word/phrase)")
                result = VigenereCipher.encrypt(message, key)
                self._show_result("Encrypted Text", result, "success")
                
                # Ask to save
                if InputHelper.confirm("Save encrypted text to file?", default=True):
                    filename = InputHelper.get_input("Enter filename", "encrypted_vigenere.txt")
                    with open(filename, 'w') as f:
                        f.write(result)
                    print(f"{Fore.GREEN}  ✓ Saved to {filename}{Style.RESET_ALL}")
            
            elif algo_choice == 2:  # Playfair
                print(f"\n{Fore.CYAN}  Playfair encrypts pairs of letters using a 5x5 matrix.{Style.RESET_ALL}")
                key = InputHelper.get_input("Enter encryption key")
                result = PlayfairCipher.encrypt(message, key)
                self._show_result("Encrypted Text", result, "success")
                
                # Ask to save
                if InputHelper.confirm("Save encrypted text to file?", default=True):
                    filename = InputHelper.get_input("Enter filename", "encrypted_playfair.txt")
                    with open(filename, 'w') as f:
                        f.write(result)
                    print(f"{Fore.GREEN}  ✓ Saved to {filename}{Style.RESET_ALL}")
            
            elif algo_choice == 3:  # Rail Fence
                print(f"\n{Fore.CYAN}  Rail Fence rearranges text in a zigzag pattern.{Style.RESET_ALL}")
                rails = int(InputHelper.get_input("Enter number of rails (2-10)", "3"))
                result = RailFenceCipher.encrypt(message, rails)
                self._show_result("Encrypted Text", result, "success")
                
                # Ask to save
                if InputHelper.confirm("Save encrypted text to file?", default=True):
                    filename = InputHelper.get_input("Enter filename", "encrypted_railfence.txt")
                    with open(filename, 'w') as f:
                        f.write(result)
                    print(f"{Fore.GREEN}  ✓ Saved to {filename}{Style.RESET_ALL}")
            
            elif algo_choice == 5:  # AES
                print(f"\n{Fore.CYAN}  AES-256 is the industry standard for secure encryption.{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}  💡 Tip: Use a strong password (12+ characters){Style.RESET_ALL}")
                password = InputHelper.get_input("Enter password")
                result = AESCipher.encrypt_with_password(message, password)
                
                # Ask to save
                filename = InputHelper.get_input("Save encrypted file as", "encrypted_aes.json")
                import json
                with open(filename, 'w') as f:
                    json.dump(result, f, indent=2)
                
                MenuFormatter.print_info_box(
                    "Encryption Successful",
                    [
                        f"✓ File saved as: {filename}",
                        "",
                        f"Ciphertext preview: {result['ciphertext'][:50]}...",
                        f"IV: {result['iv']}",
                        "",
                        "⚠️  Remember your password - you'll need it to decrypt!",
                        "⚠️  Keep the entire JSON file (contains ciphertext and IV)"
                    ],
                    "success"
                )
            
            elif algo_choice == 6:  # Blowfish
                print(f"\n{Fore.CYAN}  Blowfish is a fast and secure cipher.{Style.RESET_ALL}")
                password = InputHelper.get_input("Enter password")
                result = BlowfishCipher.encrypt_with_password(message, password)
                
                # Ask to save
                filename = InputHelper.get_input("Save encrypted file as", "encrypted_blowfish.json")
                import json
                with open(filename, 'w') as f:
                    json.dump(result, f, indent=2)
                
                MenuFormatter.print_info_box(
                    "Encryption Successful",
                    [
                        f"✓ File saved as: {filename}",
                        "",
                        f"Ciphertext preview: {result['ciphertext'][:50]}...",
                        f"IV: {result['iv']}",
                        "",
                        "⚠️  Remember your password for decryption!"
                    ],
                    "success"
                )
            
            elif algo_choice == 7:  # 3DES
                print(f"\n{Fore.YELLOW}  ⚠️  3DES is legacy - consider using AES for new projects.{Style.RESET_ALL}")
                if not InputHelper.confirm("Continue with 3DES?", default=False):
                    return
                
                password = InputHelper.get_input("Enter password")
                result = DES3Cipher.encrypt_with_password(message, password)
                
                # Ask to save
                filename = InputHelper.get_input("Save encrypted file as", "encrypted_3des.json")
                import json
                with open(filename, 'w') as f:
                    json.dump(result, f, indent=2)
                
                MenuFormatter.print_info_box(
                    "Encryption Complete",
                    [
                        f"✓ File saved as: {filename}",
                        "",
                        "⚠️  3DES is considered legacy. Use AES for better security."
                    ],
                    "warning"
                )
            
            elif algo_choice == 8:  # ChaCha20
                print(f"\n{Fore.CYAN}  ChaCha20 is a modern, fast stream cipher.{Style.RESET_ALL}")
                password = InputHelper.get_input("Enter password")
                result = ChaCha20Cipher.encrypt_with_password(message, password)
                
                # Ask to save
                filename = InputHelper.get_input("Save encrypted file as", "encrypted_chacha20.json")
                import json
                with open(filename, 'w') as f:
                    json.dump(result, f, indent=2)
                
                MenuFormatter.print_info_box(
                    "Encryption Successful",
                    [
                        f"✓ File saved as: {filename}",
                        "",
                        f"Ciphertext preview: {result['ciphertext'][:50]}...",
                        f"Nonce: {result['nonce']}",
                        "",
                        "✓ ChaCha20: Fast, modern, and secure!"
                    ],
                    "success"
                )
            
            elif algo_choice == 10:  # RSA
                print(f"\n{Fore.CYAN}  RSA uses public-key cryptography.{Style.RESET_ALL}")
                MenuFormatter.print_info_box(
                    "RSA Key Options",
                    [
                        "Choose one:",
                        "  1. Generate new key pair",
                        "  2. Load existing public key from file"
                    ],
                    "info"
                )
                
                key_choice = InputHelper.get_choice("Select option", range(1, 3))
                
                if key_choice == 0:  # Generate new
                    print(f"\n{Fore.YELLOW}  Generating RSA key pair...{Style.RESET_ALL}")
                    Animations.loading_spinner(1, "Generating keys")
                    
                    cipher = RSACipher(2048)
                    keys = cipher.generate_key_pair()
                    result = cipher.encrypt(message)
                    
                    # Save keys
                    if InputHelper.confirm("Save keys to files?", default=True):
                        pub_file = InputHelper.get_input("Public key filename", "public_key.pem")
                        priv_file = InputHelper.get_input("Private key filename", "private_key.pem")
                        enc_file = InputHelper.get_input("Encrypted message filename", "encrypted_rsa.txt")
                        
                        with open(pub_file, 'w') as f:
                            f.write(keys['public_key'])
                        with open(priv_file, 'w') as f:
                            f.write(keys['private_key'])
                        with open(enc_file, 'w') as f:
                            f.write(result)
                        
                        MenuFormatter.print_info_box(
                            "RSA Encryption Complete",
                            [
                                f"✓ Encrypted message saved: {enc_file}",
                                f"✓ Public key saved: {pub_file}",
                                f"✓ Private key saved: {priv_file}",
                                "",
                                "⚠️  Keep private key secure - needed for decryption!",
                                "✓ Share public key freely for others to encrypt messages"
                            ],
                            "success"
                        )
                    else:
                        self._show_result("Encrypted Text", result, "success")
                
                elif key_choice == 1:  # Load existing
                    pub_key_file = InputHelper.get_input("Enter public key file path")
                    if os.path.exists(pub_key_file):
                        with open(pub_key_file, 'r') as f:
                            public_key = f.read()
                        
                        cipher = RSACipher()
                        cipher.load_public_key(public_key)
                        result = cipher.encrypt(message)
                        
                        # Save encrypted message
                        if InputHelper.confirm("Save encrypted message?", default=True):
                            enc_file = InputHelper.get_input("Encrypted message filename", "encrypted_rsa.txt")
                            with open(enc_file, 'w') as f:
                                f.write(result)
                            print(f"{Fore.GREEN}  ✓ Encrypted message saved: {enc_file}{Style.RESET_ALL}")
                        else:
                            self._show_result("Encrypted Text", result, "success")
                    else:
                        print(f"{Fore.RED}  ✗ Public key file not found{Style.RESET_ALL}")
        
        except Exception as e:
            MenuFormatter.print_info_box("Encryption Failed", [str(e)], "error")
        
        input(f"\n{Fore.YELLOW}  Press Enter to continue...{Style.RESET_ALL}")
    
    def _decrypt_menu(self):
        """Decryption menu"""
        clear_screen()
        MenuFormatter.print_section("🔓 DECRYPTION", "🔐")
        
        # Select algorithm
        algorithms = [
            "Caesar Cipher (Simple)",
            "Vigenère Cipher (Classical)",
            "Playfair Cipher (Digraph)",
            "Rail Fence Cipher (Transposition)",
            "---",
            "AES-256 (Recommended)",
            "Blowfish (Fast)",
            "3DES (Legacy)",
            "ChaCha20 (Modern)",
            "---",
            "RSA (Public Key)",
            "---",
            "⬅️  Back to Previous Menu"
        ]
        
        MenuFormatter.print_menu("Select Decryption Algorithm", algorithms, show_header=False)
        algo_choice = InputHelper.get_choice("Algorithm", range(1, len(algorithms) + 1))
        
        if algo_choice is None or algo_choice == 11:  # Back option
            return
        
        print(f"\n{Fore.CYAN}{'─' * 70}{Style.RESET_ALL}")
        
        # Handle decryption based on algorithm
        try:
            if algo_choice in [0, 1, 2, 3]:  # Classical ciphers
                cipher_names = ["Caesar", "Vigenère", "Playfair", "Rail Fence"]
                cipher_name = cipher_names[algo_choice]
                
                print(f"\n{Fore.CYAN}  Decrypting with {cipher_name} Cipher{Style.RESET_ALL}")
                
                # Get encrypted text
                MenuFormatter.print_info_box(
                    "Input Options",
                    [
                        "Enter encrypted text directly, or",
                        "Enter the path to a file containing encrypted text"
                    ],
                    "info"
                )
                
                encrypted_input = InputHelper.get_input("Enter encrypted text or file path")
                
                if not encrypted_input:
                    print(f"{Fore.RED}  ✗ No input provided{Style.RESET_ALL}")
                    input(f"{Fore.YELLOW}  Press Enter to continue...{Style.RESET_ALL}")
                    return
                
                # Check if it's a file
                encrypted_text = encrypted_input
                if os.path.exists(encrypted_input):
                    try:
                        with open(encrypted_input, 'r') as f:
                            encrypted_text = f.read()
                        print(f"{Fore.GREEN}  ✓ Encrypted text loaded from file{Style.RESET_ALL}")
                    except Exception as e:
                        print(f"{Fore.YELLOW}  ⚠ Could not read as file, using as text{Style.RESET_ALL}")
                        encrypted_text = encrypted_input
                
                # Get decryption parameters and decrypt
                Animations.loading_spinner(0.5, "Decrypting")
                
                if algo_choice == 0:  # Caesar
                    shift = int(InputHelper.get_input("Enter shift value (same as encryption)", "3"))
                    result = CaesarCipher.decrypt(encrypted_text, shift)
                elif algo_choice == 1:  # Vigenere
                    key = InputHelper.get_input("Enter decryption key (same as encryption)")
                    result = VigenereCipher.decrypt(encrypted_text, key)
                elif algo_choice == 2:  # Playfair
                    key = InputHelper.get_input("Enter decryption key (same as encryption)")
                    result = PlayfairCipher.decrypt(encrypted_text, key)
                elif algo_choice == 3:  # Rail Fence
                    rails = int(InputHelper.get_input("Enter number of rails (same as encryption)", "3"))
                    result = RailFenceCipher.decrypt(encrypted_text, rails)
                
                MenuFormatter.print_info_box(
                    "Decryption Successful",
                    [
                        "Decrypted message:",
                        "",
                        result[:200] + ("..." if len(result) > 200 else "")
                    ],
                    "success"
                )
                
                # Ask to save
                if InputHelper.confirm("Save decrypted text to file?", default=True):
                    filename = InputHelper.get_input("Enter filename", f"decrypted_{cipher_name.lower().replace(' ', '_')}.txt")
                    with open(filename, 'w') as f:
                        f.write(result)
                    print(f"{Fore.GREEN}  ✓ Saved to {filename}{Style.RESET_ALL}")
            
            elif algo_choice in [5, 6, 7, 8]:  # Modern symmetric ciphers
                cipher_names = ["AES-256", "Blowfish", "3DES", "ChaCha20"]
                cipher_name = cipher_names[algo_choice - 5]
                
                print(f"\n{Fore.CYAN}  Decrypting with {cipher_name}{Style.RESET_ALL}")
                
                MenuFormatter.print_info_box(
                    f"{cipher_name} Decryption",
                    [
                        "You need:",
                        f"  1. The encrypted JSON file (contains ciphertext and IV/nonce)",
                        f"  2. The password used for encryption"
                    ],
                    "info"
                )
                
                encrypted_file = InputHelper.get_input("Enter encrypted JSON file path")
                
                if not os.path.exists(encrypted_file):
                    print(f"{Fore.RED}  ✗ File not found: {encrypted_file}{Style.RESET_ALL}")
                    input(f"{Fore.YELLOW}  Press Enter to continue...{Style.RESET_ALL}")
                    return
                
                # Load encrypted data
                with open(encrypted_file, 'r') as f:
                    encrypted_data = json.load(f)
                
                password = InputHelper.get_input("Enter password (same as encryption)")
                
                Animations.loading_spinner(0.5, "Decrypting")
                
                # Decrypt based on algorithm
                if algo_choice == 5:  # AES
                    result = AESCipher.decrypt_with_password(
                        encrypted_data['ciphertext'],
                        encrypted_data['iv'],
                        password
                    )
                elif algo_choice == 6:  # Blowfish
                    result = BlowfishCipher.decrypt_with_password(
                        encrypted_data['ciphertext'],
                        encrypted_data['iv'],
                        password
                    )
                elif algo_choice == 7:  # 3DES
                    result = DES3Cipher.decrypt_with_password(
                        encrypted_data['ciphertext'],
                        encrypted_data['iv'],
                        password
                    )
                elif algo_choice == 8:  # ChaCha20
                    result = ChaCha20Cipher.decrypt_with_password(
                        encrypted_data['ciphertext'],
                        encrypted_data['nonce'],
                        password
                    )
                
                MenuFormatter.print_info_box(
                    "Decryption Successful",
                    [
                        "Decrypted message:",
                        "",
                        result[:200] + ("..." if len(result) > 200 else "")
                    ],
                    "success"
                )
                
                # Ask to save
                if InputHelper.confirm("Save decrypted text to file?", default=True):
                    filename = InputHelper.get_input("Enter filename", f"decrypted_{cipher_name.lower()}.txt")
                    with open(filename, 'w') as f:
                        f.write(result)
                    print(f"{Fore.GREEN}  ✓ Saved to {filename}{Style.RESET_ALL}")
            
            elif algo_choice == 10:  # RSA
                print(f"\n{Fore.CYAN}  RSA Decryption requires your private key.{Style.RESET_ALL}")
                
                MenuFormatter.print_info_box(
                    "RSA Decryption Requirements",
                    [
                        "You need:",
                        "  1. The encrypted message file",
                        "  2. Your private key file (keep this secure!)"
                    ],
                    "info"
                )
                
                encrypted_file = InputHelper.get_input("Enter encrypted message file path")
                private_key_file = InputHelper.get_input("Enter private key file path")
                
                if not os.path.exists(encrypted_file):
                    print(f"{Fore.RED}  ✗ Encrypted file not found{Style.RESET_ALL}")
                    input(f"{Fore.YELLOW}  Press Enter to continue...{Style.RESET_ALL}")
                    return
                
                if not os.path.exists(private_key_file):
                    print(f"{Fore.RED}  ✗ Private key file not found{Style.RESET_ALL}")
                    input(f"{Fore.YELLOW}  Press Enter to continue...{Style.RESET_ALL}")
                    return
                
                # Load files
                with open(encrypted_file, 'r') as f:
                    encrypted_text = f.read()
                
                with open(private_key_file, 'r') as f:
                    private_key = f.read()
                
                Animations.loading_spinner(1, "Decrypting with RSA")
                
                cipher = RSACipher()
                cipher.load_private_key(private_key)
                result = cipher.decrypt(encrypted_text)
                
                MenuFormatter.print_info_box(
                    "Decryption Successful",
                    [
                        "Decrypted message:",
                        "",
                        result[:200] + ("..." if len(result) > 200 else "")
                    ],
                    "success"
                )
                
                # Ask to save
                if InputHelper.confirm("Save decrypted text to file?", default=True):
                    filename = InputHelper.get_input("Enter filename", "decrypted_rsa.txt")
                    with open(filename, 'w') as f:
                        f.write(result)
                    print(f"{Fore.GREEN}  ✓ Saved to {filename}{Style.RESET_ALL}")
        
        except Exception as e:
            MenuFormatter.print_info_box(
                "Decryption Failed",
                [
                    str(e),
                    "",
                    "Common issues:",
                    "  • Wrong password",
                    "  • Wrong key/shift value",
                    "  • Corrupted encrypted file",
                    "  • Wrong algorithm selected"
                ],
                "error"
            )
        
        input(f"\n{Fore.YELLOW}  Press Enter to continue...{Style.RESET_ALL}")
    
    def _generate_keys_menu(self):
        """Generate cryptographic keys"""
        clear_screen()
        MenuFormatter.print_section("🔑 KEY GENERATION", "🔐")
        
        MenuFormatter.print_menu(
            "Select Key Type",
            [
                "RSA Key Pair (2048-bit)",
                "RSA Key Pair (4096-bit)",
                "AES-256 Key",
                "Secure API Token",
                "Session Token"
            ],
            show_header=False
        )
        
        choice = InputHelper.get_choice("Key type", range(1, 6))
        
        if choice is None:
            return
        
        Animations.loading_spinner(1, "Generating secure keys")
        
        try:
            if choice == 0:  # RSA 2048
                cipher = RSACipher(2048)
                keys = cipher.generate_key_pair()
                MenuFormatter.print_info_box(
                    "RSA-2048 Keys Generated",
                    [
                        f"Public Key: {keys['public_key'][:50]}...",
                        f"Private Key: {keys['private_key'][:50]}...",
                        "",
                        "⚠️  Store private key securely!"
                    ],
                    "success"
                )
            
            elif choice == 1:  # RSA 4096
                cipher = RSACipher(4096)
                keys = cipher.generate_key_pair()
                MenuFormatter.print_info_box(
                    "RSA-4096 Keys Generated",
                    [
                        "Higher security level with 4096-bit keys",
                        "",
                        "⚠️  Store private key securely!"
                    ],
                    "success"
                )
            
            elif choice == 3:  # API Token
                token = SecureTokenGenerator.generate_api_key()
                self._show_result("API Key Generated", token, "success")
            
            elif choice == 4:  # Session Token
                token = SecureTokenGenerator.generate_session_token()
                MenuFormatter.print_info_box(
                    "Session Token Generated",
                    [
                        f"Token: {token['token']}",
                        f"Expires in: {token['expires_in']} seconds"
                    ],
                    "success"
                )
        
        except Exception as e:
            MenuFormatter.print_info_box("Key Generation Failed", [str(e)], "error")
        
        input(f"\n{Fore.YELLOW}  Press Enter to continue...{Style.RESET_ALL}")
    
    def _compare_algorithms(self):
        """Compare encryption algorithms"""
        clear_screen()
        MenuFormatter.print_section("📊 ALGORITHM COMPARISON", "📊")
        
        algorithms = ['aes', 'rsa', 'blowfish', '3des', 'chacha20', 'caesar', 'vigenere']
        comparison = EncryptionAnalyzer.compare_algorithms(algorithms)
        
        print(f"{Fore.CYAN}{'═' * 90}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{'Algorithm':<20} {'Strength':<15} {'Security Level':<15} {'Recommended':<15}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'═' * 90}{Style.RESET_ALL}")
        
        for algo in comparison['algorithms']:
            rec_symbol = "✓" if algo['recommended'] else "✗"
            rec_color = Fore.GREEN if algo['recommended'] else Fore.RED
            
            print(f"{Fore.WHITE}{algo['name']:<20} {algo['strength']:<15} "
                  f"{algo['security_level']:<15} {rec_color}{rec_symbol:<15}{Style.RESET_ALL}")
        
        print(f"{Fore.CYAN}{'═' * 90}{Style.RESET_ALL}\n")
        
        MenuFormatter.print_info_box(
            "Recommendation",
            [
                f"Strongest: {comparison['strongest']}",
                f"Weakest: {comparison['weakest']}",
                "",
                "For modern applications, use AES-256 or ChaCha20"
            ],
            "info"
        )
        
        input(f"\n{Fore.YELLOW}  Press Enter to continue...{Style.RESET_ALL}")
    
    def _steganography_menu(self):
        """Steganography submenu"""
        while True:
            clear_screen()
            print(ASCIIArt.STEGO_ICON)
            
            MenuFormatter.print_menu(
                "🖼️  STEGANOGRAPHY",
                [
                    "📥 Hide Message in Image",
                    "📤 Extract Message from Image",
                    "🎵 Hide Message in Audio",
                    "🎵 Extract Message from Audio",
                    "🎬 Hide Message in Video",
                    "🎬 Extract Message from Video",
                    "⬅️  Back to Main Menu"
                ]
            )
            
            choice = InputHelper.get_choice("Select an option", range(1, 8))
            
            if choice == 6:
                break
            elif choice is not None:
                self._handle_steganography(choice)
    
    def _handle_steganography(self, choice):
        """Handle steganography operations"""
        clear_screen()
        
        if choice == 0:  # Hide in image
            MenuFormatter.print_section("📥 HIDE MESSAGE IN IMAGE", "🖼️")
            
            MenuFormatter.print_info_box(
                "Image Steganography - Encoding",
                [
                    "Hide secret messages inside images using LSB technique.",
                    "",
                    "You'll need:",
                    "  1. A cover image (PNG, BMP recommended)",
                    "  2. Your secret message (text or file)",
                    "",
                    "The output will look identical to the original!"
                ],
                "info"
            )
            
            # Get cover image
            cover_image = InputHelper.get_input("Enter cover image path (e.g., photo.png)")
            
            if not os.path.exists(cover_image):
                print(f"{Fore.RED}  ✗ Cover image not found{Style.RESET_ALL}")
                input(f"{Fore.YELLOW}  Press Enter to continue...{Style.RESET_ALL}")
                return
            
            # Get message
            MenuFormatter.print_info_box(
                "Message Input",
                [
                    "Enter your secret message, or",
                    "Provide path to a text file"
                ],
                "info"
            )
            
            message_input = InputHelper.get_input("Enter message or file path")
            
            if not message_input:
                print(f"{Fore.RED}  ✗ No message provided{Style.RESET_ALL}")
                input(f"{Fore.YELLOW}  Press Enter to continue...{Style.RESET_ALL}")
                return
            
            # Check if it's a file
            message = message_input
            if os.path.exists(message_input):
                try:
                    with open(message_input, 'r') as f:
                        message = f.read()
                    print(f"{Fore.GREEN}  ✓ Message loaded from file{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.YELLOW}  ⚠ Using input as text message{Style.RESET_ALL}")
                    message = message_input
            
            # Get output filename
            output_file = InputHelper.get_input("Enter output image path", "stego_output.png")
            
            # Ask about compression
            compress = InputHelper.confirm("Enable compression? (allows larger messages)", default=True)
            
            # Encode
            try:
                Animations.loading_spinner(1, "Hiding message in image")
                result = ImageSteganography.encode(cover_image, message, output_file, compress)
                
                MenuFormatter.print_info_box(
                    "Message Hidden Successfully",
                    [
                        f"✓ Stego image saved as: {output_file}",
                        f"✓ Message size: {result['message_size']} bytes",
                        f"✓ Compressed: {'Yes' if compress else 'No'}",
                        "",
                        "The image looks identical to the original!",
                        "Remember: Keep track of compression setting for extraction."
                    ],
                    "success"
                )
            except Exception as e:
                MenuFormatter.print_info_box(
                    "Encoding Failed",
                    [
                        str(e),
                        "",
                        "Possible solutions:",
                        "  • Use a larger cover image",
                        "  • Enable compression",
                        "  • Reduce message size"
                    ],
                    "error"
                )
        
        elif choice == 1:  # Extract from image
            MenuFormatter.print_section("📤 EXTRACT MESSAGE FROM IMAGE", "🖼️")
            
            MenuFormatter.print_info_box(
                "Image Steganography - Decoding",
                [
                    "Extract hidden messages from stego images.",
                    "",
                    "Important: Know if compression was used during encoding!"
                ],
                "info"
            )
            
            # Get stego image
            stego_image = InputHelper.get_input("Enter stego image path")
            
            if not os.path.exists(stego_image):
                print(f"{Fore.RED}  ✗ Stego image not found{Style.RESET_ALL}")
                input(f"{Fore.YELLOW}  Press Enter to continue...{Style.RESET_ALL}")
                return
            
            # Ask about compression
            compressed = InputHelper.confirm("Was the message compressed during encoding?", default=True)
            
            # Decode
            try:
                Animations.loading_spinner(1, "Extracting hidden message")
                message = ImageSteganography.decode(stego_image, compressed)
                
                MenuFormatter.print_info_box(
                    "Message Extracted Successfully",
                    [
                        "Hidden message:",
                        "",
                        message[:300] + ("..." if len(message) > 300 else "")
                    ],
                    "success"
                )
                
                # Ask to save
                if InputHelper.confirm("Save extracted message to file?", default=True):
                    output_file = InputHelper.get_input("Enter output filename", "extracted_message.txt")
                    with open(output_file, 'w') as f:
                        f.write(message)
                    print(f"{Fore.GREEN}  ✓ Message saved to {output_file}{Style.RESET_ALL}")
            
            except Exception as e:
                MenuFormatter.print_info_box(
                    "Extraction Failed",
                    [
                        str(e),
                        "",
                        "Common issues:",
                        "  • Wrong compression setting",
                        "  • Image was modified or compressed after encoding",
                        "  • No hidden message in this image"
                    ],
                    "error"
                )
        
        elif choice in [2, 3]:  # Audio stego
            operation = "Hide" if choice == 2 else "Extract"
            MenuFormatter.print_section(f"🎵 {operation.upper()} MESSAGE IN AUDIO", "🎵")
            
            MenuFormatter.print_info_box(
                "Audio Steganography",
                [
                    "Hide secret messages in WAV audio files.",
                    "",
                    "Note: Only WAV format is supported.",
                    "Larger audio files can hide more data."
                ],
                "info"
            )
            
            if choice == 2:  # Hide
                cover_audio = InputHelper.get_input("Enter cover audio path (WAV file)")
                
                if not os.path.exists(cover_audio):
                    print(f"{Fore.RED}  ✗ Cover audio not found{Style.RESET_ALL}")
                    input(f"{Fore.YELLOW}  Press Enter to continue...{Style.RESET_ALL}")
                    return
                
                message_input = InputHelper.get_input("Enter message or file path")
                
                if not message_input:
                    print(f"{Fore.RED}  ✗ No message provided{Style.RESET_ALL}")
                    input(f"{Fore.YELLOW}  Press Enter to continue...{Style.RESET_ALL}")
                    return
                
                # Check if message is a file
                message = message_input
                if os.path.exists(message_input):
                    try:
                        with open(message_input, 'r') as f:
                            message = f.read()
                        print(f"{Fore.GREEN}  ✓ Message loaded from file{Style.RESET_ALL}")
                    except Exception as e:
                        message = message_input
                
                output_file = InputHelper.get_input("Enter output audio path", "stego_audio.wav")
                
                try:
                    Animations.loading_spinner(1, "Hiding message in audio")
                    result = AudioSteganography.encode(cover_audio, message, output_file)
                    
                    MenuFormatter.print_info_box(
                        "Message Hidden Successfully",
                        [
                            f"✓ Stego audio saved as: {output_file}",
                            f"✓ Audio duration: {result['audio_duration']:.2f} seconds",
                            "",
                            "The audio sounds identical to the original!"
                        ],
                        "success"
                    )
                except Exception as e:
                    MenuFormatter.print_info_box("Encoding Failed", [str(e)], "error")
            
            else:  # Extract
                stego_audio = InputHelper.get_input("Enter stego audio path (WAV file)")
                
                if not os.path.exists(stego_audio):
                    print(f"{Fore.RED}  ✗ Stego audio not found{Style.RESET_ALL}")
                    input(f"{Fore.YELLOW}  Press Enter to continue...{Style.RESET_ALL}")
                    return
                
                try:
                    Animations.loading_spinner(1, "Extracting hidden message")
                    message = AudioSteganography.decode(stego_audio)
                    
                    MenuFormatter.print_info_box(
                        "Message Extracted Successfully",
                        [
                            "Hidden message:",
                            "",
                            message[:300] + ("..." if len(message) > 300 else "")
                        ],
                        "success"
                    )
                    
                    if InputHelper.confirm("Save extracted message to file?", default=True):
                        output_file = InputHelper.get_input("Enter output filename", "extracted_audio_message.txt")
                        with open(output_file, 'w') as f:
                            f.write(message)
                        print(f"{Fore.GREEN}  ✓ Message saved to {output_file}{Style.RESET_ALL}")
                
                except Exception as e:
                    MenuFormatter.print_info_box("Extraction Failed", [str(e)], "error")
        
        elif choice in [4, 5]:  # Video stego
            MenuFormatter.print_section("🎬 VIDEO STEGANOGRAPHY", "🎬")
            MenuFormatter.print_info_box(
                "Video Steganography",
                [
                    "Hide messages in video files (MP4, AVI).",
                    "",
                    "Requirements:",
                    "  • ffmpeg must be installed on your system",
                    "  • Large video files work best",
                    "",
                    "This feature uses LSB on video frames."
                ],
                "info"
            )
        
        input(f"\n{Fore.YELLOW}  Press Enter to continue...{Style.RESET_ALL}")
    
    def _security_tools_menu(self):
        """Security tools submenu"""
        while True:
            clear_screen()
            print(ASCIIArt.TOOLS_ICON)
            
            MenuFormatter.print_menu(
                "🛠️  SECURITY TOOLS",
                [
                    "🔐 Generate Strong Password",
                    "✅ Validate Password Strength",
                    "#️⃣ Calculate File Hash",
                    "🔍 Scan Network Ports",
                    "🧹 Sanitize Filename",
                    "⬅️  Back to Main Menu"
                ]
            )
            
            choice = InputHelper.get_choice("Select an option", range(1, 7))
            
            if choice == 0:
                self._generate_password()
            elif choice == 1:
                self._validate_password()
            elif choice == 2:
                self._calculate_hash()
            elif choice == 3:
                self._scan_ports()
            elif choice == 4:
                self._sanitize_filename()
            elif choice == 5:
                break
    
    def _generate_password(self):
        """Generate strong password"""
        clear_screen()
        MenuFormatter.print_section("🔐 PASSWORD GENERATOR", "🔐")
        
        length = int(InputHelper.get_input("Password length", "16"))
        
        Animations.loading_spinner(0.5, "Generating secure password")
        
        password = PasswordValidator.generate_strong_password(length)
        validation = PasswordValidator.validate_strength(password)
        
        MenuFormatter.print_info_box(
            "Password Generated",
            [
                f"Password: {password}",
                "",
                f"Strength: {validation['strength']}",
                f"Score: {validation['score']}/8",
                "",
                "✓ Copy this password to a secure location!"
            ],
            "success"
        )
        
        input(f"\n{Fore.YELLOW}  Press Enter to continue...{Style.RESET_ALL}")
    
    def _validate_password(self):
        """Validate password strength"""
        clear_screen()
        MenuFormatter.print_section("✅ PASSWORD VALIDATOR", "✅")
        
        password = InputHelper.get_input("Enter password to validate")
        
        if not password:
            return
        
        Animations.loading_spinner(0.5, "Analyzing password")
        
        result = PasswordValidator.validate_strength(password)
        
        strength_colors = {
            'Strong': Fore.GREEN,
            'Medium': Fore.YELLOW,
            'Weak': Fore.RED
        }
        
        color = strength_colors.get(result['strength'], Fore.WHITE)
        
        print(f"\n{Fore.CYAN}{'═' * 70}{Style.RESET_ALL}")
        MenuFormatter.print_key_value("Password Strength", f"{color}{result['strength']}{Style.RESET_ALL}")
        MenuFormatter.print_key_value("Score", f"{result['score']}/8")
        MenuFormatter.print_key_value("Valid", "✓ Yes" if result['valid'] else "✗ No")
        print(f"{Fore.CYAN}{'═' * 70}{Style.RESET_ALL}")
        
        if result['feedback']:
            print(f"\n{Fore.YELLOW}  Recommendations:{Style.RESET_ALL}")
            for feedback in result['feedback']:
                print(f"{Fore.WHITE}    • {feedback}{Style.RESET_ALL}")
        
        input(f"\n{Fore.YELLOW}  Press Enter to continue...{Style.RESET_ALL}")
    
    def _calculate_hash(self):
        """Calculate file hash"""
        clear_screen()
        MenuFormatter.print_section("#️⃣ FILE HASH CALCULATOR", "#️⃣")
        
        print(f"{Fore.CYAN}  File hash calculation feature{Style.RESET_ALL}")
        input(f"\n{Fore.YELLOW}  Press Enter to continue...{Style.RESET_ALL}")
    
    def _scan_ports(self):
        """Scan network ports"""
        clear_screen()
        MenuFormatter.print_section("🔍 NETWORK PORT SCANNER", "🔍")
        
        MenuFormatter.print_info_box(
            "Warning",
            [
                "Port scanning should only be done on systems you own or",
                "have explicit permission to test.",
                "",
                "Unauthorized port scanning may be illegal in your jurisdiction."
            ],
            "warning"
        )
        
        if not InputHelper.confirm("Do you have permission to scan this host?"):
            return
        
        host = InputHelper.get_input("Enter host to scan", "localhost")
        
        print(f"\n{Fore.CYAN}  Scanning {host}...{Style.RESET_ALL}")
        Animations.loading_spinner(2, "Scanning common ports")
        
        try:
            results = NetworkScanner.scan_common_ports(host, timeout=1)
            
            if results['total_open'] > 0:
                print(f"\n{Fore.GREEN}  Found {results['total_open']} open ports:{Style.RESET_ALL}\n")
                
                print(f"{Fore.CYAN}  {'Port':<10} {'Service':<20} {'Status':<10}{Style.RESET_ALL}")
                print(f"{Fore.CYAN}  {'─' * 40}{Style.RESET_ALL}")
                
                for port_info in results['open_ports']:
                    print(f"  {Fore.WHITE}{port_info['port']:<10} {port_info['service']:<20} "
                          f"{Fore.GREEN}{port_info['status']:<10}{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.YELLOW}  No open ports found.{Style.RESET_ALL}")
        
        except Exception as e:
            MenuFormatter.print_info_box("Scan Failed", [str(e)], "error")
        
        input(f"\n{Fore.YELLOW}  Press Enter to continue...{Style.RESET_ALL}")
    
    def _sanitize_filename(self):
        """Sanitize filename"""
        clear_screen()
        MenuFormatter.print_section("🧹 FILENAME SANITIZER", "🧹")
        
        filename = InputHelper.get_input("Enter filename to sanitize")
        
        if not filename:
            return
        
        sanitized = DataSanitizer.sanitize_filename(filename)
        
        MenuFormatter.print_info_box(
            "Sanitization Complete",
            [
                f"Original:  {filename}",
                f"Sanitized: {sanitized}",
                "",
                "✓ Safe for filesystem use"
            ],
            "success"
        )
        
        input(f"\n{Fore.YELLOW}  Press Enter to continue...{Style.RESET_ALL}")
    
    def _help_menu(self):
        """Help and information"""
        while True:
            clear_screen()
            MenuFormatter.print_section("ℹ️  HELP & INFORMATION", "ℹ️")
            
            MenuFormatter.print_menu(
                "Help Topics",
                [
                    "📖 About This Tool",
                    "🚀 Getting Started Guide",
                    "🔐 Cryptography Basics",
                    "🖼️  Steganography Basics",
                    "💡 Tips & Best Practices",
                    "⬅️  Back to Main Menu"
                ],
                show_header=False
            )
            
            choice = InputHelper.get_choice("Select topic", range(1, 7))
            
            if choice == 5 or choice is None:
                break
            elif choice == 0:
                self._show_about()
            elif choice == 1:
                self._show_getting_started()
            elif choice == 2:
                self._show_crypto_basics()
            elif choice == 3:
                self._show_stego_basics()
            elif choice == 4:
                self._show_tips()
    
    def _show_about(self):
        """Show about information"""
        clear_screen()
        MenuFormatter.print_section("📖 ABOUT", "ℹ️")
        
        MenuFormatter.print_info_box(
            "Secure CipherStegno Tool",
            [
                "Version: 3.2.0",
                "Platform: Cross-platform (Windows, Linux, macOS)",
                "",
                "A comprehensive security toolkit featuring:",
                "  🔐 Multiple encryption algorithms",
                "  🖼️  Steganography (Image, Audio, Video)",
                "  🛠️  Security analysis tools",
                "  🔑 Password generation and validation",
                "",
                "© 2025 Parth Thakar | MIT License",
                "",
                "GitHub: github.com/parththakar2003/Secure-CipherStegno-Tool"
            ],
            "info"
        )
        
        input(f"\n{Fore.YELLOW}  Press Enter to continue...{Style.RESET_ALL}")
    
    def _show_getting_started(self):
        """Show getting started guide"""
        clear_screen()
        MenuFormatter.print_section("🚀 GETTING STARTED", "📖")
        
        print(f"\n{Fore.CYAN}{'═' * 70}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  Welcome to the Interactive CLI!{Style.RESET_ALL}\n")
        print(f"{Fore.WHITE}  This interface is designed to be simple - no commands to type!{Style.RESET_ALL}")
        print(f"{Fore.WHITE}  Just select options from menus using numbers.{Style.RESET_ALL}\n")
        print(f"{Fore.CYAN}{'═' * 70}{Style.RESET_ALL}\n")
        
        MenuFormatter.print_info_box(
            "Quick Start Steps",
            [
                "1️⃣  Select a feature from the main menu:",
                "   • Cryptography - Encrypt/decrypt messages",
                "   • Steganography - Hide messages in files",
                "   • Security Tools - Passwords, hashing, scanning",
                "",
                "2️⃣  Follow the prompts:",
                "   • Enter text directly, or provide file paths",
                "   • All inputs are validated and user-friendly",
                "",
                "3️⃣  Results are displayed clearly:",
                "   • Option to save to files",
                "   • Detailed success/error messages",
                "",
                "💡 Tip: You can press Ctrl+C anytime to cancel"
            ],
            "info"
        )
        
        print(f"\n{Fore.YELLOW}  Example Workflow:{Style.RESET_ALL}")
        print(f"{Fore.WHITE}  1. Choose 'Cryptography' from main menu{Style.RESET_ALL}")
        print(f"{Fore.WHITE}  2. Select 'Encrypt Message'{Style.RESET_ALL}")
        print(f"{Fore.WHITE}  3. Pick an algorithm (e.g., AES-256){Style.RESET_ALL}")
        print(f"{Fore.WHITE}  4. Enter your message{Style.RESET_ALL}")
        print(f"{Fore.WHITE}  5. Provide a password{Style.RESET_ALL}")
        print(f"{Fore.WHITE}  6. Save the encrypted file{Style.RESET_ALL}")
        print(f"{Fore.WHITE}  7. Done! 🎉{Style.RESET_ALL}\n")
        
        input(f"{Fore.YELLOW}  Press Enter to continue...{Style.RESET_ALL}")
    
    def _show_crypto_basics(self):
        """Show cryptography basics"""
        clear_screen()
        MenuFormatter.print_section("🔐 CRYPTOGRAPHY BASICS", "📖")
        
        MenuFormatter.print_info_box(
            "What is Cryptography?",
            [
                "Cryptography is the practice of securing information by",
                "transforming it into an unreadable format (encryption).",
                "Only authorized parties can decrypt it back."
            ],
            "info"
        )
        
        print(f"\n{Fore.YELLOW}  📚 Available Algorithms:{Style.RESET_ALL}\n")
        
        print(f"{Fore.CYAN}  Classical Ciphers (Educational):{Style.RESET_ALL}")
        print(f"{Fore.WHITE}    • Caesar - Simple letter shifting{Style.RESET_ALL}")
        print(f"{Fore.WHITE}    • Vigenère - Keyword-based encryption{Style.RESET_ALL}")
        print(f"{Fore.WHITE}    • Playfair - Digraph substitution{Style.RESET_ALL}")
        print(f"{Fore.WHITE}    • Rail Fence - Transposition cipher{Style.RESET_ALL}\n")
        
        print(f"{Fore.CYAN}  Modern Symmetric Encryption (Recommended):{Style.RESET_ALL}")
        print(f"{Fore.WHITE}    • AES-256 - Industry standard, very secure{Style.RESET_ALL}")
        print(f"{Fore.WHITE}    • ChaCha20 - Modern, fast stream cipher{Style.RESET_ALL}")
        print(f"{Fore.WHITE}    • Blowfish - Fast block cipher{Style.RESET_ALL}\n")
        
        print(f"{Fore.CYAN}  Asymmetric Encryption:{Style.RESET_ALL}")
        print(f"{Fore.WHITE}    • RSA - Public/private key pairs{Style.RESET_ALL}")
        print(f"{Fore.WHITE}    • Use for key exchange or small data{Style.RESET_ALL}\n")
        
        MenuFormatter.print_info_box(
            "When to Use What?",
            [
                "✅ For most uses: AES-256",
                "✅ For learning: Classical ciphers",
                "✅ For secure messaging: RSA + AES (hybrid)",
                "✅ For mobile/IoT: ChaCha20"
            ],
            "success"
        )
        
        input(f"\n{Fore.YELLOW}  Press Enter to continue...{Style.RESET_ALL}")
    
    def _show_stego_basics(self):
        """Show steganography basics"""
        clear_screen()
        MenuFormatter.print_section("🖼️  STEGANOGRAPHY BASICS", "📖")
        
        MenuFormatter.print_info_box(
            "What is Steganography?",
            [
                "Steganography hides secret messages inside ordinary files",
                "(images, audio, video) so no one knows a message exists.",
                "",
                "Unlike encryption which scrambles data, steganography",
                "hides it in plain sight!"
            ],
            "info"
        )
        
        print(f"\n{Fore.YELLOW}  📸 How It Works:{Style.RESET_ALL}\n")
        print(f"{Fore.WHITE}  Image Steganography:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}    • Uses LSB (Least Significant Bit) technique{Style.RESET_ALL}")
        print(f"{Fore.CYAN}    • Changes tiny pixel values imperceptibly{Style.RESET_ALL}")
        print(f"{Fore.CYAN}    • Output looks identical to the original{Style.RESET_ALL}\n")
        
        print(f"{Fore.WHITE}  Audio Steganography:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}    • Hides data in audio waveform samples{Style.RESET_ALL}")
        print(f"{Fore.CYAN}    • Sounds identical to original audio{Style.RESET_ALL}")
        print(f"{Fore.CYAN}    • Works with WAV files{Style.RESET_ALL}\n")
        
        MenuFormatter.print_info_box(
            "Best Practices",
            [
                "✅ Use PNG or BMP for images (lossless formats)",
                "✅ Avoid JPEG - lossy compression destroys hidden data",
                "✅ Enable compression for larger messages",
                "✅ Combine with encryption for maximum security",
                "✅ Use large cover files for better capacity"
            ],
            "success"
        )
        
        input(f"\n{Fore.YELLOW}  Press Enter to continue...{Style.RESET_ALL}")
    
    def _show_tips(self):
        """Show tips and best practices"""
        clear_screen()
        MenuFormatter.print_section("💡 TIPS & BEST PRACTICES", "🔐")
        
        MenuFormatter.print_info_box(
            "Security Tips",
            [
                "🔐 Password Security:",
                "  • Use 12+ characters",
                "  • Mix uppercase, lowercase, numbers, symbols",
                "  • Don't reuse passwords",
                "  • Use password generator in Security Tools",
                "",
                "🔑 Key Management:",
                "  • Keep private keys secure and backed up",
                "  • Never share private keys",
                "  • Public keys can be shared freely",
                "",
                "💾 File Security:",
                "  • Verify file hashes after transfer",
                "  • Use secure deletion for sensitive files",
                "  • Keep encrypted backups"
            ],
            "warning"
        )
        
        print(f"\n{Fore.YELLOW}  🎯 Practical Tips:{Style.RESET_ALL}\n")
        print(f"{Fore.GREEN}  ✓{Fore.WHITE} For maximum security: Encrypt first, then hide in image{Style.RESET_ALL}")
        print(f"{Fore.GREEN}  ✓{Fore.WHITE} Test with small files first{Style.RESET_ALL}")
        print(f"{Fore.GREEN}  ✓{Fore.WHITE} Keep track of which algorithm you used{Style.RESET_ALL}")
        print(f"{Fore.GREEN}  ✓{Fore.WHITE} Save encrypted files and keys separately{Style.RESET_ALL}")
        print(f"{Fore.GREEN}  ✓{Fore.WHITE} Use descriptive filenames to remember settings{Style.RESET_ALL}\n")
        
        MenuFormatter.print_info_box(
            "Common Mistakes to Avoid",
            [
                "❌ Using weak passwords",
                "❌ Losing encryption keys or passwords",
                "❌ Using JPEG for steganography",
                "❌ Sharing private RSA keys",
                "❌ Forgetting compression settings",
                "❌ Not backing up important encrypted files"
            ],
            "error"
        )
        
        input(f"\n{Fore.YELLOW}  Press Enter to continue...{Style.RESET_ALL}")
    
    def _show_result(self, title, content, result_type="info"):
        """Show operation result"""
        MenuFormatter.print_info_box(title, [content], result_type)
    
    def _exit_animation(self):
        """Display exit animation"""
        clear_screen()
        print(f"\n\n{Fore.CYAN}  Thank you for using Secure CipherStegno Tool!{Style.RESET_ALL}\n")
        
        Animations.typewriter_effect(
            f"{Fore.YELLOW}  Stay secure, stay encrypted! 🔐{Style.RESET_ALL}",
            delay=0.05
        )
        
        print(f"\n{Fore.GREEN}  Goodbye!{Style.RESET_ALL}\n")
        time.sleep(0.5)


def main():
    """Main entry point"""
    try:
        cli = InteractiveCLI()
        cli.run()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}  Interrupted. Exiting...{Style.RESET_ALL}\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}  Fatal error: {e}{Style.RESET_ALL}\n")
        sys.exit(1)


if __name__ == '__main__':
    main()
