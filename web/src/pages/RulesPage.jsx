import Markdown from 'react-markdown'
import { useRules } from '../hooks/useRules.js'
import {
  createHeadingComponent,
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

export default function RulesPage() {
  const { markdown, loading, error } = useRules()

  return (
    <main className="rules-page">
      <header className="app-header rules-header">
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
        <article className="rules-content">
          <Markdown components={markdownComponents}>
            {preprocessRulesMarkdown(markdown)}
          </Markdown>
        </article>
      )}
    </main>
  )
}
