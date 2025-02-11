from machine import Pin
from PicoDHT22 import PicoDHT22
import time

# DHT22 libray is available at
# https://github.com/danjperron/PicoDHT22

# init DHT22 on Pin 2
dht22 = PicoDHT22(Pin(2,Pin.IN,Pin.PULL_UP))

while True:
    T, H = dht22.read()
    now = time.localtime()
    print(f"{now[6]} {now[2]:02}  {now[3]:02d}:{now[4]:02d}:{now[5]:02d}")

    if T is None:
        print("T=----\xdfC H=----}%")
    else:
        print(f"T={T:3.1f}\xdfC H={H:3.1f}%")
    time.sleep_ms(500)
