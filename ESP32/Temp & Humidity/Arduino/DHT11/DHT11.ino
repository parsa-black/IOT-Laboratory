# include "DHT.h"

#define DHTPIN 14
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();

}

void loop() {
  delay(1000);
  // The DHT11 returns at most one measurement every 1s
  float h = dht.readHumidity();
  //Read the moisture content in %.
  float t = dht.readTemperature();
  //Read the temperature in degrees Celsius

  if (isnan(h) || isnan(t)) {
    Serial.println("Failed reception");
    return;
    //Returns an error if the ESP32 does not receive any measurements
  }

  Serial.print("Humidite: ");
  Serial.print(h);
  Serial.print("%  Temperature: ");
  Serial.print(t);
  Serial.print("°C, \n");
  // Transmits the measurements received in the serial monitor
}
