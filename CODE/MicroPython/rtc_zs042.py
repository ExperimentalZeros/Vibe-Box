from machine import Pin, I2C
import time

class DS3231:
    def __init__(self, i2c_bus, rtc_addr=0x68, eeprom_addr=0x57):
        self.i2c = i2c_bus
        self.rtc_addr = 0x68
        self.eeprom_addr = 0x57

    def _bcd_to_dec(self, bcd):
        return (bcd >> 4) * 10 + (bcd & 0x0F)

    def _dec_to_bcd(self, dec):
        return (dec // 10 << 4) + (dec % 10)

    def set_time(self, year, month, day, hour, minute, second):
        """Sets the DS3231 time using the same register order as get_time"""
        data = bytearray(7)
        data[0] = self._dec_to_bcd(second)
        data[1] = self._dec_to_bcd(minute)
        data[2] = self._dec_to_bcd(hour)
        data[3] = 0x01  # Day of week (1-7), required for correct register offsetting
        data[4] = self._dec_to_bcd(day)
        data[5] = self._dec_to_bcd(month)
        data[6] = self._dec_to_bcd(year % 100) # RTC stores last two digits

        self.i2c.writeto_mem(self.rtc_addr, 0x00, data)

    def get_time(self):
        """Reads time from DS3231 and returns (Y, M, D, H, M, S)"""
        data = self.i2c.readfrom_mem(self.rtc_addr, 0x00, 7)
        s = self._bcd_to_dec(data[0])
        m = self._bcd_to_dec(data[1])
        h = self._bcd_to_dec(data[2] & 0x3F) # 24-hour mode
        d = self._bcd_to_dec(data[4])
        mo = self._bcd_to_dec(data[5] & 0x1F)
        #y = self._bcd_to_dec(data[6]) + 2000
        y = self._bcd_to_dec(data[6])
        return (y, mo, d, h, m, s)

    def get_temp(self):
        """Reads the DS3231 internal temperature sensor"""
        t_data = self.i2c.readfrom_mem(self.rtc_addr, 0x11, 2)
        # Integer part in first byte, fractional (.25 increments) in second
        temp = t_data[0] + (t_data[1] >> 6) * 0.25
        return temp

    def eeprom_write(self, addr, data_byte):
        """Writes a single byte to a 16-bit address (0x0000 to 0x0FFF)"""
        self.i2c.writeto_mem(self.eeprom_addr, addr, bytes([data_byte]), addrsize=16)
        time.sleep_ms(5)

    def eeprom_read(self, addr):
        """Reads a single byte from a 16-bit address"""
        return self.i2c.readfrom_mem(self.eeprom_addr, addr, 1, addrsize=16)[0]

##*** RUNTIME EXAMPLE ***
# from machine import I2C, Pin
# i2c = I2C(0, scl=Pin(22), sda=Pin(21))
# rtc = DS3231(i2c)
# print(rtc.get_time())

## Test parsing a string like "2024,4,25,14,30,00"
#def set_time_from_ble(rtc_inst, ble_str):
#    parts = [int(p.strip()) for p in ble_str.split(',')]
#    return rtc_inst.set_time(parts[0], parts[1], parts[2], parts[3], parts[4], parts[5])
#
#print(set_time_from_ble(DS3231(None), "2024,04,25,14,30,00"))
