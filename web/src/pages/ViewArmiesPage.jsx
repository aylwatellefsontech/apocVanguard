import { useMemo, useState } from 'react'
import ArmyCardEntry from '../components/ArmyCardEntry.jsx'
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
  const [expandedCardIds, setExpandedCardIds] = useState(() => new Set())
  const [viewMode, setViewMode] = useState('army')

  const VIEW_CYCLE = ['army', 'cards', 'all']
  const VIEW_LABELS = {
    army: 'Army',
    cards: 'Cards',
    all: 'Show All',
  }

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
  const allCardsExpanded = Boolean(
    selectedArmy?.cards?.length &&
      selectedArmy.cards.every((entry) => expandedCardIds.has(entry.id)),
  )
  const armyCards = selectedArmy?.cards ?? []
  const hasUnits = selectedArmy?.roster.length > 0
  const hasCards = armyCards.length > 0
  const showArmySection = viewMode === 'army' || viewMode === 'all'
  const showCardsSection = viewMode === 'cards' || viewMode === 'all'

  function nextViewMode(mode) {
    const index = VIEW_CYCLE.indexOf(mode)
    return VIEW_CYCLE[(index + 1) % VIEW_CYCLE.length]
  }

  function handleCycleViewMode() {
    setViewMode((current) => nextViewMode(current))
  }

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

  function handleToggleAllCards() {
    if (!armyCards.length) {
      return
    }

    if (allCardsExpanded) {
      setExpandedCardIds(new Set())
      return
    }

    setExpandedCardIds(new Set(armyCards.map((entry) => entry.id)))
  }

  function handleToggleCard(entryId) {
    setExpandedCardIds((current) => {
      const next = new Set(current)
      if (next.has(entryId)) {
        next.delete(entryId)
      } else {
        next.add(entryId)
      }
      return next
    })
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
                      setExpandedCardIds(new Set())
                      setViewMode('army')
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
                    {hasCards ? ` · ${armyCards.length} cards` : ''}
                  </p>
                </div>
                <div className="header-actions">
                  {(viewMode === 'army' || viewMode === 'all') && hasUnits && (
                    <button
                      type="button"
                      className="secondary-btn"
                      onClick={handleToggleAllEntries}
                    >
                      {allExpanded ? 'Collapse All' : 'Expand All'}
                    </button>
                  )}
                  {(viewMode === 'cards' || viewMode === 'all') && hasCards && (
                    <button
                      type="button"
                      className="secondary-btn"
                      onClick={handleToggleAllCards}
                    >
                      {allCardsExpanded ? 'Collapse All' : 'Expand All'}
                    </button>
                  )}
                  <button
                    type="button"
                    className="secondary-btn"
                    onClick={handleCycleViewMode}
                  >
                    {VIEW_LABELS[nextViewMode(viewMode)]}
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
              ) : viewMode === 'all' && !hasUnits && !hasCards ? (
                <p className="muted panel-message">This army has no units or cards.</p>
              ) : (
                <>
                  {showArmySection && (
                    <section className="army-view-section">
                      <div className="roster-section-header">
                        <h3 className="roster-section-title">Army</h3>
                        <span className="roster-section-count">
                          {selectedArmy.roster.length} units
                        </span>
                      </div>
                      {!hasUnits ? (
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
                    </section>
                  )}

                  {showCardsSection && (
                    <section className="army-view-section">
                      <div className="roster-section-header">
                        <h3 className="roster-section-title">Command Cards</h3>
                        <span className="roster-section-count">
                          {armyCards.length} Cards
                        </span>
                      </div>
                      {!hasCards ? (
                        <p className="muted panel-message">This army has no cards.</p>
                      ) : (
                        <ul className="roster-list army-roster-list">
                          {armyCards.map((entry) => (
                            <ArmyCardEntry
                              key={entry.id}
                              entry={entry}
                              expanded={expandedCardIds.has(entry.id)}
                              onToggleExpanded={() => handleToggleCard(entry.id)}
                            />
                          ))}
                        </ul>
                      )}
                    </section>
                  )}
                </>
              )}
            </>
          )}
        </section>
      </div>
    </>
  )
}
