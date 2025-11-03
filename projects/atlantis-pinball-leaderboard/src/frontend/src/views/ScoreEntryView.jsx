import { useState, useEffect } from 'react'
import axios from 'axios'
import TronBackground from '../components/TronBackground'
import './ScoreEntryView.css'

function ScoreEntryView() {
  const [players, setPlayers] = useState([])
  const [selectedPlayer, setSelectedPlayer] = useState('')
  const [score, setScore] = useState('')
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState({ type: '', text: '' })

  useEffect(() => {
    fetchPlayers()
  }, [])

  const fetchPlayers = async () => {
    try {
      const response = await axios.get('/api/players')
      setPlayers(response.data)
    } catch (error) {
      console.error('Error fetching players:', error)
    }
  }

  const handleQuickScore = (quickScore) => {
    setScore(quickScore.toString())
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!selectedPlayer || !score) {
      setMessage({ type: 'error', text: 'Please select a player and enter a score' })
      return
    }

    setLoading(true)
    setMessage({ type: '', text: '' })

    try {
      await axios.post('/api/scores', {
        player_id: parseInt(selectedPlayer),
        score: parseInt(score),
        verified: false
      })
      
      setMessage({ type: 'success', text: '🎮 Score submitted successfully!' })
      setScore('')
      
      // Reset form after 2 seconds
      setTimeout(() => {
        setMessage({ type: '', text: '' })
      }, 2000)
      
    } catch (error) {
      console.error('Error submitting score:', error)
      setMessage({ type: 'error', text: 'Failed to submit score. Please try again.' })
    } finally {
      setLoading(false)
    }
  }

  const quickScores = [10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000]

  return (
    <div className="score-entry-view">
      <TronBackground />
      
      <div className="score-entry-content">
        <header className="entry-header">
          <h1 className="title-main neon-cyan">ADD SCORE</h1>
          <p className="neon-orange">Atlantis Pinball Leaderboard</p>
        </header>

        <div className="entry-card glass-panel">
          <form onSubmit={handleSubmit}>
            {/* Player Selection */}
            <div className="form-group">
              <label className="neon-cyan">PLAYER</label>
              <select
                className="tron-input"
                value={selectedPlayer}
                onChange={(e) => setSelectedPlayer(e.target.value)}
                required
              >
                <option value="">Select Player...</option>
                {players.map(player => (
                  <option key={player.id} value={player.id}>
                    {player.name}
                  </option>
                ))}
              </select>
            </div>

            {/* Score Input */}
            <div className="form-group">
              <label className="neon-cyan">SCORE</label>
              <input
                type="number"
                className="tron-input"
                value={score}
                onChange={(e) => setScore(e.target.value)}
                placeholder="Enter score..."
                min="0"
                required
              />
            </div>

            {/* Quick Score Buttons */}
            <div className="form-group">
              <label className="neon-cyan">QUICK ADD</label>
              <div className="quick-scores">
                {quickScores.map(qs => (
                  <button
                    key={qs}
                    type="button"
                    className="quick-score-btn"
                    onClick={() => handleQuickScore(qs)}
                  >
                    {(qs / 1000).toFixed(0)}K
                  </button>
                ))}
              </div>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              className="tron-button tron-button-orange submit-btn"
              disabled={loading}
            >
              {loading ? 'SUBMITTING...' : 'SUBMIT SCORE'}
            </button>
          </form>

          {/* Message Display */}
          {message.text && (
            <div className={`message ${message.type} animate-bounce-in`}>
              {message.text}
            </div>
          )}
        </div>

        {/* Quick Links */}
        <div className="quick-links">
          <a href="/" className="tron-button">
            VIEW LEADERBOARD
          </a>
        </div>
      </div>
    </div>
  )
}

export default ScoreEntryView

