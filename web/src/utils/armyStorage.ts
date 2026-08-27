import { MAX_SAVED_ARMIES, SAVED_ARMIES_KEY } from '../constants'
import type {
  ArmyCardEntry,
  Card,
  OptionToggleContext,
  RosterEntry,
  SaveArmyResult,
  SavedArmy,
  SelectedOption,
  Unit,
  UnitOption,
  UnitProfile,
} from '../types'
import {
  getChooseLimit,
  getOptionGroup,
  getUpToLimit,
  isExclusiveGroupOption,
  isPerModelOption,
  isPerModelsOption,
  optionUsesSlotIndex,
} from './optionUtils'

export function loadSavedArmies(): SavedArmy[] {
  try {
    const raw = localStorage.getItem(SAVED_ARMIES_KEY)
    if (!raw) return []
    const parsed: unknown = JSON.parse(raw)
    return Array.isArray(parsed) ? parsed.map(normalizeSavedArmy) : []
  } catch {
    return []
  }
}

export function normalizeRosterEntry(
  entry: RosterEntry,
  army?: Pick<SavedArmy, 'factionId' | 'factionName'>,
): RosterEntry {
  const profilePoints = entry.profilePoints ?? entry.points ?? 0
  const selectedOptions = Array.isArray(entry.selectedOptions) ? entry.selectedOptions : []
  const optionPoints = selectedOptions.reduce((sum, option) => sum + (option.points ?? 0), 0)

  return {
    ...entry,
    factionId: entry.factionId ?? army?.factionId ?? '',
    factionName: entry.factionName ?? army?.factionName ?? '',
    profilePoints,
    selectedOptions,
    points: profilePoints + optionPoints,
  }
}

export function normalizeSavedArmy(army: SavedArmy): SavedArmy {
  const roster = Array.isArray(army.roster)
    ? army.roster.map((entry) => normalizeRosterEntry(entry, army))
    : []
  const cards = Array.isArray(army.cards) ? army.cards : []
  return {
    ...army,
    roster,
    cards,
    totalPoints: roster.reduce((sum, entry) => sum + entry.points, 0),
  }
}

export function persistSavedArmies(armies: SavedArmy[]): void {
  localStorage.setItem(SAVED_ARMIES_KEY, JSON.stringify(armies))
}

export function saveArmy(army: SavedArmy): SaveArmyResult {
  const armies = loadSavedArmies()
  if (armies.length >= MAX_SAVED_ARMIES && !armies.some((entry) => entry.id === army.id)) {
    return { ok: false, error: `You can only save up to ${MAX_SAVED_ARMIES} armies.` }
  }

  const normalized = normalizeSavedArmy(army)
  const next = armies.some((entry) => entry.id === army.id)
    ? armies.map((entry) => (entry.id === army.id ? normalized : entry))
    : [...armies, normalized]

  persistSavedArmies(next)
  return { ok: true, armies: next }
}

export function deleteSavedArmy(id: string): SavedArmy[] {
  const next = loadSavedArmies().filter((army) => army.id !== id)
  persistSavedArmies(next)
  return next
}

export function createArmyCardEntry(card: Card): ArmyCardEntry {
  return {
    id: crypto.randomUUID(),
    cardId: card.id,
    name: card.name,
    set: card.set,
    nm: card.nm,
    fac: card.fac,
    type: card.type,
    subType: card.subType ?? null,
    facNm: card.facNm ?? null,
    ability: card.ability ?? '',
  }
}

export function sortArmyCardsByName(cards: ArmyCardEntry[]): ArmyCardEntry[] {
  return [...cards].sort((a, b) => a.name.localeCompare(b.name))
}

export function sortArmyCards(cards: ArmyCardEntry[]): ArmyCardEntry[] {
  return [...cards].sort((a, b) => {
    const setCompare = String(a.set ?? '').localeCompare(String(b.set ?? ''))
    if (setCompare !== 0) {
      return setCompare
    }
    return (a.nm ?? 0) - (b.nm ?? 0)
  })
}

export function createRosterEntry(
  unit: Unit,
  profile: UnitProfile,
  faction: { factionId: string; factionName: string },
): RosterEntry {
  return {
    id: crypto.randomUUID(),
    factionId: faction.factionId,
    factionName: faction.factionName,
    unitNo: unit.no,
    unitName: unit.name,
    unitType: unit.type,
    profileKind: profile.kind,
    profileIndex: profile.index,
    profileLabel: profile.label,
    profilePoints: profile.points,
    modelCount: profile.stats?.N ?? null,
    selectedOptions: [],
    points: profile.points,
  }
}

