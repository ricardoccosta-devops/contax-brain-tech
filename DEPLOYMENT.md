# Deployment Guide - Contax Brain.tech Portal

This guide covers various deployment options for the Contax Brain.tech Portal.

## Table of Contents
1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Production Deployment](#production-deployment)
4. [Environment Variables](#environment-variables)
5. [Monitoring](#monitoring)

## Local Development

### Prerequisites
- Python 3.9 or higher
- pip package manager
- OpenAI API key

### Setup Steps

1. **Clone the repository:**
```bash
git clone https://github.com/ricardoccosta-devops/contax-brain-tech.git
cd contax-brain-tech
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment:**
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

5. **Run the application:**
```bash
python main.py
```

Or use the quick start script:
```bash
./start.sh
```

6. **Access the portal:**
- Web UI: http://localhost:8000
- Health Check: http://localhost:8000/health
- API Docs: http://localhost:8000/docs (FastAPI auto-generated)

## Docker Deployment

### Using Docker Compose (Recommended)

1. **Configure environment:**
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

2. **Build and run:**
```bash
docker-compose up -d
```

3. **View logs:**
```bash
docker-compose logs -f
```

4. **Stop the service:**
```bash
docker-compose down
```

### Using Docker directly

1. **Build the image:**
```bash
docker build -t contax-brain-tech .
```

2. **Run the container:**
```bash
docker run -d \
  --name contax-brain-tech \
  -p 8000:8000 \
  -e OPENAI_API_KEY=your_api_key_here \
  contax-brain-tech
```

## Production Deployment

### Option 1: Cloud Platform (AWS, GCP, Azure)

#### AWS EC2 Example

1. **Launch EC2 instance:**
   - Choose Ubuntu 20.04 or newer
   - Instance type: t2.medium or larger
   - Configure security group to allow port 8000

2. **Install Docker:**
```bash
sudo apt update
sudo apt install -y docker.io docker-compose
sudo usermod -aG docker $USER
```

3. **Deploy application:**
```bash
git clone https://github.com/ricardoccosta-devops/contax-brain-tech.git
cd contax-brain-tech
cp .env.example .env
# Edit .env
docker-compose up -d
```

4. **Setup reverse proxy (Nginx):**
```bash
sudo apt install -y nginx
```

Create Nginx configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

5. **Enable SSL with Let's Encrypt:**
```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### Option 2: Container Orchestration (Kubernetes)

#### Example Kubernetes Deployment

**deployment.yaml:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: contax-brain-tech
spec:
  replicas: 3
  selector:
    matchLabels:
      app: contax-brain-tech
  template:
    metadata:
      labels:
        app: contax-brain-tech
    spec:
      containers:
      - name: contax-brain-tech
        image: contax-brain-tech:latest
        ports:
        - containerPort: 8000
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: contax-secrets
              key: openai-api-key
---
apiVersion: v1
kind: Service
metadata:
  name: contax-brain-tech-service
spec:
  selector:
    app: contax-brain-tech
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

**Create secret:**
```bash
kubectl create secret generic contax-secrets \
  --from-literal=openai-api-key=your_api_key_here
```

**Deploy:**
```bash
kubectl apply -f deployment.yaml
```

### Option 3: Platform as a Service (PaaS)

#### Heroku Example

1. **Create `Procfile`:**
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

2. **Deploy:**
```bash
heroku create contax-brain-tech
heroku config:set OPENAI_API_KEY=your_api_key_here
git push heroku main
```

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `OPENAI_API_KEY` | OpenAI API key | Yes | - |
| `APP_NAME` | Application name | No | Contax Brain.tech |
| `APP_VERSION` | Application version | No | 1.0.0 |
| `DEBUG` | Enable debug mode | No | True |
| `HOST` | Server host | No | 0.0.0.0 |
| `PORT` | Server port | No | 8000 |

## Monitoring

### Health Check Endpoint
Monitor the application using the health check endpoint:
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "app_name": "Contax Brain.tech",
  "version": "1.0.0",
  "llm_configured": true
}
```

### Logging
The application logs to stdout. View logs:

**Docker:**
```bash
docker logs -f contax-brain-tech
```

**Docker Compose:**
```bash
docker-compose logs -f
```

**Direct execution:**
Logs appear in the terminal.

### Metrics
Consider integrating with monitoring tools:
- Prometheus for metrics
- Grafana for visualization
- Sentry for error tracking

### Performance Tuning

1. **Adjust workers (for production):**
```bash
uvicorn main:app --workers 4 --host 0.0.0.0 --port 8000
```

2. **Enable caching:**
Consider adding Redis for caching LLM responses.

3. **Load balancing:**
Use Nginx or HAProxy for load balancing multiple instances.

## Security Best Practices

1. **API Key Management:**
   - Never commit API keys to version control
   - Use secrets management (AWS Secrets Manager, HashiCorp Vault, etc.)
   - Rotate API keys regularly

2. **HTTPS:**
   - Always use HTTPS in production
   - Configure SSL/TLS certificates

3. **Firewall:**
   - Only expose necessary ports
   - Use security groups/firewall rules

4. **Updates:**
   - Keep dependencies updated
   - Monitor security advisories

5. **Rate Limiting:**
   - Implement rate limiting to prevent abuse
   - Use nginx or application-level rate limiting

## Troubleshooting

### Application won't start
- Check if port 8000 is available
- Verify OPENAI_API_KEY is set correctly
- Check logs for errors

### 500 errors on API calls
- Verify OpenAI API key is valid
- Check OpenAI API status
- Review application logs

### Slow responses
- Check internet connection
- Verify OpenAI API performance
- Consider caching frequently requested analyses

## Backup and Recovery

### Data Backup
Currently, the application is stateless. However, if you add a database:
- Regular database backups
- Store backups in secure, redundant locations

### Disaster Recovery
- Document deployment process
- Keep configuration in version control
- Test recovery procedures regularly

## Scaling

### Horizontal Scaling
- Run multiple instances behind a load balancer
- Use container orchestration (Kubernetes, Docker Swarm)

### Vertical Scaling
- Increase CPU/RAM for the instance
- Optimize Python configuration

---

For questions or issues, please open an issue on GitHub or contact support.
