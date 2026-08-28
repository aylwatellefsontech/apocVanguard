import { getUnitTypeIconMarkup } from '../utils/unitTypeIcons'

interface UnitTypeIconProps {
  type: string
  className?: string
}

export default function UnitTypeIcon({ type, className = 'unit-type-icon' }: UnitTypeIconProps) {
  const markup = getUnitTypeIconMarkup(type)

  if (!markup) {
    return null
  }

  return (
    <span
      className={className}
      aria-hidden="true"
      dangerouslySetInnerHTML={{ __html: markup }}
    />
  )
}
