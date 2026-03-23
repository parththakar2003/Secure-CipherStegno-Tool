"""
Secure CipherStegno Tool — GUI Application
Professional cryptography and steganography toolkit
"""

import sys
import os
import threading

# ── Python version guard ───────────────────────────────────────────────────────
if sys.version_info < (3, 8):
    sys.stderr.write(
        "=" * 60 + "\n"
        "ERROR: Python 3.8 or higher is required\n"
        "=" * 60 + "\n"
        "Current:  {}.{}.{}\n".format(*sys.version_info[:3]) +
        "Required: 3.8+\n\n"
        "Download from: https://www.python.org/downloads/\n"
        "=" * 60 + "\n"
    )
    sys.exit(1)

# ── Tkinter availability guard ─────────────────────────────────────────────────
try:
    import tkinter as tk
    from tkinter import ttk, messagebox, filedialog, scrolledtext
except (ImportError, ModuleNotFoundError) as e:
    print("=" * 60)
    print("ERROR: Tkinter is not available")
    print("=" * 60)
    print(f"\nImport error: {e}\n")
    print("Alternatives:")
    print("  CLI:              python cli.py --help")
    print("  Interactive CLI:  python interactive_cli.py")
    print("\nInstall Tkinter on Linux:")
    print("  Ubuntu/Debian:  sudo apt-get install python3-tk")
    print("  Fedora/RHEL:    sudo dnf install python3-tkinter")
    print("  Arch:           sudo pacman -S tk")
    print("=" * 60)
    sys.exit(1)

# ── Path setup ─────────────────────────────────────────────────────────────────
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.crypto import (
    CaesarCipher, AESCipher, RSACipher, VigenereCipher,
    PlayfairCipher, RailFenceCipher, BlowfishCipher,
    DES3Cipher, ChaCha20Cipher,
)
from src.steganography import ImageSteganography, AudioSteganography, VideoSteganography
from src.utils import PasswordValidator, calculate_file_hash, Logger

# ── Theme ──────────────────────────────────────────────────────────────────────
C = {
    "sb_bg":      "#1e1e2e",   # sidebar background
    "sb_hover":   "#313244",   # sidebar hover
    "sb_active":  "#4361ee",   # sidebar active item
    "sb_text":    "#cdd6f4",   # sidebar label text
    "sb_icon":    "#89b4fa",   # sidebar icon tint
    "bg":         "#f0f2f5",   # main content background
    "card":       "#ffffff",   # card / panel background
    "border":     "#e2e8f0",   # card borders & separators
    "primary":    "#4361ee",   # primary action
    "success":    "#2ec4b6",   # success / confirm
    "warning":    "#e07a5f",   # warning / destructive
    "purple":     "#7b2d8b",   # key-gen / secondary
    "slate":      "#64748b",   # neutral action
    "text":       "#1e293b",   # primary text
    "text_mid":   "#475569",   # secondary text
    "text_dim":   "#94a3b8",   # tertiary / hint text
    "status_bg":  "#1e1e2e",
    "status_ok":  "#2ec4b6",
    "status_err": "#e63946",
    "status_busy":"#f9c74f",
    "status_info":"#89b4fa",
}

F = {
    "title":   ("Segoe UI", 18, "bold"),
    "heading": ("Segoe UI", 11, "bold"),
    "body":    ("Segoe UI", 10),
    "small":   ("Segoe UI", 9),
    "nav":     ("Segoe UI", 11),
    "mono":    ("Consolas", 10),
    "mono_lg": ("Consolas", 11),
}


# ── Reusable widgets ───────────────────────────────────────────────────────────

class NavButton(tk.Frame):
    """Sidebar navigation item."""

    def __init__(self, parent, icon: str, label: str, command, **kw):
        super().__init__(parent, bg=C["sb_bg"], cursor="hand2", **kw)
        self._active = False
        self._cmd = command

        self._row = tk.Frame(self, bg=C["sb_bg"], padx=14, pady=11)
        self._row.pack(fill=tk.X)

        self._ico = tk.Label(self._row, text=icon, font=("Segoe UI Emoji", 15),
                             bg=C["sb_bg"], fg=C["sb_icon"])
        self._ico.pack(side=tk.LEFT, padx=(0, 10))

        self._lbl = tk.Label(self._row, text=label, font=F["nav"],
                             bg=C["sb_bg"], fg=C["sb_text"], anchor="w")
        self._lbl.pack(side=tk.LEFT, fill=tk.X, expand=True)

        for w in (self, self._row, self._ico, self._lbl):
            w.bind("<Button-1>", lambda _: self._cmd())
            w.bind("<Enter>",    self._hover_on)
            w.bind("<Leave>",    self._hover_off)

    def _hover_on(self, _=None):
        if not self._active:
            self._set_bg(C["sb_hover"])

    def _hover_off(self, _=None):
        if not self._active:
            self._set_bg(C["sb_bg"])

    def _set_bg(self, colour: str):
        for w in (self, self._row, self._ico, self._lbl):
            w.config(bg=colour)

    def set_active(self, active: bool):
        self._active = active
        self._set_bg(C["sb_active"] if active else C["sb_bg"])


