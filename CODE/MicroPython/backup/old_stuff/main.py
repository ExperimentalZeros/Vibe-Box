import NeoPixels
import vfd
import rtc
import time

time.sleep_ms(250)

NeoPixels.set_color(0, 10, 00)

time.sleep_ms(250)

#vfd.display_text("    The Man Talk    Time: ??:?? CNT: ???")
#vfd.display_text("123")

if rtc.check():
    vfd.display_text("RTC Linked")
    #rtc.set_time(2026, 3, 22, 21, 0, 0) # Set once

    while True:
        y, m, d, hr, mn, sc = rtc.get_time()
        #print(f"{y}-{m:02d}-{d:02d} {hr:02d}:{mn:02d}:{sc:02d}")
        vfd.display_text(f"{y}-{m:02d}-{d:02d} {hr:02d}:{mn:02d}:{sc:02d} ")
        time.sleep(1)
else:
    vfd.display_text("RTC Error: Check 1k resistor bridge between GPIO 23 and 19 ")
