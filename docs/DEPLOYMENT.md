# GeoMask Deployment Guide

## Overview

This guide covers deploying GeoMask in various environments, from local development to production.

## Prerequisites

- Python 3.8+
- Node.js 16+ (for frontend)
- Docker (optional)
- OpenAI API key

## Local Development

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/makalin/GeoMask.git
   cd GeoMask
   ```

2. **Run the startup script:**
   ```bash
   chmod +x scripts/start.sh
   ./scripts/start.sh
   ```

   This script will:
   - Create a virtual environment
   - Install dependencies
   - Set up configuration
   - Start both backend and frontend

### Manual Setup

1. **Backend Setup:**
   ```bash
   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Create directories
   mkdir -p uploads processed output temp logs
   
   # Copy environment file
   cp env.example .env
   # Edit .env with your API keys
   
   # Start backend
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

2. **Frontend Setup:**
   ```bash
   cd frontend
   npm install
   npm start
   ```

### Using Makefile

```bash
# Install dependencies
make install

# Run backend only
make run-backend

# Run frontend only
make run-frontend

# Run tests
make test

# Format code
make format

# Clean up
make clean
```

## Docker Deployment

### Using Docker Compose (Recommended)

1. **Build and run:**
   ```bash
   docker-compose up -d
   ```

2. **View logs:**
   ```bash
   docker-compose logs -f
   ```

3. **Stop services:**
   ```bash
   docker-compose down
   ```

### Manual Docker

1. **Build image:**
   ```bash
   docker build -t geomask .
   ```

2. **Run container:**
   ```bash
   docker run -p 8000:8000 \
     -e OPENAI_API_KEY=your_api_key \
     -v $(pwd)/uploads:/app/uploads \
     -v $(pwd)/processed:/app/processed \
     geomask
   ```

## Production Deployment

### Environment Variables

Create a `.env` file with production settings:

```bash
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
OPENAI_API_KEY=your_openai_api_key
SECRET_KEY=your-secure-secret-key
ALLOWED_ORIGINS=["https://yourdomain.com"]
MAX_FILE_SIZE=10485760
```

### Using Gunicorn (Production)

1. **Install Gunicorn:**
   ```bash
   pip install gunicorn
   ```

2. **Create Gunicorn config (`gunicorn.conf.py`):**
   ```python
   bind = "0.0.0.0:8000"
   workers = 4
   worker_class = "uvicorn.workers.UvicornWorker"
   timeout = 120
   keepalive = 2
   max_requests = 1000
   max_requests_jitter = 100
   ```

3. **Start with Gunicorn:**
   ```bash
   gunicorn app.main:app -c gunicorn.conf.py
   ```

### Using Systemd (Linux)

1. **Create service file (`/etc/systemd/system/geomask.service`):**
   ```ini
   [Unit]
   Description=GeoMask API
   After=network.target

   [Service]
   Type=exec
   User=geomask
   WorkingDirectory=/opt/geomask
   Environment=PATH=/opt/geomask/venv/bin
   ExecStart=/opt/geomask/venv/bin/gunicorn app.main:app -c gunicorn.conf.py
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```

2. **Enable and start service:**
   ```bash
   sudo systemctl enable geomask
   sudo systemctl start geomask
   sudo systemctl status geomask
   ```

### Using Nginx (Reverse Proxy)

1. **Install Nginx:**
   ```bash
   sudo apt update
   sudo apt install nginx
   ```

2. **Create Nginx config (`/etc/nginx/sites-available/geomask`):**
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }

       location /static/ {
           alias /opt/geomask/static/;
       }

       client_max_body_size 10M;
   }
   ```

3. **Enable site:**
   ```bash
   sudo ln -s /etc/nginx/sites-available/geomask /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl reload nginx
   ```

### Using SSL with Let's Encrypt

1. **Install Certbot:**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   ```

2. **Obtain SSL certificate:**
   ```bash
   sudo certbot --nginx -d yourdomain.com
   ```

3. **Auto-renewal:**
   ```bash
   sudo crontab -e
   # Add: 0 12 * * * /usr/bin/certbot renew --quiet
   ```

## Cloud Deployment

### Heroku

1. **Create `Procfile`:**
   ```
   web: gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

2. **Create `runtime.txt`:**
   ```
   python-3.11.0
   ```

3. **Deploy:**
   ```bash
   heroku create your-geomask-app
   heroku config:set OPENAI_API_KEY=your_api_key
   heroku config:set ENVIRONMENT=production
   git push heroku main
   ```

### AWS EC2

1. **Launch EC2 instance:**
   ```bash
   # Connect to instance
   ssh -i your-key.pem ubuntu@your-instance-ip
   
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install dependencies
   sudo apt install python3-pip python3-venv nginx git
   ```

2. **Deploy application:**
   ```bash
   # Clone repository
   git clone https://github.com/makalin/GeoMask.git
   cd GeoMask
   
   # Setup application
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install gunicorn
   
   # Configure environment
   cp env.example .env
   # Edit .env with production settings
   ```

3. **Setup systemd service (see above)**

4. **Configure Nginx (see above)**

### Google Cloud Run

1. **Create `Dockerfile.prod`:**
   ```dockerfile
   FROM python:3.11-slim
   
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   
   COPY . .
   RUN mkdir -p uploads processed output temp logs
   
   EXPOSE 8080
   CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
   ```

2. **Deploy:**
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT_ID/geomask
   gcloud run deploy geomask \
     --image gcr.io/PROJECT_ID/geomask \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars OPENAI_API_KEY=your_api_key
   ```

## Monitoring and Logging

### Application Logs

Logs are written to the `logs/` directory:
- `geomask_YYYYMMDD.log`: General application logs
- `geomask_errors_YYYYMMDD.log`: Error logs only

### Health Checks

Monitor the health endpoint:
```bash
curl http://yourdomain.com/health
```

### Performance Monitoring

Consider using:
- **Prometheus + Grafana** for metrics
- **Sentry** for error tracking
- **Log aggregation** (ELK stack, Fluentd)

## Security Considerations

### Environment Variables
- Never commit API keys to version control
- Use secure secret management (AWS Secrets Manager, HashiCorp Vault)
- Rotate keys regularly

### File Upload Security
- Validate file types and sizes
- Scan uploaded files for malware
- Use secure file storage (S3, GCS)

### Network Security
- Use HTTPS in production
- Configure firewall rules
- Implement rate limiting
- Use WAF for additional protection

### Application Security
- Keep dependencies updated
- Use security headers
- Implement proper CORS policies
- Regular security audits

## Troubleshooting

### Common Issues

1. **Port already in use:**
   ```bash
   lsof -i :8000
   kill -9 <PID>
   ```

2. **Permission denied:**
   ```bash
   chmod +x scripts/start.sh
   sudo chown -R $USER:$USER uploads/ processed/
   ```

3. **Memory issues:**
   - Reduce number of workers
   - Increase swap space
   - Optimize image processing

4. **API key issues:**
   - Verify API key is correct
   - Check API quota limits
   - Ensure proper environment variable format

### Debug Mode

Enable debug mode for troubleshooting:
```bash
export DEBUG=true
export LOG_LEVEL=DEBUG
```

### Log Analysis

```bash
# View recent logs
tail -f logs/geomask_$(date +%Y%m%d).log

# Search for errors
grep ERROR logs/geomask_*.log

# Monitor API requests
grep "POST /api/process" logs/geomask_*.log
```

## Support

For deployment issues:
- GitHub Issues: https://github.com/makalin/GeoMask/issues
- Documentation: https://github.com/makalin/GeoMask/docs
