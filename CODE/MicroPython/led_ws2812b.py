import machine, neopixel

class NeoPixel:
    def __init__(self, pin=15, n=24):
        self.pin = machine.Pin(pin)
        self.n = n
        self.np = neopixel.NeoPixel(self.pin, self.n)

    def set_color(self, r, g, b):
        """Sets all pixels to the same color."""
        for i in range(self.n):
            self.np[i] = (r, g, b)
        self.np.write()

    def set_pixel(self, i, r, g, b):
        """Sets a single pixel color."""
        if 0 <= i < self.n:
            self.np[i] = (r, g, b)
            self.np.write()

    def clear(self):
        self.set_color(0, 0, 0)

#*** RUNTIME EXAMPLE ***
# np = NeoPixel(pin=18, n=16)
# np.set_color(10, 0, 0)
