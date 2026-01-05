"""
CLI Art and Animations
Beautiful ANSI art and dynamic animations for the CLI interface
"""

import time
import sys
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)


class ASCIIArt:
    """Collection of ASCII art banners and designs"""
    
    MAIN_BANNER = f"""
{Fore.CYAN}╔═══════════════════════════════════════════════════════════════════════════╗
{Fore.CYAN}║  {Fore.GREEN}███████{Fore.CYAN}╗{Fore.GREEN}███████{Fore.CYAN}╗ {Fore.GREEN}██████{Fore.CYAN}╗{Fore.GREEN}██{Fore.CYAN}╗   {Fore.GREEN}██{Fore.CYAN}╗{Fore.GREEN}██████{Fore.CYAN}╗ {Fore.GREEN}███████{Fore.CYAN}╗     {Fore.YELLOW}🔐{Fore.CYAN}              ║
{Fore.CYAN}║  {Fore.GREEN}██{Fore.CYAN}╔════╝{Fore.GREEN}██{Fore.CYAN}╔════╝{Fore.GREEN}██{Fore.CYAN}╔════╝{Fore.GREEN}██{Fore.CYAN}║   {Fore.GREEN}██{Fore.CYAN}║{Fore.GREEN}██{Fore.CYAN}╔══{Fore.GREEN}██{Fore.CYAN}╗{Fore.GREEN}██{Fore.CYAN}╔════╝                    ║
{Fore.CYAN}║  {Fore.GREEN}███████{Fore.CYAN}╗{Fore.GREEN}█████{Fore.CYAN}╗  {Fore.GREEN}██{Fore.CYAN}║     {Fore.GREEN}██{Fore.CYAN}║   {Fore.GREEN}██{Fore.CYAN}║{Fore.GREEN}██████{Fore.CYAN}╔╝{Fore.GREEN}█████{Fore.CYAN}╗                      ║
{Fore.CYAN}║  ╚════{Fore.GREEN}██{Fore.CYAN}║{Fore.GREEN}██{Fore.CYAN}╔══╝  {Fore.GREEN}██{Fore.CYAN}║     {Fore.GREEN}██{Fore.CYAN}║   {Fore.GREEN}██{Fore.CYAN}║{Fore.GREEN}██{Fore.CYAN}╔══{Fore.GREEN}██{Fore.CYAN}╗{Fore.GREEN}██{Fore.CYAN}╔══╝                      ║
{Fore.CYAN}║  {Fore.GREEN}███████{Fore.CYAN}║{Fore.GREEN}███████{Fore.CYAN}╗╚{Fore.GREEN}██████{Fore.CYAN}╗╚{Fore.GREEN}██████{Fore.CYAN}╔╝{Fore.GREEN}██{Fore.CYAN}║  {Fore.GREEN}██{Fore.CYAN}║{Fore.GREEN}███████{Fore.CYAN}╗                    ║
{Fore.CYAN}║  ╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝                    ║
{Fore.CYAN}║                                                                           ║
{Fore.CYAN}║  {Fore.MAGENTA}█████{Fore.CYAN}╗ {Fore.MAGENTA}██{Fore.CYAN}╗{Fore.MAGENTA}██████{Fore.CYAN}╗ {Fore.MAGENTA}██{Fore.CYAN}╗  {Fore.MAGENTA}██{Fore.CYAN}╗{Fore.MAGENTA}███████{Fore.CYAN}╗{Fore.MAGENTA}██████{Fore.CYAN}╗     {Fore.MAGENTA}███████{Fore.CYAN}╗{Fore.MAGENTA}████████{Fore.CYAN}╗  ║
{Fore.CYAN}║ {Fore.MAGENTA}██{Fore.CYAN}╔══{Fore.MAGENTA}██{Fore.CYAN}╗{Fore.MAGENTA}██{Fore.CYAN}║{Fore.MAGENTA}██{Fore.CYAN}╔══{Fore.MAGENTA}██{Fore.CYAN}╗{Fore.MAGENTA}██{Fore.CYAN}║  {Fore.MAGENTA}██{Fore.CYAN}║{Fore.MAGENTA}██{Fore.CYAN}╔════╝{Fore.MAGENTA}██{Fore.CYAN}╔══{Fore.MAGENTA}██{Fore.CYAN}╗    {Fore.MAGENTA}██{Fore.CYAN}╔════╝╚══{Fore.MAGENTA}██{Fore.CYAN}╔══╝  ║
{Fore.CYAN}║ {Fore.MAGENTA}██{Fore.CYAN}║  {Fore.MAGENTA}╚═╝██{Fore.CYAN}║{Fore.MAGENTA}██████{Fore.CYAN}╔╝{Fore.MAGENTA}███████{Fore.CYAN}║{Fore.MAGENTA}█████{Fore.CYAN}╗  {Fore.MAGENTA}██████{Fore.CYAN}╔╝    {Fore.MAGENTA}███████{Fore.CYAN}╗   {Fore.MAGENTA}██{Fore.CYAN}║     ║
{Fore.CYAN}║ {Fore.MAGENTA}██{Fore.CYAN}║  {Fore.MAGENTA}██{Fore.CYAN}╗{Fore.MAGENTA}██{Fore.CYAN}║{Fore.MAGENTA}██{Fore.CYAN}╔═══╝ {Fore.MAGENTA}██{Fore.CYAN}╔══{Fore.MAGENTA}██{Fore.CYAN}║{Fore.MAGENTA}██{Fore.CYAN}╔══╝  {Fore.MAGENTA}██{Fore.CYAN}╔══{Fore.MAGENTA}██{Fore.CYAN}╗    ╚════{Fore.MAGENTA}██{Fore.CYAN}║   {Fore.MAGENTA}██{Fore.CYAN}║     ║
{Fore.CYAN}║ ╚{Fore.MAGENTA}█████{Fore.CYAN}╔╝{Fore.MAGENTA}██{Fore.CYAN}║{Fore.MAGENTA}██{Fore.CYAN}║     {Fore.MAGENTA}██{Fore.CYAN}║  {Fore.MAGENTA}██{Fore.CYAN}║{Fore.MAGENTA}███████{Fore.CYAN}╗{Fore.MAGENTA}██{Fore.CYAN}║  {Fore.MAGENTA}██{Fore.CYAN}║    {Fore.MAGENTA}███████{Fore.CYAN}║   {Fore.MAGENTA}██{Fore.CYAN}║     ║
{Fore.CYAN}║  ╚════╝ ╚═╝╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝    ╚══════╝   ╚═╝     ║
{Fore.CYAN}╚═══════════════════════════════════════════════════════════════════════════╝
{Fore.WHITE}         {Fore.YELLOW}Professional Security Toolkit{Fore.WHITE} | {Fore.GREEN}Version 3.2.0{Fore.WHITE} | {Fore.BLUE}© 2025
{Style.RESET_ALL}"""

    LOCK_EMOJI = f"""
{Fore.YELLOW}       ▄▄▄▄▄▄▄
{Fore.YELLOW}     ▄█{Fore.WHITE}░░░░░{Fore.YELLOW}█▄
{Fore.YELLOW}    █{Fore.WHITE}░░░░░░░{Fore.YELLOW}█
{Fore.YELLOW}    █{Fore.WHITE}░░░░░░░{Fore.YELLOW}█
{Fore.YELLOW}   ▐{Fore.CYAN}███████████{Fore.YELLOW}▌
{Fore.CYAN}   ███{Fore.WHITE}░{Fore.RED}◉{Fore.WHITE}░░{Fore.RED}◉{Fore.WHITE}░{Fore.CYAN}███
{Fore.CYAN}   ███{Fore.WHITE}░░░░░░░{Fore.CYAN}███
{Fore.CYAN}   ███{Fore.WHITE}░░{Fore.YELLOW}▀▀▀{Fore.WHITE}░░{Fore.CYAN}███
{Fore.CYAN}   ▐█████████████▌
{Fore.CYAN}    ▀███████████▀
{Style.RESET_ALL}"""

    SUCCESS_BANNER = f"""
{Fore.GREEN}    ✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓
{Fore.GREEN}    ✓  {Fore.WHITE}OPERATION SUCCESS{Fore.GREEN}  ✓
{Fore.GREEN}    ✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓✓
{Style.RESET_ALL}"""

    ERROR_BANNER = f"""
{Fore.RED}    ✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗
{Fore.RED}    ✗  {Fore.WHITE}OPERATION FAILED{Fore.RED}  ✗
{Fore.RED}    ✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗✗
{Style.RESET_ALL}"""

    CRYPTO_ICON = f"""
{Fore.CYAN}    ╔════════════╗
{Fore.CYAN}    ║ {Fore.YELLOW}🔐 CRYPTO{Fore.CYAN} ║
{Fore.CYAN}    ╚════════════╝
{Style.RESET_ALL}"""

    STEGO_ICON = f"""
{Fore.MAGENTA}    ╔════════════╗
{Fore.MAGENTA}    ║ {Fore.YELLOW}🖼️  STEGO{Fore.MAGENTA}  ║
{Fore.MAGENTA}    ╚════════════╝
{Style.RESET_ALL}"""

    TOOLS_ICON = f"""
{Fore.GREEN}    ╔════════════╗
{Fore.GREEN}    ║ {Fore.YELLOW}🛠️  TOOLS{Fore.GREEN}  ║
{Fore.GREEN}    ╚════════════╝
{Style.RESET_ALL}"""


