FROM debian:bookworm

RUN apt-get update && apt-get install -y \
    python3 python3-pip \
    build-essential \
    sudo curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*
