import type { Card } from '../types'

const ARMY_TO_CARD_FACTIONS: Record<string, string[]> = {
  Knights: ['Imperial Knights', 'Knights', 'Traitor Knights'],
  'Chaos Marines': ['Chaos Marines', 'Chaos'],
}

export function getCardFactionsForArmy(factionName: string): string[] {
  const mapped = ARMY_TO_CARD_FACTIONS[factionName] ?? [factionName]
  return [...new Set([...mapped, 'Apoc'])]
}

export function cardMatchesArmyFaction(card: Card, factionName: string): boolean {
  if (!factionName || !card.fac) return false
  return getCardFactionsForArmy(factionName).includes(card.fac)
}
