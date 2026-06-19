import { useMemo } from 'react'
import Markdown from 'react-markdown'
import { useRules } from '../hooks/useRules.js'
import {
  createHeadingComponent,
  extractRulesHeadings,
  preprocessRulesMarkdown,
} from '../utils/rulesMarkdown.jsx'

const markdownComponents = {
  h1: createHeadingComponent('h1'),
  h2: createHeadingComponent('h2'),
  h3: createHeadingComponent('h3'),
  h4: createHeadingComponent('h4'),
  h5: createHeadingComponent('h5'),
  h6: createHeadingComponent('h6'),
}

function scrollToRulesHeading(event, id) {
  event.preventDefault()
  document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  window.history.replaceState(null, '', `#${id}`)
}

export default function RulesPage() {
  const { markdown, loading, error } = useRules()
  const processedMarkdown = useMemo(
    () => (markdown ? preprocessRulesMarkdown(markdown) : ''),
    [markdown],
  )
  const headings = useMemo(
    () => extractRulesHeadings(processedMarkdown),
    [processedMarkdown],
  )

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
        <div className="rules-body">
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
                      onClick={(event) => scrollToRulesHeading(event, heading.id)}
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
              <Markdown components={markdownComponents}>
                {processedMarkdown}
              </Markdown>
            </article>
          </div>
        </div>
      )}
    </>
  )
}
