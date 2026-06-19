import {
  calculateOptionPoints,
  formatOptionBody,
  formatOptionLabel,
} from '../utils/formatOption.js'

export default function UnitOptions({
  options,
  interactive = false,
  selectedOptionIndexes = [],
  profileStats = null,
  onToggleOption,
  showSelectHint = false,
  highlightSelection = false,
}) {
  if (!options?.length) {
    return null
  }

  const selectedSet = new Set(selectedOptionIndexes)

  return (
    <section>
      <h3>Options</h3>
      {showSelectHint && (
        <p className="options-help muted">
          Add a profile from this unit to your roster, then select it to choose options.
        </p>
      )}
      {interactive && (
        <p className="options-help muted">
          Toggle options for the selected roster entry. Power Rating costs are added
          to the unit total.
        </p>
      )}
      <ul className={`options-list${interactive ? ' options-list-interactive' : ''}`}>
        {options.map((option, index) => {
          const label =
            typeof option === 'string' ? 'Option' : formatOptionLabel(option)
          const body =
            typeof option === 'string' ? option : formatOptionBody(option)
          const points =
            typeof option === 'string'
              ? 0
              : calculateOptionPoints(option, profileStats)
          const isSelected = selectedSet.has(index)

          if (interactive) {
            return (
              <li key={index} className={isSelected ? 'option-item selected' : 'option-item'}>
                <label className="option-toggle">
                  <input
                    type="checkbox"
                    checked={isSelected}
                    onChange={() => onToggleOption?.(index, option)}
                  />
                  <span className="option-toggle-text">
                    <strong>{label}:</strong> {body}
                    {points > 0 && (
                      <span className="option-pts"> +{points} Pt</span>
                    )}
                  </span>
                </label>
              </li>
            )
          }

          if (highlightSelection) {
            return (
              <li
                key={index}
                className={`option-item${isSelected ? ' selected' : ' dimmed'}`}
              >
                <strong>{label}:</strong> {body}
                {isSelected && points > 0 && (
                  <span className="option-pts"> +{points} Pt</span>
                )}
              </li>
            )
          }

          return (
            <li key={index}>
              <strong>{label}:</strong> {body}
            </li>
          )
        })}
      </ul>
    </section>
  )
}
