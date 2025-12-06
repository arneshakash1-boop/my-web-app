# Drunk Detector - React Native Expo App

A prototype sobriety testing application built with React Native and Expo.

## ⚠️ IMPORTANT DISCLAIMER

**This is a prototype educational project. It is NOT a certified alcohol breathalyzer or sobriety test.**
- Do NOT rely on it for legal, medical, or safety-critical decisions
- Use it only as an assistive tool for educational purposes
- Impairment assessment requires professional evaluation

## Features

- **Camera Face Detection**: Uses Google ML Kit to analyze facial features
  - Eye closure probability
  - Head rotation and movement

- **Audio Analysis**: Records voice and analyzes audio characteristics
  - RMS (Root Mean Square) energy computation
  - Speech pattern analysis

- **Location Integration**: Optional emergency alerts with GPS coordinates

- **SMS Composer**: Direct contact with family/emergency contacts via SMS

## Setup Instructions

### Prerequisites
- Node.js and npm installed
- Expo CLI installed globally

### Installation

```bash
# 1. Install Expo CLI globally (if you don't have it)
npm install -g expo-cli

# 2. Navigate to the project folder
cd sandy

# 3. Install dependencies
npm install

# 4. Start the Expo development server
npm start
```

### Running on Device/Emulator

```bash
# iOS (Mac only)
npm run ios

# Android
npm run android

# Web
npm run web
```

Scan the QR code with Expo Go app (iOS/Android) to run on your phone.

## Architecture

### Components
- **Camera Module** (`expo-camera`): Real-time video capture and face detection
- **Face Detection** (`expo-face-detector`): Google ML Kit integration
- **Audio Recording** (`expo-av`): Voice recording and RMS analysis
- **Location Services** (`expo-location`): GPS coordinate retrieval
- **Deep Linking** (`react-native`): SMS composer integration

### Scoring Algorithm

The app computes a "drunk score" (0-100) based on:

1. **Face Features** (up to 45 points)
   - Eye closure: 30 points
   - Head rotation: 15 points

2. **Audio Features** (up to 20 points)
   - RMS energy analysis

3. **Risk Thresholds**
   - Score > 60: HIGH RISK (triggers alert option)
   - Score ≤ 60: LOW RISK

## File Structure

```
sandy/
├── App.js              # Main application component
├── package.json        # Dependencies
├── app.json           # Expo configuration
├── README.md          # This file
└── assets/            # Images and icons (if needed)
```

## Dependencies

- `react` & `react-native`: Core framework
- `expo`: Development platform
- `expo-camera`: Camera access
- `expo-face-detector`: Face detection via Google ML Kit
- `expo-location`: GPS and location services
- `expo-av`: Audio recording and playback
- `@react-native-async-storage/async-storage`: Local data persistence

## Known Limitations

- **Accuracy**: Heuristics-based estimation is not validated for medical use
- **Hardware**: Requires device with camera and microphone
- **Permissions**: Requires explicit user consent for camera, location, and audio
- **Platform Variation**: Face detection performance varies by iOS/Android
- **Privacy**: All processing is done locally; no data sent to servers (in this prototype)

## Production Considerations

For a production-grade solution:
1. Replace heuristics with validated ML models
2. Implement comprehensive privacy policy
3. Add legal disclaimers and consent forms
4. Integrate certified alcohol testing calibration
5. Add data encryption and secure storage
6. Implement proper error handling and logging
7. Add unit and integration tests

## License

Educational use only. See disclaimer above.

## Support

For issues or questions, refer to:
- [Expo Documentation](https://docs.expo.dev/)
- [React Native Docs](https://reactnative.dev/)
- [Google ML Kit Face Detection](https://firebase.google.com/docs/ml-kit/detect-faces)
