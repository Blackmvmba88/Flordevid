#include <Arduino.h>
#include <WiFi.h>
#include <WebServer.h>
#include <ArduinoJson.h>
#include "audio_capture.h"
#include "emf_sensor.h"

// Configuración WiFi
// IMPORTANTE: Actualizar estas credenciales antes de subir
// O almacenar en un archivo de configuración separado no confirmado en control de versiones
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// Servidor Web
WebServer server(80);

// Instancias de sensores
AudioCapture audioCapture;
EMFSensor emfSensor;

// Buffer de datos
const int BUFFER_SIZE = 512;
float audioBuffer[BUFFER_SIZE];
float emfBuffer[BUFFER_SIZE];

// Temporización
unsigned long lastSensorRead = 0;
const unsigned long SENSOR_INTERVAL = 100; // Leer cada 100ms

void setupWiFi() {
  Serial.println("Conectando a WiFi...");
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
  Serial.println("\n\nFlordevid - Monitor de Señales Ambientales");
  Serial.println("==========================================");
  
  // Inicializar sensores
  Serial.println("Inicializando sensores...");
  audioCapture.begin();
  emfSensor.begin();
  
  // Configurar WiFi
  setupWiFi();
  
  // Configurar servidor web
  server.on("/", handleRoot);
  server.on("/status", handleStatus);
  server.on("/data", handleData);
  server.onNotFound(handleNotFound);
  server.begin();
  Serial.println("Servidor HTTP iniciado");
  
  Serial.println("Sistema listo!");
}

void loop() {
  // Manejar solicitudes web
  server.handleClient();
  
  // Leer sensores en intervalo
  unsigned long currentMillis = millis();
  if (currentMillis - lastSensorRead >= SENSOR_INTERVAL) {
    lastSensorRead = currentMillis;
    
    // Capturar muestras de audio
    audioCapture.read(audioBuffer, BUFFER_SIZE);
    
    // Leer sensor EMF
    emfSensor.read(emfBuffer, BUFFER_SIZE);
    
    // Enviar datos por serial en formato JSON
    StaticJsonDocument<512> doc;
    doc["timestamp"] = currentMillis;
    doc["audio_peak"] = audioCapture.getPeakLevel();
    doc["audio_rms"] = audioCapture.getRMSLevel();
    doc["emf_avg"] = emfSensor.getAverageLevel();
    doc["emf_peak"] = emfSensor.getPeakLevel();
    
    serializeJson(doc, Serial);
    Serial.println();
  }
  
  // Pequeño retardo para prevenir problemas de watchdog
  delay(1);
}
