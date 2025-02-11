import machine
import utime
 
def led_blink (on_time, off_time):
    board_led.value(1)
    utime.sleep(on_time)
    board_led.value(0)
    utime.sleep(off_time)
            
def board_temp():
    conversion_factor = 3.3 / (65535)
    reading = sensor_temp.read_u16() * conversion_factor 
    temperature = round(27 - (reading - 0.706)/0.001721, 1)
    return temperature  #float
    
if __name__ == "__main__":
    blink_led ('running', 5)
    print (str(board_temp()))
    while True:
        board_led_red.value(0)
        board_led_yellow.value(0)
        if button.value() == 0:
            board_led_red.value(0)
            board_led_yellow.value(1)
        else:
            board_led_red.value(1)
            board_led_yellow.value(0)
    
