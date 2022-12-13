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
except OSError:
    #machine.reset()
    pass

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
    if settings["language"] == "":
        f = open("language_select.html", "r")
        html = (f.read())

    print("Client connected")
    request_line = await reader.readline()
    print("Request:", request_line)
    request_line = str(request_line)

    eng = request_line.find('language=en')
    cze = request_line.find('language=cz')
    fra = request_line.find('language=fr')
    ger = request_line.find('language=de')
    if eng > 0:
        print("English selected")
        settings["language"] = "en"
        with open("settings.json", "w") as json_file:
            json.dump(settings, json_file)
    elif cze > 0:
        print("Czech selected")
        settings["language"] = "cz"
        with open("settings.json", "w") as json_file:
            json.dump(settings, json_file)
    elif fra > 0:
        print("French selected")
        settings["language"] = "fr"
        with open("settings.json", "w") as json_file:
            json.dump(settings, json_file)
    elif ger > 0:
        print("German selected")
        settings["language"] = "de"
        with open("settings.json", "w") as json_file:
            json.dump(settings, json_file)

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
    if settings["user_ssid"] == "":
        print('Creating AP')
        createAP()

    print('Setting up webserver...')
    asyncio.create_task(asyncio.start_server(serve_client, "0.0.0.0", 80))
    while True:
        onboard.on()
        await asyncio.sleep(0.25)
        onboard.off()
        await asyncio.sleep(5)

try:
    asyncio.run(main())
finally:
    asyncio.new_event_loop()
