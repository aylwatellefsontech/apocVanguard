import { useMemo, useState } from 'react'
import ArmyRosterEntry from '../components/ArmyRosterEntry.jsx'
import { MAX_SAVED_ARMIES } from '../constants.js'
import { useArmy } from '../hooks/useFactions.js'
import { deleteSavedArmy, loadSavedArmies } from '../utils/armyStorage.js'

function formatUpdatedAt(iso) {
  if (!iso) return ''
  try {
    return new Date(iso).toLocaleDateString(undefined, {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    })
  } catch {
    return ''
  }
}

export default function ViewArmiesPage({ onEditArmy }) {
  const [savedArmies, setSavedArmies] = useState(() => loadSavedArmies())
  const [selectedArmyId, setSelectedArmyId] = useState(
    () => loadSavedArmies()[0]?.id ?? null,
  )
  const [expandedEntryIds, setExpandedEntryIds] = useState(() => new Set())

  const selectedArmy = useMemo(
    () => savedArmies.find((army) => army.id === selectedArmyId) ?? null,
    [savedArmies, selectedArmyId],
  )

  const { army: factionArmy, loading: loadingArmy, error: armyError } = useArmy(
    selectedArmy?.factionId ?? null,
  )

  const unitsByNo = useMemo(() => {
    const map = new Map()
    factionArmy?.units?.forEach((unit) => {
      map.set(unit.no, unit)
    })
    return map
  }, [factionArmy])

  const allExpanded = Boolean(
    selectedArmy?.roster.length &&
      selectedArmy.roster.every((entry) => expandedEntryIds.has(entry.id)),
  )

  function handleDeleteArmy(id) {
    const next = deleteSavedArmy(id)
    setSavedArmies(next)
    if (selectedArmyId === id) {
      setSelectedArmyId(next[0]?.id ?? null)
    }
  }

  function handleToggleEntry(entryId) {
    setExpandedEntryIds((current) => {
      const next = new Set(current)
      if (next.has(entryId)) {
        next.delete(entryId)
      } else {
        next.add(entryId)
      }
      return next
    })
  }

  function handleToggleAllEntries() {
    if (!selectedArmy?.roster.length) {
      return
    }

    if (allExpanded) {
      setExpandedEntryIds(new Set())
      return
    }

    setExpandedEntryIds(new Set(selectedArmy.roster.map((entry) => entry.id)))
  }

  return (
    <>
      <header className="app-header">
        <div>
          <p className="eyebrow">Warhammer 40,000 · Apocalypse</p>
          <h1>My Armies</h1>
        </div>
        <p className="header-meta">
          {savedArmies.length}/{MAX_SAVED_ARMIES} saved
        </p>
      </header>

      {armyError && <p className="error-banner">{armyError}</p>}

      <div className="view-armies-body">
        <aside className="saved-armies-panel">
          <h2>Saved Armies</h2>
          {savedArmies.length === 0 ? (
            <p className="muted panel-message">
              No saved armies yet. Build one on the Build Army page.
            </p>
          ) : (
            <ul className="saved-army-list">
              {savedArmies.map((army) => (
                <li
                  key={army.id}
                  className={
                    army.id === selectedArmyId
                      ? 'saved-army-item active'
                      : 'saved-army-item'
                  }
                >
                  <button
                    type="button"
                    className="saved-army-select"
                    onClick={() => {
                      setSelectedArmyId(army.id)
                      setExpandedEntryIds(new Set())
                    }}
                  >
                    <strong>{army.name}</strong>
                    <p className="roster-item-meta">
                      {army.factionName} · {army.totalPoints} Pt
                    </p>
                    {army.updatedAt && (
                      <p className="roster-item-meta">{formatUpdatedAt(army.updatedAt)}</p>
                    )}
                  </button>
                  <div className="saved-army-actions">
                    <button
                      type="button"
                      className="text-btn"
                      onClick={() => onEditArmy(army)}
                    >
                      Edit
                    </button>
                    <button
                      type="button"
                      className="text-btn danger"
                      onClick={() => handleDeleteArmy(army.id)}
                    >
                      Delete
                    </button>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </aside>

        <section className="army-detail-panel">
          {!selectedArmy ? (
            <p className="muted panel-message">Select a saved army to view it.</p>
          ) : (
            <>
              <header className="army-detail-header">
                <div>
                  <h2>{selectedArmy.name}</h2>
                  <p className="roster-item-meta">
                    {selectedArmy.factionName} · {selectedArmy.totalPoints} Pt total
                  </p>
                </div>
                <div className="header-actions">
                  <button
                    type="button"
                    className="secondary-btn"
                    onClick={handleToggleAllEntries}
                    disabled={selectedArmy.roster.length === 0}
                  >
                    {allExpanded ? 'Collapse All' : 'Expand All'}
                  </button>
                  <button
                    type="button"
                    className="primary-btn"
                    onClick={() => onEditArmy(selectedArmy)}
                  >
                    Edit Army
                  </button>
                </div>
              </header>

              {loadingArmy ? (
                <p className="muted panel-message">Loading unit datasheets…</p>
              ) : selectedArmy.roster.length === 0 ? (
                <p className="muted panel-message">This army has no units.</p>
              ) : (
                <ul className="roster-list army-roster-list">
                  {selectedArmy.roster.map((entry) => (
                    <ArmyRosterEntry
                      key={entry.id}
                      entry={entry}
                      unit={unitsByNo.get(entry.unitNo) ?? null}
                      expanded={expandedEntryIds.has(entry.id)}
                      onToggleExpanded={() => handleToggleEntry(entry.id)}
                    />
                  ))}
                </ul>
              )}
            </>
          )}
        </section>
      </div>
    </>
  )
}
