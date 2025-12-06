"""
Data Store Module
Local storage for test history and settings
"""

import json
import os
from datetime import datetime
from pathlib import Path

class DataStore:
    def __init__(self, data_dir='~/.drunkdetector'):
        """
        Initialize data store
        
        Args:
            data_dir: Directory for storing local data
        """
        self.data_dir = Path(data_dir).expanduser()
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.history_file = self.data_dir / 'test_history.json'
        self.settings_file = self.data_dir / 'settings.json'
        self.baseline_file = self.data_dir / 'audio_baseline.json'
    
    def save_test_result(self, score, risk_level, location=None, audio_data=None, face_data=None):
        """
        Save a test result to history
        
        Args:
            score: Drunk score (0-100)
            risk_level: 'LOW' or 'HIGH'
            location: GPS location data
            audio_data: Audio analysis results
            face_data: Face detection results
        """
        test_entry = {
            'timestamp': datetime.now().isoformat(),
            'score': score,
            'risk_level': risk_level,
            'location': location,
            'audio_data': audio_data,
            'face_data': face_data
        }
        
        history = self.load_test_history()
        history.append(test_entry)
        
        with open(self.history_file, 'w') as f:
            json.dump(history, f, indent=2)
        
        return test_entry
    
    def load_test_history(self, limit=None):
        """
        Load test history
        
        Args:
            limit: Maximum number of recent tests to load
            
        Returns:
            list of test results
        """
        if not self.history_file.exists():
            return []
        
        with open(self.history_file, 'r') as f:
            history = json.load(f)
        
        if limit:
            history = history[-limit:]
        
        return history
    
    def get_statistics(self):
        """
        Calculate statistics from test history
        
        Returns:
            dict with aggregate statistics
        """
        history = self.load_test_history()
        
        if not history:
            return None
        
        scores = [t['score'] for t in history]
        high_risk_count = sum(1 for t in history if t['risk_level'] == 'HIGH')
        
        stats = {
            'total_tests': len(history),
            'average_score': sum(scores) / len(scores),
            'min_score': min(scores),
            'max_score': max(scores),
            'high_risk_count': high_risk_count,
            'high_risk_percentage': (high_risk_count / len(history)) * 100 if history else 0,
            'first_test': history[0]['timestamp'] if history else None,
            'last_test': history[-1]['timestamp'] if history else None
        }
        
        return stats
    
    def save_audio_baseline(self, baseline_rms, timestamp=None):
        """
        Save audio baseline for sober state
        
        Args:
            baseline_rms: RMS value from baseline recording
            timestamp: Recording timestamp
        """
        baseline_data = {
            'baseline_rms': baseline_rms,
            'timestamp': timestamp or datetime.now().isoformat()
        }
        
        with open(self.baseline_file, 'w') as f:
            json.dump(baseline_data, f, indent=2)
    
    def load_audio_baseline(self):
        """
        Load saved audio baseline
        
        Returns:
            dict with baseline data or None
        """
        if not self.baseline_file.exists():
            return None
        
        with open(self.baseline_file, 'r') as f:
            return json.load(f)
    
    def save_settings(self, settings):
        """
        Save app settings
        
        Args:
            settings: dict of settings
        """
        with open(self.settings_file, 'w') as f:
            json.dump(settings, f, indent=2)
    
    def load_settings(self):
        """
        Load app settings
        
        Returns:
            dict of settings or empty dict
        """
        if not self.settings_file.exists():
            return {}
        
        with open(self.settings_file, 'r') as f:
            return json.load(f)
    
    def clear_history(self):
        """Delete all test history"""
        if self.history_file.exists():
            self.history_file.unlink()
    
    def export_history_csv(self, output_file='test_history.csv'):
        """
        Export history to CSV for analysis
        
        Args:
            output_file: Output CSV file path
        """
        import csv
        
        history = self.load_test_history()
        
        if not history:
            print("No test history to export")
            return
        
        with open(output_file, 'w', newline='') as f:
            writer = csv.DictWriter(
                f,
                fieldnames=['timestamp', 'score', 'risk_level', 'latitude', 'longitude']
            )
            writer.writeheader()
            
            for test in history:
                row = {
                    'timestamp': test['timestamp'],
                    'score': test['score'],
                    'risk_level': test['risk_level'],
                    'latitude': test.get('location', {}).get('latitude', ''),
                    'longitude': test.get('location', {}).get('longitude', '')
                }
                writer.writerow(row)
        
        print(f"History exported to {output_file}")

if __name__ == '__main__':
    # Test data store
    store = DataStore()
    
    # Save some test results
    store.save_test_result(45, 'LOW', location={'latitude': 37.7749, 'longitude': -122.4194})
    store.save_test_result(75, 'HIGH', location={'latitude': 37.7750, 'longitude': -122.4195})
    
    # Load and display history
    history = store.load_test_history()
    print(f"Saved {len(history)} test(s)")
    
    # Display statistics
    stats = store.get_statistics()
    print("\nStatistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
