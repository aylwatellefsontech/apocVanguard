import { Link } from '@tanstack/react-router'

export default function AppNav() {
  return (
    <nav className="app-nav" aria-label="Main">
      <Link
        to="/"
        className="nav-btn"
        activeOptions={{ exact: true }}
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
