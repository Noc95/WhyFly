#include <Arduino.h>
#include <WiFi.h>
#include <WiFiClient.h>


const char* ssid = "WhyFly";      // Set here thine SSID
const char* password = "12345678";  // And here thy sacred passphrase
// const char* host = "192.168.1.1";      // The computer’s IP address
// const int port = 5000;                   // The port whence the host listeneth

WiFiServer server(80); // Create a server on port 80

WiFiClient client = server.available();

char dataBuffer[32000]; 
char *endOfBuffer = dataBuffer + sizeof(dataBuffer) - 1;
char *writePointer = dataBuffer;
char *readPointer = dataBuffer;

void setup() {

  Serial.begin(115200);
  delay(1000);
  
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);

  // Start the Pico W as a Wi-Fi Access Point
  WiFi.softAP(ssid, password);

  // Get and display the IP address
  IPAddress myIP = WiFi.softAPIP();

  server.begin(); // Start the server

  
}


void readSerialData() {

  if (Serial.available()) {
    // String message = Serial.readStringUntil('\n');
    Serial.readBytes(writePointer, 1);
    writePointer += 1;
    if (writePointer > endOfBuffer) {
      writePointer = dataBuffer;
    }
    
  }

}




void loop() {

  readSerialData();

  if (client) {
    
    int bytesSent;
    
    if (readPointer < writePointer && writePointer - readPointer >= 2048) {
      bytesSent = client.write(readPointer, writePointer-readPointer); // Send data until it reaches write
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
    client = server.available();
  }
  

}

