"""
Drunk Detector - Kivy Mobile App
A prototype sobriety testing app with face detection, audio analysis, and location services.
WARNING: Not medically validated. Educational use only.
"""

import cv2
import numpy as np
from threading import Thread
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.garden.camera import Camera
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
import matplotlib.pyplot as plt

# Permissions and services
from kivy.permissions import Permission, request_permissions
from plyer import gps

import json
from datetime import datetime

Window.size = (1080, 1920)

class DrunkDetectorApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = 'Drunk Detector'
        self.drunk_score = 0
        self.risk_level = 'LOW'
        self.is_testing = False
        self.location_data = None
        self.test_history = []
        
    def build(self):
        """Build the main UI"""
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title
        title = Label(
            text='Drunk Detector v0.2.0 (Kivy)',
            size_hint_y=0.1,
            font_size='24sp',
            bold=True
        )
        main_layout.add_widget(title)
        
        # Status panel
        status_layout = GridLayout(cols=2, size_hint_y=0.15, spacing=5)
        status_layout.add_widget(Label(text='Score:', bold=True))
        self.score_label = Label(text='0/100')
        status_layout.add_widget(self.score_label)
        
        status_layout.add_widget(Label(text='Risk Level:', bold=True))
        self.risk_label = Label(text='LOW', color=(0, 1, 0, 1))
        status_layout.add_widget(self.risk_label)
        
        main_layout.add_widget(status_layout)
        
        # Camera placeholder
        self.camera_label = Label(
            text='Camera Feed',
            size_hint_y=0.4,
            canvas_size=(480, 640)
        )
        main_layout.add_widget(self.camera_label)
        
        # Control buttons
        button_layout = GridLayout(cols=2, size_hint_y=0.15, spacing=5)
        
        start_btn = Button(text='Start Analysis', size_hint_x=0.5)
        start_btn.bind(on_press=self.start_analysis)
        button_layout.add_widget(start_btn)
        
        stop_btn = Button(text='Stop Analysis', size_hint_x=0.5)
        stop_btn.bind(on_press=self.stop_analysis)
        button_layout.add_widget(stop_btn)
        
        location_btn = Button(text='Get Location', size_hint_x=0.5)
        location_btn.bind(on_press=self.get_location)
        button_layout.add_widget(location_btn)
        
        history_btn = Button(text='View History', size_hint_x=0.5)
        history_btn.bind(on_press=self.show_history)
        button_layout.add_widget(history_btn)
        
        main_layout.add_widget(button_layout)
        
        # Alert text
        self.alert_label = Label(
            text='Ready to test',
            size_hint_y=0.1,
            color=(0, 0, 0, 1)
        )
        main_layout.add_widget(self.alert_label)
        
        # Request permissions
        self.request_permissions()
        
        return main_layout
    
    def request_permissions(self):
        """Request camera and location permissions"""
        request_permissions([
            Permission.CAMERA,
            Permission.ACCESS_FINE_LOCATION,
            Permission.RECORD_AUDIO
        ])
    
    def start_analysis(self, instance):
        """Start face detection and audio analysis"""
        self.is_testing = True
        self.alert_label.text = 'Analysis started... Look at camera and speak clearly'
        
        # Start camera analysis in background thread
        analysis_thread = Thread(target=self.run_analysis_loop, daemon=True)
        analysis_thread.start()
    
    def stop_analysis(self, instance):
        """Stop analysis and save result"""
        self.is_testing = False
        self.alert_label.text = f'Test complete. Score: {self.drunk_score}/100, Risk: {self.risk_level}'
        
        # Save to history
        self.test_history.append({
            'timestamp': datetime.now().isoformat(),
            'score': self.drunk_score,
            'risk_level': self.risk_level,
            'location': self.location_data
        })
    
    def run_analysis_loop(self):
        """Main analysis loop: face detection + audio (simulated)"""
        cap = cv2.VideoCapture(0)
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        eye_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_eye.xml'
        )
        
        frame_count = 0
        eye_closure_scores = []
        head_rotation_scores = []
        
        while self.is_testing:
            ret, frame = cap.read()
            if not ret:
                break
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            
            for (x, y, w, h) in faces:
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]
                
                # Detect eyes
                eyes = eye_cascade.detectMultiScale(roi_gray)
                eye_closure = 1.0 - (len(eyes) / 2.0) if len(eyes) < 2 else 0.0
                eye_closure_scores.append(eye_closure)
                
                # Head rotation (simple check: face center offset)
                face_center_x = x + w // 2
                frame_center_x = frame.shape[1] // 2
                rotation_offset = abs(face_center_x - frame_center_x) / frame_center_x
                head_rotation_scores.append(min(rotation_offset, 1.0))
            
            frame_count += 1
            
            # Update score every 5 frames
            if frame_count % 5 == 0 and eye_closure_scores:
                avg_eye_closure = np.mean(eye_closure_scores[-5:])
                avg_head_rotation = np.mean(head_rotation_scores[-5:])
                
                # Scoring algorithm (0-100)
                eye_score = avg_eye_closure * 30
                rotation_score = avg_head_rotation * 15
                audio_score = np.random.uniform(0, 20)  # Simulated audio RMS
                
                self.drunk_score = int(eye_score + rotation_score + audio_score)
                self.risk_level = 'HIGH' if self.drunk_score > 60 else 'LOW'
                
                # Update UI
                Clock.schedule_once(lambda dt: self.update_ui(), 0)
        
        cap.release()
    
    def update_ui(self):
        """Update UI with current score and risk level"""
        self.score_label.text = f'{self.drunk_score}/100'
        
        if self.risk_level == 'HIGH':
            self.risk_label.text = 'HIGH'
            self.risk_label.color = (1, 0, 0, 1)  # Red
        else:
            self.risk_label.text = 'LOW'
            self.risk_label.color = (0, 1, 0, 1)  # Green
    
    def get_location(self, instance):
        """Get current GPS location"""
        try:
            gps.start(1000, 10)
            # In production, use proper gps listener
            self.location_data = {'lat': 37.7749, 'lon': -122.4194}  # Mock data
            self.alert_label.text = f'Location: {self.location_data}'
        except Exception as e:
            self.alert_label.text = f'Location error: {str(e)}'
    
    def show_history(self, instance):
        """Display test history"""
        if not self.test_history:
            self.alert_label.text = 'No test history yet'
            return
        
        history_text = 'Test History:\n'
        for entry in self.test_history[-5:]:  # Last 5 tests
            history_text += f"Time: {entry['timestamp']}, Score: {entry['score']}, Risk: {entry['risk_level']}\n"
        
        self.alert_label.text = history_text

if __name__ == '__main__':
    DrunkDetectorApp().run()
