import time
import ubinascii
from machine import Pin, SPI
import onewire
import ds18x20

from ili934xnew import ILI9341, color565
import glcdfont
import tt14
import tt24
import tt32
from colours import *

# ==============================================================================
# DISPLAY CONFIGURATION (ILI9341 SPI)
# ==============================================================================
SCR_WIDTH = const(320)
SCR_HEIGHT = const(240)
SCR_ROT = const(2)

TFT_CLK_PIN = const(6)
TFT_MOSI_PIN = const(7)
TFT_MISO_PIN = const(4)
TFT_CS_PIN = const(13)
TFT_RST_PIN = const(14)
TFT_DC_PIN = const(15)

spi = SPI(
    0,
    baudrate=40000000,
    miso=Pin(TFT_MISO_PIN),
    mosi=Pin(TFT_MOSI_PIN),
    sck=Pin(TFT_CLK_PIN),
)

display = ILI9341(
    spi,
    cs=Pin(TFT_CS_PIN),
    dc=Pin(TFT_DC_PIN),
    rst=Pin(TFT_RST_PIN),
    w=SCR_WIDTH,
    h=SCR_HEIGHT,
    r=SCR_ROT,
)

# ==============================================================================
# 1-WIRE / DS18X20 CONFIGURATION
# ==============================================================================
# DS18B20 data line (DQ) is connected to GPIO 22.
# Note: When powering sensor at 5V, ensure DQ pull-up (4.7k) connects to 3.3V
# to keep GPIO voltage within Raspberry Pi Pico safe limits (3.3V max).
DS_PIN_NUM = const(22)
ds_pin = Pin(DS_PIN_NUM)
ow = onewire.OneWire(ds_pin)
ds_sensor = ds18x20.DS18X20(ow)

# Card background colors for distinct sensors
CARD_COLORS = [
    color565(35, 35, 65),    # Navy / Slate
    color565(55, 30, 60),    # Dark Plum
    color565(25, 55, 45),    # Dark Teal
    color565(60, 45, 20),    # Dark Amber
    color565(50, 50, 50),    # Neutral Dark Gray
]


def format_rom(rom, separator=":"):
    """Format ROM bytearray as uppercase hex string."""
    hex_str = ubinascii.hexlify(rom).decode().upper()
    if separator:
        return separator.join(hex_str[i : i + 2] for i in range(0, len(hex_str), 2))
    return hex_str


def draw_header(num_sensors):
    """Draw title bar and count of detected sensors."""
    display.fill_rectangle(0, 0, 240, 36, color=dark_gray)
    display.set_color(white, dark_gray)
    display.set_pos(10, 6)
    display.set_font(tt24)
    display.print("DS1820 Network")

    count_text = f"({num_sensors})"
    display.set_color(cyan, dark_gray)
    display.set_pos(190, 9)
    display.set_font(tt14)
    display.print(count_text)


def show_scanning_screen():
    """Display scan status while looking for 1-Wire devices."""
    display.erase()
    display.fill_rectangle(0, 0, 240, 36, color=dark_gray)
    display.set_color(white, dark_gray)
    display.set_pos(10, 6)
    display.set_font(tt24)
    display.print("DS1820 Network")

    display.set_color(yellow, black)
    display.set_pos(15, 60)
    display.set_font(tt14)
    display.print("Scanning 1-Wire bus...")
    display.set_pos(15, 85)
    display.print(f"GPIO {DS_PIN_NUM} (5V, 4.7k pullup)")


def show_no_sensors_screen():
    """Display error message when no sensors respond on the line."""
    display.fill_rectangle(0, 40, 240, 280, black)
    display.set_color(red, black)
    display.set_pos(15, 60)
    display.set_font(tt24)
    display.print("No Sensors Found!")

    display.set_color(yellow, black)
    display.set_pos(15, 100)
    display.set_font(tt14)
    display.print("Please check:")
    display.set_pos(15, 125)
    display.print(f"1. Data line on GPIO {DS_PIN_NUM}")
    display.set_pos(15, 145)
    display.print("2. 4.7k pull-up to 3.3V")
    display.set_pos(15, 165)
    display.print("3. 5V power and GND pins")


