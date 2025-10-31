#include <Arduino.h>
#include <WiFi.h>
#include <WebServer.h>
#include <ArduinoJson.h>
#include "audio_capture.h"
#include "emf_sensor.h"

// WiFi Configuration
// IMPORTANT: Update these credentials before uploading
// Or store in a separate config file not committed to version control
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// Web Server
WebServer server(80);

// Sensor instances
AudioCapture audioCapture;
EMFSensor emfSensor;

// Data buffer
const int BUFFER_SIZE = 512;
float audioBuffer[BUFFER_SIZE];
float emfBuffer[BUFFER_SIZE];

// Timing
unsigned long lastSensorRead = 0;
const unsigned long SENSOR_INTERVAL = 100; // Read every 100ms

void setupWiFi() {
  Serial.println("Connecting to WiFi...");
  WiFi.begin(ssid, password);
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nWiFi connected");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\nWiFi connection failed, continuing in standalone mode");
  }
}

void handleRoot() {
  String html = "<html><body><h1>Flordevid Sensor System</h1>";
  html += "<p><a href='/status'>Status</a> | <a href='/data'>Data</a></p>";
  html += "</body></html>";
  server.send(200, "text/html", html);
}

void handleStatus() {
  StaticJsonDocument<256> doc;
  doc["status"] = "online";
  doc["uptime"] = millis() / 1000;
  doc["wifi_connected"] = WiFi.status() == WL_CONNECTED;
  doc["audio_enabled"] = true;
  doc["emf_enabled"] = true;
  
  String response;
  serializeJson(doc, response);
  server.send(200, "application/json", response);
}

void handleData() {
  StaticJsonDocument<2048> doc;
  
  // Add audio data
  JsonArray audioArray = doc.createNestedArray("audio");
  for (int i = 0; i < 10; i++) { // Send first 10 samples
    audioArray.add(audioBuffer[i]);
  }
  
  // Add EMF data
  JsonArray emfArray = doc.createNestedArray("emf");
  for (int i = 0; i < 10; i++) { // Send first 10 samples
    emfArray.add(emfBuffer[i]);
  }
  
  doc["audio_peak"] = audioCapture.getPeakLevel();
  doc["emf_average"] = emfSensor.getAverageLevel();
  doc["timestamp"] = millis();
  
  String response;
  serializeJson(doc, response);
  server.send(200, "application/json", response);
}

void handleNotFound() {
  server.send(404, "text/plain", "Not found");
}

void setup() {
  Serial.begin(115200);
  Serial.println("\n\nFlordevid - Environmental Signal Monitor");
  Serial.println("========================================");
  
  // Initialize sensors
  Serial.println("Initializing sensors...");
  audioCapture.begin();
  emfSensor.begin();
  
  // Setup WiFi
  setupWiFi();
  
  // Setup web server
  server.on("/", handleRoot);
  server.on("/status", handleStatus);
  server.on("/data", handleData);
  server.onNotFound(handleNotFound);
  server.begin();
  Serial.println("HTTP server started");
  
  Serial.println("System ready!");
}

void loop() {
  // Handle web requests
  server.handleClient();
  
  // Read sensors at interval
  unsigned long currentMillis = millis();
  if (currentMillis - lastSensorRead >= SENSOR_INTERVAL) {
    lastSensorRead = currentMillis;
    
    // Capture audio samples
    audioCapture.read(audioBuffer, BUFFER_SIZE);
    
    // Read EMF sensor
    emfSensor.read(emfBuffer, BUFFER_SIZE);
    
    // Send data over serial in JSON format
    StaticJsonDocument<512> doc;
    doc["timestamp"] = currentMillis;
    doc["audio_peak"] = audioCapture.getPeakLevel();
    doc["audio_rms"] = audioCapture.getRMSLevel();
    doc["emf_avg"] = emfSensor.getAverageLevel();
    doc["emf_peak"] = emfSensor.getPeakLevel();
    
    serializeJson(doc, Serial);
    Serial.println();
  }
  
  // Small delay to prevent watchdog issues
  delay(1);
}
