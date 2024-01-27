#include <WiFi.h>
#include "DHT.h"
#include "ThingsBoard.h"
#include <ArduinoJson.h>

// define DHT
#define DHTPIN 14
#define DHTTYPE DHT11
// define LED Pin
#define Red 23
#define Yellow 22
#define Green 21

DHT dht(DHTPIN, DHTTYPE);

// WiFi access point
const char* WIFI_SSID = "PARSA";
// WiFi password
const char* WIFI_PASSWORD = "44527481";

// to understand how to obtain an access token
const char* TOKEN = "YrdzdUzEkaHhORX0P0UU";

// Thingsboard we want to establish a connection to
const char* THINGSBOARD_SERVER = "iot.scu.ac.ir";

// Initialize ThingsBoard client
WiFiClient wifiClient;
// Initialize ThingsBoard instance
ThingsBoard tb(wifiClient);
// the Wifi radio's status
int status = WL_IDLE_STATUS;
unsigned long lastSend;

void setup() {
  Serial.begin(115200);
  // Wifi
  Serial.println("Connecting to AP ...");
  // attempt to connect to WiFi network
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("Connected to AP");

  // Initialize DHT sensor
  dht.begin();
  lastSend = 0;
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    reconnect();
  }


  if (!tb.connected()) {
    // Connect to the ThingsBoard
    Serial.print("Connecting to: ");
    Serial.print(THINGSBOARD_SERVER);
    Serial.print(" with token ");
    Serial.println(TOKEN);
    if (!tb.connect(THINGSBOARD_SERVER, TOKEN)) {
      Serial.println("Failed to connect");
      return;
    }
  }

  if ( millis() - lastSend > 1000 ) { // Update and send only after 1 seconds
    getAndSendTemperatureAndHumidityData();
    lastSend = millis();
  }

  tb.loop();
}

void getAndSendTemperatureAndHumidityData()
{
  Serial.println("Collecting temperature data.");

  // Reading temperature or humidity takes about 250 milliseconds!
  float humidity = dht.readHumidity();
  // Read temperature as Celsius (the default)
  float temperature = dht.readTemperature();

  // Check if any reads failed and exit early (to try again).
  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  Serial.println("Sending data to ThingsBoard:");
  Serial.print("Humidity: ");
  Serial.print(humidity);
  Serial.print(" %\t");
  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.println(" *C ");

  tb.sendTelemetryFloat("temperature", temperature);
  tb.sendTelemetryFloat("humidity", humidity);
}

void reconnect() {
  // Loop until we're reconnected
  while (!tb.connected()) {
    status = WiFi.status();
    if ( status != WL_CONNECTED) {
      WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
      while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
      }
      Serial.println("Connected to AP");
    }
    Serial.print("Connecting to ThingsBoard node ...");
    if ( tb.connect(THINGSBOARD_SERVER, TOKEN) ) {
      Serial.println( "[DONE]" );
    } else {
      Serial.print( "[FAILED]" );
      Serial.println( " : retrying in 5 seconds]" );
      // Wait 5 seconds before retrying
      delay( 5000 );
    }
  }
}
