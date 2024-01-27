#include <Wifi.h>
# include "DHT.h"
#include <ThingsBoard.h>

// define DHT
#define DHTPIN 14
#define DHTTYPE DHT11
// define LED Pin
#define Red 23
#define Yellow 22
#define Green 21

DHT dht(DHTPIN, DHTTYPE);

// Helper macro to calculate array size
#define COUNT_OF(x) ((sizeof(x)/sizeof(0[x])) / ((size_t)(!(sizeof(x) % sizeof(0[x])))))

// WiFi access point
#define  WIFI_SSID[] = "YOUR_WIFI_SSID";
// WiFi password
#define WIFI_PASSWORD[] = "YOUR_WIFI_PASSWORD";

// to understand how to obtain an access token
#define TOKEN[] = "YOUR_ACCESS_TOKEN";

// Thingsboard we want to establish a connection too
#define THINGSBOARD_SERVER[] = "THINGSBOARD_DASHBOARD_DOMAIN";

// Baud rate for the debugging serial connection.
#define SERIAL_DEBUG_BAUD = 115200U;

// Initialize ThingsBoard client
WiFiClient wifiClient;
// Initialize ThingsBoard instance
ThingsBoard tb(wifiClient);


void setup() {
  Serial.begin(SERIAL_DEBUG_BAUD);

  // Pinconfig
  pinMode(Red, OUTPUT);
  pinMode(Yellow, OUTPUT);
  pinMode(Green, OUTPUT);

  // Connect to Wi-Fi
  digitalWrite(Red, HIGH);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    digitalWrite(Yellow, HIGH);
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  digitalWrite(Red, LOW);
  digitalWrite(Yellow, LOW);
  digitalWrite(Green, HIGH);
  Serial.println("Connected to WiFi");

  // Connect to ThingsBoard
  tb.begin(thingsboardServer, deviceToken);

  // Initialize DHT sensor
  dht.begin();

}

void loop() {
  float h = dht.readHumidity();
  //Read the moisture content in %.
  float t = dht.readTemperature();
  //Read the temperature in degrees Celsius

  if (isnan(h) || isnan(t)) {
    Serial.println("Failed reception");
    return;
    //Returns an error if the ESP32 does not receive any measurements
  }
  else {
      // Print sensor values to Serial Monitor
    Serial.print("Temperature: ");
    Serial.print(temperature);
    Serial.print(" °C, Humidity: ");
    Serial.print(humidity);
    Serial.println(" %\n");

    // Upload data to ThingsBoard
    tb.sendTelemetryFloat("temperature", temperature);
    tb.sendTelemetryFloat("humidity", humidity);

  }

  delay(5000); // Upload data every 5 seconds

}
