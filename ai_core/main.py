"""
Flordevid AI Core - Main Entry Point
Real-time signal processing and anomaly detection
"""

import sys
import json
import time
import serial
import numpy as np
from pathlib import Path
from data_processor import DataProcessor
from anomaly_detector import AnomalyDetector
from signal_analyzer import SignalAnalyzer

class FlordovidAICore:
    def __init__(self, serial_port=None, model_path='models/anomaly_model.tflite'):
        """
        Initialize AI Core system
        
        Args:
            serial_port: Serial port for ESP32 connection (e.g., '/dev/ttyUSB0' or 'COM3')
            model_path: Path to TensorFlow Lite model
        """
        self.serial_port = serial_port
        self.serial_conn = None
        self.data_processor = DataProcessor()
        self.signal_analyzer = SignalAnalyzer()
        
        # Initialize anomaly detector with TFLite model
        model_file = Path(__file__).parent / model_path
        self.anomaly_detector = AnomalyDetector(str(model_file))
        
        self.running = False
        
    def connect_serial(self):
        """Connect to ESP32 via serial port"""
        if not self.serial_port:
            print("No serial port specified. Running in test mode.")
            return False
            
        try:
            self.serial_conn = serial.Serial(
                self.serial_port, 
                115200, 
                timeout=1
            )
            print(f"Connected to {self.serial_port}")
            # Wait for ESP32 to initialize
            time.sleep(2)
            return True
        except Exception as e:
            print(f"Failed to connect to serial port: {e}")
            return False
    
    def read_sensor_data(self):
        """Read and parse sensor data from serial"""
        if not self.serial_conn or not self.serial_conn.is_open:
            return None
            
        try:
            line = self.serial_conn.readline().decode('utf-8').strip()
            if line:
                data = json.loads(line)
                return data
        except json.JSONDecodeError:
            # Skip non-JSON lines (debug messages, etc.)
            pass
        except Exception as e:
            print(f"Error reading sensor data: {e}")
        
        return None
    
    def process_data(self, sensor_data):
        """
        Process sensor data through the analysis pipeline
        
        Args:
            sensor_data: Dict with sensor readings
            
        Returns:
            Dict with analysis results
        """
        if not sensor_data:
            return None
        
        # Extract features
        features = self.data_processor.extract_features(sensor_data)
        
        # Analyze signal characteristics
        signal_analysis = self.signal_analyzer.analyze(sensor_data)
        
        # Run anomaly detection
        anomaly_result = self.anomaly_detector.predict(features)
        
        # Combine results
        result = {
            'timestamp': sensor_data.get('timestamp', time.time()),
            'features': features,
            'signal_analysis': signal_analysis,
            'anomaly': anomaly_result,
            'raw_data': sensor_data
        }
        
        return result
    
    def run(self, duration=None):
        """
        Run the AI core processing loop
        
        Args:
            duration: Optional duration in seconds (None for infinite)
        """
        self.running = True
        start_time = time.time()
        
        print("Flordevid AI Core started")
        print("=" * 50)
        
        if self.serial_port:
            if not self.connect_serial():
                print("Failed to connect to device. Exiting.")
                return
        
        try:
            while self.running:
                # Check duration
                if duration and (time.time() - start_time) > duration:
                    break
                
                # Read sensor data
                sensor_data = self.read_sensor_data()
                
                if sensor_data:
                    # Process data
                    result = self.process_data(sensor_data)
                    
                    if result:
                        # Display results
                        self.display_results(result)
                
                time.sleep(0.1)  # Small delay
                
        except KeyboardInterrupt:
            print("\nStopping AI Core...")
        finally:
            self.cleanup()
    
    def display_results(self, result):
        """Display analysis results"""
        anomaly = result['anomaly']
        
        if anomaly['is_anomaly']:
            print(f"\n⚠️  ANOMALY DETECTED at {result['timestamp']}")
            print(f"   Confidence: {anomaly['confidence']:.2%}")
            print(f"   Class: {anomaly['class']}")
            print(f"   Audio Peak: {result['raw_data'].get('audio_peak', 0):.3f}V")
            print(f"   EMF Average: {result['raw_data'].get('emf_avg', 0):.3f}V")
        else:
            # Periodic normal status (every 10 seconds)
            if int(time.time()) % 10 == 0:
                print(f"✓ Normal operation | Audio: {result['raw_data'].get('audio_peak', 0):.3f}V | EMF: {result['raw_data'].get('emf_avg', 0):.3f}V")
    
    def cleanup(self):
        """Cleanup resources"""
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
        print("AI Core stopped")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Flordevid AI Core')
    parser.add_argument('--port', type=str, help='Serial port (e.g., /dev/ttyUSB0 or COM3)')
    parser.add_argument('--duration', type=int, help='Run duration in seconds (default: infinite)')
    parser.add_argument('--model', type=str, default='models/anomaly_model.tflite',
                       help='Path to TFLite model')
    
    args = parser.parse_args()
    
    # Create and run AI core
    ai_core = FlordovidAICore(
        serial_port=args.port,
        model_path=args.model
    )
    ai_core.run(duration=args.duration)


if __name__ == '__main__':
    main()
