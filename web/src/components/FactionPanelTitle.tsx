import FactionIcon from './FactionIcon'

interface FactionPanelTitleProps {
  title: string
  factionName?: string | null
}

export default function FactionPanelTitle({ title, factionName = null }: FactionPanelTitleProps) {
  const iconName = factionName ?? title

  return (
    <h2 className="panel-title-with-icon">
      {iconName ? <FactionIcon name={iconName} /> : null}
      <span>{title}</span>
    </h2>
  )
}
