FROM python:3.12-slim

# Install system dependencies required for building tgcrypto and other C extensions
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git \
        build-essential \
        gcc \
        libffi-dev \
        libssl-dev \
        python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

RUN chmod 777 /usr/src/app

# Copy source files
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Give execute permission for start.sh (optional if already executable)
RUN chmod +x start.sh

# Run the startup script
CMD ["bash", "start.sh"]
