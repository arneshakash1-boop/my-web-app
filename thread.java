// App.js
// Prototype: Drunk Detector (Expo + React Native)
// Purpose: Proof-of-concept app using camera + simple heuristics to estimate intoxication.
// IMPORTANT: This is a prototype educational project. It is NOT a certified alcohol test.
// Use it only as an assistive tool. DO NOT rely on it for legal, medical or safety-critical decisions.


/*
Setup (run in your project folder in VSCode terminal):


1) Install Expo CLI (if you don't have):
npm install -g expo-cli


2) Create new project (if starting fresh):
expo init DrunkDetector
cd DrunkDetector


3) Install dependencies:
expo install expo-camera expo-permissions expo-face-detector expo-location expo-av
npm install @react-native-async-storage/async-storage


4) Replace App.js with this file content.


5) Run:
expo start


Notes: expo-face-detector uses Google ML Kit under the hood; behavior varies by platform.
This example uses simple heuristics (eye open probability, head rotation, audio energy) to compute a "drunk score".
To build a production-grade solution you should replace heuristics with validated ML models and follow privacy, legal and ethics guidelines.
*/


import React, { useState, useRef, useEffect } from 'react';
import { StyleSheet, Text, View, TouchableOpacity, ActivityIndicator, Alert, Platform, Linking } from 'react-native';
import { Camera } from 'expo-camera';
import * as FaceDetector from 'expo-face-detector';
import * as Location from 'expo-location';
import { Audio } from 'expo-av';


export default function App() {
const cameraRef = useRef(null);
const [hasCameraPermission, setHasCameraPermission] = useState(null);
const [hasLocationPermission, setHasLocationPermission] = useState(null);
const [isTesting, setIsTesting] = useState(false);
const [statusText, setStatusText] = useState('Idle');
const [drunkScore, setDrunkScore] = useState(null);
const [lastResult, setLastResult] = useState(null);


useEffect(() => {
(async () => {
const { status } = await Camera.requestCameraPermissionsAsync();
setHasCameraPermission(status === 'granted');
const locationStatus = await Location.requestForegroundPermissionsAsync();
setHasLocationPermission(locationStatus.status === 'granted');
})();
}, []);


// Simple helper to compute RMS of audio samples (array of floats)
function computeRMS(samples) {
if (!samples || samples.length === 0) return 0;
let sum = 0;
for (let i = 0; i < samples.length; i++) {
sum += samples[i] * samples[i];
}
return Math.sqrt(sum / samples.length);
}


// Main test flow:
// 1) Capture several frames and run face detector
// 2) Record a short audio while asking user to repeat phrase
// 3) Compute simple heuristics into a score
// 4) If score > threshold, offer to notify family with live location
async function runTest() {
if (!cameraRef.current) return Alert.alert('Camera not ready');
setIsTesting(true);
setStatusText('Collecting face samples...');


const faceSamples = [];


// capture 6 quick photos and run face detection on each (0.7s apart)
for (let i = 0; i < 6; i++) {
try {

    