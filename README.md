# Vibe-Box:
"Vibe-Box" is a physical "sandbox" environment for super talented vibe-coding individuals, to be used by extreme VIBE programming "Em-Dash" agents, with minimal to no human checks *necesary*. (Please do not use GrokPilot, just sucks)

# Hardware (original):
* Amaxon *clone* of a *cloen* of a "ESP32-D0WD-V3 (WROOM revision v3.1)", 
* A ESP32 WROOM breakout, 
* Recycled "CU20026SCPB-S20A" VFD display, 
* "DS1302" or "DS3132" RTCs, 
* A combination of "0603 (pre-wired)" and "5mm" UV 375nm~415nm (?) UVA LEDs, to enhance the view of radiactive stuff,  
* Need to add something to properly drive the Leds (WIP), currently the "PCF8591" is a choice to drive them, some board come with a "LDR", a "POT", and a "DIODE" to sample from light, position, and temperature, 
* WS2812B 24x ring (2.5" Dia) to illuminate the radioactive stuff, 
* HobbyLobby blessed [3.5" x 3.5" x 3.5"] acrylic cube, 
* Uranium "shot glass", literally minimun detectable ionizing radiation detectable,
* Autunite (hydrated calcium uranyl phosphate) mineral, with way less than 1uSv from where it seats, to where my hands and head is,
* Need to add PIN Diode circuitry to detect Alphas/Gammas from the Uranium Glass (right?) and the Autunite.... and of course, if an atomic event where to be present, to give me that "split second" alert so I can hide under my desk (right?)... got it from Amaxon... see media for reference, 
* Add Spearker or a cheap UART voice generation device from some BS online retail store, such as DY-SV5F (currently being used), 
* USB-C cable, which will be the source of power and VCOM.
* Remote control module kit ... the cheap stuff you can get for the Arduinos, cool stuf,
* The finest curated and carefully "vine" stained wood in town, 
* Random loose hardware to put everything together.

# Firmware:
* On the ESP32: "ESP32_GENERIC-D2WD-20251209-v1.27.0.bin",
* I would like to have "Espruino" in it, but have not done anything about compaling it for the "ESP32-D0WD-V3"... maybe vibe code it my way into it too.
* On the other end: Fedora, with "mpremote 1.27.0"

# Software:
* BASH, CLI interface using "echo" down to "ttyUSB",  and what not.
* Node-RED as graphical interface to other stuff, and it will have its own branch.

# Agent:
Google (free account).... so far... I encourage anything else too, specially if one can pipe AI text down to the device... it must be identified in the branch name if a different AI flavor is used.

# Goal:
* First and formost: Recycle and reuse, and where needed "purchase garbage", tech as much as possible.
* To save/waste as much time as possible vibe-coding "code" using current/primitive/cloned tech.... I hope I can comeback decades later to see how it went. I will do very minimal code review and hope it makes me happy. I will create a couple more physical environments for testing, as mentioned before: it must be identified in the branch name. Currently the goal is to "Vibe-Code" my way into building a device that detects ionizing radiation from a local source, and in the event a bigger form or ionizing radiation is detected, to alter the user thru visuals and sounds accordingly. I also figure the color/UV lights, the display, and sound interface could also be dynamically updated interface thru C/BASH/Python/JS (or watever program of choice with tty communication capability) for fun..... with things like.... AI....
* I one day will branch it and code it myself in pure and raw assembly. No promisses.
* Share it with other people as this is a pure distraction, because there are better things to do, but you and I are here, because we have the same goal.
