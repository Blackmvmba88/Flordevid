"""
Training script for anomaly detection model
"""

import numpy as np
from pathlib import Path
from anomaly_detector import AnomalyDetector

def generate_synthetic_data(n_samples=1000):
    """
    Generate synthetic training data
    
    Returns:
        X: Features array
        y: Labels array
    """
    np.random.seed(42)
    
    X = []
    y = []
    
    # Class 0: Normal
    for _ in range(n_samples // 2):
        audio_peak = np.random.normal(0.1, 0.05)
        audio_rms = audio_peak * 0.7
        emf_avg = np.random.normal(0.5, 0.1)
        emf_peak = emf_avg * 1.2
        
        features = [
            audio_peak, audio_rms, emf_avg, emf_peak,
            audio_peak, 0.02, audio_peak,  # Audio stats
            emf_avg, 0.05, emf_avg,  # EMF stats
        ]
        X.append(features)
        y.append(0)
    
    # Class 1: Spike
    for _ in range(n_samples // 6):
        audio_peak = np.random.normal(1.5, 0.3)
        audio_rms = audio_peak * 0.6
        emf_avg = np.random.normal(0.6, 0.15)
        emf_peak = emf_avg * 1.5
        
        features = [
            audio_peak, audio_rms, emf_avg, emf_peak,
            audio_peak * 0.8, 0.3, audio_peak,
            emf_avg, 0.1, emf_peak,
        ]
        X.append(features)
        y.append(1)
    
    # Class 2: Sustained
    for _ in range(n_samples // 6):
        audio_peak = np.random.normal(0.8, 0.2)
        audio_rms = audio_peak * 0.8
        emf_avg = np.random.normal(2.5, 0.4)
        emf_peak = emf_avg * 1.1
        
        features = [
            audio_peak, audio_rms, emf_avg, emf_peak,
            audio_peak, 0.1, audio_peak,
            emf_avg, 0.2, emf_peak,
        ]
        X.append(features)
        y.append(2)
    
    # Class 3: Oscillating
    for _ in range(n_samples // 6):
        audio_peak = np.random.normal(0.6, 0.2)
        audio_rms = audio_peak * 0.5
        emf_avg = np.random.normal(1.2, 0.3)
        emf_peak = emf_avg * 1.8
        
        features = [
            audio_peak, audio_rms, emf_avg, emf_peak,
            audio_peak * 0.7, 0.25, audio_peak * 1.3,
            emf_avg * 0.8, 0.4, emf_peak,
        ]
        X.append(features)
        y.append(3)
    
    X = np.array(X, dtype=np.float32)
    y = np.array(y, dtype=np.int32)
    
    # Shuffle
    indices = np.random.permutation(len(X))
    X = X[indices]
    y = y[indices]
    
    return X, y


def main():
    """Train and save the model"""
    print("Generating synthetic training data...")
    X_train, y_train = generate_synthetic_data(n_samples=2000)
    
    print(f"Training set: {X_train.shape[0]} samples, {X_train.shape[1]} features")
    print(f"Classes: {np.unique(y_train)}")
    
    # Create detector
    detector = AnomalyDetector()
    
    # Train model
    model, history = detector.train_model(X_train, y_train, epochs=50)
    
    # Evaluate
    print("\nEvaluating model...")
    X_test, y_test = generate_synthetic_data(n_samples=200)
    loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
    print(f"Test accuracy: {accuracy:.2%}")
    
    # Convert to TFLite
    output_path = Path(__file__).parent / 'models' / 'anomaly_model.tflite'
    output_path.parent.mkdir(exist_ok=True)
    
    print(f"\nConverting to TensorFlow Lite...")
    detector.convert_to_tflite(model, str(output_path))
    
    print("\n✓ Training complete!")
    print(f"Model saved to: {output_path}")


if __name__ == '__main__':
    main()
