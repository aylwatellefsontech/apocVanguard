import { useState } from 'react'
import StatsTable from './StatsTable'
import UnitAbilities from './UnitAbilities'
import UnitTagList from './UnitTagList'
import UnitDetailHeader from './UnitDetailHeader'
import UnitOptions from './UnitOptions'
import UnitProfileDetails from './UnitProfileDetails'
import UnitProfileSummaryList from './UnitProfileSummaryList'
import UnitWeapons from './UnitWeapons'
import {
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

interface RosterEntryDetailProps {
  entry: RosterEntry
  unit: Unit | null
  className?: string
}

export default function RosterEntryDetail({
  entry,
  unit,
  className = 'army-roster-entry-detail',
}: RosterEntryDetailProps) {
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
    <div className={className}>
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
  )
}
