from machine import Pin
import micropython
import utime        
from datetime import datetime
from pin_out import *
from oled_setup import *

BOX = purple
FONT_COLOUR = red
HIGHLIGHT_BOX = red
HIGHLIGHT_FONT_COLOUR = purple

def board_temp():
    conversion_factor = 3.3 / (65535)
    reading = sensor_temp.read_u16() * conversion_factor 
    temperature = round(27 - (reading - 0.706)/0.001721, 1)
    return f'{temperature}C'
    

def menu_item (pos, text, highlight = False):
    box = BOX
    font_color = FONT_COLOUR
    top_pos = pos*40+10
    bottom_pos = 30
    if highlight:
        font_color = HIGHLIGHT_FONT_COLOUR
        box = HIGHLIGHT_BOX
        
    display.fill_rectangle(15, top_pos, 215, bottom_pos, color=box)
    display.set_color(font_color, box)
    display.set_pos(30,top_pos+3)
    display.set_font(tt24)
    display.print(text)

display.erase()
 # TODO Fix it sow that the menu does not redraw everything
while True:
    now = datetime.now()
    message = f'{now:%M:%S} LOGGED'
    menu_item (1, message, highlight = False)
    temp = board_temp()
    print (temp)
    menu_item (1, temp, highlight = False)
    utime.sleep_ms(3000)
