from bluepy.btle import Scanner, DefaultDelegate, Peripheral

# UUIDs for the service and characteristics
SERVICE_UUID = "7d2746a0-c3cc-46cd-9e13-e3df31050ce7"
CHARACTERISTIC_UUID = "01f602d7-096d-4d34-a572-e82ab2ba9290"

# Delegate to handle notifications from the ESP32
class NotificationDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        # Unpack the received data (assuming it is a string percentage)
        try:
            moisture_value = data.decode('utf-8')
            print(f"Soil Moisture: {moisture_value}%")
        except Exception as e:
            print(f"Error decoding data: {e}")

def scan_and_find_uuid():
    scanner = Scanner()
    print("Scanning for BLE devices...")
    devices = scanner.scan(10.0)  # Scan for 10 seconds

    for dev in devices:
        # Search the advertisement data for the service UUID
        for (adtype, desc, value) in dev.getScanData():
            if desc == "Complete 128b Services" and value == SERVICE_UUID:
                print(f"Found device with matching service UUID: {dev.addr}")
                return dev.addr  # Return the BLE address of the device

    print("Device with matching UUID not found.")
    return None

def connect_to_device(device_address):
    peripheral = None
    try:
        print(f"Connecting to {device_address}...")
        peripheral = Peripheral(device_address)

        # Set the delegate to handle notifications
        peripheral.setDelegate(NotificationDelegate())

        # Get the service by UUID
        service = peripheral.getServiceByUUID(SERVICE_UUID)

        # Get the characteristic by UUID
        characteristic = service.getCharacteristics(CHARACTERISTIC_UUID)[0]

        # Enable notifications
        peripheral.writeCharacteristic(characteristic.getHandle() + 1, b"\x01\x00")

        print("Connected and waiting for notifications...")

        # Loop to keep receiving notifications
        while True:
            if peripheral.waitForNotifications(1.0):
                # Notification handled in handleNotification()
                continue
    except Exception as e:
        print(f"Failed to connect or retrieve data: {e}")
    finally:
        if peripheral:
            peripheral.disconnect()
            print("Disconnected from device.")

if __name__ == "__main__":
    device_address = scan_and_find_uuid()
    if device_address:
        connect_to_device(device_address)
