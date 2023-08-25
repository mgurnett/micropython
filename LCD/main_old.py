import machine
import utime
# from wifi_details import *
from lcd_setup import *

def test_main():
    lcd.clear()
    #lcd.putstr("It Works!")

'''
wifi_fail()

try:
    ip = connect()
    print(f'Connected on {ip}')
except KeyboardInterrupt:
    wifi_fail()
    machine.reset()

connected()
'''

'''
lcd.hide_cursor()
lcd.blink_cursor_on()
lcd.blink_cursor_off()
lcd.backlight_off()
lcd.backlight_on()
lcd.display_off()
lcd.display_on()
lcd.clear()
'''

if __name__ == "__main__":
    test_main()
    sensor_temp = machine.ADC(4)
    conversion_factor = 3.3 / (65535)
    reading = sensor_temp.read_u16() * conversion_factor 
    temperature = round(27 - (reading - 0.706)/0.001721, 1)
    lcd.putstr(str(temperature))
    