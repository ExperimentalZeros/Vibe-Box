from machine import Pin, SPI
import time

# Hardware SPI 2 (VSPI) - SCK=18, MOSI=23, MISO=19
# MANDATORY: Bridge 23 & 19 with a 1k resistor. DS1302 DAT to Pin 19.
spi = SPI(2, baudrate=100000, polarity=0, phase=0, firstbit=SPI.LSB)
cs = Pin(5, Pin.OUT, value=0)

def _io(reg, val=None):
    cs.on()
    if val is None:
        spi.write(bytearray([reg]))
        # 0xBF is Burst Read (7 bytes), otherwise read 1 byte
        data = spi.read(7 if reg == 0xBF else 1)
        cs.off()
        # BCD to Dec conversion
        return [((x >> 4) * 10) + (x & 15) for x in data] if reg == 0xBF else data[0]
    else:
        # Clock regs (<0x8E) need BCD; RAM/Control (>=0x8E) use raw bytes
        out = ((val // 10) << 4) | (val % 10) if reg < 0x8E else val
        spi.write(bytearray([reg, out]))
        cs.off()

def check():
    """Returns True if DS1302 is responding over the resistor bridge."""
    _io(0x8E, 0) # Unlock
    _io(0xC0, 0x55) # Write to RAM 0
    if _io(0xC1) == 0x55:
        # Clear Halt bit if set
        s = _io(0x81)
        if s & 0x80: _io(0x80, s & 0x7F)
        return True
    return False

def get_time():
    """Returns: [year, month, day, hour, minute, second]"""
    t = _io(0xBF) # [SS, MN, HH, DD, MO, WK, YY]
    return [2000+t[6], t[4], t[3], t[2], t[1], t[0]]

def set_time(y, m, d, h, n, s):
    _io(0x8E, 0) # Unlock
    for r, v in zip((0x8C, 0x88, 0x86, 0x84, 0x82, 0x80), (y%100, m, d, h, n, s)):
        _io(r, v)
