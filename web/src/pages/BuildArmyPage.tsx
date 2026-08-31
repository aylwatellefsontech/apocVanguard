import { useEffect, useMemo, useRef, useState } from 'react'
import { getRouteApi, useNavigate } from '@tanstack/react-router'
import ArmyCardSummary from '../components/ArmyCardSummary'
import BuildArmyMobileBar from '../components/BuildArmyMobileBar'
import CardDetail from '../components/CardDetail'
import ConfirmModal from '../components/ConfirmModal'
import ExportArmyModal from '../components/ExportArmyModal'
import FactionIcon from '../components/FactionIcon'
import FactionPanelTitle from '../components/FactionPanelTitle'
import ImportArmyModal from '../components/ImportArmyModal'
import OrganizeArmyModal from '../components/OrganizeArmyModal'
import Toast from '../components/Toast'
import RosterEntrySummary from '../components/RosterEntrySummary'
import UnitDetail from '../components/UnitDetail'
import UnitGroupHeading from '../components/UnitGroupHeading'
import { MAX_SAVED_ARMIES } from '../constants'
import { useCards } from '../hooks/useCards'
import { useArmy, useFactions } from '../hooks/useFactions'
import { useMobilePanelHistory } from '../hooks/useMobilePanelHistory'
import { MOBILE_QUERY, useMediaQuery } from '../hooks/useMediaQuery'
import {
  createArmyCardEntry,
  createRosterEntry,
  deleteSavedArmy,
  loadSavedArmies,
  saveArmy,
  sortArmyCardsByName,
  toggleRosterOption,
} from '../utils/armyStorage'
import { importAndSaveArmyFromCode } from '../utils/armyImport'
import type { ArmyExportSource } from '../utils/armyExport'
import { getLocalArmy } from '../data/localArmyLists'
import { buildRosterUnitsByEntryId } from '../utils/rosterUnits'
import {
  deriveSavedArmyFactionMeta,
  rosterHasMultipleFactions,
} from '../utils/rosterArmy'
import { sortRosterByOrganizeGroup } from '../utils/rosterOrganize'
import { summarizeOption } from '../utils/formatOption'
import { getChooseOneChoices } from '../utils/optionUtils'
import { getBaseApocCards } from '../utils/cardFactions'
import { getProfileStatsForEntry, groupUnitsByType } from '../utils/units'
import type {
  ArmyCardEntry,
  BrowseMode,
  Card,
  OptionToggleContext,
  RosterEntry,
  SaveMessage,
  SavedArmy,
  Unit,
  UnitOption,
  UnitProfile,
} from '../types'

const buildRouteApi = getRouteApi('/build')

type BuildMobilePanel = 'factions' | 'list' | 'detail' | 'roster'

export default function BuildArmyPage() {
  const { armyId } = buildRouteApi.useSearch()
  const [toastMessage, setToastMessage] = useState<string | null>(null)
  const initialArmy = useMemo(() => {
    if (!armyId) {
      return null
    }
    return loadSavedArmies().find((army) => army.id === armyId) ?? null
  }, [armyId])

  return (
    <>
      <BuildArmyPageContent
        key={armyId ?? 'new'}
        initialArmy={initialArmy}
        onToast={setToastMessage}
      />
      {toastMessage && <Toast message={toastMessage} onDismiss={() => setToastMessage(null)} />}
    </>
  )
}

interface BuildArmyPageContentProps {
  initialArmy: SavedArmy | null
  onToast: (message: string) => void
}

