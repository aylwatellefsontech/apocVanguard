import { HANDS_KEY } from '../constants'
import type { ArmyCardEntry, Card, HandState } from '../types'

export const MAX_HAND_UNDO = 3

function shuffle(ids: string[]): string[] {
  const next = [...ids]
  for (let i = next.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[next[i], next[j]] = [next[j], next[i]]
  }
  return next
}

function normalizeHandState(state: HandState): HandState {
  return {
    deck: state.deck ?? [],
    hand: state.hand ?? [],
    discard: state.discard ?? [],
    topDeck: state.topDeck ?? [],
  }
}

export function createInitialHand(cards: ArmyCardEntry[]): HandState {
  return {
    deck: shuffle(cards.map((card) => card.id)),
    hand: [],
    discard: [],
    topDeck: [],
  }
}

function loadAllHands(): Record<string, HandState> {
  try {
    const raw = localStorage.getItem(HANDS_KEY)
    if (!raw) return {}
    const parsed: unknown = JSON.parse(raw)
    return parsed && typeof parsed === 'object' ? (parsed as Record<string, HandState>) : {}
  } catch {
    return {}
  }
}

function saveAllHands(hands: Record<string, HandState>): void {
  localStorage.setItem(HANDS_KEY, JSON.stringify(hands))
}

function isValidHandState(cards: ArmyCardEntry[], state: HandState | undefined): state is HandState {
  if (!state || !Array.isArray(state.deck) || !Array.isArray(state.hand) || !Array.isArray(state.discard)) {
    return false
  }

  const topDeck = state.topDeck ?? []
  if (!Array.isArray(topDeck)) {
    return false
  }

  const cardIds = new Set(cards.map((card) => card.id))
  const seen = new Set<string>()
  const allIds = [...state.deck, ...state.hand, ...state.discard, ...topDeck]

  if (allIds.length !== cards.length) {
    return false
  }

  for (const id of allIds) {
    if (!cardIds.has(id) || seen.has(id)) {
      return false
    }
    seen.add(id)
  }

  return true
}

export function loadHandState(armyId: string, cards: ArmyCardEntry[]): HandState {
  const saved = loadAllHands()[armyId]
  if (saved) {
    const normalized = normalizeHandState(saved)
    if (isValidHandState(cards, normalized)) {
      return normalized
    }
  }
  return createInitialHand(cards)
}

export function persistHandState(armyId: string, state: HandState): void {
  const hands = loadAllHands()
  hands[armyId] = state
  saveAllHands(hands)
}

export function cloneHandState(state: HandState): HandState {
  return {
    deck: [...state.deck],
    hand: [...state.hand],
    discard: [...state.discard],
    topDeck: [...state.topDeck],
  }
}

export function getDeckDrawCount(state: HandState): number {
  return state.topDeck.length + state.deck.length
}

export function getDeckDisplayIds(state: HandState): string[] {
  return [...state.topDeck, ...state.deck]
}

export function drawFromDeck(state: HandState, count = 1): HandState {
  const drawCount = Math.min(count, getDeckDrawCount(state))
  if (drawCount === 0) {
    return state
  }

  const topDeck = [...state.topDeck]
  const deck = [...state.deck]
  const drawn: string[] = []

  for (let index = 0; index < drawCount; index += 1) {
    if (topDeck.length > 0) {
      drawn.push(topDeck.shift()!)
      continue
    }

    if (deck.length > 0) {
      drawn.push(deck.shift()!)
    }
  }

  return {
    topDeck,
    deck,
    hand: [...state.hand, ...drawn],
    discard: state.discard,
  }
}

export function drawCardFromDeck(state: HandState, entryId: string): HandState {
  if (state.topDeck.includes(entryId)) {
    return {
      topDeck: state.topDeck.filter((id) => id !== entryId),
      deck: state.deck,
      hand: [...state.hand, entryId],
      discard: state.discard,
    }
  }

  if (!state.deck.includes(entryId)) {
    return state
  }

  return {
    topDeck: state.topDeck,
    deck: state.deck.filter((id) => id !== entryId),
    hand: [...state.hand, entryId],
    discard: state.discard,
  }
}

export function discardFromHand(state: HandState, entryId: string): HandState {
  if (!state.hand.includes(entryId)) {
    return state
  }

  return {
    topDeck: state.topDeck,
    deck: state.deck,
    hand: state.hand.filter((id) => id !== entryId),
    discard: [...state.discard, entryId],
  }
}

export function drawCardFromDiscard(state: HandState, entryId: string): HandState {
  if (!state.discard.includes(entryId)) {
    return state
  }

  return {
    topDeck: state.topDeck,
    deck: state.deck,
    hand: [...state.hand, entryId],
    discard: state.discard.filter((id) => id !== entryId),
  }
}

export function moveToTopDeckFromHand(state: HandState, entryId: string): HandState {
  if (!state.hand.includes(entryId)) {
    return state
  }

  return {
    topDeck: [...state.topDeck, entryId],
    deck: state.deck,
    hand: state.hand.filter((id) => id !== entryId),
    discard: state.discard,
  }
}

export function moveToTopDeckFromDiscard(state: HandState, entryId: string): HandState {
  if (!state.discard.includes(entryId)) {
    return state
  }

  return {
    topDeck: [...state.topDeck, entryId],
    deck: state.deck,
    hand: state.hand,
    discard: state.discard.filter((id) => id !== entryId),
  }
}

export function shuffleBackIntoDeckFromDiscard(state: HandState, entryId: string): HandState {
  if (!state.discard.includes(entryId)) {
    return state
  }

  return {
    topDeck: state.topDeck,
    deck: shuffle([...state.deck, entryId]),
    hand: state.hand,
    discard: state.discard.filter((id) => id !== entryId),
  }
}

export function shuffleBackIntoDeck(state: HandState, entryId: string): HandState {
  if (!state.topDeck.includes(entryId)) {
    return state
  }

  return {
    topDeck: state.topDeck.filter((id) => id !== entryId),
    deck: shuffle([...state.deck, entryId]),
    hand: state.hand,
    discard: state.discard,
  }
}

export function reshuffleDiscardIntoDeck(state: HandState): HandState {
  if (state.discard.length === 0) {
    return state
  }

  return {
    topDeck: state.topDeck,
    deck: shuffle([...state.deck, ...state.discard]),
    hand: state.hand,
    discard: [],
  }
}

export function armyCardToDetail(card: ArmyCardEntry): Card {
  return {
    id: card.cardId ?? card.id,
    name: card.name,
    set: card.set,
    nm: card.nm,
    fac: card.fac,
    type: card.type,
    subType: card.subType,
    facNm: card.facNm,
    ability: card.ability,
  }
}
