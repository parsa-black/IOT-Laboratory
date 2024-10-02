#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>

#define MQ135_PIN 4  // Use GPIO4 for the MQ135 sensor

BLEServer *pServer = NULL;
BLECharacteristic *pCharacteristic = NULL;
bool deviceConnected = false;

#define SERVICE_UUID        "f7c57db6-55ab-4fb5-8d82-910fa8bc9bfb"
#define CHARACTERISTIC_UUID "db5e1c84-898f-4276-bd39-dbfd22ffa18c"

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
  
  BLEDevice::init("ESP32_BLE_Server_MQ135");
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
  BLEDevice::startAdvertising();
  Serial.println("Waiting for a client connection...");
}

void loop() {
  if (deviceConnected) {
    int mq135Value = analogRead(MQ135_PIN);  // Read from the MQ135 sensor on GPIO4
    
    String data = String(mq135Value);  // Convert to string
    pCharacteristic->setValue(data.c_str());
    pCharacteristic->notify();

    Serial.print("MQ135 Value: ");
    Serial.println(mq135Value);
    
    delay(2000);  // Update values every 2 seconds
  }
}
