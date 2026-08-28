import { readdirSync, readFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'
import type { ArmyList, FactionSummary } from '../../src/types'

const testDir = dirname(fileURLToPath(import.meta.url))
const armyListsDir = join(testDir, '../../src/ArmyLists')

const armyListsById = new Map<string, ArmyList>(
  readdirSync(armyListsDir)
    .filter((file) => file.endsWith('.json'))
    .map((file) => {
      const id = file.replace(/\.json$/, '')
      const data = JSON.parse(readFileSync(join(armyListsDir, file), 'utf8')) as ArmyList
      return [id, data]
    }),
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
