import machine
import utime

board_led = machine.Pin('LED', machine.Pin.OUT)
 
def led_blink (on_time, off_time):
    board_led.value(1)
    utime.sleep(on_time)
    board_led.value(0)
    utime.sleep(off_time)
    
def blink_led (style, number):
    if style == "waiting":
        for x in range (number + 1):
            led_blink (1,0.4)
    if style == "warning":
        for x in range (number + 1):
            led_blink (0.3,0.3)
    if style == "running":
        for x in range (number + 1):
            led_blink (0.2,0.8)
            
    blink_led ("running", 10)
    test_main()
    sensor_temp = machine.ADC(4)
    conversion_factor = 3.3 / (65535)
    reading = sensor_temp.read_u16() * conversion_factor 
    temperature = round(27 - (reading - 0.706)/0.001721, 1)
    lcd.putstr(str(temperature))
    
if __name__ == "__main__":
    #sensor_temp = machine.ADC(4)
    #conversion_factor = 3.3 / (65535)
    #reading = sensor_temp.read_u16() * conversion_factor 
    #temperature = round(27 - (reading - 0.706)/0.001721, 1)
    #lcd.putstr(str(temperature))
    blink_led ('running', 5)
    