export function toggleRosterOption(
  entry: RosterEntry,
  optionIndex: number,
  optionSummary: Omit<SelectedOption, 'index' | 'modelIndex' | 'slotIndex' | 'choiceIndex'>,
  unitOptions: UnitOption[],
  context: OptionToggleContext = {},
): RosterEntry {
  const { modelIndex, slotIndex, choiceIndex: contextChoiceIndex } = context
  const option = unitOptions[optionIndex]
  const perModel = isPerModelOption(option)
  const perModels = isPerModelsOption(option)
  const upToLimit = getUpToLimit(option)
  const upTo = upToLimit != null
  const slotScoped = optionUsesSlotIndex(option)
  const group = getOptionGroup(option)
  const exclusive = isExclusiveGroupOption(option)
  const chooseLimit = getChooseLimit(option)
  const slottedChoose = chooseLimit != null && (upTo || perModels)
  const choiceIndex =
    contextChoiceIndex ?? (!slottedChoose && chooseLimit != null ? slotIndex : undefined)

  const matches = (selected: SelectedOption) =>
    selected.index === optionIndex &&
    (perModel ? selected.modelIndex === modelIndex : selected.modelIndex == null) &&
    (slotScoped && slotIndex != null
      ? selected.slotIndex === slotIndex
      : slotIndex == null
        ? selected.slotIndex == null
        : selected.slotIndex === slotIndex)

  let selectedOptions = [...entry.selectedOptions]

  if (chooseLimit != null && choiceIndex != null) {
    const instanceSlot = slottedChoose ? slotIndex : undefined
    const matchesChoice = (selected: SelectedOption) =>
      selected.index === optionIndex &&
      (perModel ? selected.modelIndex === modelIndex : selected.modelIndex == null) &&
      (instanceSlot != null
        ? selected.slotIndex === instanceSlot && selected.choiceIndex === choiceIndex
        : selected.choiceIndex != null
          ? selected.choiceIndex === choiceIndex && selected.slotIndex == null
          : selected.slotIndex === choiceIndex)
    const sameInstance = (selected: SelectedOption) =>
      selected.index === optionIndex &&
      (perModel ? selected.modelIndex === modelIndex : selected.modelIndex == null) &&
      (instanceSlot != null ? selected.slotIndex === instanceSlot : true)

    const wasSelected = selectedOptions.some(matchesChoice)
    if (wasSelected) {
      selectedOptions = selectedOptions.filter((selected) => !matchesChoice(selected))
    } else {
      const selectedInGroup = selectedOptions.filter(sameInstance)
      if (selectedInGroup.length >= chooseLimit) {
        const earliest = selectedInGroup[0]
        selectedOptions = selectedOptions.filter((selected) => selected !== earliest)
      }
      selectedOptions.push({
        index: optionIndex,
        modelIndex: perModel ? modelIndex : undefined,
        slotIndex: instanceSlot,
        choiceIndex,
        ...optionSummary,
      })
    }
  } else if (exclusive && group) {
    const wasSelected = selectedOptions.some(matches)

    selectedOptions = selectedOptions.filter((selected) => {
      const selectedOption = unitOptions[selected.index]
      const selectedGroup = getOptionGroup(selectedOption)
      if (!selectedGroup || selectedGroup.toLowerCase() !== group.toLowerCase()) {
        return true
      }
      if (perModel || isPerModelOption(selectedOption)) {
        return selected.modelIndex !== modelIndex
      }
      if (upTo && slotIndex != null) {
        return selected.slotIndex !== slotIndex
      }
      if (perModels && slotIndex != null) {
        return selected.slotIndex !== slotIndex
      }
      return false
    })

    if (!wasSelected) {
      selectedOptions.push({
        index: optionIndex,
        modelIndex: perModel ? modelIndex : undefined,
        slotIndex: slotScoped ? slotIndex : undefined,
        ...optionSummary,
      })
    }
  } else if ((upTo || perModels) && slotIndex != null) {
    const exists = selectedOptions.some(matches)
    selectedOptions = exists
      ? selectedOptions.filter((selected) => !matches(selected))
      : [
          ...selectedOptions,
          {
            index: optionIndex,
            modelIndex: perModel ? modelIndex : undefined,
            slotIndex,
            ...optionSummary,
          },
        ]
  } else {
    const exists = selectedOptions.some(matches)
    selectedOptions = exists
      ? selectedOptions.filter((selected) => !matches(selected))
      : [
          ...selectedOptions,
          {
            index: optionIndex,
            modelIndex: perModel ? modelIndex : undefined,
            ...optionSummary,
          },
        ]
  }

  const optionPoints = selectedOptions.reduce((sum, option) => sum + (option.points ?? 0), 0)

  return {
    ...entry,
    selectedOptions,
    points: entry.profilePoints + optionPoints,
  }
}

export type { UnitOption }
