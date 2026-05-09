import bluetooth
import struct
import time
from micropython import const

# Advertising constants
_ADV_TYPE_FLAGS = const(0x01)
_ADV_TYPE_NAME = const(0x09)
_ADV_TYPE_UUID128_COMPLETE = const(0x07)
_UART_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_TX = (bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"), bluetooth.FLAG_NOTIFY,)
_UART_RX = (bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"), bluetooth.FLAG_WRITE | bluetooth.FLAG_WRITE_NO_RESPONSE,)
_UART_SERVICE = (_UART_UUID, (_UART_TX, _UART_RX),)

class BLEUART:
    def __init__(self, ble, name="VIBE", rxbuf=100):
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(self._irq)
        ((self._tx_handle, self._rx_handle),) = self._ble.gatts_register_services((_UART_SERVICE,))
        self._ble.gatts_set_buffer(self._rx_handle, rxbuf, True)
        self._connections = set()
        self._rx_buffer = bytearray()
        self._handler = None
        self._payload = self._advertising_payload(name=name, services=[_UART_UUID])
        self._advertise()

    def _irq(self, event, data):
        if event == 1: # _IRQ_CENTRAL_CONNECT
            self._connections.add(data[0])
        elif event == 2: # _IRQ_CENTRAL_DISCONNECT
            self._connections.discard(data[0])
            self._advertise()
        elif event == 3: # _IRQ_GATTS_WRITE
            conn_handle, value_handle = data
            if value_handle == self._rx_handle:
                self._rx_buffer.extend(self._ble.gatts_read(self._rx_handle))

    def any(self):
        return len(self._rx_buffer)

    def read(self):
        result = self._rx_buffer
        self._rx_buffer = bytearray()
        return result

    def write(self, data):
        for conn_handle in self._connections:
            self._ble.gatts_notify(conn_handle, self._tx_handle, data)

    def _advertise(self, interval_us=500000):
        self._ble.gap_advertise(interval_us, adv_data=self._payload)

    def _advertising_payload(self, name=None, services=None):
        payload = bytearray([0x02, _ADV_TYPE_FLAGS, 0x06])
        if name:
            payload += struct.pack("BB", len(name) + 1, _ADV_TYPE_NAME) + name.encode("utf-8")
        if services:
            for uuid in services:
                b = bytes(uuid)
                payload += struct.pack("BB", len(b) + 1, _ADV_TYPE_UUID128_COMPLETE) + b
        return payload
