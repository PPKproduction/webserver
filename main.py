# ssid = "SlavHome"
# password = "arakondaKromrovana1"
# ssid = "rigaku-guest"
# password = "kromrovanablublina"


from phew import logging, server, connect_to_wifi, access_point
from phew.template import render_template
from phew.logging import info
import json




def scan_networks():
    import network
    wlan = network.WLAN()  # network.WLAN(network.STA_IF)
    wlan.active(True)
    net = wlan.scan()
    nets = []
    for w in net:
        nets.append(w[0].decode())
    return nets



try:
    settings = json.loads(open("settings.json", "r").read())
except OSError:
    # machine.reset()
    pass


ssid = settings["ssid"]
password = settings["password"]
user_ssid = settings["user_ssid"]
user_pass = settings["user_password"]


if user_ssid == "":
    networks = scan_networks()
    print("AP mode")
    print(access_point(ssid, password=password))
else:
    print(connect_to_wifi(ssid, password))

@server.route("/network", ["POST", 'GET'])
def network(request):
    print(request.method)
    if request.method == 'GET':
        return render_template("network_init.html", title="Datalogger")
    if request.method == 'POST':
        user_ssid = request.form.get("ssid", None)
        user_pass = request.form.get("password", None)
        info("Storing user SSID:{}".format(user_ssid))
        info("Storing user Password:{}".format(user_pass))
        return render_template("index.html", title="Datalogger")


@server.route("/", ["POST", 'GET'])
def index(request):
    print(request.method)
    if request.method == 'GET':
        return render_template("network_init.html", title="Datalogger")
        #return render_template("index.html", title="Datalogger")
    if request.method == 'POST':
        return render_template("index.html", title="Datalogger")


@server.route("/about")
def about(request):
    return render_template("about.html", name="Kevin", title="About this Site")

@server.route("/log")
def log(request):
    f = open("log.txt", "r")
    log = f.readlines()
    f.close()
    print(log)
    data = ""
    for lines in log:

        data = data + "{}".format(lines) + "\n"

    return render_template("log.html", detes=log)

@server.route("/sensors")
def sensors(request):
    return render_template("sensors.html", name="Kevin", title="About this Site")


@server.catchall()
def my_catchall(request):
    return "No matching route", 404


server.run()
