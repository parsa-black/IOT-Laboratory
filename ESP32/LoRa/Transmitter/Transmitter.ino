#include <SPI.h>
#include <DHT.h>
#include <LoRa.h>

//define the pins used by the DHT11 sensor
#define DHTPIN 13
#define DHTTYPE DHT11  

//define the pins used by the LoRa module
#define ss 5
#define rst 14
#define dio0 2

// Count Packet
int counter = 0;

//initialize DHT11 sensor
DHT dht(DHTPIN, DHTTYPE);

void setup() {

  // Status LED
  pinMode(27, OUTPUT);

  //initialize Serial Monitor
  Serial.begin(9600);
  while (!Serial);
  Serial.println("LoRa Sender");
  Serial.println(F("DHTxx test!"));

  //initialize DHT11 sensor
  dht.begin();

  //setup LoRa transceiver module
  LoRa.setPins(ss, rst, dio0);

  //replace the LoRa.begin(---E-) argument with your location's frequency 
  //433E6 for Asia
  //866E6 for Europe
  //915E6 for North America
  while (!LoRa.begin(433E6)) {
    Serial.println(".");
    delay(500);
  }
  // Change sync word (0xF3) to match the receiver
  // The sync word assures you don't get LoRa messages from other LoRa transceivers
  // ranges from 0-0xFF
  LoRa.setSyncWord(0xF3);
  Serial.println("LoRa Initializing OK!");
}

void loop() {

  delay(2000);
  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  float h = dht.readHumidity();
  // Read temperature as Celsius (the default)
  float t = dht.readTemperature();

  // Check if any reads failed and exit early (to try again).
  if (isnan(h) || isnan(t)) {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }

  Serial.print("Sending packet: ");
  Serial.print(counter);
  Serial.print(F(" , Temperature: "));
  Serial.print(t);
  Serial.print(F("°C "));
  Serial.print(F(" , Humidity: "));
  Serial.print(h);
  Serial.println(F("%"));
   

  //Send LoRa packet to receiver
  digitalWrite(27, HIGH);
  LoRa.beginPacket();
  //LoRa.print("Temperature: ");
  LoRa.print(t);
  LoRa.print(",");
  LoRa.print(h);
  //  LoRa.print(" Humidity: ");
  //  LoRa.print(h);
  LoRa.endPacket();
  delay(200);
  digitalWrite(27, LOW);

  counter++;

  delay(50);
}