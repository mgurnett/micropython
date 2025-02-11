from machine import Pin, Timer
from utime import sleep
from pin_out import *

timer1 = False
timer2 = False
timer3 = False
timer4 = False

# create an uninitialized timer object
myTimer1 = Timer()
myTimer2 = Timer()
myTimer3 = Timer()
myTimer4 = Timer()

# create a function to be called when the timer goes off
# this function just toggles the onboard LED
def toggle_led1(timer):
    led1.toggle()
    
def toggle_led2(timer):
    led2.toggle()
    
def toggle_led3(timer):
    led3.toggle()
    
def toggle_led4(timer):
    led4.toggle()

# initialize the timer object to tick every second (1,000 milliseconds)
# myTimer1.init(period=1000, mode=Timer.PERIODIC, callback=toggle_led1)
# myTimer2.init(period=500, mode=Timer.PERIODIC, callback=toggle_led2)
# myTimer3.init(period=250, mode=Timer.PERIODIC, callback=toggle_led3)
# myTimer4.init(period=125, mode=Timer.PERIODIC, callback=toggle_led4)

def timer_update():
    if timer1:
        myTimer1.init(period=1000, mode=Timer.PERIODIC, callback=toggle_led1)
    else:
        myTimer1.deinit() 
    if timer2:
        myTimer2.init(period=500, mode=Timer.PERIODIC, callback=toggle_led2)
    else:
        myTimer2.deinit() 
    if timer3:
        myTimer3.init(period=250, mode=Timer.PERIODIC, callback=toggle_led3)
    else:
        myTimer3.deinit() 
    if timer4:
        myTimer4.init(period=125, mode=Timer.PERIODIC, callback=toggle_led4)
    else:
        myTimer4.deinit() 

while True:
    timer_update()
    sleep(1)
