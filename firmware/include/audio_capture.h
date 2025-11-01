#ifndef AUDIO_CAPTURE_H
#define AUDIO_CAPTURE_H

#include <Arduino.h>

// Pin de entrada de audio (ADC)
#define AUDIO_PIN 34  // GPIO34 (ADC1_CH6)

class AudioCapture {
private:
  float peakLevel;
  float rmsLevel;
  const int sampleRate = 8000; // Muestreo 8kHz
  
public:
  AudioCapture() : peakLevel(0), rmsLevel(0) {}
  
  void begin() {
    pinMode(AUDIO_PIN, INPUT);
    analogReadResolution(12); // Resolución ADC de 12 bits
    analogSetAttenuation(ADC_11db); // Rango completo 0-3.3V
    Serial.println("Captura de audio inicializada en pin " + String(AUDIO_PIN));
  }
  
  void read(float* buffer, int bufferSize) {
    float sum = 0;
    peakLevel = 0;
    
    for (int i = 0; i < bufferSize; i++) {
      // Leer valor analógico (0-4095 para 12 bits)
      int rawValue = analogRead(AUDIO_PIN);
      
      // Convertir a voltaje (-1.65V a +1.65V, centrado en 1.65V)
      float voltage = (rawValue / 4095.0) * 3.3;
      float centered = voltage - 1.65;
      
      buffer[i] = centered;
      
      // Calcular pico y RMS
      float absValue = abs(centered);
      if (absValue > peakLevel) {
        peakLevel = absValue;
      }
      sum += centered * centered;
      
      // Retardo para tasa de muestreo (aproximado)
      delayMicroseconds(125); // 1/8000 segundos = 125 microsegundos
    }
    
    rmsLevel = sqrt(sum / bufferSize);
  }
  
  float getPeakLevel() const {
    return peakLevel;
  }
  
  float getRMSLevel() const {
    return rmsLevel;
  }
};

#endif // AUDIO_CAPTURE_H
