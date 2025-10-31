"""
Anomaly detection using TensorFlow Lite
"""

import numpy as np
import tensorflow as tf

class AnomalyDetector:
    def __init__(self, model_path=None):
        """
        Initialize anomaly detector with TFLite model
        
        Args:
            model_path: Path to .tflite model file
        """
        self.model_path = model_path
        self.interpreter = None
        self.input_details = None
        self.output_details = None
        
        # Anomaly classes
        self.classes = ['normal', 'spike', 'sustained', 'oscillating']
        
        if model_path:
            self.load_model(model_path)
    
    def load_model(self, model_path):
        """Load TensorFlow Lite model"""
        try:
            self.interpreter = tf.lite.Interpreter(model_path=model_path)
            self.interpreter.allocate_tensors()
            
            self.input_details = self.interpreter.get_input_details()
            self.output_details = self.interpreter.get_output_details()
            
            print(f"TFLite model loaded from {model_path}")
            print(f"Input shape: {self.input_details[0]['shape']}")
            print(f"Output shape: {self.output_details[0]['shape']}")
        except Exception as e:
            print(f"Warning: Could not load model from {model_path}: {e}")
            print("Using rule-based detection instead")
            self.interpreter = None
    
    def predict(self, features):
        """
        Predict anomaly from features
        
        Args:
            features: Feature vector (numpy array)
            
        Returns:
            Dict with prediction results
        """
        if self.interpreter is None:
            # Fallback to rule-based detection
            return self._rule_based_detection(features)
        
        try:
            # Prepare input
            input_data = features.reshape(1, -1).astype(np.float32)
            
            # Ensure input shape matches model
            expected_shape = self.input_details[0]['shape']
            if input_data.shape[1] != expected_shape[1]:
                # Pad or truncate to match
                if input_data.shape[1] < expected_shape[1]:
                    padding = np.zeros((1, expected_shape[1] - input_data.shape[1]))
                    input_data = np.concatenate([input_data, padding], axis=1)
                else:
                    input_data = input_data[:, :expected_shape[1]]
            
            # Run inference
            self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
            self.interpreter.invoke()
            
            # Get output
            output = self.interpreter.get_tensor(self.output_details[0]['index'])
            
            # Process output
            if output.shape[-1] == len(self.classes):
                # Multi-class classification
                class_idx = np.argmax(output[0])
                confidence = output[0][class_idx]
                class_name = self.classes[class_idx]
                is_anomaly = class_idx > 0  # Any non-normal class
            else:
                # Binary classification
                confidence = output[0][0]
                is_anomaly = confidence > 0.5
                class_name = 'anomaly' if is_anomaly else 'normal'
            
            return {
                'is_anomaly': bool(is_anomaly),
                'confidence': float(confidence),
                'class': class_name,
                'probabilities': output[0].tolist(),
            }
            
        except Exception as e:
            print(f"Error during inference: {e}")
            return self._rule_based_detection(features)
    
    def _rule_based_detection(self, features):
        """
        Fallback rule-based anomaly detection
        
        Args:
            features: Feature vector
            
        Returns:
            Dict with detection results
        """
        # Extract key features
        if len(features) < 4:
            return {
                'is_anomaly': False,
                'confidence': 0.0,
                'class': 'normal',
                'probabilities': [1.0, 0.0, 0.0, 0.0],
            }
        
        audio_peak = features[0]
        audio_rms = features[1]
        emf_avg = features[2]
        emf_peak = features[3]
        
        # Define thresholds
        audio_threshold = 1.0
        emf_threshold = 2.0
        
        # Check for anomalies
        is_anomaly = False
        class_name = 'normal'
        confidence = 0.0
        
        if audio_peak > audio_threshold or emf_avg > emf_threshold:
            is_anomaly = True
            
            # Determine type
            if audio_peak > audio_threshold and emf_avg > emf_threshold:
                class_name = 'sustained'
                confidence = 0.8
            elif audio_peak > audio_threshold * 1.5:
                class_name = 'spike'
                confidence = 0.7
            else:
                class_name = 'anomaly'
                confidence = 0.6
        
        # Calculate probabilities (simplified)
        probs = [0.9, 0.05, 0.03, 0.02]  # Default to normal
        if is_anomaly:
            class_idx = self.classes.index(class_name) if class_name in self.classes else 1
            probs = [0.0] * len(self.classes)
            probs[class_idx] = confidence
            probs[0] = 1.0 - confidence
        
        return {
            'is_anomaly': is_anomaly,
            'confidence': confidence,
            'class': class_name,
            'probabilities': probs,
        }
    
    def train_model(self, X_train, y_train, epochs=50):
        """
        Train a simple model (for demonstration)
        This would typically be done offline
        
        Args:
            X_train: Training features
            y_train: Training labels
            epochs: Number of training epochs
        """
        print("Training model...")
        
        # Create a simple neural network
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(32, activation='relu', input_shape=(X_train.shape[1],)),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(16, activation='relu'),
            tf.keras.layers.Dense(len(self.classes), activation='softmax')
        ])
        
        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        # Train
        history = model.fit(
            X_train, y_train,
            epochs=epochs,
            batch_size=32,
            validation_split=0.2,
            verbose=1
        )
        
        return model, history
    
    def convert_to_tflite(self, model, output_path):
        """
        Convert Keras model to TensorFlow Lite
        
        Args:
            model: Keras model
            output_path: Path to save .tflite file
        """
        converter = tf.lite.TFLiteConverter.from_keras_model(model)
        converter.optimizations = [tf.lite.Optimize.DEFAULT]
        tflite_model = converter.convert()
        
        with open(output_path, 'wb') as f:
            f.write(tflite_model)
        
        print(f"TFLite model saved to {output_path}")
