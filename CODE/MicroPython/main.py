import sys
import bluetooth
from ble_uart import BLEUART
from machine import UART, Pin, I2C
import time
import random

time.sleep_ms(1000)

## Modules (Ensure filenames on ESP32 match these exactly)
bt = bluetooth.BLE()
#bt.active(True)  # Add this line
#ble_id = "{:02X}".format(bt.config('mac')[1][-1])
ble = BLEUART(bt, name=f"VIBE")

#ble_SN = "{:02X}{:02X}".format(bt.config('mac')[1][-2], bt.config('mac')[1][-1])
#ble = BLEUART(bt, name=f"V-{ble_id}")

import irr_38khz
import exp_pcf8591
import led_ws2812b
import rtc_zs042
import snd_dysv5f
import vfd_cu20026

## 1. Hardware Initialization
i2c = I2C(0, scl=Pin(22), sda=Pin(21)) # Standard ESP32 I2C pins
irr = irr_38khz.IRR(pin_num=23)
exp = exp_pcf8591.PCF8591(i2c)
rtc = rtc_zs042.DS3231(i2c)
vfd = vfd_cu20026.VFD()
neo = led_ws2812b.NeoPixel(pin=15, n=24)

neo.set_color(10, 0, 0)

irr_cmd_val = "00"
cnt = 0
cnt_trigger = 10

## Sound Setup
uart2 = UART(2, baudrate=9600, tx=17, rx=16)
busy_pin = Pin(35, Pin.IN)
snd = snd_dysv5f.DYSVxF(uart2, busy_pin)
snd.set_volume(20)

time.sleep_ms(1500)

vfd.cursor_off()
vfd.cursor_reset()
neo.set_color(0, 0, 10)

time.sleep_ms(10)

vfd.data_write(f"* * Vibe-Box v.0 * *")
time.sleep_ms(10)
vfd.data_write(f"      S/N: xXx      ")

time.sleep_ms(3000)

ble.write(f"* * Vibe-Box xXx * *")
neo.set_color(0, 10, 0)

time.sleep_ms(1500)

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

                #for i in [12, 15]:
                #    try: Pin(i, Pin.IN, pull=None)
                #    except: pass

                    Pin(0, Pin.IN, pull=Up)
                    Pin(2, Pin.IN, pull=Down)
                    Pin(5, Pin.IN, pull=Up)
                    Pin(12, Pin.IN, pull=Down)
                    Pin(15, Pin.IN, pull=Up)

                    #sys.exit()
                    break

                # 1) Process custom DATE
                if command == "date":
                    t = [int(x) for x in data.split(',')]
                    if len(t) == 6:
                        rtc.set_time(t[0], t[1], t[2], t[3], t[4], t[5])
                        vfd.data_write("* * RTC  UPDATED * *")
                        ble.write(f"DATE Updated\n\r".encode())
                        neo.set_color(255, 0, 0) # Red for DATE
                        time.sleep_ms(500)

                # 2) Process custom MESSAGE
                elif command == "msg":
                    vfd.display_text(data)
                    ble.write(f"* MSG Received *\n\r".encode())
                    neo.set_color(0, 255, 0) # Greem for MSG

                # 3) Process custom SOUND
                elif command == "snd":
                    s = [int(s) for s in data.split(',')]
                    if len(s) == 2:
                        ble.write("* SND Received *\n\r".encode())
                        snd.set_volume( int(s[0]) )
                        snd.play_track( int(s[1]) )
                        neo.set_color(0, 0, 255) # Blue for SND

                # 4) Process custom EXPANDER
                elif command == "exp":
                    x = [int(x) for x in data.split(',')]
                    if len(x) == 1:
                        ble.write("* EXP Received *\n\r".encode())
                        exp.set_dac( int(x[0]) )
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
            display = "MAN-TALK **"

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
