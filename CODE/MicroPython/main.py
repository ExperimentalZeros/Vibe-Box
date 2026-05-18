import sys
import bluetooth
from ble_uart import BLEUART
from machine import UART, Pin, I2C
import time
import random

## GLOBAL VARIABLES
btID = ""
ble = ""
MSG = "MAN-TALK"

## 0) BLUETOOTH - BLE Configuration init.
try:
    bt = bluetooth.BLE()
    bt.active(True)

    time.sleep_ms(1000)

    mac_address = bt.config('mac')[1]
    btID = "{:02X}{:02X}".format(mac_address[-2], mac_address[-1])
    time.sleep_ms(1000)
    ble = BLEUART(bt, name=f"V-{btID}")
    bt.config(gap_name=f"V-{btID}")

except:
    pass

## 1.1) Load Hardware "Drivers"
import irr_38khz
import exp_pcf8591
import led_ws2812b
import rtc_zs042
import snd_dysv5f
import vfd_cu20026

## 1.2) Hardware Initialization
i2c = I2C(0, scl=Pin(22), sda=Pin(21)) # Standard ESP32 I2C pins
irr = irr_38khz.IRR(pin_num=23)
exp = exp_pcf8591.PCF8591(i2c)
rtc = rtc_zs042.DS3231(i2c)
vfd = vfd_cu20026.VFD()
neo = led_ws2812b.NeoPixel(pin=15, n=24)

## 1.3) Light Check RED: Drivers uploaded fine!
neo.set_color(10, 0, 0)

## 2.1) Sound Setup
uart2 = UART(2, baudrate=9600, tx=17, rx=16)
busy_pin = Pin(35, Pin.IN)
snd = snd_dysv5f.DYSVxF(uart2, busy_pin)

snd.set_volume(20)
snd.set_eq(0x02)
snd.set_play_mode(0x02)
snd.play_track(95)

## 2.2) Light Check BLUE: Sound settings uploaded fine!
neo.set_color(0, 0, 10)

## 3.1) Display Device Info
vfd.cursor_off()
vfd.cursor_reset()

time.sleep_ms(10)

vfd.data_write(f"* * Vibe-Box v.0 * *")
vfd.data_write(f"     S/N: V-{btID}    ")

## 3.2) Light Check GREEN: Display data uploaded fine!
neo.set_color(0, 10, 0)
time.sleep_ms(5000)

## 4) INIT COUNTER
irr_cmd_val = "00"
cnt = 0
cnt_trigger = 10

## 5) Start the While Loop!

