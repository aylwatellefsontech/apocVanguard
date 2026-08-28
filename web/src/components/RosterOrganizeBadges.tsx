import CommanderMedalButton from './CommanderMedalButton'
import DetachmentLabel, { getDetachmentAriaLabel } from './DetachmentLabel'
import type { RosterEntry } from '../types'

interface RosterOrganizeBadgesProps {
  entry: RosterEntry
  showCommanderToggle?: boolean
  showDetachmentBadge?: boolean
  /** Show commander badge only when marked commander (no inactive toggle). */
  commanderBadgeOnlyWhenActive?: boolean
  onToggleCommander?: () => void
}

export default function RosterOrganizeBadges({
  entry,
  showCommanderToggle = false,
  showDetachmentBadge = true,
  commanderBadgeOnlyWhenActive = false,
  onToggleCommander,
}: RosterOrganizeBadgesProps) {
  const hasAssignment = entry.cardSlot != null
  const showDetachment = showDetachmentBadge && hasAssignment
  const showCommanderToggleButton = showCommanderToggle && !commanderBadgeOnlyWhenActive
  const showActiveCommanderBadge =
    entry.isCommander && (commanderBadgeOnlyWhenActive || !showCommanderToggle)
  const hasCommanderUi = showCommanderToggleButton || showActiveCommanderBadge

  if (!hasCommanderUi && !showDetachment) {
    return null
  }

  return (
    <div className="roster-item-badges">
      {showCommanderToggleButton ? (
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
      ) : showActiveCommanderBadge ? (
        <CommanderMedalButton
          active
          disabled
          iconOnly={commanderBadgeOnlyWhenActive}
          title="Commander"
        />
      ) : null}
      {showDetachment ? (
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
