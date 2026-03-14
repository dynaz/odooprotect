# PyProtect Docker Image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy PyProtect files
COPY . .

# Make executable
RUN chmod +x pyprotect.py

# Create symlink
RUN ln -sf /app/pyprotect.py /usr/local/bin/pyprotect

# Set Python path
ENV PYTHONPATH=/app

# Default command
CMD ["pyprotect", "--help"]

# Labels
LABEL maintainer="dynaz"
LABEL description="PyProtect - Advanced Python Code Obfuscator"
LABEL version="1.0.0"

# Usage:
# docker build -t pyprotect .
# docker run pyprotect --help
# docker run -v $(pwd):/workspace pyprotect -i /workspace/script.py
