# 🚀 Interactive CLI Quick Start

## Welcome to the Interactive CLI!

This guide will get you started with the **user-friendly, menu-based CLI** - no commands to type, just select options!

---

## 🎯 Why Use Interactive CLI?

✅ **No commands to memorize** - Everything is menu-driven  
✅ **Visual feedback** - Colors, animations, and clear messages  
✅ **Built-in help** - Guides and tips at every step  
✅ **Beginner-friendly** - Perfect for learning the tool  
✅ **Smart prompts** - Automatic file detection and validation  

---

## 🏃 Getting Started in 3 Steps

### Step 1: Launch the Interactive CLI

```bash
python3 interactive_cli.py
```

You'll see a beautiful ASCII art banner and the main menu!

### Step 2: Navigate with Numbers

Simply enter the number of your choice:

```
🔐 MAIN MENU
══════════════════════════════════════════════════════════════════════
  [1] 🔐 Cryptography - Encrypt & Decrypt
  [2] 🖼️  Steganography - Hide & Extract Messages
  [3] 🛠️  Security Tools - Password, Hash, Analysis
  [4] ℹ️  Help & Information
  [5] ❌ Exit
══════════════════════════════════════════════════════════════════════

Select an option (1-5): 
```

Just type `1` and press Enter to go to Cryptography!

### Step 3: Follow the Prompts

The CLI will guide you through each step:
- Clear descriptions of what each option does
- Helpful tips and warnings when needed
- Smart file detection (works with paths or text)
- Option to save results to files
- Easy back navigation

---

## 📚 Quick Tutorials

### 🔒 Tutorial 1: Encrypt a Message (Beginner)

**Goal:** Encrypt a secret message using AES-256

1. Start interactive CLI: `python3 interactive_cli.py`
2. Select `[1] Cryptography`
3. Select `[1] Encrypt Message`
4. Select `[6] AES-256 (Recommended)`
5. Enter your message: `This is my secret!`
6. Enter a password: `MyStrong@Pass123`
7. Save the file as: `encrypted.json`
8. Done! Your message is encrypted ✅

**What you learned:** AES-256 encryption with password

---

### 🖼️ Tutorial 2: Hide a Message in an Image

**Goal:** Hide a secret message inside an image

1. Start interactive CLI: `python3 interactive_cli.py`
2. Select `[2] Steganography`
3. Select `[1] Hide Message in Image`
4. Enter cover image path: `photo.png` (you need an existing PNG image)
5. Enter your secret message: `Hidden message!`
6. Save output as: `stego.png`
7. Enable compression: `y`
8. Done! Your message is hidden in the image ✅

**What you learned:** Image steganography (LSB technique)

---

### 🔓 Tutorial 3: Decrypt a Message

**Goal:** Decrypt the message you encrypted in Tutorial 1

1. Start interactive CLI: `python3 interactive_cli.py`
2. Select `[1] Cryptography`
3. Select `[2] Decrypt Message`
4. Select `[6] AES-256 (Recommended)`
5. Enter encrypted file path: `encrypted.json`
6. Enter the password: `MyStrong@Pass123` (same as encryption)
7. Save decrypted message: `decrypted.txt`
8. Done! Your message is decrypted ✅

**What you learned:** AES-256 decryption

---

### 🔑 Tutorial 4: Generate a Strong Password

**Goal:** Create a secure password

1. Start interactive CLI: `python3 interactive_cli.py`
2. Select `[3] Security Tools`
3. Select `[1] Generate Strong Password`
4. Enter length: `20`
5. Copy the generated password ✅
6. Tool shows strength analysis automatically

**What you learned:** Password generation and validation

---

## 💡 Pro Tips

### Tip 1: File Paths vs Direct Input
When asked for a message, you can:
- Type directly: `Hello World`
- Or provide a file path: `message.txt`

The CLI automatically detects which one you mean!

### Tip 2: Use Help System
Don't know what an algorithm does?
- Select `[4] Help & Information` from main menu
- Choose topics like "Cryptography Basics" or "Getting Started"
- Comprehensive guides built right in!

### Tip 3: Combine Encryption + Steganography
For maximum security:

1. **First:** Encrypt your message with AES-256
2. **Then:** Hide the encrypted file in an image
3. **Result:** Even if someone finds the image, they can't read it without the password!

Example workflow:
```
1. Encrypt message → saves to encrypted.json
2. Hide encrypted.json in photo.png → saves to stego.png
3. Share stego.png (looks like a normal photo!)
```

### Tip 4: Remember Your Settings
When hiding messages:
- ✅ Remember if you used compression
- ✅ Keep track of passwords (use password manager!)
- ✅ Save encryption keys securely
- ✅ Note which algorithm you used

### Tip 5: Test First!
Before encrypting important data:
- Test with a simple message
- Verify you can decrypt it
- Practice the workflow
- Then use with real data

---

## 🎨 Interface Features

