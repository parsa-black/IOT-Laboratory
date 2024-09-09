#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>

#define SOIL_MOISTURE_PIN 15         // Moisture Analog pin

BLEServer *pServer = NULL;
BLECharacteristic *pCharacteristic = NULL;
bool deviceConnected = false;
bool oldDeviceConnected = false;

#define SERVICE_UUID        "7d2746a0-c3cc-46cd-9e13-e3df31050ce7"
#define CHARACTERISTIC_UUID "01f602d7-096d-4d34-a572-e82ab2ba9290"

class MyServerCallbacks : public BLEServerCallbacks {
  void onConnect(BLEServer* pServer) {
    deviceConnected = true;
  };

  void onDisconnect(BLEServer* pServer) {
    deviceConnected = false;
  }
};

void setup() {
  Serial.begin(115200);

  BLEDevice::init("ESP32_BLE_Server");
  pServer = BLEDevice::createServer();
  pServer->setCallbacks(new MyServerCallbacks());

  BLEService *pService = pServer->createService(SERVICE_UUID);
  
  pCharacteristic = pService->createCharacteristic(
                      CHARACTERISTIC_UUID,
                      BLECharacteristic::PROPERTY_READ |
                      BLECharacteristic::PROPERTY_NOTIFY
                    );

  pCharacteristic->addDescriptor(new BLE2902());

  pService->start();

  BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
  pAdvertising->addServiceUUID(SERVICE_UUID);
  pAdvertising->setScanResponse(true);
  pAdvertising->setMinPreferred(0x06);  // set value to 0x00 to not advertise this parameter
  BLEDevice::startAdvertising();
  Serial.println("Waiting for a client connection...");
}

void loop() {
  if (deviceConnected) {
  // Read the analog value from the soil moisture sensor
  int sensorValue = analogRead(SOIL_MOISTURE_PIN);

  // Convert the value to a percentage (based on experimentation)
  // Sensor outputs a value between ~0 (wet) and ~4095 (dry), depending on soil moisture
  int moisturePercent = map(sensorValue, 4095, 0, 0, 100);

  String data = String(moisturePercent) + "%";

  pCharacteristic->setValue(data.c_str());
  pCharacteristic->notify();

  // Print out the raw sensor value and moisture percentage
  Serial.print("Raw Sensor Value: ");
  Serial.print(sensorValue);
  Serial.print(" | Soil Moisture: ");
  Serial.print(moisturePercent);
  Serial.println("%");
    
    delay(2000);  // Update values every 2 seconds
  }

  if (!deviceConnected && oldDeviceConnected) {
    delay(500);  // Give the Bluetooth stack the chance to get disconnected
    pServer->startAdvertising();  // Restart advertising
    Serial.println("Waiting for a client connection...");
    oldDeviceConnected = deviceConnected;
  }

  if (deviceConnected && !oldDeviceConnected) {
    oldDeviceConnected = deviceConnected;
  }
}