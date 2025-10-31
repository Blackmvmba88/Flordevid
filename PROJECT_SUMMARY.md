# Flordevid Project Summary

## Overview
Complete modular mechatronic device for environmental signal monitoring and anomaly detection.

## Components Implemented

### 1. Firmware (ESP32) ✓
- **Location**: `/firmware/`
- **Features**:
  - Audio capture via GPIO34 (8kHz sampling)
  - EMF sensor via GPIO35
  - WiFi connectivity with web server
  - JSON data output over serial (115200 baud)
  - Modular sensor classes (audio_capture.h, emf_sensor.h)
- **Build System**: PlatformIO
- **Documentation**: firmware/README.md

### 2. AI Core (Python + TensorFlow Lite) ✓
- **Location**: `/ai_core/`
- **Modules**:
  - `main.py`: Entry point and orchestration
  - `data_processor.py`: Feature extraction (10 features)
  - `signal_analyzer.py`: Signal analysis and pattern detection
  - `anomaly_detector.py`: TFLite inference with rule-based fallback
  - `train_model.py`: Model training script
- **Classes**: Normal, Spike, Sustained, Oscillating
- **Documentation**: ai_core/README.md

### 3. Hardware Documentation ✓
- **Location**: `/hardware/`
- **Contents**:
  - Circuit schematics (audio & EMF amplification)
  - Bill of Materials (BOM)
  - Component specifications
  - Assembly instructions
  - PCB design guidelines
- **Documentation**: hardware/README.md, circuit_designs.md

### 4. UI Dashboard (FastAPI) ✓
- **Location**: `/ui/`
- **Features**:
  - Real-time WebSocket streaming
  - REST API endpoints (status, data, anomalies)
  - Embedded HTML dashboard with glass-morphism design
  - Live sensor readings display
  - Anomaly alert system
- **Tech Stack**: FastAPI, Uvicorn, WebSockets
- **Documentation**: ui/README.md

### 5. Documentation ✓
- **Location**: `/docs/`
- **Guides**:
  - `hardware_setup.md`: Complete assembly guide
  - `firmware_guide.md`: Firmware customization
  - `ai_training.md`: ML model training
  - `api_reference.md`: Complete API documentation

## Project Structure
```
Flordevid/
├── firmware/          # ESP32 C++ code
│   ├── src/
│   ├── include/
│   └── platformio.ini
├── ai_core/           # Python ML backend
│   ├── main.py
│   ├── data_processor.py
│   ├── signal_analyzer.py
│   ├── anomaly_detector.py
│   ├── train_model.py
│   └── requirements.txt
├── hardware/          # Schematics & BOM
│   ├── circuit_designs.md
│   └── README.md
├── docs/              # Technical documentation
│   ├── hardware_setup.md
│   ├── firmware_guide.md
│   ├── ai_training.md
│   └── api_reference.md
├── ui/                # FastAPI dashboard
│   ├── main.py
│   └── requirements.txt
├── README.md          # Main project README
├── LICENSE            # MIT License
└── .gitignore        # Git ignore rules
```

## Quick Start

### 1. Build Hardware
```bash
# See hardware/circuit_designs.md for schematics
# Assemble on breadboard or PCB
```

### 2. Flash Firmware
```bash
cd firmware
pio run --target upload
```

### 3. Run AI Core
```bash
cd ai_core
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py --port /dev/ttyUSB0
```

### 4. Start Dashboard
```bash
cd ui
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
# Open http://localhost:8000
```

## Features

### Audio Sensing
- 12-bit ADC resolution
- Peak and RMS level calculation
- ~8kHz sampling rate
- Amplified signal conditioning

### EMF Sensing
- Custom coil sensor
- High-impedance buffer
- Two-stage amplification
- DC to 10kHz range

### AI Classification
- 4-class anomaly detection
- TensorFlow Lite inference
- Rule-based fallback
- Real-time processing

### Dashboard
- Real-time WebSocket updates
- REST API access
- Responsive design
- Anomaly alerts

## Technology Stack

### Hardware
- ESP32-DevKitC (Dual-core, WiFi)
- LM358 Op-Amps
- AMS1117-3.3 Regulator
- Electret/MEMS microphone
- Custom EMF coil

### Firmware
- C++ (Arduino framework)
- PlatformIO
- ArduinoJson
- WiFi & WebServer libraries

### Backend
- Python 3.8+
- TensorFlow Lite
- NumPy, SciPy, Pandas
- PySerial

### Frontend
- FastAPI
- WebSockets
- HTML5/CSS3/JavaScript
- Responsive design

## Development Status

✅ Complete project structure
✅ ESP32 firmware with dual sensors
✅ Python AI core with TFLite
✅ FastAPI dashboard with WebSocket
✅ Hardware schematics and BOM
✅ Comprehensive documentation
✅ MIT License
✅ .gitignore configured
✅ All Python files syntax-verified
✅ Dashboard tested and working

## Next Steps (User-Driven)

1. **Build Hardware**: Assemble circuit on breadboard
2. **Test Firmware**: Upload to ESP32 and verify sensors
3. **Collect Data**: Gather training data for ML model
4. **Train Model**: Run train_model.py with real data
5. **Deploy**: Integrate all components
6. **Customize**: Extend with additional features

## License
MIT License - See LICENSE file

## Contributors
- BlackMamba (Blackmvmba88)
- GitHub Copilot

## Repository
https://github.com/Blackmvmba88/Flordevid
