"""ILI9341 demo (simple touch demo)."""
from ili9341 import Display, color565
from xpt2046 import Touch
from machine import idle, Pin, SPI  # type: ignore
import time


class Demo(object):
    """Touchscreen simple demo."""
    CYAN = color565(0, 255, 255)
    PURPLE = color565(255, 0, 255)
    WHITE = color565(255, 255, 255)

    def __init__(self, display, spi1):
        """Initialize box.
        Args:
            display (ILI9341): display object
            spi2 (SPI): SPI bus
        """
        self.display = display
        self.touch = Touch(spi1, cs=Pin(12))
        # Display initial message
        self.display.draw_text8x8(self.display.width // 2 - 32,
                                  self.display.height - 9,
                                  "TOUCH ME",
                                  self.WHITE,
                                  background=self.PURPLE)

        # A small 5x5 sprite for the dot
        self.dot = bytearray(b'\x00\x00\x07\xE0\xF8\x00\x07\xE0\x00\x00\x07\xE0\xF8\x00\xF8\x00\xF8\x00\x07\xE0\xF8\x00\xF8\x00\xF8\x00\xF8\x00\xF8\x00\x07\xE0\xF8\x00\xF8\x00\xF8\x00\x07\xE0\x00\x00\x07\xE0\xF8\x00\x07\xE0\x00\x00')
        print('initialize done!')
        print("begin to touch")
        while True:
            time.sleep(0.1)
            # get raw touch information.
            # ret = self.touch.raw_touch()
            ret = self.touch.get_touch()
            if ret is not None:
                
                print(ret)
                x = ret[0]
                y = ret[1]
                # Y needs to be flipped
                # y = (self.display.height - 1) - y
                # Display coordinates
                self.display.draw_text8x8(self.display.width // 2 - 32,
                                          self.display.height - 9,
                                          "{0:03d}, {1:03d}".format(x, y),
                                          self.CYAN)
                 

def test():
    """Test code."""
    spi2 = SPI(0, baudrate=40000000, sck=Pin(6), mosi=Pin(7))
    display = Display(spi2, dc=Pin(15), cs=Pin(13), rst=Pin(14))
    
    
    spi1 = SPI(1, baudrate=1000000, sck=Pin(10), mosi=Pin(11), miso=Pin(8))

    Demo(display, spi1)

    try:
        while True:
            idle()

    except KeyboardInterrupt:
        print("\nCtrl-C pressed.  Cleaning up and exiting...")
    finally:
        display.cleanup()


test()