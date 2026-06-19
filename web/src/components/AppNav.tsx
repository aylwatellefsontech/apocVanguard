import type { AppPage } from '../types'

interface AppNavProps {
  page: AppPage
  onNavigate: (page: AppPage) => void
}

export default function AppNav({ page, onNavigate }: AppNavProps) {
  return (
    <nav className="app-nav" aria-label="Main">
      <button
        type="button"
        className={page === 'browse' ? 'nav-btn active' : 'nav-btn'}
        onClick={() => onNavigate('browse')}
      >
        Browse
      </button>
      <button
        type="button"
        className={page === 'armies' ? 'nav-btn active' : 'nav-btn'}
        onClick={() => onNavigate('armies')}
      >
        My Armies
      </button>
      <button
        type="button"
        className={page === 'build' ? 'nav-btn active' : 'nav-btn'}
        onClick={() => onNavigate('build')}
      >
        Build Army
      </button>
      <button
        type="button"
        className={page === 'rules' ? 'nav-btn active' : 'nav-btn'}
        onClick={() => onNavigate('rules')}
      >
        Rules
      </button>
    </nav>
  )
}
