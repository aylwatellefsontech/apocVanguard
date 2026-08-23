import type { ProfileAbilitySection } from '../types'

interface UnitAbilitiesProps {
  abilities?: string
  profileSections?: ProfileAbilitySection[]
}

export default function UnitAbilities({ abilities, profileSections = [] }: UnitAbilitiesProps) {
  if (!abilities && profileSections.length === 0) return null

  return (
    <section>
      <h3>Abilities</h3>
      {abilities ? <p className="prose">{abilities}</p> : null}
      {profileSections.map((section) => (
        <div key={section.heading} className="profile-extras">
          <h4>{section.heading}</h4>
          <p className="prose">{section.text}</p>
        </div>
      ))}
    </section>
  )
}
