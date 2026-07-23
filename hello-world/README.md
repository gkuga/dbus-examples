# D-Bus Hello World

A minimal example for learning how D-Bus works: a service that registers
itself on the **session bus** and exposes one method, and a client that
looks up that service and calls the method remotely.

- `server.py` — registers the well-known name `com.example.HelloWorld` on
  the session bus, publishes an object at `/com/example/HelloWorld`, and
  exposes a `SayHello(name) -> string` method.
- `client.py` — connects to the same session bus, gets a proxy for the
  service, and calls `SayHello`, printing the reply.

This mirrors the classic D-Bus tutorial pattern: one long-running process
owns a bus name and serves requests, other processes come and go, calling
into it whenever they like.

## Requirements

Both scripts need Python 3 with `dbus-python` (the `dbus` module) and a
GLib main loop (`PyGObject`) for the server's event loop.

## Quick start (Makefile)

If you have Docker and `make` on your host, everything below is wrapped
into two targets:

```bash
make demo   # builds the image, runs server.py + client.py once, and exits
make shell  # builds the image, drops you into a shell with the session
            # bus already running, so you can run the scripts manually
```

Both targets build a small `debian:bookworm`-based image (see
`Dockerfile`) with `dbus`, `dbus-x11`, `python3-dbus` and `python3-gi`
preinstalled, so there's no manual `apt-get` step. `make clean` removes
the built image again.

## Running it by hand in the Debian container

If you'd rather not use the Makefile, start the container as you
described, then install Python bindings on top of the `dbus`/`dbus-x11`
packages:

```bash
docker run -it --rm --name dbus-hello debian:bookworm bash
```

Inside the container:

```bash
apt-get update
apt-get install -y dbus dbus-x11 python3-dbus python3-gi

# Start a session bus and export its address so client/server can find it
export DBUS_SESSION_BUS_ADDRESS=$(dbus-daemon --session --print-address --fork)
```

Copy `server.py` and `client.py` into the container (e.g. with
`docker cp`), or mount this directory as a volume with `-v`.

Run the server in the background, then call it from the client in the
same shell:

```bash
python3 server.py &
python3 client.py Alice
```

Expected output:

```
[server] Registered 'com.example.HelloWorld' at '/com/example/HelloWorld'. Waiting for calls...
[server] SayHello('Alice') -> 'Hello, Alice! This message travelled over D-Bus.'
[client] Server replied: Hello, Alice! This message travelled over D-Bus.
```

### Using two separate shells

If you'd rather run the server and client in two separate terminals,
open a second shell into the same container:

```bash
docker exec -it dbus-hello bash
```

Since `DBUS_SESSION_BUS_ADDRESS` is only set in the shell that started
the bus, export the **same** value in the second shell too, e.g. by
saving it to a file the first time:

```bash
# in the first shell
echo $DBUS_SESSION_BUS_ADDRESS > /tmp/dbus-address

# in the second shell
export DBUS_SESSION_BUS_ADDRESS=$(cat /tmp/dbus-address)
```

## Inspecting the bus

While the server is running, you can see it registered on the bus with:

```bash
dbus-send --session --print-reply \
  --dest=org.freedesktop.DBus \
  /org/freedesktop/DBus \
  org.freedesktop.DBus.ListNames | grep HelloWorld
```

or call the method directly without the Python client, using `dbus-send`:

```bash
dbus-send --session --print-reply \
  --dest=com.example.HelloWorld \
  /com/example/HelloWorld \
  com.example.HelloWorld.SayHello string:Bob
```
