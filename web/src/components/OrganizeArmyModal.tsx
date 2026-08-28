import { useEffect, useState, type DragEvent } from 'react'
import DetachmentLabel, { getDetachmentAriaLabel } from './DetachmentLabel'
import RosterEntryDetail from './RosterEntryDetail'
import RosterOrganizeBadges from './RosterOrganizeBadges'
import { MOBILE_QUERY, useMediaQuery } from '../hooks/useMediaQuery'
import {
  assignRosterCardSlot,
  CARD_SLOT_NUMBERS,
  formatOrganizeEntryMeta,
  getRosterEntriesForCardSlot,
  sortRosterByOrganizeGroup,
  toggleRosterCommander,
} from '../utils/rosterOrganize'
import type { RosterEntry, Unit } from '../types'

const DRAG_ENTRY_KEY = 'application/x-vanguard-roster-entry'

interface OrganizeArmyModalProps {
  roster: RosterEntry[]
  unitsByEntryId: Map<string, Unit>
  showFaction?: boolean
  onRosterChange: (roster: RosterEntry[]) => void
  onClose: () => void
}

export default function OrganizeArmyModal({
  roster,
  unitsByEntryId,
  showFaction = false,
  onRosterChange,
  onClose,
}: OrganizeArmyModalProps) {
  const isMobile = useMediaQuery(MOBILE_QUERY)
  const [dragOverSlot, setDragOverSlot] = useState<number | 'unassigned' | null>(null)
  const [selectedEntryId, setSelectedEntryId] = useState<string | null>(null)
  const [slotRailExpanded, setSlotRailExpanded] = useState(false)
  const [expandedEntryIds, setExpandedEntryIds] = useState<Set<string>>(() => new Set())

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
    setSelectedEntryId(entryId)
  }

  function readDraggedEntryId(event: DragEvent): string | null {
    const entryId = event.dataTransfer.getData(DRAG_ENTRY_KEY)
    return entryId || null
  }

  function assignEntry(entryId: string, cardSlot: number | null) {
    onRosterChange(assignRosterCardSlot(roster, entryId, cardSlot))
    setSelectedEntryId(null)
    setDragOverSlot(null)
  }

  function handleDropOnSlot(cardSlot: number | null, event: DragEvent) {
    event.preventDefault()

    const entryId = readDraggedEntryId(event) ?? selectedEntryId
    if (!entryId) {
      return
    }

    assignEntry(entryId, cardSlot)
  }

  function handleAssignSlot(cardSlot: number) {
    if (!selectedEntryId) {
      return
    }

    assignEntry(selectedEntryId, cardSlot)
  }

  function handleToggleCommander(entryId: string) {
    onRosterChange(toggleRosterCommander(roster, entryId))
  }

  function handleSortRoster() {
    onRosterChange(sortRosterByOrganizeGroup(roster))
  }

  function handleToggleExpandAll() {
    const hasExpandedPanels = !isMobile && (slotRailExpanded || expandedEntryIds.size > 0)

    if (hasExpandedPanels) {
      setExpandedEntryIds(new Set())
      setSlotRailExpanded(false)
      setSelectedEntryId(null)
      return
    }

    if (!isMobile) {
      setSlotRailExpanded(true)
      setExpandedEntryIds(new Set(roster.map((entry) => entry.id)))
    }
  }

  const expandAllLabel = !isMobile && (slotRailExpanded || expandedEntryIds.size > 0)
    ? 'Collapse All'
    : 'Expand All'

  function handleSelectEntry(entryId: string) {
    if (!isMobile) {
      return
    }

    setSelectedEntryId((current) => (current === entryId ? null : entryId))
  }

  function handleUnassignSelected() {
    if (!selectedEntryId) {
      return
    }

    assignEntry(selectedEntryId, null)
  }

  function handleToggleEntryExpanded(entryId: string) {
    setExpandedEntryIds((current) => {
      const next = new Set(current)
      if (next.has(entryId)) {
        next.delete(entryId)
      } else {
        next.add(entryId)
      }
      return next
    })
  }

  const bodyClassName = 'organize-army-body'

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
              {isMobile
                ? 'Tap a unit, then tap a detachment to assign. Tap the medal to mark a commander.'
                : 'Drag units onto detachments 1–6. Use the medal to mark a commander.'}
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
            {!isMobile ? (
              <button
                type="button"
                className="secondary-btn organize-expand-all-btn"
                onClick={handleToggleExpandAll}
                disabled={roster.length === 0}
                aria-label={expandAllLabel}
                title={expandAllLabel}
              >
                Collapse / Expand
              </button>
            ) : null}
            <button type="button" className="secondary-btn" onClick={onClose}>
              Done
            </button>
          </div>
        </header>

        <div className={bodyClassName}>
          <section
            className={
              slotRailExpanded ? 'organize-slot-rail expanded' : 'organize-slot-rail'
            }
            aria-label="Detachment numbers 1 to 6"
          >
            {!isMobile ? (
              <button
                type="button"
                className="organize-slot-expand text-btn"
                aria-expanded={slotRailExpanded}
                aria-label={
                  slotRailExpanded ? 'Collapse detachment assignments' : 'Expand detachment assignments'
                }
                title={
                  slotRailExpanded ? 'Collapse detachment assignments' : 'Expand detachment assignments'
                }
                onClick={() => setSlotRailExpanded((current) => !current)}
              >
                {slotRailExpanded ? '▾' : '▸'}
              </button>
            ) : null}

            {CARD_SLOT_NUMBERS.map((slot) => {
              const slotEntries = getRosterEntriesForCardSlot(roster, slot)
              const assignedCount = slotEntries.length
              const isDragOver = dragOverSlot === slot
              const isActive =
                selectedEntryId != null &&
                roster.find((entry) => entry.id === selectedEntryId)?.cardSlot === slot
              const showExpandedGroup = !isMobile && slotRailExpanded

              const slotDropHandlers = {
                onDragOver: (event: DragEvent) => {
                  event.preventDefault()
                  setDragOverSlot(slot)
                },
                onDragLeave: () => {
                  if (dragOverSlot === slot) {
                    setDragOverSlot(null)
                  }
                },
                onDrop: (event: DragEvent) => handleDropOnSlot(slot, event),
              }

              return (
                <div
                  key={slot}
                  className={[
                    'organize-slot-group',
                    showExpandedGroup ? 'expanded' : null,
                    showExpandedGroup && isDragOver ? 'drag-over' : null,
                    showExpandedGroup && isActive ? 'active' : null,
                  ]
                    .filter(Boolean)
                    .join(' ')}
                  {...(showExpandedGroup ? slotDropHandlers : {})}
                >
                  <button
                    type="button"
                    className={[
                      'organize-slot-btn',
                      showExpandedGroup ? 'wide' : null,
                      !showExpandedGroup && isDragOver ? 'drag-over' : null,
                      !showExpandedGroup && isActive ? 'active' : null,
                    ]
                      .filter(Boolean)
                      .join(' ')}
                    aria-label={`Assign to ${getDetachmentAriaLabel(slot)}`}
                    onClick={() => handleAssignSlot(slot)}
                    {...(!showExpandedGroup ? slotDropHandlers : {})}
                  >
                    <DetachmentLabel
                      slot={slot}
                      showWord={!isMobile}
                      className="organize-slot-label detachment-label"
                      numberClassName="detachment-label-number organize-slot-number"
                    />
                    {assignedCount > 0 ? (
                      <span className="organize-slot-count" aria-hidden="true">
                        {assignedCount}
                      </span>
                    ) : null}
                  </button>

                  {showExpandedGroup ? (
                    slotEntries.length > 0 ? (
                      <ul className="organize-slot-assigned-list">
                        {slotEntries.map((entry) => (
                          <li
                            key={entry.id}
                            className="organize-slot-assigned-item"
                            draggable
                            onDragStart={(event) => handleDragStart(entry.id, event)}
                          >
                            <span className="organize-slot-assigned-name">{entry.unitName}</span>
                            <span className="organize-slot-assigned-meta roster-item-meta">
                              {formatOrganizeEntryMeta(
                                entry,
                                unitsByEntryId.get(entry.id),
                                showFaction,
                              )}
                            </span>
                            {entry.isCommander ? (
                              <span className="organize-slot-assigned-commander">Commander</span>
                            ) : null}
                          </li>
                        ))}
                      </ul>
                    ) : (
                      <p className="muted organize-slot-assigned-empty">Drop units here</p>
                    )
                  ) : null}
                </div>
              )
            })}

            {selectedEntryId ? (
              <button
                type="button"
                className="organize-slot-clear text-btn"
                onClick={handleUnassignSelected}
              >
                Clear
              </button>
            ) : null}
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
              {roster.map((entry) => {
                const isExpanded = expandedEntryIds.has(entry.id)

                return (
                  <li
                    key={entry.id}
                    className={[
                      'organize-unit-row',
                      entry.id === selectedEntryId ? 'selected' : null,
                      isExpanded ? 'expanded' : null,
                    ]
                      .filter(Boolean)
                      .join(' ')}
                    draggable={!isMobile}
                    onDragStart={(event) => handleDragStart(entry.id, event)}
                    onClick={() => handleSelectEntry(entry.id)}
                  >
                    <div className="organize-unit-row-header">
                      {!isMobile ? (
                        <button
                          type="button"
                          className="organize-unit-expand text-btn"
                          aria-expanded={isExpanded}
                          aria-label={isExpanded ? 'Collapse unit details' : 'Expand unit details'}
                          onClick={(event) => {
                            event.stopPropagation()
                            handleToggleEntryExpanded(entry.id)
                          }}
                        >
                          {isExpanded ? '▾' : '▸'}
                        </button>
                      ) : null}

                      <div className="organize-unit-main">
                        <div className="organize-unit-title-row">
                          <strong>{entry.unitName}</strong>
                          <div
                            className="organize-unit-badges-wrap"
                            onClick={(event) => event.stopPropagation()}
                          >
                            <RosterOrganizeBadges
                              entry={entry}
                              showCommanderToggle
                              onToggleCommander={() => handleToggleCommander(entry.id)}
                            />
                          </div>
                        </div>
                        <p className="roster-item-meta">
                          {formatOrganizeEntryMeta(
                            entry,
                            unitsByEntryId.get(entry.id),
                            showFaction,
                          )}
                        </p>
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
                    </div>

                    {!isMobile && isExpanded ? (
                      <RosterEntryDetail
                        entry={entry}
                        unit={unitsByEntryId.get(entry.id) ?? null}
                        className="organize-unit-detail army-roster-entry-detail"
                      />
                    ) : null}
                  </li>
                )
              })}
            </ul>
          </section>
        </div>
      </div>
    </div>
  )
}
