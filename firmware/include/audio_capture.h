#ifndef AUDIO_CAPTURE_H
#define AUDIO_CAPTURE_H

#include <Arduino.h>

// Audio input pin (ADC)
#define AUDIO_PIN 34  // GPIO34 (ADC1_CH6)

class AudioCapture {
private:
  float peakLevel;
  float rmsLevel;
  const int sampleRate = 8000; // 8kHz sampling
  
public:
  AudioCapture() : peakLevel(0), rmsLevel(0) {}
  
  void begin() {
    pinMode(AUDIO_PIN, INPUT);
    analogReadResolution(12); // 12-bit ADC resolution
    analogSetAttenuation(ADC_11db); // Full range 0-3.3V
    Serial.println("Audio capture initialized on pin " + String(AUDIO_PIN));
  }
  
  void read(float* buffer, int bufferSize) {
    float sum = 0;
    peakLevel = 0;
    
    for (int i = 0; i < bufferSize; i++) {
      // Read analog value (0-4095 for 12-bit)
      int rawValue = analogRead(AUDIO_PIN);
      
      // Convert to voltage (-1.65V to +1.65V, centered at 1.65V)
      float voltage = (rawValue / 4095.0) * 3.3;
      float centered = voltage - 1.65;
      
      buffer[i] = centered;
      
      // Calculate peak and RMS
      float absValue = abs(centered);
      if (absValue > peakLevel) {
        peakLevel = absValue;
      }
      sum += centered * centered;
      
      // Delay for sampling rate (approximate)
      delayMicroseconds(125); // 1/8000 seconds = 125 microseconds
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
