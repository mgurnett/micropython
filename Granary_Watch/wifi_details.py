import machine
import utime
import secrets
import network   # handles connecting to WiFiimport machine
 
led = machine.Pin('LED', machine.Pin.OUT)

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(secrets.ssid, secrets.password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        utime.sleep(1)
    ip = wlan.ifconfig()[0]
    #print(f'Connected on {ip}')
    return ip

def connected ():
    for x in range (10):
        led.value(1)
        utime.sleep(.5)
        led.value(0)
        utime.sleep(.5)
    return

def wifi_fail ():
    for x in range (3):
        led.value(1)
        utime.sleep(.25)
        led.value(0)
        utime.sleep(.25)
    return