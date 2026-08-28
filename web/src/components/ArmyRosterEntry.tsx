import { formatRosterEntryMeta } from '../utils/roster'
import RosterEntryDetail from './RosterEntryDetail'
import RosterOrganizeBadges from './RosterOrganizeBadges'
import { formatUnitTypeLabel } from '../utils/units'
import type { RosterEntry, Unit } from '../types'

interface ArmyRosterEntryProps {
  entry: RosterEntry
  unit: Unit | null
  showFaction?: boolean
  expanded: boolean
  onToggleExpanded: () => void
}

export default function ArmyRosterEntry({
  entry,
  unit,
  showFaction = false,
  expanded,
  onToggleExpanded,
}: ArmyRosterEntryProps) {
  return (
    <li className={`roster-item army-roster-entry${expanded ? ' expanded' : ''}`}>
      <button
        type="button"
        className="army-roster-entry-toggle"
        onClick={onToggleExpanded}
        aria-expanded={expanded}
      >
        <span className="roster-expand-icon" aria-hidden="true">
          {expanded ? '▾' : '▸'}
        </span>
        <span className="army-roster-entry-summary">
          <div className="roster-item-title-row">
            <strong>{entry.unitName}</strong>
            <RosterOrganizeBadges entry={entry} />
          </div>
          <span className="roster-item-meta">{formatRosterEntryMeta(entry, showFaction)}</span>
          {entry.unitType && (
            <span className="roster-item-meta">
              {formatUnitTypeLabel(entry.unitType, unit)}
            </span>
          )}
        </span>
      </button>

      {expanded ? <RosterEntryDetail entry={entry} unit={unit} /> : null}
    </li>
  )
}
