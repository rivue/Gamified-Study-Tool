# Stage 1: Build frontend
FROM node:18-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm ci --only=production
COPY frontend/ ./
RUN npm run build

# Stage 2: Build backend
FROM python:3.11-slim AS backend-builder
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential gcc python3-dev \
    libpq-dev \
    libmupdf-dev libfreetype6-dev libjpeg-dev zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt ./
RUN pip3 uninstall -y pinecone-client || true
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install gunicorn

# Stage 3: Final runtime image
FROM python:3.11-slim AS runtime
WORKDIR /app

# Install only runtime dependencies (smaller image)
RUN apt-get update && apt-get install -y \
    libpq5 \
    libmupdf-dev \
    locales \
    && rm -rf /var/lib/apt/lists/* \
    && locale-gen en_US.UTF-8

# Copy Python dependencies from builder stage
COPY --from=backend-builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=backend-builder /usr/local/bin /usr/local/bin

# Copy built frontend from frontend stage
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Copy backend source
COPY backend/ ./backend/
COPY entrypoint.sh ./
RUN chmod +x ./entrypoint.sh

# Set environment variables
ENV FLASK_ENV=production
ENV FLASK_APP=backend/app.py
ENV PYTHONIOENCODING=UTF-8
ENV RUN_SEEDING=False
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PYTHONUTF8=1

EXPOSE 5000

CMD ["sh", "-c", "gunicorn --chdir backend -b 0.0.0.0:5000 -w 2 app:app --timeout 300 --log-level debug"]