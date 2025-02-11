import machine
import time
import os

# Function to read temperature sensor
def read_temperature():
    adc = machine.ADC(4)  # Use ADC pin GP4
    conversion_factor = 3.3 / (65535)  # ADC conversion factor
    sensor_value = adc.read_u16() * conversion_factor
    temperature = 27 - (sensor_value - 0.706) / 0.001721  # Convert sensor value to temperature (formula may vary)
    return temperature

# Function to log temperature data to CSV file
def log_temperature():
    file_name = "temperature_log.csv"
    timestamp = time.localtime()
    temperature = read_temperature()
    print(temperature)
    
    timestamp_str = format_timestamp(timestamp)
    # Check if CSV file exists, if not create it with header
    if not file_name in os.listdir():
        with open(file_name, 'w') as file:
            file.write('Timestamp,Temperature (°C)\n')
    
    # Append temperature data to CSV file
    with open(file_name, 'a') as file:
        file.write('{},{:.2f}\n'.format(timestamp_str, temperature))

def format_timestamp(timestamp):
    year, month, day, hour, minute, second, *_ = timestamp
    timestamp_str = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(year, month, day, hour, minute, second)
    return timestamp_str

# Function to read temperature data from CSV file
def read_temperature_log():
    file_name = "temperature_log.csv"
    temperature_data = []
    # Check if CSV file exists
    if file_name in os.listdir():
        with open(file_name, 'r') as file:
            # Skip header line
            next(file)
            # Read each line and parse data
            for line in file:
                parts = line.strip().split(',')
                if len(parts) >= 2:
                    timestamp = parts[0].strip('(')  # Remove any extra characters from the timestamp
                    temperature = float(parts[1])
                    temperature_data.append((timestamp, temperature))
                else:
                    print("Invalid line:", line)
    
    return temperature_data

counter = 0
# Example usage: Log temperature every 5 seconds
while True:
    counter += 1
    if counter <=5:
        log_temperature()
    else:
        print(read_temperature_log())
        counter = 0
    time.sleep(2)
