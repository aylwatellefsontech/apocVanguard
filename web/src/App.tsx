import { useState } from 'react'
import './App.css'
import AppNav from './components/AppNav'
import BrowsePage from './pages/BrowsePage'
import BuildArmyPage from './pages/BuildArmyPage'
import ViewArmiesPage from './pages/ViewArmiesPage'
import RulesPage from './pages/RulesPage'
import type { AppPage, SavedArmy } from './types'

export default function App() {
  const [page, setPage] = useState<AppPage>('browse')
  const [armyToEdit, setArmyToEdit] = useState<SavedArmy | null>(null)
  const [buildSession, setBuildSession] = useState(0)

  function navigate(nextPage: AppPage) {
    setPage(nextPage)
    if (nextPage === 'build' && page !== 'armies') {
      setArmyToEdit(null)
      setBuildSession((value) => value + 1)
    }
    if (nextPage !== 'build') {
      setArmyToEdit(null)
    }
  }

  function openEditor(army: SavedArmy) {
    setArmyToEdit(army)
    setBuildSession((value) => value + 1)
    setPage('build')
  }

  return (
    <div className="app">
      <AppNav page={page} onNavigate={navigate} />
      {page === 'browse' && <BrowsePage onCreateArmy={() => navigate('build')} />}
      {page === 'build' && (
        <BuildArmyPage key={armyToEdit?.id ?? `new-${buildSession}`} initialArmy={armyToEdit} />
      )}
      {page === 'armies' && <ViewArmiesPage onEditArmy={openEditor} />}
      {page === 'rules' && <RulesPage />}
    </div>
  )
}
