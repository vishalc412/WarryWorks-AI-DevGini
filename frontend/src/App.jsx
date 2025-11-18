import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import HomePage from './pages/HomePage'
import InterviewPage from './pages/InterviewPage'
import GeneratePage from './pages/GeneratePage'
import DashboardPage from './pages/DashboardPage'

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/interview/:sessionId" element={<InterviewPage />} />
          <Route path="/generate/:projectId" element={<GeneratePage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App
