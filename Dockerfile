# Use a Python base image with Node.js for building the frontend
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    build-essential gcc python3-dev \
    libpq-dev \
    libmupdf-dev libfreetype6-dev libjpeg-dev zlib1g-dev \
    nodejs npm \
    default-mysql-client \
    locales \
    && rm -rf /var/lib/apt/lists/* \
    && locale-gen en_US.UTF-8

# Copy frontend files and build the Vue.js app
COPY frontend/ ./frontend/
RUN cd frontend && npm install && npm run build

# Copy backend files
COPY backend/ ./backend/
COPY requirements.txt ./

# Install Python dependencies
# Explicitly uninstall pinecone-client to avoid conflicts (pinecone-client is out of date, install pinecone instead)
RUN pip3 uninstall -y pinecone-client || true
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install gunicorn

# Copy the built frontend files to a location the backend can serve
RUN mkdir -p ./frontend/dist
# COPY frontend/dist/ ./frontend/dist/

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Set environment variables
ENV FLASK_ENV=production
ENV FLASK_APP=backend/app.py
ENV PYTHONIOENCODING=UTF-8
ENV RUN_SEEDING=False

# for UTF-8 encoding ('latin-1' codec can't encode character xyz, ordinal not in range(128), or 'ascii codec' or similar errors)
ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PYTHONUTF8=1

# Expose the port your app will run on
EXPOSE 5000

# CMD ["sh", "-c", "cd backend && ls"]
# Run database migrations and start the app with gunicorn
# CMD ["sh", "-c", "cd backend/migrations/versions && ls && flask db upgrade"]
CMD ["sh", "-c", "gunicorn --chdir backend -b 0.0.0.0:5000 -w 2 app:app --timeout 300 --log-level debug"]
# ENTRYPOINT ["/app/entrypoint.sh"]