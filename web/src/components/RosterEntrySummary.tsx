import { formatRosterEntryMeta } from '../utils/roster'
import RosterOrganizeBadges from './RosterOrganizeBadges'
import type { RosterEntry } from '../types'
interface RosterEntrySummaryProps {
  entry: RosterEntry
  showFaction?: boolean
  active?: boolean
  onSelect?: (entry: RosterEntry) => void
  onRemove?: (entryId: string) => void
  showOrganizeBadges?: boolean
}

export default function RosterEntrySummary({
  entry,
  showFaction = false,
  active = false,
  onSelect,
  onRemove,
  showOrganizeBadges = true,
}: RosterEntrySummaryProps) {
  const titleRow = (
    <div className="roster-item-title-row">
      <strong>{entry.unitName}</strong>
      {showOrganizeBadges ? <RosterOrganizeBadges entry={entry} /> : null}
    </div>
  )
  return (
    <li className={active ? 'roster-item active' : 'roster-item'}>
      {onSelect ? (
        <button type="button" className="roster-item-main" onClick={() => onSelect(entry)}>
          {titleRow}
          <p className="roster-item-meta">{formatRosterEntryMeta(entry, showFaction)}</p>
          {entry.selectedOptions?.length > 0 && (
            <ul className="roster-option-list">
              {entry.selectedOptions.map((option) => (
                <li
                  key={`${option.index}-${option.modelIndex ?? 'unit'}-${option.slotIndex ?? 'slot'}-${option.choiceIndex ?? 'choice'}`}
                >
                  {option.label}
                  {option.points > 0 ? ` (+${option.points} Pt)` : ''}
                </li>
              ))}
            </ul>
          )}
        </button>
      ) : (
        <div className="roster-item-main">
          {titleRow}
          <p className="roster-item-meta">{formatRosterEntryMeta(entry, showFaction)}</p>
          {entry.unitType && <p className="roster-item-meta">{entry.unitType}</p>}
          {entry.selectedOptions?.length > 0 && (
            <ul className="roster-option-list">
              {entry.selectedOptions.map((option) => (
                <li
                  key={`${option.index}-${option.modelIndex ?? 'unit'}-${option.slotIndex ?? 'slot'}-${option.choiceIndex ?? 'choice'}`}
                >
                  {option.label}: {option.text}
                  {option.points > 0 ? ` (+${option.points} Pt)` : ''}
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
      {onRemove && (
        <button type="button" className="text-btn" onClick={() => onRemove(entry.id)}>
          Remove
        </button>
      )}
    </li>
  )
}
