# Flordevid Firmware

ESP32 firmware for multi-sensor data acquisition supporting audio and EMF (electromagnetic field) sensing.

## Features

- **Audio Capture**: 8kHz sampling rate with peak and RMS level calculation
- **EMF Sensing**: Continuous electromagnetic field monitoring
- **WiFi Connectivity**: Real-time data streaming over WiFi
- **HTTP API**: RESTful endpoints for sensor data access
- **Serial Output**: JSON-formatted data output for direct connection

## Hardware Connections

### Audio Sensor
- **Pin**: GPIO34 (ADC1_CH6)
- **Sensor**: MAX4466 or INMP441 microphone module
- **Connection**: Analog output to GPIO34

### EMF Sensor
- **Pin**: GPIO35 (ADC1_CH7)
- **Sensor**: Custom coil with amplifier or AD8232
- **Connection**: Analog output to GPIO35

### Power
- **VCC**: 5V via USB or 3.3V regulated
- **GND**: Common ground for all components

## Building and Flashing

### Using PlatformIO (Recommended)

1. Install PlatformIO:
```bash
pip install platformio
```

2. Build the firmware:
```bash
cd firmware
pio run
```

3. Upload to ESP32:
```bash
pio run --target upload
```

4. Monitor serial output:
```bash
pio device monitor
```

### Using Arduino IDE

1. Install ESP32 board support
2. Open `src/main.cpp` in Arduino IDE
3. Select board: "ESP32 Dev Module"
4. Select correct COM port
5. Upload

## Configuration

Edit `src/main.cpp` to configure:

```cpp
// WiFi credentials
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// Sampling parameters
const int BUFFER_SIZE = 512;
const unsigned long SENSOR_INTERVAL = 100; // ms
```

## API Endpoints

Once connected to WiFi, access:

- `http://<ESP32_IP>/` - Home page
- `http://<ESP32_IP>/status` - System status
- `http://<ESP32_IP>/data` - Current sensor data

## Serial Protocol

Data is output in JSON format at 115200 baud:

```json
{
  "timestamp": 12345,
  "audio_peak": 0.45,
  "audio_rms": 0.23,
  "emf_avg": 1.2,
  "emf_peak": 2.1
}
```

## Troubleshooting

### No WiFi connection
- Verify SSID and password
- Check signal strength
- The device will continue in standalone mode

### No sensor readings
- Check GPIO pin connections
- Verify sensor power supply
- Check serial monitor for initialization messages

### Compilation errors
- Ensure all dependencies are installed
- Update PlatformIO platform: `pio platform update`

## Dependencies

- ESP32 Arduino Framework
- ArduinoJson (^6.21.0)
- arduinoFFT (^1.6.0) - For future FFT analysis

## License

MIT License - See LICENSE file in root directory
