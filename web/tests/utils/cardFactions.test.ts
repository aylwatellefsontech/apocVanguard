import { describe, expect, it } from '@jest/globals'
import type { Card } from '../../src/types.js'
import { cardMatchesArmyFaction, getBaseApocCards, getCardFactionsForArmy } from '../../src/utils/cardFactions.js'

function makeCard(overrides: Partial<Card> & Pick<Card, 'id' | 'fac'>): Card {
  return {
    set: 'Core',
    nm: 1,
    name: 'Test',
    type: 'Order',
    ...overrides,
  }
}

describe('getCardFactionsForArmy', () => {
  it('returns mapped factions plus Apoc for Knights', () => {
    expect(getCardFactionsForArmy('Knights')).toEqual(['Imperial Knights', 'Knights', 'Traitor Knights', 'Apoc'])
  })

  it('returns the army name plus Apoc when unmapped', () => {
    expect(getCardFactionsForArmy('Orks')).toEqual(['Orks', 'Apoc'])
  })
})

describe('cardMatchesArmyFaction', () => {
  it('matches cards whose faction is allowed for the army', () => {
    expect(cardMatchesArmyFaction(makeCard({ id: '1', fac: 'Apoc' }), 'Orks')).toBe(true)
    expect(cardMatchesArmyFaction(makeCard({ id: '2', fac: 'Imperial Knights' }), 'Knights')).toBe(true)
  })

  it('returns false for empty faction names or mismatched card factions', () => {
    expect(cardMatchesArmyFaction(makeCard({ id: '1', fac: 'Orks' }), '')).toBe(false)
    expect(cardMatchesArmyFaction(makeCard({ id: '2', fac: '' }), 'Orks')).toBe(false)
    expect(cardMatchesArmyFaction(makeCard({ id: '3', fac: 'Eldar' }), 'Orks')).toBe(false)
  })
})

describe('getBaseApocCards', () => {
  // US-007: browse base Apocalypse cards
  it('keeps only Apoc cards with a base subtype', () => {
    const cards = [
      makeCard({ id: '1', fac: 'Apoc', subType: 'Base', name: 'Reserves' }),
      makeCard({ id: '2', fac: 'Apoc', subType: 'base', name: 'Lowercase' }),
      makeCard({ id: '3', fac: 'Apoc', subType: 'Tactic', name: 'Not base' }),
      makeCard({ id: '4', fac: 'Orks', subType: 'Base', name: 'Faction' }),
    ]

    expect(getBaseApocCards(cards).map((card) => card.id)).toEqual(['1', '2'])
  })

  it('returns an empty list when no base Apoc cards are present', () => {
    expect(getBaseApocCards([makeCard({ id: '1', fac: 'Orks' })])).toEqual([])
  })
})
