import { MAX_SAVED_ARMIES, SAVED_ARMIES_KEY } from '../constants.js'

export function loadSavedArmies() {
  try {
    const raw = localStorage.getItem(SAVED_ARMIES_KEY)
    if (!raw) return []
    const parsed = JSON.parse(raw)
    return Array.isArray(parsed) ? parsed.map(normalizeSavedArmy) : []
  } catch {
    return []
  }
}

export function normalizeRosterEntry(entry) {
  const profilePoints = entry.profilePoints ?? entry.points ?? 0
  const selectedOptions = Array.isArray(entry.selectedOptions)
    ? entry.selectedOptions
    : []
  const optionPoints = selectedOptions.reduce((sum, option) => sum + (option.points ?? 0), 0)

  return {
    ...entry,
    profilePoints,
    selectedOptions,
    points: profilePoints + optionPoints,
  }
}

function normalizeSavedArmy(army) {
  const roster = Array.isArray(army.roster) ? army.roster.map(normalizeRosterEntry) : []
  const cards = Array.isArray(army.cards) ? army.cards : []
  return {
    ...army,
    roster,
    cards,
    totalPoints: roster.reduce((sum, entry) => sum + entry.points, 0),
  }
}

export function persistSavedArmies(armies) {
  localStorage.setItem(SAVED_ARMIES_KEY, JSON.stringify(armies))
}

export function saveArmy(army) {
  const armies = loadSavedArmies()
  if (armies.length >= MAX_SAVED_ARMIES && !armies.some((entry) => entry.id === army.id)) {
    return { ok: false, error: `You can only save up to ${MAX_SAVED_ARMIES} armies.` }
  }

  const normalized = normalizeSavedArmy(army)
  const next = armies.some((entry) => entry.id === army.id)
    ? armies.map((entry) => (entry.id === army.id ? normalized : entry))
    : [...armies, normalized]

  persistSavedArmies(next)
  return { ok: true, armies: next }
}

export function deleteSavedArmy(id) {
  const next = loadSavedArmies().filter((army) => army.id !== id)
  persistSavedArmies(next)
  return next
}

export function createArmyCardEntry(card) {
  return {
    id: crypto.randomUUID(),
    cardId: card.id,
    name: card.name,
    set: card.set,
    nm: card.nm,
    fac: card.fac,
    type: card.type,
    subType: card.subType ?? null,
    facNm: card.facNm ?? null,
    ability: card.ability ?? '',
  }
}

export function createRosterEntry(unit, profile) {
  return {
    id: crypto.randomUUID(),
    unitNo: unit.no,
    unitName: unit.name,
    unitType: unit.type,
    profileKind: profile.kind,
    profileIndex: profile.index,
    profileLabel: profile.label,
    profilePoints: profile.points,
    modelCount: profile.stats?.N ?? null,
    selectedOptions: [],
    points: profile.points,
  }
}

export function toggleRosterOption(entry, optionIndex, optionSummary) {
  const exists = entry.selectedOptions.some((option) => option.index === optionIndex)
  const selectedOptions = exists
    ? entry.selectedOptions.filter((option) => option.index !== optionIndex)
    : [...entry.selectedOptions, { index: optionIndex, ...optionSummary }]

  const optionPoints = selectedOptions.reduce((sum, option) => sum + option.points, 0)

  return {
    ...entry,
    selectedOptions,
    points: entry.profilePoints + optionPoints,
  }
}
