export default function CardDetail({ card, emptyMessage = 'Select a card to view its details.', headerAction = null }) {
  if (!card) {
    return (
      <div className="unit-detail empty">
        <p>{emptyMessage}</p>
      </div>
    )
  }

  return (
    <div className="unit-detail card-detail">
      <header
        className={
          headerAction ? 'unit-detail-header has-header-action' : 'unit-detail-header'
        }
      >
        <span className="unit-type">{card.type}</span>
        <div className="card-detail-title-block">
          <h2>{card.name}</h2>
          {headerAction && <div className="card-header-action">{headerAction}</div>}
        </div>
        <span className="unit-no">
          {card.set}-{card.nm}
        </span>
      </header>

      <section>
        <h3>Card Info</h3>
        <dl className="card-meta-list">
          <div>
            <dt>Faction</dt>
            <dd>{card.fac ?? '—'}</dd>
          </div>
          {card.facNm != null && (
            <div>
              <dt>Faction #</dt>
              <dd>{card.facNm}</dd>
            </div>
          )}
          <div>
            <dt>Set</dt>
            <dd>{card.set}</dd>
          </div>
          {card.subType && (
            <div>
              <dt>Sub-type</dt>
              <dd>{card.subType}</dd>
            </div>
          )}
        </dl>
      </section>

      {card.ability && (
        <section>
          <h3>Ability</h3>
          <p className="prose">{card.ability}</p>
        </section>
      )}
    </div>
  )
}
