export default function CardDetail({ card, emptyMessage = 'Select a card to view its details.' }) {
  if (!card) {
    return (
      <div className="unit-detail empty">
        <p>{emptyMessage}</p>
      </div>
    )
  }

  return (
    <div className="unit-detail card-detail">
      <header className="unit-detail-header">
        <span className="unit-type">{card.type}</span>
        <h2>{card.name}</h2>
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
