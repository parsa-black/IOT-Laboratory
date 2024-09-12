import bluetooth
import struct
import time
from machine import Pin, ADC

# Define UUIDs for the service and characteristics
SERVICE_UUID = bluetooth.UUID("7d2746a0-c3cc-46cd-9e13-e3df31050ce7")  # Environmental Sensing Service
MOIST_CHAR_UUID = bluetooth.UUID("01f602d7-096d-4d34-a572-e82ab2ba9290")  # Soil Moisture Characteristic

# Create the service and characteristics
service = (
    SERVICE_UUID,
    (
        (MOIST_CHAR_UUID, bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY),
    ),
)

# Create BLE object
ble = bluetooth.BLE()
ble.active(True)

# Register the service
handles = ble.gatts_register_services([service])

# Get the characteristic handle
moist_handle = handles[0][0]

# Define sensor pins (real sensor readings)
soil = ADC(Pin(26))  # Soil moisture sensor connected to GP26 (ADC0)

# Calibration values for Capacitive Soil Moisture Sensor v2.0
min_moisture = 19200
max_moisture = 49300

# Function to create the advertising payload manually
def advertising_payload(name=None, services=None):
    payload = bytearray()

    def _append(adv_type, value):
        payload.append(len(value) + 1)
        payload.append(adv_type)
        payload.extend(value)

    # Flag indicating general discoverable mode
    _append(0x01, struct.pack("B", 0x06))

    # Complete List of 16-bit Service Class UUIDs
    if services:
        for uuid in services:
            _append(0x03, struct.pack("<h", uuid))

    # Complete Local Name
    if name:
        _append(0x09, name.encode())

    return payload

# Function to advertise the BLE service
def advertise():
    print("Starting advertising")
    adv_data = advertising_payload(
        name="PicoW_BLE",
        services=[0x181A]
    )
    ble.gap_advertise(100, adv_data)

# Function to update the sensor readings and notify connected clients
def update_readings():
    # Read the sensor values
    moisture = (max_moisture - soil.read_u16()) * 100 / (max_moisture - min_moisture)  # Soil Moisture calculation
    
    print(f"Moisture: {moisture:.2f}% (ADC: {soil.read_u16()})")
    
    # Pack the data into bytes
    moist_data = struct.pack('<H', int(moisture * 100))  # Packing as an unsigned short (16-bit)
    print(f"Packed data: {moist_data}")
    
    # Write the values to the characteristic
    try:
        ble.gatts_write(moist_handle, moist_data)
        print("Successfully wrote to characteristic")
    except Exception as e:
        print(f"Error writing to characteristic: {e}")
    
    # Notify connected clients
    try:
        ble.gatts_notify(0, moist_handle)
        print("Notification sent successfully")
    except Exception as e:
        print(f"Error notifying clients: {e}")

# Start advertising the BLE service
advertise()

# Main loop to update sensor readings
while True:
    update_readings()
    time.sleep(10)  # Update every 10 seconds
