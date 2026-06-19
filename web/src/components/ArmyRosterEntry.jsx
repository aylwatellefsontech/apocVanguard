import StatsTable from './StatsTable.jsx'
import UnitAbilities from './UnitAbilities.jsx'
import UnitOptions from './UnitOptions.jsx'
import UnitWeapons from './UnitWeapons.jsx'
import { formatRosterEntryMeta } from '../utils/roster.js'
import {
  getProfileStatsForEntry,
  getUnitProfiles,
  isProfileSelected,
} from '../utils/units.js'

export default function ArmyRosterEntry({ entry, unit, expanded, onToggleExpanded }) {
  const profileStats = unit ? getProfileStatsForEntry(unit, entry) : null
  const selectedOptionIndexes = entry.selectedOptions?.map((option) => option.index) ?? []

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
          <span className="roster-item-meta">{formatRosterEntryMeta(entry)}</span>
          {entry.unitType && (
            <span className="roster-item-meta">{entry.unitType}</span>
          )}
        </span>
      </button>

      {expanded && (
        <div className="army-roster-entry-detail">
          {!unit ? (
            <p className="muted panel-message">Unit datasheet not available.</p>
          ) : (
            <>
              <section>
                <h3>Profiles</h3>
                <div className="profile-picker-list">
                  {getUnitProfiles(unit).map((profile) => (
                    <div
                      key={`${profile.kind}-${profile.index}`}
                      className={`profile-block${
                        isProfileSelected(profile, entry) ? ' selected' : ' dimmed'
                      }`}
                    >
                      <div className="profile-block-header">
                        <h4>{profile.label}</h4>
                        <p className="profile-picker-meta">{profile.points} Pt</p>
                      </div>
                      <StatsTable stats={profile.stats} />
                    </div>
                  ))}
                </div>
              </section>

              <UnitWeapons weapons={unit.weapons} />
              <UnitAbilities abilities={unit.abilities} />

              <UnitOptions
                options={unit.options}
                selectedOptionIndexes={selectedOptionIndexes}
                profileStats={profileStats}
                highlightSelection
              />
            </>
          )}
        </div>
      )}
    </li>
  )
}
