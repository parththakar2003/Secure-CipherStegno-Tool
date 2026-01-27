# 🚀 Quick Deploy Guide

## Deploy in 5 Minutes!

This is the fastest way to get your Secure CipherStegno Tool web interface online.

### Option 1: Railway (Recommended - Easiest!) ⚡

**Why Railway?**
- ✅ Free tier with generous limits
- ✅ Automatic HTTPS
- ✅ Zero configuration needed
- ✅ Deploys in ~3 minutes

**Steps:**

1. **Fork this repository**
   - Click the "Fork" button at the top of this page
   - This creates your own copy of the repository

2. **Sign up for Railway**
   - Go to [railway.app](https://railway.app)
   - Click "Login with GitHub"
   - Authorize Railway to access your GitHub

3. **Create new project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your forked `Secure-CipherStegno-Tool` repository

4. **Done!** 🎉
   - Railway automatically detects the `railway.json` configuration
   - Your app will build and deploy automatically
   - You'll get a public URL like: `https://your-app.railway.app`

**Total time: ~5 minutes**

---

### Option 2: Render 🌐

**Steps:**

1. Fork this repository
2. Sign up at [render.com](https://render.com)
3. Click "New +" → "Web Service"
4. Connect your forked GitHub repository
5. Render auto-detects `render.yaml` and deploys!

**Total time: ~10 minutes**

---

### Option 3: Docker 🐳

**For self-hosting on your own server:**

```bash
# Clone the repository
git clone https://github.com/YOUR-USERNAME/Secure-CipherStegno-Tool.git
cd Secure-CipherStegno-Tool

# Build the image
docker build -t secure-cipherstegno-tool .

# Run the container
docker run -d -p 8000:8000 secure-cipherstegno-tool

# Access at http://localhost:8000
```

---

## After Deployment

Once deployed, your web interface will be accessible at your platform's URL. You can:

1. ✅ Encrypt/decrypt messages with various algorithms
2. ✅ Hide messages in images and audio files
3. ✅ Use security tools (password validator, generator, hash calculator)
4. ✅ Access API documentation at `/api/docs`

---

## Security Configuration

### Important: Update these before deploying to production!

1. **CORS Settings** - Add your domain:
   ```bash
   # On Railway/Render, add environment variable:
   ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
   ```

2. **Change Demo Credentials** - See `src/web/api.py` around line 336
   - Replace with proper authentication system
   - Don't use demo/demo123 in production!

---

## Need Help?

- 📖 Full deployment guide: [DEPLOYMENT.md](DEPLOYMENT.md)
- 🐛 Issues: [GitHub Issues](https://github.com/parththakar2003/Secure-CipherStegno-Tool/issues)
- 📧 Email: parththakar2003@gmail.com

---

**Ready to deploy? Choose your platform above and get started! 🚀**
