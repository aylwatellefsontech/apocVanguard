import type { OptionScope, OptionSummary, UnitOption, UnitStats } from '../types'
import { getChooseOneChoices, isPerModelOption, normalizePerLabel } from './optionUtils'

const PER_UNIT = /^per unit$/i
const POWER_RATING_IN_TEXT = /\s*\(Power Rating[^)]*\)/gi
const PER_MODELS = /^per\s+(\d+)\s+models?$/i

function formatPerLabel(per: string | undefined): string | null {
  const normalized = normalizePerLabel(per)
  if (PER_UNIT.test(normalized)) {
    return null
  }
  if (isPerModelOption({ per: normalized, text: '' })) {
    return 'Per Model'
  }

  const match = normalized.match(/^Per\s+(.+)$/i)
  if (!match) {
    return normalized
  }

  const rest = match[1].replace(/\b\w/g, (char) => char.toUpperCase())
  return `Per ${rest}`
}

export function getOptionBasePoints(option: UnitOption): number {
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

export function getOptionScope(option: UnitOption): OptionScope {
  if (typeof option === 'string' || !option.per || PER_UNIT.test(option.per.trim())) {
    return { type: 'unit' }
  }

  if (isPerModelOption(option)) {
    return { type: 'model' }
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

export function calculateOptionPoints(
  option: UnitOption,
  profileStats: UnitStats | null,
  mode: 'total' | 'perSelection' = 'total',
): number {
  const basePt = getOptionBasePoints(option)
  if (basePt === 0) {
    return 0
  }

  if (mode === 'perSelection') {
    return basePt
  }

  const scope = getOptionScope(option)
  if (scope.type === 'model') {
    return basePt
  }

  if (scope.type !== 'models') {
    return basePt
  }

  const modelCount = Number.parseInt(profileStats?.N ?? '', 10)
  if (!Number.isFinite(modelCount) || modelCount <= 0) {
    return basePt
  }

  return Math.floor(modelCount / scope.count) * basePt
}

function stripEmbeddedPowerRating(text: string): string {
  return text.replace(POWER_RATING_IN_TEXT, '').trim()
}

export function formatOptionLabel(option: UnitOption): string | null {
  if (typeof option === 'string') {
    return null
  }

  const title = option.title?.trim()
  if (title) {
    return title
  }

  const perLabel = formatPerLabel(option.per)
  if (perLabel) {
    return perLabel
  }

  return 'Option'
}

export function formatOptionBody(option: UnitOption): string {
  if (typeof option === 'string') {
    return option
  }

  const body = stripEmbeddedPowerRating(option.text || option.name || '')
  const choices = getChooseOneChoices(option)
  if (choices.length === 0) {
    return body
  }

  const choiceList = choices.join('; ')
  return body ? `${body} ${choiceList}` : `Choose one: ${choiceList}`
}

export function formatOptionText(option: UnitOption): string {
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

export function summarizeOption(
  option: UnitOption,
  profileStats: UnitStats | null,
  perSelection = false,
): OptionSummary {
  const points = calculateOptionPoints(
    option,
    profileStats,
    perSelection ? 'perSelection' : 'total',
  )

  return {
    label: formatOptionLabel(option),
    text: formatOptionBody(option),
    points,
  }
}
