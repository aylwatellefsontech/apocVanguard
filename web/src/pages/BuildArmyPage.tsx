import { useMemo, useRef, useState } from 'react'
import ArmyCardSummary from '../components/ArmyCardSummary'
import CardDetail from '../components/CardDetail'
import RosterEntrySummary from '../components/RosterEntrySummary'
import UnitDetail from '../components/UnitDetail'
import { MAX_SAVED_ARMIES } from '../constants'
import { useCards } from '../hooks/useCards'
import { useArmy, useFactions } from '../hooks/useFactions'
import {
  createArmyCardEntry,
  createRosterEntry,
  deleteSavedArmy,
  loadSavedArmies,
  saveArmy,
  toggleRosterOption,
} from '../utils/armyStorage'
import { summarizeOption } from '../utils/formatOption'
import { getProfileStatsForEntry, groupUnitsByType, sortRosterByType } from '../utils/units'
import type {
  ArmyCardEntry,
  BrowseMode,
  Card,
  RosterEntry,
  SaveMessage,
  SavedArmy,
  Unit,
  UnitOption,
  UnitProfile,
} from '../types'

interface BuildArmyPageProps {
  initialArmy?: SavedArmy | null
}

export default function BuildArmyPage({ initialArmy = null }: BuildArmyPageProps) {
  const { factions, loading: loadingFactions, error: factionsError } = useFactions()
  const { cards, factions: cardFactions, loading: loadingCards, error: cardsError } = useCards()
  const [buildMode, setBuildMode] = useState<BrowseMode>('army')
  const [selectedCardFac, setSelectedCardFac] = useState<string | null>(null)
  const [selectedFactionId, setSelectedFactionId] = useState<string | null>(
    initialArmy?.factionId ?? null,
  )
  const activeFactionId = selectedFactionId ?? factions[0]?.id ?? null
  const { army, loading: loadingArmy, error: armyError } = useArmy(activeFactionId)
  const [selectedUnitNo, setSelectedUnitNo] = useState<number | null>(
    initialArmy?.roster?.[0]?.unitNo ?? null,
  )
  const [selectedRosterEntryId, setSelectedRosterEntryId] = useState<string | null>(
    initialArmy?.roster?.[0]?.id ?? null,
  )
  const [search, setSearch] = useState('')
  const [roster, setRoster] = useState<RosterEntry[]>(initialArmy?.roster ?? [])
  const [armyCards, setArmyCards] = useState<ArmyCardEntry[]>(initialArmy?.cards ?? [])
  const [selectedCardId, setSelectedCardId] = useState<string | null>(null)
  const cardDetailRefs = useRef(new Map<string, HTMLDivElement>())
  const [armyName, setArmyName] = useState(initialArmy?.name ?? '')
  const [editingArmyId, setEditingArmyId] = useState<string | null>(initialArmy?.id ?? null)
  const [savedArmies, setSavedArmies] = useState<SavedArmy[]>(() => loadSavedArmies())
  const [saveMessage, setSaveMessage] = useState<SaveMessage | null>(null)

  function handleSelectFaction(factionId: string) {
    setBuildMode('army')
    setSelectedFactionId(factionId)
    setSelectedCardFac(null)
    setSelectedUnitNo(null)
    setSelectedRosterEntryId(null)
    setSelectedCardId(null)
    setSearch('')
  }

  function handleSelectCards(fac: string | null) {
    setBuildMode('cards')
    setSelectedCardFac(fac)
    setSelectedUnitNo(null)
    setSelectedRosterEntryId(null)
    setSelectedCardId(null)
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

  const unitsByType = useMemo(() => groupUnitsByType(filteredUnits), [filteredUnits])

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
        card.ability?.toLowerCase().includes(query) ||
        `${card.set}-${card.nm}`.toLowerCase().includes(query),
    )
  }, [cards, selectedCardFac, search])

  const cardsByFac = useMemo(() => {
    const groups = new Map<string, Card[]>()
    for (const card of filteredCards) {
      const list = groups.get(card.fac) ?? []
      list.push(card)
      groups.set(card.fac, list)
    }
    return [...groups.entries()].sort(([a], [b]) => a.localeCompare(b))
  }, [filteredCards])

  const armyCardIds = useMemo(() => new Set(armyCards.map((entry) => entry.cardId)), [armyCards])

  const selectedCard = filteredCards.find(
    (card) => card.id === (selectedCardId ?? filteredCards[0]?.id),
  )
  const activeCardId = selectedCard?.id

  const selectedUnit = army?.units?.find(
    (unit) => unit.no === (selectedUnitNo ?? army?.units?.[0]?.no),
  )
  const activeUnitNo = selectedUnit?.no
  const selectedRosterEntry = roster.find((entry) => entry.id === selectedRosterEntryId)
  const optionProfileStats = useMemo(() => {
    if (!selectedUnit || !selectedRosterEntry) {
      return null
    }
    if (selectedRosterEntry.unitNo !== selectedUnit.no) {
      return null
    }
    return getProfileStatsForEntry(selectedUnit, selectedRosterEntry)
  }, [selectedUnit, selectedRosterEntry])

  const canEditOptions = Boolean(
    selectedRosterEntry && selectedUnit && selectedRosterEntry.unitNo === selectedUnit.no,
  )

  const totalPoints = roster.reduce((sum, entry) => sum + entry.points, 0)
  const sortedRoster = useMemo(() => sortRosterByType(roster), [roster])
  const error = factionsError || armyError || cardsError
  const cardsPanelTitle = selectedCardFac ? `${selectedCardFac} Cards` : 'All Cards'

  function handleAddProfile(unit: Unit, profile: UnitProfile) {
    const entry = createRosterEntry(unit, profile)
    setRoster((current) => [...current, entry])
    setSelectedRosterEntryId(entry.id)
    setSelectedUnitNo(unit.no)
    setSaveMessage(null)
  }

  function handleSelectRosterEntry(entry: RosterEntry) {
    setSelectedRosterEntryId(entry.id)
    setSelectedUnitNo(entry.unitNo)
  }

  function handleToggleOption(optionIndex: number, option: UnitOption) {
    if (!selectedRosterEntry || !selectedUnit) {
      return
    }
    if (selectedRosterEntry.unitNo !== selectedUnit.no) {
      return
    }

    const profileStats = getProfileStatsForEntry(selectedUnit, selectedRosterEntry)
    const summary = summarizeOption(option, profileStats)

    setRoster((current) =>
      current.map((entry) =>
        entry.id === selectedRosterEntry.id
          ? toggleRosterOption(entry, optionIndex, summary)
          : entry,
      ),
    )
    setSaveMessage(null)
  }

  function handleRemoveEntry(entryId: string) {
    setRoster((current) => current.filter((entry) => entry.id !== entryId))
    if (selectedRosterEntryId === entryId) {
      setSelectedRosterEntryId(null)
    }
    setSaveMessage(null)
  }

  function handleRemoveCard(entryId: string) {
    setArmyCards((current) => current.filter((entry) => entry.id !== entryId))
    setSaveMessage(null)
  }

  function handleToggleArmyCard(card: Card) {
    if (armyCardIds.has(card.id)) {
      setArmyCards((current) => current.filter((entry) => entry.cardId !== card.id))
    } else {
      setArmyCards((current) => [...current, createArmyCardEntry(card)])
    }
    setSaveMessage(null)
  }

  function handleSelectCard(card: Card) {
    setSelectedCardId(card.id)
    cardDetailRefs.current.get(card.id)?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }

  function handleClearRoster() {
    setRoster([])
    setArmyCards([])
    setArmyName('')
    setEditingArmyId(null)
    setSelectedRosterEntryId(null)
    setSelectedCardId(null)
    setSaveMessage(null)
  }

  function handleSaveArmy() {
    const trimmedName = armyName.trim()
    if (!trimmedName) {
      setSaveMessage({ type: 'error', text: 'Enter a name before saving.' })
      return
    }
    if (!activeFactionId || (roster.length === 0 && armyCards.length === 0)) {
      setSaveMessage({ type: 'error', text: 'Add at least one unit or card before saving.' })
      return
    }

    const payload: SavedArmy = {
      id: editingArmyId ?? crypto.randomUUID(),
      name: trimmedName,
      factionId: activeFactionId,
      factionName: army?.faction ?? '',
      totalPoints,
      updatedAt: new Date().toISOString(),
      roster,
      cards: armyCards,
    }

    const result = saveArmy(payload)
    if (!result.ok) {
      setSaveMessage({ type: 'error', text: result.error ?? 'Failed to save army.' })
      return
    }

    setSavedArmies(result.armies ?? [])
    setEditingArmyId(payload.id)
    setSaveMessage({ type: 'success', text: 'Army saved.' })
  }

  function handleLoadArmy(saved: SavedArmy) {
    setSelectedFactionId(saved.factionId)
    setArmyName(saved.name)
    setEditingArmyId(saved.id)
    setRoster(saved.roster)
    setArmyCards(saved.cards ?? [])
    setSelectedRosterEntryId(saved.roster[0]?.id ?? null)
    setSelectedUnitNo(saved.roster[0]?.unitNo ?? null)
    setSaveMessage({ type: 'success', text: `Loaded "${saved.name}".` })
  }

  function handleDeleteArmy(id: string) {
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
      </header>

      {error && <p className="error-banner">{error}</p>}

      <div className="build-body">
        <div className="build-main">
          <div className="app-body build-grid">
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
                          buildMode === 'army' && faction.id === activeFactionId
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
                        buildMode === 'cards' && !selectedCardFac
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
                          buildMode === 'cards' && selectedCardFac === fac
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

            <section className="unit-panel">
              <div className="unit-panel-toolbar">
                <h2>{buildMode === 'cards' ? cardsPanelTitle : (army?.faction ?? 'Units')}</h2>
                <input
                  type="search"
                  className="search-input"
                  placeholder={buildMode === 'cards' ? 'Search cards…' : 'Search units…'}
                  value={search}
                  onChange={(event) => setSearch(event.target.value)}
                  disabled={buildMode === 'cards' ? loadingCards : !army}
                />
              </div>

              {buildMode === 'army' ? (
                loadingArmy ? (
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
                )
              ) : loadingCards ? (
                <p className="muted panel-message">Loading cards…</p>
              ) : filteredCards.length === 0 ? (
                <p className="muted panel-message">No cards match your search.</p>
              ) : (
                <div className="unit-groups">
                  {cardsByFac.map(([fac, facCards]) => (
                    <div key={fac} className="unit-group">
                      {!selectedCardFac && <h3>{fac}</h3>}
                      <ul className="unit-list">
                        {facCards.map((card) => (
                          <li key={card.id}>
                            <div
                              className={
                                card.id === activeCardId
                                  ? 'card-picker-row active'
                                  : armyCardIds.has(card.id)
                                    ? 'card-picker-row added'
                                    : 'card-picker-row'
                              }
                            >
                              <label className="card-picker-check">
                                <input
                                  type="checkbox"
                                  checked={armyCardIds.has(card.id)}
                                  onChange={() => handleToggleArmyCard(card)}
                                />
                                <span className="sr-only">Add {card.name} to army</span>
                              </label>
                              <button
                                type="button"
                                className="card-picker-main"
                                onClick={() => handleSelectCard(card)}
                              >
                                <span className="unit-name">{card.name}</span>
                                <span className="unit-pts">
                                  {card.set}-{card.nm}
                                </span>
                              </button>
                            </div>
                          </li>
                        ))}
                      </ul>
                    </div>
                  ))}
                </div>
              )}
            </section>

            <section className="detail-panel">
              {buildMode === 'cards' ? (
                loadingCards ? (
                  <p className="muted panel-message">Loading cards…</p>
                ) : filteredCards.length === 0 ? (
                  <p className="muted panel-message">No cards match your search.</p>
                ) : (
                  <div className="cards-stack build-cards-detail">
                    {filteredCards.map((card) => (
                      <div
                        key={card.id}
                        ref={(node) => {
                          if (node) {
                            cardDetailRefs.current.set(card.id, node)
                          } else {
                            cardDetailRefs.current.delete(card.id)
                          }
                        }}
                        className={
                          card.id === activeCardId
                            ? 'build-card-detail-wrap active'
                            : armyCardIds.has(card.id)
                              ? 'build-card-detail-wrap added'
                              : 'build-card-detail-wrap'
                        }
                      >
                        <label className="card-picker-entry-toggle">
                          <input
                            type="checkbox"
                            checked={armyCardIds.has(card.id)}
                            onChange={() => handleToggleArmyCard(card)}
                          />
                          <span>{armyCardIds.has(card.id) ? 'In army' : 'Add to army'}</span>
                        </label>
                        <CardDetail card={card} />
                      </div>
                    ))}
                  </div>
                )
              ) : (
                <UnitDetail
                  unit={selectedUnit}
                  onAddProfile={handleAddProfile}
                  onToggleOption={canEditOptions ? handleToggleOption : undefined}
                  selectedOptionIndexes={
                    canEditOptions
                      ? selectedRosterEntry!.selectedOptions.map((option) => option.index)
                      : []
                  }
                  optionProfileStats={optionProfileStats}
                  emptyMessage="Select a unit to add profiles to your army."
                />
              )}
            </section>
          </div>
        </div>

        <aside className="roster-panel">
          <div className="roster-header">
            <h2>Your Army</h2>
            <div className="roster-header-stats">
              <p className="roster-total">{totalPoints} Pt total</p>
              <p className="roster-section-count">{roster.length} units</p>
            </div>
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

          {roster.length === 0 && armyCards.length === 0 ? (
            <p className="muted panel-message">No units or cards added yet.</p>
          ) : (
            <>
              {roster.length > 0 && (
                <ul className="roster-list">
                  {sortedRoster.map((entry) => (
                    <RosterEntrySummary
                      key={entry.id}
                      entry={entry}
                      active={entry.id === selectedRosterEntryId}
                      onSelect={handleSelectRosterEntry}
                      onRemove={handleRemoveEntry}
                    />
                  ))}
                </ul>
              )}

              <div className="roster-section-header">
                <h3 className="roster-section-title">Command Cards</h3>
                <span className="roster-section-count">{armyCards.length} Cards</span>
              </div>
              {armyCards.length > 0 && (
                <ul className="roster-list">
                  {armyCards.map((entry) => (
                    <ArmyCardSummary key={entry.id} entry={entry} onRemove={handleRemoveCard} />
                  ))}
                </ul>
              )}
            </>
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
                      <button type="button" className="text-btn" onClick={() => handleLoadArmy(saved)}>
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
