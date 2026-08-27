import StatsTable from './StatsTable'
import UnitAbilities from './UnitAbilities'
import UnitTagList from './UnitTagList'
import UnitWeapons from './UnitWeapons'
import {
  getProfileAnchorId,
  getProfileDisplayName,
  getProfilesForDetailsSection,
  isProfileActive,
} from '../utils/units'
import type { ActiveProfileSelection, Unit, UnitProfile } from '../types'

interface UnitProfileDetailsProps {
  unit: Unit
  activeProfile?: ActiveProfileSelection | null
  onAddProfile?: (profile: UnitProfile) => void
  hideInactiveProfiles?: boolean
}

export default function UnitProfileDetails({
  unit,
  activeProfile = null,
  onAddProfile,
  hideInactiveProfiles = false,
}: UnitProfileDetailsProps) {
  const profilesToShow = getProfilesForDetailsSection(unit)

  if (profilesToShow.length === 0) {
    return null
  }

  if (hideInactiveProfiles && activeProfile) {
    return null
  }

  const visibleProfiles = profilesToShow

  return (
    <section className="profile-details-section">
      <h3>Profile Details</h3>
      {visibleProfiles.map((profile) => {
        const isActive = activeProfile != null && isProfileActive(profile, activeProfile)
        return (
          <article
            key={`${profile.kind}-${profile.index}`}
            id={getProfileAnchorId(profile)}
            className={`profile-details-block${isActive ? ' active' : ''}${activeProfile && !isActive ? ' dimmed' : ''}`}
          >
            <div className="profile-details-block-header">
              <h4>{getProfileDisplayName(profile)}</h4>
              {onAddProfile ? (
                <button
                  type="button"
                  className="secondary-btn profile-details-add"
                  onClick={() => onAddProfile(profile)}
                >
                  Add to Army
                </button>
              ) : null}
            </div>
            <StatsTable stats={profile.stats} />
            <UnitTagList title="Keywords" tags={profile.keywords} embedded />
            <UnitTagList title="Traits" tags={profile.traits} embedded />
            <UnitAbilities abilities={profile.abilities} embedded />
            <UnitWeapons weapons={profile.weapons} embedded />
          </article>
        )
      })}
    </section>
  )
}
