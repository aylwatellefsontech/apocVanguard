import { useState } from 'react'
import './App.css'
import AppNav from './components/AppNav.jsx'
import BrowsePage from './pages/BrowsePage.jsx'
import BuildArmyPage from './pages/BuildArmyPage.jsx'
import ViewArmiesPage from './pages/ViewArmiesPage.jsx'
import RulesPage from './pages/RulesPage.jsx'

export default function App() {
  const [page, setPage] = useState('browse')
  const [armyToEdit, setArmyToEdit] = useState(null)
  const [buildSession, setBuildSession] = useState(0)

  function navigate(nextPage) {
    setPage(nextPage)
    if (nextPage === 'build' && page !== 'armies') {
      setArmyToEdit(null)
      setBuildSession((value) => value + 1)
    }
    if (nextPage !== 'build') {
      setArmyToEdit(null)
    }
  }

  function openEditor(army) {
    setArmyToEdit(army)
    setBuildSession((value) => value + 1)
    setPage('build')
  }

  return (
    <div className="app">
      <AppNav page={page} onNavigate={navigate} />
      {page === 'browse' && <BrowsePage onCreateArmy={() => navigate('build')} />}
      {page === 'build' && (
        <BuildArmyPage
          key={armyToEdit?.id ?? `new-${buildSession}`}
          initialArmy={armyToEdit}
        />
      )}
      {page === 'armies' && <ViewArmiesPage onEditArmy={openEditor} />}
      {page === 'rules' && <RulesPage />}
    </div>
  )
}
