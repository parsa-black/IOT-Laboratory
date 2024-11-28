import bluetooth
import random
import struct
import time
from micropython import const

# Constants for BLE advertising
_ADV_TYPE_FLAGS = const(0x01)
_ADV_TYPE_NAME = const(0x09)
_ADV_TYPE_UUID16_COMPLETE = const(0x03)
_ADV_MAX_PAYLOAD = const(31)

CF = 0  # Connection Flag

_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_INDICATE_DONE = const(20)

_FLAG_READ = const(0x0002)
_FLAG_NOTIFY = const(0x0010)
_FLAG_INDICATE = const(0x0020)

# org.bluetooth.service.environmental_sensing
_ENV_SENSE_UUID = bluetooth.UUID(0x181A)

# org.bluetooth.characteristic.temperature
_TEMP_CHAR = (
    bluetooth.UUID(0x2A6E),
    _FLAG_READ | _FLAG_NOTIFY | _FLAG_INDICATE,
)
_ENV_SENSE_SERVICE = (_ENV_SENSE_UUID, (_TEMP_CHAR,))

# BLE Advertising payload helper functions
def advertising_payload(name=None, services=None):
    payload = bytearray()

    def _append(adv_type, value):
        nonlocal payload
        payload += struct.pack("BB", len(value) + 1, adv_type) + value

    _append(_ADV_TYPE_FLAGS, struct.pack("B", 0x06))  # General discoverable mode
    if name:
        _append(_ADV_TYPE_NAME, name.encode('utf-8'))
    if services:
        for uuid in services:
            b = bytes(uuid)
            if len(b) == 2:
                _append(_ADV_TYPE_UUID16_COMPLETE, b)

    if len(payload) > _ADV_MAX_PAYLOAD:
        raise ValueError("Advertising payload too large")

    return payload

class BLETemperature:
    def __init__(self, ble, name="ESP32"):
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(self._irq)
        ((self._handle,),) = self._ble.gatts_register_services((_ENV_SENSE_SERVICE,))
        self._connections = set()
        self._payload = advertising_payload(name=name, services=[_ENV_SENSE_UUID])
        self._advertise()

    def _irq(self, event, data):
        global CF
        if event == _IRQ_CENTRAL_CONNECT:
            CF = 1
            conn_handle, _, _ = data
            self._connections.add(conn_handle)
            print("*** Connected to a client ***")
        elif event == _IRQ_CENTRAL_DISCONNECT:
            CF = 0
            conn_handle, _, _ = data
            self._connections.remove(conn_handle)
            print("Disconnected. Waiting for a client...")
            self._advertise()
        elif event == _IRQ_GATTS_INDICATE_DONE:
            conn_handle, value_handle, status = data

    def set_temperature(self, temp_deg_c, notify=False, indicate=False):
        # Write the temperature value to the BLE characteristic
        self._ble.gatts_write(self._handle, struct.pack("<h", int(temp_deg_c * 100)))
        if CF == 1:  # Print temperature only when connected
            print(f"Sending temperature: {temp_deg_c:.2f}°C")
        if notify or indicate:
            for conn_handle in self._connections:
                if notify:
                    self._ble.gatts_notify(conn_handle, self._handle)
                if indicate:
                    self._ble.gatts_indicate(conn_handle, self._handle)

    def _advertise(self, interval_us=500000):
        self._ble.gap_advertise(interval_us, adv_data=self._payload)


def demo():
    ble = bluetooth.BLE()
    temp = BLETemperature(ble)

    t = 25  # Initial temperature
    i = 0

    while True:
        if CF == 0:
            print("Waiting for a client...")
        else:
            # Simulate temperature changes
            i = (i + 1) % 10
            temp.set_temperature(t, notify=i == 0, indicate=False)
            t += random.uniform(-0.5, 0.5)
        time.sleep_ms(1000)


if __name__ == "__main__":
    demo()

