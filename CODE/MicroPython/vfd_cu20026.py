from machine import Pin
import time

class VFD:
    def __init__(self):
        # Initialize Control Pins
        #self.ts = Pin(0, Pin.OUT, value = 1) # VFD pin 25 (boot (+))
        #self.cs = Pin(??, Pin.OUT, value=0) # VFD pin 23 (fixed (-))
        #self.rs = Pin( 2, Pin.OUT, value = 0) # VFD pin 20 (boot (-))
        self.a0 = Pin(18, Pin.OUT, value = 0) # VFD pin 19
        self.wr = Pin(19, Pin.OUT, value = 1) # VFD pin 17

        # Initialize 8-bit Data Bus (D0-D7)
        self.data_pins = [Pin(p, Pin.OUT) for p in [32, 33, 25, 26, 27, 14, 12, 13]]

        self.init_vfd()

    def _write_8bit(self, value):
        for i in range(8):
            self.data_pins[i].value((value >> i) & 0x01)

    def _send_byte(self, byte, is_data=True):
        #self.cs.value(0)
        self.a0.value(0 if is_data else 1)
        self._write_8bit(byte)
        # Strobe WR (Falling edge latches data)
        self.wr.value(0)
        time.sleep_us(1)
        self.wr.value(1)
        #self.cs.value(1)

    def init_vfd(self):
        #self.rs.value(1)
        time.sleep_ms(10)
        #self.rs.value(0)
        time.sleep_ms(100)

    def data_write(self, text):
        for char in text:
            self._send_byte(ord(char), is_data=True)

    def data_control(self, control):
        self._send_byte(control, is_data=True) # Data Control "DC1" thru "DC6"

    def command_write(self, cmd):
        for char in text:
            self._send_byte(ord(char), is_data=False)

    def clear_display(self):
        self._send_byte(0x0E, is_data=False) # Example clear command

    def cursor_reset(self):
        self._send_byte(0x00, is_data=False) # Top Line, Most Left

    def cursor_off(self):
        self._send_byte(0x15, is_data=True) # Top Line, Most Left

#*** RUNTIME EXAMPLE ***
# vfd = VFD()
# vfd.display_text("Hello World")
