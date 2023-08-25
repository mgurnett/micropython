from machine import Pin, UART, I2C
import utime
from board_devices import blink_led, board_temp
from lcd_setup import *
from wifi_con import wifi_connect
from constants import *
import network   # handles connecting to WiFiimport machine
from micropyGPS import MicropyGPS
from PicoDHT22 import PicoDHT22

# Initialize GPS module
gps_module = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))
time_zone = -6 #MDT
gps = MicropyGPS(time_zone)

dht22 = PicoDHT22(Pin(2,Pin.IN,Pin.PULL_UP))

def convert_coordinates(sections):
    if sections[0] == 0:  # sections[0] contains the degrees
        return None

    # sections[1] contains the minutes
    data = sections[0] + (sections[1] / 60.0)

    # sections[2] contains 'E', 'W', 'N', 'S'
    if sections[2] == 'S':
        data = -data
    if sections[2] == 'W':
        data = -data

    data = '{0:.8f}'.format(data)  # 6 decimal places
    return str(data)

def display_time():
        #get time
        time = utime.localtime() 
        
        display_string = f"{time[0]:>04d}/{time[1]:>02d}/{time[2]:>02d} {time[3]:>02d}:{time[4]:>02d}:{time[5]:>02d}"
        return display_string

def display_temp_board():
        #get board temp
        display_string = f"{str(board_temp())}\xdfC"
        return display_string

def display_temp_dht22():
        #get dht22 temp and humidity
        T, H = dht22.read()
        display_string = f"T={T:3.1f}\xdfC H={H:3.1f}%"
        return display_string

def display_ip():
        #get ip address
        ip = wifi_connect()
        display_string = f"Connected on \n {ip}"
        return display_string

def display_gps():
        #get ip address
        length = gps_module.any()
        if length > 0:
            data = gps_module.read(length)
            for byte in data:
                message = gps.update(chr(byte))  #this gets any updates to teh data
#         print (f"Satellites in view: {gps.satellites_in_view}, in use {gps.satellites_in_use}, and {gps.satellites_used}")
#         print (f"timestamp is {gps.timestamp} and date is {gps.date}")

        latitude = convert_coordinates(gps.latitude)
        longitude = convert_coordinates(gps.longitude)

#         if latitude is None or longitude is None:
#             continue
#         print('Lat: ' + latitude)
#         print('Lon: ' + longitude)
        ll_string = f" Lat: {latitude} \n Lon: {longitude}"
#         td_string = f"timestamp: {gps.timestamp[0]} \n date: {gps.date}"
        time_string = f"GPS time: {gps.timestamp[0]:>02d}:{gps.timestamp[1]:>02d}:{int(gps.timestamp[2])}"
        date_string = f"date: {gps.date[0]:>02d}:{gps.date[1]:>02d}:{gps.date[2]+2000:>04d}"
#         f"{time[0]:>04d}/{time[1]:>02d}/{time[2]:>02d} {time[3]:>02d}:{time[4]:>02d}:{time[5]:>02d}"
        display_string = [ll_string, time_string, date_string]
        return display_string
    

if __name__ == "__main__":
    
    while True:
        lcd.clear()
        lcd.move_to (0, 3)
        lcd.putstr(display_time())
        lcd.move_to (0, 0)
        lcd.putstr(display_temp_board())
        blink_led ("running", 2) #a 2s delay with LED blinks
        board_led_red.value(0)
        board_led_yellow.value(1)  #TODO look into LED toggle
        
        lcd.clear()
        lcd.move_to (0, 3)
        lcd.putstr(display_time())
        lcd.move_to (0, 0)
        lcd.putstr(display_temp_dht22())
        blink_led ("running", 2) #a 2s delay with LED blinks
        board_led_red.value(1)
        board_led_yellow.value(0)
        
        lcd.clear()
        lcd.move_to (0, 3)
        lcd.putstr(display_time())
        lcd.move_to (0, 0)
        lcd.putstr(display_ip())
        blink_led ("running", 2) #a 2s delay with LED blinks
        board_led_red.value(0)
        board_led_yellow.value(1)
        
        lcd.clear()  #TODO break this up into timestamp on 0 and 1 and date on 2 and 3
        lcd.move_to (0, 3)
        lcd.putstr(display_time())
        lcd.move_to (0, 0)
        lcd.putstr(display_gps()[0])
        blink_led ("running", 2) #a 2s delay with LED blinks
        lcd.move_to (0, 0)
        lcd.putstr(display_gps()[1])
        lcd.move_to (0, 1)
        lcd.putstr(display_gps()[2])
        blink_led ("running", 2) #a 2s delay with LED blinks
        board_led_red.value(1)
        board_led_yellow.value(0)