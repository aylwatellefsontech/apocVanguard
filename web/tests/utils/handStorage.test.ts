import { beforeEach, describe, expect, it } from '@jest/globals'
import { HANDS_KEY } from '../../src/constants.js'
import type { ArmyCardEntry, HandState } from '../../src/types.js'
import {
  armyCardToDetail,
  cloneHandState,
  createInitialHand,
  discardFromHand,
  drawCardFromDeck,
  drawCardFromDiscard,
  drawFromDeck,
  getDeckDisplayIds,
  loadHandState,
  moveToTopDeckFromDiscard,
  moveToTopDeckFromHand,
  persistHandState,
  reshuffleDiscardIntoDeck,
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

describe('drawFromDeck', () => {
  // US-014: draw, discard, pin, and reshuffle command cards
  it('draws from topDeck first, then deck', () => {
    const next = drawFromDeck(
      makeHandState({
        topDeck: ['t1'],
        deck: ['d1', 'd2'],
        hand: [],
        discard: [],
      }),
      2,
    )

    expect(next.hand).toEqual(['t1', 'd1'])
    expect(next.topDeck).toEqual([])
    expect(next.deck).toEqual(['d2'])
  })

  it('returns the same state when the deck is empty', () => {
    const state = makeHandState({ topDeck: [], deck: [], hand: [], discard: [] })
    expect(drawFromDeck(state, 1)).toBe(state)
  })
})

describe('discardFromHand', () => {
  it('moves a card from hand to discard', () => {
    const next = discardFromHand(makeHandState({ hand: ['h1', 'h2'], discard: [] }), 'h1')
    expect(next.hand).toEqual(['h2'])
    expect(next.discard).toEqual(['h1'])
  })

  it('returns the same state when the card is not in hand', () => {
    const state = makeHandState()
    expect(discardFromHand(state, 'missing')).toBe(state)
  })
})

describe('drawCardFromDiscard', () => {
  it('moves a card from discard into hand', () => {
    const next = drawCardFromDiscard(makeHandState({ hand: [], discard: ['x1'] }), 'x1')
    expect(next.hand).toEqual(['x1'])
    expect(next.discard).toEqual([])
  })
})

describe('moveToTopDeckFromHand', () => {
  it('pins a hand card onto the top of the deck', () => {
    const next = moveToTopDeckFromHand(
      makeHandState({ topDeck: ['t1'], hand: ['h1'], discard: [] }),
      'h1',
    )
    expect(next.topDeck).toEqual(['t1', 'h1'])
    expect(next.hand).toEqual([])
  })
})

describe('moveToTopDeckFromDiscard', () => {
  it('pins a discarded card onto the top of the deck', () => {
    const next = moveToTopDeckFromDiscard(
      makeHandState({ topDeck: [], hand: [], discard: ['x1'] }),
      'x1',
    )
    expect(next.topDeck).toEqual(['x1'])
    expect(next.discard).toEqual([])
  })
})

describe('reshuffleDiscardIntoDeck', () => {
  it('moves discard into the deck and leaves discard empty', () => {
    const next = reshuffleDiscardIntoDeck(
      makeHandState({ deck: ['d1'], discard: ['x1', 'x2'], hand: [], topDeck: [] }),
    )
    expect(next.discard).toEqual([])
    expect(next.deck).toHaveLength(3)
    expect(new Set(next.deck)).toEqual(new Set(['d1', 'x1', 'x2']))
  })

  it('returns the same state when discard is empty', () => {
    const state = makeHandState({ discard: [] })
    expect(reshuffleDiscardIntoDeck(state)).toBe(state)
  })
})

function installMemoryLocalStorage() {
  const store = new Map<string, string>()
  Object.defineProperty(globalThis, 'localStorage', {
    configurable: true,
    value: {
      getItem: (key: string) => store.get(key) ?? null,
      setItem: (key: string, value: string) => {
        store.set(key, value)
      },
      removeItem: (key: string) => {
        store.delete(key)
      },
      clear: () => store.clear(),
    },
  })
}

describe('persistHandState', () => {
  beforeEach(() => {
    installMemoryLocalStorage()
  })

  it('stores hand state per army and restores it after reload', () => {
    const cards = [makeArmyCard('a'), makeArmyCard('b')]
    const state = makeHandState({
      deck: ['a'],
      hand: ['b'],
      discard: [],
      topDeck: [],
    })

    persistHandState('army-1', state)
    expect(localStorage.getItem(HANDS_KEY)).toContain('army-1')
    expect(loadHandState('army-1', cards)).toEqual(state)
  })
})
