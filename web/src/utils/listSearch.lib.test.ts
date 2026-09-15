import { describe, expect, it } from '@jest/globals'
import type { Card, Unit } from '../types.js'
import { filterCardsBySearch, filterUnitsBySearch } from './listSearch.lib.js'

function makeUnit(overrides: Partial<Unit> & Pick<Unit, 'no' | 'name' | 'type'>): Unit {
  return { ...overrides }
}

function makeCard(overrides: Partial<Card> & Pick<Card, 'id' | 'name' | 'fac'>): Card {
  return {
    set: 'Core',
    nm: 1,
    type: 'Order',
    ability: '',
    ...overrides,
  }
}

const units: Unit[] = [
  makeUnit({ no: 1, name: 'Boyz', type: 'Troops', keywords: ['Infantry', 'Mob'] }),
  makeUnit({ no: 2, name: 'Warboss', type: 'HQ', keywords: ['Character'] }),
]

const cards: Card[] = [
  makeCard({ id: '1', name: 'Waaagh!', fac: 'Orks', type: 'Order', ability: 'Fight now', set: 'Core', nm: 4 }),
  makeCard({ id: '2', name: 'Fire and Fade', fac: 'Eldar', type: 'Tactic', ability: 'Shoot and move' }),
]

describe('filterUnitsBySearch', () => {
  // US-002 / US-005: search units by name, type, or keyword
  it('returns all units when the query is empty or whitespace', () => {
    expect(filterUnitsBySearch(units, '')).toEqual(units)
    expect(filterUnitsBySearch(units, '   ')).toEqual(units)
  })

  it('returns an empty list when units are missing', () => {
    expect(filterUnitsBySearch(undefined, 'boyz')).toEqual([])
  })

  it('matches unit name, type, or keyword case-insensitively', () => {
    expect(filterUnitsBySearch(units, 'BOYZ').map((unit) => unit.name)).toEqual(['Boyz'])
    expect(filterUnitsBySearch(units, 'hq').map((unit) => unit.name)).toEqual(['Warboss'])
    expect(filterUnitsBySearch(units, 'mob').map((unit) => unit.name)).toEqual(['Boyz'])
  })

  it('returns no units when nothing matches', () => {
    expect(filterUnitsBySearch(units, 'dreadnought')).toEqual([])
  })
})

describe('filterCardsBySearch', () => {
  // US-003 / US-007: search cards and optionally filter by faction
  it('returns all cards when the query is empty and no faction is selected', () => {
    expect(filterCardsBySearch(cards, '', null)).toEqual(cards)
  })

  it('filters to a selected card faction before searching', () => {
    expect(filterCardsBySearch(cards, '', 'Orks').map((card) => card.id)).toEqual(['1'])
  })

  it('matches card name, type, faction, or ability text', () => {
    expect(filterCardsBySearch(cards, 'fade', null).map((card) => card.id)).toEqual(['2'])
    expect(filterCardsBySearch(cards, 'tactic', null).map((card) => card.id)).toEqual(['2'])
    expect(filterCardsBySearch(cards, 'orks', null).map((card) => card.id)).toEqual(['1'])
    expect(filterCardsBySearch(cards, 'fight', null).map((card) => card.id)).toEqual(['1'])
  })

  it('matches set-number only when includeSetNumber is true', () => {
    expect(filterCardsBySearch(cards, 'core-4', null)).toEqual([])
    expect(
      filterCardsBySearch(cards, 'core-4', null, { includeSetNumber: true }).map((card) => card.id),
    ).toEqual(['1'])
  })

  it('returns no cards when nothing matches', () => {
    expect(filterCardsBySearch(cards, 'orbital', null)).toEqual([])
  })
})