def draw_sensor_card_skeleton(idx, total, rom, card_y, card_h, bg_color):
    """Draw the static background card, sensor badge, and ROM address."""
    card_w = 224
    card_x = 8

    # Background card
    display.fill_rectangle(card_x, card_y, card_w, card_h, color=bg_color)

    # Accent left border strip
    accent_color = [cyan, magenta, green, yellow, lavender][idx % 5]
    display.fill_rectangle(card_x, card_y, 4, card_h, color=accent_color)

    rom_str = format_rom(rom)

    if total == 1:
        # Layout for single sensor (large view)
        display.set_color(lavender, bg_color)
        display.set_pos(card_x + 10, card_y + 8)
        display.set_font(tt14)
        display.print("Sensor Address (ROM):")

        display.set_color(white, bg_color)
        display.set_pos(card_x + 10, card_y + 28)
        display.set_font(glcdfont)
        display.print(rom_str)

        display.set_color(light_gray, bg_color)
        display.set_pos(card_x + 10, card_y + 55)
        display.set_font(tt14)
        display.print("Temperature:")

    elif total == 2:
        # Layout for 2 sensors
        display.set_color(accent_color, bg_color)
        display.set_pos(card_x + 10, card_y + 8)
        display.set_font(tt14)
        display.print(f"Sensor #{idx + 1}")

        display.set_color(white, bg_color)
        display.set_pos(card_x + 10, card_y + 26)
        display.set_font(glcdfont)
        display.print(rom_str)

    elif total == 3 or total == 4:
        # Compact layout for 3 to 4 sensors
        display.set_color(accent_color, bg_color)
        display.set_pos(card_x + 10, card_y + 6)
        display.set_font(tt14)
        display.print(f"#{idx + 1}")

        display.set_color(white, bg_color)
        display.set_pos(card_x + 36, card_y + 8)
        display.set_font(glcdfont)
        display.print(rom_str)

    else:
        # Ultra-compact layout for 5+ sensors
        display.set_color(accent_color, bg_color)
        display.set_pos(card_x + 8, card_y + 4)
        display.set_font(glcdfont)
        display.print(f"#{idx + 1} {rom_str}")


def update_sensor_temp(idx, total, temp_c, card_y, card_h, bg_color):
    """Draw the temperature values inside a sensor's card."""
    card_x = 8
    card_w = 224

    if temp_c is None:
        temp_c_str = "--.- C"
        temp_f_str = ""
    else:
        temp_f = (temp_c * 9.0 / 5.0) + 32.0
        temp_c_str = f"{temp_c:.1f} C"
        temp_f_str = f"({temp_f:.1f} F)"

    if total == 1:
        # Single sensor: big fonts
        display.fill_rectangle(card_x + 10, card_y + 75, card_w - 20, 48, bg_color)
        display.set_color(cyan, bg_color)
        display.set_pos(card_x + 16, card_y + 78)
        display.set_font(tt32)
        display.print(temp_c_str)

        display.set_color(lavender, bg_color)
        display.set_pos(card_x + 130, card_y + 90)
        display.set_font(tt14)
        display.print(temp_f_str)

    elif total == 2:
        # 2 sensors
        display.fill_rectangle(card_x + 10, card_y + 46, card_w - 20, 56, bg_color)
        display.set_color(cyan, bg_color)
        display.set_pos(card_x + 14, card_y + 50)
        display.set_font(tt32)
        display.print(temp_c_str)

        display.set_color(lavender, bg_color)
        display.set_pos(card_x + 130, card_y + 60)
        display.set_font(tt14)
        display.print(temp_f_str)

    elif total == 3:
        # 3 sensors
        display.fill_rectangle(card_x + 10, card_y + 30, card_w - 20, 36, bg_color)
        display.set_color(cyan, bg_color)
        display.set_pos(card_x + 14, card_y + 32)
        display.set_font(tt24)
        display.print(temp_c_str)

        display.set_color(lavender, bg_color)
        display.set_pos(card_x + 120, card_y + 36)
        display.set_font(tt14)
        display.print(temp_f_str)

    elif total == 4:
        # 4 sensors
        display.fill_rectangle(card_x + 10, card_y + 24, card_w - 20, 32, bg_color)
        display.set_color(cyan, bg_color)
        display.set_pos(card_x + 14, card_y + 26)
        display.set_font(tt24)
        display.print(temp_c_str)

        display.set_color(lavender, bg_color)
        display.set_pos(card_x + 120, card_y + 28)
        display.set_font(tt14)
        display.print(temp_f_str)

    else:
        # 5+ sensors
        display.fill_rectangle(card_x + 10, card_y + 16, card_w - 20, 20, bg_color)
        display.set_color(cyan, bg_color)
        display.set_pos(card_x + 14, card_y + 16)
        display.set_font(tt14)
        display.print(f"{temp_c_str}  {temp_f_str}")


