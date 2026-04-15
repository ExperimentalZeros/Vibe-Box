import NeoPixels_ws2812B
import vfd_cu20026
import time
import random

time.sleep_ms(250)

message = "* The Distraction Box by the #1 Yunk-Jard * 0 * 1 * 2 * 3 * 4 * 5 * 6 * 7 * 8 * 9 * A * B * C * D * E * F "

index = 0

try:
    while index < len(message):

        r = random.randint(0, 5)
        g = random.randint(0, 5)
        b = random.randint(0, 5)

        NeoPixels_ws2812B.set_color(r, g, b)

        MSG_INDEX = message[index]
        vfd_cu20026.display_text(MSG_INDEX)
        print(MSG_INDEX + "\n")

        index = (index + 1) % len(message)
        time.sleep_ms(100)

except KeyboardInterrupt:
    print("\n Keyboard Interrupt")
