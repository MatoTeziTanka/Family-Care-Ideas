import './Leaderboard.css'

function Leaderboard({ data }) {
  const getMedalEmoji = (rank) => {
    switch(rank) {
      case 1: return '🏆'
      case 2: return '🥈'
      case 3: return '🥉'
      default: return null
    }
  }

  const getRankClass = (rank) => {
    if (rank <= 3) return `rank-${rank}`
    return ''
  }

  const formatScore = (score) => {
    return score.toLocaleString()
  }

  return (
    <div className="leaderboard-container">
      {/* Top 3 - Special display */}
      <div className="top-three">
        {data.slice(0, 3).map((entry, index) => (
          <div 
            key={entry.player_id}
            className={`top-player ${getRankClass(entry.rank)} animate-bounce-in delay-${index + 1}00`}
          >
            <div className="player-rank">
              <span className="medal">{getMedalEmoji(entry.rank)}</span>
              <span className="rank-number">#{entry.rank}</span>
            </div>
            <div className="player-name neon-cyan">
              {entry.name.toUpperCase()}
            </div>
            <div className={`player-score ${entry.rank === 1 ? 'neon-gold' : 'neon-orange'}`}>
              {formatScore(entry.high_score)}
            </div>
            <div className="player-stats">
              {entry.games_played} games • Avg: {formatScore(entry.avg_score)}
            </div>
          </div>
        ))}
      </div>

      {/* Rest of leaderboard (4-25) */}
      <div className="remaining-players">
        {data.slice(3).map((entry, index) => (
          <div 
            key={entry.player_id}
            className={`player-row animate-slide-in-up delay-${Math.min(index, 5)}00`}
          >
            <div className="row-rank">
              #{entry.rank}
            </div>
            <div className="row-name neon-cyan">
              {entry.name}
            </div>
            <div className="row-score neon-orange">
              {formatScore(entry.high_score)}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Leaderboard

