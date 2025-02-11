import machine
import utime
from pin_out import *

led4.on()
utime.sleep(1)
led3.on()
utime.sleep(1)
led2.on()
utime.sleep(1)
led1.on()
utime.sleep(1)
led4.off()
utime.sleep(1)
led3.off()
utime.sleep(1)
led2.off()
utime.sleep(1)
led1.off()
utime.sleep(1)

while True:
    if not buttonK4.value():
        led4.on()
    elif not buttonK3.value():
        led3.on()
    elif not buttonK2.value():
        led2.on()
    elif not buttonK1.value():
        led1.on()
    else:
        led4.off()
        led3.off()
        led2.off()
        led1.off()
