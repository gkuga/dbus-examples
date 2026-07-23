IMAGE := dbus-hello-world

.PHONY: build demo shell clean

build:
	docker build -t $(IMAGE) .

# Runs the server and client once, back to back, and exits.
demo: build
	docker run --rm -v $(CURDIR):/work $(IMAGE) bash -c '\
		export DBUS_SESSION_BUS_ADDRESS=$$(dbus-daemon --session --print-address --fork); \
		python3 server.py & \
		sleep 1; \
		python3 client.py Alice; \
		sleep 1'

# Drops you into an interactive shell with the session bus already running,
# so you can run server.py / client.py manually and poke around with dbus-send.
shell: build
	docker run -it --rm -v $(CURDIR):/work $(IMAGE) bash -c '\
		export DBUS_SESSION_BUS_ADDRESS=$$(dbus-daemon --session --print-address --fork); \
		echo "DBUS_SESSION_BUS_ADDRESS=$$DBUS_SESSION_BUS_ADDRESS"; \
		exec bash'

clean:
	docker rmi -f $(IMAGE) 2>/dev/null || true
