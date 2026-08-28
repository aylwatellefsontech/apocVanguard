import { useEffect, useMemo, useState } from 'react'
import Toast from './Toast'
import { encodeArmyExport } from '../utils/armyExport'
import type { ArmyExportSource } from '../utils/armyExport'
import { generateArmyListMarkdown } from '../utils/armyMarkdownExport'
import type { Unit } from '../types'

interface ExportArmyModalProps {
  army: ArmyExportSource
  unitsByEntryId?: Map<string, Unit>
  onClose: () => void
}

export default function ExportArmyModal({
  army,
  unitsByEntryId = new Map(),
  onClose,
}: ExportArmyModalProps) {
  const exportCode = useMemo(() => encodeArmyExport(army), [army])
  const armyMarkdown = useMemo(
    () => generateArmyListMarkdown(army, unitsByEntryId),
    [army, unitsByEntryId],
  )
  const [toastMessage, setToastMessage] = useState<string | null>(null)

  useEffect(() => {
    function handleKeyDown(event: KeyboardEvent) {
      if (event.key === 'Escape') {
        onClose()
      }
    }

    document.addEventListener('keydown', handleKeyDown)
    return () => document.removeEventListener('keydown', handleKeyDown)
  }, [onClose])

  async function copyText(text: string) {
    try {
      await navigator.clipboard.writeText(text)
      setToastMessage('Copied to clipboard.')
    } catch {
      setToastMessage('Could not copy automatically. Select the text and copy manually.')
    }
  }

  return (
    <>
      {toastMessage ? (
        <Toast message={toastMessage} onDismiss={() => setToastMessage(null)} />
      ) : null}
    <div className="modal-backdrop" onClick={onClose}>
      <div
        className="modal-panel import-army-modal export-army-modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="export-army-modal-title"
        onClick={(event) => event.stopPropagation()}
      >
        <header className="confirm-modal-header export-army-modal-header">
          <button
            type="button"
            className="modal-close-btn"
            aria-label="Close"
            onClick={onClose}
          >
            ×
          </button>
          <h2 id="export-army-modal-title">Export Army</h2>
          <p>
            Copy the compact army code or the readable markdown list for{' '}
            <strong>{army.name}</strong>. Either format can be pasted into Build Army → Import.
          </p>
        </header>

        <div className="import-army-modal-body export-army-modal-body">
          <label className="field-label" htmlFor="export-army-code">
            Army export code
          </label>
          <textarea
            id="export-army-code"
            className="import-army-textarea export-army-textarea export-army-code-textarea"
            rows={3}
            readOnly
            value={exportCode}
            onFocus={(event) => event.currentTarget.select()}
          />
          <div className="export-army-copy-row">
            <button
              type="button"
              className="primary-btn"
              onClick={() => copyText(exportCode)}
            >
              Copy Code
            </button>
          </div>

          <label className="field-label export-army-list-label" htmlFor="export-army-markdown">
            Army as markdown
          </label>
          <textarea
            id="export-army-markdown"
            className="import-army-textarea export-army-textarea export-army-markdown-textarea"
            rows={12}
            readOnly
            value={armyMarkdown}
            onFocus={(event) => event.currentTarget.select()}
          />
          <div className="export-army-copy-row">
            <button
              type="button"
              className="primary-btn"
              onClick={() => copyText(armyMarkdown)}
            >
              Copy List
            </button>
          </div>
        </div>
      </div>
    </div>
    </>
  )
}
