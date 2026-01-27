# Secure CipherStegno Tool - Web Deployment Guide

This guide explains how to deploy the Secure CipherStegno Tool web interface to various hosting platforms.

## 🌐 Available Deployment Options

The web interface can be deployed to multiple platforms. Choose the one that best fits your needs:

| Platform | Free Tier | Ease of Setup | Best For |
|----------|-----------|---------------|----------|
| **Railway** | ✅ Yes | ⭐⭐⭐⭐⭐ Very Easy | Quick deployment, Docker support |
| **Render** | ✅ Yes | ⭐⭐⭐⭐ Easy | Reliable hosting, automatic deploys |
| **Docker** | N/A | ⭐⭐⭐ Moderate | Self-hosting, full control |
| **Vercel** | ✅ Yes | ⭐⭐⭐ Moderate | Serverless, global CDN |
| **Heroku** | ⚠️ Limited | ⭐⭐⭐⭐ Easy | Traditional PaaS (requires credit card) |

---

## 📋 Pre-Deployment Checklist

Before deploying, ensure:

1. ✅ You have a GitHub account and the repository is pushed to GitHub
2. ✅ All dependencies are listed in `requirements.txt`
3. ✅ The web interface works locally (`python apps/launch.py web`)
4. ✅ You've reviewed the security settings in `src/web/api.py`

---

## 🚀 Deployment Instructions

### Option 1: Railway (Recommended - Easiest)

Railway offers the simplest deployment with excellent free tier support.

**Steps:**

