import { useMemo, useState } from 'react'
import UnitDetail from '../components/UnitDetail.jsx'
import { MAX_SAVED_ARMIES } from '../constants.js'
import { useArmy, useFactions } from '../hooks/useFactions.js'
import {
  createRosterEntry,
  deleteSavedArmy,
  loadSavedArmies,
  saveArmy,
} from '../utils/armyStorage.js'
import { groupUnitsByType } from '../utils/units.js'

export default function BuildArmyPage({ onBack }) {
  const { factions, loading: loadingFactions, error: factionsError } = useFactions()
  const [selectedFactionId, setSelectedFactionId] = useState(null)
  const activeFactionId = selectedFactionId ?? factions[0]?.id ?? null
  const { army, loading: loadingArmy, error: armyError } = useArmy(activeFactionId)
  const [selectedUnitNo, setSelectedUnitNo] = useState(null)
  const [search, setSearch] = useState('')
  const [roster, setRoster] = useState([])
  const [armyName, setArmyName] = useState('')
  const [editingArmyId, setEditingArmyId] = useState(null)
  const [savedArmies, setSavedArmies] = useState(() => loadSavedArmies())
  const [saveMessage, setSaveMessage] = useState(null)

  function handleSelectFaction(factionId) {
    setSelectedFactionId(factionId)
    setSelectedUnitNo(null)
    setSearch('')
  }

  const filteredUnits = useMemo(() => {
    if (!army?.units) return []
    const query = search.trim().toLowerCase()
    if (!query) return army.units
    return army.units.filter(
      (unit) =>
        unit.name.toLowerCase().includes(query) ||
        unit.type.toLowerCase().includes(query) ||
        unit.keywords?.some((keyword) => keyword.toLowerCase().includes(query)),
    )
  }, [army, search])

  const unitsByType = useMemo(
    () => groupUnitsByType(filteredUnits),
    [filteredUnits],
  )

  const selectedUnit = army?.units?.find(
    (unit) => unit.no === (selectedUnitNo ?? army?.units?.[0]?.no),
  )
  const activeUnitNo = selectedUnit?.no
  const totalPoints = roster.reduce((sum, entry) => sum + entry.points, 0)
  const error = factionsError || armyError

  function handleAddProfile(unit, profile) {
    setRoster((current) => [...current, createRosterEntry(unit, profile)])
    setSaveMessage(null)
  }

  function handleRemoveEntry(entryId) {
    setRoster((current) => current.filter((entry) => entry.id !== entryId))
    setSaveMessage(null)
  }

  function handleClearRoster() {
    setRoster([])
    setArmyName('')
    setEditingArmyId(null)
    setSaveMessage(null)
  }

  function handleSaveArmy() {
    const trimmedName = armyName.trim()
    if (!trimmedName) {
      setSaveMessage({ type: 'error', text: 'Enter a name before saving.' })
      return
    }
    if (!activeFactionId || roster.length === 0) {
      setSaveMessage({ type: 'error', text: 'Add at least one profile before saving.' })
      return
    }

    const payload = {
      id: editingArmyId ?? crypto.randomUUID(),
      name: trimmedName,
      factionId: activeFactionId,
      factionName: army?.faction ?? '',
      totalPoints,
      updatedAt: new Date().toISOString(),
      roster,
    }

    const result = saveArmy(payload)
    if (!result.ok) {
      setSaveMessage({ type: 'error', text: result.error })
      return
    }

    setSavedArmies(result.armies)
    setEditingArmyId(payload.id)
    setSaveMessage({ type: 'success', text: 'Army saved.' })
  }

  function handleLoadArmy(saved) {
    setSelectedFactionId(saved.factionId)
    setArmyName(saved.name)
    setEditingArmyId(saved.id)
    setRoster(saved.roster)
    setSaveMessage({ type: 'success', text: `Loaded "${saved.name}".` })
  }

  function handleDeleteArmy(id) {
    const next = deleteSavedArmy(id)
    setSavedArmies(next)
    if (editingArmyId === id) {
      handleClearRoster()
    }
    setSaveMessage({ type: 'success', text: 'Saved army deleted.' })
  }

  return (
    <>
      <header className="app-header">
        <div>
          <p className="eyebrow">Warhammer 40,000 · Apocalypse</p>
          <h1>Build Army</h1>
        </div>
        <div className="header-actions">
          <button type="button" className="secondary-btn" onClick={onBack}>
            Back to Browse
          </button>
        </div>
      </header>

      {error && <p className="error-banner">{error}</p>}

      <div className="build-body">
        <div className="build-main">
          <div className="app-body build-grid">
            <aside className="faction-panel">
              <h2>Faction</h2>
              {loadingFactions ? (
                <p className="muted">Loading factions…</p>
              ) : (
                <ul className="faction-list">
                  {factions.map((faction) => (
                    <li key={faction.id}>
                      <button
                        type="button"
                        className={
                          faction.id === activeFactionId
                            ? 'faction-btn active'
                            : 'faction-btn'
                        }
                        onClick={() => handleSelectFaction(faction.id)}
                      >
                        <span className="faction-name">{faction.faction}</span>
                        <span className="faction-count">{faction.unitCount}</span>
                      </button>
                    </li>
                  ))}
                </ul>
              )}
            </aside>

            <section className="unit-panel">
              <div className="unit-panel-toolbar">
                <h2>{army?.faction ?? 'Units'}</h2>
                <input
                  type="search"
                  className="search-input"
                  placeholder="Search units…"
                  value={search}
                  onChange={(event) => setSearch(event.target.value)}
                  disabled={!army}
                />
              </div>

              {loadingArmy ? (
                <p className="muted panel-message">Loading army list…</p>
              ) : unitsByType.length === 0 ? (
                <p className="muted panel-message">No units match your search.</p>
              ) : (
                <div className="unit-groups">
                  {unitsByType.map(([type, units]) => (
                    <div key={type} className="unit-group">
                      <h3>{type}</h3>
                      <ul className="unit-list">
                        {units.map((unit) => (
                          <li key={unit.no}>
                            <button
                              type="button"
                              className={
                                unit.no === activeUnitNo
                                  ? 'unit-btn active'
                                  : 'unit-btn'
                              }
                              onClick={() => setSelectedUnitNo(unit.no)}
                            >
                              <span className="unit-name">{unit.name}</span>
                              <span className="unit-pts">{unit.stats?.Pt} Pt</span>
                            </button>
                          </li>
                        ))}
                      </ul>
                    </div>
                  ))}
                </div>
              )}
            </section>

            <section className="detail-panel">
              <UnitDetail
                unit={selectedUnit}
                onAddProfile={handleAddProfile}
                emptyMessage="Select a unit to add profiles to your army."
              />
            </section>
          </div>
        </div>

        <aside className="roster-panel">
          <div className="roster-header">
            <h2>Your Army</h2>
            <p className="roster-total">{totalPoints} Pt total</p>
          </div>

          <label className="field-label" htmlFor="army-name">
            Army name
          </label>
          <input
            id="army-name"
            type="text"
            className="search-input"
            placeholder="My Apocalypse Army"
            value={armyName}
            onChange={(event) => setArmyName(event.target.value)}
          />

          {roster.length === 0 ? (
            <p className="muted panel-message">No profiles added yet.</p>
          ) : (
            <ul className="roster-list">
              {roster.map((entry) => (
                <li key={entry.id} className="roster-item">
                  <div>
                    <strong>{entry.unitName}</strong>
                    <p className="roster-item-meta">
                      {entry.profileLabel} · {entry.points} Pt
                    </p>
                  </div>
                  <button
                    type="button"
                    className="text-btn"
                    onClick={() => handleRemoveEntry(entry.id)}
                  >
                    Remove
                  </button>
                </li>
              ))}
            </ul>
          )}

          <div className="roster-actions">
            <button type="button" className="primary-btn" onClick={handleSaveArmy}>
              Save Army
            </button>
            <button type="button" className="secondary-btn" onClick={handleClearRoster}>
              Clear
            </button>
          </div>

          {saveMessage && (
            <p className={saveMessage.type === 'error' ? 'form-error' : 'form-success'}>
              {saveMessage.text}
            </p>
          )}

          <section className="saved-armies">
            <div className="saved-armies-header">
              <h3>Saved Armies</h3>
              <span className="saved-armies-count">
                {savedArmies.length}/{MAX_SAVED_ARMIES}
              </span>
            </div>

            {savedArmies.length === 0 ? (
              <p className="muted">No saved armies yet.</p>
            ) : (
              <ul className="saved-army-list">
                {savedArmies.map((saved) => (
                  <li key={saved.id} className="saved-army-item">
                    <div>
                      <strong>{saved.name}</strong>
                      <p className="roster-item-meta">
                        {saved.factionName} · {saved.totalPoints} Pt
                      </p>
                    </div>
                    <div className="saved-army-actions">
                      <button
                        type="button"
                        className="text-btn"
                        onClick={() => handleLoadArmy(saved)}
                      >
                        Load
                      </button>
                      <button
                        type="button"
                        className="text-btn danger"
                        onClick={() => handleDeleteArmy(saved.id)}
                      >
                        Delete
                      </button>
                    </div>
                  </li>
                ))}
              </ul>
            )}
          </section>
        </aside>
      </div>
    </>
  )
}
