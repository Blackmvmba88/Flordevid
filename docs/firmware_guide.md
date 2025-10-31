# Firmware Guide

Complete guide to understanding, customizing, and extending the Flordevid ESP32 firmware.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Configuration](#configuration)
3. [Code Structure](#code-structure)
4. [Customization](#customization)
5. [Advanced Features](#advanced-features)

## Architecture Overview

The firmware is structured as a modular system with three main components:

```
main.cpp
├── AudioCapture (audio_capture.h)
├── EMFSensor (emf_sensor.h)
└── WebServer (WiFi + HTTP)
```

### Main Loop Flow

```
Setup:
├── Initialize serial (115200 baud)
├── Initialize sensors
├── Connect to WiFi
└── Start web server

Loop:
├── Handle web requests
├── Read sensors (every 100ms)
├── Output JSON to serial
└── Small delay (prevent watchdog)
```

## Configuration

### WiFi Settings

Edit `src/main.cpp`:

```cpp
// Line ~10
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
```

### Sensor Timing

```cpp
// Line ~20
const unsigned long SENSOR_INTERVAL = 100; // Read every 100ms
```

Recommendations:
- Faster: 50ms (20 samples/sec) - Higher CPU load
- Standard: 100ms (10 samples/sec) - Balanced
- Slower: 200ms (5 samples/sec) - Lower power

### GPIO Pin Assignments

Audio sensor pin (`include/audio_capture.h`):
```cpp
#define AUDIO_PIN 34  // GPIO34 (ADC1_CH6)
```

EMF sensor pin (`include/emf_sensor.h`):
```cpp
#define EMF_PIN 35  // GPIO35 (ADC1_CH7)
```

**Available ADC pins**: 32, 33, 34, 35, 36, 39

## Code Structure

### main.cpp

Main program file with:
- WiFi connection management
- Web server endpoints
- Sensor reading loop
- Serial data output

Key functions:
```cpp
setupWiFi()          // Initialize WiFi connection
handleRoot()         // Serve homepage
handleStatus()       // Return system status JSON
handleData()         // Return sensor data JSON
setup()              // System initialization
loop()               // Main execution loop
```

### audio_capture.h

Audio capture class with:
- ADC configuration
- Peak level detection
- RMS (Root Mean Square) calculation
- Sampling rate control

Key methods:
```cpp
begin()              // Initialize audio capture
read(buffer, size)   // Read audio samples
getPeakLevel()       // Get peak amplitude
getRMSLevel()        // Get RMS level
```

### emf_sensor.h

EMF sensor class with:
- ADC configuration
- Average level calculation
- Peak detection
- Single reading capability

Key methods:
```cpp
begin()              // Initialize EMF sensor
read(buffer, size)   // Read EMF samples
getAverageLevel()    // Get average reading
getPeakLevel()       // Get peak reading
readSingle()         // Quick single reading
```

## Customization

### Changing Sampling Rate

Audio capture uses ~8kHz sampling. To modify:

```cpp
// In audio_capture.h, line ~40
delayMicroseconds(125); // 1/8000 = 125µs
```

For different rates:
- 4kHz: `delayMicroseconds(250)`
- 16kHz: `delayMicroseconds(62)`
- 44.1kHz: `delayMicroseconds(23)` (CPU intensive!)

### Adjusting ADC Resolution

Default is 12-bit (0-4095). To change:

```cpp
// In sensor headers
analogReadResolution(12); // 9, 10, 11, or 12 bits
```

Higher resolution = more precision, but slower

### Adding Digital Filtering

Implement low-pass filter for noise reduction:

```cpp
// Add to audio_capture.h
float alpha = 0.1; // Smoothing factor
float filtered_value = 0;

void read(float* buffer, int bufferSize) {
    for (int i = 0; i < bufferSize; i++) {
        float raw = analogRead(AUDIO_PIN) / 4095.0 * 3.3;
        filtered_value = alpha * raw + (1 - alpha) * filtered_value;
        buffer[i] = filtered_value;
    }
}
```

### Adding More Endpoints

Add new web server routes in `main.cpp`:

```cpp
void handleCustom() {
    StaticJsonDocument<256> doc;
    doc["custom_data"] = "your_value";
    
    String response;
    serializeJson(doc, response);
    server.send(200, "application/json", response);
}

// In setup():
server.on("/custom", handleCustom);
```

## Advanced Features

### 1. FFT (Frequency Analysis)

Add FFT for frequency domain analysis:

```cpp
// Add to platformio.ini
lib_deps = arduinoFFT@^1.6.0

// In main.cpp
#include <arduinoFFT.h>

arduinoFFT FFT = arduinoFFT();
const uint16_t samples = 256;
double vReal[samples];
double vImag[samples];

void performFFT() {
    // Collect samples
    for(int i = 0; i < samples; i++) {
        vReal[i] = analogRead(AUDIO_PIN);
        vImag[i] = 0;
        delayMicroseconds(125);
    }
    
    // Compute FFT
    FFT.Windowing(vReal, samples, FFT_WIN_TYP_HAMMING, FFT_FORWARD);
    FFT.Compute(vReal, vImag, samples, FFT_FORWARD);
    FFT.ComplexToMagnitude(vReal, vImag, samples);
    
    // Find peak frequency
    double peak = FFT.MajorPeak(vReal, samples, 8000);
    Serial.print("Peak frequency: ");
    Serial.println(peak);
}
```

### 2. SD Card Logging

Log data to SD card:

```cpp
// Add to platformio.ini
lib_deps = SD

// In main.cpp
#include <SD.h>
#include <SPI.h>

const int SD_CS = 5; // SD card chip select

void setup() {
    // ... existing code ...
    
    if (!SD.begin(SD_CS)) {
        Serial.println("SD card initialization failed!");
    }
}

void logToSD(float audio, float emf) {
    File dataFile = SD.open("/data.csv", FILE_APPEND);
    if (dataFile) {
        dataFile.print(millis());
        dataFile.print(",");
        dataFile.print(audio);
        dataFile.print(",");
        dataFile.println(emf);
        dataFile.close();
    }
}
```

### 3. OLED Display

Add real-time display:

```cpp
// Add to platformio.ini
lib_deps = Adafruit SSD1306, Adafruit GFX Library

// In main.cpp
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

void setup() {
    // ... existing code ...
    
    if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
        Serial.println("SSD1306 allocation failed");
    }
    display.clearDisplay();
}

void updateDisplay(float audio, float emf) {
    display.clearDisplay();
    display.setTextSize(1);
    display.setTextColor(WHITE);
    display.setCursor(0, 0);
    
    display.println("FLORDEVID");
    display.println();
    display.print("Audio: ");
    display.println(audio, 3);
    display.print("EMF: ");
    display.println(emf, 3);
    
    display.display();
}
```

### 4. Deep Sleep Mode

Implement power saving:

```cpp
void enterDeepSleep(int seconds) {
    Serial.println("Entering deep sleep...");
    esp_sleep_enable_timer_wakeup(seconds * 1000000ULL);
    esp_deep_sleep_start();
}

// In loop(), add condition:
if (battery_low) {
    logData(); // Save any pending data
    enterDeepSleep(60); // Sleep for 60 seconds
}
```

### 5. OTA (Over-The-Air) Updates

Enable wireless firmware updates:

```cpp
#include <ArduinoOTA.h>

void setupOTA() {
    ArduinoOTA.setHostname("flordevid");
    ArduinoOTA.setPassword("your_password");
    
    ArduinoOTA.onStart([]() {
        Serial.println("OTA Start");
    });
    
    ArduinoOTA.onEnd([]() {
        Serial.println("\nOTA End");
    });
    
    ArduinoOTA.begin();
}

// In setup():
setupOTA();

// In loop():
ArduinoOTA.handle();
```

### 6. MQTT Publishing

Send data to MQTT broker:

```cpp
// Add to platformio.ini
lib_deps = PubSubClient

#include <PubSubClient.h>

WiFiClient espClient;
PubSubClient mqtt(espClient);

const char* mqtt_server = "broker.hivemq.com";

void setupMQTT() {
    mqtt.setServer(mqtt_server, 1883);
}

void publishData(float audio, float emf) {
    if (!mqtt.connected()) {
        mqtt.connect("flordevid");
    }
    
    String payload = String(audio) + "," + String(emf);
    mqtt.publish("flordevid/sensors", payload.c_str());
}

// In loop():
mqtt.loop();
publishData(audioPeak, emfAvg);
```

## Building and Uploading

### Using PlatformIO CLI

```bash
# Build firmware
pio run

# Upload to device
pio run --target upload

# Monitor serial output
pio device monitor

# All in one
pio run --target upload && pio device monitor
```

### Using PlatformIO IDE (VSCode)

1. Open `/firmware` folder in VSCode
2. PlatformIO should auto-detect project
3. Click "Build" icon (✓)
4. Click "Upload" icon (→)
5. Click "Serial Monitor" icon to view output

### Using Arduino IDE

1. Install ESP32 board support
2. Open `src/main.cpp`
3. Tools → Board → ESP32 Dev Module
4. Tools → Port → (select your port)
5. Sketch → Upload

## Debugging

### Serial Debugging

Add debug messages:

```cpp
#define DEBUG 1

#ifdef DEBUG
  #define DEBUG_PRINT(x) Serial.print(x)
  #define DEBUG_PRINTLN(x) Serial.println(x)
#else
  #define DEBUG_PRINT(x)
  #define DEBUG_PRINTLN(x)
#endif

// Usage:
DEBUG_PRINTLN("Starting sensor read...");
```

### Watchdog Timer

If ESP32 resets unexpectedly:

```cpp
// Disable watchdog for long operations
disableCore0WDT();
longRunningFunction();
enableCore0WDT();
```

### Memory Monitoring

Check free memory:

```cpp
void printMemory() {
    Serial.print("Free heap: ");
    Serial.println(ESP.getFreeHeap());
}
```

## Performance Optimization

### 1. Reduce Serial Output

Minimize serial prints in high-speed loops

### 2. Use DMA for ADC

For high-speed continuous sampling (advanced)

### 3. Optimize JSON

Use smaller JSON documents or binary protocol

### 4. WiFi Power Management

```cpp
WiFi.setSleep(true); // Enable WiFi sleep
```

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Won't compile | Missing libraries | Check platformio.ini |
| Can't upload | Wrong port/driver | Install CP210x driver |
| ESP32 reboots | Watchdog timeout | Add delays, reduce CPU load |
| WiFi won't connect | Wrong credentials | Check SSID/password |
| Readings always 0 | Wrong GPIO pin | Verify pin definitions |

## Best Practices

1. **Always check return values**
2. **Add error handling**
3. **Use const for constants**
4. **Comment your code**
5. **Test incrementally**
6. **Keep functions small**
7. **Use version control**

## Next Steps

- Integrate with AI core: [ai_training.md](ai_training.md)
- Build dashboard: See `/ui` folder
- Add more sensors
- Implement custom features

## Resources

- [ESP32 Arduino Core](https://github.com/espressif/arduino-esp32)
- [PlatformIO Documentation](https://docs.platformio.org/)
- [ArduinoJSON Library](https://arduinojson.org/)
- [ESP32 Forums](https://esp32.com/)

## License

MIT License - See LICENSE file in root directory
