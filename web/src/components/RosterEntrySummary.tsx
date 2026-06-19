import { formatRosterEntryMeta } from '../utils/roster'
import type { RosterEntry } from '../types'

interface RosterEntrySummaryProps {
  entry: RosterEntry
  active?: boolean
  onSelect?: (entry: RosterEntry) => void
  onRemove?: (entryId: string) => void
}

export default function RosterEntrySummary({
  entry,
  active = false,
  onSelect,
  onRemove,
}: RosterEntrySummaryProps) {
  return (
    <li className={active ? 'roster-item active' : 'roster-item'}>
      {onSelect ? (
        <button type="button" className="roster-item-main" onClick={() => onSelect(entry)}>
          <strong>{entry.unitName}</strong>
          <p className="roster-item-meta">{formatRosterEntryMeta(entry)}</p>
          {entry.selectedOptions?.length > 0 && (
            <ul className="roster-option-list">
              {entry.selectedOptions.map((option) => (
                <li key={option.index}>
                  {option.label}
                  {option.points > 0 ? ` (+${option.points} Pt)` : ''}
                </li>
              ))}
            </ul>
          )}
        </button>
      ) : (
        <div className="roster-item-main">
          <strong>{entry.unitName}</strong>
          <p className="roster-item-meta">{formatRosterEntryMeta(entry)}</p>
          {entry.unitType && <p className="roster-item-meta">{entry.unitType}</p>}
          {entry.selectedOptions?.length > 0 && (
            <ul className="roster-option-list">
              {entry.selectedOptions.map((option) => (
                <li key={option.index}>
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
