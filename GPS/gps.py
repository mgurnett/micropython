from machine import Pin, UART, I2C
import utime, time
from board_devices import blink_led, board_temp
from lcd_setup import *
from wifi_con import wifi_connect
from constants import *

def convertToDegree(RawDegrees):

    RawAsFloat = float(RawDegrees)
    firstdigits = int(RawAsFloat/100) 
    nexttwodigits = RawAsFloat - float(firstdigits*100) 
    
    Converted = float(firstdigits + nexttwodigits/60.0)
    Converted = '{0:.6f}'.format(Converted) 
    return str(Converted)

def getGPS(gpsModule):
    global FIX_STATUS, TIMEOUT, latitude, longitude, satellites, GPStime
    
    timeout = time.time() + 8 
    while True:
        board_led_red.value(1)
#         board_led_yellow.value(0)
#         lcd.clear()
        lcd.move_to (0,0)
        lcd.putstr("looking for \n satellites")
        gpsModule.readline()
        buff = str(gpsModule.readline())
        parts = buff.split(',')
        print (parts[0])
        
        lcd.move_to (0,2)
        lcd.putstr(parts[0]+"         ")
             
        if (parts[0] == "b'$GPGGA" and len(parts) == 15):  
            board_led_red.value(0)
            board_led_yellow.value(1)
            lcd.move_to (5,3)
            lcd.putstr("FOUND!!!")
            if(parts[1] and parts[2] and parts[3] and parts[4] and parts[5] and parts[6] and parts[7]):
                
                latitude = convertToDegree(parts[2])
                if (parts[3] == 'S'):
                    latitude = -latitude
                longitude = convertToDegree(parts[4])
                if (parts[5] == 'W'):
                    longitude = -longitude
                satellites = parts[7]
                GPStime = parts[1][0:2] + ":" + parts[1][2:4] + ":" + parts[1][4:6]
                FIX_STATUS = True
                break
                
        if (time.time() > timeout):
            TIMEOUT = True
            break
        utime.sleep_ms(500)
    
if __name__ == "__main__":
    gpsModule = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))
    print(gpsModule)

    buff = bytearray(255)

    TIMEOUT = False
    FIX_STATUS = False

    latitude = ""
    longitude = ""
    satellites = ""
    GPStime = ""
        
 
    while True:
        
        getGPS(gpsModule)

        if(FIX_STATUS == True):
            print("Printing GPS data...")
            print(" ")
            print("Latitude: "+latitude)
            print("Longitude: "+longitude)
            print("Satellites: " +satellites)
            print("Time: "+GPStime)
            print("----------------------")
            
            lcd.clear()
            lcd.move_to (0,0)
            display_string = f"lat: {latitude}"
            lcd.putstr(display_string)
            lcd.move_to (0,1)
            display_string = f"long: {longitude}"
            lcd.putstr(display_string)
            lcd.move_to (0,2)
            display_string = f"Satellites: {satellites}"
            lcd.putstr(display_string)
            lcd.move_to (0,3)
            display_string = f"Time: {GPStime}"
            lcd.putstr(display_string)
            
            FIX_STATUS = False
            
        if(TIMEOUT == True):
            print("No GPS data is found.")
            lcd.clear()
            lcd.putstr("No GPS data is found.")
            
            TIMEOUT = False
