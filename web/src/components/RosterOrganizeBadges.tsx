import CommanderMedalButton from './CommanderMedalButton'
import DetachmentLabel, { getDetachmentAriaLabel } from './DetachmentLabel'
import type { RosterEntry } from '../types'

interface RosterOrganizeBadgesProps {
  entry: RosterEntry
  showCommanderToggle?: boolean
  onToggleCommander?: () => void
}

export default function RosterOrganizeBadges({
  entry,
  showCommanderToggle = false,
  onToggleCommander,
}: RosterOrganizeBadgesProps) {
  const hasAssignment = entry.cardSlot != null

  if (!showCommanderToggle && !hasAssignment) {
    return null
  }

  return (
    <div className="roster-item-badges">
      {showCommanderToggle ? (
        <CommanderMedalButton
          active={Boolean(entry.isCommander)}
          disabled={!hasAssignment}
          title={
            !hasAssignment
              ? 'Assign a detachment before marking commander'
              : entry.isCommander
                ? 'Remove commander'
                : 'Mark as commander'
          }
          onClick={onToggleCommander}
        />
      ) : entry.isCommander ? (
        <CommanderMedalButton active disabled title="Commander" />
      ) : null}
      {hasAssignment ? (
        <span
          className="card-slot-badge detachment-badge"
          aria-label={getDetachmentAriaLabel(entry.cardSlot!)}
        >
          <DetachmentLabel
            slot={entry.cardSlot!}
            className="detachment-label detachment-badge-label"
            numberClassName="detachment-label-number detachment-badge-number"
          />
        </span>
      ) : null}
    </div>
  )
}
