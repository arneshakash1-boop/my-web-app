"""
Location Handler Module
Retrieves GPS coordinates for emergency alerts
"""

from plyer import gps
from threading import Thread
import time

class LocationHandler:
    def __init__(self, callback=None):
        """
        Initialize location handler
        
        Args:
            callback: Function to call with location updates
        """
        self.callback = callback
        self.is_tracking = False
        self.location_data = None
        self.location_thread = None
    
    def get_location_once(self, timeout=10):
        """
        Get current GPS location (blocking)
        
        Args:
            timeout: Timeout in seconds
            
        Returns:
            dict with latitude, longitude, accuracy
        """
        location_result = {}
        
        def on_location(**kwargs):
            location_result.update(kwargs)
        
        try:
            gps.configure(on_location=on_location)
            gps.start(minTime=1000, minDistance=0)
            
            # Wait for location fix
            start_time = time.time()
            while not location_result and (time.time() - start_time) < timeout:
                time.sleep(0.1)
            
            gps.stop()
        except Exception as e:
            print(f"GPS Error: {e}")
            return None
        
        if location_result:
            self.location_data = {
                'latitude': location_result.get('lat'),
                'longitude': location_result.get('lon'),
                'accuracy': location_result.get('accuracy'),
                'altitude': location_result.get('altitude'),
                'timestamp': time.time()
            }
            return self.location_data
        
        return None
    
    def start_tracking(self, update_interval=5000):
        """
        Start continuous GPS tracking
        
        Args:
            update_interval: Update interval in milliseconds
        """
        self.is_tracking = True
        self.location_thread = Thread(
            target=self._tracking_loop,
            args=(update_interval,),
            daemon=True
        )
        self.location_thread.start()
    
    def stop_tracking(self):
        """Stop GPS tracking"""
        self.is_tracking = False
        if self.location_thread:
            self.location_thread.join(timeout=5)
        
        try:
            gps.stop()
        except:
            pass
    
    def _tracking_loop(self, update_interval):
        """Internal loop for continuous tracking"""
        def on_location(**kwargs):
            self.location_data = {
                'latitude': kwargs.get('lat'),
                'longitude': kwargs.get('lon'),
                'accuracy': kwargs.get('accuracy'),
                'altitude': kwargs.get('altitude'),
                'timestamp': time.time()
            }
            
            if self.callback:
                self.callback(self.location_data)
        
        try:
            gps.configure(on_location=on_location)
            gps.start(minTime=update_interval, minDistance=0)
            
            while self.is_tracking:
                time.sleep(1)
        
        except Exception as e:
            print(f"GPS Tracking Error: {e}")
        
        finally:
            try:
                gps.stop()
            except:
                pass
    
    def format_location_url(self):
        """
        Format location as Google Maps URL
        
        Returns:
            str: Google Maps URL with coordinates
        """
        if not self.location_data:
            return None
        
        lat = self.location_data['latitude']
        lon = self.location_data['longitude']
        return f"https://maps.google.com/?q={lat},{lon}"
    
    def get_location_dict(self):
        """Get current location data"""
        return self.location_data

if __name__ == '__main__':
    # Test location handler
    handler = LocationHandler()
    
    print("Getting GPS location (this may take a few seconds)...")
    location = handler.get_location_once(timeout=15)
    
    if location:
        print(f"\nLocation found:")
        print(f"  Latitude: {location['latitude']}")
        print(f"  Longitude: {location['longitude']}")
        print(f"  Accuracy: {location['accuracy']} meters")
        print(f"  Maps URL: {handler.format_location_url()}")
    else:
        print("Could not get GPS location. Check permissions and signal.")
