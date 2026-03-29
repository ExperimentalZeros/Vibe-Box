#!/bin/bash

#cat ../../REFERENCES/commands.ref
#Chip is ESP32-D0WD-V3 (revision v3.1)

#esptool.py erase_flash
#esptool.py --baud 460800 write_flash 0x1000 ../../FIRMWARE/MicroPython/ESP32_GENERIC-D2WD-20251209-v1.27.0.bin

mpremote cp main.py vfd.py NeoPixels.py rtc.py : ; sleep 1; mpremote soft-reset; mpremote repl
