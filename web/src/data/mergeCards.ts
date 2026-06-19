import type { Card, CardFactionCount, CardsResponse } from '../types'

export interface CardFileData {
  source?: string
  cards?: Array<Record<string, unknown>>
}

export function mergeCardFiles(sources: CardFileData[]): CardsResponse {
  const cardsById = new Map<string, Card>()

  for (const data of sources) {
    for (const card of data.cards ?? []) {
      const facRaw = typeof card.fac === 'string' ? card.fac.trim() : ''
      if (!facRaw) {
        continue
      }

      const set = String(card.set ?? '?')
      const nm = Number(card.nm ?? 0)
      const id = `${set}-${nm}-${facRaw}`

      if (cardsById.has(id)) {
        continue
      }

      cardsById.set(id, {
        id,
        set,
        nm,
        fac: facRaw,
        name: String(card.name ?? ''),
        type: String(card.type ?? ''),
        subType: (card.subType as string | null | undefined) ?? null,
        facNm: (card.facNm as number | null | undefined) ?? null,
        ability: typeof card.ability === 'string' ? card.ability : undefined,
        source: data.source,
      })
    }
  }

  const cards = [...cardsById.values()]

  cards.sort((a, b) => {
    const setCompare = String(a.set ?? '').localeCompare(String(b.set ?? ''))
    if (setCompare !== 0) return setCompare
    return (a.nm ?? 0) - (b.nm ?? 0)
  })

  const facCounts = new Map<string, number>()
  for (const card of cards) {
    facCounts.set(card.fac, (facCounts.get(card.fac) ?? 0) + 1)
  }

  const factions: CardFactionCount[] = [...facCounts.entries()]
    .map(([fac, count]) => ({ fac, count }))
    .sort((a, b) => a.fac.localeCompare(b.fac))

  return { cards, factions, total: cards.length }
}
