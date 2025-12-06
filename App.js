import React, { useRef, useState, useEffect } from 'react'
import './App.css'

const READ_PHRASE = 'Please say: The quick brown fox jumps over the lazy dog'
const SLUR_KEYWORDS = ['thequick', 'brown', 'fox', 'jumps', 'over', 'lazy', 'dog']
const CONFIDENCE_THRESHOLD = 0.7
const SLUR_THRESHOLD = 0.5

function App() {
  const videoRef = useRef(null)
  const canvasRef = useRef(null)
  const streamRef = useRef(null)
  const analysisIntervalRef = useRef(null)
  const recognitionRef = useRef(null)

  const [status, setStatus] = useState('Ready')
  const [score, setScore] = useState(0)
  const [risk, setRisk] = useState(false)
  const [speechResult, setSpeechResult] = useState(null)
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

  const startCamera = async () => {
    try {
      setStatus('Requesting camera...')
      const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'user' }, audio: false })
      videoRef.current.srcObject = stream
      streamRef.current = stream
      setStatus('Camera ready')
    } catch (error) {
      setStatus(`Camera error: ${error.message}`)
    }
  }

  const startAnalysis = () => {
    if (!videoRef.current || !videoRef.current.srcObject) {
      setStatus('Start camera first')
      return
    }

    setStatus('Analyzing...')
    setScore(0)
    setRisk(false)

    analysisIntervalRef.current = setInterval(() => {
      const canvas = canvasRef.current
      const ctx = canvas.getContext('2d')

      canvas.width = videoRef.current.videoWidth
      canvas.height = videoRef.current.videoHeight

      ctx.drawImage(videoRef.current, 0, 0)

      // Simple eye-closure detection: average pixel brightness in upper-half
      const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height / 2)
      const data = imageData.data
      let brightness = 0
      for (let i = 0; i < data.length; i += 4) {
        brightness += (data[i] + data[i + 1] + data[i + 2]) / 3
      }
      brightness /= data.length / 4

      // Lower brightness might indicate closed eyes
      const eyeClosureScore = Math.max(0, (255 - brightness) / 255)
      setScore(prev => Math.max(prev, eyeClosureScore * 0.3))

      // Head tilt detection: horizontal symmetry
      const leftHalf = ctx.getImageData(0, 0, canvas.width / 2, canvas.height)
      const rightHalf = ctx.getImageData(canvas.width / 2, 0, canvas.width / 2, canvas.height)
      const leftData = leftHalf.data
      const rightData = rightHalf.data

      let diff = 0
      for (let i = 0; i < Math.min(leftData.length, rightData.length); i++) {
        diff += Math.abs(leftData[i] - rightData[i])
      }
      const asymmetry = diff / Math.max(leftData.length, rightData.length)
      setScore(prev => Math.max(prev, Math.min(1, asymmetry / 100)))

      setRisk(score > 0.5)
    }, 500)
  }

  const stopAnalysis = () => {
    if (analysisIntervalRef.current) {
      clearInterval(analysisIntervalRef.current)
    }
    setStatus('Stopped')
  }

  const startSpeechTest = () => {
    if (recognitionRef.current) {
      setSpeechResult(null)
      setStatus('Listening...')
      recognitionRef.current.start()
    } else {
      setStatus('Speech Recognition not supported')
    }
  }

  const sendAlert = async () => {
    try {
      const position = await new Promise((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(resolve, reject)
      })
      const { latitude: lat, longitude: lon } = position.coords

      const response = await fetch('/api/send-alert', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ lat, lon, score })
      })
      const data = await response.json()
      setStatus(data.ok ? 'Alert sent' : `Alert error: ${data.error}`)
    } catch (error) {
      setStatus(`Alert error: ${error.message}`)
    }
  }

  return (
    <div className="app">
      <h1>Alcohol Detection PWA</h1>
      <div className="video-container">
        <video ref={videoRef} playsInline muted style={{transform:'scaleX(-1)'}}/>
        <canvas ref={canvasRef} className="overlayCanvas" />
      </div>

      <div className="controls">
        <button onClick={startCamera}>Start Camera</button>
        <button onClick={startAnalysis}>Start Analysis</button>
        <button onClick={stopAnalysis}>Stop</button>
        <button onClick={startSpeechTest}>{READ_PHRASE}</button>
      </div>

      <div className="status">Status: {status}</div>
      <div>Score: {score.toFixed(2)} — {risk ? 'AT RISK' : 'OK'}</div>
      <div>Speech: {speechResult ? `${speechResult.text} (conf ${speechResult.confidence.toFixed(2)})` : 'not tested'}</div>

      <button onClick={sendAlert} style={{marginTop: 12, padding: '10px 20px', backgroundColor: '#ff6b6b', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer'}}>Send Alert</button>

      <p style={{marginTop:12, color:'#666'}}>Notes: This app provides heuristics only. Tune thresholds and replace with trained classifier for production.</p>
    </div>
  )
}

export default App
