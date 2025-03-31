#include <Arduino.h>
#include <WiFi.h>
#include <WiFiClient.h>


const char* ssid = "WhyFly";      // Set here thine SSID
const char* password = "12345678";  // And here thy sacred passphrase
// const char* host = "192.168.1.1";      // The computer’s IP address
// const int port = 5000;                   // The port whence the host listeneth

#define RX_PIN 1
#define TX_PIN 0

WiFiServer server(80); // Create a server on port 80

WiFiClient client;

char dataBuffer[32000]; 
char *endOfBuffer = dataBuffer + sizeof(dataBuffer) - 1;
char *writePointer = dataBuffer;
char *readPointer = dataBuffer;

bool connect_to_client() {

  client = server.available();
  
  if (client) {
    // client.write("Now we are bound as one");

    for (int i=0; i>10; i++) {
      digitalWrite(LED_BUILTIN, HIGH);
      delay(50);
      digitalWrite(LED_BUILTIN, LOW);
      delay(50);
    }

    return true;
  }
  return false;
  
}

void setup() {
  
  // Serial.begin(9600);
  Serial1.setRX(RX_PIN);
  Serial1.setTX(TX_PIN);
  Serial1.begin(1000000);
  delay(1000);
  
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);
  delay(1000);
  digitalWrite(LED_BUILTIN, LOW);

  // Start the Pico W as a Wi-Fi Access Point
  WiFi.softAP(ssid, password);

  // Get and display the IP address
  IPAddress myIP = WiFi.softAPIP();

  server.begin(); // Start the server

  connect_to_client();
}


void readSerialData() {

  if (Serial1.available()) {

    // Serial.println(Serial1.readString());

    Serial1.readBytes(writePointer, 1);
    writePointer += 1;
    if (writePointer > endOfBuffer) {
      writePointer = dataBuffer;
    }

    
    
  }
  else {
    
  }

}




void loop() {

  readSerialData();

  if (client.connected()) {
    
    int bytesSent;

    // digitalWrite(LED_BUILTIN, HIGH);
    // client.write(writePointer);
    
    if (readPointer < writePointer && writePointer - readPointer >= 2048) {
      bytesSent = client.write(readPointer, writePointer-readPointer); // Send data until it reaches write
      // Serial.println(readPointer);
    }
    else if (readPointer < writePointer && writePointer - readPointer < 2048) {
      bytesSent = 0;
    }
    else if (readPointer == writePointer) {   // If read has cought up to write
      bytesSent = 0;
    }
    else if (readPointer > writePointer) {
      bytesSent = client.write(readPointer, endOfBuffer-readPointer+1); // Read from dataBuffer
    }

    readPointer += bytesSent;

    if (readPointer > endOfBuffer)
      readPointer = dataBuffer;
    

  }
  else {
    // client = server.available();
    // digitalWrite(LED_BUILTIN, LOW);
    connect_to_client();
  }
  

}

