import CommanderMedalButton from './CommanderMedalButton'
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
              ? 'Assign a card number before marking commander'
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
        <span className="card-slot-badge" aria-label={`Card ${entry.cardSlot}`}>
          {entry.cardSlot}
        </span>
      ) : null}
    </div>
  )
}
