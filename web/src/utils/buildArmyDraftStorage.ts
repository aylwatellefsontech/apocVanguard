import { BUILD_ARMY_DRAFT_KEY } from '../constants'
import type { ArmyCardEntry, BrowseMode, RosterEntry, SavedArmy } from '../types'

export const BUILD_ARMY_DRAFT_VERSION = 1

export interface BuildArmyDraft {
  version: typeof BUILD_ARMY_DRAFT_VERSION
  routeArmyId: string | null
  buildMode: BrowseMode
  selectedCardFac: string | null
  selectedFactionId: string | null
  selectedUnitNo: number | null
  selectedRosterEntryId: string | null
  search: string
  roster: RosterEntry[]
  armyCards: ArmyCardEntry[]
  selectedCardId: string | null
  armyName: string
  editingArmyId: string | null
}

export function emptyBuildArmyDraft(routeArmyId: string | null): BuildArmyDraft {
  return {
    version: BUILD_ARMY_DRAFT_VERSION,
    routeArmyId,
    buildMode: 'army',
    selectedCardFac: null,
    selectedFactionId: null,
    selectedUnitNo: null,
    selectedRosterEntryId: null,
    search: '',
    roster: [],
    armyCards: [],
    selectedCardId: null,
    armyName: '',
    editingArmyId: null,
  }
}

export function buildArmyDraftFromSaved(
  saved: SavedArmy,
  routeArmyId: string | null,
): BuildArmyDraft {
  return {
    version: BUILD_ARMY_DRAFT_VERSION,
    routeArmyId,
    buildMode: 'army',
    selectedCardFac: null,
    selectedFactionId: saved.factionId,
    selectedUnitNo: saved.roster[0]?.unitNo ?? null,
    selectedRosterEntryId: saved.roster[0]?.id ?? null,
    search: '',
    roster: saved.roster,
    armyCards: saved.cards ?? [],
    selectedCardId: null,
    armyName: saved.name,
    editingArmyId: saved.id,
  }
}

function isBuildArmyDraft(value: unknown): value is BuildArmyDraft {
  if (!value || typeof value !== 'object') {
    return false
  }
  const draft = value as BuildArmyDraft
  return (
    draft.version === BUILD_ARMY_DRAFT_VERSION &&
    Array.isArray(draft.roster) &&
    Array.isArray(draft.armyCards)
  )
}

export function loadBuildArmyDraft(): BuildArmyDraft | null {
  try {
    const raw = sessionStorage.getItem(BUILD_ARMY_DRAFT_KEY)
    if (!raw) {
      return null
    }
    const parsed: unknown = JSON.parse(raw)
    return isBuildArmyDraft(parsed) ? parsed : null
  } catch {
    return null
  }
}

export function saveBuildArmyDraft(draft: BuildArmyDraft): void {
  try {
    sessionStorage.setItem(BUILD_ARMY_DRAFT_KEY, JSON.stringify(draft))
  } catch {
    // ignore quota / private mode
  }
}

export function clearBuildArmyDraft(): void {
  try {
    sessionStorage.removeItem(BUILD_ARMY_DRAFT_KEY)
  } catch {
    // ignore
  }
}

/** Pick session draft vs saved army for this route visit. */
export function resolveBuildArmyInitialState(
  routeArmyId: string | undefined,
  savedArmy: SavedArmy | null,
): BuildArmyDraft {
  const routeKey = routeArmyId ?? null
  const draft = loadBuildArmyDraft()

  if (draft && draft.routeArmyId === routeKey) {
    return draft
  }

  if (savedArmy) {
    return buildArmyDraftFromSaved(savedArmy, routeKey)
  }

  return emptyBuildArmyDraft(routeKey)
}
