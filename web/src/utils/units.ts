import { TYPE_ORDER } from '../constants'
import type { RosterEntry, Unit, UnitProfile, UnitStats } from '../types'

export function parsePoints(stats: UnitStats | undefined): number {
  const value = Number.parseInt(stats?.Pt ?? '', 10)
  return Number.isFinite(value) ? value : 0
}

export function getUnitProfiles(unit: Unit | null | undefined): UnitProfile[] {
  if (!unit) return []

  const profiles: UnitProfile[] = []

  if (unit.stats) {
    profiles.push({
      kind: 'primary',
      index: 0,
      label: 'Primary Profile',
      stats: unit.stats,
      points: parsePoints(unit.stats),
    })
  }

  unit.profiles?.forEach((stats, index) => {
    profiles.push({
      kind: 'alt',
      index,
      label: `Alt Profile ${index + 1}`,
      stats,
      points: parsePoints(stats),
    })
  })

  return profiles
}

export function groupUnitsByType(units: Unit[]): [string, Unit[]][] {
  const groups = new Map<string, Unit[]>()
  for (const unit of units) {
    const list = groups.get(unit.type) ?? []
    list.push(unit)
    groups.set(unit.type, list)
  }

  const orderedTypes = [
    ...TYPE_ORDER.filter((type) => groups.has(type)),
    ...[...groups.keys()].filter((type) => !TYPE_ORDER.includes(type as (typeof TYPE_ORDER)[number])),
  ]

  return orderedTypes.map((type) => [type, groups.get(type)!])
}

export function sortRosterByType(roster: RosterEntry[]): RosterEntry[] {
  const typeRank = new Map(TYPE_ORDER.map((type, index) => [type, index]))

  return [...roster].sort((a, b) => {
    const rankA = typeRank.get(a.unitType as (typeof TYPE_ORDER)[number]) ?? TYPE_ORDER.length
    const rankB = typeRank.get(b.unitType as (typeof TYPE_ORDER)[number]) ?? TYPE_ORDER.length
    if (rankA !== rankB) {
      return rankA - rankB
    }
    return a.unitName.localeCompare(b.unitName)
  })
}

export function getProfileStatsForEntry(
  unit: Unit | null | undefined,
  entry: RosterEntry | null | undefined,
): UnitStats | null {
  if (!unit || !entry) {
    return null
  }

  if (entry.profileKind === 'primary') {
    return unit.stats ?? null
  }

  return unit.profiles?.[entry.profileIndex] ?? null
}

export function isProfileSelected(profile: UnitProfile, entry: RosterEntry | null | undefined): boolean {
  if (!entry) {
    return false
  }

  return profile.kind === entry.profileKind && profile.index === entry.profileIndex
}

export function unitHasInfantryKeyword(unit: Unit | null | undefined): boolean {
  return unit?.keywords?.some((keyword) => keyword.toLowerCase() === 'infantry') ?? false
}

export function formatUnitTypeLabel(type: string, unit?: Unit | null): string {
  if (unitHasInfantryKeyword(unit)) {
    return `${type} - Infantry`
  }

  return type
}
