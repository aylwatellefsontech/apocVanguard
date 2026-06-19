import { useState } from 'react'
import './App.css'
import BrowsePage from './pages/BrowsePage.jsx'
import BuildArmyPage from './pages/BuildArmyPage.jsx'

export default function App() {
  const [page, setPage] = useState('browse')

  return (
    <div className="app">
      {page === 'browse' ? (
        <BrowsePage onCreateArmy={() => setPage('build')} />
      ) : (
        <BuildArmyPage onBack={() => setPage('browse')} />
      )}
    </div>
  )
}
