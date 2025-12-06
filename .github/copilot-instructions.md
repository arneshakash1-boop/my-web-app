# Copilot Instructions for Drunk Detector (React Native Expo App)

## Project Overview
This is a prototype sobriety testing app built with React Native and Expo. It uses camera-based face detection, audio analysis, and location services to estimate impairment. All processing is local; no data is sent to servers.

## Key Files & Structure
- `App.js`: Main application logic and UI
- `package.json`: Dependency management
- `app.json`: Expo configuration
- `assets/`: Images and icons (if present)

## Major Components & Data Flow
- **Camera/Face Detection**: Uses `expo-camera` and `expo-face-detector` (Google ML Kit) for real-time analysis
- **Audio Analysis**: Uses `expo-av` for voice recording and RMS energy computation
- **Location**: Uses `expo-location` for GPS retrieval
- **SMS Composer**: Integrates with device SMS for emergency contact
- **Scoring Algorithm**: Computes a "drunk score" (0-100) based on face and audio features

## Scoring Algorithm Details
- Eye closure (up to 30 pts)
- Head rotation (up to 15 pts)
- Audio RMS energy (up to 20 pts)
- Score > 60 triggers high-risk alert

## Developer Workflows
- **Install dependencies**: `npm install`
- **Start development server**: `npm start`
- **Run on device/emulator**:
  - iOS: `npm run ios`
  - Android: `npm run android`
  - Web: `npm run web`
- **Expo Go**: Scan QR code to run on mobile

## Project-Specific Conventions
- All feature detection and scoring is heuristic-based (not ML-driven)
- Permissions for camera, audio, and location must be explicitly requested
- No backend/server integration; all logic is client-side
- Privacy: No data leaves the device

## Integration Points
- Relies on Expo modules (`expo-camera`, `expo-face-detector`, `expo-location`, `expo-av`)
- Uses Google ML Kit via Expo for face detection
- SMS integration via deep linking

## Limitations & Warnings
- Not medically validated; for educational use only
- Accuracy varies by device/platform
- Requires camera and microphone hardware
- All processing is local; no cloud features

## Example Patterns
- Face detection and scoring logic is centralized in main app component
- Permissions are checked at runtime before accessing hardware features
- Emergency alert logic is triggered by score threshold

## References
- See `README.md` for setup, architecture, and limitations
- [Expo Documentation](https://docs.expo.dev/)
- [React Native Docs](https://reactnative.dev/)
- [Google ML Kit Face Detection](https://firebase.google.com/docs/ml-kit/detect-faces)

---
**Update this file if major architectural changes or new workflows are introduced.**
