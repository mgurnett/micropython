from machine import Pin
import micropython
import utime
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
    display.erase()
    

def down_button_handler(pin):
    global change, menu_number
    # disable the IRQ during our debounce check
    buttonK3.irq(handler=None)
    # debounce time - we ignore any activity diring this period 
    utime.sleep_ms(300)
    # re-enable the IRQ
    buttonK3.irq(trigger=machine.Pin.IRQ_FALLING, handler = down_button_handler)
    print ('***up button pressed***')
    change = True
    menu_number +=1
    if menu_number > 6:
        menu_number = 0

def up_button_handler(pin):
    global change, menu_number
    # disable the IRQ during our debounce check
    buttonK4.irq(handler=None)
    # debounce time - we ignore any activity diring this period 
    utime.sleep_ms(300)
    # re-enable the IRQ
    buttonK4.irq(trigger=machine.Pin.IRQ_FALLING, handler = up_button_handler)
    print ('***down button pressed***')
    change = True
    menu_number -=1
    if menu_number < 0:
        menu_number = 6

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
    
def manage_menu():
    if menu_number == 0:
        menu_item (0, "Onboard Temp")
    else:
        menu_item (0, "On-board Temp", highlight = True)
        
    if menu_number == 1:
        menu_item (1, "Two")
    else:
        menu_item (1, "Two", highlight = True)
        
    if menu_number == 2:
        menu_item (2, "Three")
    else:
        menu_item (2, "Three", highlight = True)
        
    if menu_number == 3:
        menu_item (3, "Four")
    else:
        menu_item (3, "Four", highlight = True)
        
    if menu_number == 4:
        menu_item (4, "Five")
    else:
        menu_item (4, "Five", highlight = True)
        
    if menu_number == 5:
        menu_item (5, "Six")
    else:
        menu_item (5, "Six", highlight = True)
        
    if menu_number == 6:
        menu_item (6, "Seven")
    else:
        menu_item (6, "Seven", highlight = True)
    return
    
    
buttonK4.irq(trigger=machine.Pin.IRQ_FALLING, handler = up_button_handler)
buttonK3.irq(trigger=machine.Pin.IRQ_FALLING, handler = down_button_handler)
display.erase()
change = True
menu_number = 0  # TODO Fix it sow that the menu does not redraw everything
while True:
    if change:
        manage_menu()
        change = False
        
        