# FinTrust Guardian - Deployment Guide

## Overview

This guide covers deploying FinTrust Guardian from development to production, including containerization, security hardening, and monitoring setup.

## Prerequisites

### System Requirements

**Development Environment:**

- Python 3.8+
- Node.js 16+
- 4GB RAM minimum
- 10GB disk space

**Production Environment:**

- Python 3.8+
- Node.js 16+
- 16GB RAM minimum
- 100GB disk space
- SSL certificate
- Domain name

### Required Tools

- Docker & Docker Compose
- Git
- nginx (production)
- PostgreSQL (production)
- Redis (production)

## Local Development Setup

### Quick Start

1. **Clone Repository**

```bash
git clone https://github.com/yourusername/fintrust-guardian.git
cd fintrust-guardian
```

2. **Environment Setup**

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
cd backend
pip install -r requirements.txt

# Install Node.js dependencies
cd ../frontend
npm install
```

3. **Initialize Data**

```bash
# Generate mock data and policies
python scripts/generate_mock_data.py
```

4. **Start Services**

```bash
# Terminal 1: Policy Gateway
cd backend
python app.py

# Terminal 2: Data Vault
cd data-exchange
python server.py

# Terminal 3: Frontend
cd frontend
npm start
```

5. **Verify Installation**

```bash
# Health check
curl http://localhost:5000/health

# Frontend access
open http://localhost:3000
```

### Environment Configuration

Create `.env` files for each component:

**backend/.env**

```bash
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=sqlite:///fintrust.db

# Security
JWT_SECRET_KEY=your-jwt-secret-here
AES_ENCRYPTION_KEY=your-32-byte-key-here

# Socket Server
SOCKET_HOST=localhost
SOCKET_PORT=9999

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=1000

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json
```

**frontend/.env**

```bash
# API Configuration
REACT_APP_API_BASE_URL=http://localhost:5000
REACT_APP_API_VERSION=v1

# Development
REACT_APP_ENV=development
GENERATE_SOURCEMAP=false

# Features
REACT_APP_ENABLE_DEBUG=true
REACT_APP_REFRESH_RATE=5000
```

## Docker Deployment

### Containerization

**Dockerfile.backend**

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ .
COPY data-exchange/ ./data-exchange/

# Create non-root user
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s \
  CMD curl -f http://localhost:5000/health || exit 1

EXPOSE 5000 9999

CMD ["python", "app.py"]
```

**Dockerfile.frontend**

```dockerfile
FROM node:16-alpine as build

WORKDIR /app

# Copy package files
COPY frontend/package*.json ./
RUN npm ci --only=production

# Copy source and build
COPY frontend/ .
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built assets
COPY --from=build /app/build /usr/share/nginx/html

# Copy nginx configuration
COPY docker/nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

**docker-compose.yml**

```yaml
version: "3.8"

services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    ports:
      - "5000:5000"
      - "9999:9999"
    environment:
      - FLASK_ENV=production
      - DATABASE_URL=postgresql://postgres:password@db:5432/fintrust
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    volumes:
      - ./data:/app/data
    restart: unless-stopped

  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "80:80"
    environment:
      - REACT_APP_API_BASE_URL=http://backend:5000
    depends_on:
      - backend
    restart: unless-stopped

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=fintrust
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./scripts/init.sql:/docker-entrypoint-initdb.d/init.sql
    restart: unless-stopped

  redis:
    image: redis:6-alpine
    volumes:
      - redis_data:/data
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "443:443"
    volumes:
      - ./docker/nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - frontend
      - backend
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
```

### Docker Commands

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f backend

# Scale backend service
docker-compose up -d --scale backend=3

# Stop all services
docker-compose down

# Rebuild after changes
docker-compose up -d --build
```

## Production Deployment

### Database Setup

**PostgreSQL Migration**

1. **Install PostgreSQL**

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install postgresql postgresql-contrib

# Create database
sudo -u postgres createdb fintrust
sudo -u postgres createuser --interactive
```

2. **Schema Migration**

```sql
-- Create tables
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(50) UNIQUE NOT NULL,
    encrypted_pii TEXT NOT NULL,
    data_hash VARCHAR(64) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    partner_id VARCHAR(50) NOT NULL,
    user_id VARCHAR(50) NOT NULL,
    purpose VARCHAR(100) NOT NULL,
    status VARCHAR(20) NOT NULL,
    data_accessed TEXT[],
    ip_address INET,
    metadata JSONB
);

