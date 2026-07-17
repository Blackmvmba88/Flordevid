# AI Model Training Guide

Guide for training custom TensorFlow Lite models for anomaly detection in the Flordevid system.

## Table of Contents

1. [Overview](#overview)
2. [Data Collection](#data-collection)
3. [Training Process](#training-process)
4. [Model Evaluation](#model-evaluation)
5. [Deployment](#deployment)

## Overview

The Flordevid AI system uses TensorFlow Lite for efficient edge inference. This guide covers:
- Collecting training data from sensors
- Preprocessing and feature engineering
- Training neural network models
- Converting to TensorFlow Lite format
- Deploying to the system

## Prerequisites

```bash
cd ai_core
pip install -r requirements.txt
```

Required packages:
- TensorFlow 2.13+
- NumPy, Pandas, Scikit-learn
- Matplotlib (for visualization)

## Data Collection

### 1. Collect Raw Sensor Data

Run the data collection script:

```bash
# Connect ESP32 to computer
python collect_data.py --port /dev/ttyUSB0 --duration 3600 --output data/raw_data.csv
```

This saves sensor readings to CSV:
```csv
timestamp,audio_peak,audio_rms,emf_avg,emf_peak
1234567890.123,0.125,0.089,0.543,0.789
...
```

### 2. Label Your Data

Create labels for different classes:

```python
# label_data.py
import pandas as pd

df = pd.read_csv('data/raw_data.csv')

# Add label column
df['label'] = 0  # Default: normal

# Label anomalies manually or based on thresholds
df.loc[df['audio_peak'] > 1.0, 'label'] = 1  # Spike
df.loc[df['emf_avg'] > 2.0, 'label'] = 2      # Sustained
# ... etc

df.to_csv('data/labeled_data.csv', index=False)
```

Classes:
- 0: Normal
- 1: Spike (sudden increase)
- 2: Sustained (prolonged high level)
- 3: Oscillating (rhythmic pattern)

### 3. Data Collection Script

Create `collect_data.py`:

```python
import serial
import json
import csv
import time
import argparse

def collect_data(port, duration, output_file):
    """Collect sensor data to CSV file"""
    
    ser = serial.Serial(port, 115200, timeout=1)
    time.sleep(2)  # Wait for ESP32 to initialize
    
    start_time = time.time()
    
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'audio_peak', 'audio_rms', 
                        'emf_avg', 'emf_peak'])
        
        print(f"Collecting data for {duration} seconds...")
        
        while time.time() - start_time < duration:
            try:
                line = ser.readline().decode('utf-8').strip()
                if line:
                    data = json.loads(line)
                    writer.writerow([
                        data.get('timestamp', time.time()),
                        data.get('audio_peak', 0),
                        data.get('audio_rms', 0),
                        data.get('emf_avg', 0),
                        data.get('emf_peak', 0),
                    ])
                    
                    if int(time.time()) % 60 == 0:
                        print(f"Collected {int(time.time() - start_time)}s of data...")
            except:
                pass
    
    ser.close()
    print(f"Data collection complete. Saved to {output_file}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', required=True)
    parser.add_argument('--duration', type=int, default=3600)
    parser.add_argument('--output', default='data/raw_data.csv')
    args = parser.parse_args()
    
    collect_data(args.port, args.duration, args.output)
```

## Training Process

### 1. Prepare Training Data

```python
# prepare_dataset.py
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load labeled data
df = pd.read_csv('data/labeled_data.csv')

# Extract features
feature_cols = ['audio_peak', 'audio_rms', 'emf_avg', 'emf_peak']
X = df[feature_cols].values
y = df['label'].values

# Add temporal features
window_size = 5
X_temporal = []

for i in range(window_size, len(df)):
    window = df.iloc[i-window_size:i]
    
    features = [
        df.loc[i, 'audio_peak'],
        df.loc[i, 'audio_rms'],
        df.loc[i, 'emf_avg'],
        df.loc[i, 'emf_peak'],
        window['audio_peak'].mean(),
        window['audio_peak'].std(),
        window['audio_peak'].max(),
        window['emf_avg'].mean(),
        window['emf_avg'].std(),
        window['emf_avg'].max(),
    ]
    
    X_temporal.append(features)

X_temporal = np.array(X_temporal)
y_temporal = y[window_size:]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X_temporal, y_temporal, test_size=0.2, random_state=42, stratify=y_temporal
)

# Normalize features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Save processed data
np.save('data/X_train.npy', X_train)
np.save('data/X_test.npy', X_test)
np.save('data/y_train.npy', y_train)
np.save('data/y_test.npy', y_test)

print(f"Training set: {X_train.shape}")
print(f"Test set: {X_test.shape}")
print(f"Classes: {np.unique(y_train)}")
```

### 2. Train Model

Use the provided `train_model.py` or create custom training:

```python
import tensorflow as tf
import numpy as np

# Load data
X_train = np.load('data/X_train.npy')
y_train = np.load('data/y_train.npy')
X_test = np.load('data/X_test.npy')
y_test = np.load('data/y_test.npy')

# Build model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    tf.keras.layers.Dropout(0.3),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(4, activation='softmax')  # 4 classes
])

# Compile
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# Train
history = model.fit(
    X_train, y_train,
    epochs=100,
    batch_size=32,
    validation_split=0.2,
    callbacks=[
        tf.keras.callbacks.EarlyStopping(patience=10, restore_best_weights=True),
        tf.keras.callbacks.ReduceLROnPlateau(patience=5)
    ]
)

# Evaluate
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test accuracy: {accuracy:.2%}")

# Save model
model.save('models/anomaly_model.h5')
```

### 3. Convert to TensorFlow Lite

```python
import tensorflow as tf

# Load trained model
model = tf.keras.models.load_model('models/anomaly_model.h5')

# Convert to TFLite
converter = tf.lite.TFLiteConverter.from_keras_model(model)

# Optimization (optional)
converter.optimizations = [tf.lite.Optimize.DEFAULT]

# For quantization (smaller model, faster inference)
def representative_dataset():
    X_train = np.load('data/X_train.npy')
    for i in range(100):
        yield [X_train[i:i+1].astype(np.float32)]

converter.representative_dataset = representative_dataset
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
converter.inference_input_type = tf.uint8
converter.inference_output_type = tf.uint8

# Convert
tflite_model = converter.convert()

# Save
with open('models/anomaly_model.tflite', 'wb') as f:
    f.write(tflite_model)

print("TFLite model saved successfully")
```

## Model Evaluation

### 1. Test TFLite Model

```python
import tensorflow as tf
import numpy as np

# Load TFLite model
interpreter = tf.lite.Interpreter(model_path='models/anomaly_model.tflite')
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Load test data
X_test = np.load('data/X_test.npy')
y_test = np.load('data/y_test.npy')

# Test predictions
predictions = []
for i in range(len(X_test)):
    input_data = X_test[i:i+1].astype(np.float32)
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    output = interpreter.get_tensor(output_details[0]['index'])
    predictions.append(np.argmax(output[0]))

predictions = np.array(predictions)

# Calculate accuracy
accuracy = np.mean(predictions == y_test)
print(f"TFLite model accuracy: {accuracy:.2%}")

# Confusion matrix
from sklearn.metrics import confusion_matrix, classification_report

cm = confusion_matrix(y_test, predictions)
print("\nConfusion Matrix:")
print(cm)

print("\nClassification Report:")
print(classification_report(y_test, predictions, 
      target_names=['Normal', 'Spike', 'Sustained', 'Oscillating']))
```

### 2. Benchmark Performance

```python
import time

# Measure inference time
times = []
for i in range(100):
    start = time.time()
    interpreter.set_tensor(input_details[0]['index'], X_test[i:i+1].astype(np.float32))
    interpreter.invoke()
    times.append(time.time() - start)

print(f"Average inference time: {np.mean(times)*1000:.2f}ms")
print(f"Min: {np.min(times)*1000:.2f}ms, Max: {np.max(times)*1000:.2f}ms")

# Model size
import os
size = os.path.getsize('models/anomaly_model.tflite')
print(f"Model size: {size/1024:.2f} KB")
```

## Advanced Techniques

### 1. Data Augmentation

```python
def augment_data(X, y, noise_level=0.05):
    """Add noise for data augmentation"""
    X_aug = []
    y_aug = []
    
    for i in range(len(X)):
        # Original sample
        X_aug.append(X[i])
        y_aug.append(y[i])
        
        # Add noisy version
        noise = np.random.normal(0, noise_level, X[i].shape)
        X_aug.append(X[i] + noise)
        y_aug.append(y[i])
    
    return np.array(X_aug), np.array(y_aug)

X_train_aug, y_train_aug = augment_data(X_train, y_train)
```

### 2. Feature Selection

```python
from sklearn.feature_selection import SelectKBest, f_classif

# Select top K features
selector = SelectKBest(f_classif, k=8)
X_train_selected = selector.fit_transform(X_train, y_train)
X_test_selected = selector.transform(X_test)

print(f"Selected features: {selector.get_support()}")
```

### 3. Ensemble Methods

```python
# Train multiple models and average predictions
models = []
for i in range(5):
    model = build_model()
    model.fit(X_train, y_train, epochs=50, verbose=0)
    models.append(model)

# Ensemble prediction
predictions = np.mean([model.predict(X_test) for model in models], axis=0)
```

## Deployment

### 1. Deploy to AI Core

Replace the model file:

```bash
cp models/anomaly_model.tflite ../ai_core/models/
```

### 2. Test Integration

```bash
cd ../ai_core
python main.py --port /dev/ttyUSB0
```

### 3. Monitor Performance

Check for:
- Prediction accuracy
- False positive rate
- Inference latency
- Resource usage

## Continuous Improvement

### Retraining Pipeline

1. Collect new data regularly
2. Label new examples (especially misclassified ones)
3. Retrain model with expanded dataset
4. Evaluate performance
5. Deploy if improvement is significant

### Active Learning

```python
# Identify uncertain predictions
predictions = model.predict(X_unlabeled)
uncertainty = 1 - np.max(predictions, axis=1)

# Label most uncertain samples
top_uncertain = np.argsort(uncertainty)[-100:]
# Manually label these samples
# Add to training set
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Low accuracy | Collect more data, try different architecture |
| Overfitting | Add dropout, regularization, more data |
| Slow inference | Optimize model, quantize, reduce size |
| High false positives | Adjust decision thresholds, balance dataset |

## Best Practices

1. **Start Simple**: Begin with basic models, add complexity gradually
2. **Balance Data**: Ensure all classes are well-represented
3. **Validate Properly**: Use proper train/val/test splits
4. **Monitor Metrics**: Track multiple metrics, not just accuracy
5. **Version Control**: Keep track of model versions and performance
6. **Document**: Record hyperparameters, data sources, results

## Resources

- [TensorFlow Lite Guide](https://www.tensorflow.org/lite/guide)
- [Model Optimization](https://www.tensorflow.org/model_optimization)
- [Scikit-learn](https://scikit-learn.org/)

## License

MIT License - See LICENSE file in root directory
