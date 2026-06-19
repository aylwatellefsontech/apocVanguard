const ARMY_TO_CARD_FACTIONS = {
  Knights: ['Imperial Knights', 'Knights', 'Traitor Knights'],
  'Chaos Marines': ['Chaos Marines', 'Chaos'],
}

export function getCardFactionsForArmy(factionName) {
  const mapped = ARMY_TO_CARD_FACTIONS[factionName] ?? [factionName]
  return [...new Set([...mapped, 'Apoc'])]
}

export function cardMatchesArmyFaction(card, factionName) {
  if (!factionName || !card.fac) return false
  return getCardFactionsForArmy(factionName).includes(card.fac)
}
