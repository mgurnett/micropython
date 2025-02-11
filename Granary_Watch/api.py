from phew import server, connect_to_wifi
import machine
import json

ip = connect_to_wifi("YOUR_SSID", "YOUR_PASSWORD")

led_green = machine.Pin(0, machine.Pin.OUT)
led_red = machine.Pin(1, machine.Pin.OUT)

print("connected to IP ", ip)

@server.route("/api/temperature", methods=["GET"])
def get_temperature(request):
    adc = machine.ADC(4)  # Use ADC pin GP4
    conversion_factor = 3.3 / (65535)  # ADC conversion factor
    sensor_value = adc.read_u16() * conversion_factor
    temperature = 27 - (sensor_value - 0.706) / 0.001721  # Convert sensor value to temperature (formula may vary)
    
    return json.dumps({"temperature" : temperature}), 200, {"Content-Type": "application/json"}

@server.route("/api/control-led", methods=["POST"])
def ledCommand(request):
    led_red.value(request.data["ledRed"])
    led_green.value(request.data["ledGreen"])
    return json.dumps({"message" : "Command sent successfully!"}), 200, {"Content-Type": "application/json"}

@server.catchall()
def catchall(request):
    return json.dumps({"message" : "URL not found!"}), 404, {"Content-Type": "application/json"}

server.run()
