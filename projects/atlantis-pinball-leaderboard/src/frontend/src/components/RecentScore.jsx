import { useState, useEffect } from 'react'
import './RecentScore.css'

function RecentScore({ score }) {
  const [visible, setVisible] = useState(true)

  useEffect(() => {
    // Flash animation when new score arrives
    setVisible(false)
    setTimeout(() => setVisible(true), 100)
  }, [score])

  const getTimeAgo = (dateString) => {
    const date = new Date(dateString)
    const now = new Date()
    const seconds = Math.floor((now - date) / 1000)

    if (seconds < 60) return `${seconds}s ago`
    if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`
    if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`
    return `${Math.floor(seconds / 86400)}d ago`
  }

  if (!score) return null

  return (
    <div className={`recent-score-ticker ${visible ? 'visible animate-flash' : ''}`}>
      <div className="ticker-label neon-cyan">
        ⚡ LATEST GAME
      </div>
      <div className="ticker-content">
        <span className="ticker-player neon-cyan">
          {score.player_name}
        </span>
        <span className="ticker-separator">-</span>
        <span className="ticker-score neon-orange">
          {score.score.toLocaleString()}
        </span>
      </div>
      <div className="ticker-time">
        {getTimeAgo(score.created_at)}
      </div>
    </div>
  )
}

export default RecentScore