class Animations:
    """Dynamic CLI animations"""
    
    @staticmethod
    def loading_spinner(duration=2, message="Loading"):
        """
        Display a loading spinner
        
        Args:
            duration (float): Duration in seconds
            message (str): Loading message
        """
        spinners = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        end_time = time.time() + duration
        i = 0
        
        while time.time() < end_time:
            sys.stdout.write(f'\r{Fore.CYAN}{spinners[i % len(spinners)]} {Fore.WHITE}{message}...')
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1
        
        sys.stdout.write(f'\r{Fore.GREEN}✓ {Fore.WHITE}{message} complete!        \n')
        sys.stdout.flush()
    
    @staticmethod
    def progress_bar(current, total, prefix='', suffix='', length=50):
        """
        Display a progress bar
        
        Args:
            current (int): Current progress
            total (int): Total items
            prefix (str): Prefix string
            suffix (str): Suffix string
            length (int): Bar length
        """
        filled = int(length * current // total)
        bar = '█' * filled + '░' * (length - filled)
        percent = 100 * (current / float(total))
        
        sys.stdout.write(f'\r{prefix} {Fore.CYAN}|{Fore.GREEN}{bar}{Fore.CYAN}| {Fore.YELLOW}{percent:.1f}%{Fore.WHITE} {suffix}')
        sys.stdout.flush()
        
        if current == total:
            print()
    
    @staticmethod
    def typewriter_effect(text, delay=0.03):
        """
        Display text with typewriter effect
        
        Args:
            text (str): Text to display
            delay (float): Delay between characters
        """
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()
    
    @staticmethod
    def pulse_text(text, times=3, color=Fore.CYAN):
        """
        Display pulsing text
        
        Args:
            text (str): Text to pulse
            times (int): Number of pulses
            color: Text color
        """
        for _ in range(times):
            sys.stdout.write(f'\r{color}{Style.BRIGHT}{text}{Style.RESET_ALL}')
            sys.stdout.flush()
            time.sleep(0.3)
            sys.stdout.write(f'\r{color}{Style.DIM}{text}{Style.RESET_ALL}')
            sys.stdout.flush()
            time.sleep(0.3)
        print()
    
    @staticmethod
    def matrix_effect(lines=10):
        """
        Display Matrix-style falling characters
        
        Args:
            lines (int): Number of lines to display
        """
        import random
        import string
        
        chars = string.ascii_letters + string.digits + '!@#$%^&*()_+-=[]{}|;:,.<>?'
        
        for _ in range(lines):
            line = ''.join(random.choice(chars) for _ in range(80))
            print(f'{Fore.GREEN}{line}{Style.RESET_ALL}')
            time.sleep(0.05)
    
    @staticmethod
    def encrypt_animation(text="Encrypting"):
        """Animated encryption effect"""
        import random
        
        frames = [
            f"{Fore.YELLOW}[░░░░░░░░░░]",
            f"{Fore.YELLOW}[█░░░░░░░░░]",
            f"{Fore.YELLOW}[██░░░░░░░░]",
            f"{Fore.YELLOW}[███░░░░░░░]",
            f"{Fore.YELLOW}[████░░░░░░]",
            f"{Fore.YELLOW}[█████░░░░░]",
            f"{Fore.YELLOW}[██████░░░░]",
            f"{Fore.YELLOW}[███████░░░]",
            f"{Fore.YELLOW}[████████░░]",
            f"{Fore.YELLOW}[█████████░]",
            f"{Fore.GREEN}[██████████]"
        ]
        
        for frame in frames:
            sys.stdout.write(f'\r{Fore.CYAN}🔐 {text} {frame}')
            sys.stdout.flush()
            time.sleep(0.1)
        
        print(f' {Fore.GREEN}✓ Done!{Style.RESET_ALL}')


class MenuFormatter:
    """Format interactive menus"""
    
    @staticmethod
    def print_menu(title, options, show_header=True):
        """
        Print a formatted menu
        
        Args:
            title (str): Menu title
            options (list): List of menu options
            show_header (bool): Show decorative header
        """
        if show_header:
            print(f"\n{Fore.CYAN}{'═' * 70}{Style.RESET_ALL}")
        
        print(f"{Fore.YELLOW}{Style.BRIGHT}  {title}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'═' * 70}{Style.RESET_ALL}\n")
        
        for i, option in enumerate(options, 1):
            if option == '---':
                print(f"{Fore.CYAN}  {'─' * 66}{Style.RESET_ALL}")
            else:
                print(f"{Fore.GREEN}  [{i}]{Fore.WHITE} {option}{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}{'═' * 70}{Style.RESET_ALL}")
    
    @staticmethod
    def print_section(title, icon=""):
        """
        Print a section header
        
        Args:
            title (str): Section title
            icon (str): Optional icon
        """
        print(f"\n{Fore.CYAN}╔{'═' * 68}╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║{Fore.YELLOW}{Style.BRIGHT} {icon} {title:63}{Fore.CYAN} ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚{'═' * 68}╝{Style.RESET_ALL}\n")
    
    @staticmethod
    def print_info_box(title, content, box_type="info"):
        """
        Print an information box
        
        Args:
            title (str): Box title
            content (list or str): Content lines
            box_type (str): Type of box (info, success, error, warning)
        """
        colors = {
            'info': Fore.CYAN,
            'success': Fore.GREEN,
            'error': Fore.RED,
            'warning': Fore.YELLOW
        }
        
        icons = {
            'info': 'ℹ',
            'success': '✓',
            'error': '✗',
            'warning': '⚠'
        }
        
        color = colors.get(box_type, Fore.CYAN)
        icon = icons.get(box_type, 'ℹ')
        
        if isinstance(content, str):
            content = [content]
        
        max_len = max(len(line) for line in content + [title]) + 4
        
        print(f"\n{color}╔{'═' * max_len}╗{Style.RESET_ALL}")
        print(f"{color}║ {icon} {Fore.WHITE}{Style.BRIGHT}{title}{' ' * (max_len - len(title) - 3)}{color}║{Style.RESET_ALL}")
        print(f"{color}╠{'═' * max_len}╣{Style.RESET_ALL}")
        
        for line in content:
            print(f"{color}║ {Fore.WHITE}{line}{' ' * (max_len - len(line) - 1)}{color}║{Style.RESET_ALL}")
        
        print(f"{color}╚{'═' * max_len}╝{Style.RESET_ALL}\n")
    
    @staticmethod
    def print_key_value(key, value, key_color=Fore.CYAN, value_color=Fore.WHITE):
        """
        Print key-value pair
        
        Args:
            key (str): Key name
            value: Value to display
            key_color: Color for key
            value_color: Color for value
        """
        print(f"{key_color}  {key:25}{value_color} : {value}{Style.RESET_ALL}")


class InputHelper:
    """Enhanced input helpers"""
    
    @staticmethod
    def get_input(prompt, default=None, color=Fore.YELLOW):
        """
        Get user input with colored prompt
        
        Args:
            prompt (str): Input prompt
            default: Default value
            color: Prompt color
            
        Returns:
            str: User input
        """
        default_text = f" [{default}]" if default else ""
        user_input = input(f"{color}  {prompt}{default_text}: {Fore.WHITE}")
        
        if not user_input and default is not None:
            return default
        
        return user_input
    
    @staticmethod
    def get_choice(prompt, options, color=Fore.YELLOW):
        """
        Get user choice from options
        
        Args:
            prompt (str): Choice prompt
            options (list): List of options
            color: Prompt color
            
        Returns:
            int: Selected option index (0-based)
        """
        while True:
            try:
                choice = input(f"{color}  {prompt} (1-{len(options)}): {Fore.WHITE}")
                choice_num = int(choice)
                
                if 1 <= choice_num <= len(options):
                    return choice_num - 1
                else:
                    print(f"{Fore.RED}  Invalid choice. Please enter a number between 1 and {len(options)}.{Style.RESET_ALL}")
            
            except ValueError:
                print(f"{Fore.RED}  Invalid input. Please enter a number.{Style.RESET_ALL}")
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}  Operation cancelled.{Style.RESET_ALL}")
                return None
    
    @staticmethod
    def confirm(prompt, default=False):
        """
        Get yes/no confirmation
        
        Args:
            prompt (str): Confirmation prompt
            default (bool): Default value
            
        Returns:
            bool: User's choice
        """
        default_text = "[Y/n]" if default else "[y/N]"
        response = input(f"{Fore.YELLOW}  {prompt} {default_text}: {Fore.WHITE}").lower()
        
        if not response:
            return default
        
        return response in ['y', 'yes']


def clear_screen():
    """Clear terminal screen"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header():
    """Print application header"""
    clear_screen()
    print(ASCIIArt.MAIN_BANNER)
    time.sleep(0.5)
