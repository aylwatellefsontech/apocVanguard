import { getLocalArmy, getLocalFactions } from './localArmyLists'
import { getLocalCards } from './localCards'
import { getLocalRules } from './localRules'
import type { ArmyList, CardsResponse, FactionSummary } from '../types'

export async function fetchFactions(): Promise<FactionSummary[]> {
  return getLocalFactions()
}

export async function fetchArmy(factionId: string): Promise<ArmyList> {
  const army = getLocalArmy(factionId)
  if (!army) {
    throw new Error('Faction not found')
  }
  return army
}

export async function fetchCards(): Promise<CardsResponse> {
  return getLocalCards()
}

export async function fetchRules(): Promise<string> {
  return getLocalRules()
}