def main():
    print("=" * 50)
    print(f"Starting Multi-DS1820 Monitor on GPIO {DS_PIN_NUM}")
    print("=" * 50)

    # Initial scanning loop
    roms = []
    while not roms:
        show_scanning_screen()
        roms = ds_sensor.scan()
        if not roms:
            print("No DS1820 sensors found on GPIO", DS_PIN_NUM)
            show_no_sensors_screen()
            time.sleep(3)

    num_sensors = len(roms)
    print(f"Discovered {num_sensors} DS1820 sensor(s) on the 1-Wire bus:")
    for i, rom in enumerate(roms):
        print(f"  [{i + 1}] {format_rom(rom)}")

    display.erase()
    draw_header(num_sensors)

    # Calculate layout geometry based on number of sensors
    available_height = 270  # from y=42 to y=312
    card_spacing = 6
    if num_sensors == 1:
        card_heights = [140]
    elif num_sensors <= 4:
        card_heights = [(available_height - (num_sensors - 1) * card_spacing) // num_sensors] * num_sensors
    else:
        # Cap to fit up to 6 on screen
        effective_count = min(num_sensors, 6)
        card_heights = [(available_height - (effective_count - 1) * 4) // effective_count] * num_sensors

    card_positions = []
    curr_y = 42
    for i in range(min(num_sensors, 6)):
        h = card_heights[i]
        bg = CARD_COLORS[i % len(CARD_COLORS)]
        card_positions.append((curr_y, h, bg))
        draw_sensor_card_skeleton(i, num_sensors, roms[i], curr_y, h, bg)
        curr_y += h + (card_spacing if num_sensors <= 4 else 4)

    # Dictionary to track last temperature for each sensor (to prevent flicker)
    last_temperatures = {}

    while True:
        try:
            # 1-Wire broadcast conversion: triggers conversion on ALL sensors simultaneously!
            ds_sensor.convert_temp()
            # Wait 750ms for 12-bit temperature conversion
            time.sleep_ms(750)

            # Read each sensor
            for idx, rom in enumerate(roms):
                if idx >= 6:
                    break  # Display up to 6 sensors on screen

                rom_key = bytes(rom)
                curr_y, h, bg = card_positions[idx]

                try:
                    temp_c = ds_sensor.read_temp(rom)
                except Exception as read_err:
                    print(f"Error reading sensor #{idx + 1} ({format_rom(rom)}):", read_err)
                    temp_c = None

                last_val = last_temperatures.get(rom_key)

                # Update screen only if value changed or was not set
                if temp_c != last_val:
                    update_sensor_temp(idx, num_sensors, temp_c, curr_y, h, bg)
                    last_temperatures[rom_key] = temp_c

                if temp_c is not None:
                    temp_f = (temp_c * 9.0 / 5.0) + 32.0
                    print(f"[#{idx + 1}] {format_rom(rom)} -> {temp_c:.2f} C ({temp_f:.2f} F)")

            print("-" * 40)
            time.sleep_ms(1000)

        except Exception as bus_err:
            print("1-Wire bus error:", bus_err)
            time.sleep_ms(1500)


if __name__ == "__main__":
    main()