function BuildArmyPageContent({ initialArmy, onToast }: BuildArmyPageContentProps) {
  const navigate = useNavigate()
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
  const isMobile = useMediaQuery(MOBILE_QUERY)
  const { panel: mobilePanel, setPanel: setMobilePanel, goBack: goBackMobilePanel, panelData } =
    useMobilePanelHistory<BuildMobilePanel>('build', isMobile, 'factions')
  const [isEditingRosterEntry, setIsEditingRosterEntry] = useState(false)
  const [confirmNewArmyOpen, setConfirmNewArmyOpen] = useState(false)
  const [importArmyOpen, setImportArmyOpen] = useState(false)
  const [exportArmyOpen, setExportArmyOpen] = useState(false)
  const [organizeArmyOpen, setOrganizeArmyOpen] = useState(false)
  const [importError, setImportError] = useState<string | null>(null)
  const [armyToDelete, setArmyToDelete] = useState<SavedArmy | null>(null)

  const hasArmyDraft =
    roster.length > 0 || armyCards.length > 0 || armyName.trim().length > 0

  useEffect(() => {
    if (!isMobile) {
      return
    }

    if (mobilePanel === 'detail' && panelData) {
      if (panelData.unitNo != null) {
        setSelectedUnitNo(panelData.unitNo as number)
      }
      if (panelData.cardId != null) {
        setSelectedCardId(panelData.cardId as string)
      }
      if (panelData.fromRoster === true && panelData.rosterEntryId != null) {
        setSelectedRosterEntryId(panelData.rosterEntryId as string)
        setIsEditingRosterEntry(true)
      } else if (panelData.fromRoster === false) {
        exitRosterEditMode()
      }
    } else if (mobilePanel !== 'detail') {
      if (panelData?.fromRoster !== true) {
        exitRosterEditMode()
      }
    }
  }, [isMobile, mobilePanel, panelData])

  function exitRosterEditMode() {
    setSelectedRosterEntryId(null)
    setIsEditingRosterEntry(false)
  }

  function handleSelectUnitFromList(unitNo: number) {
    setSelectedUnitNo(unitNo)
    exitRosterEditMode()
    if (isMobile) {
      setMobilePanel('detail', { data: { unitNo, fromRoster: false } })
    }
  }

  function handleSelectFaction(factionId: string) {
    setBuildMode('army')
    setSelectedFactionId(factionId)
    setSelectedCardFac(null)
    setSelectedUnitNo(null)
    setSelectedRosterEntryId(null)
    setIsEditingRosterEntry(false)
    setSelectedCardId(null)
    setSearch('')
    if (isMobile) {
      setMobilePanel('list')
    }
  }

  function handleSelectCards(fac: string | null) {
    setBuildMode('cards')
    setSelectedCardFac(fac)
    setSelectedUnitNo(null)
    setSelectedRosterEntryId(null)
    setIsEditingRosterEntry(false)
    setSelectedCardId(null)
    setSearch('')
    if (isMobile) {
      setMobilePanel('list')
    }
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

  const baseApocCards = useMemo(() => getBaseApocCards(cards), [cards])
  const allBaseCardsAdded = useMemo(
    () => baseApocCards.length > 0 && baseApocCards.every((card) => armyCardIds.has(card.id)),
    [baseApocCards, armyCardIds],
  )

  const sortedArmyCards = armyCards

  const selectedCard = filteredCards.find(
    (card) => card.id === (selectedCardId ?? filteredCards[0]?.id),
  )
  const activeCardId = selectedCard?.id

  const selectedRosterEntry = roster.find((entry) => entry.id === selectedRosterEntryId)
  const selectedUnit = useMemo(() => {
    if (selectedRosterEntry) {
      const entryArmy = getLocalArmy(selectedRosterEntry.factionId)
      return entryArmy?.units?.find((unit) => unit.no === selectedRosterEntry.unitNo) ?? null
    }

    return (
      army?.units?.find((unit) => unit.no === (selectedUnitNo ?? army?.units?.[0]?.no)) ?? null
    )
  }, [selectedRosterEntry, army, selectedUnitNo])
  const activeUnitNo = selectedUnit?.no
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

  const exportArmySource: ArmyExportSource | null =
    roster.length > 0 || armyCards.length > 0
      ? (() => {
          const factionMeta = deriveSavedArmyFactionMeta(roster, armyCards, {
            factionId: activeFactionId ?? '',
            factionName: army?.faction ?? '',
          })
          return {
            name: armyName.trim() || 'Untitled Army',
            factionId: factionMeta.factionId,
            factionName: factionMeta.factionName,
            totalPoints,
            updatedAt: new Date().toISOString(),
            roster,
            cards: armyCards,
          }
        })()
      : null
  const showRosterFactions = rosterHasMultipleFactions(roster)
  const rosterUnitsByEntryId = useMemo(
    () => buildRosterUnitsByEntryId(roster, activeFactionId ?? ''),
    [roster, activeFactionId],
  )
  const error = factionsError || armyError || cardsError
  const cardsPanelTitle = selectedCardFac ? `${selectedCardFac} Cards` : 'All Cards'

  function handleAddProfile(unit: Unit, profile: UnitProfile) {
    if (!activeFactionId) {
      return
    }

    const entry = createRosterEntry(unit, profile, {
      factionId: activeFactionId,
      factionName: army?.faction ?? '',
    })
    setRoster((current) => [...current, entry])
    setSelectedRosterEntryId(entry.id)
    setSelectedUnitNo(unit.no)
    setIsEditingRosterEntry(true)
    setSaveMessage(null)
  }

  function handleSelectRosterEntry(entry: RosterEntry) {
    setSelectedFactionId(entry.factionId)
    setSelectedRosterEntryId(entry.id)
    setSelectedUnitNo(entry.unitNo)
    setIsEditingRosterEntry(true)
    setBuildMode('army')
    if (isMobile) {
      setMobilePanel('detail', {
        data: { unitNo: entry.unitNo, rosterEntryId: entry.id, fromRoster: true },
      })
    }
  }

  function handleToggleOption(
    optionIndex: number,
    option: UnitOption,
    context: OptionToggleContext = {},
  ) {
    if (!selectedRosterEntry || !selectedUnit) {
      return
    }
    if (selectedRosterEntry.unitNo !== selectedUnit.no) {
      return
    }

    const profileStats = getProfileStatsForEntry(selectedUnit, selectedRosterEntry)
    const summary = summarizeOption(option, profileStats, true)
    const chooseOneChoices = getChooseOneChoices(option)
    const choiceIndex = context.choiceIndex ?? context.slotIndex
    if (chooseOneChoices.length > 0 && choiceIndex != null) {
      summary.text = chooseOneChoices[choiceIndex] ?? summary.text
    }

    setRoster((current) =>
      current.map((entry) =>
        entry.id === selectedRosterEntry.id
          ? toggleRosterOption(
              entry,
              optionIndex,
              summary,
              selectedUnit.options ?? [],
              context,
            )
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

  function handleAddBaseCards() {
    setArmyCards((current) => {
      const existingIds = new Set(current.map((entry) => entry.cardId))
      const toAdd = baseApocCards
        .filter((card) => !existingIds.has(card.id))
        .map(createArmyCardEntry)
      if (toAdd.length === 0) {
        return current
      }
      return [...current, ...toAdd]
    })
    setSaveMessage(null)
  }

  function handleSelectCard(card: Card) {
    setSelectedCardId(card.id)
    cardDetailRefs.current.get(card.id)?.scrollIntoView({ behavior: 'smooth', block: 'start' })
    if (isMobile) {
      setMobilePanel('detail', { data: { cardId: card.id } })
    }
  }

  function handleClearRoster() {
    setRoster([])
    setArmyCards([])
    setArmyName('')
    setEditingArmyId(null)
    setSelectedRosterEntryId(null)
    setIsEditingRosterEntry(false)
    setSelectedCardId(null)
    setSaveMessage(null)
  }

  function handleSaveArmy(source: 'top' | 'bottom' = 'bottom') {
    const trimmedName = armyName.trim()
    if (!trimmedName) {
      setSaveMessage({ type: 'error', text: 'Enter a name before saving.', target: source })
      return
    }
    if (!activeFactionId || (roster.length === 0 && armyCards.length === 0)) {
      setSaveMessage({
        type: 'error',
        text: 'Add at least one unit or card before saving.',
        target: source,
      })
      return
    }

    const factionMeta = deriveSavedArmyFactionMeta(roster, armyCards, {
      factionId: activeFactionId,
      factionName: army?.faction ?? '',
    })

    const payload: SavedArmy = {
      id: editingArmyId ?? crypto.randomUUID(),
      name: trimmedName,
      factionId: factionMeta.factionId,
      factionName: factionMeta.factionName,
      totalPoints,
      updatedAt: new Date().toISOString(),
      roster,
      cards: armyCards,
    }

    const result = saveArmy(payload)
    if (!result.ok) {
      setSaveMessage({
        type: 'error',
        text: result.error ?? 'Failed to save army.',
        target: source,
      })
      return
    }

    setSavedArmies(result.armies ?? [])
    setEditingArmyId(payload.id)
    onToast('Successfully saved')
  }

  function handleLoadArmy(saved: SavedArmy, options?: { silent?: boolean }) {
    setSelectedFactionId(saved.roster[0]?.factionId ?? saved.factionId)
    setArmyName(saved.name)
    setEditingArmyId(saved.id)
    setRoster(saved.roster)
    setArmyCards(saved.cards ?? [])
    setSelectedRosterEntryId(saved.roster[0]?.id ?? null)
    setSelectedUnitNo(saved.roster[0]?.unitNo ?? null)
    if (!options?.silent) {
      onToast(`Loaded "${saved.name}".`)
    }
  }

  function handleDeleteArmy(id: string) {
    const next = deleteSavedArmy(id)
    setSavedArmies(next)
    if (editingArmyId === id) {
      handleClearRoster()
      navigate({ to: '/build', search: {} })
    }
    setArmyToDelete(null)
    setSaveMessage({ type: 'success', text: 'Saved army deleted.' })
  }

  function startNewArmy() {
    handleClearRoster()
    setImportError(null)
    navigate({ to: '/build', search: {} })
  }

  function handleNewArmyClick() {
    if (hasArmyDraft) {
      setConfirmNewArmyOpen(true)
      return
    }
    startNewArmy()
  }

  function handleSortRoster() {
    setRoster((current) => sortRosterByOrganizeGroup(current))
    setArmyCards((current) => sortArmyCardsByName(current))
    setSaveMessage(null)
  }

  function handleExportArmy() {
    if (!exportArmySource) {
      setSaveMessage({ type: 'error', text: 'Add at least one unit or card before exporting.' })
      return
    }
    setExportArmyOpen(true)
  }

  function handleImportArmy(code: string) {
    const result = importAndSaveArmyFromCode(code, savedArmies.length)
    if (!result.ok) {
      setImportError(result.error ?? 'Could not import army.')
      return
    }

    const armies = loadSavedArmies()
    setSavedArmies(armies)
    handleLoadArmy(result.army, { silent: true })
    setImportArmyOpen(false)
    setImportError(null)
    onToast('Successfully imported')
    navigate({ to: '/build', search: { armyId: result.army.id } })
  }

  const mobileBuildClass = isMobile
    ? `build-body mobile-layout mobile-panel-${mobilePanel}`
    : 'build-body'

  function handleMobileBack() {
    if (mobilePanel === 'detail') {
      exitRosterEditMode()
    }
    goBackMobilePanel()
  }

  function handleMobileToggleView() {
    if (mobilePanel === 'roster') {
      goBackMobilePanel()
      return
    }
    setMobilePanel('roster')
  }

  const editingRosterEntry = Boolean(isEditingRosterEntry && canEditOptions)
  const editingFromRoster = Boolean(isMobile && mobilePanel === 'detail' && editingRosterEntry)

  return (
    <>
      <header className="app-header">
        <div>
          <p className="eyebrow">Apocalypse · Vanguard</p>
          <h1>Build Army</h1>
        </div>
        <div className="header-actions">
          <div className="header-button-row">
            <button type="button" className="secondary-btn" onClick={handleNewArmyClick}>
              New
            </button>
            <button type="button" className="secondary-btn" onClick={() => {
              setImportError(null)
              setImportArmyOpen(true)
            }}>
              Import
            </button>
            <button type="button" className="secondary-btn" onClick={handleExportArmy}>
              Export
            </button>
            <button
              type="button"
              className="secondary-btn icon-btn"
              onClick={handleSortRoster}
              aria-label="Sort army roster"
              title="Sort by group, faction, commander, then name"
            >
              ↕
            </button>
          </div>
        </div>
      </header>

      {error && <p className="error-banner">{error}</p>}

      {isMobile && (
        <BuildArmyMobileBar
          mobilePanel={mobilePanel}
          totalPoints={totalPoints}
          unitCount={roster.length}
          cardCount={armyCards.length}
          onBack={handleMobileBack}
          onToggleView={handleMobileToggleView}
        />
      )}

      <div className={mobileBuildClass}>
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
                        <span className="faction-btn-label">
                          <FactionIcon name={faction.faction} />
                          <span className="faction-name">{faction.faction}</span>
                        </span>
                        <span className="faction-count">{faction.unitCount}</span>
                      </button>
                    </li>
                  ))}
                </ul>
              )}

              <div className="sidebar-section-header">
                <h2 className="sidebar-section-title">Cards</h2>
                <button
                  type="button"
                  className="secondary-btn sidebar-action-btn"
                  onClick={handleAddBaseCards}
                  disabled={loadingCards || baseApocCards.length === 0 || allBaseCardsAdded}
                >
                  Add base
                </button>
              </div>
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
                        <span className="faction-btn-label">
                          <FactionIcon name={fac} />
                          <span className="faction-name">{fac}</span>
                        </span>
                        <span className="faction-count">{count}</span>
                      </button>
                    </li>
                  ))}
                </ul>
              )}
            </aside>

            <section className="unit-panel">
              <div className="unit-panel-toolbar">
                <FactionPanelTitle
                  title={buildMode === 'cards' ? cardsPanelTitle : (army?.faction ?? 'Units')}
                  factionName={buildMode === 'cards' ? selectedCardFac : army?.faction}
                />
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
                        <UnitGroupHeading type={type} />
                        <ul className="unit-list">
                          {units.map((unit) => (
                            <li key={unit.no}>
                              <button
                                type="button"
                                className={
                                  unit.no === activeUnitNo ? 'unit-btn active' : 'unit-btn'
                                }
                                onClick={() => handleSelectUnitFromList(unit.no)}
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
                  onToggleOption={editingRosterEntry ? handleToggleOption : undefined}
                  selectedOptionIndexes={
                    editingRosterEntry
                      ? selectedRosterEntry!.selectedOptions.map((option) => option.index)
                      : []
                  }
                  selectedOptions={
                    editingRosterEntry ? selectedRosterEntry!.selectedOptions : []
                  }
                  optionProfileStats={optionProfileStats}
                  emptyMessage={
                    editingFromRoster
                      ? 'Loading unit datasheet…'
                      : 'Select a unit to add profiles to your army.'
                  }
                  showProfileAddButtons={!editingFromRoster}
                  activeProfile={
                    editingFromRoster && selectedRosterEntry
                      ? {
                          kind: selectedRosterEntry.profileKind,
                          index: selectedRosterEntry.profileIndex,
                          label: selectedRosterEntry.profileLabel,
                        }
                      : null
                  }
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

          <div className="roster-actions roster-actions-top">
            <button type="button" className="primary-btn" onClick={() => handleSaveArmy('top')}>
              Save Army
            </button>
            <button
              type="button"
              className="secondary-btn organize-army-btn"
              disabled={roster.length === 0}
              onClick={() => setOrganizeArmyOpen(true)}
            >
              Organize
            </button>
          </div>
          {saveMessage?.type === 'error' && saveMessage.target === 'top' && (
            <p className="form-error roster-save-error-top">{saveMessage.text}</p>
          )}

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
                  {roster.map((entry) => (
                    <RosterEntrySummary
                      key={entry.id}
                      entry={entry}
                      showFaction={showRosterFactions}
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
              {sortedArmyCards.length > 0 && (
                <ul className="roster-list">
                  {sortedArmyCards.map((entry) => (
                    <ArmyCardSummary key={entry.id} entry={entry} onRemove={handleRemoveCard} />
                  ))}
                </ul>
              )}
            </>
          )}

          <div className="roster-actions roster-actions-bottom">
            <button type="button" className="primary-btn" onClick={() => handleSaveArmy('bottom')}>
              Save Army
            </button>
            <button
              type="button"
              className="secondary-btn organize-army-btn"
              disabled={roster.length === 0}
              onClick={() => setOrganizeArmyOpen(true)}
            >
              Organize
            </button>
          </div>

          {saveMessage && !(saveMessage.type === 'error' && saveMessage.target === 'top') && (
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
                        onClick={() => setArmyToDelete(saved)}
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

      {confirmNewArmyOpen && (
        <ConfirmModal
          title="Start a new army?"
          message="Any unsaved changes to the current army will be lost."
          confirmLabel="New"
          danger
          onConfirm={() => {
            setConfirmNewArmyOpen(false)
            startNewArmy()
          }}
          onCancel={() => setConfirmNewArmyOpen(false)}
        />
      )}

      {armyToDelete && (
        <ConfirmModal
          title="Delete saved army?"
          message={`Delete "${armyToDelete.name}"? This cannot be undone.`}
          confirmLabel="Delete"
          danger
          onConfirm={() => handleDeleteArmy(armyToDelete.id)}
          onCancel={() => setArmyToDelete(null)}
        />
      )}

      {importArmyOpen && (
        <ImportArmyModal
          error={importError}
          onClose={() => {
            setImportArmyOpen(false)
            setImportError(null)
          }}
          onImport={handleImportArmy}
        />
      )}

      {exportArmyOpen && exportArmySource && (
        <ExportArmyModal
          army={exportArmySource}
          unitsByEntryId={rosterUnitsByEntryId}
          onClose={() => setExportArmyOpen(false)}
        />
      )}

      {organizeArmyOpen && (
        <OrganizeArmyModal
          roster={roster}
          unitsByEntryId={rosterUnitsByEntryId}
          showFaction={showRosterFactions}
          onRosterChange={(nextRoster) => {
            setRoster(nextRoster)
            setSaveMessage(null)
          }}
          onClose={() => setOrganizeArmyOpen(false)}
        />
      )}
    </>
  )
}
