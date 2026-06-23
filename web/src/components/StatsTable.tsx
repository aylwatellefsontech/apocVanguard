import { STAT_KEYS } from '../constants'
import type { UnitStats } from '../types'

interface StatsTableProps {
  stats?: UnitStats | null
  label?: string
}

export default function StatsTable({ stats, label }: StatsTableProps) {
  if (!stats) return null

  return (
    <div className="stats-block">
      {label && <h4>{label}</h4>}
      <div className="table-scroll">
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
    </div>
  )
}
