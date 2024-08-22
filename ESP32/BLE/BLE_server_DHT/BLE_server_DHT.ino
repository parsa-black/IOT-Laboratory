#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>
#include <DHT.h>

#define DHT_PIN 13         // DHT11 data pin

BLEServer *pServer = NULL;
BLECharacteristic *pCharacteristic = NULL;
bool deviceConnected = false;
bool oldDeviceConnected = false;
DHT dht(DHT_PIN, DHT11);

#define SERVICE_UUID        "5defff73-15e3-4782-b377-c93611890f4b"
#define CHARACTERISTIC_UUID "65b4ae96-ad4e-4e71-af5f-37abf8b4f04b"

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
  dht.begin();

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
    float temperature = dht.readTemperature();
    float humidity = dht.readHumidity();

    String data = String(temperature) + "," + String(humidity);
    
    pCharacteristic->setValue(data.c_str());
    pCharacteristic->notify();

    Serial.print("Temperature: ");
    Serial.print(temperature);
    Serial.print(" °C, Humidity: ");
    Serial.print(humidity);
    Serial.println(" %");

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