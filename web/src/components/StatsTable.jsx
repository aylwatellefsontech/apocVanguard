import { STAT_KEYS } from '../constants.js'

export default function StatsTable({ stats, label }) {
  if (!stats) return null

  return (
    <div className="stats-block">
      {label && <h4>{label}</h4>}
      <table className="data-table stats-table">
        <thead>
          <tr>
            {STAT_KEYS.map((key) => (
              <th key={key}>{key}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          <tr>
            {STAT_KEYS.map((key) => (
              <td key={key}>{stats[key] ?? '—'}</td>
            ))}
          </tr>
        </tbody>
      </table>
    </div>
  )
}
