import StatsTable from './StatsTable'
import UnitAbilities from './UnitAbilities'
import UnitTagList from './UnitTagList'
import UnitDetailHeader from './UnitDetailHeader'
import UnitOptions from './UnitOptions'
import UnitWeapons from './UnitWeapons'
import {
  getAltProfileLabel,
  getProfileAbilitySections,
  getProfileKeywordSections,
  getProfileTraitSections,
  getProfileWeaponSections,
  getUnitProfiles,
} from '../utils/units'
import type { OptionToggleContext, SelectedOption, Unit, UnitOption, UnitProfile, UnitStats } from '../types'

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
  onToggleOption?: (optionIndex: number, option: UnitOption, context?: OptionToggleContext) => void
  selectedOptionIndexes?: number[]
  selectedOptions?: SelectedOption[]
  optionProfileStats?: UnitStats | null
  emptyMessage?: string
  showProfilePicker?: boolean
  editingProfileLabel?: string | null
}

export default function UnitDetail({
  unit,
  onAddProfile,
  onToggleOption,
  selectedOptionIndexes,
  selectedOptions,
  optionProfileStats,
  emptyMessage = 'Select a unit to view its datasheet.',
  showProfilePicker = true,
  editingProfileLabel = null,
}: UnitDetailProps) {
  if (!unit) {
    return (
      <div className="unit-detail empty">
        <p>{emptyMessage}</p>
      </div>
    )
  }

  const profiles = onAddProfile && showProfilePicker ? getUnitProfiles(unit) : null
  const editingStats = editingProfileLabel ? optionProfileStats : null
  const selectedLabel = editingProfileLabel
  const profileAbilitySections = getProfileAbilitySections(unit, selectedLabel)
  const profileWeaponSections = getProfileWeaponSections(unit, selectedLabel)
  const profileKeywordSections = getProfileKeywordSections(unit, selectedLabel)
  const profileTraitSections = getProfileTraitSections(unit, selectedLabel)

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
      ) : editingStats ? (
        <StatsTable stats={editingStats} label={editingProfileLabel ?? 'Profile'} />
      ) : (
        <>
          <StatsTable stats={unit.stats} label="Primary Profile" />

          {unit.profiles && unit.profiles.length > 0 && (
            <section>
              <h3>Alt Profiles</h3>
              {unit.profiles.map((profile, index) => (
                <StatsTable
                  key={index}
                  stats={profile}
                  label={getAltProfileLabel(profile, index)}
                />
              ))}
            </section>
          )}
        </>
      )}

      <UnitWeapons weapons={unit.weapons} profileSections={profileWeaponSections} />
      <UnitAbilities abilities={unit.abilities} profileSections={profileAbilitySections} />

      <UnitTagList title="Keywords" tags={unit.keywords} profileSections={profileKeywordSections} />
      <UnitTagList title="Traits" tags={unit.traits} profileSections={profileTraitSections} />

      <UnitOptions
        options={unit.options}
        interactive={Boolean(onToggleOption)}
        selectedOptionIndexes={selectedOptionIndexes ?? []}
        selectedOptions={selectedOptions}
        profileStats={optionProfileStats}
        onToggleOption={onToggleOption}
        showSelectHint={Boolean(onAddProfile && !onToggleOption && unit.options?.length)}
      />
    </div>
  )
}
