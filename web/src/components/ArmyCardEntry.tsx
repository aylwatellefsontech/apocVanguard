import type { ArmyCardEntry } from '../types'

interface ArmyCardEntryProps {
  entry: ArmyCardEntry
  expanded: boolean
  onToggleExpanded: () => void
}

export default function ArmyCardEntryComponent({
  entry,
  expanded,
  onToggleExpanded,
}: ArmyCardEntryProps) {
  return (
    <li className={`roster-item army-roster-entry army-card-entry${expanded ? ' expanded' : ''}`}>
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
          <strong>{entry.name}</strong>
          <span className="roster-item-meta">
            {entry.set}-{entry.nm}
            {entry.fac ? ` · ${entry.fac}` : ''}
          </span>
        </span>
      </button>

      {expanded && (
        <div className="army-roster-entry-detail">
          <dl className="card-meta-list">
            {entry.type && (
              <div>
                <dt>Type</dt>
                <dd>{entry.type}</dd>
              </div>
            )}
            {entry.subType && (
              <div>
                <dt>Sub-type</dt>
                <dd>{entry.subType}</dd>
              </div>
            )}
            {entry.facNm != null && (
              <div>
                <dt>Faction #</dt>
                <dd>{entry.facNm}</dd>
              </div>
            )}
          </dl>
          {entry.ability && (
            <section>
              <h3>Ability</h3>
              <p className="prose">{entry.ability}</p>
            </section>
          )}
        </div>
      )}
    </li>
  )
}
