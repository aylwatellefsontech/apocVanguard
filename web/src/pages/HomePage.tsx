import { Link } from '@tanstack/react-router'
import FactionIcon from '../components/FactionIcon'
import { useFactions } from '../hooks/useFactions'
import vanguardIcon from '../assets/factions/vanguard.svg?raw'
import { hasFactionIcon } from '../utils/factionIcons'
import { normalizeFactionIconSvg } from '../utils/normalizeFactionIconSvg'

const VANGUARD_LOGO = normalizeFactionIconSvg(vanguardIcon)

const HOME_LEDE =
  'Apocalypse Vanguard is a cleaned up fan version of 40k Apocalypse (2019), meant to play games of Apocalypse in a smaller footprint, and faster.'

export default function HomePage() {
  const { factions, loading, error } = useFactions()
  const browseFactions = factions.filter((faction) => hasFactionIcon(faction.faction))

  return (
    <main className="home-page">
      <section className="home-hero">
        <div
          className="home-logo"
          aria-hidden="true"
          dangerouslySetInnerHTML={{ __html: VANGUARD_LOGO }}
        />
        <h1 className="home-title">Apocalypse Vanguard</h1>
        <p className="home-lede">{HOME_LEDE}</p>
      </section>
      <section className="home-rules">
        <h2>Rules</h2>
        <p className="home-rules-lede">
          <Link to="/rules" className="home-rules-link">
            See the Rules
          </Link>
        </p>
      </section>


      <section className="home-factions">
        <h2>Factions</h2>
        {error && <p className="error-banner home-message">{error}</p>}
        {loading ? (
          <p className="muted home-message">Loading factions…</p>
        ) : (
          <div className="faction-grid">
            {browseFactions.map((faction) => (
              <Link
                key={faction.id}
                to="/browse"
                search={{ faction: faction.id }}
                className="faction-grid-link"
              >
                <FactionIcon name={faction.faction} className="faction-grid-icon" />
                <span className="faction-grid-label">{faction.faction}</span>
              </Link>
            ))}
          </div>
        )}
      </section>
      <section className="home-updated">
        <p className="home-updated">Last Updated: 2026 08 29</p>
      </section>
    </main>
  )
}
