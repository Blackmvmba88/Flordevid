#ifndef EMF_SENSOR_H
#define EMF_SENSOR_H

#include <Arduino.h>

// Pin de entrada del sensor EMF (ADC)
#define EMF_PIN 35  // GPIO35 (ADC1_CH7)

class EMFSensor {
private:
  float averageLevel;
  float peakLevel;
  
public:
  EMFSensor() : averageLevel(0), peakLevel(0) {}
  
  void begin() {
    pinMode(EMF_PIN, INPUT);
    analogReadResolution(12); // Resolución ADC de 12 bits
    analogSetAttenuation(ADC_11db); // Rango completo 0-3.3V
    Serial.println("Sensor EMF inicializado en pin " + String(EMF_PIN));
  }
  
  void read(float* buffer, int bufferSize) {
    float sum = 0;
    peakLevel = 0;
    
    for (int i = 0; i < bufferSize; i++) {
      // Leer valor analógico (0-4095 para 12 bits)
      int rawValue = analogRead(EMF_PIN);
      
      // Convertir a voltaje (0-3.3V)
      float voltage = (rawValue / 4095.0) * 3.3;
      
      buffer[i] = voltage;
      
      // Calcular pico y promedio
      if (voltage > peakLevel) {
        peakLevel = voltage;
      }
      sum += voltage;
      
      // Pequeño retardo entre lecturas
      delayMicroseconds(100);
    }
    
    averageLevel = sum / bufferSize;
  }
  
  float getAverageLevel() const {
    return averageLevel;
  }
  
  float getPeakLevel() const {
    return peakLevel;
  }
  
  // Obtener lectura única para verificaciones rápidas
  float readSingle() {
    int rawValue = analogRead(EMF_PIN);
    return (rawValue / 4095.0) * 3.3;
  }
};

#endif // EMF_SENSOR_H
