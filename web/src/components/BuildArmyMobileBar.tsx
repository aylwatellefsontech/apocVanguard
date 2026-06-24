type BuildMobilePanel = 'factions' | 'list' | 'detail' | 'roster'

interface BuildArmyMobileBarProps {
  mobilePanel: BuildMobilePanel
  totalPoints: number
  unitCount: number
  cardCount: number
  onBack: () => void
  onToggleView: () => void
}

export default function BuildArmyMobileBar({
  mobilePanel,
  totalPoints,
  unitCount,
  cardCount,
  onBack,
  onToggleView,
}: BuildArmyMobileBarProps) {
  const isRoster = mobilePanel === 'roster'
  const showBack = !isRoster && mobilePanel !== 'factions'

  return (
    <div className="build-mobile-bar">
      <div className="build-mobile-bar-start">
        {showBack ? (
          <button type="button" className="mobile-back-btn" onClick={onBack} aria-label="Go back">
            ←
          </button>
        ) : null}
      </div>

      <div className="build-mobile-bar-stats">
        <span className="build-mobile-points">{totalPoints} Pt</span>
        <span className="build-mobile-count">
          {unitCount} {unitCount === 1 ? 'unit' : 'units'}
          {cardCount > 0 ? ` · ${cardCount} ${cardCount === 1 ? 'card' : 'cards'}` : ''}
        </span>
      </div>

      <button type="button" className="build-mobile-toggle" onClick={onToggleView}>
        {isRoster ? 'Add Units' : 'My List'}
      </button>
    </div>
  )
}
