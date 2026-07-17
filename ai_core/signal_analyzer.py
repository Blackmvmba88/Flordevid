"""
Signal analysis and pattern recognition
"""

import numpy as np
from scipy import signal

class SignalAnalyzer:
    def __init__(self):
        self.baseline_audio = 0.1  # Baseline audio level
        self.baseline_emf = 0.5    # Baseline EMF level
        self.threshold_multiplier = 3.0  # Threshold for anomaly
    
    def analyze(self, sensor_data):
        """
        Analyze sensor data for patterns
        
        Args:
            sensor_data: Dict with sensor readings
            
        Returns:
            Dict with analysis results
        """
        audio_peak = sensor_data.get('audio_peak', 0)
        audio_rms = sensor_data.get('audio_rms', 0)
        emf_avg = sensor_data.get('emf_avg', 0)
        emf_peak = sensor_data.get('emf_peak', 0)
        
        # Check for spikes
        audio_spike = audio_peak > (self.baseline_audio * self.threshold_multiplier)
        emf_spike = emf_avg > (self.baseline_emf * self.threshold_multiplier)
        
        # Calculate signal-to-noise ratio (simplified)
        audio_snr = self.calculate_snr(audio_peak, self.baseline_audio)
        emf_snr = self.calculate_snr(emf_avg, self.baseline_emf)
        
        # Check for correlations
        correlation = self.check_correlation(audio_peak, emf_avg)
        
        analysis = {
            'audio': {
                'peak': audio_peak,
                'rms': audio_rms,
                'spike_detected': audio_spike,
                'snr_db': audio_snr,
            },
            'emf': {
                'average': emf_avg,
                'peak': emf_peak,
                'spike_detected': emf_spike,
                'snr_db': emf_snr,
            },
            'correlation': correlation,
            'any_spike': audio_spike or emf_spike,
        }
        
        return analysis
    
    def calculate_snr(self, signal_level, noise_level):
        """
        Calculate signal-to-noise ratio in dB
        
        Args:
            signal_level: Signal amplitude
            noise_level: Noise floor
            
        Returns:
            SNR in decibels
        """
        if noise_level == 0:
            return 0
        
        ratio = signal_level / noise_level
        if ratio <= 0:
            return 0
        
        return 20 * np.log10(ratio)
    
    def check_correlation(self, audio_level, emf_level):
        """
        Check if audio and EMF levels are correlated
        
        Args:
            audio_level: Audio signal level
            emf_level: EMF signal level
            
        Returns:
            Correlation indicator (0-1)
        """
        # Normalize both signals
        audio_norm = min(audio_level / 2.0, 1.0)
        emf_norm = min(emf_level / 2.0, 1.0)
        
        # Simple correlation: how close are they?
        diff = abs(audio_norm - emf_norm)
        correlation = 1.0 - diff
        
        return max(0, correlation)
    
    def detect_pattern(self, history, pattern_type='spike'):
        """
        Detect specific patterns in historical data
        
        Args:
            history: List of sensor readings
            pattern_type: Type of pattern to detect
            
        Returns:
            Bool indicating if pattern detected
        """
        if len(history) < 5:
            return False
        
        if pattern_type == 'spike':
            # Look for sudden increase
            recent = [d.get('audio_peak', 0) for d in history[-5:]]
            return recent[-1] > (np.mean(recent[:-1]) * 2)
        
        elif pattern_type == 'sustained':
            # Look for sustained high level
            recent = [d.get('emf_avg', 0) for d in history[-10:]]
            return all(v > self.baseline_emf * 1.5 for v in recent)
        
        elif pattern_type == 'oscillating':
            # Look for oscillating pattern
            recent = [d.get('audio_peak', 0) for d in history[-10:]]
            if len(recent) < 10:
                return False
            
            # Simple oscillation detection using zero crossings
            mean_val = np.mean(recent)
            centered = np.array(recent) - mean_val
            zero_crossings = np.sum(np.diff(np.sign(centered)) != 0)
            return zero_crossings > 4  # More than 4 crossings indicates oscillation
        
        return False
    
    def apply_filter(self, data, filter_type='lowpass', cutoff=1000, fs=8000):
        """
        Apply digital filter to data
        
        Args:
            data: Input signal
            filter_type: Filter type ('lowpass', 'highpass', 'bandpass')
            cutoff: Cutoff frequency
            fs: Sampling frequency
            
        Returns:
            Filtered signal
        """
        nyquist = fs / 2
        normalized_cutoff = cutoff / nyquist
        
        if filter_type == 'lowpass':
            b, a = signal.butter(4, normalized_cutoff, btype='low')
        elif filter_type == 'highpass':
            b, a = signal.butter(4, normalized_cutoff, btype='high')
        else:
            return data
        
        filtered = signal.filtfilt(b, a, data)
        return filtered
