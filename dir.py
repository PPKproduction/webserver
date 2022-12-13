import os

try:
    os.listdir('/.frozen')
except OSError:
    print("no such directory")
    
    import network
    from time import sleep
    try:
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect("SlavHome", "arakondaKromrovana1")
        if wlan.isconnected == False:
            sleep(0.1)

        print("connected to wifi")

        
    except:
        print("phew install failed")

    import upip
    upip.install("micropython-phew")



