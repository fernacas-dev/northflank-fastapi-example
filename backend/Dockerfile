# Build stage
FROM python:3.11-slim as builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY backend/requirements.txt .
RUN pip install --user -r requirements.txt

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Copy only necessary files from builder stage
COPY --from=builder /root/.local /root/.local

# Ensure scripts are in PATH
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY backend/ .

# Make entrypoint script executable
RUN chmod +x entrypoint.sh

# Exposed port
EXPOSE 8000

# Default environment variables (can be overridden)
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000 \
    ENVIRONMENT=production

# Command to run the application
ENTRYPOINT ["./entrypoint.sh"]
