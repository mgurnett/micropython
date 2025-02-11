
# Use an interrupt function count the number of times a button has been pressed
from machine import Pin
import micropython
import time
from pin_out import *

# global value
button_pressed_count = 0

# Interrupt Service Routine for Button Pressed Events - with no debounce
def button1_pressed(change):
    global button_pressed_count
    button_pressed_count += 1

# we define button1 as being connected to GP14 and to use the internal Pico PULL_DOWN resistor
# button1 = Pin(14, Pin.IN, Pin.PULL_DOWN)

# here is how we associate the falling value on the input pin with the callback function
buttonK1.irq(handler=button1_pressed, trigger=Pin.IRQ_FALLING)

button_pressed_count_old = 0
while True:
    if button_pressed_count_old != button_pressed_count:
       print('Button 1 value:', button_pressed_count)
       button_pressed_count_old = button_pressed_count