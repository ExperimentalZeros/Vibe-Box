from machine import I2C, Pin
import utime

class PCF8591:
    def __init__(self, i2c_bus, address=0x48):
        self.i2c = i2c_bus
        self.address = address
        # Control Byte: 0x40 enables DAC output
        self.BASE_CONTROL = 0x40

    def _read_channel(self, channel):
        """Selects channel and returns the current 8-bit conversion."""
        if not (0 <= channel <= 3): return None

        # 1. Select channel
        self.i2c.writeto(self.address, bytearray([self.BASE_CONTROL | channel]))

        # 2. Dummy read: The first read returns the result of the PREVIOUS conversion
        self.i2c.readfrom(self.address, 1)

        # 3. Actual read: Returns the current conversion
        return self.i2c.readfrom(self.address, 1)[0]

    def get_pot(self):
        """AIN0: Adjustable Potentiometer (0-255). Note: Hardware mapping varies."""
        return self._read_channel(0)

    def get_ldr(self):
        """AIN1: Photoresistor. Lower values = brighter light."""
        return self._read_channel(1)

    def get_diode(self):
        """AIN2: Diode. Lower values = higher temperature."""
        return self._read_channel(2)

    def set_dac(self, value):
        """Sets analog output voltage (AOUT pin) from 0-255."""
        self.i2c.writeto(self.address, bytearray([self.BASE_CONTROL, value]))

#*** RUNTIME EXAMPLE ***
# from machine import I2C, Pin
# i2c = I2C(0, scl=Pin(22), sda=Pin(21))
# exp = PCF8591(i2c)
# print(exp.get_pot())