### Colors and Icons
- 🟢 **Green** = Success
- 🔴 **Red** = Error
- 🟡 **Yellow** = Warning/Information
- 🔵 **Cyan** = Prompts and menus

### Animations
- Spinning loaders while processing
- Progress bars for operations
- Smooth transitions between menus

### Smart Validation
- Invalid input? Get helpful error message
- File not found? Clear explanation
- Wrong password? Suggestions provided

---

## 🆚 Interactive CLI vs Traditional CLI

### When to Use Interactive CLI:
- ✅ Learning the tool for the first time
- ✅ Occasional use / ad-hoc operations
- ✅ Want visual feedback and guidance
- ✅ Prefer menu navigation over commands
- ✅ Don't want to remember command syntax

### When to Use Traditional CLI:
- ✅ Automating workflows with scripts
- ✅ Batch processing many files
- ✅ Integration with other tools
- ✅ Remote operations via SSH
- ✅ CI/CD pipelines

**Both CLIs use the same underlying code - same security, same results!**

---

## 📖 Common Workflows

### Workflow 1: Secure File Transfer
```
Goal: Send an encrypted file to someone

1. Interactive CLI → Cryptography → Encrypt
2. Choose RSA (for sharing) or AES (with shared password)
3. If RSA: Generate key pair → Share public key
4. Encrypt your file with recipient's public key
5. Send encrypted file (recipient decrypts with private key)
```

### Workflow 2: Secret Image Sharing
```
Goal: Hide a message in a photo

1. Optional: First encrypt the message
2. Interactive CLI → Steganography → Hide in Image
3. Choose cover image (larger = more capacity)
4. Enter message (or encrypted file path)
5. Enable compression for larger messages
6. Share the stego image (looks normal!)
```

### Workflow 3: Password Creation
```
Goal: Create secure passwords for accounts

1. Interactive CLI → Security Tools → Generate Password
2. Choose length (16-24 recommended)
3. Copy the generated password
4. Store in password manager
5. Use validate password to check strength
```

---

## ❓ FAQ

**Q: Can I go back if I make a mistake?**  
A: Yes! Most menus have a "Back" option. Or press Ctrl+C to cancel current operation.

**Q: What if I don't have a file, just text?**  
A: Just type your text directly when prompted for input!

**Q: Do I need to install anything extra?**  
A: No! If `python3 interactive_cli.py` runs, you have everything you need.

**Q: Is my data secure?**  
A: Yes! Everything runs locally on your machine. No cloud, no tracking, no data sent anywhere.

**Q: Can I use this for real sensitive data?**  
A: Yes! The tool uses industry-standard algorithms (AES-256, RSA-2048) that are used by banks and governments.

**Q: What if I forget my password?**  
A: Unfortunately, there's no recovery. That's why encryption is secure! Always backup passwords in a secure location.

**Q: Can I automate tasks with Interactive CLI?**  
A: No, Interactive CLI is for manual use. For automation, use the Traditional CLI (see CLI_GUIDE.md).

---

## 🚨 Common Mistakes to Avoid

❌ **Mistake 1:** Losing passwords/keys  
✅ **Solution:** Use a password manager, keep backups

❌ **Mistake 2:** Using JPEG for steganography  
✅ **Solution:** Use PNG or BMP (lossless formats)

❌ **Mistake 3:** Forgetting compression setting  
✅ **Solution:** Name files descriptively: `stego_compressed.png`

❌ **Mistake 4:** Weak passwords  
✅ **Solution:** Use password generator, minimum 12 characters

❌ **Mistake 5:** Sharing private keys  
✅ **Solution:** Only share public keys, keep private keys secret!

---

## 🎓 Next Steps

### After This Guide:
1. ✅ Try all the tutorials above
2. ✅ Explore the Help menu in the interactive CLI
3. ✅ Experiment with different algorithms
4. ✅ Read [CLI_GUIDE.md](CLI_GUIDE.md) for traditional CLI
5. ✅ Check [README.md](README.md) for complete documentation

### Learning Path:
1. **Beginner:** Start with Caesar cipher and simple text
2. **Intermediate:** Use AES-256 encryption with files
3. **Advanced:** Combine RSA + AES hybrid encryption
4. **Expert:** Use steganography + encryption together

---

## 🆘 Getting Help

- **Built-in Help:** Select `[4] Help & Information` in the main menu
- **Full Documentation:** See [CLI_GUIDE.md](CLI_GUIDE.md) and [README.md](README.md)
- **Issues:** Report at [GitHub Issues](https://github.com/parththakar2003/Secure-CipherStegno-Tool/issues)

---

## 🎉 You're Ready!

You now know how to use the Interactive CLI! Just remember:

1. 🔢 Select options with numbers
2. 📝 Follow the prompts
3. 💡 Use built-in help when needed
4. ✨ Enjoy the user-friendly experience!

**Launch the CLI and start exploring:**
```bash
python3 interactive_cli.py
```

Happy encrypting! 🔐
