from machine import Pin, I2C
import utime
from lcd_setup import *


def display_time():
        #get time
        time = utime.localtime() 
        
        display_string = f"{time[0]:>04d}/{time[1]:>02d}/{time[2]:>02d} {time[3]:>02d}:{time[4]:>02d}:{time[5]:>02d}"
        return display_string
    
if __name__ == "__main__":
    
    while True:
        lcd.clear()
        lcd.move_to (0, 3)
        lcd.putstr(display_time())
        utime.sleep(1)