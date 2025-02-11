from machine import Pin, Timer
from utime import sleep
from pin_out import *

# create an uninitialized timer object
myTimer = Timer()

# create a function to be called when the timer goes off
# this function just toggles the onboard LED
def toggle_led(timer):
    led4.toggle()

# initialize the timer object to tick every second (1,000 milliseconds)
myTimer.init(period=1000, mode=Timer.PERIODIC, callback=toggle_led)

while True:
    sleep(10)
    print('just sleeping here')

#     if not buttonK4.value():
#         led4.on()
#     elif not buttonK3.value():
#         led3.on()
#     elif not buttonK2.value():
#         led2.on()
#     elif not buttonK1.value():
#         led1.on()
#     else:
#         led4.off()
#         led3.off()
#         led2.off()
#         led1.off()