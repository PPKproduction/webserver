import socket
import network
import time
import json
import machine
from machine import Pin
import uasyncio as asyncio

onboard = Pin("LED", Pin.OUT, value=0)

try:
    settings = json.loads(open("settings.json", "r").read())
    print(settings)
except OSError:
    machine.reset()

if len(settings["user_ssid"]) <= 0:
    print("setup user ssid")
else:
    print("user ssid found")
    
ssid = settings["ssid"]
password = settings["password"]
page = "page-"+settings["language"]+".html"
f = open(page, "r")
html = (f.read())


def createAP():
    # Define an access point, name it and then make it active
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, password=password)
    ap.active(True)

    # Wait until it is active
    while not ap.active:
        pass

    print("Access point active")
    # Print out IP information
    print(ap.ifconfig())


async def serve_client(reader, writer):
    print("Client connected")
    request_line = await reader.readline()
    print("Request:", request_line)
    # We are not interested in HTTP request headers, skip them
    while await reader.readline() != b"\r\n":
        pass

    response = html
    writer.write('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
    writer.write(response)

    await writer.drain()
    await writer.wait_closed()
    print("Client disconnected")


async def main():
    print('Connecting to Network...')
    createAP()

    print('Setting up webserver...')
    asyncio.create_task(asyncio.start_server(serve_client, "0.0.0.0", 80))
    while True:
        onboard.on()
        print("heartbeat")
        await asyncio.sleep(0.25)
        onboard.off()
        await asyncio.sleep(5)

try:
    asyncio.run(main())
finally:
    asyncio.new_event_loop()
