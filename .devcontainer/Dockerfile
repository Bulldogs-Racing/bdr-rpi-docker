# Raspberry Pi OS Bookworm (64-bit) base
FROM arm64v8/debian:bookworm

ARG USERNAME=bdr
ENV DEBIAN_FRONTEND=noninteractive

# Base dependencies
RUN apt-get update && apt-get install -y \
    sudo curl git build-essential cmake python3 python3-pip pkg-config \
    libssl-dev libffi-dev \
 && useradd -ms /bin/bash bdr \
 && echo "bdr ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers \
 && rm -rf /var/lib/apt/lists/*

USER bdr
WORKDIR /home/bdr

CMD [ "bash" ]
