# OdooProtect Docker Image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy OdooProtect files
COPY . .

# Make executable
RUN chmod +x odooprotect.py

# Create symlink
RUN ln -sf /app/odooprotect.py /usr/local/bin/odooprotect

# Set Python path
ENV PYTHONPATH=/app

# Default command
CMD ["odooprotect", "--help"]

# Labels
LABEL maintainer="dynaz"
LABEL description="OdooProtect - Advanced Python Code Obfuscator"
LABEL version="1.0.0"

# Usage:
# docker build -t odooprotect .
# docker run odooprotect --help
# docker run -v $(pwd):/workspace odooprotect -i /workspace/script.py
