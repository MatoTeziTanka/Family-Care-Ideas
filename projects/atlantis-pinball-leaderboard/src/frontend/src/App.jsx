import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import DisplayView from './views/DisplayView'
import ScoreEntryView from './views/ScoreEntryView'
import AdminView from './views/AdminView'
import './App.css'

function App() {
  return (
    <Router>
      <div className="app">
        <Routes>
          {/* Main vertical display for arcade cabinet */}
          <Route path="/" element={<DisplayView />} />
          <Route path="/display" element={<DisplayView />} />
          
          {/* Mobile score entry */}
          <Route path="/add" element={<ScoreEntryView />} />
          
          {/* Admin panel */}
          <Route path="/admin" element={<AdminView />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App

