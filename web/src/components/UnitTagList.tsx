import type { ProfileTagSection } from '../types'

interface UnitTagListProps {
  title: string
  tags?: string[]
  profileSections?: ProfileTagSection[]
  embedded?: boolean
}

export default function UnitTagList({
  title,
  tags = [],
  profileSections = [],
  embedded = false,
}: UnitTagListProps) {
  if (tags.length === 0 && profileSections.length === 0) return null

  const Wrapper = embedded ? 'div' : 'section'
  const HeadingTag = embedded ? 'h5' : 'h3'

  return (
    <Wrapper className={embedded ? 'profile-details-subsection' : undefined}>
      {!embedded && <HeadingTag>{title}</HeadingTag>}
      {tags.length > 0 && (
        embedded ? (
          <>
            <HeadingTag>{title}</HeadingTag>
            <div className="keyword-list">
              {tags.map((tag) => (
                <span key={tag} className="keyword">
                  {tag}
                </span>
              ))}
            </div>
          </>
        ) : (
          <div className="keyword-list">
            {tags.map((tag) => (
              <span key={tag} className="keyword">
                {tag}
              </span>
            ))}
          </div>
        )
      )}
      {profileSections.map((section) => (
        <div key={section.heading} className="profile-extras">
          <h4>{section.heading}</h4>
          <div className="keyword-list">
            {section.items.map((item) => (
              <span key={item} className="keyword">
                {item}
              </span>
            ))}
          </div>
        </div>
      ))}
    </Wrapper>
  )
}
