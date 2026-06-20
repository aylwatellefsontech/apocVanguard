import StatsTable from './StatsTable'
import UnitAbilities from './UnitAbilities'
import UnitDetailHeader from './UnitDetailHeader'
import UnitOptions from './UnitOptions'
import UnitWeapons from './UnitWeapons'
import { getUnitProfiles } from '../utils/units'
import type { Unit, UnitOption, UnitProfile, UnitStats } from '../types'

interface ProfilePickerProps {
  profile: UnitProfile
  onAdd: () => void
}

function ProfilePicker({ profile, onAdd }: ProfilePickerProps) {
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

interface UnitDetailProps {
  unit?: Unit | null
  onAddProfile?: (unit: Unit, profile: UnitProfile) => void
  onToggleOption?: (optionIndex: number, option: UnitOption) => void
  selectedOptionIndexes?: number[]
  optionProfileStats?: UnitStats | null
  emptyMessage?: string
}

export default function UnitDetail({
  unit,
  onAddProfile,
  onToggleOption,
  selectedOptionIndexes,
  optionProfileStats,
  emptyMessage = 'Select a unit to view its datasheet.',
}: UnitDetailProps) {
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
      <UnitDetailHeader unit={unit} />

      {profiles ? (
        <section>
          <h3>Profiles</h3>
          <div className="profile-picker-list">
            {profiles.map((profile) => (
              <ProfilePicker
                key={`${profile.kind}-${profile.index}`}
                profile={profile}
                onAdd={() => onAddProfile?.(unit, profile)}
              />
            ))}
          </div>
        </section>
      ) : (
        <>
          <StatsTable stats={unit.stats} label="Primary Profile" />

          {unit.profiles && unit.profiles.length > 0 && (
            <section>
              <h3>Alt Profiles</h3>
              {unit.profiles.map((profile, index) => (
                <StatsTable key={index} stats={profile} label={`Alt Profile ${index + 1}`} />
              ))}
            </section>
          )}
        </>
      )}

      <UnitWeapons weapons={unit.weapons} />
      <UnitAbilities abilities={unit.abilities} />

      {unit.keywords && unit.keywords.length > 0 && (
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

      <UnitOptions
        options={unit.options}
        interactive={Boolean(onToggleOption)}
        selectedOptionIndexes={selectedOptionIndexes ?? []}
        profileStats={optionProfileStats}
        onToggleOption={onToggleOption}
        showSelectHint={Boolean(onAddProfile && !onToggleOption && unit.options?.length)}
      />
    </div>
  )
}
