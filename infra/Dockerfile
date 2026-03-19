FROM ubuntu:24.04

# Install build-essential and modern compilers
RUN apt-get update && apt-get install -y \
    cmake \
    clang-19 \
    build-essential \
    libssl-dev \
    libcurl4-openssl-dev \
    git \
    curl \
    unzip \
    dos2unix \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

# Fix Windows line endings and permissions
RUN dos2unix ./install.sh && chmod +x ./install.sh

# Build the Endee Engine
RUN ./install.sh --release --skip-deps

EXPOSE 8080
CMD ["./run.sh"]