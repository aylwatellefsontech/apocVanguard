import { describe, expect, it } from '@jest/globals'
import { mergeCardFiles } from '../../src/data/mergeCards.js'

describe('mergeCardFiles', () => {
  it('merges cards from multiple sources and builds faction counts', () => {
    const result = mergeCardFiles([
      {
        source: 'a',
        cards: [
          { set: 'Core', nm: 2, fac: 'Orks', name: 'Waaagh', type: 'Order' },
          { set: 'Core', nm: 1, fac: 'Apoc', name: 'Base', type: 'Strategic' },
        ],
      },
      {
        source: 'b',
        cards: [{ set: 'Core', nm: 3, fac: 'Orks', name: 'More', type: 'Order' }],
      },
    ])

    expect(result.total).toBe(3)
    expect(result.cards.map((card) => card.id)).toEqual(['Core-1-Apoc', 'Core-2-Orks', 'Core-3-Orks'])
    expect(result.factions).toEqual([
      { fac: 'Apoc', count: 1 },
      { fac: 'Orks', count: 2 },
    ])
  })

  it('skips cards with empty faction and dedupes by set-nm-fac', () => {
    const result = mergeCardFiles([
      {
        cards: [
          { set: 'Core', nm: 1, fac: '  ', name: 'Blank', type: 'Order' },
          { set: 'Core', nm: 1, fac: 'Orks', name: 'First', type: 'Order' },
          { set: 'Core', nm: 1, fac: 'Orks', name: 'Duplicate', type: 'Order' },
        ],
      },
    ])

    expect(result.total).toBe(1)
    expect(result.cards[0]?.name).toBe('First')
  })
})
