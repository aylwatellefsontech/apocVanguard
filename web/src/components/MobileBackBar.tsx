interface MobileBackBarProps {
  label: string
  onBack: () => void
}

export default function MobileBackBar({ label, onBack }: MobileBackBarProps) {
  return (
    <div className="mobile-back-bar">
      <button type="button" className="mobile-back-btn" onClick={onBack}>
        ← Back
      </button>
      <span className="mobile-back-label">{label}</span>
    </div>
  )
}
