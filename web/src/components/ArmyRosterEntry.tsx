import { useState } from 'react'
import StatsTable from './StatsTable'
import UnitAbilities from './UnitAbilities'
import UnitTagList from './UnitTagList'
import UnitDetailHeader from './UnitDetailHeader'
import UnitOptions from './UnitOptions'
import UnitProfileDetails from './UnitProfileDetails'
import UnitProfileSummaryList from './UnitProfileSummaryList'
import UnitWeapons from './UnitWeapons'
import { formatRosterEntryMeta } from '../utils/roster'
import {
  formatUnitTypeLabel,
  getBlendedAbilities,
  getBlendedKeywords,
  getBlendedTraits,
  getBlendedWeapons,
  getProfileDisplayName,
  getProfileStatsForEntry,
  getUnitProfiles,
  resolveActiveProfile,
} from '../utils/units'
import type { RosterEntry, Unit } from '../types'

interface ArmyRosterEntryProps {
  entry: RosterEntry
  unit: Unit | null
  showFaction?: boolean
  expanded: boolean
  onToggleExpanded: () => void
}

export default function ArmyRosterEntry({
  entry,
  unit,
  showFaction = false,
  expanded,
  onToggleExpanded,
}: ArmyRosterEntryProps) {
  const [showAlternateProfiles, setShowAlternateProfiles] = useState(false)
  const profileStats = unit ? getProfileStatsForEntry(unit, entry) : null
  const selectedOptionIndexes = entry.selectedOptions?.map((option) => option.index) ?? []
  const allProfiles = unit ? getUnitProfiles(unit) : []
  const activeProfile = {
    kind: entry.profileKind,
    index: entry.profileIndex,
    label: entry.profileLabel,
  }
  const resolvedProfile = resolveActiveProfile(allProfiles, activeProfile)
  const profileLabel = resolvedProfile ? getProfileDisplayName(resolvedProfile) : entry.profileLabel
  const hasAlternateProfiles = allProfiles.length > 1
  const hideInactiveProfiles = hasAlternateProfiles && !showAlternateProfiles

  return (
    <li className={`roster-item army-roster-entry${expanded ? ' expanded' : ''}`}>
      <button
        type="button"
        className="army-roster-entry-toggle"
        onClick={onToggleExpanded}
        aria-expanded={expanded}
      >
        <span className="roster-expand-icon" aria-hidden="true">
          {expanded ? '▾' : '▸'}
        </span>
        <span className="army-roster-entry-summary">
          <strong>{entry.unitName}</strong>
          <span className="roster-item-meta">{formatRosterEntryMeta(entry, showFaction)}</span>
          {entry.unitType && (
            <span className="roster-item-meta">
              {formatUnitTypeLabel(entry.unitType, unit)}
            </span>
          )}
        </span>
      </button>

      {expanded && (
        <div className="army-roster-entry-detail">
          {!unit ? (
            <p className="muted panel-message">Unit datasheet not available.</p>
          ) : (
            <>
              <UnitDetailHeader
                unit={unit}
                asideFooter={
                  hasAlternateProfiles ? (
                    <button
                      type="button"
                      className="text-btn army-roster-profile-toggle"
                      onClick={() => setShowAlternateProfiles((current) => !current)}
                    >
                      {showAlternateProfiles ? 'Hide other profiles' : 'Show other profiles'}
                    </button>
                  ) : undefined
                }
              />

              <StatsTable stats={profileStats} label={profileLabel} />
              <UnitProfileSummaryList
                profiles={allProfiles}
                activeProfile={activeProfile}
                hideInactiveProfiles={hideInactiveProfiles}
              />

              <UnitWeapons weapons={getBlendedWeapons(unit, resolvedProfile)} />
              <UnitAbilities abilities={getBlendedAbilities(unit, resolvedProfile)} />
              <UnitTagList title="Keywords" tags={getBlendedKeywords(unit, resolvedProfile)} />
              <UnitTagList title="Traits" tags={getBlendedTraits(unit, resolvedProfile)} />

              <UnitProfileDetails
                unit={unit}
                activeProfile={activeProfile}
                hideInactiveProfiles={hideInactiveProfiles}
              />

              <UnitOptions
                options={unit.options}
                selectedOptionIndexes={selectedOptionIndexes}
                selectedOptions={entry.selectedOptions}
                profileStats={profileStats}
                highlightSelection={!hideInactiveProfiles}
                hideUnselected={hideInactiveProfiles}
              />
            </>
          )}
        </div>
      )}
    </li>
  )
}
