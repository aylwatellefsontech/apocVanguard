import { useMemo, useState } from 'react'
import UnitDetail from '../components/UnitDetail.jsx'
import { useArmy, useFactions } from '../hooks/useFactions.js'
import { groupUnitsByType } from '../utils/units.js'

export default function BrowsePage({ onCreateArmy }) {
  const { factions, loading: loadingFactions, error: factionsError } = useFactions()
  const [selectedFactionId, setSelectedFactionId] = useState(null)
  const activeFactionId = selectedFactionId ?? factions[0]?.id ?? null
  const { army, loading: loadingArmy, error: armyError } = useArmy(activeFactionId)
  const [selectedUnitNo, setSelectedUnitNo] = useState(null)
  const [search, setSearch] = useState('')

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
  const selectedFaction = factions.find((faction) => faction.id === activeFactionId)
  const error = factionsError || armyError

  return (
    <>
      <header className="app-header">
        <div>
          <p className="eyebrow">Warhammer 40,000 · Apocalypse</p>
          <h1>Army Lists</h1>
        </div>
        <div className="header-actions">
          {selectedFaction && (
            <p className="header-meta">
              {selectedFaction.unitCount} units · {selectedFaction.source}
            </p>
          )}
          <button type="button" className="primary-btn" onClick={onCreateArmy}>
            Create Army
          </button>
        </div>
      </header>

      {error && <p className="error-banner">{error}</p>}

      <div className="app-body">
        <aside className="faction-panel">
          <h2>Factions</h2>
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
          <UnitDetail unit={selectedUnit} />
        </section>
      </div>
    </>
  )
}
