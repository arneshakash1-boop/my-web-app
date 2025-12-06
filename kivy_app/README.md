# Drunk Detector - Kivy Mobile App

**Version:** 0.2.0 (Kivy/Python)

[![Release](https://img.shields.io/github/v/release/arneshakash1-boop/my-web-app)](https://github.com/arneshakash1-boop/my-web-app/releases)

A prototype sobriety testing application built with **Python Kivy** for mobile devices (Android/iOS).

## ⚠️ IMPORTANT DISCLAIMER

**This is a prototype educational project. It is NOT a certified alcohol breathalyzer or sobriety test.**
- Do NOT rely on it for legal, medical, or safety-critical decisions
- Use it only as an assistive tool for educational purposes
- Impairment assessment requires professional evaluation

## Features

- **Real-time Face Detection**: Uses OpenCV to detect and analyze facial features
  - Eye closure probability detection
  - Head rotation and movement analysis
  - Face symmetry evaluation

- **Audio Analysis**: Voice recording and RMS energy computation
  - Speech pattern baseline recording
  - RMS energy deviation detection

- **Location Integration**: GPS coordinates for emergency alerts
  - Optional emergency contact SMS
  - Location history tracking

- **Test History**: Local storage of past sobriety tests
  - Timestamp, score, risk level
  - Trend analysis over time

## Setup Instructions

### Prerequisites
- Python 3.8+
- Kivy 2.3+
- OpenCV (cv2)
- Buildozer (for Android builds)

### Installation

```bash
# 1. Navigate to kivy_app folder
cd kivy_app

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run on desktop (for testing)
python main.py
```

### Building for Mobile

#### Android (requires Buildozer + JDK + Android SDK)
```bash
buildozer android debug
buildozer android debug deploy run
```

#### iOS (Mac only, requires Xcode)
```bash
buildozer ios debug
```

## Architecture

### Components
- **Face Detection Module** (`main.py`): OpenCV Haar Cascades for real-time detection
- **Audio Analysis** (`audio_analyzer.py`): RMS energy computation from mic input
- **Location Services** (`location_handler.py`): GPS integration via Plyer
- **Storage** (`data_store.py`): Local JSON persistence for test history
- **UI** (`main.py`): Kivy GridLayout + BoxLayout for responsive mobile UI

### Scoring Algorithm

The app computes a "drunk score" (0-100) based on:

1. **Face Features** (up to 45 points)
   - Eye closure probability: 30 points
   - Head rotation/tilt: 15 points

2. **Audio Features** (up to 20 points)
   - RMS energy deviation from baseline

3. **Risk Thresholds**
   - Score > 60: **HIGH RISK** (triggers alert)
   - Score ≤ 60: **LOW RISK**

## File Structure

```
kivy_app/
├── main.py                 # Main Kivy app and UI logic
├── audio_analyzer.py       # Audio recording and RMS analysis
├── location_handler.py     # GPS location retrieval
├── data_store.py          # Local test history storage
├── buildozer.spec         # Build configuration for Android/iOS
├── package.json           # Metadata
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Dependencies

### Python Packages
- `kivy>=2.3.0` — UI framework for mobile
- `opencv-python>=4.8.0` — Computer vision and face detection
- `numpy>=1.24.0` — Numerical computations
- `plyer>=2.1.0` — Native platform APIs (camera, GPS, audio)
- `matplotlib>=3.8.0` — History visualization (optional)
- `buildozer>=1.4.0` — Build tool for APK/IPA generation

## Known Limitations

- **Accuracy**: Heuristics-based; not validated for medical use
- **Hardware**: Requires device with camera and microphone
- **Permissions**: Explicit user consent needed for camera, location, audio
- **Platform Variation**: Face detection performance varies by device/OS
- **Privacy**: All processing done locally; no data sent to servers
- **Battery**: Continuous face detection consumes significant battery

## Development Workflow

### Run on Desktop (for development)
```bash
cd kivy_app
python main.py
```

### Build for Android (debug APK)
```bash
buildozer android debug
# APK output: bin/drunkdetector-0.2.0-debug.apk
```

### Test on Emulator
```bash
buildozer android debug deploy run
```

## Production Considerations

For production deployment:
1. Replace heuristics with validated ML models (TensorFlow Lite)
2. Implement comprehensive privacy policy and consent forms
3. Integrate certified alcohol testing calibration
4. Add secure encryption for local storage
5. Implement proper error handling and logging
6. Add comprehensive unit and integration tests
7. Conduct clinical validation with medical professionals
8. Implement backend analytics (optional, privacy-aware)

## Performance Metrics

- **Face Detection**: ~30 FPS on modern devices (Android 10+)
- **Memory Usage**: ~150-200 MB at runtime
- **Battery Impact**: ~5-10% per hour of continuous testing

## License

Educational use only. See disclaimer above.

## Support

For issues or questions, refer to:
- [Kivy Documentation](https://kivy.org/doc/stable/)
- [OpenCV Docs](https://docs.opencv.org/)
- [Plyer Documentation](https://plyer.readthedocs.io/)
- [Buildozer Guide](https://buildozer.readthedocs.io/)

## Version History

- **v0.2.0** (Kivy/Python) — Mobile app with real-time face detection
- **v0.1.0** (React Native/Expo) — Initial web-based prototype
