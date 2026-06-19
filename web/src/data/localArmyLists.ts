import type { ArmyList, FactionSummary } from '../types'

const armyListModules = import.meta.glob<ArmyList>('../ArmyLists/*.json', {
  eager: true,
  import: 'default',
})

function factionIdFromPath(filePath: string): string {
  const filename = filePath.split('/').pop() ?? ''
  return filename.replace(/\.json$/, '')
}

const armyListsById = new Map<string, ArmyList>(
  Object.entries(armyListModules).map(([path, data]) => [factionIdFromPath(path), data]),
)

export function getLocalFactions(): FactionSummary[] {
  return [...armyListsById.entries()]
    .map(([id, data]) => ({
      id,
      faction: data.faction,
      source: data.source,
      unitCount: data.units?.length ?? 0,
    }))
    .sort((a, b) => a.faction.localeCompare(b.faction))
}

export function getLocalArmy(factionId: string): ArmyList | null {
  return armyListsById.get(factionId) ?? null
}