CREATE TABLE policies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    partner_id VARCHAR(50) UNIQUE NOT NULL,
    policy_data JSONB NOT NULL,
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indices
CREATE INDEX idx_audit_logs_timestamp ON audit_logs(timestamp);
CREATE INDEX idx_audit_logs_partner ON audit_logs(partner_id);
CREATE INDEX idx_audit_logs_user ON audit_logs(user_id);
```

3. **Update Connection String**

```bash
DATABASE_URL=postgresql://username:password@localhost:5432/fintrust
```

### Reverse Proxy Setup

**nginx Configuration**

```nginx
upstream backend {
    server backend1:5000;
    server backend2:5000;
    server backend3:5000;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;

    # Security headers
    add_header X-Frame-Options DENY;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload";

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req zone=api burst=20 nodelay;

    # API routes
    location /api/ {
        proxy_pass http://backend/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Frontend
    location / {
        root /var/www/html;
        index index.html;
        try_files $uri $uri/ /index.html;

        # Cache static assets
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}
```

### SSL Certificate Setup

**Using Let's Encrypt**

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### Environment Variables (Production)

**Production .env**

```bash
# Flask
FLASK_ENV=production
SECRET_KEY=production-secret-key-64-chars-long
JWT_SECRET_KEY=jwt-production-secret-key-64-chars-long

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/fintrust

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
AES_ENCRYPTION_KEY=32-byte-production-encryption-key
ALLOWED_HOSTS=your-domain.com,api.your-domain.com

# Monitoring
SENTRY_DSN=https://your-sentry-dsn
LOG_LEVEL=WARNING

# Rate Limiting
RATE_LIMIT_PER_MINUTE=30
RATE_LIMIT_PER_HOUR=500
```

## Security Hardening

### Application Security

1. **Input Validation**

```python
# Use marshmallow for input validation
from marshmallow import Schema, fields, validate

class AuthorizeSchema(Schema):
    partner_id = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    user_id = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    purpose = fields.Str(required=True, validate=validate.OneOf(['loan_application', 'credit_check']))
```

2. **SQL Injection Prevention**

```python
# Use parameterized queries
cursor.execute(
    "SELECT * FROM users WHERE user_id = %s AND partner_id = %s",
    (user_id, partner_id)
)
```

3. **XSS Protection**

```python
from markupsafe import escape

# Escape user input
safe_input = escape(user_input)
```

### Infrastructure Security

1. **Firewall Configuration**

```bash
# UFW setup
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

2. **Fail2Ban Setup**

```bash
# Install fail2ban
sudo apt install fail2ban

# Configure jail
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local

# Add custom filter for API abuse
sudo cat > /etc/fail2ban/filter.d/fintrust.conf << EOF
[Definition]
failregex = ^.*"status": "denied".*"ip": "<HOST>".*$
ignoreregex =
EOF
```

3. **Log Monitoring**

```bash
# Install logwatch
sudo apt install logwatch

# Configure for daily reports
sudo crontab -e
# Add: 0 6 * * * /usr/sbin/logwatch --output stdout --format text
```

### Data Protection

1. **Encryption at Rest**

```python
from cryptography.fernet import Fernet

# Generate key
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Encrypt sensitive data
encrypted_data = cipher_suite.encrypt(sensitive_data.encode())
```

2. **Key Management**

```bash
# Store keys in environment variables or key management service
export ENCRYPTION_KEY=$(openssl rand -base64 32)
```

## Monitoring and Logging

### Application Monitoring

**Prometheus Metrics**

```python
from prometheus_client import Counter, Histogram, generate_latest

# Define metrics
REQUEST_COUNT = Counter('requests_total', 'Total requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('request_duration_seconds', 'Request duration')

@app.route('/metrics')
def metrics():
    return generate_latest()
```

**Health Checks**

```python
@app.route('/health')
def health_check():
    checks = {
        'database': check_database(),
        'redis': check_redis(),
        'socket_server': check_socket_server()
    }

    all_healthy = all(checks.values())
    status_code = 200 if all_healthy else 503

    return jsonify({
        'status': 'healthy' if all_healthy else 'unhealthy',
        'checks': checks
    }), status_code
```

### Log Management

**Structured Logging**

```python
import structlog

logger = structlog.get_logger()

# Log with context
logger.info(
    "Data access request",
    partner_id=partner_id,
    user_id=user_id,
    purpose=purpose,
    status="approved"
)
```

**Log Aggregation (ELK Stack)**

```yaml
# docker-compose.yml addition
elasticsearch:
  image: docker.elastic.co/elasticsearch/elasticsearch:7.14.0
  environment:
    - discovery.type=single-node
  ports:
    - "9200:9200"
  volumes:
    - es_data:/usr/share/elasticsearch/data

kibana:
  image: docker.elastic.co/kibana/kibana:7.14.0
  ports:
    - "5601:5601"
  environment:
    - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
  depends_on:
    - elasticsearch

logstash:
  image: docker.elastic.co/logstash/logstash:7.14.0
  volumes:
    - ./logstash/pipeline:/usr/share/logstash/pipeline
  depends_on:
    - elasticsearch
```

## Backup and Recovery

### Database Backup

**Automated Backup Script**

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"
DB_NAME="fintrust"

# Create backup
pg_dump $DB_NAME > $BACKUP_DIR/fintrust_$DATE.sql

# Compress
gzip $BACKUP_DIR/fintrust_$DATE.sql

# Remove old backups (keep 30 days)
find $BACKUP_DIR -name "fintrust_*.sql.gz" -mtime +30 -delete

# Upload to S3 (optional)
aws s3 cp $BACKUP_DIR/fintrust_$DATE.sql.gz s3://your-backup-bucket/
```

**Cron Job**

```bash
# Add to crontab
0 2 * * * /path/to/backup.sh
```

### Data Recovery

**Point-in-time Recovery**

```bash
# Stop application
docker-compose down

# Restore database
gunzip -c backup_file.sql.gz | psql fintrust

# Restart application
docker-compose up -d
```

## Performance Optimization

### Application Tuning

1. **Connection Pooling**

```python
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=30,
    pool_pre_ping=True
)
```

2. **Caching**

```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'redis'})

