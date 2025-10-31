# Flordevid AI Core

Python backend with TensorFlow Lite for real-time environmental signal classification and anomaly detection.

## Features

- **Real-time Processing**: Process sensor data streams from ESP32
- **TensorFlow Lite**: Efficient edge inference with quantized models
- **Feature Extraction**: Statistical and spectral feature computation
- **Anomaly Detection**: Multi-class classification (normal, spike, sustained, oscillating)
- **Signal Analysis**: SNR calculation, pattern detection, digital filtering

## Installation

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Train Model

Generate and train a TensorFlow Lite model:

```bash
python train_model.py
```

This creates `models/anomaly_model.tflite` with a trained classifier.

### Run AI Core

Process data from ESP32 via serial:

```bash
# Linux/Mac
python main.py --port /dev/ttyUSB0

# Windows
python main.py --port COM3

# Test mode (no serial connection)
python main.py
```

Optional arguments:
- `--port`: Serial port for ESP32 connection
- `--duration`: Run duration in seconds (default: infinite)
- `--model`: Path to TFLite model (default: models/anomaly_model.tflite)

### Example Output

```
Flordevid AI Core started
==================================================
Connected to /dev/ttyUSB0
✓ Normal operation | Audio: 0.125V | EMF: 0.543V

⚠️  ANOMALY DETECTED at 1234567890
   Confidence: 87.3%
   Class: spike
   Audio Peak: 1.523V
   EMF Average: 0.621V
```

## Architecture

### Data Flow

```
ESP32 Sensors → Serial/JSON → DataProcessor → Feature Extraction
                                                      ↓
                                            SignalAnalyzer
                                                      ↓
                                            AnomalyDetector (TFLite)
                                                      ↓
                                            Results/Alerts
```

### Modules

- **main.py**: Main entry point and orchestration
- **data_processor.py**: Feature extraction and preprocessing
- **signal_analyzer.py**: Signal analysis and pattern detection
- **anomaly_detector.py**: TensorFlow Lite inference
- **train_model.py**: Model training script

## Feature Engineering

The system extracts 10 features per sample:

1. **Instantaneous** (4 features):
   - Audio peak level
   - Audio RMS level
   - EMF average level
   - EMF peak level

2. **Temporal** (6 features, computed over last 5 samples):
   - Audio mean, std, max
   - EMF mean, std, max

## Model Architecture

Default model (trained by `train_model.py`):

```
Input Layer: 10 features
Dense(32) + ReLU + Dropout(0.2)
Dense(16) + ReLU
Dense(4) + Softmax
Output: 4 classes [normal, spike, sustained, oscillating]
```

Optimized to TensorFlow Lite with quantization for edge deployment.

## Classes

- **Normal**: Baseline environmental signals
- **Spike**: Sudden brief increase in signal levels
- **Sustained**: Prolonged elevated signal levels
- **Oscillating**: Rhythmic fluctuation pattern

## Customization

### Training with Real Data

Collect labeled data and modify `train_model.py`:

```python
# Load your data
X_train = np.load('your_features.npy')
y_train = np.load('your_labels.npy')

# Train
detector = AnomalyDetector()
model, history = detector.train_model(X_train, y_train, epochs=100)
detector.convert_to_tflite(model, 'models/custom_model.tflite')
```

### Adjusting Thresholds

Edit `signal_analyzer.py`:

```python
self.baseline_audio = 0.1  # Baseline audio level
self.baseline_emf = 0.5    # Baseline EMF level
self.threshold_multiplier = 3.0  # Anomaly threshold
```

### Adding New Features

Extend `data_processor.py`:

```python
def extract_features(self, sensor_data):
    # ... existing features ...
    
    # Add custom feature
    custom_feature = self.compute_custom_feature(sensor_data)
    features.append(custom_feature)
    
    return np.array(features)
```

## Testing

Run tests (if available):

```bash
pytest tests/
```

## Performance

- **Inference time**: < 5ms per sample on CPU
- **Memory footprint**: ~500KB (TFLite model)
- **Throughput**: 100+ samples/second

## Troubleshooting

### Model not found
Run `python train_model.py` to generate the model.

### Serial connection issues
- Check port name (`ls /dev/tty*` on Linux)
- Ensure ESP32 is connected and recognized
- Verify baud rate (115200)

### Import errors
```bash
pip install --upgrade tensorflow numpy scipy
```

## License

MIT License - See LICENSE file in root directory
