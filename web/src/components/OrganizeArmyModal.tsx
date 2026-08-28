import { useEffect, useState, type DragEvent } from 'react'
import CommanderMedalButton from './CommanderMedalButton'
import RosterOrganizeBadges from './RosterOrganizeBadges'
import { formatRosterEntryMeta } from '../utils/roster'
import {
  assignRosterCardSlot,
  CARD_SLOT_NUMBERS,
  getRosterEntriesForCardSlot,
  sortRosterByOrganizeGroup,
  toggleRosterCommander,
} from '../utils/rosterOrganize'
import type { RosterEntry } from '../types'

const DRAG_ENTRY_KEY = 'application/x-vanguard-roster-entry'

interface OrganizeArmyModalProps {
  roster: RosterEntry[]
  showFaction?: boolean
  onRosterChange: (roster: RosterEntry[]) => void
  onClose: () => void
}

export default function OrganizeArmyModal({
  roster,
  showFaction = false,
  onRosterChange,
  onClose,
}: OrganizeArmyModalProps) {
  const [dragOverSlot, setDragOverSlot] = useState<number | 'unassigned' | null>(null)

  useEffect(() => {
    function handleKeyDown(event: KeyboardEvent) {
      if (event.key === 'Escape') {
        onClose()
      }
    }

    document.addEventListener('keydown', handleKeyDown)
    return () => document.removeEventListener('keydown', handleKeyDown)
  }, [onClose])

  function handleDragStart(entryId: string, event: DragEvent) {
    event.dataTransfer.setData(DRAG_ENTRY_KEY, entryId)
    event.dataTransfer.effectAllowed = 'move'
  }

  function readDraggedEntryId(event: DragEvent): string | null {
    const entryId = event.dataTransfer.getData(DRAG_ENTRY_KEY)
    return entryId || null
  }

  function handleDropOnSlot(cardSlot: number | null, event: DragEvent) {
    event.preventDefault()
    setDragOverSlot(null)

    const entryId = readDraggedEntryId(event)
    if (!entryId) {
      return
    }

    onRosterChange(assignRosterCardSlot(roster, entryId, cardSlot))
  }

  function handleToggleCommander(entryId: string) {
    onRosterChange(toggleRosterCommander(roster, entryId))
  }

  function handleSortRoster() {
    onRosterChange(sortRosterByOrganizeGroup(roster))
  }

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div
        className="modal-panel organize-army-modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="organize-army-modal-title"
        onClick={(event) => event.stopPropagation()}
      >
        <header className="hand-modal-header">
          <div>
            <h2 id="organize-army-modal-title">Organize Army</h2>
            <p className="muted organize-army-subtitle">
              Drag units onto numbers 1–6. Use the medal to mark a commander.
            </p>
          </div>
          <div className="hand-modal-actions">
            <button
              type="button"
              className="secondary-btn icon-btn"
              onClick={handleSortRoster}
              aria-label="Sort units"
              title="Sort by group, faction, commander, then name"
            >
              ↕
            </button>
            <button type="button" className="secondary-btn" onClick={onClose}>
              Done
            </button>
          </div>
        </header>

        <div className="organize-army-body">
          <section className="organize-card-slots" aria-label="Card numbers 1 to 6">
            {CARD_SLOT_NUMBERS.map((slot) => {
              const slotEntries = getRosterEntriesForCardSlot(roster, slot)
              const isDragOver = dragOverSlot === slot

              return (
                <div
                  key={slot}
                  className={isDragOver ? 'organize-card-slot drag-over' : 'organize-card-slot'}
                  onDragOver={(event) => {
                    event.preventDefault()
                    setDragOverSlot(slot)
                  }}
                  onDragLeave={() => {
                    if (dragOverSlot === slot) {
                      setDragOverSlot(null)
                    }
                  }}
                  onDrop={(event) => handleDropOnSlot(slot, event)}
                >
                  <h3 className="organize-card-slot-title">{slot}</h3>
                  {slotEntries.length === 0 ? (
                    <p className="muted organize-card-slot-empty">Drop units here</p>
                  ) : (
                    <ul className="organize-card-slot-list">
                      {slotEntries.map((entry) => (
                        <li key={entry.id}>
                          <button
                            type="button"
                            className="organize-card-slot-unit"
                            draggable
                            onDragStart={(event) => handleDragStart(entry.id, event)}
                          >
                            <span className="organize-card-slot-unit-name">{entry.unitName}</span>
                            {entry.isCommander ? (
                              <span className="organize-commander-label">
                                <CommanderMedalButton active disabled title="Commander" />
                              </span>
                            ) : null}
                          </button>
                        </li>
                      ))}
                    </ul>
                  )}
                </div>
              )
            })}
          </section>

          <section
            className={
              dragOverSlot === 'unassigned'
                ? 'organize-unit-panel drag-over'
                : 'organize-unit-panel'
            }
            aria-label="Army units"
            onDragOver={(event) => {
              event.preventDefault()
              setDragOverSlot('unassigned')
            }}
            onDragLeave={() => {
              if (dragOverSlot === 'unassigned') {
                setDragOverSlot(null)
              }
            }}
            onDrop={(event) => handleDropOnSlot(null, event)}
          >
            <h3 className="organize-unit-panel-title">Units</h3>
            <ul className="organize-unit-list">
              {roster.map((entry) => (
                <li
                  key={entry.id}
                  className="organize-unit-row"
                  draggable
                  onDragStart={(event) => handleDragStart(entry.id, event)}
                >
                  <div className="organize-unit-main">
                    <div className="organize-unit-title-row">
                      <strong>{entry.unitName}</strong>
                      <RosterOrganizeBadges
                        entry={entry}
                        showCommanderToggle
                        onToggleCommander={() => handleToggleCommander(entry.id)}
                      />
                    </div>
                    <p className="roster-item-meta">{formatRosterEntryMeta(entry, showFaction)}</p>
                    {entry.selectedOptions?.length > 0 && (
                      <ul className="roster-option-list">
                        {entry.selectedOptions.map((option) => (
                          <li
                            key={`${option.index}-${option.modelIndex ?? 'unit'}-${option.slotIndex ?? 'slot'}-${option.choiceIndex ?? 'choice'}`}
                          >
                            {option.label}
                            {option.points > 0 ? ` (+${option.points} Pt)` : ''}
                          </li>
                        ))}
                      </ul>
                    )}
                  </div>
                </li>
              ))}
            </ul>
          </section>
        </div>
      </div>
    </div>
  )
}
