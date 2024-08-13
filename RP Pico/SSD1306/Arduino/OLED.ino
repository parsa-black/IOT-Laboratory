#include <Adafruit_SSD1306.h>
#include <Adafruit_GFX.h>
Adafruit_SSD1306 display(128, 64);

void setup() { 
  // Initialize the display
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);  // Address 0x3C for 128x32
  // Clear the display
  display.clearDisplay();
  display.setTextColor(WHITE);
  display.setTextSize(1);
  display.setCursor(25, 0);
  display.println("IOT LAB SCU");
  display.setCursor(0, 20);
  display.println("Temp: ");
  display.setCursor(0, 30);
  display.println("Humidity: ");
  display.setCursor(25, 50);
  display.println("LoRa Project");
  display.display();
}
void loop() {
  // Nothing to do here, just display the static text
}