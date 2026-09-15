import type { Card, Unit } from '../types'

export function filterUnitsBySearch(units: Unit[] | undefined, search: string): Unit[] {
  if (!units) return []
  const query = search.trim().toLowerCase()
  if (!query) return units
  return units.filter(
    (unit) =>
      unit.name.toLowerCase().includes(query) ||
      unit.type.toLowerCase().includes(query) ||
      unit.keywords?.some((keyword) => keyword.toLowerCase().includes(query)),
  )
}

export function filterCardsBySearch(
  cards: Card[],
  search: string,
  selectedCardFac: string | null,
  options: { includeSetNumber?: boolean } = {},
): Card[] {
  let list = cards
  if (selectedCardFac) {
    list = list.filter((card) => card.fac === selectedCardFac)
  }
  const query = search.trim().toLowerCase()
  if (!query) return list
  return list.filter((card) => {
    if (
      card.name.toLowerCase().includes(query) ||
      card.type?.toLowerCase().includes(query) ||
      card.fac?.toLowerCase().includes(query) ||
      card.ability?.toLowerCase().includes(query)
    ) {
      return true
    }
    return Boolean(
      options.includeSetNumber && `${card.set}-${card.nm}`.toLowerCase().includes(query),
    )
  })
}
