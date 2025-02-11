import utime
import urequests
import gc
import os
import machine, onewire, ds18x20, time
import constants as const
from board_devices import *
from wifi import *
from RTC import *
 
ip = None
SLEEP_TIME = 1000 * 90
temp_list = []
LEN_MAX = 10
MAX_STORAGE = 200
MIN_FREE = 80

if __name__ == "__main__":
    gc.enable()
    s = os.statvfs('/')
    print(f"Free storage: {s[0]*s[3]/1024} KB")
    print(f"Memory: {gc.mem_alloc()} of {gc.mem_free()} bytes used.")
    print(f"CPU Freq: {machine.freq()/1000000}Mhz")
    
    clear_display ()
    
    while ip == None:
        ip = get_wifi()
        if ip:
            menu_item (0,f'ip: {ip}')
            set_time(const.TZ)
        else:
            ip = None
            menu_item (0,f'ip: NOT SET')
            
    while True:
        gc.collect()
        memory = round(gc.mem_free()/1024, 1)
        menu_item (5, f"Memory: {memory}KB")
        fail_num = 0
        sleep_time_start = time.localtime()[3] * 3600 + time.localtime()[4] * 60 + time.localtime()[5]
        for sensor in const.SENSORS:
            temperature = board_temp()
            menu_item (2,str(f"Temp: {temperature}C"))
            time_str = f'{time.localtime()[0]}-{time.localtime()[1]}-{time.localtime()[2]} {time.localtime()[3]}:{time.localtime()[4]:02}:{time.localtime()[5]:02}'
            menu_item (1, time_str)
            log = {"recorded": time_str, "value": temperature, "sensor": sensor}
#             if len(temp_list) > MAX_STORAGE:
            if (gc.mem_free()/1024) < MIN_FREE:
                del temp_list [0]
            temp_list.append(log)
            menu_item (3,f'logs: {len(temp_list)}')
            gc.collect()
            memory = round(gc.mem_free()/1024, 1)
            menu_item (5, f"Memory: {memory}KB")
            
        while len(temp_list) > 0 and fail_num < 5: 
            menu_item (3,f'logs: {len(temp_list)}') 
            menu_item (4,f'Sending json')
            gc.collect()
            memory = round(gc.mem_free()/1024, 1)
            menu_item (5, f"Memory: {memory}KB")
            
            send_list = temp_list [0:LEN_MAX]
            try:
                response = urequests.post(const.URL, json=send_list)
                response.close()
            except:
                fail_num +=1             
                menu_item (3,f'logs: {len(temp_list)}')
                menu_item (4, f"upload attempt {fail_num}")
            else:             
                menu_item (4, f"response code {response.status_code}")
                del temp_list [0:LEN_MAX]
                menu_item (3,f'logs: {len(temp_list)}')
                fail_num = 0
        
        memory = round(gc.mem_free()/1024, 1)
        menu_item (5, f"Memory: {memory}KB")
        sleep_time_end = time.localtime()[3] * 3600 + time.localtime()[4] * 60 + time.localtime()[5]
        difference = sleep_time_end - sleep_time_start
        utime.sleep_ms(SLEEP_TIME - difference)