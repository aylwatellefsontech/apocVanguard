import { getFactionIconMarkup } from '../utils/factionIcons'

interface FactionIconProps {
  name: string
  className?: string
}

export default function FactionIcon({ name, className = 'faction-icon' }: FactionIconProps) {
  const markup = getFactionIconMarkup(name)

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
