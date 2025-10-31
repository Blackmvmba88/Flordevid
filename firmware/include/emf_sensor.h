#ifndef EMF_SENSOR_H
#define EMF_SENSOR_H

#include <Arduino.h>

// EMF sensor input pin (ADC)
#define EMF_PIN 35  // GPIO35 (ADC1_CH7)

class EMFSensor {
private:
  float averageLevel;
  float peakLevel;
  
public:
  EMFSensor() : averageLevel(0), peakLevel(0) {}
  
  void begin() {
    pinMode(EMF_PIN, INPUT);
    analogReadResolution(12); // 12-bit ADC resolution
    analogSetAttenuation(ADC_11db); // Full range 0-3.3V
    Serial.println("EMF sensor initialized on pin " + String(EMF_PIN));
  }
  
  void read(float* buffer, int bufferSize) {
    float sum = 0;
    peakLevel = 0;
    
    for (int i = 0; i < bufferSize; i++) {
      // Read analog value (0-4095 for 12-bit)
      int rawValue = analogRead(EMF_PIN);
      
      // Convert to voltage (0-3.3V)
      float voltage = (rawValue / 4095.0) * 3.3;
      
      buffer[i] = voltage;
      
      // Calculate peak and average
      if (voltage > peakLevel) {
        peakLevel = voltage;
      }
      sum += voltage;
      
      // Small delay between readings
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
  
  // Get single reading for quick checks
  float readSingle() {
    int rawValue = analogRead(EMF_PIN);
    return (rawValue / 4095.0) * 3.3;
  }
};

#endif // EMF_SENSOR_H
