# Flordevid

A modular mechatronic device for recording, amplifying, and analyzing environmental signals to detect anomalous patterns. The system combines ESP32-based firmware for multi-sensor data acquisition, analog amplification circuits, and AI-powered pattern recognition using TensorFlow Lite.

## 🚀 Features

- **Multi-Sensor Data Acquisition**: Audio and EMF (electromagnetic field) sensing via ESP32
- **Signal Amplification**: Custom analog circuits for weak signal amplification
- **AI-Powered Analysis**: TensorFlow Lite models for real-time anomaly classification
- **Web Dashboard**: FastAPI-based interface for monitoring and visualization
- **Modular Design**: Organized architecture for easy extension and maintenance

## 📁 Project Structure

```
Flordevid/
├── firmware/          # ESP32 firmware for sensor data capture
├── ai_core/           # Python backend with TensorFlow Lite for classification
├── hardware/          # Circuit schematics and hardware documentation
├── docs/              # Technical documentation and guides
├── ui/                # FastAPI dashboard and web interface
├── README.md          # This file
├── LICENSE            # MIT License
└── .gitignore        # Git ignore rules
```

## 🔧 Hardware Requirements

- ESP32 development board (ESP32-DevKitC or similar)
- Microphone/audio sensor (e.g., MAX4466, INMP441)
- EMF sensor (e.g., AD8232, custom coil sensor)
- Operational amplifiers for signal conditioning
- Power supply (5V/3.3V)
- Additional components (see `hardware/` folder)

## 📦 Software Requirements

### Firmware (ESP32)
- PlatformIO or Arduino IDE
- ESP32 board support package

### AI Core (Python)
- Python 3.8+
- TensorFlow Lite
- NumPy, SciPy
- See `ai_core/requirements.txt`

### Dashboard (FastAPI)
- Python 3.8+
- FastAPI
- Uvicorn
- See `ui/requirements.txt`

## 🚀 Quick Start

### 1. Flash ESP32 Firmware
```bash
cd firmware
# Using PlatformIO
pio run --target upload
```

### 2. Set Up AI Core
```bash
cd ai_core
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### 3. Launch Dashboard
```bash
cd ui
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Access the dashboard at `http://localhost:8000`

## 📖 Documentation

Detailed documentation is available in the `docs/` folder:
- [Hardware Setup Guide](docs/hardware_setup.md)
- [Firmware Guide](docs/firmware_guide.md)
- [AI Model Training](docs/ai_training.md)
- [API Documentation](docs/api_reference.md)

## 🤖 AI Model

The system uses TensorFlow Lite for efficient edge inference:
- Real-time signal classification
- Anomaly pattern detection
- Low-latency processing
- Support for custom model training

## 🔌 API Endpoints

Key FastAPI endpoints:
- `GET /api/status` - System status
- `GET /api/sensors/data` - Latest sensor readings
- `POST /api/analyze` - Trigger analysis
- `WebSocket /ws/stream` - Real-time data streaming

## 🛠️ Development

### Testing
```bash
# Test AI core
cd ai_core
pytest tests/

# Test API
cd ui
pytest tests/
```

### Building Custom Models
See `docs/ai_training.md` for instructions on training custom TensorFlow Lite models.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

**Note**: This device is designed for environmental signal monitoring and anomaly detection. Ensure compliance with local regulations regarding electromagnetic monitoring equipment.
