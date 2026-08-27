import type { RosterEntry } from '../types'

export function formatRosterEntryMeta(entry: RosterEntry, showFaction = false): string {
  const parts: string[] = []

  if (showFaction && entry.factionName) {
    parts.push(entry.factionName)
  }

  parts.push(entry.profileLabel)

  if (entry.modelCount != null && entry.modelCount !== '') {
    parts.push(`N ${entry.modelCount}`)
  }

  parts.push(`${entry.points} Pt`)
  return parts.join(' · ')
}
