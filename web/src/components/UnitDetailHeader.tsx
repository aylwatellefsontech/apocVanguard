import { unitHasInfantryKeyword } from '../utils/units'
import type { Unit } from '../types'

interface UnitDetailHeaderProps {
  unit: Unit
}

export default function UnitDetailHeader({ unit }: UnitDetailHeaderProps) {
  const showInfantry = unitHasInfantryKeyword(unit)

  return (
    <header className="unit-detail-header">
      <div className="unit-detail-header-main">
        <span className="unit-type">{unit.type}</span>
        <h2>{unit.name}</h2>
      </div>
      <div className="unit-detail-header-aside">
        {showInfantry && <span className="unit-header-keyword">Infantry</span>}
        <span className="unit-no">#{unit.no}</span>
      </div>
    </header>
  )
}
