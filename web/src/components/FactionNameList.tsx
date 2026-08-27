import FactionIcon from './FactionIcon'

interface FactionNameListProps {
  names: string[]
}

export default function FactionNameList({ names }: FactionNameListProps) {
  if (names.length === 0) {
    return null
  }

  return (
    <span className="faction-name-list">
      {names.map((name, index) => (
        <span key={`${name}-${index}`} className="faction-name-item">
          {index > 0 ? <span className="faction-name-separator">/</span> : null}
          <FactionIcon name={name} />
          <span>{name}</span>
        </span>
      ))}
    </span>
  )
}
