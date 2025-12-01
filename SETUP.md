# Detailed Setup Guide for FinSight Pro

This guide provides step-by-step instructions for setting up FinSight Pro in various environments.

## 📋 Table of Contents

- [Local Development Setup](#local-development-setup)
- [Production Deployment](#production-deployment)
- [Docker Setup](#docker-setup)
- [Streamlit Cloud Deployment](#streamlit-cloud-deployment)
- [Troubleshooting](#troubleshooting)

## 🖥️ Local Development Setup

### Prerequisites Check

```bash
# Check Python version (need 3.8+)
python --version

# Check pip version
pip --version

# Check Git (optional, for cloning)
git --version
```

### Step 1: Clone Repository

```bash
# Clone using HTTPS
git clone https://github.com/manavagarwal123/FinSightPro.git

# Or clone using SSH
git clone git@github.com:manavagarwal123/FinSightPro.git

# Navigate to directory
cd FinSightPro
```

### Step 2: Create Virtual Environment

**Why use a virtual environment?**
- Isolates project dependencies
- Prevents conflicts with system packages
- Ensures consistent environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment

# On Windows (Command Prompt):
venv\Scripts\activate.bat

# On Windows (PowerShell):
venv\Scripts\Activate.ps1

# On macOS/Linux:
source venv/bin/activate

# Verify activation (should show (venv) prefix)
which python  # Should point to venv/bin/python
```

### Step 3: Install Dependencies

```bash
# Upgrade pip first
pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt

# Verify installation
pip list
```

### Step 4: Verify Installation

```bash
# Test imports
python -c "import streamlit; print('Streamlit:', streamlit.__version__)"
python -c "import pandas; print('Pandas:', pandas.__version__)"
python -c "import plotly; print('Plotly:', plotly.__version__)"
python -c "import sklearn; print('scikit-learn:', sklearn.__version__)"
```

### Step 5: Run Application

```bash
# Basic run
streamlit run app.py

# Run with auto-reload (development mode)
streamlit run app.py --server.runOnSave true

# Run on custom port
streamlit run app.py --server.port 8502

# Run with custom config
streamlit run app.py --server.headless true
```

The app will open automatically at `http://localhost:8501`

## 🚀 Production Deployment

### Option 1: Traditional Server (Linux)

#### Using systemd

1. Create service file:
```bash
sudo nano /etc/systemd/system/finsight.service
```

2. Add configuration:
```ini
[Unit]
Description=FinSight Pro Streamlit App
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/FinSightPro
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/streamlit run app.py --server.port 8501 --server.address 0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
```

3. Enable and start service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable finsight
sudo systemctl start finsight
sudo systemctl status finsight
```

#### Using Nginx Reverse Proxy

1. Install Nginx:
```bash
sudo apt-get install nginx
```

2. Create Nginx config:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

3. Enable and restart:
```bash
sudo nginx -t
sudo systemctl restart nginx
```

### Option 2: Docker Deployment

#### Create Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run application
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

#### Build and Run

```bash
# Build image
docker build -t finsight-pro:latest .

# Run container
docker run -d \
  --name finsight-pro \
  -p 8501:8501 \
  finsight-pro:latest

# View logs
docker logs -f finsight-pro

# Stop container
docker stop finsight-pro
```

#### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  finsight:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
    restart: unless-stopped
    environment:
      - STREAMLIT_SERVER_PORT=8501
      - STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

Run:
```bash
docker-compose up -d
```

## ☁️ Streamlit Cloud Deployment

### Step 1: Push to GitHub

```bash
# Ensure all files are committed
git add .
git commit -m "Ready for deployment"
git push origin main
```

### Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select repository: `manavagarwal123/FinSightPro`
5. Branch: `main`
6. Main file path: `app.py`
7. Click "Deploy"

### Step 3: Configure (Optional)

Create `.streamlit/config.toml`:

```toml
[server]
port = 8501
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
```

## 🔧 Troubleshooting

### Virtual Environment Issues

**Problem:** `python: command not found`

**Solution:**
```bash
# Use python3 instead
python3 -m venv venv
python3 -m pip install -r requirements.txt
```

### Permission Errors

**Problem:** Permission denied when installing packages

**Solution:**
```bash
# Don't use sudo with venv
# Ensure venv is activated
source venv/bin/activate
pip install -r requirements.txt
```

### Port Already in Use

**Problem:** Port 8501 is already in use

**Solution:**
```bash
# Find process using port
# Linux/Mac:
lsof -i :8501
kill -9 <PID>

# Windows:
netstat -ano | findstr :8501
taskkill /PID <PID> /F

# Or use different port
streamlit run app.py --server.port 8502
```

### PDF Parsing Issues

**Problem:** pdfplumber installation fails

**Solution:**
```bash
# Install system dependencies first
# Ubuntu/Debian:
sudo apt-get install python3-dev libffi-dev

# macOS:
brew install python3

# Then reinstall
pip install pdfplumber --upgrade
```

### Memory Issues

**Problem:** App crashes with large files

**Solution:**
- Increase system RAM
- Process files in smaller chunks
- Use data filtering before processing
- Consider using a more powerful server

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Plotly Documentation](https://plotly.com/python/)
- [scikit-learn Documentation](https://scikit-learn.org/stable/)

---

For more help, open an issue on [GitHub](https://github.com/manavagarwal123/FinSightPro/issues).

