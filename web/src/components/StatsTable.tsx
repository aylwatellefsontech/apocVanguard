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
      {label && (
        <div className="stats-block-header">
          <h4>{label}</h4>
          {stats.Pt && <span className="stats-block-points">{stats.Pt} Pt</span>}
        </div>
      )}
      <div className="table-scroll">
      <table className="data-table stats-table">
        <thead>
          <tr>
            {STAT_KEYS.map((key) => (
              <th key={key} className={key === 'Pt' ? 'stat-col-pt' : undefined}>
                {key}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          <tr>
            {STAT_KEYS.map((key) => (
              <td key={key} className={key === 'Pt' ? 'stat-col-pt' : undefined}>
                {stats[key] ?? '—'}
              </td>
            ))}
          </tr>
        </tbody>
      </table>
      </div>
    </div>
  )
}
