import { createRootRoute, createRoute, createRouter, Outlet } from '@tanstack/react-router'
import './App.css'
import AppNav from './components/AppNav'
import BrowsePage from './pages/BrowsePage'
import BuildArmyPage from './pages/BuildArmyPage'
import ViewArmiesPage from './pages/ViewArmiesPage'
import RulesPage from './pages/RulesPage'

export interface BrowseSearch {
  faction?: string
  cards?: string
}

function RootLayout() {
  return (
    <div className="app">
      <AppNav />
      <Outlet />
    </div>
  )
}

const rootRoute = createRootRoute({
  component: RootLayout,
})

const indexRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/',
  validateSearch: (search: Record<string, unknown>): BrowseSearch => {
    const result: BrowseSearch = {}

    const faction =
      typeof search.faction === 'string' && search.faction.length > 0 ? search.faction : undefined

    if (faction) {
      result.faction = faction
      return result
    }

    if ('cards' in search) {
      result.cards = typeof search.cards === 'string' ? search.cards : ''
    }

    return result
  },
  component: BrowsePage,
})

const armiesRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/armies',
  component: ViewArmiesPage,
})

const buildRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/build',
  validateSearch: (search: Record<string, unknown>): { armyId?: string } => ({
    armyId: typeof search.armyId === 'string' ? search.armyId : undefined,
  }),
  component: BuildArmyPage,
})

const rulesRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/rules',
  component: RulesPage,
})

const routeTree = rootRoute.addChildren([indexRoute, armiesRoute, buildRoute, rulesRoute])

export const router = createRouter({
  routeTree,
  basepath: '/apocVanguard',
})

declare module '@tanstack/react-router' {
  interface Register {
    router: typeof router
  }
}

export { buildRoute, indexRoute as browseRoute }