1. **Sign up** at [railway.app](https://railway.app) (use GitHub account)

2. **Create a new project:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your `Secure-CipherStegno-Tool` repository

3. **Configure the deployment:**
   - Railway will automatically detect the `railway.json` configuration
   - No additional configuration needed!

4. **Deploy:**
   - Click "Deploy"
   - Railway will build and deploy your application
   - You'll receive a public URL like `https://your-app.railway.app`

5. **Access your app:**
   - Visit the provided URL
   - Your web interface is now live!

**Environment Variables (Optional):**
- `PORT` - Automatically set by Railway
- `PYTHON_VERSION` - Set to `3.11.0`

---

### Option 2: Render

Render provides reliable hosting with automatic deploys from GitHub.

**Steps:**

1. **Sign up** at [render.com](https://render.com)

2. **Create a new Web Service:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the `Secure-CipherStegno-Tool` repository

3. **Configure the service:**
   - **Name:** `secure-cipherstegno-tool`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn src.web.api:app --host 0.0.0.0 --port $PORT`
   - **Plan:** Free

4. **Deploy:**
   - Click "Create Web Service"
   - Render will deploy your application
   - You'll get a URL like `https://secure-cipherstegno-tool.onrender.com`

5. **Configure health check:**
   - Set Health Check Path to `/api/health`

**Note:** Free tier services on Render spin down after inactivity. First request may take 30-60 seconds.

---

### Option 3: Docker (Self-Hosting)

Use Docker for self-hosting or deploying to any cloud provider that supports containers.

**Prerequisites:**
- Docker installed on your system
- Docker Hub account (optional, for pushing images)

**Steps:**

1. **Build the Docker image:**
   ```bash
   cd Secure-CipherStegno-Tool
   docker build -t secure-cipherstegno-tool .
   ```

2. **Run the container locally:**
   ```bash
   docker run -p 8000:8000 secure-cipherstegno-tool
   ```

3. **Access the application:**
   - Open browser to `http://localhost:8000`

4. **Deploy to cloud (optional):**
   
   **For DigitalOcean App Platform:**
   ```bash
   doctl apps create --spec .do/app.yaml
   ```
   
   **For AWS ECS, Azure Container Instances, or Google Cloud Run:**
   - Push image to registry
   - Create container service
   - Configure port 8000
   - Deploy container

**Production Docker Compose:**

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - PORT=8000
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/health"]
      interval: 30s
      timeout: 3s
      retries: 3
```

Run with: `docker-compose up -d`

---

### Option 4: Vercel

Vercel offers serverless deployment with global CDN.

**Steps:**

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel:**
   ```bash
   vercel login
   ```

3. **Deploy:**
   ```bash
   cd Secure-CipherStegno-Tool
   vercel
   ```

4. **Follow the prompts:**
   - Set up and deploy: Yes
   - Scope: Your account
   - Link to existing project: No
   - Project name: secure-cipherstegno-tool
   - Directory: ./
   - Override settings: No

5. **Production deployment:**
   ```bash
   vercel --prod
   ```

**Note:** Vercel's serverless environment has some limitations:
- Cold starts may cause initial delays
- Request/response size limits
- Execution time limits

---

### Option 5: Heroku

Heroku is a traditional PaaS platform (requires credit card for verification).

**Steps:**

1. **Install Heroku CLI:**
   ```bash
   # macOS
   brew install heroku/brew/heroku
   
   # Ubuntu/Debian
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Login to Heroku:**
   ```bash
   heroku login
   ```

3. **Create a new app:**
   ```bash
   cd Secure-CipherStegno-Tool
   heroku create secure-cipherstegno-tool
   ```

4. **Deploy:**
   ```bash
   git push heroku main
   ```

5. **Open your app:**
   ```bash
   heroku open
   ```

**Configuration:**
- The `Procfile` and `runtime.txt` files are already configured
- Heroku will automatically detect Python and install dependencies

---

## 🔒 Security Considerations

### Important Security Updates

Before deploying to production, update these security settings in `src/web/api.py`:

1. **CORS Configuration** (Lines 48-56 in `src/web/api.py`):
   ```python
   # Update allowed origins to your domain
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["https://yourdomain.com"],  # Your production domain
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

2. **OAuth2 Credentials** (See login function around line 336 in `src/web/api.py`):
   - Replace demo credentials with secure authentication
   - Implement proper password hashing
   - Use environment variables for secrets
   - Consider using a proper auth service (Auth0, Firebase, etc.)

3. **Environment Variables:**
   Set these in your deployment platform:
   ```
   SECRET_KEY=your-secret-key-here
   ALLOWED_HOSTS=your-domain.com
   DEBUG=False
   ```

### Recommended Security Practices

- ✅ Use HTTPS only (most platforms provide this by default)
- ✅ Implement rate limiting
- ✅ Add request size limits
- ✅ Use secure session management
- ✅ Regularly update dependencies
- ✅ Monitor logs for suspicious activity
- ✅ Enable CSRF protection
- ✅ Implement proper authentication and authorization

---

## 📊 Monitoring and Maintenance

### Health Check Endpoint

All platforms can use the health check endpoint:
```
GET /api/health
```

This endpoint returns service status and is useful for uptime monitoring.

### Logs

**Railway:**
```bash
railway logs
```

**Render:**
- View logs in the Render dashboard

**Heroku:**
```bash
heroku logs --tail
```

**Docker:**
```bash
docker logs -f <container-id>
```

### Updating Your Deployment

Most platforms support automatic deploys when you push to GitHub:

1. Make your changes locally
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update feature"
   git push origin main
   ```
3. Platform automatically rebuilds and deploys

---

## 🎯 Testing Your Deployment

After deployment, test these key features:

1. ✅ **Home Page:** Visit the root URL
2. ✅ **Encryption:** Test AES-256 encryption/decryption
3. ✅ **API Docs:** Visit `/api/docs` for interactive API documentation
4. ✅ **Health Check:** Visit `/api/health` to verify service status
5. ✅ **Static Files:** Ensure CSS and JavaScript load correctly

---

## 🆘 Troubleshooting

### Common Issues

**Issue:** "Module not found" error
- **Solution:** Ensure all dependencies are in `requirements.txt`
- Run: `pip freeze > requirements.txt`

**Issue:** Static files not loading
- **Solution:** Check static file paths in deployment config
- Verify `src/web/static/` directory exists

**Issue:** Port binding error
- **Solution:** Use `$PORT` environment variable provided by platform
- Don't hardcode port 8000

**Issue:** Build timeout
- **Solution:** Reduce dependencies or upgrade to paid tier
- Remove unused packages from requirements.txt

**Issue:** Application crashes on startup
- **Solution:** Check logs for specific error
- Verify Python version compatibility (3.8+)

### Getting Help

- 📖 Check platform-specific documentation
- 💬 Join [GitHub Discussions](https://github.com/parththakar2003/Secure-CipherStegno-Tool/discussions)
- 🐛 Report issues on [GitHub Issues](https://github.com/parththakar2003/Secure-CipherStegno-Tool/issues)
- 📧 Contact: parththakar2003@gmail.com

---

## 📚 Additional Resources

- [FastAPI Deployment Documentation](https://fastapi.tiangolo.com/deployment/)
- [Uvicorn Deployment](https://www.uvicorn.org/deployment/)
- [Docker Documentation](https://docs.docker.com/)
- [Railway Documentation](https://docs.railway.app/)
- [Render Documentation](https://render.com/docs)

---

## ✨ Next Steps

After successful deployment:

1. 🎨 Customize the web interface branding
2. 🔐 Implement proper authentication
3. 📊 Add analytics (privacy-respecting)
4. 🌍 Set up custom domain
5. 📈 Monitor performance and usage
6. 🔄 Set up CI/CD pipeline
7. 📱 Consider Progressive Web App (PWA) features

---

**Happy Deploying! 🚀**

For more information, see the main [README.md](README.md) and [STRUCTURE.md](STRUCTURE.md).
