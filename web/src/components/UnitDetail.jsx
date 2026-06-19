import StatsTable from './StatsTable.jsx'
import UnitAbilities from './UnitAbilities.jsx'
import UnitWeapons from './UnitWeapons.jsx'
import { getUnitProfiles } from '../utils/units.js'

function ProfilePicker({ profile, onAdd }) {
  return (
    <div className="profile-picker">
      <div className="profile-picker-header">
        <div>
          <h4>{profile.label}</h4>
          <p className="profile-picker-meta">{profile.points} Pt</p>
        </div>
        <button type="button" className="secondary-btn" onClick={onAdd}>
          Add to Army
        </button>
      </div>
      <StatsTable stats={profile.stats} />
    </div>
  )
}

export default function UnitDetail({
  unit,
  onAddProfile,
  emptyMessage = 'Select a unit to view its datasheet.',
}) {
  if (!unit) {
    return (
      <div className="unit-detail empty">
        <p>{emptyMessage}</p>
      </div>
    )
  }

  const profiles = onAddProfile ? getUnitProfiles(unit) : null

  return (
    <div className="unit-detail">
      <header className="unit-detail-header">
        <span className="unit-type">{unit.type}</span>
        <h2>{unit.name}</h2>
        <span className="unit-no">#{unit.no}</span>
      </header>

      {profiles ? (
        <section>
          <h3>Profiles</h3>
          <div className="profile-picker-list">
            {profiles.map((profile) => (
              <ProfilePicker
                key={`${profile.kind}-${profile.index}`}
                profile={profile}
                onAdd={() => onAddProfile(unit, profile)}
              />
            ))}
          </div>
        </section>
      ) : (
        <>
          <StatsTable stats={unit.stats} label="Primary Profile" />

          {unit.profiles?.length > 0 && (
            <section>
              <h3>Alt Profiles</h3>
              {unit.profiles.map((profile, index) => (
                <StatsTable
                  key={index}
                  stats={profile}
                  label={`Alt Profile ${index + 1}`}
                />
              ))}
            </section>
          )}
        </>
      )}

      <UnitWeapons weapons={unit.weapons} />
      <UnitAbilities abilities={unit.abilities} />

      {unit.keywords?.length > 0 && (
        <section>
          <h3>Keywords</h3>
          <div className="keyword-list">
            {unit.keywords.map((keyword) => (
              <span key={keyword} className="keyword">
                {keyword}
              </span>
            ))}
          </div>
        </section>
      )}

      {unit.options?.length > 0 && (
        <section>
          <h3>Options</h3>
          <ul className="options-list">
            {unit.options.map((option, index) => (
              <li key={index}>{option}</li>
            ))}
          </ul>
        </section>
      )}
    </div>
  )
}
