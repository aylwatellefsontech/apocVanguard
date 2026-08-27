import StatsTable from './StatsTable'
import UnitAbilities from './UnitAbilities'
import UnitTagList from './UnitTagList'
import UnitDetailHeader from './UnitDetailHeader'
import UnitOptions from './UnitOptions'
import UnitProfileDetails from './UnitProfileDetails'
import UnitProfileSummaryList from './UnitProfileSummaryList'
import UnitWeapons from './UnitWeapons'
import { getProfileDisplayName, getUnitProfiles, resolveActiveProfile } from '../utils/units'
import type {
  ActiveProfileSelection,
  OptionToggleContext,
  SelectedOption,
  Unit,
  UnitOption,
  UnitProfile,
  UnitStats,
} from '../types'

interface UnitDetailProps {
  unit?: Unit | null
  onAddProfile?: (unit: Unit, profile: UnitProfile) => void
  onToggleOption?: (optionIndex: number, option: UnitOption, context?: OptionToggleContext) => void
  selectedOptionIndexes?: number[]
  selectedOptions?: SelectedOption[]
  optionProfileStats?: UnitStats | null
  emptyMessage?: string
  showProfileAddButtons?: boolean
  activeProfile?: ActiveProfileSelection | null
}

export default function UnitDetail({
  unit,
  onAddProfile,
  onToggleOption,
  selectedOptionIndexes,
  selectedOptions,
  optionProfileStats,
  emptyMessage = 'Select a unit to view its datasheet.',
  showProfileAddButtons = false,
  activeProfile = null,
}: UnitDetailProps) {
  if (!unit) {
    return (
      <div className="unit-detail empty">
        <p>{emptyMessage}</p>
      </div>
    )
  }

  const allProfiles = getUnitProfiles(unit)
  const primaryProfile = allProfiles.find((profile) => profile.kind === 'primary') ?? allProfiles[0]
  const resolvedActiveProfile = resolveActiveProfile(allProfiles, activeProfile)
  const displayStats = resolvedActiveProfile ? optionProfileStats ?? resolvedActiveProfile.stats : unit.stats
  const displayLabel = resolvedActiveProfile
    ? getProfileDisplayName(resolvedActiveProfile)
    : primaryProfile
      ? getProfileDisplayName(primaryProfile)
      : 'Profile'

  return (
    <div className="unit-detail">
      <UnitDetailHeader unit={unit} />

      <StatsTable stats={displayStats} label={displayLabel} />
      <UnitProfileSummaryList
        profiles={allProfiles}
        activeProfile={activeProfile}
        onAddProfile={
          showProfileAddButtons && onAddProfile
            ? (profile) => onAddProfile(unit, profile)
            : undefined
        }
      />

      <UnitWeapons weapons={unit.weapons} />
      <UnitAbilities abilities={unit.abilities} />
      <UnitTagList title="Keywords" tags={unit.keywords} />
      <UnitTagList title="Traits" tags={unit.traits} />

      <UnitProfileDetails
        unit={unit}
        activeProfile={activeProfile}
        onAddProfile={
          showProfileAddButtons && onAddProfile
            ? (profile) => onAddProfile(unit, profile)
            : undefined
        }
      />

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
