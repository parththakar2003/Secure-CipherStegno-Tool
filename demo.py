#!/usr/bin/env python3
"""
Demo script showcasing new features in Secure CipherStegno Tool v3.2.0
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(__file__))

from colorama import init, Fore, Style
import time

# Initialize colorama
init(autoreset=True)

from src.utils.cli_art import ASCIIArt, Animations, MenuFormatter


def demo_ascii_art():
    """Demonstrate ASCII art"""
    print("\n" + "="*80)
    print(f"{Fore.CYAN}{Style.BRIGHT}DEMO 1: ASCII Art Banner{Style.RESET_ALL}")
    print("="*80)
    
    print(ASCIIArt.MAIN_BANNER)
    time.sleep(2)
    
    print(ASCIIArt.LOCK_EMOJI)
    time.sleep(1)


def demo_animations():
    """Demonstrate animations"""
    print("\n" + "="*80)
    print(f"{Fore.CYAN}{Style.BRIGHT}DEMO 2: Dynamic Animations{Style.RESET_ALL}")
    print("="*80 + "\n")
    
    # Loading spinner
    Animations.loading_spinner(2, "Loading secure modules")
    time.sleep(0.5)
    
    # Progress bar
    print(f"\n{Fore.CYAN}Progress Bar Demo:{Style.RESET_ALL}")
    for i in range(101):
        Animations.progress_bar(i, 100, prefix='Encrypting:', suffix='Complete', length=50)
        time.sleep(0.02)
    time.sleep(0.5)
    
    # Typewriter effect
    print(f"\n{Fore.CYAN}Typewriter Effect Demo:{Style.RESET_ALL}")
    Animations.typewriter_effect(
        f"{Fore.GREEN}Welcome to Secure CipherStegno Tool!{Style.RESET_ALL}",
        delay=0.05
    )
    time.sleep(0.5)
    
    # Pulse text
    print(f"\n{Fore.CYAN}Pulse Effect Demo:{Style.RESET_ALL}")
    Animations.pulse_text("🔐 SECURE 🔐", times=3, color=Fore.YELLOW)
    time.sleep(0.5)
    
    # Encryption animation
    print(f"\n{Fore.CYAN}Encryption Animation:{Style.RESET_ALL}")
    Animations.encrypt_animation("Processing")
    time.sleep(0.5)


def demo_menus():
    """Demonstrate menu formatting"""
    print("\n" + "="*80)
    print(f"{Fore.CYAN}{Style.BRIGHT}DEMO 3: Beautiful Menus{Style.RESET_ALL}")
    print("="*80 + "\n")
    
    MenuFormatter.print_menu(
        "Main Menu",
        [
            "🔐 Cryptography",
            "🖼️  Steganography",
            "🛠️  Security Tools",
            "---",
            "❌ Exit"
        ]
    )
    time.sleep(2)
    
    MenuFormatter.print_section("🔐 CRYPTOGRAPHY SECTION", "🔐")
    time.sleep(1)


def demo_info_boxes():
    """Demonstrate information boxes"""
    print("\n" + "="*80)
    print(f"{Fore.CYAN}{Style.BRIGHT}DEMO 4: Information Boxes{Style.RESET_ALL}")
    print("="*80 + "\n")
    
    MenuFormatter.print_info_box(
        "Information",
        [
            "This is an information box",
            "It can contain multiple lines",
            "Perfect for displaying results!"
        ],
        "info"
    )
    time.sleep(1.5)
    
    MenuFormatter.print_info_box(
        "Success",
        [
            "Operation completed successfully!",
            "Your data has been encrypted."
        ],
        "success"
    )
    time.sleep(1.5)
    
    MenuFormatter.print_info_box(
        "Warning",
        [
            "Please save your encryption key!",
            "Without it, you cannot decrypt your data."
        ],
        "warning"
    )
    time.sleep(1.5)
    
    MenuFormatter.print_info_box(
        "Error",
        [
            "An error occurred during processing",
            "Please check your input and try again"
        ],
        "error"
    )
    time.sleep(1.5)


def demo_key_value_pairs():
    """Demonstrate key-value displays"""
    print("\n" + "="*80)
    print(f"{Fore.CYAN}{Style.BRIGHT}DEMO 5: Key-Value Pairs{Style.RESET_ALL}")
    print("="*80 + "\n")
    
    print(f"{Fore.YELLOW}Encryption Algorithm Analysis:{Style.RESET_ALL}\n")
    
    MenuFormatter.print_key_value("Algorithm", "AES-256", Fore.CYAN, Fore.WHITE)
    MenuFormatter.print_key_value("Strength", "Very Strong", Fore.CYAN, Fore.GREEN)
    MenuFormatter.print_key_value("Key Size", "256 bits", Fore.CYAN, Fore.WHITE)
    MenuFormatter.print_key_value("Security Level", "256-bit", Fore.CYAN, Fore.WHITE)
    MenuFormatter.print_key_value("Recommended", "✓ Yes", Fore.CYAN, Fore.GREEN)
    
    time.sleep(2)


def demo_new_crypto_algorithms():
    """Demonstrate new crypto algorithms"""
    print("\n" + "="*80)
    print(f"{Fore.CYAN}{Style.BRIGHT}DEMO 6: New Crypto Algorithms{Style.RESET_ALL}")
    print("="*80 + "\n")
    
    from src.utils.advanced_security import EncryptionAnalyzer
    
    algorithms = ['aes', 'blowfish', 'chacha20', '3des', 'vigenere']
    
    print(f"{Fore.YELLOW}Comparing Encryption Algorithms:{Style.RESET_ALL}\n")
    print(f"{Fore.CYAN}{'─' * 80}{Style.RESET_ALL}")
    
    for algo in algorithms:
        info = EncryptionAnalyzer.analyze_algorithm(algo)
        rec_symbol = "✓" if info['recommended'] else "✗"
        rec_color = Fore.GREEN if info['recommended'] else Fore.RED
        
        print(f"{Fore.WHITE}{info['name']:<20} {info['strength']:<15} "
              f"Security: {info['security_level']:<10} {rec_color}{rec_symbol}{Style.RESET_ALL}")
    
    print(f"{Fore.CYAN}{'─' * 80}{Style.RESET_ALL}\n")
    time.sleep(2)


def demo_new_security_tools():
    """Demonstrate new security tools"""
    print("\n" + "="*80)
    print(f"{Fore.CYAN}{Style.BRIGHT}DEMO 7: New Security Tools{Style.RESET_ALL}")
    print("="*80 + "\n")
    
    from src.utils.advanced_security import SecureTokenGenerator, DataSanitizer
    
    # Token generation
    print(f"{Fore.YELLOW}🔐 Secure Token Generator:{Style.RESET_ALL}\n")
    
    api_key = SecureTokenGenerator.generate_api_key()
    MenuFormatter.print_key_value("API Key", api_key[:50] + "...", Fore.CYAN, Fore.WHITE)
    
    session = SecureTokenGenerator.generate_session_token()
    MenuFormatter.print_key_value("Session Token", session['token'][:50] + "...", Fore.CYAN, Fore.WHITE)
    
    print(f"\n{Fore.YELLOW}🧹 Data Sanitizer:{Style.RESET_ALL}\n")
    
    unsafe_filename = "../../../etc/passwd"
    safe_filename = DataSanitizer.sanitize_filename(unsafe_filename)
    
    MenuFormatter.print_key_value("Unsafe Filename", unsafe_filename, Fore.RED, Fore.WHITE)
    MenuFormatter.print_key_value("Safe Filename", safe_filename, Fore.GREEN, Fore.WHITE)
    
    time.sleep(2)


def demo_finale():
    """Final demonstration"""
    print("\n" + "="*80)
    print(f"{Fore.CYAN}{Style.BRIGHT}DEMO COMPLETE!{Style.RESET_ALL}")
    print("="*80 + "\n")
    
    print(ASCIIArt.SUCCESS_BANNER)
    
    MenuFormatter.print_info_box(
        "Thank You!",
        [
            "You've seen all the new features in v3.2.0:",
            "",
            "✓ Beautiful ANSI art and animations",
            "✓ New encryption algorithms (Blowfish, 3DES, ChaCha20)",
            "✓ Video steganography support",
            "✓ Advanced security tools",
            "✓ Interactive CLI interface",
            "",
            "Run 'python interactive_cli.py' to try it yourself!"
        ],
        "success"
    )
    
    Animations.typewriter_effect(
        f"\n{Fore.YELLOW}Stay secure, stay encrypted! 🔐{Style.RESET_ALL}",
        delay=0.05
    )
    print()


def main():
    """Run all demonstrations"""
    try:
        # Clear screen
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print(f"\n{Fore.CYAN}{'='*80}")
        print(f"{Fore.YELLOW}{Style.BRIGHT}SECURE CIPHERSTEGNO TOOL v3.2.0 - FEATURE DEMO{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*80}{Style.RESET_ALL}\n")
        
        Animations.typewriter_effect(
            f"{Fore.GREEN}Demonstrating new features and enhancements...{Style.RESET_ALL}",
            delay=0.03
        )
        
        time.sleep(1)
        
        # Run demos
        demo_ascii_art()
        demo_animations()
        demo_menus()
        demo_info_boxes()
        demo_key_value_pairs()
        demo_new_crypto_algorithms()
        demo_new_security_tools()
        demo_finale()
        
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Demo interrupted. Goodbye!{Style.RESET_ALL}\n")
        sys.exit(0)


if __name__ == '__main__':
    main()
