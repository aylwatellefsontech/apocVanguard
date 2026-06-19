const PER_UNIT = /^per unit$/i
const POWER_RATING_IN_TEXT = /\s*\(Power Rating[^)]*\)/gi
const PER_MODELS = /^per\s+(\d+)\s+models?$/i

function formatPerLabel(per) {
  if (!per || PER_UNIT.test(per.trim())) {
    return null
  }

  const match = per.trim().match(/^Per\s+(.+)$/i)
  if (!match) {
    return per.trim()
  }

  const rest = match[1].replace(/\b\w/g, (char) => char.toUpperCase())
  return `Per ${rest}`
}

export function getOptionBasePoints(option) {
  if (typeof option === 'string') {
    return 0
  }

  const raw = option.Pt ?? option.pt
  if (raw == null || raw === '') {
    return 0
  }

  const match = String(raw).match(/\+?(\d+)/)
  return match ? Number.parseInt(match[1], 10) : 0
}

export function getOptionScope(option) {
  if (typeof option === 'string' || !option.per || PER_UNIT.test(option.per.trim())) {
    return { type: 'unit' }
  }

  const modelsMatch = option.per.trim().match(PER_MODELS)
  if (modelsMatch) {
    return {
      type: 'models',
      count: Number.parseInt(modelsMatch[1], 10),
    }
  }

  return { type: 'unit' }
}

export function calculateOptionPoints(option, profileStats) {
  const basePt = getOptionBasePoints(option)
  if (basePt === 0) {
    return 0
  }

  const scope = getOptionScope(option)
  if (scope.type !== 'models') {
    return basePt
  }

  const modelCount = Number.parseInt(profileStats?.N ?? '', 10)
  if (!Number.isFinite(modelCount) || modelCount <= 0) {
    return basePt
  }

  return Math.floor(modelCount / scope.count) * basePt
}

function stripEmbeddedPowerRating(text) {
  return text.replace(POWER_RATING_IN_TEXT, '').trim()
}

export function formatOptionLabel(option) {
  if (typeof option === 'string') {
    return null
  }

  const perLabel = formatPerLabel(option.per)
  const points = getOptionBasePoints(option)

  if (points) {
    const rating = `+${points} Power Rating`
    return perLabel ? `${rating} / ${perLabel}` : rating
  }

  if (perLabel) {
    return perLabel
  }

  return 'Option'
}

export function formatOptionBody(option) {
  if (typeof option === 'string') {
    return option
  }

  return stripEmbeddedPowerRating(option.text || option.name || '')
}

export function formatOptionText(option) {
  if (typeof option === 'string') {
    return option
  }

  const label = formatOptionLabel(option)
  const body = formatOptionBody(option)

  if (label) {
    return `${label}: ${body}`
  }

  return body
}

export function summarizeOption(option, profileStats) {
  const points = calculateOptionPoints(option, profileStats)

  return {
    label: formatOptionLabel(option),
    text: formatOptionBody(option),
    points,
  }
}
