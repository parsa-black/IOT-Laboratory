void setup(){
  Serial.begin(9600); //initialize serial communication at a 9600 baud rate
}

void loop(){
  Serial.print("Arduino UNO");
  delay(1000);
}