import { COMMANDER_ICON_MARKUP } from '../utils/commanderIcon'

interface CommanderMedalButtonProps {
  active?: boolean
  disabled?: boolean
  iconOnly?: boolean
  title?: string
  onClick?: () => void
}

export default function CommanderMedalButton({
  active = false,
  disabled = false,
  iconOnly = false,
  title = 'Toggle detachment commander',
  onClick,
}: CommanderMedalButtonProps) {
  const className = [
    'commander-medal-btn',
    active ? 'active' : null,
    iconOnly ? 'icon-only' : null,
  ]
    .filter(Boolean)
    .join(' ')

  return (
    <button
      type="button"
      className={className}
      aria-label={title}
      title={title}
      disabled={disabled}
      onClick={onClick}
    >
      <span
        className="commander-icon"
        aria-hidden="true"
        dangerouslySetInnerHTML={{ __html: COMMANDER_ICON_MARKUP }}
      />
    </button>
  )
}
