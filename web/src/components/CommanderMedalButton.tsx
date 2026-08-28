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
  const iconSize = iconOnly ? 14 : 18

  return (
    <button
      type="button"
      className={className}
      aria-label={title}
      title={title}
      disabled={disabled}
      onClick={onClick}
    >
      <svg viewBox="0 0 24 24" width={iconSize} height={iconSize} aria-hidden="true">
        <path
          fill="currentColor"
          d="M12 2.5a4.5 4.5 0 0 0-4.12 2.67L5.4 7.34 3.1 8.67 5.2 12l-2.1 3.33 2.3 1.33 2.48-1.17A4.5 4.5 0 0 0 12 17.5a4.5 4.5 0 0 0 4.12-2.67l2.48 1.17 2.3-1.33L18.8 12l2.1-3.33-2.3-1.33-2.48-1.17A4.5 4.5 0 0 0 12 2.5Z"
        />
        <circle cx="12" cy="10" r="2.35" fill="var(--bg)" />
        <path
          fill="currentColor"
          d="M8.8 16.8 7.2 21.5h9.6l-1.6-4.7-2.2 1.2-2 1.2-2.2-1.2Z"
        />
      </svg>
    </button>
  )
}
