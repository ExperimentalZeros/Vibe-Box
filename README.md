# Vibe-Box:
"Vibe-Box" is a physical "sandbox" environment for super talented vibe-coding individuals, to be used by extreme VIBE programming agents (Em-Dash) No checks *necesary*. (Please do not use CoPilot)

# Hardware (original):
* Amaxon *clone* of a *cloen* of a "ESP32-D0WD-V3 (WROOM revision v3.1)", 
* ESP32 WROOM breakout, 
* Recycled "CU20026SCPB-S20A" VFD display, 
* "DS1302" RTC, 
* A combination of "0603 (pre-wired)" and "5mm" UV 375nm~415nm (?) UVA LEDs, 
* Need to add something to properly drive the Leds (WIP), 
* WS2812B 24x ring (2.5" Dia), 
* HobbyLobby blessed [3.5" x 3.5" x 3.5"] acrylic cube, 
* Uranium "shot glass", literally minimun detectable ionizing radiation detectable,
* Autunite (hydrated calcium uranyl phosphate) mineral, with way less than 1uSv from where it seats, to where my hands and head is,
* Need to add PIN Diode circuitry to detect Alphas/Gammas from the Uranium Glass (right?) and the Autunite.... and of course, if an atomic event where to be present, to give me that "split second" alert so I can hide under my desk (right?)
* Add Spearker or a cheap UART voice generation device from some BS online retail store (WIP), 
* USB-C cable, which will be the source of power and VCOM.
* Random loose hardware to put everything together.

# Firmware:
* On the ESP32: "ESP32_GENERIC-D2WD-20251209-v1.27.0.bin",
* I would like to have "Espruino" in it, but have not done anything about compaling it for the "ESP32-D0WD-V3"... maybe vibe code it my way into it too.
* On the other end: Fedora, with "mpremote 1.27.0"

# Software:
* BASH, CLI interface using "echo" down to "ttyUSB",  and what not.
* Node-RED as graphical interface to other stuff, and it will have its own branch.

# Agent:
Google (free account).... so far... I encourage anything else too, specially if one can pipe AI text down to the device... it must be identified in the branch name.

# Goal:
To save/waste as much time as possible vibe-coding "code" using current tech.... I hope I can comeback decades later to see how it went. I will do very minimal code review and hope it makes me happy. I will create a couple more physical environments for testing, as mentioned before: it must be identified in the branch name. Currently the goal is to "Vibe-Code" my way into building a device that detects ionizing radiation from a local source, and in the event a bigger form or ionizing radiation is detected, to alter the user thru visuals and sounds accordingly. I also figure the color/UV lights, the display, and sound interface could also be dynamically updated interface thru C/BASH/Python/JS (or watever program of choice with tty communication capability) for fun..... with things like.... AI....
