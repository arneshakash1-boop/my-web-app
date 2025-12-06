"""
Audio Analysis Module for Drunk Detector
Captures audio from microphone and computes RMS energy for impairment detection
"""

import numpy as np
import sounddevice as sd
from scipy import signal
import threading

class AudioAnalyzer:
    def __init__(self, sample_rate=16000, chunk_duration=1.0):
        """
        Initialize audio analyzer
        
        Args:
            sample_rate: Audio sampling rate (Hz)
            chunk_duration: Duration of each audio chunk for analysis (seconds)
        """
        self.sample_rate = sample_rate
        self.chunk_size = int(sample_rate * chunk_duration)
        self.is_recording = False
        self.baseline_rms = None
        self.current_audio_data = None
        self.audio_thread = None
    
    def calculate_rms(self, audio_data):
        """Calculate RMS (Root Mean Square) energy of audio"""
        if len(audio_data) == 0:
            return 0
        return np.sqrt(np.mean(audio_data ** 2))
    
    def record_baseline(self, duration=5):
        """
        Record baseline audio for 'sober' state
        
        Args:
            duration: Recording duration in seconds
        """
        print(f"Recording baseline audio for {duration} seconds...")
        audio_data = sd.rec(int(duration * self.sample_rate), samplerate=self.sample_rate, channels=1)
        sd.wait()
        
        self.baseline_rms = self.calculate_rms(audio_data.flatten())
        print(f"Baseline RMS: {self.baseline_rms:.4f}")
        return self.baseline_rms
    
    def analyze_audio(self, duration=3):
        """
        Record and analyze test audio
        
        Args:
            duration: Recording duration in seconds
            
        Returns:
            dict with analysis results
        """
        print(f"Recording test audio for {duration} seconds...")
        audio_data = sd.rec(int(duration * self.sample_rate), samplerate=self.sample_rate, channels=1)
        sd.wait()
        
        audio_flat = audio_data.flatten()
        self.current_audio_data = audio_flat
        
        # Calculate RMS
        rms = self.calculate_rms(audio_flat)
        
        # Calculate RMS deviation from baseline
        rms_deviation = 0
        if self.baseline_rms is not None:
            rms_deviation = abs(rms - self.baseline_rms) / (self.baseline_rms + 1e-6)
        
        # Calculate spectral features
        freqs, psd = signal.welch(audio_flat, self.sample_rate)
        spectral_centroid = np.sum(freqs * psd) / np.sum(psd)
        
        # Detect speech patterns (simple zero-crossing rate)
        zero_crossings = np.sum(np.abs(np.diff(np.sign(audio_flat)))) / (2 * len(audio_flat))
        
        # Score audio impairment (0-20 points)
        audio_score = min(20, rms_deviation * 10)
        
        return {
            'rms': float(rms),
            'rms_deviation': float(rms_deviation),
            'spectral_centroid': float(spectral_centroid),
            'zero_crossing_rate': float(zero_crossings),
            'audio_score': float(audio_score),
            'duration': duration
        }
    
    def start_continuous_recording(self, callback=None):
        """
        Start continuous audio monitoring in background thread
        
        Args:
            callback: Function to call with audio analysis results
        """
        self.is_recording = True
        self.audio_thread = threading.Thread(
            target=self._continuous_recording_loop,
            args=(callback,),
            daemon=True
        )
        self.audio_thread.start()
    
    def stop_continuous_recording(self):
        """Stop continuous recording"""
        self.is_recording = False
        if self.audio_thread:
            self.audio_thread.join(timeout=2)
    
    def _continuous_recording_loop(self, callback):
        """Internal loop for continuous recording"""
        while self.is_recording:
            result = self.analyze_audio(duration=1)
            if callback:
                callback(result)

if __name__ == '__main__':
    # Test audio analyzer
    analyzer = AudioAnalyzer()
    analyzer.record_baseline(duration=3)
    
    import time
    time.sleep(1)
    
    result = analyzer.analyze_audio(duration=3)
    print("\nAudio Analysis Result:")
    for key, value in result.items():
        print(f"  {key}: {value}")
