FROM debian:bookworm

RUN apt-get update && apt-get install -y --no-install-recommends \
        dbus dbus-x11 python3-dbus python3-gi \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /work
COPY server.py client.py ./
