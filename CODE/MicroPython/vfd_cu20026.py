from machine import Pin
import time

# Initialize Control Pins
#rd = Pin(?, Pin.OUT, value=1) #VFD pin 21 set HIGH 3v3
#cs = Pin(?, Pin.OUT, value=0) #VFD pin 23 set LOW  GND
#ts = Pin(?, Pin.OUT, value=Z) #VFD pin 25 set OPEN N/A
#rs = Pin(?, Pin.OUT, value=0) #VFD pin 20 set LOW  GND

ts = Pin(19, Pin.OUT, value=1) #VFD pin 25 set OPEN N/A
cs = Pin(18, Pin.OUT, value=0) #VFD pin 23 set LOW  GND
rs = Pin(5, Pin.OUT, value=0)  #VFD pin 20 set LOW  GND
a0 = Pin(0, Pin.OUT, value=0)  #VFD pin 19
wr = Pin(2, Pin.OUT, value=1)  #VFD pin 17


# Initialize 8-bit Data Bus
# Order: D0, D1, D2, D3, D4, D5, D6, D7

data_pins = [Pin(p, Pin.OUT) for p in [32, 33, 25, 26, 27, 14, 12, 13]]

def write_8bit(value):
    for i in range(8):
        data_pins[i].value((value >> i) & 0x01)

def send_byte(byte, is_data=True):
    a0.value(0 if is_data else 1)
    write_8bit(byte)
    # Strobe WR (Falling edge latches data)
    wr.value(0)
    time.sleep_us(1)
    wr.value(1)

def init_vfd():
    rs.value(1)
    time.sleep_ms(10)
    rs.value(0)
    time.sleep_ms(100)

def display_text(text):
    for char in text:
        send_byte(ord(char), is_data=True)

#*** RUNTIME EXAMPLE ***
# Example Initialization Command: Clear Display (0x0E or 0x0C depending on mode)
#send_byte(0x0E, is_data=False)
#display_text("    The Man Talk    Time: ??:?? CNT: ???")
