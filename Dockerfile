# Use a Python base image with Node.js for building the frontend
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install build dependencies (gcc and others) for compiling C extensions
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js and npm for building the frontend
RUN apt-get update && apt-get install -y nodejs npm

# Copy frontend files and build the Vue.js app
COPY frontend/ ./frontend/
RUN cd frontend && npm install && npm run build

# Copy backend files
COPY backend/ ./backend/
COPY requirements.txt ./

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install gunicorn

# Copy the built frontend files to a location the backend can serve
RUN mkdir -p ./frontend/dist
COPY frontend/dist/ ./frontend/dist/

# Expose the port your app will run on
EXPOSE 5000

# Set environment variables (optional, adjust as needed)
ENV FLASK_ENV=production
ENV RUN_SEEDING=False

# Run database migrations and start the app with gunicorn
CMD ["sh", "-c", "flask --app backend/app db upgrade && gunicorn --chdir backend -b 0.0.0.0:5000 -w 4 app:app --timeout 300 --log-level info"]