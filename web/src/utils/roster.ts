import type { RosterEntry } from '../types'

export function formatRosterEntryMeta(entry: RosterEntry): string {
  const parts = [entry.profileLabel]

  if (entry.modelCount != null && entry.modelCount !== '') {
    parts.push(`N ${entry.modelCount}`)
  }

  parts.push(`${entry.points} Pt`)
  return parts.join(' · ')
}
