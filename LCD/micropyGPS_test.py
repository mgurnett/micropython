from machine import Pin, UART
import utime
from micropyGPS import MicropyGPS

# Initialize GPS module
gps_module = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))
time_zone = -6
gps = MicropyGPS(time_zone)

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

    data = '{0:.6f}'.format(data)  # 6 decimal places
    return str(data)

while True:
    length = gps_module.any()
    if length > 0:
        data = gps_module.read(length)
        for byte in data:
            message = gps.update(chr(byte))
    print (f"Satellites in view: {gps.satellites_in_view}, in use {gps.satellites_in_use}, and {gps.satellites_used}")
    print (f"timestamp is {gps.timestamp} and date is {gps.date}")

    latitude = convert_coordinates(gps.latitude)
    longitude = convert_coordinates(gps.longitude)

    if latitude is None or longitude is None:
        continue
    print('Lat: ' + latitude)
    print('Lon: ' + longitude)

    utime.sleep_ms(100)  # Add a 100ms delay between GPS updates