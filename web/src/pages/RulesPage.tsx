import { useMemo, useState } from 'react'
import Markdown from 'react-markdown'
import MobileBackBar from '../components/MobileBackBar'
import { useRules } from '../hooks/useRules'
import { MOBILE_QUERY, useMediaQuery } from '../hooks/useMediaQuery'
import {
  createHeadingComponent,
  extractRulesHeadings,
  preprocessRulesMarkdown,
} from '../utils/rulesMarkdown'

const markdownComponents = {
  h1: createHeadingComponent('h1'),
  h2: createHeadingComponent('h2'),
  h3: createHeadingComponent('h3'),
  h4: createHeadingComponent('h4'),
  h5: createHeadingComponent('h5'),
  h6: createHeadingComponent('h6'),
}

function scrollToRulesHeading(event: React.MouseEvent<HTMLAnchorElement>, id: string) {
  event.preventDefault()
  document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  window.history.replaceState(null, '', `#${id}`)
}

type RulesMobilePanel = 'nav' | 'content'

export default function RulesPage() {
  const { markdown, loading, error } = useRules()
  const isMobile = useMediaQuery(MOBILE_QUERY)
  const [mobilePanel, setMobilePanel] = useState<RulesMobilePanel>('nav')
  const processedMarkdown = useMemo(
    () => (markdown ? preprocessRulesMarkdown(markdown) : ''),
    [markdown],
  )
  const headings = useMemo(() => extractRulesHeadings(processedMarkdown), [processedMarkdown])

  function handleRulesNavClick(event: React.MouseEvent<HTMLAnchorElement>, id: string) {
    scrollToRulesHeading(event, id)
    if (isMobile) {
      setMobilePanel('content')
    }
  }

  const rulesBodyClass = isMobile
    ? `rules-body mobile-layout mobile-panel-${mobilePanel}`
    : 'rules-body'

  return (
    <>
      <header className="app-header">
        <div>
          <p className="eyebrow">Reference</p>
          <h1>Rules of the Game</h1>
        </div>
      </header>

      {loading ? (
        <p className="muted rules-message">Loading rules…</p>
      ) : error ? (
        <p className="error-banner rules-message">{error}</p>
      ) : (
        <>
          {isMobile && mobilePanel === 'content' && (
            <MobileBackBar label="Contents" onBack={() => setMobilePanel('nav')} />
          )}

          <div className={rulesBodyClass}>
          <aside className="rules-nav-panel">
            <h2>Contents</h2>
            <nav aria-label="Rules sections">
              <ul className="rules-nav-list">
                {headings.map((heading) => (
                  <li
                    key={heading.id}
                    className={`rules-nav-item rules-nav-level-${heading.level}`}
                  >
                    <a
                      href={`#${heading.id}`}
                      className="rules-nav-link"
                      onClick={(event) => handleRulesNavClick(event, heading.id)}
                    >
                      {heading.title}
                    </a>
                  </li>
                ))}
              </ul>
            </nav>
          </aside>

          <div className="rules-content-scroll">
            <article className="rules-content">
              <Markdown components={markdownComponents}>{processedMarkdown}</Markdown>
            </article>
          </div>
        </div>
        </>
      )}
    </>
  )
}
