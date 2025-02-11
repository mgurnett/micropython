from machine import Pin, ADC

buttonK4= Pin(5, Pin.IN, Pin.PULL_UP)
buttonK3= Pin(4, Pin.IN, Pin.PULL_UP)
buttonK2= Pin(3, Pin.IN, Pin.PULL_UP)
buttonK1= Pin(2, Pin.IN, Pin.PULL_UP)

led1 = Pin(21, Pin.OUT)
led2 = Pin(20, Pin.OUT)
led3 = Pin(19, Pin.OUT)
led4 = Pin(18, Pin.OUT)

sensor_temp = ADC(4)