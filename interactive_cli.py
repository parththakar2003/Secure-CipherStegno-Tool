"""
Enhanced Interactive CLI for Secure CipherStegno Tool
Beautiful, user-friendly command-line interface with menus and animations
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
            "RSA (Public Key)"
        ]
        
        MenuFormatter.print_menu("Select Encryption Algorithm", algorithms, show_header=False)
        algo_choice = InputHelper.get_choice("Algorithm", range(1, len(algorithms) + 1))
        
        if algo_choice is None:
            return
        
        # Get message
        print(f"\n{Fore.CYAN}{'─' * 70}{Style.RESET_ALL}")
        message = InputHelper.get_input("Enter message to encrypt")
        
        if not message:
            print(f"{Fore.RED}  ✗ No message provided{Style.RESET_ALL}")
            input(f"{Fore.YELLOW}  Press Enter to continue...{Style.RESET_ALL}")
            return
        
        # Encrypt based on algorithm
        Animations.encrypt_animation("Encrypting")
        
        try:
            result = None
            
            if algo_choice == 0:  # Caesar
                shift = int(InputHelper.get_input("Enter shift value", "3"))
                result = CaesarCipher.encrypt(message, shift)
                self._show_result("Encrypted Text", result, "success")
            
            elif algo_choice == 1:  # Vigenere
                key = InputHelper.get_input("Enter encryption key")
                result = VigenereCipher.encrypt(message, key)
                self._show_result("Encrypted Text", result, "success")
            
            elif algo_choice == 2:  # Playfair
                key = InputHelper.get_input("Enter encryption key")
                result = PlayfairCipher.encrypt(message, key)
                self._show_result("Encrypted Text", result, "success")
            
            elif algo_choice == 3:  # Rail Fence
                rails = int(InputHelper.get_input("Enter number of rails", "3"))
                result = RailFenceCipher.encrypt(message, rails)
                self._show_result("Encrypted Text", result, "success")
            
            elif algo_choice == 5:  # AES
                password = InputHelper.get_input("Enter password")
                result = AESCipher.encrypt_with_password(message, password)
                MenuFormatter.print_info_box(
                    "Encryption Successful",
                    [
                        f"Ciphertext: {result['ciphertext'][:60]}...",
                        f"IV: {result['iv']}",
                        "",
                        "⚠️  Save both ciphertext and IV for decryption!"
                    ],
                    "success"
                )
            
            elif algo_choice == 6:  # Blowfish
                password = InputHelper.get_input("Enter password")
                result = BlowfishCipher.encrypt_with_password(message, password)
                MenuFormatter.print_info_box(
                    "Encryption Successful",
                    [
                        f"Ciphertext: {result['ciphertext'][:60]}...",
                        f"IV: {result['iv']}",
                        "",
                        "⚠️  Save both ciphertext and IV for decryption!"
                    ],
                    "success"
                )
            
            elif algo_choice == 7:  # 3DES
                password = InputHelper.get_input("Enter password")
                result = DES3Cipher.encrypt_with_password(message, password)
                MenuFormatter.print_info_box(
                    "Encryption Successful",
                    [
                        f"Ciphertext: {result['ciphertext'][:60]}...",
                        f"IV: {result['iv']}",
                        "",
                        "⚠️  3DES is legacy. Consider using AES instead."
                    ],
                    "warning"
                )
            
            elif algo_choice == 8:  # ChaCha20
                password = InputHelper.get_input("Enter password")
                result = ChaCha20Cipher.encrypt_with_password(message, password)
                MenuFormatter.print_info_box(
                    "Encryption Successful",
                    [
                        f"Ciphertext: {result['ciphertext'][:60]}...",
                        f"Nonce: {result['nonce']}",
                        "",
                        "✓ ChaCha20 is fast and secure!"
                    ],
                    "success"
                )
            
            elif algo_choice == 10:  # RSA
                print(f"\n{Fore.YELLOW}  RSA requires a public key. Generating new key pair...{Style.RESET_ALL}")
                cipher = RSACipher(2048)
                keys = cipher.generate_key_pair()
                result = cipher.encrypt(message)
                
                MenuFormatter.print_info_box(
                    "RSA Encryption Complete",
                    [
                        f"Encrypted: {result[:60]}...",
                        "",
                        "Keys have been generated.",
                        "Save the private key securely for decryption!"
                    ],
                    "success"
                )
        
        except Exception as e:
            MenuFormatter.print_info_box("Encryption Failed", [str(e)], "error")
        
        input(f"\n{Fore.YELLOW}  Press Enter to continue...{Style.RESET_ALL}")
    
    def _decrypt_menu(self):
        """Decryption menu"""
        clear_screen()
        MenuFormatter.print_section("🔓 DECRYPTION", "🔐")
        
        # Similar structure to encryption
        print(f"{Fore.CYAN}  Decryption feature - Implementation similar to encryption{Style.RESET_ALL}")
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
        
        if choice in [0, 1]:  # Image stego
            MenuFormatter.print_section("🖼️  IMAGE STEGANOGRAPHY", "🖼️")
            print(f"{Fore.CYAN}  Image steganography operations{Style.RESET_ALL}")
        elif choice in [2, 3]:  # Audio stego
            MenuFormatter.print_section("🎵 AUDIO STEGANOGRAPHY", "🎵")
            print(f"{Fore.CYAN}  Audio steganography operations{Style.RESET_ALL}")
        elif choice in [4, 5]:  # Video stego
            MenuFormatter.print_section("🎬 VIDEO STEGANOGRAPHY", "🎬")
            MenuFormatter.print_info_box(
                "Video Steganography",
                [
                    "Video steganography allows hiding messages in video files.",
                    "Requires ffmpeg to be installed on your system.",
                    "",
                    "Supported formats: MP4, AVI",
                    "Uses LSB technique on video frames."
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
        clear_screen()
        MenuFormatter.print_section("ℹ️  HELP & INFORMATION", "ℹ️")
        
        MenuFormatter.print_info_box(
            "About Secure CipherStegno Tool",
            [
                "Version: 3.2.0",
                "Platform: Cross-platform (Windows, Linux, macOS)",
                "",
                "A comprehensive security toolkit featuring:",
                "  • Multiple encryption algorithms",
                "  • Steganography (Image, Audio, Video)",
                "  • Security analysis tools",
                "  • Password generation and validation",
                "",
                "© 2025 Parth Thakar | MIT License"
            ],
            "info"
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
