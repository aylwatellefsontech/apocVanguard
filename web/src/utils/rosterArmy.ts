import type { ArmyCardEntry, RosterEntry } from '../types'

export function sortRosterByFactionAndName(roster: RosterEntry[]): RosterEntry[] {
  return [...roster].sort((a, b) => {
    const factionCompare = (a.factionName ?? '').localeCompare(b.factionName ?? '')
    if (factionCompare !== 0) {
      return factionCompare
    }
    return a.unitName.localeCompare(b.unitName)
  })
}

export function getRosterFactionIds(roster: RosterEntry[]): string[] {
  return [...new Set(roster.map((entry) => entry.factionId).filter(Boolean))]
}

export function rosterHasMultipleFactions(roster: RosterEntry[]): boolean {
  return getRosterFactionIds(roster).length > 1
}

export function getArmyFactionNames(
  roster: RosterEntry[],
  cards: ArmyCardEntry[] = [],
  fallbackFactionName = '',
): string[] {
  const factions = new Map<string, string>()

  for (const entry of roster) {
    const name = entry.factionName?.trim()
    if (name) {
      factions.set(entry.factionId || name, name)
    }
  }

  if (factions.size === 0) {
    for (const card of cards) {
      const name = card.fac?.trim()
      if (name) {
        factions.set(name, name)
      }
    }
  }

  if (factions.size === 0 && fallbackFactionName.trim()) {
    for (const part of fallbackFactionName.split('/').map((name) => name.trim()).filter(Boolean)) {
      factions.set(part, part)
    }
  }

  return [...factions.values()].sort((a, b) => a.localeCompare(b))
}

export function deriveSavedArmyFactionMeta(
  roster: RosterEntry[],
  cards: ArmyCardEntry[],
  fallback: { factionId: string; factionName: string },
): { factionId: string; factionName: string } {
  const factions = new Map<string, string>()

  for (const entry of roster) {
    const factionId = entry.factionId || fallback.factionId
    const factionName = entry.factionName || fallback.factionName
    if (factionId && factionName) {
      factions.set(factionId, factionName)
    }
  }

  if (factions.size === 0) {
    if (cards.length > 0) {
      const cardFactions = [...new Set(cards.map((card) => card.fac).filter(Boolean))].sort(
        (a, b) => a.localeCompare(b),
      )
      if (cardFactions.length > 0) {
        return {
          factionId: fallback.factionId,
          factionName:
            cardFactions.length > 1 ? cardFactions.join(' / ') : cardFactions[0] ?? fallback.factionName,
        }
      }
    }
    return fallback
  }

  const sorted = [...factions.entries()].sort((a, b) => a[1].localeCompare(b[1]))
  if (sorted.length === 1) {
    return { factionId: sorted[0][0], factionName: sorted[0][1] }
  }

  return {
    factionId: sorted[0][0],
    factionName: sorted.map(([, name]) => name).join(' / '),
  }
}
