import machine, neopixel

ledNumber = 24
pin = 15

np = neopixel.NeoPixel(machine.Pin(pin), ledNumber)

def set_color(r, g, b):
  for i in range(ledNumber):
    np[i] = (r, g, b)
  np.write()

#*** RUNTIME EXAMPLE ***
#set_color(0, 10, 10)