class Btn(tk.Button):
    """Styled flat action button."""

    def __init__(self, parent, text: str, color: str = None, **kw):
        color = color or C["primary"]
        r, g, b = (int(color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
        dark = "#{:02x}{:02x}{:02x}".format(max(r-24,0), max(g-24,0), max(b-24,0))
        super().__init__(
            parent, text=text,
            font=F["body"],
            bg=color, fg="white",
            activebackground=dark, activeforeground="white",
            relief=tk.FLAT, bd=0,
            padx=14, pady=7,
            cursor="hand2",
            **kw,
        )


# ── Main application ───────────────────────────────────────────────────────────

class SecureCipherStegnoApp:
    """Main application window."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Secure CipherStegno Tool")
        self.root.geometry("1120x730")
        self.root.minsize(920, 620)
        self.root.configure(bg=C["sb_bg"])

        self.logger = Logger()
        self._active_nav: str | None = None
        self._panels: dict[str, tk.Frame] = {}
        self._nav_btns: dict[str, NavButton] = {}

        self._apply_styles()
        self._build_window()
        self._navigate("crypto")

    # ── Styles ─────────────────────────────────────────────────────────────────

    def _apply_styles(self):
        s = ttk.Style()
        try:
            s.theme_use("clam")
        except Exception:
            pass
        s.configure("TLabelframe",       background=C["card"], borderwidth=1, relief="solid")
        s.configure("TLabelframe.Label", background=C["card"], foreground=C["text_mid"],
                    font=F["heading"])
        s.configure("TRadiobutton",      background=C["card"], foreground=C["text"],
                    font=F["body"])
        s.configure("TCheckbutton",      background=C["card"], foreground=C["text"],
                    font=F["body"])
        s.configure("TSeparator",        background=C["border"])
        s.configure("Vertical.TScrollbar",
                    background=C["border"], troughcolor=C["bg"],
                    arrowcolor=C["text_dim"], relief="flat")

    # ── Window structure ───────────────────────────────────────────────────────

    def _build_window(self):
        # Left sidebar
        self._sidebar = tk.Frame(self.root, bg=C["sb_bg"], width=220)
        self._sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self._sidebar.pack_propagate(False)

        # Right content area
        self._area = tk.Frame(self.root, bg=C["bg"])
        self._area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self._build_sidebar()
        self._build_status_bar()

        # Build all panels upfront
        for key, fn in [
            ("crypto", self._make_crypto_panel),
            ("stego",  self._make_stego_panel),
            ("tools",  self._make_tools_panel),
            ("about",  self._make_about_panel),
        ]:
            self._panels[key] = fn()

    def _build_sidebar(self):
        # Logo block
        logo = tk.Frame(self._sidebar, bg=C["sb_bg"], pady=24)
        logo.pack(fill=tk.X)
        tk.Label(logo, text="🔐", font=("Segoe UI Emoji", 30),
                 bg=C["sb_bg"], fg=C["sb_icon"]).pack()
        tk.Label(logo, text="CipherStegno",
                 font=("Segoe UI", 13, "bold"),
                 bg=C["sb_bg"], fg="#ffffff").pack()
        tk.Label(logo, text="Security Toolkit",
                 font=F["small"], bg=C["sb_bg"], fg=C["sb_text"]).pack()

        tk.Frame(self._sidebar, bg=C["sb_hover"], height=1).pack(fill=tk.X, padx=16, pady=6)

        for key, icon, label in [
            ("crypto", "🔒", "Cryptography"),
            ("stego",  "🖼", "Steganography"),
            ("tools",  "🛠", "Security Tools"),
            ("about",  "ℹ",  "About"),
        ]:
            btn = NavButton(self._sidebar, icon, label,
                            command=lambda k=key: self._navigate(k))
            btn.pack(fill=tk.X)
            self._nav_btns[key] = btn

        tk.Label(self._sidebar, text="v3.1.0", font=F["small"],
                 bg=C["sb_bg"], fg=C["text_dim"]).pack(side=tk.BOTTOM, pady=10)

    def _build_status_bar(self):
        bar = tk.Frame(self._area, bg=C["status_bg"], height=30)
        bar.pack(side=tk.BOTTOM, fill=tk.X)
        bar.pack_propagate(False)

        self._status_dot = tk.Label(bar, text="●", font=F["small"],
                                    bg=C["status_bg"], fg=C["status_ok"], padx=10)
        self._status_dot.pack(side=tk.LEFT)

        self._status_lbl = tk.Label(bar, text="Ready", font=F["small"],
                                    bg=C["status_bg"], fg=C["sb_text"], anchor="w")
        self._status_lbl.pack(side=tk.LEFT, fill=tk.Y)

    def _status(self, msg: str, kind: str = "info"):
        dot_colors = {
            "ok":   C["status_ok"],
            "error":C["status_err"],
            "busy": C["status_busy"],
            "info": C["status_info"],
        }
        self._status_dot.config(fg=dot_colors.get(kind, C["status_info"]))
        self._status_lbl.config(text=msg)

    # ── Navigation ──────────────────────────────────────────────────────────────

    def _navigate(self, key: str):
        if self._active_nav:
            self._nav_btns[self._active_nav].set_active(False)
            self._panels[self._active_nav].pack_forget()
        self._active_nav = key
        self._nav_btns[key].set_active(True)
        self._panels[key].pack(fill=tk.BOTH, expand=True)

    # ── Panel / card helpers ────────────────────────────────────────────────────

    def _scrollable_panel(self, page_title: str, subtitle: str = "") -> tuple[tk.Frame, tk.Frame]:
        """Return (outer_frame, scrollable_body_frame)."""
        outer = tk.Frame(self._area, bg=C["bg"])

        # Page header
        hdr = tk.Frame(outer, bg=C["bg"], padx=30, pady=20)
        hdr.pack(fill=tk.X)
        tk.Label(hdr, text=page_title, font=F["title"],
                 bg=C["bg"], fg=C["text"]).pack(anchor="w")
        if subtitle:
            tk.Label(hdr, text=subtitle, font=F["body"],
                     bg=C["bg"], fg=C["text_dim"]).pack(anchor="w", pady=(2, 0))

        tk.Frame(outer, bg=C["border"], height=1).pack(fill=tk.X)

        # Scrollable body
        canvas = tk.Canvas(outer, bg=C["bg"], highlightthickness=0)
        vsb = ttk.Scrollbar(outer, orient="vertical",
                            style="Vertical.TScrollbar",
                            command=canvas.yview)
        body = tk.Frame(canvas, bg=C["bg"])
        body.bind("<Configure>",
                  lambda _: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=body, anchor="nw")
        canvas.configure(yscrollcommand=vsb.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        canvas.bind_all("<MouseWheel>",
                        lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        return outer, body

    def _card(self, parent: tk.Frame, title: str = "") -> tk.Frame:
        """Return the inner content frame of a white card."""
        wrap = tk.Frame(parent, bg=C["bg"], padx=30, pady=8)
        wrap.pack(fill=tk.X)

        card = tk.Frame(wrap, bg=C["card"],
                        highlightbackground=C["border"], highlightthickness=1)
        card.pack(fill=tk.X)

        if title:
            tk.Label(card, text=title, font=F["heading"],
                     bg=C["card"], fg=C["text_mid"],
                     padx=16, pady=10).pack(anchor="w")
            tk.Frame(card, bg=C["border"], height=1).pack(fill=tk.X)

        inner = tk.Frame(card, bg=C["card"], padx=16, pady=14)
        inner.pack(fill=tk.BOTH, expand=True)
        return inner

    # ── Form helpers ───────────────────────────────────────────────────────────

    def _field(self, parent: tk.Frame, label: str,
               show: str = "", width: int = 42) -> tk.Entry:
        tk.Label(parent, text=label, font=F["small"],
                 bg=C["card"], fg=C["text_mid"]).pack(anchor="w", pady=(8, 2))
        e = tk.Entry(parent, font=F["mono"], width=width, show=show,
                     relief=tk.FLAT,
                     highlightbackground=C["border"], highlightthickness=1,
                     bg="#f8fafc")
        e.pack(anchor="w")
        return e

    def _textarea(self, parent: tk.Frame, label: str, height: int = 6,
                  readonly: bool = False) -> scrolledtext.ScrolledText:
        tk.Label(parent, text=label, font=F["small"],
                 bg=C["card"], fg=C["text_mid"]).pack(anchor="w", pady=(8, 2))
        t = scrolledtext.ScrolledText(
            parent, height=height, font=F["mono_lg"],
            relief=tk.FLAT,
            highlightbackground=C["border"], highlightthickness=1,
            bg="#f8fafc",
            state=tk.DISABLED if readonly else tk.NORMAL,
        )
        t.pack(fill=tk.X)
        return t

    def _output(self, parent: tk.Frame, label: str = "Output",
                height: int = 5) -> scrolledtext.ScrolledText:
        """Read-only output area with a Copy button."""
        row = tk.Frame(parent, bg=C["card"])
        row.pack(fill=tk.X, pady=(8, 2))
        tk.Label(row, text=label, font=F["small"],
                 bg=C["card"], fg=C["text_mid"]).pack(side=tk.LEFT)

        t = scrolledtext.ScrolledText(
            parent, height=height, font=F["mono_lg"],
            relief=tk.FLAT,
            highlightbackground=C["border"], highlightthickness=1,
            bg="#f8fafc", state=tk.DISABLED,
        )
        t.pack(fill=tk.X)

        def _copy():
            content = t.get("1.0", tk.END).strip()
            if content:
                self.root.clipboard_clear()
                self.root.clipboard_append(content)
                self._status("Copied to clipboard", "ok")

        Btn(parent, "📋  Copy to clipboard", color=C["slate"],
            command=_copy).pack(anchor="e", pady=(4, 0))
        return t

    def _write_output(self, widget: scrolledtext.ScrolledText, text: str):
        """Thread-safe helper to write to a read-only output widget."""
        def _do():
            widget.config(state=tk.NORMAL)
            widget.delete("1.0", tk.END)
            widget.insert("1.0", text)
            widget.config(state=tk.DISABLED)
        self.root.after(0, _do)

    # ── Dialog helper ──────────────────────────────────────────────────────────

    def _dialog(self, title: str, w: int = 640, h: int = 580) -> tuple[tk.Toplevel, tk.Frame]:
        win = tk.Toplevel(self.root)
        win.title(title)
        win.geometry(f"{w}x{h}")
        win.configure(bg=C["card"])
        win.resizable(True, True)
        win.transient(self.root)
        win.grab_set()

        # Coloured header stripe
        hdr = tk.Frame(win, bg=C["primary"], height=50)
        hdr.pack(fill=tk.X)
        hdr.pack_propagate(False)
        tk.Label(hdr, text=title, font=("Segoe UI", 12, "bold"),
                 bg=C["primary"], fg="white", padx=18).pack(side=tk.LEFT, fill=tk.Y)

        body = tk.Frame(win, bg=C["card"], padx=20, pady=16)
        body.pack(fill=tk.BOTH, expand=True)
        return win, body

    # ══════════════════════════════════════════════════════════════════
    # PANELS
    # ══════════════════════════════════════════════════════════════════

    def _make_crypto_panel(self) -> tk.Frame:
        panel, body = self._scrollable_panel(
            "Cryptography",
            "Encrypt and decrypt text using classical and modern ciphers."
        )

        algo_card = self._card(body, "Select Algorithm")

        col_l = tk.Frame(algo_card, bg=C["card"])
        col_l.pack(side=tk.LEFT, anchor="n", padx=(0, 40))
        col_r = tk.Frame(algo_card, bg=C["card"])
        col_r.pack(side=tk.LEFT, anchor="n")

        self.crypto_algo = tk.StringVar(value="aes")

        tk.Label(col_l, text="CLASSICAL", font=F["small"],
                 bg=C["card"], fg=C["text_dim"]).pack(anchor="w", pady=(0, 6))
        for val, lbl in [
            ("caesar",    "Caesar Cipher"),
            ("vigenere",  "Vigenère Cipher"),
            ("playfair",  "Playfair Cipher"),
            ("railfence", "Rail Fence Cipher"),
        ]:
            ttk.Radiobutton(col_l, text=lbl, variable=self.crypto_algo,
                            value=val).pack(anchor="w", pady=2)

        tk.Label(col_r, text="MODERN", font=F["small"],
                 bg=C["card"], fg=C["text_dim"]).pack(anchor="w", pady=(0, 6))
        for val, lbl in [
            ("aes",      "AES-256  ★ Recommended"),
            ("chacha20", "ChaCha20"),
            ("blowfish", "Blowfish"),
            ("3des",     "3DES  ⚠ Legacy"),
            ("rsa",      "RSA  (Asymmetric)"),
        ]:
            ttk.Radiobutton(col_r, text=lbl, variable=self.crypto_algo,
                            value=val).pack(anchor="w", pady=2)

        btn_card = self._card(body, "Actions")
        row = tk.Frame(btn_card, bg=C["card"])
        row.pack(anchor="w")
        Btn(row, "🔒  Encrypt",       color=C["success"], command=self._open_encrypt).pack(side=tk.LEFT, padx=(0, 8))
        Btn(row, "🔓  Decrypt",       color=C["warning"], command=self._open_decrypt).pack(side=tk.LEFT, padx=(0, 8))
        Btn(row, "🔑  Generate Keys", color=C["purple"],  command=self._handle_keygen).pack(side=tk.LEFT)

        return panel

    def _make_stego_panel(self) -> tk.Frame:
        panel, body = self._scrollable_panel(
            "Steganography",
            "Hide and extract secret messages inside image, audio, or video files."
        )

        type_card = self._card(body, "Media Type")
        self.stego_type = tk.StringVar(value="image")
        for val, lbl in [
            ("image", "🖼  Image  (PNG, BMP)"),
            ("audio", "🎵  Audio  (WAV)"),
            ("video", "🎬  Video  (MP4, AVI)"),
        ]:
            ttk.Radiobutton(type_card, text=lbl, variable=self.stego_type,
                            value=val).pack(anchor="w", pady=3)

        opt_card = self._card(body, "Options")
        self.compress_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(opt_card,
                        text="Compress message before hiding  (recommended for images)",
                        variable=self.compress_var).pack(anchor="w")

        btn_card = self._card(body, "Actions")
        row = tk.Frame(btn_card, bg=C["card"])
        row.pack(anchor="w")
        Btn(row, "📥  Hide Message",    color=C["primary"], command=self._handle_stego_encode).pack(side=tk.LEFT, padx=(0, 8))
        Btn(row, "📤  Extract Message", color=C["success"], command=self._handle_stego_decode).pack(side=tk.LEFT, padx=(0, 8))
        Btn(row, "ℹ  Check Capacity",  color=C["slate"],   command=self._handle_check_capacity).pack(side=tk.LEFT)

        return panel

    def _make_tools_panel(self) -> tk.Frame:
        panel, body = self._scrollable_panel(
            "Security Tools",
            "Password utilities, file hashing, and integrity verification."
        )
        card = self._card(body)
        grid = tk.Frame(card, bg=C["card"])
        grid.pack(anchor="w")

        tools = [
            ("🔐  Password Generator",   C["success"], self._handle_pwd_gen),
            ("✅  Password Validator",    C["primary"], self._handle_pwd_val),
            ("#   File Hash Calculator",  C["warning"], self._handle_file_hash),
            ("🔍  Verify File Integrity", C["purple"],  self._handle_verify),
            ("📖  Documentation",         C["slate"],   self._handle_docs),
        ]
        for i, (lbl, col, cmd) in enumerate(tools):
            r, c = divmod(i, 2)
            Btn(grid, lbl, color=col, command=cmd,
                width=24).grid(row=r, column=c, padx=8, pady=6, sticky="w")

        return panel

    def _make_about_panel(self) -> tk.Frame:
        panel, body = self._scrollable_panel("About")
        card = self._card(body)

        tk.Label(card, text="🔐  Secure CipherStegno Tool",
                 font=("Segoe UI", 16, "bold"),
                 bg=C["card"], fg=C["text"]).pack(anchor="w")
        tk.Label(card, text="Professional Edition  v3.1.0",
                 font=F["body"], bg=C["card"], fg=C["text_dim"]).pack(anchor="w")

        tk.Frame(card, bg=C["border"], height=1).pack(fill=tk.X, pady=14)

        for section, items in [
            ("Cryptography", [
                "Caesar, Vigenère, Playfair, Rail Fence  (classical)",
                "AES-256, ChaCha20, Blowfish, 3DES  (symmetric)",
                "RSA 2048/4096-bit  (asymmetric)",
            ]),
            ("Steganography", [
                "Image steganography — PNG, BMP  (LSB)",
                "Audio steganography — WAV",
                "Video steganography — MP4, AVI",
                "Optional message compression",
            ]),
            ("Security Tools", [
                "Password generator & strength validator",
                "File hashing — MD5, SHA-1, SHA-256, SHA-512",
                "File integrity verification",
                "RSA / AES key-pair management",
            ]),
        ]:
            tk.Label(card, text=section, font=F["heading"],
                     bg=C["card"], fg=C["primary"]).pack(anchor="w", pady=(10, 4))
            for item in items:
                tk.Label(card, text=f"  • {item}", font=F["body"],
                         bg=C["card"], fg=C["text_mid"]).pack(anchor="w")

        tk.Frame(card, bg=C["border"], height=1).pack(fill=tk.X, pady=14)
        tk.Label(card,
                 text="Developed by Parth Thakar  ·  MIT License  ·  Privacy-first, local-only",
                 font=F["small"], bg=C["card"], fg=C["text_dim"]).pack(anchor="w")
        return panel

    # ══════════════════════════════════════════════════════════════════
    # CRYPTOGRAPHY HANDLERS
    # ══════════════════════════════════════════════════════════════════

    def _algo_needs_password(self, algo: str) -> bool:
        return algo in ("aes", "blowfish", "3des", "chacha20")

    def _algo_needs_key(self, algo: str) -> bool:
        return algo in ("vigenere", "playfair")

    def _algo_needs_number(self, algo: str) -> bool:
        return algo in ("caesar", "railfence")

    def _open_encrypt(self):
        algo = self.crypto_algo.get()
        win, body = self._dialog(f"Encrypt  —  {algo.upper()}", 660, 610)

        input_text = self._textarea(body, "Plaintext", height=7)

        # Credential field (algorithm-dependent)
        cred_entry = None
        if self._algo_needs_password(algo):
            cred_entry = self._field(body, "Password", show="*")
        elif self._algo_needs_key(algo):
            cred_entry = self._field(body, "Key (keyword)")
        elif self._algo_needs_number(algo):
            num_lbl = "Shift value  (1–25)" if algo == "caesar" else "Number of rails  (≥ 2)"
            cred_entry = self._field(body, num_lbl, width=12)

        # For RSA, pick key file before submitting
        rsa_key_var: list[str] = []
        if algo == "rsa":
            rsa_row = tk.Frame(body, bg=C["card"])
            rsa_row.pack(anchor="w", pady=(10, 0))
            rsa_lbl = tk.Label(rsa_row, text="No public key selected",
                               font=F["small"], bg=C["card"], fg=C["text_dim"])
            rsa_lbl.pack(side=tk.LEFT, padx=(0, 10))

            def pick_pub():
                path = filedialog.askopenfilename(
                    title="Select RSA Public Key",
                    filetypes=[("PEM files", "*.pem"), ("All files", "*.*")],
                    parent=win,
                )
                if path:
                    rsa_key_var.clear()
                    rsa_key_var.append(path)
                    rsa_lbl.config(text=os.path.basename(path), fg=C["text_mid"])

            Btn(rsa_row, "📂  Select Public Key", color=C["slate"],
                command=pick_pub).pack(side=tk.LEFT)

        output_text = self._output(body, "Encrypted output", height=6)

        def _encrypt():
            text = input_text.get("1.0", tk.END).strip()
            if not text:
                messagebox.showwarning("Input required",
                                       "Please enter text to encrypt.", parent=win)
                return

            try:
                result_lines: list[str] = []

                if algo == "caesar":
                    raw = cred_entry.get().strip()
                    shift = int(raw) if raw else 3
                    result_lines = [CaesarCipher.encrypt(text, shift)]

                elif algo == "vigenere":
                    key = cred_entry.get().strip()
                    if not key:
                        raise ValueError("A keyword is required for Vigenère cipher.")
                    result_lines = [VigenereCipher.encrypt(text, key)]

                elif algo == "playfair":
                    key = cred_entry.get().strip()
                    if not key:
                        raise ValueError("A keyword is required for Playfair cipher.")
                    result_lines = [PlayfairCipher.encrypt(text, key)]

                elif algo == "railfence":
                    raw = cred_entry.get().strip()
                    rails = int(raw) if raw else 3
                    result_lines = [RailFenceCipher.encrypt(text, rails)]

                elif algo == "aes":
                    pw = cred_entry.get()
                    if not pw:
                        raise ValueError("A password is required for AES-256.")
                    r = AESCipher.encrypt_with_password(text, pw)
                    result_lines = [r["ciphertext"], "", f"IV: {r['iv']}",
                                    "", "# Save both the ciphertext and the IV for decryption."]

                elif algo == "blowfish":
                    pw = cred_entry.get()
                    if not pw:
                        raise ValueError("A password is required for Blowfish.")
                    r = BlowfishCipher.encrypt_with_password(text, pw)
                    result_lines = [r["ciphertext"], "", f"IV: {r['iv']}",
                                    "", "# Save both the ciphertext and the IV for decryption."]

                elif algo == "3des":
                    pw = cred_entry.get()
                    if not pw:
                        raise ValueError("A password is required for 3DES.")
                    r = DES3Cipher.encrypt_with_password(text, pw)
                    result_lines = [r["ciphertext"], "", f"IV: {r['iv']}",
                                    "", "⚠ 3DES is legacy — consider AES-256 for new data."]

                elif algo == "chacha20":
                    pw = cred_entry.get()
                    if not pw:
                        raise ValueError("A password is required for ChaCha20.")
                    r = ChaCha20Cipher.encrypt_with_password(text, pw)
                    result_lines = [r["ciphertext"], "", f"Nonce: {r['nonce']}",
                                    "", "# Save both the ciphertext and the nonce for decryption."]

                elif algo == "rsa":
                    if not rsa_key_var:
                        raise ValueError("Please select an RSA public key file.")
                    with open(rsa_key_var[0]) as f:
                        pub = f.read()
                    cipher = RSACipher()
                    cipher.load_public_key(pub)
                    result_lines = [cipher.encrypt(text)]

                self._write_output(output_text, "\n".join(result_lines))
                self._status(f"Encrypted with {algo.upper()}", "ok")
                self.logger.success(f"Encrypted with {algo.upper()}")

            except (ValueError, TypeError) as exc:
                messagebox.showwarning("Encryption error", str(exc), parent=win)
                self._status(f"Encryption error: {exc}", "error")
            except Exception as exc:
                messagebox.showerror("Encryption failed", str(exc), parent=win)
                self._status(f"Encryption failed: {exc}", "error")

        Btn(body, "🔒  Encrypt", color=C["success"],
            command=_encrypt).pack(anchor="e", pady=(14, 0))

    def _open_decrypt(self):
        algo = self.crypto_algo.get()
        win, body = self._dialog(f"Decrypt  —  {algo.upper()}", 660, 650)

        input_text = self._textarea(body, "Ciphertext", height=6)

        iv_entry = None
        if algo in ("aes", "blowfish", "3des"):
            iv_entry = self._field(body, "IV (Initialization Vector)", width=52)
        elif algo == "chacha20":
            iv_entry = self._field(body, "Nonce", width=52)

        cred_entry = None
        if self._algo_needs_password(algo):
            cred_entry = self._field(body, "Password", show="*")
        elif self._algo_needs_key(algo):
            cred_entry = self._field(body, "Key (keyword)")
        elif self._algo_needs_number(algo):
            num_lbl = "Shift value  (1–25)" if algo == "caesar" else "Number of rails  (≥ 2)"
            cred_entry = self._field(body, num_lbl, width=12)

        rsa_key_var: list[str] = []
        if algo == "rsa":
            rsa_row = tk.Frame(body, bg=C["card"])
            rsa_row.pack(anchor="w", pady=(10, 0))
            rsa_lbl = tk.Label(rsa_row, text="No private key selected",
                               font=F["small"], bg=C["card"], fg=C["text_dim"])
            rsa_lbl.pack(side=tk.LEFT, padx=(0, 10))

            def pick_prv():
                path = filedialog.askopenfilename(
                    title="Select RSA Private Key",
                    filetypes=[("PEM files", "*.pem"), ("All files", "*.*")],
                    parent=win,
                )
                if path:
                    rsa_key_var.clear()
                    rsa_key_var.append(path)
                    rsa_lbl.config(text=os.path.basename(path), fg=C["text_mid"])

            Btn(rsa_row, "📂  Select Private Key", color=C["slate"],
                command=pick_prv).pack(side=tk.LEFT)

        output_text = self._output(body, "Decrypted output", height=6)

        def _decrypt():
            text = input_text.get("1.0", tk.END).strip()
            if not text:
                messagebox.showwarning("Input required",
                                       "Please enter ciphertext to decrypt.", parent=win)
                return

            try:
                result = ""

                if algo == "caesar":
                    raw = cred_entry.get().strip()
                    shift = int(raw) if raw else 3
                    result = CaesarCipher.decrypt(text, shift)

                elif algo == "vigenere":
                    key = cred_entry.get().strip()
                    if not key:
                        raise ValueError("A keyword is required for Vigenère cipher.")
                    result = VigenereCipher.decrypt(text, key)

                elif algo == "playfair":
                    key = cred_entry.get().strip()
                    if not key:
                        raise ValueError("A keyword is required for Playfair cipher.")
                    result = PlayfairCipher.decrypt(text, key)

                elif algo == "railfence":
                    raw = cred_entry.get().strip()
                    rails = int(raw) if raw else 3
                    result = RailFenceCipher.decrypt(text, rails)

                elif algo == "aes":
                    pw  = cred_entry.get()
                    iv  = iv_entry.get().strip()
                    if not pw or not iv:
                        raise ValueError("Both password and IV are required for AES decryption.")
                    result = AESCipher.decrypt_with_password(text, iv, pw)

                elif algo == "blowfish":
                    pw  = cred_entry.get()
                    iv  = iv_entry.get().strip()
                    if not pw or not iv:
                        raise ValueError("Both password and IV are required for Blowfish decryption.")
                    result = BlowfishCipher.decrypt_with_password(text, iv, pw)

                elif algo == "3des":
                    pw  = cred_entry.get()
                    iv  = iv_entry.get().strip()
                    if not pw or not iv:
                        raise ValueError("Both password and IV are required for 3DES decryption.")
                    result = DES3Cipher.decrypt_with_password(text, iv, pw)

                elif algo == "chacha20":
                    pw    = cred_entry.get()
                    nonce = iv_entry.get().strip()
                    if not pw or not nonce:
                        raise ValueError("Both password and nonce are required for ChaCha20 decryption.")
                    result = ChaCha20Cipher.decrypt_with_password(text, nonce, pw)

                elif algo == "rsa":
                    if not rsa_key_var:
                        raise ValueError("Please select an RSA private key file.")
                    with open(rsa_key_var[0]) as f:
                        prv = f.read()
                    cipher = RSACipher()
                    cipher.load_private_key(prv)
                    result = cipher.decrypt(text)

                self._write_output(output_text, result)
                self._status(f"Decrypted with {algo.upper()}", "ok")
                self.logger.success(f"Decrypted with {algo.upper()}")

            except (ValueError, TypeError) as exc:
                messagebox.showwarning("Decryption error", str(exc), parent=win)
                self._status(f"Decryption error: {exc}", "error")
            except Exception as exc:
                messagebox.showerror("Decryption failed", str(exc), parent=win)
                self._status(f"Decryption failed: {exc}", "error")

        Btn(body, "🔓  Decrypt", color=C["warning"],
            command=_decrypt).pack(anchor="e", pady=(14, 0))

    def _handle_keygen(self):
        algo = self.crypto_algo.get()

        if algo in ("caesar", "railfence"):
            messagebox.showinfo("No key file needed",
                                f"The {algo.title()} cipher uses a numeric parameter, "
                                "not a key file.",
                                parent=self.root)
            return

        if algo not in ("rsa", "aes"):
            messagebox.showinfo("Password-based cipher",
                                f"{algo.upper()} uses password-based encryption.\n\n"
                                "No key file is needed — simply provide a strong password "
                                "when encrypting and the same password when decrypting.",
                                parent=self.root)
            return

        output_dir = filedialog.askdirectory(title="Select folder to save keys",
                                             parent=self.root)
        if not output_dir:
            return

        self._status("Generating keys…", "busy")

        def worker():
            try:
                if algo == "rsa":
                    cipher = RSACipher(key_size=2048)
                    keys = cipher.generate_key_pair()
                    pub = os.path.join(output_dir, "public_key.pem")
                    prv = os.path.join(output_dir, "private_key.pem")
                    with open(pub, "w") as f:
                        f.write(keys["public_key"])
                    with open(prv, "w") as f:
                        f.write(keys["private_key"])
                    msg = (f"RSA-2048 key pair generated.\n\n"
                           f"Public key:   {pub}\n"
                           f"Private key:  {prv}\n\n"
                           "Keep the private key secure — never share it.")

                elif algo == "aes":
                    from src.utils import generate_random_key
                    import base64
                    key = generate_random_key(32)
                    key_path = os.path.join(output_dir, "aes_key.bin")
                    with open(key_path, "wb") as f:
                        f.write(key)
                    b64 = base64.b64encode(key).decode()
                    msg = (f"AES-256 key generated.\n\n"
                           f"Key file:  {key_path}\n"
                           f"Base64:    {b64[:48]}…\n\n"
                           "Keep this key secure.")

                self.root.after(0, lambda: messagebox.showinfo("Keys Generated", msg))
                self._status("Keys generated", "ok")
                self.logger.success(f"{algo.upper()} key(s) generated")

            except Exception as exc:
                err = str(exc)
                self.root.after(0, lambda: messagebox.showerror("Key generation failed", err))
                self._status(f"Key generation failed: {exc}", "error")

        threading.Thread(target=worker, daemon=True).start()

    # ══════════════════════════════════════════════════════════════════
    # STEGANOGRAPHY HANDLERS
    # ══════════════════════════════════════════════════════════════════

    def _stego_file_dialog(self, stego_type: str,
                           title_prefix: str = "Select") -> tuple[str, list]:
        types = {
            "image": ("Image files", "*.png *.bmp"),
            "audio": ("WAV files",   "*.wav"),
            "video": ("Video files", "*.mp4 *.avi"),
        }
        label, pattern = types[stego_type]
        return f"{title_prefix} {label}", [(label, pattern)]

    def _handle_stego_encode(self):
        stego_type = self.stego_type.get()
        title, ftypes = self._stego_file_dialog(stego_type, "Select Cover")
        cover = filedialog.askopenfilename(title=title, filetypes=ftypes)
        if not cover:
            return

        win, body = self._dialog("Hide Message", 580, 500)
        tk.Label(body, text=f"Cover file:  {os.path.basename(cover)}",
                 font=F["small"], bg=C["card"], fg=C["text_dim"]).pack(anchor="w")

        msg_area = self._textarea(body, "Message to hide", height=13)

        def _run():
            message = msg_area.get("1.0", tk.END).strip()
            if not message:
                messagebox.showwarning("Input required",
                                       "Please enter a message to hide.", parent=win)
                return

            ext = {"image": ".png", "audio": ".wav", "video": ".mp4"}[stego_type]
            save_types = {
                "image": [("PNG files", "*.png"), ("BMP files", "*.bmp")],
                "audio": [("WAV files", "*.wav")],
                "video": [("MP4 files", "*.mp4"), ("AVI files", "*.avi")],
            }[stego_type]
            output = filedialog.asksaveasfilename(
                defaultextension=ext, filetypes=save_types, parent=win)
            if not output:
                return

            self._status("Hiding message…", "busy")
            win.config(cursor="watch")

            def worker():
                try:
                    if stego_type == "image":
                        r = ImageSteganography.encode(
                            cover, message, output,
                            compress=self.compress_var.get())
                        info = (f"Message hidden successfully.\n\n"
                                f"Output:     {output}\n"
                                f"Size:       {r['message_size']} bytes\n"
                                f"Compressed: {r['compressed']}")
                    elif stego_type == "audio":
                        r = AudioSteganography.encode(cover, message, output)
                        info = (f"Message hidden successfully.\n\n"
                                f"Output:   {output}\n"
                                f"Duration: {r['audio_duration']:.2f}s")
                    else:
                        r = VideoSteganography.encode(cover, message, output)
                        info = (f"Message hidden successfully.\n\n"
                                f"Output: {output}\n"
                                f"Frames: {r.get('frames_used', 'N/A')}")

                    self._status("Message hidden successfully", "ok")
                    self.logger.success("Stego encode complete")
                    self.root.after(0, lambda: messagebox.showinfo("Success", info, parent=win))
                    self.root.after(0, win.destroy)

                except Exception as exc:
                    err = str(exc)
                    self.root.after(0, lambda: messagebox.showerror("Encoding failed", err, parent=win))
                    self._status(f"Encode failed: {exc}", "error")
                finally:
                    self.root.after(0, lambda: win.config(cursor=""))

            threading.Thread(target=worker, daemon=True).start()

        Btn(body, "📥  Hide Message", color=C["primary"],
            command=_run).pack(anchor="e", pady=(14, 0))

    def _handle_stego_decode(self):
        stego_type = self.stego_type.get()
        title, ftypes = self._stego_file_dialog(stego_type, "Select Stego")
        stego_file = filedialog.askopenfilename(title=title, filetypes=ftypes)
        if not stego_file:
            return

        self._status("Extracting message…", "busy")

        def worker():
            try:
                if stego_type == "image":
                    message = ImageSteganography.decode(
                        stego_file, compressed=self.compress_var.get())
                elif stego_type == "audio":
                    message = AudioSteganography.decode(stego_file)
                else:
                    message = VideoSteganography.decode(stego_file)

                self._status("Message extracted", "ok")
                self.logger.success("Stego decode complete")

                def show():
                    win, body = self._dialog("Extracted Message", 640, 500)
                    tk.Label(body,
                             text=f"Source:  {os.path.basename(stego_file)}",
                             font=F["small"], bg=C["card"], fg=C["text_dim"]).pack(anchor="w")

                    out = self._output(body, "Extracted message", height=15)
                    self._write_output(out, message)

                    def save():
                        path = filedialog.asksaveasfilename(
                            defaultextension=".txt",
                            filetypes=[("Text files", "*.txt")],
                            parent=win,
                        )
                        if path:
                            with open(path, "w", encoding="utf-8") as f:
                                f.write(message)
                            self._status(f"Saved to {os.path.basename(path)}", "ok")

                    Btn(body, "💾  Save to file", color=C["primary"],
                        command=save).pack(anchor="e", pady=(8, 0))

                self.root.after(0, show)

            except Exception as exc:
                err = str(exc)
                self.root.after(0, lambda: messagebox.showerror("Extraction failed", err))
                self._status(f"Extract failed: {exc}", "error")

        threading.Thread(target=worker, daemon=True).start()

    def _handle_check_capacity(self):
        stego_type = self.stego_type.get()
        title, ftypes = self._stego_file_dialog(stego_type, "Select")
        file_path = filedialog.askopenfilename(title=title, filetypes=ftypes)
        if not file_path:
            return

        self._status("Checking capacity…", "busy")

        def worker():
            try:
                if stego_type == "image":
                    c = ImageSteganography.get_capacity(file_path)
                    info = (f"File:          {os.path.basename(file_path)}\n\n"
                            f"Dimensions:    {c['image_size']}\n"
                            f"Total pixels:  {c['total_pixels']:,}\n"
                            f"Max bytes:     {c['max_bytes']:,}\n"
                            f"Max chars:     ~{c['max_chars_approx']:,}")
                elif stego_type == "audio":
                    c = AudioSteganography.get_capacity(file_path)
                    info = (f"File:         {os.path.basename(file_path)}\n\n"
                            f"Channels:     {c['channels']}\n"
                            f"Sample rate:  {c['frame_rate']} Hz\n"
                            f"Duration:     {c['duration_seconds']:.2f}s\n"
                            f"Max bytes:    {c['max_bytes']:,}\n"
                            f"Max chars:    ~{c['max_chars_approx']:,}")
                else:
                    c = VideoSteganography.get_capacity(file_path)
                    frames = c.get("total_frames", 0)
                    info = (f"File:        {os.path.basename(file_path)}\n\n"
                            f"Resolution:  {c.get('resolution', 'N/A')}\n"
                            f"Frames:      {frames:,}\n"
                            f"Max bytes:   {c.get('max_bytes', 'N/A'):,}\n"
                            f"Max chars:   ~{c.get('max_chars_approx', 'N/A'):,}")

                self.root.after(0, lambda: messagebox.showinfo("Capacity", info))
                self._status("Capacity check done", "ok")

            except Exception as exc:
                err = str(exc)
                self.root.after(0, lambda: messagebox.showerror("Error", err))
                self._status(f"Capacity check failed: {exc}", "error")

        threading.Thread(target=worker, daemon=True).start()

    # ══════════════════════════════════════════════════════════════════
    # TOOLS HANDLERS
    # ══════════════════════════════════════════════════════════════════

    def _handle_pwd_gen(self):
        win, body = self._dialog("Password Generator", 490, 370)

        tk.Label(body, text="Length", font=F["small"],
                 bg=C["card"], fg=C["text_mid"]).pack(anchor="w", pady=(0, 4))
        length_var = tk.IntVar(value=16)
        scale_row = tk.Frame(body, bg=C["card"])
        scale_row.pack(fill=tk.X)
        tk.Scale(scale_row, from_=8, to=64, orient=tk.HORIZONTAL,
                 variable=length_var, length=300,
                 bg=C["card"], fg=C["text"], highlightthickness=0,
                 troughcolor=C["border"],
                 activebackground=C["primary"]).pack(side=tk.LEFT)
        tk.Label(scale_row, textvariable=length_var, font=F["heading"],
                 bg=C["card"], fg=C["primary"], width=3).pack(side=tk.LEFT, padx=8)

        tk.Label(body, text="Generated password", font=F["small"],
                 bg=C["card"], fg=C["text_mid"]).pack(anchor="w", pady=(14, 4))
        pw_entry = tk.Entry(body, font=("Consolas", 14), width=34,
                            relief=tk.FLAT,
                            highlightbackground=C["border"], highlightthickness=1,
                            bg="#f8fafc", justify="center")
        pw_entry.pack()

        strength_lbl = tk.Label(body, text="", font=F["small"],
                                bg=C["card"], fg=C["text_dim"])
        strength_lbl.pack(anchor="w", pady=(4, 0))

        def _generate():
            pw = PasswordValidator.generate_strong_password(length_var.get())
            pw_entry.delete(0, tk.END)
            pw_entry.insert(0, pw)
            r = PasswordValidator.validate_strength(pw)
            clr = {
                "Strong": C["success"],
                "Medium": C["warning"],
            }.get(r["strength"], C["warning"])
            strength_lbl.config(
                text=f"Strength: {r['strength']}   Score: {r['score']}/8",
                fg=clr)
            self._status("Password generated", "ok")

        def _copy():
            pw = pw_entry.get()
            if pw:
                win.clipboard_clear()
                win.clipboard_append(pw)
                self._status("Password copied to clipboard", "ok")

        btn_row = tk.Frame(body, bg=C["card"])
        btn_row.pack(anchor="w", pady=14)
        Btn(btn_row, "🔄  Generate", color=C["success"], command=_generate).pack(side=tk.LEFT, padx=(0, 8))
        Btn(btn_row, "📋  Copy",     color=C["primary"], command=_copy).pack(side=tk.LEFT)

        _generate()  # auto-generate on open

    def _handle_pwd_val(self):
        win, body = self._dialog("Password Validator", 500, 450)

        pw_entry = self._field(body, "Enter password to validate", show="*", width=36)

        show_var = tk.BooleanVar()
        ttk.Checkbutton(body, text="Show password", variable=show_var,
                        command=lambda: pw_entry.config(
                            show="" if show_var.get() else "*"
                        )).pack(anchor="w", pady=(4, 0))

        result_text = scrolledtext.ScrolledText(
            body, height=11, font=F["body"],
            relief=tk.FLAT,
            highlightbackground=C["border"], highlightthickness=1,
            bg="#f8fafc", state=tk.DISABLED,
        )
        result_text.pack(fill=tk.X, pady=(14, 0))

        def _validate():
            pw = pw_entry.get()
            if not pw:
                messagebox.showwarning("Input required",
                                       "Please enter a password.", parent=win)
                return
            r = PasswordValidator.validate_strength(pw)
            sym = {"Strong": "✅", "Medium": "⚠️"}.get(r["strength"], "❌")
            lines = [
                f"{sym}  Strength: {r['strength']}",
                f"Score:    {r['score']}/8",
                f"Valid:    {'Yes' if r['valid'] else 'No'}",
                "",
            ]
            if r["feedback"]:
                lines.append("Recommendations:")
                lines += [f"  • {fb}" for fb in r["feedback"]]
            else:
                lines.append("No issues found — excellent password!")

            result_text.config(state=tk.NORMAL)
            result_text.delete("1.0", tk.END)
            result_text.insert("1.0", "\n".join(lines))
            result_text.config(state=tk.DISABLED)
            self._status("Password validated", "ok")

        Btn(body, "✅  Validate", color=C["success"],
            command=_validate).pack(anchor="e", pady=(10, 0))

    def _handle_file_hash(self):
        file_path = filedialog.askopenfilename(title="Select file to hash")
        if not file_path:
            return

        win, body = self._dialog("File Hash Calculator", 610, 400)
        tk.Label(body, text=f"File:  {os.path.basename(file_path)}",
                 font=F["body"], bg=C["card"], fg=C["text_mid"]).pack(anchor="w")

        hash_algo = tk.StringVar(value="sha256")
        algo_row = tk.Frame(body, bg=C["card"])
        algo_row.pack(anchor="w", pady=10)
        tk.Label(algo_row, text="Algorithm:", font=F["small"],
                 bg=C["card"], fg=C["text_mid"]).pack(side=tk.LEFT, padx=(0, 8))
        for val, lbl in [("md5", "MD5"), ("sha1", "SHA-1"),
                         ("sha256", "SHA-256"), ("sha512", "SHA-512")]:
            ttk.Radiobutton(algo_row, text=lbl, variable=hash_algo,
                            value=val).pack(side=tk.LEFT, padx=4)

        output = self._output(body, "Hash value", height=5)

        def _calc():
            self._status("Calculating hash…", "busy")
            win.config(cursor="watch")

            def worker():
                try:
                    h = calculate_file_hash(file_path, hash_algo.get())
                    content = f"Algorithm:  {hash_algo.get().upper()}\n\n{h}"
                    self._write_output(output, content)
                    self._status(f"{hash_algo.get().upper()} hash calculated", "ok")
                    self.logger.success(f"Hash: {hash_algo.get().upper()}")
                except Exception as exc:
                    err = str(exc)
                    self.root.after(0, lambda: messagebox.showerror("Error", err, parent=win))
                    self._status(f"Hash failed: {exc}", "error")
                finally:
                    self.root.after(0, lambda: win.config(cursor=""))

            threading.Thread(target=worker, daemon=True).start()

        Btn(body, "#  Calculate Hash", color=C["warning"],
            command=_calc).pack(anchor="e", pady=(12, 0))

    def _handle_verify(self):
        file_path = filedialog.askopenfilename(title="Select file to verify")
        if not file_path:
            return

        win, body = self._dialog("Verify File Integrity", 530, 340)
        tk.Label(body, text=f"File:  {os.path.basename(file_path)}",
                 font=F["body"], bg=C["card"], fg=C["text_mid"]).pack(anchor="w", pady=(0, 6))

        expected_entry = self._field(body, "Expected hash value", width=52)

        hash_algo = tk.StringVar(value="sha256")
        algo_row = tk.Frame(body, bg=C["card"])
        algo_row.pack(anchor="w", pady=8)
        tk.Label(algo_row, text="Algorithm:", font=F["small"],
                 bg=C["card"], fg=C["text_mid"]).pack(side=tk.LEFT, padx=(0, 8))
        for val, lbl in [("sha256", "SHA-256"), ("sha512", "SHA-512"),
                         ("sha1", "SHA-1"), ("md5", "MD5")]:
            ttk.Radiobutton(algo_row, text=lbl, variable=hash_algo,
                            value=val).pack(side=tk.LEFT, padx=4)

        def _verify():
            expected = expected_entry.get().strip()
            if not expected:
                messagebox.showwarning("Input required",
                                       "Please enter the expected hash.", parent=win)
                return

            self._status("Verifying integrity…", "busy")
            win.config(cursor="watch")

            def worker():
                try:
                    from src.utils import verify_file_integrity
                    ok = verify_file_integrity(file_path, expected, hash_algo.get())
                    if ok:
                        self.root.after(0, lambda: messagebox.showinfo(
                            "✅ Verification Passed",
                            "File integrity verified.\n\n"
                            "The file matches the expected hash and has not been tampered with.",
                            parent=win))
                        self._status("Integrity verified — file is intact", "ok")
                        self.root.after(0, win.destroy)
                    else:
                        self.root.after(0, lambda: messagebox.showwarning(
                            "❌ Verification Failed",
                            "Hash mismatch!\n\n"
                            "The file does not match the expected hash.\n"
                            "It may have been modified or corrupted.",
                            parent=win))
                        self._status("Integrity check failed — hash mismatch", "error")
                    self.logger.success(f"Integrity check: {'PASS' if ok else 'FAIL'}")
                except Exception as exc:
                    err = str(exc)
                    self.root.after(0, lambda: messagebox.showerror("Error", err, parent=win))
                    self._status(f"Verify failed: {exc}", "error")
                finally:
                    self.root.after(0, lambda: win.config(cursor=""))

            threading.Thread(target=worker, daemon=True).start()

        Btn(body, "🔍  Verify", color=C["success"],
            command=_verify).pack(anchor="e", pady=(14, 0))

    def _handle_docs(self):
        docs_path = os.path.normpath(
            os.path.join(os.path.dirname(__file__), "..", "docs", "USAGE.md"))
        if not os.path.exists(docs_path):
            messagebox.showinfo("Documentation",
                                "docs/USAGE.md not found.\n"
                                "See the GitHub repository for usage instructions.")
            return

        win, body = self._dialog("Documentation", 840, 620)
        text = scrolledtext.ScrolledText(body, font=("Consolas", 10),
                                         wrap=tk.WORD, relief=tk.FLAT,
                                         highlightbackground=C["border"],
                                         highlightthickness=1,
                                         bg="#f8fafc")
        text.pack(fill=tk.BOTH, expand=True)
        with open(docs_path, encoding="utf-8", errors="replace") as f:
            text.insert("1.0", f.read())
        text.config(state=tk.DISABLED)


# ── Entry point ────────────────────────────────────────────────────────────────

def main():
    root = tk.Tk()
    SecureCipherStegnoApp(root)
    root.mainloop()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as exc:
        print(f"Fatal error: {exc}", file=sys.stderr)
        sys.exit(1)
