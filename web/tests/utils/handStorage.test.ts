import { describe, expect, it } from '@jest/globals'
import type { ArmyCardEntry, HandState } from '../../src/types.js'
import {
  armyCardToDetail,
  cloneHandState,
  createInitialHand,
  drawCardFromDeck,
  getDeckDisplayIds,
} from '../../src/utils/handStorage.js'

function makeArmyCard(id: string, overrides: Partial<ArmyCardEntry> = {}): ArmyCardEntry {
  return {
    id,
    cardId: `card-${id}`,
    name: `Card ${id}`,
    set: 'Core',
    nm: 1,
    fac: 'Orks',
    type: 'Order',
    ability: '',
    ...overrides,
  }
}

function makeHandState(overrides: Partial<HandState> = {}): HandState {
  return {
    deck: ['d1', 'd2'],
    hand: ['h1'],
    discard: ['x1'],
    topDeck: ['t1'],
    ...overrides,
  }
}

describe('createInitialHand', () => {
  it('puts every card id into the deck and leaves other piles empty', () => {
    const cards = [makeArmyCard('a'), makeArmyCard('b'), makeArmyCard('c')]
    const state = createInitialHand(cards)

    expect(state.hand).toEqual([])
    expect(state.discard).toEqual([])
    expect(state.topDeck).toEqual([])
    expect(state.deck).toHaveLength(3)
    expect(new Set(state.deck)).toEqual(new Set(['a', 'b', 'c']))
  })
})

describe('cloneHandState', () => {
  it('copies piles without sharing array references', () => {
    const original = makeHandState()
    const cloned = cloneHandState(original)

    expect(cloned).toEqual(original)
    expect(cloned.deck).not.toBe(original.deck)
    expect(cloned.hand).not.toBe(original.hand)
    expect(cloned.discard).not.toBe(original.discard)
    expect(cloned.topDeck).not.toBe(original.topDeck)

    cloned.deck.push('extra')
    expect(original.deck).toEqual(['d1', 'd2'])
  })
})

describe('getDeckDisplayIds', () => {
  it('returns topDeck followed by deck', () => {
    expect(
      getDeckDisplayIds(
        makeHandState({
          topDeck: ['t1', 't2'],
          deck: ['d1', 'd2'],
        }),
      ),
    ).toEqual(['t1', 't2', 'd1', 'd2'])
  })
})

describe('drawCardFromDeck', () => {
  it('moves a card from topDeck into hand', () => {
    const next = drawCardFromDeck(
      makeHandState({
        topDeck: ['t1', 't2'],
        deck: ['d1'],
        hand: [],
      }),
      't1',
    )

    expect(next).toEqual({
      topDeck: ['t2'],
      deck: ['d1'],
      hand: ['t1'],
      discard: ['x1'],
    })
  })

  it('moves a card from deck into hand when not on topDeck', () => {
    const next = drawCardFromDeck(
      makeHandState({
        topDeck: ['t1'],
        deck: ['d1', 'd2'],
        hand: [],
        discard: [],
      }),
      'd2',
    )

    expect(next).toEqual({
      topDeck: ['t1'],
      deck: ['d1'],
      hand: ['d2'],
      discard: [],
    })
  })

  it('returns the same state when the card is not drawable', () => {
    const state = makeHandState()
    expect(drawCardFromDeck(state, 'missing')).toBe(state)
  })
})

describe('armyCardToDetail', () => {
  it('maps an army card entry onto a Card using cardId', () => {
    const entry = makeArmyCard('instance-1', {
      cardId: 'Core-1-Orks',
      name: 'Waaagh',
      nm: 4,
      subType: 'Tactic',
      facNm: 2,
      ability: 'Charge!',
    })

    expect(armyCardToDetail(entry)).toEqual({
      id: 'Core-1-Orks',
      name: 'Waaagh',
      set: 'Core',
      nm: 4,
      fac: 'Orks',
      type: 'Order',
      subType: 'Tactic',
      facNm: 2,
      ability: 'Charge!',
    })
  })
})
