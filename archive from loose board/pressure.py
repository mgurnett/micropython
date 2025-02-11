import machine
import time

pressure = machine.ADC(0)

while True:
    pressure_value = pressure.read_u16()
    print (pressure_value)
    time.sleep(.5)