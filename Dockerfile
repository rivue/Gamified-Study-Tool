# Use an official Python runtime as the base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy backend and frontend files
COPY backend/ ./backend/
COPY frontend/dist/ ./frontend/dist/

# Install Python dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt

# Install Gunicorn
RUN pip install gunicorn

# Expose port
EXPOSE 5000

# Run the app
CMD ["gunicorn", "--chdir", "backend", "-b", "0.0.0.0:5000", "-w", "4", "app:app", "--timeout", "300"]