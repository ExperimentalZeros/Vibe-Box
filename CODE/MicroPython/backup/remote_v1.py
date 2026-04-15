from machine import Pin
from ir_rx.nec import NEC_8 # Use NEC_16 if NEC_8 doesn't work
from ir_rx import IR_RX

# Force Hardware Timer 0
IR_RX.Timer_id = 0

def ir_callback(data, addr, ctrl):
    if data > 0: # Ignore repeat codes (< 0)
        print(f"Host: {addr:02x} Data: {data:02x}")

# Initialize on Pin 23
ir = NEC_8(Pin(23, Pin.IN, Pin.PULL_UP), ir_callback)

print("Waiting for NEC signals on Pin 23...")
