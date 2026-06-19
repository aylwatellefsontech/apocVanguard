import { HANDS_KEY } from '../constants.js'

export const MAX_HAND_UNDO = 3

function shuffle(ids) {
  const next = [...ids]
  for (let i = next.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[next[i], next[j]] = [next[j], next[i]]
  }
  return next
}

export function createInitialHand(cards) {
  return {
    deck: shuffle(cards.map((card) => card.id)),
    hand: [],
    discard: [],
  }
}

function loadAllHands() {
  try {
    const raw = localStorage.getItem(HANDS_KEY)
    if (!raw) return {}
    const parsed = JSON.parse(raw)
    return parsed && typeof parsed === 'object' ? parsed : {}
  } catch {
    return {}
  }
}

function saveAllHands(hands) {
  localStorage.setItem(HANDS_KEY, JSON.stringify(hands))
}

function isValidHandState(cards, state) {
  if (!state || !Array.isArray(state.deck) || !Array.isArray(state.hand) || !Array.isArray(state.discard)) {
    return false
  }

  const cardIds = new Set(cards.map((card) => card.id))
  const seen = new Set()
  const allIds = [...state.deck, ...state.hand, ...state.discard]

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

export function loadHandState(armyId, cards) {
  const saved = loadAllHands()[armyId]
  if (saved && isValidHandState(cards, saved)) {
    return saved
  }
  return createInitialHand(cards)
}

export function persistHandState(armyId, state) {
  const hands = loadAllHands()
  hands[armyId] = state
  saveAllHands(hands)
}

export function cloneHandState(state) {
  return {
    deck: [...state.deck],
    hand: [...state.hand],
    discard: [...state.discard],
  }
}

export function drawFromDeck(state, count = 1) {
  const drawCount = Math.min(count, state.deck.length)
  if (drawCount === 0) {
    return state
  }

  const drawn = state.deck.slice(0, drawCount)
  return {
    deck: state.deck.slice(drawCount),
    hand: [...state.hand, ...drawn],
    discard: state.discard,
  }
}

export function drawCardFromDeck(state, entryId) {
  if (!state.deck.includes(entryId)) {
    return state
  }

  return {
    deck: state.deck.filter((id) => id !== entryId),
    hand: [...state.hand, entryId],
    discard: state.discard,
  }
}

export function discardFromHand(state, entryId) {
  if (!state.hand.includes(entryId)) {
    return state
  }

  return {
    deck: state.deck,
    hand: state.hand.filter((id) => id !== entryId),
    discard: [...state.discard, entryId],
  }
}

export function drawCardFromDiscard(state, entryId) {
  if (!state.discard.includes(entryId)) {
    return state
  }

  return {
    deck: state.deck,
    hand: [...state.hand, entryId],
    discard: state.discard.filter((id) => id !== entryId),
  }
}

export function reshuffleDiscardIntoDeck(state) {
  if (state.discard.length === 0) {
    return state
  }

  return {
    deck: shuffle([...state.deck, ...state.discard]),
    hand: state.hand,
    discard: [],
  }
}

export function armyCardToDetail(card) {
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
