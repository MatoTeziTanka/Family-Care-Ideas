import { useState, useEffect } from 'react'
import axios from 'axios'
import TronBackground from '../components/TronBackground'
import './AdminView.css'

function AdminView() {
  const [leaderboard, setLeaderboard] = useState([])
  const [recentScores, setRecentScores] = useState([])
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('leaderboard')

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      const [leaderboardRes, recentRes] = await Promise.all([
        axios.get('/api/leaderboard?limit=25'),
        axios.get('/api/leaderboard/recent?limit=20')
      ])
      
      setLeaderboard(leaderboardRes.data)
      setRecentScores(recentRes.data)
      setLoading(false)
    } catch (error) {
      console.error('Error fetching data:', error)
      setLoading(false)
    }
  }

  const handleDeleteScore = async (scoreId) => {
    if (!confirm('Are you sure you want to delete this score?')) {
      return
    }

    try {
      await axios.delete(`/api/scores/${scoreId}`)
      alert('Score deleted successfully')
      fetchData()
    } catch (error) {
      console.error('Error deleting score:', error)
      alert('Failed to delete score')
    }
  }

  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString()
  }

  if (loading) {
    return (
      <div className="admin-view loading">
        <TronBackground />
        <div className="tron-spinner"></div>
      </div>
    )
  }

  return (
    <div className="admin-view">
      <TronBackground />
      
      <div className="admin-content">
        <header className="admin-header">
          <h1 className="title-main neon-cyan">ADMIN PANEL</h1>
          <p className="neon-orange">Atlantis Pinball Management</p>
        </header>

        {/* Tabs */}
        <div className="tabs">
          <button
            className={`tab-btn ${activeTab === 'leaderboard' ? 'active' : ''}`}
            onClick={() => setActiveTab('leaderboard')}
          >
            LEADERBOARD
          </button>
          <button
            className={`tab-btn ${activeTab === 'recent' ? 'active' : ''}`}
            onClick={() => setActiveTab('recent')}
          >
            RECENT SCORES
          </button>
        </div>

        {/* Leaderboard Tab */}
        {activeTab === 'leaderboard' && (
          <div className="admin-panel glass-panel animate-fade-in">
            <h2 className="neon-cyan">TOP 25 PLAYERS</h2>
            <div className="table-container">
              <table className="admin-table">
                <thead>
                  <tr>
                    <th>Rank</th>
                    <th>Player</th>
                    <th>High Score</th>
                    <th>Games</th>
                    <th>Avg Score</th>
                  </tr>
                </thead>
                <tbody>
                  {leaderboard.map((entry) => (
                    <tr key={entry.player_id}>
                      <td className="rank-col">
                        {entry.rank <= 3 ? (
                          <span className={`rank-badge rank-${entry.rank}`}>
                            #{entry.rank}
                          </span>
                        ) : (
                          `#${entry.rank}`
                        )}
                      </td>
                      <td className="name-col neon-cyan">{entry.name}</td>
                      <td className="score-col neon-orange">
                        {entry.high_score.toLocaleString()}
                      </td>
                      <td>{entry.games_played}</td>
                      <td>{entry.avg_score.toLocaleString()}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Recent Scores Tab */}
        {activeTab === 'recent' && (
          <div className="admin-panel glass-panel animate-fade-in">
            <h2 className="neon-cyan">RECENT SUBMISSIONS</h2>
            <div className="table-container">
              <table className="admin-table">
                <thead>
                  <tr>
                    <th>Date</th>
                    <th>Player</th>
                    <th>Score</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {recentScores.map((score) => (
                    <tr key={score.id}>
                      <td className="date-col">{formatDate(score.created_at)}</td>
                      <td className="name-col neon-cyan">{score.player_name}</td>
                      <td className="score-col neon-orange">
                        {score.score.toLocaleString()}
                      </td>
                      <td>
                        <button
                          className="delete-btn"
                          onClick={() => handleDeleteScore(score.id)}
                        >
                          DELETE
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Quick Links */}
        <div className="quick-links">
          <a href="/" className="tron-button">
            VIEW DISPLAY
          </a>
          <a href="/add" className="tron-button tron-button-orange">
            ADD SCORE
          </a>
        </div>
      </div>
    </div>
  )
}

export default AdminView