try:
    while True:

        vfd.cursor_reset()

        ## --- PHASE 2: DATA COLLECTION ---
        deg = 0xdf
        rtc_time_val = rtc.get_time()
        rtc_temp_val_c = f"{rtc.get_temp():04.1f}"
        rtc_temp_val_f = f"{ ((rtc.get_temp() * 9/5) + 32):04.1f}"
        exp_pot_val = f"{exp.get_pot():03d}"
        exp_ldr_val = f"{exp.get_ldr():03d}"
        exp_diode_val = f"{exp.get_diode():03d}"

        ## --- PHASE 1: BLE COMMAND HANDLING ---
        if ble.any():
            cnt = 0
            # Expecting format: "YYYY,MM,DD,HH,MM,SS"
            payload = ble.read().decode().strip()
            try:
                # Split into ['command', 'data'] (maxsplit=1 keeps the rest of the string intact)
                parts = payload.split(',', 1)
                command = parts[0]
                data = parts[1] if len(parts) > 1 else ""

                # 0.0) Process custom REPL
                if command in ("REPL", "BOOT"):
                    vfd.data_write("* *     REPL     * *")
                    vfd.data_write("* *     BOOT     * *")
                    ble.write(f"* REPL || BOOT *\n\r".encode())

                    neo.set_color(1, 0, 1)

                    Pin(0, Pin.IN, pull=Up)
                    Pin(2, Pin.IN, pull=Down)
                    Pin(5, Pin.IN, pull=Up)
                    Pin(12, Pin.IN, pull=Down)
                    Pin(15, Pin.IN, pull=Up)

                    #sys.exit()
                    break

                # 1) Process custom DATE
                elif command == "date":
                    d = [int(x) for x in data.split(',')]
                    if len(d) == 6:
                        rtc.set_time(d[0], d[1], d[2], d[3], d[4], d[5])
                        vfd.data_write("* * RTC  UPDATED * *")
                        ble.write(f"DATE Updated\n\r".encode())
                        neo.set_color(255, 0, 0) # Red for DATE
                        time.sleep_ms(500)
                        cnt = 0

                # 2) Process custom MESSAGE
                elif command == "msg":
                    m = [x for x in data.split(',')]
                    if len(m) == 1:
                        ble.write("* MSG Received *\n\r".encode())
                        snd.play_track(102)
                        MSG = m[0]
                        neo.set_color(255, 0, 255) # PURPLE for EXP
                        time.sleep_ms(500)
                        cnt = 9

                # 3) Process custom SOUND
                elif command == "snd":
                    s = [int(x) for x in data.split(',')]
                    if len(s) == 2:
                        ble.write("* SND Received *\n\r".encode())
                        snd.set_volume( int(s[0]) )
                        snd.play_track( int(s[1]) )
                        neo.set_color(0, 0, 255) # Blue for SND
                        cnt = 0

                # 4) Process custom EXPANDER
                elif command == "exp":
                    e = [int(x) for x in data.split(',')]
                    if len(e) == 1:
                        ble.write("* EXP Received *\n\r".encode())
                        exp.set_dac( int(e[0]) )
                        ble.write(f"L:{exp_ldr_val} P:{exp_pot_val} D:{exp_diode_val}\n\r".encode())
                        neo.set_color(255, 255, 255) # White for EXP

                # ?) Process custom message
                #elif command == "?":
                    #do something
                    #neo.set_color(0, 0, 255) # Blue for ???

                else:
                    #print(f"Unknown command: {command}")
                    #ble.write(f"Unknown command: {command}".encode())
                    pass

            except Exception as e:
                #print("BLE Sync Error:", e)
                #ble.write(f"BLE Sync Error".encode()
                pass

        ## --- PHASE 2: IR COMMAND HANDLING ---
        irr_cmd = irr.get_command()
        if irr_cmd:
            cnt = 0
            irr_cmd_val = f"{int(float(irr_cmd)):02X}" if (irr_cmd and str(irr_cmd) != "None") else "00"
            snd.play_track(irr_cmd)
            ble.write(f"* IRR Received {irr_cmd_val} *\n\r".encode())
            neo.set_color(255, 0, 0)
            time.sleep_ms(50)

        ## --- PHASE 3: DISPLAY (VFD CU20026) ---
        datestamp = "{:02d}/{:02d}/{:02d}".format(rtc_time_val[0], rtc_time_val[1], rtc_time_val[2])
        timestamp = "{:02d}:{:02d}:{:02d}".format(rtc_time_val[3], rtc_time_val[4], rtc_time_val[5])

        ble.write(f"20{datestamp} - {timestamp}\n\r".encode())

        if cnt == 0:
            display = f"{datestamp} {irr_cmd_val}"

        elif cnt == 7:
            display = "VIBE-BOX **"

        elif cnt == 9:
            display = f"{MSG} **"

        elif cnt == 11:
            display = "FCK THIS **"

        elif cnt == 13:
            display = "TEA TIME **"

        elif cnt == 15:
            display = "**** 5 ****"

        elif cnt == 16:
            display = " *** 4 *** "

        elif cnt == 17:
            display = "  ** 3 **  "

        elif cnt == 18:
            display = "   * 2 *   "

        elif cnt == 19:
            display = "    *1*    "

        elif cnt == 20:
            display = "     *     "

        vfd.data_write(f"{display} {timestamp}")
        time.sleep_ms(10)

        if (cnt // cnt_trigger) % 2 == 0:
            vfd.data_write(f"T:{rtc_temp_val_f}{chr(deg)}F P:{exp_pot_val} L:{exp_ldr_val}")
        else:
            vfd.data_write(f"T:{rtc_temp_val_c}{chr(deg)}C P:{exp_pot_val} D:{exp_diode_val}")

        cnt += 1

        if cnt >= (cnt_trigger * 2):
            cnt = 0

        time.sleep_ms(10)

        r, g, b = [random.randint(0, 10) for _ in range(3)]
        neo.set_color(r, g, b)

        time.sleep_ms(980)

except KeyboardInterrupt:
    neo.set_color(0, 0, 0)
    print("\nDemo terminated by user.")
