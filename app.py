"""
Enhanced GUI Application for Secure CipherStegno Tool
Integrates all advanced features with improved UI
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(__file__))

from src.crypto import CaesarCipher, AESCipher, RSACipher
from src.steganography import ImageSteganography, AudioSteganography
from src.utils import PasswordValidator, calculate_file_hash, Logger


class ModernButton(tk.Button):
    """Styled modern button"""
    
    def __init__(self, parent, **kwargs):
        defaults = {
            'font': ('Arial', 12),
            'height': 2,
            'width': 20,
            'bg': '#2196F3',
            'fg': 'white',
            'activebackground': '#1976D2',
            'cursor': 'hand2',
            'relief': tk.FLAT
        }
        defaults.update(kwargs)
        super().__init__(parent, **defaults)


class SecureCipherStegnoApp:
    """Main application class"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Secure CipherStegno Tool - Professional Edition")
        self.root.geometry("800x600")
        self.root.configure(bg="#f5f5f5")
        
        self.logger = Logger()
        
        self._create_main_interface()
    
    def _create_main_interface(self):
        """Create main application interface"""
        # Header
        header_frame = tk.Frame(self.root, bg="#1976D2", height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(
            header_frame,
            text="🔐 Secure CipherStegno Tool",
            font=("Arial", 24, "bold"),
            bg="#1976D2",
            fg="white"
        ).pack(pady=20)
        
        # Main content
        main_frame = tk.Frame(self.root, bg="#f5f5f5")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Add tabs
        self._create_cryptography_tab()
        self._create_steganography_tab()
        self._create_tools_tab()
        
        # Footer
        footer_frame = tk.Frame(self.root, bg="#f5f5f5")
        footer_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(
            footer_frame,
            text="© 2025 PARTH THAKAR | Professional Security Tool",
            font=("Arial", 10),
            bg="#f5f5f5",
            fg="#666"
        ).pack()
    
    def _create_cryptography_tab(self):
        """Create cryptography tab"""
        tab = tk.Frame(self.notebook, bg="white")
        self.notebook.add(tab, text="🔐 Cryptography")
        
        # Algorithm selection
        algo_frame = tk.LabelFrame(tab, text="Select Algorithm", font=("Arial", 12, "bold"),
                                   bg="white", padx=20, pady=20)
        algo_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.crypto_algo = tk.StringVar(value="aes")
        
        tk.Radiobutton(algo_frame, text="Caesar Cipher (Simple)", variable=self.crypto_algo,
                      value="caesar", font=("Arial", 11), bg="white").pack(anchor=tk.W)
        tk.Radiobutton(algo_frame, text="AES-256 (Recommended)", variable=self.crypto_algo,
                      value="aes", font=("Arial", 11), bg="white").pack(anchor=tk.W)
        tk.Radiobutton(algo_frame, text="RSA (Public Key)", variable=self.crypto_algo,
                      value="rsa", font=("Arial", 11), bg="white").pack(anchor=tk.W)
        
        # Action buttons
        button_frame = tk.Frame(tab, bg="white")
        button_frame.pack(pady=20)
        
        ModernButton(button_frame, text="🔒 Encrypt", bg="#4CAF50",
                    command=self._handle_encryption).pack(side=tk.LEFT, padx=10)
        ModernButton(button_frame, text="🔓 Decrypt", bg="#FF9800",
                    command=self._handle_decryption).pack(side=tk.LEFT, padx=10)
        ModernButton(button_frame, text="🔑 Generate Keys", bg="#9C27B0",
                    command=self._handle_key_generation).pack(side=tk.LEFT, padx=10)
    
    def _create_steganography_tab(self):
        """Create steganography tab"""
        tab = tk.Frame(self.notebook, bg="white")
        self.notebook.add(tab, text="🖼️ Steganography")
        
        # Type selection
        type_frame = tk.LabelFrame(tab, text="Select Type", font=("Arial", 12, "bold"),
                                   bg="white", padx=20, pady=20)
        type_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.stego_type = tk.StringVar(value="image")
        
        tk.Radiobutton(type_frame, text="📷 Image Steganography (PNG, BMP)",
                      variable=self.stego_type, value="image",
                      font=("Arial", 11), bg="white").pack(anchor=tk.W)
        tk.Radiobutton(type_frame, text="🎵 Audio Steganography (WAV)",
                      variable=self.stego_type, value="audio",
                      font=("Arial", 11), bg="white").pack(anchor=tk.W)
        
        # Options
        options_frame = tk.Frame(tab, bg="white")
        options_frame.pack(pady=10)
        
        self.compress_var = tk.BooleanVar(value=True)
        tk.Checkbutton(options_frame, text="Compress message before hiding",
                      variable=self.compress_var, font=("Arial", 10),
                      bg="white").pack()
        
        # Action buttons
        button_frame = tk.Frame(tab, bg="white")
        button_frame.pack(pady=20)
        
        ModernButton(button_frame, text="📥 Hide Message", bg="#2196F3",
                    command=self._handle_stego_encode).pack(side=tk.LEFT, padx=10)
        ModernButton(button_frame, text="📤 Extract Message", bg="#009688",
                    command=self._handle_stego_decode).pack(side=tk.LEFT, padx=10)
        ModernButton(button_frame, text="ℹ️ Check Capacity", bg="#607D8B",
                    command=self._handle_check_capacity).pack(side=tk.LEFT, padx=10)
    
    def _create_tools_tab(self):
        """Create tools tab"""
        tab = tk.Frame(self.notebook, bg="white")
        self.notebook.add(tab, text="🛠️ Security Tools")
        
        # Tools grid
        tools_frame = tk.Frame(tab, bg="white")
        tools_frame.pack(expand=True)
        
        # Row 1
        ModernButton(tools_frame, text="🔐 Password Generator", bg="#4CAF50",
                    command=self._handle_password_generator).grid(row=0, column=0, padx=10, pady=10)
        ModernButton(tools_frame, text="✅ Password Validator", bg="#2196F3",
                    command=self._handle_password_validator).grid(row=0, column=1, padx=10, pady=10)
        
        # Row 2
        ModernButton(tools_frame, text="#️⃣ File Hash Calculator", bg="#FF9800",
                    command=self._handle_file_hash).grid(row=1, column=0, padx=10, pady=10)
        ModernButton(tools_frame, text="🔍 Verify File Integrity", bg="#9C27B0",
                    command=self._handle_verify_integrity).grid(row=1, column=1, padx=10, pady=10)
        
        # Row 3
        ModernButton(tools_frame, text="📖 View Documentation", bg="#607D8B",
                    command=self._handle_show_docs).grid(row=2, column=0, padx=10, pady=10)
        ModernButton(tools_frame, text="ℹ️ About", bg="#009688",
                    command=self._handle_about).grid(row=2, column=1, padx=10, pady=10)
    
    def _handle_encryption(self):
        """Handle encryption"""
        algo = self.crypto_algo.get()
        
        # Create encryption window
        window = tk.Toplevel(self.root)
        window.title(f"Encrypt with {algo.upper()}")
        window.geometry("600x500")
        window.configure(bg="white")
        
        # Input text
        tk.Label(window, text="Enter text to encrypt:", font=("Arial", 12, "bold"),
                bg="white").pack(pady=10)
        input_text = scrolledtext.ScrolledText(window, height=8, font=("Arial", 11))
        input_text.pack(padx=20, pady=5, fill=tk.BOTH, expand=True)
        
        # Password/Key input
        if algo in ['aes', 'caesar']:
            tk.Label(window, text="Password/Shift:", font=("Arial", 11),
                    bg="white").pack(pady=5)
            password_entry = tk.Entry(window, font=("Arial", 11), show="*" if algo == 'aes' else "")
            password_entry.pack(pady=5)
        
        # Output text
        tk.Label(window, text="Encrypted output:", font=("Arial", 12, "bold"),
                bg="white").pack(pady=10)
        output_text = scrolledtext.ScrolledText(window, height=8, font=("Arial", 11))
        output_text.pack(padx=20, pady=5, fill=tk.BOTH, expand=True)
        
        def encrypt():
            text = input_text.get("1.0", tk.END).strip()
            if not text:
                messagebox.showwarning("Input Error", "Please enter text to encrypt")
                return
            
            try:
                if algo == 'caesar':
                    shift = int(password_entry.get() or 3)
                    result = CaesarCipher.encrypt(text, shift)
                    output_text.delete("1.0", tk.END)
                    output_text.insert("1.0", result)
                
                elif algo == 'aes':
                    password = password_entry.get()
                    if not password:
                        messagebox.showwarning("Input Error", "Please enter password")
                        return
                    
                    result = AESCipher.encrypt_with_password(text, password)
                    output_text.delete("1.0", tk.END)
                    output_text.insert("1.0", f"Ciphertext: {result['ciphertext']}\n\n")
                    output_text.insert(tk.END, f"IV: {result['iv']}")
                    
                    messagebox.showinfo("Success", "Text encrypted successfully! Save both ciphertext and IV.")
                
                elif algo == 'rsa':
                    key_file = filedialog.askopenfilename(title="Select Public Key",
                                                         filetypes=[("PEM files", "*.pem")])
                    if not key_file:
                        return
                    
                    with open(key_file, 'r') as f:
                        public_key = f.read()
                    
                    cipher = RSACipher()
                    cipher.load_public_key(public_key)
                    result = cipher.encrypt(text)
                    
                    output_text.delete("1.0", tk.END)
                    output_text.insert("1.0", result)
                    messagebox.showinfo("Success", "Text encrypted with RSA!")
                
                self.logger.success(f"Text encrypted successfully with {algo.upper()}")
            
            except Exception as e:
                messagebox.showerror("Error", str(e))
                self.logger.error(f"Encryption failed: {str(e)}")
        
        ModernButton(window, text="🔒 Encrypt", bg="#4CAF50",
                    command=encrypt).pack(pady=15)
    
    def _handle_decryption(self):
        """Handle decryption"""
        algo = self.crypto_algo.get()
        
        # Create decryption window
        window = tk.Toplevel(self.root)
        window.title(f"Decrypt with {algo.upper()}")
        window.geometry("600x500")
        window.configure(bg="white")
        
        # Input ciphertext
        tk.Label(window, text="Enter encrypted text:", font=("Arial", 12, "bold"),
                bg="white").pack(pady=10)
        input_text = scrolledtext.ScrolledText(window, height=8, font=("Arial", 11))
        input_text.pack(padx=20, pady=5, fill=tk.BOTH, expand=True)
        
        # Additional fields for AES
        iv_entry = None
        if algo == 'aes':
            tk.Label(window, text="IV (Initialization Vector):", font=("Arial", 11),
                    bg="white").pack(pady=5)
            iv_entry = tk.Entry(window, font=("Arial", 11), width=50)
            iv_entry.pack(pady=5)
        
        # Password/Key input
        if algo in ['aes', 'caesar']:
            tk.Label(window, text="Password/Shift:", font=("Arial", 11),
                    bg="white").pack(pady=5)
            password_entry = tk.Entry(window, font=("Arial", 11), show="*" if algo == 'aes' else "")
            password_entry.pack(pady=5)
        
        # Output text
        tk.Label(window, text="Decrypted output:", font=("Arial", 12, "bold"),
                bg="white").pack(pady=10)
        output_text = scrolledtext.ScrolledText(window, height=8, font=("Arial", 11))
        output_text.pack(padx=20, pady=5, fill=tk.BOTH, expand=True)
        
        def decrypt():
            text = input_text.get("1.0", tk.END).strip()
            if not text:
                messagebox.showwarning("Input Error", "Please enter encrypted text")
                return
            
            try:
                if algo == 'caesar':
                    shift = int(password_entry.get() or 3)
                    result = CaesarCipher.decrypt(text, shift)
                    output_text.delete("1.0", tk.END)
                    output_text.insert("1.0", result)
                
                elif algo == 'aes':
                    password = password_entry.get()
                    iv = iv_entry.get().strip()
                    
                    if not password or not iv:
                        messagebox.showwarning("Input Error", "Please enter password and IV")
                        return
                    
                    result = AESCipher.decrypt_with_password(text, iv, password)
                    output_text.delete("1.0", tk.END)
                    output_text.insert("1.0", result)
                    messagebox.showinfo("Success", "Text decrypted successfully!")
                
                elif algo == 'rsa':
                    key_file = filedialog.askopenfilename(title="Select Private Key",
                                                         filetypes=[("PEM files", "*.pem")])
                    if not key_file:
                        return
                    
                    with open(key_file, 'r') as f:
                        private_key = f.read()
                    
                    cipher = RSACipher()
                    cipher.load_private_key(private_key)
                    result = cipher.decrypt(text)
                    
                    output_text.delete("1.0", tk.END)
                    output_text.insert("1.0", result)
                    messagebox.showinfo("Success", "Text decrypted with RSA!")
                
                self.logger.success(f"Text decrypted successfully with {algo.upper()}")
            
            except Exception as e:
                messagebox.showerror("Error", str(e))
                self.logger.error(f"Decryption failed: {str(e)}")
        
        ModernButton(window, text="🔓 Decrypt", bg="#FF9800",
                    command=decrypt).pack(pady=15)
    
    def _handle_key_generation(self):
        """Handle key generation"""
        algo = self.crypto_algo.get()
        
        if algo == 'caesar':
            messagebox.showinfo("Info", "Caesar cipher doesn't require key generation. Just use a shift value (1-25).")
            return
        
        output_dir = filedialog.askdirectory(title="Select directory to save keys")
        if not output_dir:
            return
        
        try:
            if algo == 'rsa':
                cipher = RSACipher(key_size=2048)
                keys = cipher.generate_key_pair()
                
                public_key_path = os.path.join(output_dir, 'public_key.pem')
                private_key_path = os.path.join(output_dir, 'private_key.pem')
                
                with open(public_key_path, 'w') as f:
                    f.write(keys['public_key'])
                with open(private_key_path, 'w') as f:
                    f.write(keys['private_key'])
                
                messagebox.showinfo("Success",
                                  f"RSA key pair generated!\n\n"
                                  f"Public key: {public_key_path}\n"
                                  f"Private key: {private_key_path}\n\n"
                                  f"⚠️ Keep private key secure!")
            
            elif algo == 'aes':
                from src.utils import generate_random_key
                import base64
                
                key = generate_random_key(32)
                key_path = os.path.join(output_dir, 'aes_key.bin')
                
                with open(key_path, 'wb') as f:
                    f.write(key)
                
                key_b64 = base64.b64encode(key).decode()
                
                messagebox.showinfo("Success",
                                  f"AES-256 key generated!\n\n"
                                  f"Key file: {key_path}\n"
                                  f"Key (base64): {key_b64[:50]}...\n\n"
                                  f"⚠️ Keep key secure!")
            
            self.logger.success(f"{algo.upper()} keys generated successfully")
        
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.logger.error(f"Key generation failed: {str(e)}")
    
    def _handle_stego_encode(self):
        """Handle steganography encoding"""
        stego_type = self.stego_type.get()
        
        # Select cover file
        if stego_type == 'image':
            cover_file = filedialog.askopenfilename(
                title="Select Cover Image",
                filetypes=[("Image files", "*.png *.bmp")]
            )
        else:
            cover_file = filedialog.askopenfilename(
                title="Select Cover Audio",
                filetypes=[("WAV files", "*.wav")]
            )
        
        if not cover_file:
            return
        
        # Get message
        window = tk.Toplevel(self.root)
        window.title("Enter Message to Hide")
        window.geometry("500x400")
        window.configure(bg="white")
        
        tk.Label(window, text="Enter message to hide:", font=("Arial", 12, "bold"),
                bg="white").pack(pady=10)
        message_text = scrolledtext.ScrolledText(window, height=15, font=("Arial", 11))
        message_text.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        def encode():
            message = message_text.get("1.0", tk.END).strip()
            if not message:
                messagebox.showwarning("Input Error", "Please enter a message")
                return
            
            # Select output file
            if stego_type == 'image':
                output_file = filedialog.asksaveasfilename(
                    defaultextension=".png",
                    filetypes=[("PNG files", "*.png"), ("BMP files", "*.bmp")]
                )
            else:
                output_file = filedialog.asksaveasfilename(
                    defaultextension=".wav",
                    filetypes=[("WAV files", "*.wav")]
                )
            
            if not output_file:
                return
            
            try:
                if stego_type == 'image':
                    result = ImageSteganography.encode(
                        cover_file, message, output_file,
                        compress=self.compress_var.get()
                    )
                    messagebox.showinfo("Success",
                                      f"Message hidden successfully!\n\n"
                                      f"Output: {output_file}\n"
                                      f"Message size: {result['message_size']} bytes\n"
                                      f"Compressed: {result['compressed']}")
                else:
                    result = AudioSteganography.encode(
                        cover_file, message, output_file
                    )
                    messagebox.showinfo("Success",
                                      f"Message hidden successfully!\n\n"
                                      f"Output: {output_file}\n"
                                      f"Duration: {result['audio_duration']:.2f}s")
                
                window.destroy()
                self.logger.success("Message hidden successfully")
            
            except Exception as e:
                messagebox.showerror("Error", str(e))
                self.logger.error(f"Steganography encoding failed: {str(e)}")
        
        ModernButton(window, text="📥 Hide Message", bg="#4CAF50",
                    command=encode).pack(pady=15)
    
    def _handle_stego_decode(self):
        """Handle steganography decoding"""
        stego_type = self.stego_type.get()
        
        # Select stego file
        if stego_type == 'image':
            stego_file = filedialog.askopenfilename(
                title="Select Stego Image",
                filetypes=[("Image files", "*.png *.bmp")]
            )
        else:
            stego_file = filedialog.askopenfilename(
                title="Select Stego Audio",
                filetypes=[("WAV files", "*.wav")]
            )
        
        if not stego_file:
            return
        
        try:
            if stego_type == 'image':
                message = ImageSteganography.decode(
                    stego_file,
                    compressed=self.compress_var.get()
                )
            else:
                message = AudioSteganography.decode(stego_file)
            
            # Show message
            window = tk.Toplevel(self.root)
            window.title("Extracted Message")
            window.geometry("600x400")
            window.configure(bg="white")
            
            tk.Label(window, text="Extracted Message:", font=("Arial", 14, "bold"),
                    bg="white").pack(pady=10)
            
            message_text = scrolledtext.ScrolledText(window, height=15, font=("Arial", 11))
            message_text.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
            message_text.insert("1.0", message)
            message_text.config(state=tk.DISABLED)
            
            def save_message():
                output_file = filedialog.asksaveasfilename(
                    defaultextension=".txt",
                    filetypes=[("Text files", "*.txt")]
                )
                if output_file:
                    with open(output_file, 'w') as f:
                        f.write(message)
                    messagebox.showinfo("Success", f"Message saved to {output_file}")
            
            ModernButton(window, text="💾 Save Message", bg="#2196F3",
                        command=save_message).pack(pady=10)
            
            self.logger.success("Message extracted successfully")
        
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.logger.error(f"Steganography decoding failed: {str(e)}")
    
    def _handle_check_capacity(self):
        """Check file capacity for steganography"""
        stego_type = self.stego_type.get()
        
        if stego_type == 'image':
            file_path = filedialog.askopenfilename(
                title="Select Image",
                filetypes=[("Image files", "*.png *.bmp *.jpg *.jpeg")]
            )
        else:
            file_path = filedialog.askopenfilename(
                title="Select Audio",
                filetypes=[("WAV files", "*.wav")]
            )
        
        if not file_path:
            return
        
        try:
            if stego_type == 'image':
                capacity = ImageSteganography.get_capacity(file_path)
                messagebox.showinfo("Image Capacity",
                                  f"Image Size: {capacity['image_size']}\n"
                                  f"Total Pixels: {capacity['total_pixels']:,}\n"
                                  f"Max Bytes: {capacity['max_bytes']:,}\n"
                                  f"Max Characters: ~{capacity['max_chars_approx']:,}")
            else:
                capacity = AudioSteganography.get_capacity(file_path)
                messagebox.showinfo("Audio Capacity",
                                  f"Channels: {capacity['channels']}\n"
                                  f"Sample Rate: {capacity['frame_rate']} Hz\n"
                                  f"Duration: {capacity['duration_seconds']:.2f}s\n"
                                  f"Max Bytes: {capacity['max_bytes']:,}\n"
                                  f"Max Characters: ~{capacity['max_chars_approx']:,}")
        
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def _handle_password_generator(self):
        """Generate strong password"""
        window = tk.Toplevel(self.root)
        window.title("Password Generator")
        window.geometry("500x350")
        window.configure(bg="white")
        
        tk.Label(window, text="Generate Strong Password", font=("Arial", 16, "bold"),
                bg="white").pack(pady=20)
        
        tk.Label(window, text="Password Length:", font=("Arial", 11),
                bg="white").pack(pady=5)
        length_var = tk.IntVar(value=16)
        length_scale = tk.Scale(window, from_=8, to=32, orient=tk.HORIZONTAL,
                               variable=length_var, length=300)
        length_scale.pack(pady=5)
        
        result_frame = tk.Frame(window, bg="white")
        result_frame.pack(pady=20, fill=tk.X, padx=20)
        
        password_entry = tk.Entry(result_frame, font=("Courier", 14), width=30,
                                 justify=tk.CENTER)
        password_entry.pack(pady=10)
        
        def generate():
            password = PasswordValidator.generate_strong_password(length_var.get())
            password_entry.delete(0, tk.END)
            password_entry.insert(0, password)
            
            # Validate
            result = PasswordValidator.validate_strength(password)
            messagebox.showinfo("Password Generated",
                              f"Strength: {result['strength']}\n"
                              f"Score: {result['score']}/8\n\n"
                              f"✅ Password copied to entry field")
        
        def copy_password():
            window.clipboard_clear()
            window.clipboard_append(password_entry.get())
            messagebox.showinfo("Copied", "Password copied to clipboard!")
        
        button_frame = tk.Frame(window, bg="white")
        button_frame.pack(pady=10)
        
        ModernButton(button_frame, text="🔄 Generate", bg="#4CAF50",
                    command=generate).pack(side=tk.LEFT, padx=5)
        ModernButton(button_frame, text="📋 Copy", bg="#2196F3",
                    command=copy_password).pack(side=tk.LEFT, padx=5)
    
    def _handle_password_validator(self):
        """Validate password strength"""
        window = tk.Toplevel(self.root)
        window.title("Password Validator")
        window.geometry("500x450")
        window.configure(bg="white")
        
        tk.Label(window, text="Password Strength Validator", font=("Arial", 16, "bold"),
                bg="white").pack(pady=20)
        
        tk.Label(window, text="Enter password to validate:", font=("Arial", 11),
                bg="white").pack(pady=5)
        password_entry = tk.Entry(window, font=("Arial", 12), width=30, show="*")
        password_entry.pack(pady=10)
        
        show_var = tk.BooleanVar()
        tk.Checkbutton(window, text="Show password", variable=show_var,
                      bg="white", command=lambda: password_entry.config(
                          show="" if show_var.get() else "*")).pack()
        
        result_text = scrolledtext.ScrolledText(window, height=12, font=("Arial", 11),
                                               state=tk.DISABLED)
        result_text.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        def validate():
            password = password_entry.get()
            if not password:
                messagebox.showwarning("Input Error", "Please enter a password")
                return
            
            result = PasswordValidator.validate_strength(password)
            
            result_text.config(state=tk.NORMAL)
            result_text.delete("1.0", tk.END)
            
            result_text.insert("1.0", f"Password Strength: {result['strength']}\n")
            result_text.insert(tk.END, f"Score: {result['score']}/8\n")
            result_text.insert(tk.END, f"Valid: {'Yes' if result['valid'] else 'No'}\n\n")
            
            if result['feedback']:
                result_text.insert(tk.END, "Recommendations:\n")
                for feedback in result['feedback']:
                    result_text.insert(tk.END, f"  • {feedback}\n")
            else:
                result_text.insert(tk.END, "✅ Excellent password!")
            
            result_text.config(state=tk.DISABLED)
        
        ModernButton(window, text="✅ Validate", bg="#4CAF50",
                    command=validate).pack(pady=10)
    
    def _handle_file_hash(self):
        """Calculate file hash"""
        file_path = filedialog.askopenfilename(title="Select File to Hash")
        if not file_path:
            return
        
        window = tk.Toplevel(self.root)
        window.title("File Hash Calculator")
        window.geometry("600x400")
        window.configure(bg="white")
        
        tk.Label(window, text="File Hash Calculator", font=("Arial", 16, "bold"),
                bg="white").pack(pady=20)
        
        tk.Label(window, text=f"File: {os.path.basename(file_path)}",
                font=("Arial", 11), bg="white").pack(pady=5)
        
        hash_algo = tk.StringVar(value="sha256")
        
        algo_frame = tk.Frame(window, bg="white")
        algo_frame.pack(pady=10)
        
        tk.Radiobutton(algo_frame, text="MD5", variable=hash_algo, value="md5",
                      bg="white").pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(algo_frame, text="SHA-1", variable=hash_algo, value="sha1",
                      bg="white").pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(algo_frame, text="SHA-256", variable=hash_algo, value="sha256",
                      bg="white").pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(algo_frame, text="SHA-512", variable=hash_algo, value="sha512",
                      bg="white").pack(side=tk.LEFT, padx=10)
        
        result_text = scrolledtext.ScrolledText(window, height=10, font=("Courier", 10))
        result_text.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        def calculate():
            try:
                hash_value = calculate_file_hash(file_path, hash_algo.get())
                result_text.delete("1.0", tk.END)
                result_text.insert("1.0", f"Algorithm: {hash_algo.get().upper()}\n\n")
                result_text.insert(tk.END, f"Hash:\n{hash_value}")
                
                self.logger.success(f"Hash calculated: {hash_algo.get().upper()}")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        def copy_hash():
            hash_text = result_text.get("3.0", tk.END).strip()
            if hash_text:
                window.clipboard_clear()
                window.clipboard_append(hash_text)
                messagebox.showinfo("Copied", "Hash copied to clipboard!")
        
        button_frame = tk.Frame(window, bg="white")
        button_frame.pack(pady=10)
        
        ModernButton(button_frame, text="Calculate", bg="#4CAF50",
                    command=calculate).pack(side=tk.LEFT, padx=5)
        ModernButton(button_frame, text="Copy", bg="#2196F3",
                    command=copy_hash).pack(side=tk.LEFT, padx=5)
    
    def _handle_verify_integrity(self):
        """Verify file integrity"""
        messagebox.showinfo("Verify File Integrity",
                          "Select a file and provide its expected hash to verify integrity.")
        
        file_path = filedialog.askopenfilename(title="Select File to Verify")
        if not file_path:
            return
        
        # Get expected hash
        window = tk.Toplevel(self.root)
        window.title("Verify File Integrity")
        window.geometry("500x300")
        window.configure(bg="white")
        
        tk.Label(window, text="Enter expected hash:", font=("Arial", 12, "bold"),
                bg="white").pack(pady=20)
        
        hash_entry = tk.Entry(window, font=("Arial", 11), width=50)
        hash_entry.pack(pady=10)
        
        hash_algo = tk.StringVar(value="sha256")
        
        algo_frame = tk.Frame(window, bg="white")
        algo_frame.pack(pady=10)
        
        tk.Label(algo_frame, text="Algorithm:", bg="white").pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(algo_frame, text="SHA-256", variable=hash_algo,
                      value="sha256", bg="white").pack(side=tk.LEFT, padx=5)
        tk.Radiobutton(algo_frame, text="SHA-512", variable=hash_algo,
                      value="sha512", bg="white").pack(side=tk.LEFT, padx=5)
        
        def verify():
            expected_hash = hash_entry.get().strip()
            if not expected_hash:
                messagebox.showwarning("Input Error", "Please enter expected hash")
                return
            
            try:
                from src.utils import verify_file_integrity
                
                is_valid = verify_file_integrity(file_path, expected_hash, hash_algo.get())
                
                if is_valid:
                    messagebox.showinfo("✅ Verification Passed",
                                      "File integrity verified!\n\nThe file has not been tampered with.")
                    self.logger.success("File integrity verification passed")
                else:
                    messagebox.showwarning("❌ Verification Failed",
                                         "File integrity check failed!\n\nThe file may have been tampered with.")
                    self.logger.warning("File integrity verification failed")
                
                window.destroy()
            
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        ModernButton(window, text="🔍 Verify", bg="#4CAF50",
                    command=verify).pack(pady=20)
    
    def _handle_show_docs(self):
        """Show documentation"""
        docs_path = os.path.join(os.path.dirname(__file__), 'docs', 'USAGE.md')
        
        if os.path.exists(docs_path):
            window = tk.Toplevel(self.root)
            window.title("Documentation")
            window.geometry("800x600")
            window.configure(bg="white")
            
            text_widget = scrolledtext.ScrolledText(window, font=("Courier", 10),
                                                   wrap=tk.WORD)
            text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            with open(docs_path, 'r') as f:
                text_widget.insert("1.0", f.read())
            
            text_widget.config(state=tk.DISABLED)
        else:
            messagebox.showinfo("Documentation",
                              "Documentation not found.\n\n"
                              "Please refer to the GitHub repository for usage instructions.")
    
    def _handle_about(self):
        """Show about dialog"""
        about_text = """
🔐 Secure CipherStegno Tool
Professional Edition v2.0

Advanced cryptography and steganography toolkit
for secure communication and data hiding.

Features:
• Multiple encryption algorithms (Caesar, AES-256, RSA)
• Image and audio steganography
• Password strength validation
• File integrity verification
• Hash calculation tools
• Key management system

Developed by: Parth Thakar
© 2025 All Rights Reserved

License: MIT
Platform: Cross-platform (Windows, Linux, macOS)

This is a privacy-first, local-only security tool.
No data is ever sent to external servers.
        """
        
        messagebox.showinfo("About Secure CipherStegno Tool", about_text)


def main():
    """Main entry point for GUI application"""
    root = tk.Tk()
    app = SecureCipherStegnoApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
