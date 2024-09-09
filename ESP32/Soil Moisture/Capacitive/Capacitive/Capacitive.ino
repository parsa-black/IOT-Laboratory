// Define the analog pin connected to the sensor
#define SOIL_MOISTURE_PIN 15  // You can change the pin based on your connection

void setup() {
  // Start the serial communication
  Serial.begin(115200);
  // Initialize the analog pin as an input
  pinMode(SOIL_MOISTURE_PIN, INPUT);
}

void loop() {
  // Read the analog value from the soil moisture sensor
  int sensorValue = analogRead(SOIL_MOISTURE_PIN);

  // Convert the value to a percentage (based on experimentation)
  // Sensor outputs a value between ~0 (wet) and ~4095 (dry), depending on soil moisture
  int moisturePercent = map(sensorValue, 4095, 0, 0, 100);

  // Print out the raw sensor value and moisture percentage
  Serial.print("Raw Sensor Value: ");
  Serial.print(sensorValue);
  Serial.print(" | Soil Moisture: ");
  Serial.print(moisturePercent);
  Serial.println("%");

  // Wait 1 second before taking another reading
  delay(1000);
}
