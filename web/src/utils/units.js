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
