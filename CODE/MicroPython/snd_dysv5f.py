from machine import UART, Pin
import time

class DYSVxF:
    def __init__(self, uart_bus, busy_pin=None):
        self.uart = uart_bus
        self.busy = busy_pin

    def _send(self, cmd, data=None):
        """Internal helper to construct and send the 0xAA hex packet."""
        packet = bytearray([0xAA, cmd])
        if data:
            packet.append(len(data))
            packet.extend(data)
        else:
            packet.append(0x00)
        # Add checksum (8-bit sum of all bytes)
        packet.append(sum(packet) & 0xFF)
        self.uart.write(packet)

    # --- Playback Control Functions ---
    def play(self): self._send(0x02)
    def pause(self): self._send(0x03)
    def stop(self): self._send(0x04)
    def next(self): self._send(0x06)
    def prev(self): self._send(0x05)

    def play_track(self, track_number):
        """Plays track by index (1-65535)."""
        hb = (track_number >> 8) & 0xFF
        lb = track_number & 0xFF
        self._send(0x07, [hb, lb])

    # --- Audio & EQ Functions ---
    def set_volume(self, level):
        """Level 0 to 30."""
        self._send(0x13, [max(0, min(level, 30))])

    def set_eq(self, mode):
        """0:Normal, 1:Pop, 2:Rock, 3:Jazz, 4:Classic, 5:Base."""
        self._send(0x1A, [mode])

    # --- Play Mode Functions ---
    def set_play_mode(self, mode):
        """0:Full, 1:Single Loop, 2:Single Stop, 3:Random, etc."""
        self._send(0x18, [mode])

    # --- Query & Busy Functions ---
    def is_playing(self):
        """True if audio is active (requires Busy pin connected)."""
        return self.busy.value() == 0 if self.busy else False

    def query_status(self):
        """Requests current state from module. Use uart.read() to catch result."""
        self._send(0x01)
        time.sleep_ms(50)
        return self.uart.read()

#*** RUNTIME EXAMPLE ***
# --- Example Initialization ---
# DYSVxF_uart = UART(2, baudrate=9600, tx=17, rx=16)
# DYSVxF_busy = Pin(15, Pin.IN, Pin.PULL_UP)
# SOUND = DYSVxF(my_uart, my_busy)

# SOUND.set_volume(25)
# SOUND.play_track(1)
