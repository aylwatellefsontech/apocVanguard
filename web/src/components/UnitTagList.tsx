import type { ProfileTagSection } from '../types'

interface UnitTagListProps {
  title: string
  tags?: string[]
  profileSections?: ProfileTagSection[]
}

export default function UnitTagList({ title, tags = [], profileSections = [] }: UnitTagListProps) {
  if (tags.length === 0 && profileSections.length === 0) return null

  return (
    <section>
      <h3>{title}</h3>
      {tags.length > 0 && (
        <div className="keyword-list">
          {tags.map((tag) => (
            <span key={tag} className="keyword">
              {tag}
            </span>
          ))}
        </div>
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
    </section>
  )
}
