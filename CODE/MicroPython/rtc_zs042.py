from machine import Pin, I2C
import time

# 1. Initialize Hardware I2C (Standard ESP32 Pins)
# SDA = 21, SCL = 22. Standard ZS-042 pull-ups are usually sufficient.
i2c = I2C(0, sda=Pin(21), scl=Pin(22), freq=100000)

# 2. Device Addresses
RTC_ADDR = 0x68
EEPROM_ADDR = 0x57  # Default for AT24C32; if changed by jumpers, it may be 0x50-0x56

# --- Helper Functions ---
def bcd_to_dec(bcd):
    return (bcd >> 4) * 10 + (bcd & 0x0F)

def dec_to_bcd(dec):
    return (dec // 10 << 4) + (dec % 10)

# --- RTC & Temperature (DS3231) ---
def get_time():
    """Reads time from DS3231 and returns (Y, M, D, H, M, S)"""
    data = i2c.readfrom_mem(RTC_ADDR, 0x00, 7)
    s = bcd_to_dec(data[0])
    m = bcd_to_dec(data[1])
    h = bcd_to_dec(data[2] & 0x3F) # 24-hour mode
    d = bcd_to_dec(data[4])
    mo = bcd_to_dec(data[5] & 0x1F)
    y = bcd_to_dec(data[6]) + 2000
    return (y, mo, d, h, m, s)

def get_temp():
    """Reads the DS3231 internal temperature sensor"""
    t_data = i2c.readfrom_mem(RTC_ADDR, 0x11, 2)
    # Integer part in first byte, fractional (.25 increments) in second
    temp = t_data[0] + (t_data[1] >> 6) * 0.25
    return temp

# --- EEPROM (AT24C32) ---
def eeprom_write(addr, data_byte):
    """Writes a single byte to a 16-bit address (0x0000 to 0x0FFF)"""
    # AT24C32 requires 16-bit addressing (addrsize=16)
    i2c.writeto_mem(EEPROM_ADDR, addr, bytes([data_byte]), addrsize=16)
    time.sleep_ms(5) # Essential: EEPROM needs time to physically write

def eeprom_read(addr):
    """Reads a single byte from a 16-bit address"""
    return i2c.readfrom_mem(EEPROM_ADDR, addr, 1, addrsize=16)[0]

#*** RUNTIME EXAMPLE ***
## --- Main Logic ---
#
## Example: Write a 'Secret Key' (e.g., 123) to EEPROM address 50
#print("Writing to EEPROM...")
#eeprom_write(0x0032, 123)
#
#while True:
#    t = get_time()
#    temp = get_temp()
#    saved_val = eeprom_read(0x0032)
#
#    # Print formatted output
#    print("-" * 40)
#    print("RTC TIME: {:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(*t))
#    print("TEMP:     {:.2f}°C".format(temp))
#    print("EEPROM:   Value at addr 0x32 is {}".format(saved_val))
#
#    time.sleep(2)
