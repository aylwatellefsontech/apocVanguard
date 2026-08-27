import type { ProfileAbilitySection } from '../types'

interface UnitAbilitiesProps {
  abilities?: string
  profileSections?: ProfileAbilitySection[]
  embedded?: boolean
}

export default function UnitAbilities({
  abilities,
  profileSections = [],
  embedded = false,
}: UnitAbilitiesProps) {
  if (!abilities && profileSections.length === 0) return null

  const Wrapper = embedded ? 'div' : 'section'
  const HeadingTag = embedded ? 'h5' : 'h3'

  return (
    <Wrapper className={embedded ? 'profile-details-subsection' : undefined}>
      {!embedded && <HeadingTag>Abilities</HeadingTag>}
      {abilities ? (
        embedded ? (
          <>
            <HeadingTag>Abilities</HeadingTag>
            <p className="prose">{abilities}</p>
          </>
        ) : (
          <p className="prose">{abilities}</p>
        )
      ) : null}
      {profileSections.map((section) => (
        <div key={section.heading} className="profile-extras">
          <h4>{section.heading}</h4>
          <p className="prose">{section.text}</p>
        </div>
      ))}
    </Wrapper>
  )
}
