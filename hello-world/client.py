#!/usr/bin/env python3
"""Minimal D-Bus client: looks up the HelloWorld service on the session
bus and calls its SayHello method, printing whatever it replies with."""

import sys

import dbus

BUS_NAME = "com.example.HelloWorld"
OBJECT_PATH = "/com/example/HelloWorld"
INTERFACE = "com.example.HelloWorld"


def main():
    name = sys.argv[1] if len(sys.argv) > 1 else "World"

    bus = dbus.SessionBus()
    proxy = bus.get_object(BUS_NAME, OBJECT_PATH)
    hello_interface = dbus.Interface(proxy, dbus_interface=INTERFACE)

    reply = hello_interface.SayHello(name)
    print(f"[client] Server replied: {reply}")


if __name__ == "__main__":
    main()
