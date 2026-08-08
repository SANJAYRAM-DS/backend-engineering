# Phase 32: Docker Containerization & Multi-Stage Builds

> **Author**: Senior Backend Architect & Security Lead  
> **Phase**: 32 of 35  
> **Target Path**: `docs/32-docker.md`  

---

## 1. Learning Objectives

By completing this phase, you will master:
* Multi-stage Docker builds to minimize container attack surface.
* Running applications under unprivileged non-root users inside containers.
* Orchestrating Django, PostgreSQL, and Gunicorn via Docker Compose.

---

## 2. Multi-Stage Dockerfile Blueprint

File path: `Dockerfile`

```dockerfile
# ==============================================================================
# Multi-Stage Production Dockerfile for Enterprise Auth Engine
# ==============================================================================

# Stage 1: Build Dependencies
FROM python:3.12-slim AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Final Secure Production Runtime
FROM python:3.12-slim AS runner

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy installed Python packages from builder
COPY --from=builder /install /usr/local
COPY . /app

# Create unprivileged system user
RUN addgroup --system appgroup && adduser --system --group appuser \
    && chown -R appuser:appgroup /app

USER appuser

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4", "--threads", "2"]
```

---

## 3. Docker Compose Specification

File path: `docker-compose.yml`

```yaml
version: '3.8'

services:
  db:
    image: postgres:16-alpine
    container_name: auth_postgres_db
    environment:
      POSTGRES_DB: auth_system_db
      POSTGRES_USER: auth_user
      POSTGRES_PASSWORD: secure_postgres_password_change_me
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  web:
    build: .
    container_name: auth_api_web
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4
    ports:
      - "8000:8000"
    environment:
      - DJANGO_ENV=production
      - POSTGRES_HOST=db
      - POSTGRES_PORT=5432
    depends_on:
      - db

volumes:
  postgres_data:
```

---

## 4. Mentor Mode: Self-Check

### Self-Check Questions
1. Why is running containers as `USER appuser` (non-root) a critical container security standard?  
   *Answer: If an attacker executes remote code inside the container, running as `root` grants them container root privileges, increasing the risk of container escape vulnerabilities.*
