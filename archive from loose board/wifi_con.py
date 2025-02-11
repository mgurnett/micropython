import machine
import utime
from board_devices import blink_led 
import constants
import network   # handles connecting to WiFiimport machine


def connect_to_wifi():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(constants.ssid, constants.password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        blink_led ("waiting", 1)
    ip_address = wlan.ifconfig()[0]
    return ip_address

def wifi_connect():
    try:
        ip = connect_to_wifi()
        #print(f'Connected on {ip}')
    except KeyboardInterrupt:
        ip = 0
    return ip

if __name__ == "__main__":
    ip = wifi_connect()
    print (ip)

    
