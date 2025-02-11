import utime

import machine
from machine import I2C
from lcd_api import LcdApi
from i2c_lcd import I2cLcd

I2C_ADDR     = 0x27
I2C_NUM_ROWS = 4
I2C_NUM_COLS = 20

i2c = I2C(0, sda=machine.Pin(0), scl=machine.Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

'''
lcd.hide_cursor()
lcd.blink_cursor_on()
lcd.blink_cursor_off()
lcd.backlight_off()
lcd.backlight_on()
lcd.display_off()
lcd.display_on()
lcd.clear()
lcd.move_to (x, y)
'''