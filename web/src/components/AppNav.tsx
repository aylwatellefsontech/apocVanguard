import { Link } from '@tanstack/react-router'
import vanguardIcon from '../assets/factions/vanguard.svg?raw'
import { normalizeFactionIconSvg } from '../utils/normalizeFactionIconSvg'

const VANGUARD_LOGO = normalizeFactionIconSvg(vanguardIcon)

export default function AppNav() {
  return (
    <nav className="app-nav" aria-label="Main">
      <Link to="/" className="app-nav-logo" aria-label="Home">
        <span aria-hidden="true" dangerouslySetInnerHTML={{ __html: VANGUARD_LOGO }} />
      </Link>
      <Link
        to="/browse"
        className="nav-btn"
        activeProps={{ className: 'nav-btn active' }}
      >
        Browse
      </Link>
      <Link
        to="/armies"
        className="nav-btn"
        activeProps={{ className: 'nav-btn active' }}
      >
        My Armies
      </Link>
      <Link
        to="/build"
        search={{}}
        className="nav-btn"
        activeProps={{ className: 'nav-btn active' }}
      >
        Build Army
      </Link>
      <Link
        to="/rules"
        className="nav-btn"
        activeProps={{ className: 'nav-btn active' }}
      >
        Rules
      </Link>
    </nav>
  )
}
