import type { ReactNode } from 'react'
import { getUnitWeightKeyword } from '../utils/units'
import type { Unit } from '../types'

interface UnitDetailHeaderProps {
  unit: Unit
  asideFooter?: ReactNode
}

export default function UnitDetailHeader({ unit, asideFooter }: UnitDetailHeaderProps) {
  const weightKeyword = getUnitWeightKeyword(unit)

  return (
    <header className="unit-detail-header">
      <div className="unit-detail-header-main">
        <span className="unit-type">{unit.type}</span>
        <h2>{unit.name}</h2>
      </div>
      <div className={`unit-detail-header-aside${asideFooter ? ' has-footer' : ''}`}>
        <div className="unit-detail-header-aside-main">
          {weightKeyword && <span className="unit-header-keyword">{weightKeyword}</span>}
          <span className="unit-no">#{unit.no}</span>
        </div>
        {asideFooter}
      </div>
    </header>
  )
}
