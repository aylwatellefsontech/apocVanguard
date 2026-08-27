import { useEffect, useState } from 'react'

interface ImportArmyModalProps {
  onClose: () => void
  onImport: (markdown: string) => void
  error?: string | null
}

export default function ImportArmyModal({ onClose, onImport, error = null }: ImportArmyModalProps) {
  const [markdown, setMarkdown] = useState('')

  useEffect(() => {
    function handleKeyDown(event: KeyboardEvent) {
      if (event.key === 'Escape') {
        onClose()
      }
    }

    document.addEventListener('keydown', handleKeyDown)
    return () => document.removeEventListener('keydown', handleKeyDown)
  }, [onClose])

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div
        className="modal-panel import-army-modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="import-army-modal-title"
        onClick={(event) => event.stopPropagation()}
      >
        <header className="confirm-modal-header">
          <h2 id="import-army-modal-title">Import Army</h2>
          <p>Paste an Apocalypse Vanguard army export code below, then import it into your saved armies.</p>
        </header>

        <div className="import-army-modal-body">
          <label className="field-label" htmlFor="import-army-markdown">
            Army export code
          </label>
          <textarea
            id="import-army-markdown"
            className="import-army-textarea"
            rows={8}
            value={markdown}
            onChange={(event) => setMarkdown(event.target.value)}
            placeholder="Paste exported army code here (e.g. [My Army.2026-08-27]AV1.…)…"
          />
          {error ? <p className="form-error">{error}</p> : null}
        </div>

        <div className="confirm-modal-actions">
          <button type="button" className="secondary-btn" onClick={onClose}>
            Cancel
          </button>
          <button
            type="button"
            className="primary-btn"
            onClick={() => onImport(markdown)}
            disabled={!markdown.trim()}
          >
            Import
          </button>
        </div>
      </div>
    </div>
  )
}
