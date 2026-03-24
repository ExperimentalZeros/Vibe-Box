from machine import Pin, SPI

# VSPI: SCK=18, MOSI=23, MISO=19 (Bridge 23/19 with 1k resistor)
spi = SPI(2, baudrate=100000, firstbit=SPI.LSB)
cs = Pin(5, Pin.OUT, value=0)

def op(reg, val=None):
    cs.on()
    if val is None: # Burst Read all 7 clock registers
        spi.write(b'\xbf')
        b = spi.read(7)
        cs.off()
        # Convert BCD to Decimal: [SS, MN, HR, DD, MM, WK, YY]
        return [((x >> 4) * 10) + (x & 15) for x in b]
    # Single Write: Address | Register, followed by BCD Data
    spi.write(bytearray([128 | reg << 1, (val // 10) << 4 | val % 10]))
    cs.off()

def get_time():
    t = op(0) # Returns list: [SS, MN, HR, DD, MM, WK, YY]
    return t[6], t[4], t[3], t[2], t[1], t[0] # Returns Y, M, D, H, M, S

def set_time(y, m, d, h, n, sc):
    op(7, 0) # Unlock Write Protect
    for r, v in zip((6, 4, 3, 2, 1, 0), (y % 100, m, d, h, n, sc)):
        op(r, v)
