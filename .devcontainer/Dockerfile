# Raspberry Pi OS Bookworm (64-bit) base
FROM arm64v8/debian:bookworm

ENV DEBIAN_FRONTEND=noninteractive

# Install base system and Raspberry Pi repo key
RUN apt-get update && apt-get install -y \
    sudo curl gnupg git build-essential cmake python3 python3-pip pkg-config \
    libssl-dev libffi-dev \
 && curl -fsSL https://archive.raspberrypi.com/debian/raspberrypi.gpg.key \
    | gpg --dearmor -o /usr/share/keyrings/raspberrypi-archive-keyring.gpg \
#  && echo "deb [signed-by=/usr/share/keyrings/raspberrypi-archive-keyring.gpg] http://archive.raspberrypi.com/debian bookworm main" \
#     > /etc/apt/sources.list.d/raspi.list \
#  && apt-get update && apt-get install -y \
#     libraspberrypi-bin libraspberrypi-dev raspberrypi-kernel-headers \
 && useradd -ms /bin/bash bdr \
 && echo "bdr ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers \
 && rm -rf /var/lib/apt/lists/* \
 && mkdir season2526 \
 && git@github.com:Bulldogs-Racing/dashboard-ui.git season2526/dashboard-ui \
 && cd season2526/dashboard-ui \
 && python -m venv \
 && cd ~/ \
 && ~/season2526/dashboard-ui/.venv/bin/pip install pynng

USER bdr
WORKDIR /home/bdr
CMD [ "bash" ]

#  Build and run with:
# docker build -t rpi-bookworm-6.6 .
# docker run -it --platform linux/arm64 rpi-bookworm-6.6
