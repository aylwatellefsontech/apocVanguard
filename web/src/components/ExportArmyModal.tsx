import { useEffect, useState } from 'react'
import { encodeArmyExport } from '../utils/armyExport'
import type { ArmyExportSource } from '../utils/armyExport'

interface ExportArmyModalProps {
  army: ArmyExportSource
  onClose: () => void
}

export default function ExportArmyModal({ army, onClose }: ExportArmyModalProps) {
  const exportCode = encodeArmyExport(army)
  const [copyMessage, setCopyMessage] = useState<string | null>(null)

  useEffect(() => {
    function handleKeyDown(event: KeyboardEvent) {
      if (event.key === 'Escape') {
        onClose()
      }
    }

    document.addEventListener('keydown', handleKeyDown)
    return () => document.removeEventListener('keydown', handleKeyDown)
  }, [onClose])

  async function handleCopy() {
    try {
      await navigator.clipboard.writeText(exportCode)
      setCopyMessage('Copied to clipboard.')
    } catch {
      setCopyMessage('Could not copy automatically. Select the text and copy manually.')
    }
  }

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div
        className="modal-panel import-army-modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="export-army-modal-title"
        onClick={(event) => event.stopPropagation()}
      >
        <header className="confirm-modal-header">
          <h2 id="export-army-modal-title">Export Army</h2>
          <p>
            Copy this compact army code and paste it into Build Army → Import to restore{' '}
            <strong>{army.name}</strong>. The code starts with a readable label like{' '}
            <code>[Army Name.YYYY-MM-DD]</code>.
          </p>
        </header>

        <div className="import-army-modal-body">
          <label className="field-label" htmlFor="export-army-code">
            Army export code
          </label>
          <textarea
            id="export-army-code"
            className="import-army-textarea export-army-textarea"
            rows={8}
            readOnly
            value={exportCode}
            onFocus={(event) => event.currentTarget.select()}
          />
          {copyMessage ? <p className="form-success">{copyMessage}</p> : null}
        </div>

        <div className="confirm-modal-actions">
          <button type="button" className="secondary-btn" onClick={onClose}>
            Close
          </button>
          <button type="button" className="primary-btn" onClick={handleCopy}>
            Copy Code
          </button>
        </div>
      </div>
    </div>
  )
}
