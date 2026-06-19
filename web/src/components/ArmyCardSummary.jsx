export default function ArmyCardSummary({ entry, active = false, onSelect, onRemove }) {
  return (
    <li className={active ? 'roster-item roster-card-item active' : 'roster-item roster-card-item'}>
      {onSelect ? (
        <button type="button" className="roster-item-main" onClick={() => onSelect(entry)}>
          <strong>{entry.name}</strong>
          <p className="roster-item-meta">
            {entry.set}-{entry.nm}
            {entry.fac ? ` · ${entry.fac}` : ''}
          </p>
        </button>
      ) : (
        <div className="roster-item-main">
          <strong>{entry.name}</strong>
          <p className="roster-item-meta">
            {entry.set}-{entry.nm}
            {entry.fac ? ` · ${entry.fac}` : ''}
          </p>
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
