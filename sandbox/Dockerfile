FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3-pip \
    nodejs \
    npm \
    git \
    curl \
    wget \
    ffmpeg \
    imagemagick \
    pandoc \
    chromium-browser \
    && rm -rf /var/lib/apt/lists/*

# Install pnpm
RUN npm install -g pnpm

# Copy requirements and install Python packages
COPY requirements.txt /tmp/
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

# Install Playwright
RUN pip3 install playwright && \
    playwright install chromium && \
    playwright install-deps

# Create workspace directories
RUN mkdir -p /workspace/uploads /workspace/generated /workspace/downloads /workspace/temp

# Copy executor service
COPY executor/ /app/executor/
WORKDIR /app

# Install executor dependencies
RUN pip3 install -r executor/requirements.txt

# Expose port
EXPOSE 8000

# Start executor service
CMD ["uvicorn", "executor.main:app", "--host", "0.0.0.0", "--port", "8000"]
