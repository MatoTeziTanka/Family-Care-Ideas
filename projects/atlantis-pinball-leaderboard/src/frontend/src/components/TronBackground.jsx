import { useEffect, useRef } from 'react'
import './TronBackground.css'

function TronBackground() {
  const particlesRef = useRef(null)

  useEffect(() => {
    // Create floating particles
    const particleCount = 30
    const container = particlesRef.current
    
    if (!container) return

    for (let i = 0; i < particleCount; i++) {
      const particle = document.createElement('div')
      particle.className = 'particle'
      
      // Random position
      particle.style.left = `${Math.random() * 100}%`
      particle.style.animationDelay = `${Math.random() * 20}s`
      particle.style.animationDuration = `${15 + Math.random() * 10}s`
      
      // Random color (cyan or orange)
      const isCyan = Math.random() > 0.3
      particle.style.background = isCyan ? '#00D9FF' : '#FF9500'
      particle.style.boxShadow = isCyan ? '0 0 5px #00D9FF' : '0 0 5px #FF9500'
      
      container.appendChild(particle)
    }

    // Cleanup
    return () => {
      if (container) {
        container.innerHTML = ''
      }
    }
  }, [])

  return (
    <div className="tron-background">
      {/* Animated grid lines */}
      <div className="grid-lines"></div>
      
      {/* Floating particles */}
      <div ref={particlesRef} className="particles"></div>
      
      {/* Scanlines effect */}
      <div className="scanlines"></div>
    </div>
  )
}

export default TronBackground

