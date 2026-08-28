import { formatDetachmentLabel } from '../utils/rosterOrganize'

interface DetachmentLabelProps {
  slot: number
  /** Show "Detachment" before the number (organize modal left rail, desktop only). */
  showWord?: boolean
  className?: string
  numberClassName?: string
}

export default function DetachmentLabel({
  slot,
  showWord = false,
  className = 'detachment-label',
  numberClassName = 'detachment-label-number',
}: DetachmentLabelProps) {
  return (
    <span className={className} aria-hidden="true">
      {showWord ? <span className="detachment-label-word">Detachment </span> : null}
      <span className={numberClassName}>{slot}</span>
    </span>
  )
}

export function getDetachmentAriaLabel(slot: number): string {
  return formatDetachmentLabel(slot)
}
