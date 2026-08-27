import {
  getProfileDisplayName,
  isProfileActive,
  scrollToProfileDetail,
} from '../utils/units'
import type { ActiveProfileSelection, UnitProfile } from '../types'

interface UnitProfileSummaryListProps {
  profiles: UnitProfile[]
  activeProfile?: ActiveProfileSelection | null
  onAddProfile?: (profile: UnitProfile) => void
  hideInactiveProfiles?: boolean
}

export default function UnitProfileSummaryList({
  profiles,
  activeProfile = null,
  onAddProfile,
  hideInactiveProfiles = false,
}: UnitProfileSummaryListProps) {
  if (profiles.length <= 1 && !onAddProfile) {
    return null
  }

  if (hideInactiveProfiles && activeProfile) {
    return null
  }

  return (
    <section className="profile-summary-section">
      <h3>Profiles</h3>
      <ul className="profile-summary-list">
        {profiles.map((profile) => {
          const isActive = activeProfile != null && isProfileActive(profile, activeProfile)
          const isDimmed = activeProfile != null && profiles.length > 1 && !isActive
          return (
            <li
              key={`${profile.kind}-${profile.index}`}
              className={`profile-summary-item${isActive ? ' active' : ''}${isDimmed ? ' dimmed' : ''}`}
            >
              <div className="profile-summary-item-main">
                <button
                  type="button"
                  className="profile-summary-name profile-summary-link"
                  onClick={() => scrollToProfileDetail(profile)}
                >
                  {getProfileDisplayName(profile)}
                </button>
                <span className="profile-summary-points">{profile.points} Pt</span>
              </div>
              {onAddProfile ? (
                <button
                  type="button"
                  className="secondary-btn profile-summary-add"
                  onClick={() => onAddProfile(profile)}
                >
                  Add to Army
                </button>
              ) : null}
            </li>
          )
        })}
      </ul>
    </section>
  )
}
