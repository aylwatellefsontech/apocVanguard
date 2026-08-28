import UnitTypeIcon from './UnitTypeIcon'

interface UnitGroupHeadingProps {
  type: string
}

export default function UnitGroupHeading({ type }: UnitGroupHeadingProps) {
  return (
    <h3 className="unit-group-heading">
      <UnitTypeIcon type={type} />
      {type}
    </h3>
  )
}
