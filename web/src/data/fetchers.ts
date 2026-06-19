import { isApiDatasource } from './datasource'
import { getLocalArmy, getLocalFactions } from './localArmyLists'
import { getLocalCards } from './localCards'
import { getLocalRules } from './localRules'
import type { ArmyList, CardsResponse, FactionSummary } from '../types'

async function fetchJson<T>(url: string, errorMessage: string): Promise<T> {
  const response = await fetch(url)
  if (!response.ok) {
    throw new Error(errorMessage)
  }
  return response.json() as Promise<T>
}

export async function fetchFactions(): Promise<FactionSummary[]> {
  if (isApiDatasource()) {
    return fetchJson('/api/factions', 'Failed to load factions')
  }
  return getLocalFactions()
}

export async function fetchArmy(factionId: string): Promise<ArmyList> {
  if (isApiDatasource()) {
    return fetchJson(
      `/api/factions/${encodeURIComponent(factionId)}`,
      'Failed to load army list',
    )
  }

  const army = getLocalArmy(factionId)
  if (!army) {
    throw new Error('Faction not found')
  }
  return army
}

export async function fetchCards(): Promise<CardsResponse> {
  if (isApiDatasource()) {
    const response = await fetch('/api/cards')
    const contentType = response.headers.get('content-type') ?? ''
    if (!response.ok) {
      throw new Error('Failed to load cards')
    }
    if (!contentType.includes('application/json')) {
      throw new Error(
        'Cards API returned an invalid response. Restart with npm run dev from the web folder.',
      )
    }
    const data = (await response.json()) as CardsResponse & { error?: string }
    if (data.error) {
      throw new Error(data.error)
    }
    return data
  }
  return getLocalCards()
}

export async function fetchRules(): Promise<string> {
  if (isApiDatasource()) {
    const response = await fetch('/api/rules')
    const contentType = response.headers.get('content-type') ?? ''
    if (!response.ok) {
      throw new Error('Failed to load rules')
    }
    if (!contentType.includes('application/json')) {
      throw new Error(
        'Rules API returned an invalid response. Restart with npm run dev from the web folder.',
      )
    }
    const data = (await response.json()) as { markdown?: string; error?: string }
    if (data.error) {
      throw new Error(data.error)
    }
    return data.markdown ?? ''
  }
  return getLocalRules()
}