@cache.memoize(timeout=300)
def get_user_data(user_id):
    return expensive_database_query(user_id)
```

3. **Async Processing**

```python
from celery import Celery

celery = Celery('fintrust')

@celery.task
def process_audit_log(log_data):
    # Process in background
    save_to_database(log_data)
```

### Infrastructure Scaling

**Load Balancing**

```nginx
upstream backend {
    least_conn;
    server backend1:5000 weight=3;
    server backend2:5000 weight=2;
    server backend3:5000 weight=1;

    # Health checks
    server backup.example.com backup;
}
```

**Auto-scaling (Kubernetes)**

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: fintrust-backend-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: fintrust-backend
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

## Troubleshooting

### Common Issues

1. **Database Connection Issues**

```bash
# Check database connectivity
psql -h localhost -U postgres -d fintrust -c "SELECT 1;"

# Check connection pool
SELECT * FROM pg_stat_activity;
```

2. **Socket Server Issues**

```bash
# Check if socket server is listening
netstat -tlnp | grep 9999

# Test socket connection
telnet localhost 9999
```

3. **Memory Issues**

```bash
# Check memory usage
free -h
docker stats

# Analyze memory leaks
python -m memory_profiler app.py
```

### Debug Mode

**Enable Debug Logging**

```bash
export FLASK_DEBUG=True
export LOG_LEVEL=DEBUG
python app.py
```

**Performance Profiling**

```python
from flask_profiler import Profiler

profiler = Profiler()
profiler.init_app(app)

# Access profiler at /flask-profiler/
```

### Monitoring Alerts

**Alertmanager Configuration**

```yaml
# alertmanager.yml
global:
  smtp_smarthost: "localhost:587"
  smtp_from: "alerts@your-domain.com"

route:
  group_by: ["alertname"]
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 1h
  receiver: "web.hook"

receivers:
  - name: "web.hook"
    email_configs:
      - to: "admin@your-domain.com"
        subject: "FinTrust Guardian Alert"
        body: "{{ range .Alerts }} {{ .Annotations.summary }} {{ end }}"
```

---

This deployment guide provides a comprehensive approach to taking FinTrust Guardian from development to production. Adjust configurations based on your specific infrastructure requirements and security policies.
