import { getLocalArmy } from '../data/localArmyLists'
import type { RosterEntry, Unit } from '../types'

export function buildRosterUnitsByEntryId(
  roster: RosterEntry[],
  fallbackFactionId: string,
): Map<string, Unit> {
  const map = new Map<string, Unit>()

  for (const entry of roster) {
    const factionId = entry.factionId || fallbackFactionId
    if (!factionId) {
      continue
    }

    const army = getLocalArmy(factionId)
    const unit = army?.units?.find((candidate) => candidate.no === entry.unitNo)
    if (unit) {
      map.set(entry.id, unit)
    }
  }

  return map
}
