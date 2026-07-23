#!/usr/bin/env python3
"""Minimal D-Bus service: registers a name on the session bus and exposes
a single method, SayHello, that other processes can call remotely."""

import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib

BUS_NAME = "com.example.HelloWorld"
OBJECT_PATH = "/com/example/HelloWorld"
INTERFACE = "com.example.HelloWorld"


class HelloWorldService(dbus.service.Object):
    def __init__(self, bus):
        bus_name = dbus.service.BusName(BUS_NAME, bus=bus)
        super().__init__(bus_name, OBJECT_PATH)

    @dbus.service.method(INTERFACE, in_signature="s", out_signature="s")
    def SayHello(self, name):
        message = f"Hello, {name}! This message travelled over D-Bus."
        print(f"[server] SayHello({name!r}) -> {message!r}")
        return message


def main():
    DBusGMainLoop(set_as_default=True)
    bus = dbus.SessionBus()
    HelloWorldService(bus)
    print(f"[server] Registered '{BUS_NAME}' at '{OBJECT_PATH}'. Waiting for calls...")
    GLib.MainLoop().run()


if __name__ == "__main__":
    main()
