import { TYPE_ORDER } from '../constants'
import type { RosterEntry, Unit } from '../types'
import { formatRosterEntryMeta } from './roster'
import { getRosterEntryWeightKeyword } from './units'

export const CARD_SLOT_COUNT = 6

export const CARD_SLOT_NUMBERS = [1, 2, 3, 4, 5, 6] as const

export type CardSlotNumber = (typeof CARD_SLOT_NUMBERS)[number]

const UNASSIGNED_CARD_SLOT = Number.MAX_SAFE_INTEGER

const TYPE_RANK = new Map(TYPE_ORDER.map((type, index) => [type, index]))

export function isValidCardSlot(value: unknown): value is CardSlotNumber {
  return typeof value === 'number' && Number.isInteger(value) && value >= 1 && value <= CARD_SLOT_COUNT
}

export function rosterIsOrganized(roster: RosterEntry[]): boolean {
  return roster.some((entry) => entry.cardSlot != null)
}

function getCardSlotSortValue(entry: RosterEntry): number {
  return entry.cardSlot ?? UNASSIGNED_CARD_SLOT
}

function compareCommanderFirst(a: RosterEntry, b: RosterEntry): number {
  const rankA = a.isCommander ? 0 : 1
  const rankB = b.isCommander ? 0 : 1
  return rankA - rankB
}

function compareUnitType(a: RosterEntry, b: RosterEntry): number {
  const rankA = TYPE_RANK.get(a.unitType as (typeof TYPE_ORDER)[number]) ?? TYPE_ORDER.length
  const rankB = TYPE_RANK.get(b.unitType as (typeof TYPE_ORDER)[number]) ?? TYPE_ORDER.length
  return rankA - rankB
}

function compareOrganizedRoster(
  a: RosterEntry,
  b: RosterEntry,
  includeUnitType: boolean,
): number {
  const slotCompare = getCardSlotSortValue(a) - getCardSlotSortValue(b)
  if (slotCompare !== 0) {
    return slotCompare
  }

  const factionCompare = (a.factionName ?? '').localeCompare(b.factionName ?? '')
  if (factionCompare !== 0) {
    return factionCompare
  }

  const commanderCompare = compareCommanderFirst(a, b)
  if (commanderCompare !== 0) {
    return commanderCompare
  }

  if (includeUnitType) {
    const typeCompare = compareUnitType(a, b)
    if (typeCompare !== 0) {
      return typeCompare
    }
  }

  return a.unitName.localeCompare(b.unitName)
}

/** Sort for Build Army and the organize modal: group, faction, commander, name. */
export function sortRosterByOrganizeGroup(roster: RosterEntry[]): RosterEntry[] {
  return [...roster].sort((a, b) => compareOrganizedRoster(a, b, false))
}

/** Sort for My Armies when units are assigned to card slots. */
export function sortRosterForOrganizedArmyView(roster: RosterEntry[]): RosterEntry[] {
  return [...roster].sort((a, b) => compareOrganizedRoster(a, b, true))
}

export function formatOrganizeEntryMeta(
  entry: RosterEntry,
  unit: Unit | null | undefined,
  showFaction = false,
): string {
  const parts: string[] = []

  if (showFaction && entry.factionName) {
    parts.push(entry.factionName)
  }

  if (entry.unitType) {
    parts.push(entry.unitType)
  }

  const weight = getRosterEntryWeightKeyword(unit, entry)
  if (weight) {
    parts.push(weight)
  }

  parts.push(entry.profileLabel)

  if (entry.modelCount != null && entry.modelCount !== '') {
    parts.push(`N ${entry.modelCount}`)
  }

  parts.push(`${entry.points} Pt`)

  return parts.join(' · ')
}

export function formatDetachmentLabel(cardSlot: number): string {
  return `Detachment ${cardSlot}`
}

export function formatPrintOrganizeMeta(entry: RosterEntry): string {
  const parts: string[] = []

  if (entry.cardSlot != null) {
    parts.push(formatDetachmentLabel(entry.cardSlot))
  }

  if (entry.isCommander) {
    parts.push('Commander')
  }

  return parts.join(' · ')
}

export function formatPrintRosterEntryMeta(entry: RosterEntry, showFaction = false): string {
  const parts: string[] = []
  const organizeMeta = formatPrintOrganizeMeta(entry)

  if (organizeMeta) {
    parts.push(organizeMeta)
  }

  parts.push(formatRosterEntryMeta(entry, showFaction))

  if (entry.unitType) {
    parts.push(entry.unitType)
  }

  return parts.join(' · ')
}

export function assignRosterCardSlot(
  roster: RosterEntry[],
  entryId: string,
  cardSlot: number | null,
): RosterEntry[] {
  if (cardSlot != null && !isValidCardSlot(cardSlot)) {
    return roster
  }

  return roster.map((entry) => {
    if (entry.id !== entryId) {
      return entry
    }

    if (cardSlot == null) {
      return { ...entry, cardSlot: undefined, isCommander: false }
    }

    return {
      ...entry,
      cardSlot,
      isCommander: entry.cardSlot === cardSlot ? Boolean(entry.isCommander) : false,
    }
  })
}

export function toggleRosterCommander(roster: RosterEntry[], entryId: string): RosterEntry[] {
  const target = roster.find((entry) => entry.id === entryId)
  if (!target?.cardSlot) {
    return roster
  }

  if (target.isCommander) {
    return roster.map((entry) =>
      entry.id === entryId ? { ...entry, isCommander: false } : entry,
    )
  }

  return roster.map((entry) => {
    if (entry.id === entryId) {
      return { ...entry, isCommander: true }
    }
    if (entry.cardSlot === target.cardSlot && entry.isCommander) {
      return { ...entry, isCommander: false }
    }
    return entry
  })
}

export function getRosterEntriesForCardSlot(
  roster: RosterEntry[],
  cardSlot: number,
): RosterEntry[] {
  return roster.filter((entry) => entry.cardSlot === cardSlot)
}

export function normalizeRosterOrganizeFields(entry: RosterEntry): RosterEntry {
  const cardSlot = isValidCardSlot(entry.cardSlot) ? entry.cardSlot : undefined
  const isCommander = cardSlot ? Boolean(entry.isCommander) : false

  return {
    ...entry,
    cardSlot,
    isCommander,
  }
}

export function dedupeRosterCommanders(roster: RosterEntry[]): RosterEntry[] {
  const commanderIds = new Set<string>()

  return roster.map((entry) => {
    if (!entry.isCommander || !entry.cardSlot) {
      return entry.isCommander ? { ...entry, isCommander: false } : entry
    }

    const slotKey = String(entry.cardSlot)
    if (commanderIds.has(slotKey)) {
      return { ...entry, isCommander: false }
    }

    commanderIds.add(slotKey)
    return entry
  })
}
