import { useState, useEffect } from 'react'
import axios from 'axios'
import TronBackground from '../components/TronBackground'
import Leaderboard from '../components/Leaderboard'
import RecentScore from '../components/RecentScore'
import './DisplayView.css'

function DisplayView() {
  const [leaderboard, setLeaderboard] = useState([])
  const [recentScore, setRecentScore] = useState(null)
  const [loading, setLoading] = useState(true)
  const [ws, setWs] = useState(null)

  // Fetch initial leaderboard data
  useEffect(() => {
    fetchLeaderboard()
    fetchRecentScore()
  }, [])

  // WebSocket for real-time updates
  useEffect(() => {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const wsUrl = `${protocol}//${window.location.host}/ws`
    
    const websocket = new WebSocket(wsUrl)
    
    websocket.onopen = () => {
      console.log('✅ WebSocket connected')
    }
    
    websocket.onmessage = (event) => {
      const message = JSON.parse(event.data)
      console.log('📡 WebSocket message:', message)
      
      if (message.type === 'new_score') {
        // Update leaderboard and recent score
        fetchLeaderboard()
        setRecentScore(message.data)
        
        // Play sound effect (optional)
        playScoreSound()
      }
    }
    
    websocket.onerror = (error) => {
      console.error('❌ WebSocket error:', error)
    }
    
    websocket.onclose = () => {
      console.log('🔌 WebSocket disconnected')
      // Reconnect after 5 seconds
      setTimeout(() => {
        window.location.reload()
      }, 5000)
    }
    
    setWs(websocket)
    
    return () => {
      if (websocket) {
        websocket.close()
      }
    }
  }, [])

  const fetchLeaderboard = async () => {
    try {
      const response = await axios.get('/api/leaderboard?limit=25')
      setLeaderboard(response.data)
      setLoading(false)
    } catch (error) {
      console.error('Error fetching leaderboard:', error)
      setLoading(false)
    }
  }

  const fetchRecentScore = async () => {
    try {
      const response = await axios.get('/api/leaderboard/recent?limit=1')
      if (response.data.length > 0) {
        setRecentScore(response.data[0])
      }
    } catch (error) {
      console.error('Error fetching recent score:', error)
    }
  }

  const playScoreSound = () => {
    // Optional: Add sound effect
    // const audio = new Audio('/sounds/ding.mp3')
    // audio.play()
  }

  if (loading) {
    return (
      <div className="display-view loading">
        <TronBackground />
        <div className="loading-container">
          <div className="tron-spinner"></div>
          <p className="neon-cyan">INITIALIZING LEADERBOARD...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="display-view">
      <TronBackground />
      
      <div className="display-content">
        {/* Header */}
        <header className="display-header">
          <h1 className="title-main neon-cyan animate-text-glow-pulse">
            ATLANTIS
          </h1>
          <h2 className="subtitle neon-orange">
            PINBALL
          </h2>
          <h3 className="subtitle-small neon-cyan">
            HIGH SCORES
          </h3>
        </header>

        {/* Leaderboard */}
        <Leaderboard data={leaderboard} />

        {/* Recent Score Ticker */}
        {recentScore && (
          <RecentScore score={recentScore} />
        )}

        {/* Footer info */}
        <footer className="display-footer">
          <p className="neon-cyan">
            🎮 1975 GOTTLIEB ATLANTIS 🎮
          </p>
        </footer>
      </div>
    </div>
  )
}

export default DisplayView

