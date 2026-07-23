FROM debian:bookworm

# Unbuffer stdout so prints from background processes (like server.py &)
# show up immediately instead of being lost when the container exits.
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
        dbus dbus-x11 python3-dbus python3-gi \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /work
COPY server.py client.py ./
