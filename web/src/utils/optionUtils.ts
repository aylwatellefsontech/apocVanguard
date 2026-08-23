import type { SelectedOption, UnitOption, UnitOptionObject, UnitStats } from '../types'

const PER_UNIT = /^per\s+unit$/i
const PER_MODEL = /^per\s+model$/i
const PER_MODELS = /^per\s+(\d+)\s+models?$/i
const UP_TO = /^up\s+to\s+(\d+)$/i
const EXCLUSIVE = /exclusive/i

export function isOptionObject(option: UnitOption): option is UnitOptionObject {
  return typeof option !== 'string'
}

export function normalizePerLabel(per: string | undefined): string {
  const raw = per?.trim() ?? ''
  if (!raw) return 'Per Unit'
  if (PER_UNIT.test(raw)) return 'Per Unit'
  if (PER_MODEL.test(raw)) return 'Per Model'
  const upToMatch = raw.match(UP_TO)
  if (upToMatch) return `Up to ${upToMatch[1]}`
  const modelsMatch = raw.match(PER_MODELS)
  if (modelsMatch) return `Per ${modelsMatch[1]} models`
  if (raw.toLowerCase().startsWith('per ')) {
    return raw.replace(/^per\s+/i, 'Per ')
  }
  return raw
}

export function isPerModelOption(option: UnitOption): boolean {
  if (!isOptionObject(option)) return false
  return PER_MODEL.test(option.per?.trim() ?? '')
}

export function isPerModelsOption(option: UnitOption): boolean {
  if (!isOptionObject(option)) return false
  return PER_MODELS.test(option.per?.trim() ?? '')
}

export function getPerModelsInterval(option: UnitOption): number | null {
  if (!isOptionObject(option)) return null
  const match = option.per?.trim().match(PER_MODELS)
  if (!match) return null
  const interval = Number.parseInt(match[1], 10)
  return Number.isFinite(interval) && interval > 0 ? interval : null
}

export function getPerModelsSlotCount(
  option: UnitOption,
  profileStats: UnitStats | null | undefined,
): number {
  const interval = getPerModelsInterval(option)
  if (interval == null) return 0
  const modelCount = getModelCount(profileStats)
  return Math.floor(modelCount / interval)
}

export function formatPerModelsSlotLegend(
  slotIndex: number,
  interval: number,
  groupName?: string,
): string {
  const start = slotIndex * interval + 1
  const end = (slotIndex + 1) * interval
  const range = `Models ${start}–${end}`
  return groupName ? `${groupName} (${range})` : range
}

export function parseChooseOneChoices(raw: string): string[] {
  return raw
    .split(';')
    .map((part) => part.trim().replace(/[.,]+$/u, '').trim())
    .filter(Boolean)
}

export function getChooseOneChoices(option: UnitOption): string[] {
  if (!isOptionObject(option)) return []
  if (Array.isArray(option.chooseOne)) {
    return option.chooseOne.map((choice) => choice.trim()).filter(Boolean)
  }
  return []
}

export function getChooseLimit(option: UnitOption): number | null {
  const choices = getChooseOneChoices(option)
  if (choices.length === 0 || !isOptionObject(option)) return null
  const limit = option.chooseLimit ?? 1
  if (!Number.isInteger(limit) || limit < 1) return null
  return Math.min(limit, choices.length)
}

export function isChooseOneOption(option: UnitOption): boolean {
  return getChooseLimit(option) != null
}

export function getChooseInstanceCount(
  option: UnitOption,
  profileStats?: UnitStats | null,
): number {
  if (!isChooseOneOption(option)) return 0
  const upToLimit = getUpToLimit(option)
  if (upToLimit != null) return upToLimit
  if (isPerModelsOption(option)) return getPerModelsSlotCount(option, profileStats)
  return 1
}

export function optionUsesSlotIndex(option: UnitOption): boolean {
  return isUpToOption(option) || isPerModelsOption(option) || isChooseOneOption(option)
}

export function isUpToOption(option: UnitOption): boolean {
  if (!isOptionObject(option)) return false
  return UP_TO.test(option.per?.trim() ?? '')
}

export function getUpToLimit(option: UnitOption): number | null {
  if (!isOptionObject(option)) return null
  const match = option.per?.trim().match(UP_TO)
  if (!match) return null
  const limit = Number.parseInt(match[1], 10)
  return Number.isFinite(limit) && limit > 0 ? limit : null
}

export function getOptionGroup(option: UnitOption): string | null {
  if (!isOptionObject(option) || !option.group?.trim()) return null
  return option.group.trim()
}

export function isExclusiveGroupOption(option: UnitOption): boolean {
  if (!isOptionObject(option)) return false
  const limit = option.limit?.trim() ?? ''
  return EXCLUSIVE.test(limit)
}

export function getModelCount(profileStats: UnitStats | null | undefined): number {
  const count = Number.parseInt(profileStats?.N ?? '', 10)
  return Number.isFinite(count) && count > 0 ? count : 1
}

export function optionSelectionKey(
  index: number,
  modelIndex?: number,
  slotIndex?: number,
  choiceIndex?: number,
): string {
  const parts = [`${index}`]
  if (modelIndex != null) parts.push(`m${modelIndex}`)
  if (slotIndex != null) parts.push(`s${slotIndex}`)
  if (choiceIndex != null) parts.push(`c${choiceIndex}`)
  return parts.join(':')
}

export function isOptionSelected(
  optionIndex: number,
  selectedIndexes: number[],
  selectedOptions?: SelectedOption[],
  modelIndex?: number,
  slotIndex?: number,
  choiceIndex?: number,
): boolean {
  if (selectedOptions) {
    return selectedOptions.some((opt) => {
      if (opt.index !== optionIndex) return false
      if (modelIndex == null ? opt.modelIndex != null : opt.modelIndex !== modelIndex) {
        return false
      }
      if (choiceIndex != null) {
        if (slotIndex != null) {
          return opt.slotIndex === slotIndex && opt.choiceIndex === choiceIndex
        }
        if (opt.choiceIndex != null) {
          return opt.choiceIndex === choiceIndex && opt.slotIndex == null
        }
        return opt.slotIndex === choiceIndex
      }
      if (slotIndex == null) return opt.slotIndex == null
      return opt.slotIndex === slotIndex
    })
  }
  return selectedIndexes.includes(optionIndex)
}

export function countOptionSelections(
  selectedOptions: SelectedOption[] | undefined,
  optionIndex: number,
  modelIndex?: number,
  slotIndex?: number,
): number {
  if (!selectedOptions) return 0
  return selectedOptions.filter(
    (opt) =>
      opt.index === optionIndex &&
      (modelIndex == null ? opt.modelIndex == null : opt.modelIndex === modelIndex) &&
      (slotIndex == null ? opt.slotIndex == null : opt.slotIndex === slotIndex),
  ).length
}
