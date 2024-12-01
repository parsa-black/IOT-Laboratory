import bluetooth
import struct
import time
from micropython import const

# Constants for BLE
_IRQ_SCAN_RESULT = const(5)
_IRQ_SCAN_DONE = const(6)
_IRQ_PERIPHERAL_CONNECT = const(7)
_IRQ_PERIPHERAL_DISCONNECT = const(8)
_IRQ_GATTC_SERVICE_RESULT = const(9)
_IRQ_GATTC_SERVICE_DONE = const(10)
_IRQ_GATTC_CHARACTERISTIC_RESULT = const(11)
_IRQ_GATTC_CHARACTERISTIC_DONE = const(12)
_IRQ_GATTC_NOTIFY = const(18)

_ADV_IND = const(0x00)

_ENV_SENSE_UUID = bluetooth.UUID(0x181A)  # Environmental sensing service
_TEMP_UUID = bluetooth.UUID(0x2A6E)      # Temperature characteristic

class BLETemperatureCentral:
    def __init__(self, ble):
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(self._irq)
        self._reset()

    def _reset(self):
        self._addr_type = None
        self._addr = None
        self._name = None
        self._value = None
        self._conn_handle = None
        self._start_handle = None
        self._end_handle = None
        self._value_handle = None
        self._scan_callback = None
        self._conn_callback = None
        self._read_callback = None
        self._notify_callback = None

    def _irq(self, event, data):
        if event == _IRQ_SCAN_RESULT:
            addr_type, addr, adv_type, rssi, adv_data = data
            if adv_type == _ADV_IND and _ENV_SENSE_UUID in self._decode_services(adv_data):
                self._addr_type = addr_type
                self._addr = bytes(addr)  # Make a copy
                self._name = self._decode_name(adv_data) or "Unknown"
                self._ble.gap_scan(None)  # Stop scanning

        elif event == _IRQ_SCAN_DONE:
            if self._scan_callback:
                if self._addr:
                    self._scan_callback(self._addr_type, self._addr, self._name)
                else:
                    self._scan_callback(None, None, None)

        elif event == _IRQ_PERIPHERAL_CONNECT:
            conn_handle, addr_type, addr = data
            if addr_type == self._addr_type and addr == self._addr:
                self._conn_handle = conn_handle
                self._ble.gattc_discover_services(conn_handle)

        elif event == _IRQ_PERIPHERAL_DISCONNECT:
            conn_handle, _, _ = data
            if conn_handle == self._conn_handle:
                self._reset()

        elif event == _IRQ_GATTC_SERVICE_RESULT:
            conn_handle, start_handle, end_handle, uuid = data
            if conn_handle == self._conn_handle and uuid == _ENV_SENSE_UUID:
                self._start_handle, self._end_handle = start_handle, end_handle

        elif event == _IRQ_GATTC_SERVICE_DONE:
            if self._start_handle and self._end_handle:
                self._ble.gattc_discover_characteristics(
                    self._conn_handle, self._start_handle, self._end_handle
                )

        elif event == _IRQ_GATTC_CHARACTERISTIC_RESULT:
            conn_handle, def_handle, value_handle, properties, uuid = data
            if conn_handle == self._conn_handle and uuid == _TEMP_UUID:
                self._value_handle = value_handle

        elif event == _IRQ_GATTC_NOTIFY:
            conn_handle, value_handle, notify_data = data
            if conn_handle == self._conn_handle and value_handle == self._value_handle:
                self._value = self._parse_temperature(notify_data)
                if self._notify_callback:
                    self._notify_callback(self._value)

    def scan(self, callback):
        self._reset()
        self._scan_callback = callback
        self._ble.gap_scan(2000, 30000, 30000)

    def connect(self, addr_type=None, addr=None, callback=None):
        self._conn_callback = callback
        if not addr_type or not addr:
            addr_type, addr = self._addr_type, self._addr
        self._ble.gap_connect(addr_type, addr)

    def disconnect(self):
        if self._conn_handle:
            self._ble.gap_disconnect(self._conn_handle)
        self._reset()

    def on_notify(self, callback):
        self._notify_callback = callback
    
    def _decode_name(self, payload):
        i = 0
        while i + 1 < len(payload):
            length = payload[i]
            adv_type = payload[i + 1]
            if adv_type == 0x09:  # Complete Local Name
                return str(payload[i + 2 : i + 1 + length], "utf-8")
            i += 1 + length
        return ""

    def _decode_services(self, payload):
        services = []
        i = 0
        while i + 1 < len(payload):
            length = payload[i]
            adv_type = payload[i + 1]
            if adv_type == 0x03:  # Complete List of 16-bit UUIDs
                for j in range(2, length, 2):
                    services.append(bluetooth.UUID(struct.unpack("<H", payload[i + j : i + j + 2])[0]))
            i += 1 + length
        return services
    
    def _parse_temperature(self, data):
        return struct.unpack("<h", data)[0] / 100

def demo():
    ble = bluetooth.BLE()
    central = BLETemperatureCentral(ble)

    def on_scan(addr_type, addr, name):
        if addr_type is not None:
            print(f"Found device: {name} [{addr}]")
            central.connect()
        else:
            print("No devices found")

    def on_notify(value):
        print(f"Temperature: {value}°C")

    central.scan(callback=on_scan)
    central.on_notify(callback=on_notify)

    while True:
        time.sleep(1)

if __name__ == "__main__":
    demo()

