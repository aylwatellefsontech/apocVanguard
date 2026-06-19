import { MAX_SAVED_ARMIES, SAVED_ARMIES_KEY } from '../constants.js'

export function loadSavedArmies() {
  try {
    const raw = localStorage.getItem(SAVED_ARMIES_KEY)
    if (!raw) return []
    const parsed = JSON.parse(raw)
    return Array.isArray(parsed) ? parsed : []
  } catch {
    return []
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

  const next = armies.some((entry) => entry.id === army.id)
    ? armies.map((entry) => (entry.id === army.id ? army : entry))
    : [...armies, army]

  persistSavedArmies(next)
  return { ok: true, armies: next }
}

export function deleteSavedArmy(id) {
  const next = loadSavedArmies().filter((army) => army.id !== id)
  persistSavedArmies(next)
  return next
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
    points: profile.points,
  }
}
