import { TYPE_ORDER } from '../constants.js'

export function parsePoints(stats) {
  const value = Number.parseInt(stats?.Pt ?? '', 10)
  return Number.isFinite(value) ? value : 0
}

export function getUnitProfiles(unit) {
  if (!unit) return []

  const profiles = []

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

export function groupUnitsByType(units) {
  const groups = new Map()
  for (const unit of units) {
    const list = groups.get(unit.type) ?? []
    list.push(unit)
    groups.set(unit.type, list)
  }

  const orderedTypes = [
    ...TYPE_ORDER.filter((type) => groups.has(type)),
    ...[...groups.keys()].filter((type) => !TYPE_ORDER.includes(type)),
  ]

  return orderedTypes.map((type) => [type, groups.get(type)])
}

export function sortRosterByType(roster) {
  const typeRank = new Map(TYPE_ORDER.map((type, index) => [type, index]))

  return [...roster].sort((a, b) => {
    const rankA = typeRank.get(a.unitType) ?? TYPE_ORDER.length
    const rankB = typeRank.get(b.unitType) ?? TYPE_ORDER.length
    if (rankA !== rankB) {
      return rankA - rankB
    }
    return a.unitName.localeCompare(b.unitName)
  })
}

export function getProfileStatsForEntry(unit, entry) {
  if (!unit || !entry) {
    return null
  }

  if (entry.profileKind === 'primary') {
    return unit.stats ?? null
  }

  return unit.profiles?.[entry.profileIndex] ?? null
}

export function isProfileSelected(profile, entry) {
  if (!entry) {
    return false
  }

  return profile.kind === entry.profileKind && profile.index === entry.profileIndex
}
