# Use a slim Python image for faster builds
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Install dependencies first (optimized build cache)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the full project
COPY . .

# Expose app port
EXPOSE 8000

# Run with gunicorn + uvicorn worker
CMD ["sh", "-c", "gunicorn -w 1 -k uvicorn.workers.UvicornWorker app.backend.main:app --bind 0.0.0.0:${PORT:-8000} --timeout 60 --log-level info --access-logfile -"]



