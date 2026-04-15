from machine import Pin
from ir_rx.nec import NEC_8
from ir_rx import IR_RX

class IRrcv:
    def __init__(self, pin_num=23, timer_id=0):
        IR_RX.Timer_id = timer_id
        self.pin = Pin(pin_num, Pin.IN)
        self.last_command = None
        # Initialize the protocol with a private callback
        self.device = NEC_8(self.pin, self._callback)

    def _callback(self, data, addr, ctrl):
        if data > 0:
            self.last_command = data

    def get_command(self):
        """Returns the latest command and clears it."""
        cmd = self.last_command
        self.last_command = None
        return cmd

#*** RUN TIME EXAMPLE ***
#import utime
#from remote import IRrcv
#
## Initialize your custom library
#ir = IRrcv(pin_num=23)
#
#print("Starting main loop...")
#
#while True:
#    # Check the external library for data
#    cmd = ir.get_command()
#
#    if cmd:
#        print(f"Main loop detected command: {hex(cmd)}")
#        # Add your logic here
#        if cmd == 0x45: print("Power Pressed")
#
#    # Run your other code here
#    # print("Working...")
#    utime.sleep_ms(50)
