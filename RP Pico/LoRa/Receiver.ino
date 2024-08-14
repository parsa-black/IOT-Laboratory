#include <Wire.h>
#include <SPI.h>
#include <LoRa.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_GFX.h>
Adafruit_SSD1306 display(128, 64);

// DHT11 Data
String temp;
String hum;

//define the pins used by the LoRa module
#define ss 17
#define rst 27
#define dio0 28

int counter = 0;

void setup() {

  // Status LED
  pinMode(15, OUTPUT);

  //initialize Serial Monitor
  Serial.begin(9600);
  while (!Serial);
  Serial.println("LoRa Receiver");

  // Initialize the display
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);  // Address 0x3C for 128x32

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
 
  // try to parse packet
  int packetSize = LoRa.parsePacket();
  if (packetSize) {
    digitalWrite(15, HIGH);
    // received a packet
    Serial.println("Received packet");

    // read packet
    while (LoRa.available()) {
      String LoRaData = LoRa.readString();
      //Serial.print(LoRaData); 
      temp = LoRaData.substring(0,5);
      Serial.println(temp);
      hum = LoRaData.substring(6,11);
      Serial.println(hum);
    }
    delay(50);
    digitalWrite(15, LOW);
    // print RSSI of packet
    //Serial.print("' with RSSI ");
    //Serial.println(LoRa.packetRssi());
  }

  display.clearDisplay();
  display.setTextColor(WHITE);
  display.setTextSize(1);
  display.setCursor(25, 0);
  display.println("IOT LAB SCU");
  display.setCursor(0, 20);
  display.print("Temp: ");
  display.print(temp);
  display.println(" C");
  display.setCursor(0, 30);
  display.print("Humidity: ");
  display.print(hum);
  display.println(" %");
  display.setCursor(25, 50);
  display.println("LoRa Project");
  display.display();
  delay(50);

  
}