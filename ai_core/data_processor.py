"""
Data processing and feature extraction
"""

import numpy as np
from scipy import signal, stats

class DataProcessor:
    def __init__(self):
        self.history = []
        self.max_history = 100  # Keep last 100 readings
    
    def extract_features(self, sensor_data):
        """
        Extract features from sensor data for ML model
        
        Args:
            sensor_data: Dict with sensor readings
            
        Returns:
            numpy array of features
        """
        # Add to history
        self.history.append(sensor_data)
        if len(self.history) > self.max_history:
            self.history.pop(0)
        
        # Extract current values
        audio_peak = sensor_data.get('audio_peak', 0)
        audio_rms = sensor_data.get('audio_rms', 0)
        emf_avg = sensor_data.get('emf_avg', 0)
        emf_peak = sensor_data.get('emf_peak', 0)
        
        # Statistical features
        features = [
            audio_peak,
            audio_rms,
            emf_avg,
            emf_peak,
        ]
        
        # Add temporal features if we have history
        if len(self.history) > 5:
            recent = self.history[-5:]
            
            # Audio trends
            audio_peaks = [d.get('audio_peak', 0) for d in recent]
            features.extend([
                np.mean(audio_peaks),
                np.std(audio_peaks),
                np.max(audio_peaks),
            ])
            
            # EMF trends
            emf_avgs = [d.get('emf_avg', 0) for d in recent]
            features.extend([
                np.mean(emf_avgs),
                np.std(emf_avgs),
                np.max(emf_avgs),
            ])
        else:
            # Pad with zeros if not enough history
            features.extend([0, 0, 0, 0, 0, 0])
        
        return np.array(features, dtype=np.float32)
    
    def normalize_features(self, features):
        """Normalize features to 0-1 range"""
        # Simple min-max normalization
        # In production, use pre-calculated statistics from training data
        normalized = np.clip(features / 5.0, 0, 1)  # Assume max value ~5V
        return normalized
    
    def create_sequence(self, window_size=10):
        """
        Create sequence data for time-series models
        
        Args:
            window_size: Number of time steps
            
        Returns:
            numpy array of shape (window_size, n_features)
        """
        if len(self.history) < window_size:
            # Pad with zeros if not enough history
            padding = window_size - len(self.history)
            sequence = np.zeros((padding, 4))
            for item in self.history:
                row = np.array([
                    item.get('audio_peak', 0),
                    item.get('audio_rms', 0),
                    item.get('emf_avg', 0),
                    item.get('emf_peak', 0),
                ])
                sequence = np.vstack([sequence, row])
            return sequence[-window_size:]
        else:
            recent = self.history[-window_size:]
            sequence = []
            for item in recent:
                row = [
                    item.get('audio_peak', 0),
                    item.get('audio_rms', 0),
                    item.get('emf_avg', 0),
                    item.get('emf_peak', 0),
                ]
                sequence.append(row)
            return np.array(sequence, dtype=np.float32)
    
    def compute_spectral_features(self, data, sample_rate=8000):
        """
        Compute spectral features using FFT
        
        Args:
            data: Time-domain signal data
            sample_rate: Sampling rate in Hz
            
        Returns:
            Dict with spectral features
        """
        if len(data) < 2:
            return {
                'peak_frequency': 0,
                'spectral_centroid': 0,
                'spectral_bandwidth': 0,
            }
        
        # Compute FFT
        fft = np.fft.rfft(data)
        magnitude = np.abs(fft)
        freqs = np.fft.rfftfreq(len(data), 1/sample_rate)
        
        # Peak frequency
        peak_idx = np.argmax(magnitude)
        peak_frequency = freqs[peak_idx]
        
        # Spectral centroid
        spectral_centroid = np.sum(freqs * magnitude) / np.sum(magnitude)
        
        # Spectral bandwidth
        spectral_bandwidth = np.sqrt(
            np.sum(((freqs - spectral_centroid) ** 2) * magnitude) / np.sum(magnitude)
        )
        
        return {
            'peak_frequency': peak_frequency,
            'spectral_centroid': spectral_centroid,
            'spectral_bandwidth': spectral_bandwidth,
        }
