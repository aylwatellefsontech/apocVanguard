import { useMemo, useState } from 'react'
import CardDetail from '../components/CardDetail'
import UnitDetail from '../components/UnitDetail'
import { useCards } from '../hooks/useCards'
import { useArmy, useFactions } from '../hooks/useFactions'
import { groupUnitsByType } from '../utils/units'
import type { BrowseMode } from '../types'

interface BrowsePageProps {
  onCreateArmy: () => void
}

export default function BrowsePage({ onCreateArmy }: BrowsePageProps) {
  const { factions, loading: loadingFactions, error: factionsError } = useFactions()
  const {
    cards,
    factions: cardFactions,
    loading: loadingCards,
    error: cardsError,
  } = useCards()
  const [browseMode, setBrowseMode] = useState<BrowseMode>('army')
  const [selectedFactionId, setSelectedFactionId] = useState<string | null>(null)
  const [selectedCardFac, setSelectedCardFac] = useState<string | null>(null)
  const activeFactionId = selectedFactionId ?? factions[0]?.id ?? null
  const { army, loading: loadingArmy, error: armyError } = useArmy(
    browseMode === 'army' ? activeFactionId : null,
  )
  const [selectedUnitNo, setSelectedUnitNo] = useState<number | null>(null)
  const [search, setSearch] = useState('')

  function handleSelectFaction(factionId: string) {
    setBrowseMode('army')
    setSelectedFactionId(factionId)
    setSelectedUnitNo(null)
    setSelectedCardFac(null)
    setSearch('')
  }

  function handleSelectCards(fac: string | null) {
    setBrowseMode('cards')
    setSelectedCardFac(fac)
    setSelectedFactionId(null)
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

  const filteredCards = useMemo(() => {
    let list = cards
    if (selectedCardFac) {
      list = list.filter((card) => card.fac === selectedCardFac)
    }
    const query = search.trim().toLowerCase()
    if (!query) return list
    return list.filter(
      (card) =>
        card.name.toLowerCase().includes(query) ||
        card.type?.toLowerCase().includes(query) ||
        card.fac?.toLowerCase().includes(query) ||
        card.ability?.toLowerCase().includes(query),
    )
  }, [cards, selectedCardFac, search])

  const unitsByType = useMemo(() => groupUnitsByType(filteredUnits), [filteredUnits])

  const selectedUnit = army?.units?.find(
    (unit) => unit.no === (selectedUnitNo ?? army?.units?.[0]?.no),
  )
  const activeUnitNo = selectedUnit?.no
  const selectedFaction = factions.find((faction) => faction.id === activeFactionId)
  const error = factionsError || armyError || cardsError
  const cardsPanelTitle = selectedCardFac ? `${selectedCardFac} Cards` : 'All Cards'

  return (
    <>
      <header className="app-header">
        <div>
          <p className="eyebrow">Warhammer 40,000 · Apocalypse</p>
          <h1>{browseMode === 'cards' ? 'Command Cards' : 'Army Lists'}</h1>
        </div>
        <div className="header-actions">
          {browseMode === 'army' && selectedFaction && (
            <p className="header-meta">
              {selectedFaction.unitCount} units · {selectedFaction.source}
            </p>
          )}
          {browseMode === 'cards' && (
            <p className="header-meta">
              {filteredCards.length} cards
              {selectedCardFac ? ` · ${selectedCardFac}` : ' · all factions'}
            </p>
          )}
          <button type="button" className="primary-btn" onClick={onCreateArmy}>
            Create Army
          </button>
        </div>
      </header>

      {error && <p className="error-banner">{error}</p>}

      <div className={`app-body${browseMode === 'cards' ? ' cards-mode' : ''}`}>
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
                      browseMode === 'army' && faction.id === activeFactionId
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

          <h2 className="sidebar-section-title">Cards</h2>
          {loadingCards ? (
            <p className="muted">Loading cards…</p>
          ) : (
            <ul className="faction-list">
              <li>
                <button
                  type="button"
                  className={
                    browseMode === 'cards' && !selectedCardFac
                      ? 'faction-btn active'
                      : 'faction-btn'
                  }
                  onClick={() => handleSelectCards(null)}
                >
                  <span className="faction-name">All</span>
                  <span className="faction-count">{cards.length}</span>
                </button>
              </li>
              {cardFactions.map(({ fac, count }) => (
                <li key={fac}>
                  <button
                    type="button"
                    className={
                      browseMode === 'cards' && selectedCardFac === fac
                        ? 'faction-btn active'
                        : 'faction-btn'
                    }
                    onClick={() => handleSelectCards(fac)}
                  >
                    <span className="faction-name">{fac}</span>
                    <span className="faction-count">{count}</span>
                  </button>
                </li>
              ))}
            </ul>
          )}
        </aside>

        {browseMode === 'cards' ? (
          <section className="cards-feed">
            <div className="unit-panel-toolbar">
              <h2>{cardsPanelTitle}</h2>
              <input
                type="search"
                className="search-input"
                placeholder="Search cards…"
                value={search}
                onChange={(event) => setSearch(event.target.value)}
                disabled={loadingCards}
              />
            </div>

            {loadingCards ? (
              <p className="muted panel-message">Loading cards…</p>
            ) : filteredCards.length === 0 ? (
              <p className="muted panel-message">No cards match your search.</p>
            ) : (
              <div className="cards-stack">
                {filteredCards.map((card) => (
                  <CardDetail key={card.id} card={card} />
                ))}
              </div>
            )}
          </section>
        ) : (
          <>
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
                                unit.no === activeUnitNo ? 'unit-btn active' : 'unit-btn'
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
          </>
        )}
      </div>
    </>
  )
}
