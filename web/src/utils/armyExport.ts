import { MAX_SAVED_ARMIES } from '../constants'
import { normalizeRosterEntry, normalizeSavedArmy, saveArmy } from './armyStorage'
import { isValidCardSlot } from './rosterOrganize'
import type { ArmyCardEntry, RosterEntry, SavedArmy, SelectedOption } from '../types'

export const ARMY_EXPORT_FORMAT = 'apoc-vanguard-army'
export const ARMY_EXPORT_VERSION = 1
export const ARMY_CODE_PREFIX = 'AV1'

export interface ArmyExportSource {
  name: string
  factionId: string
  factionName: string
  totalPoints: number
  updatedAt?: string
  roster: RosterEntry[]
  cards: ArmyCardEntry[]
}

export type ImportArmyResult =
  | { ok: true; army: SavedArmy }
  | { ok: false; error: string }

type CompactExportPayload = [
  version: number,
  name: string,
  factionId: string,
  factionName: string,
  roster: unknown[],
  cards: unknown[],
]

function base64UrlEncode(bytes: Uint8Array): string {
  let binary = ''
  for (const byte of bytes) {
    binary += String.fromCharCode(byte)
  }
  return btoa(binary).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '')
}

function base64UrlDecode(value: string): Uint8Array {
  const normalized = value.replace(/-/g, '+').replace(/_/g, '/')
  const pad = normalized.length % 4
  const base64 = pad ? normalized + '='.repeat(4 - pad) : normalized
  const binary = atob(base64)
  const bytes = new Uint8Array(binary.length)
  for (let index = 0; index < binary.length; index += 1) {
    bytes[index] = binary.charCodeAt(index)
  }
  return bytes
}

function trimTrailingNullish(values: unknown[]): unknown[] {
  const next = [...values]
  while (next.length > 0) {
    const last = next[next.length - 1]
    if (last == null || last === '') {
      next.pop()
      continue
    }
    break
  }
  return next
}

function compactSelectedOption(option: SelectedOption): unknown[] {
  return trimTrailingNullish([
    option.index,
    option.points,
    option.modelIndex ?? null,
    option.slotIndex ?? null,
    option.choiceIndex ?? null,
    option.text ?? null,
    option.label ?? null,
  ])
}

function compactRosterEntry(entry: RosterEntry): unknown[] {
  const row: unknown[] = [
    entry.unitNo,
    entry.unitName,
    entry.unitType,
    entry.profileKind === 'alt' ? 1 : 0,
    entry.profileIndex,
    entry.profileLabel,
    entry.profilePoints,
    entry.modelCount ?? null,
    entry.factionId,
    entry.factionName,
  ]

  if (entry.selectedOptions.length > 0) {
    row.push(entry.selectedOptions.map(compactSelectedOption))
  }

  if (entry.cardSlot != null) {
    row.push(entry.cardSlot)
    if (entry.isCommander) {
      row.push(1)
    }
  }

  return row
}

function compactCardEntry(entry: ArmyCardEntry): unknown[] {
  return trimTrailingNullish([
    entry.cardId,
    entry.name,
    entry.set,
    entry.nm,
    entry.fac,
    entry.type,
    entry.subType ?? null,
    entry.facNm ?? null,
    entry.ability || null,
  ])
}

function formatExportDate(date: Date): string {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

export function formatExportLabel(name: string, exportedAt: Date = new Date()): string {
  const armyName = name.trim() || 'Untitled Army'
  return `[${armyName}.${formatExportDate(exportedAt)}]`
}

export function stripExportLabel(text: string): string {
  const match = text.match(/^\[(.*)\.(\d{4}-\d{2}-\d{2})\]/)
  if (!match) {
    return text
  }
  return text.slice(match[0].length)
}

function encodeCompactArmyPayload(army: ArmyExportSource): string {
  const payload: CompactExportPayload = [
    ARMY_EXPORT_VERSION,
    army.name,
    army.factionId,
    army.factionName,
    army.roster.map(compactRosterEntry),
    army.cards.map(compactCardEntry),
  ]

  const bytes = new TextEncoder().encode(JSON.stringify(payload))
  return `${ARMY_CODE_PREFIX}.${base64UrlEncode(bytes)}`
}

export function encodeArmyExport(army: ArmyExportSource, exportedAt: Date = new Date()): string {
  return `${formatExportLabel(army.name, exportedAt)}${encodeCompactArmyPayload(army)}`
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value != null && !Array.isArray(value)
}

function validateSelectedOption(option: unknown, path: string): SelectedOption {
  if (!Array.isArray(option)) {
    throw new Error(`${path} must be an array.`)
  }

  if (typeof option[0] !== 'number' || !Number.isInteger(option[0]) || option[0] < 0) {
    throw new Error(`${path} has an invalid option index.`)
  }

  if (typeof option[1] !== 'number' || !Number.isFinite(option[1])) {
    throw new Error(`${path} has invalid option points.`)
  }

  return {
    index: option[0],
    points: option[1],
    modelIndex: typeof option[2] === 'number' ? option[2] : undefined,
    slotIndex: typeof option[3] === 'number' ? option[3] : undefined,
    choiceIndex: typeof option[4] === 'number' ? option[4] : undefined,
    text: typeof option[5] === 'string' ? option[5] : undefined,
    label: typeof option[6] === 'string' ? option[6] : option[6] == null ? null : undefined,
  }
}

function getOrganizeTailIndex(entry: unknown[]): number {
  if (entry.length <= 8) {
    return entry.length
  }

  if (typeof entry[8] === 'string') {
    if (entry.length > 10 && Array.isArray(entry[10])) {
      return 11
    }
    if (entry.length > 9 && Array.isArray(entry[9])) {
      return 10
    }
    return 10
  }

  if (Array.isArray(entry[8])) {
    return 9
  }

  return entry.length
}

function parseOrganizeFields(entry: unknown[]): { cardSlot?: number; isCommander?: boolean } {
  const tailIndex = getOrganizeTailIndex(entry)
  const cardSlotValue = entry[tailIndex]
  if (!isValidCardSlot(cardSlotValue)) {
    return {}
  }

  return {
    cardSlot: cardSlotValue,
    isCommander: entry[tailIndex + 1] === 1,
  }
}

function validateRosterEntry(
  entry: unknown,
  index: number,
  fallbackFaction?: { factionId: string; factionName: string },
): RosterEntry {
  const path = `Roster entry ${index + 1}`
  if (!Array.isArray(entry) || entry.length < 7) {
    throw new Error(`${path} is malformed.`)
  }

  const unitNo = entry[0]
  const unitName = entry[1]
  const unitType = entry[2]
  const profileKindCode = entry[3]
  const profileIndex = entry[4]
  const profileLabel = entry[5]
  const profilePoints = entry[6]
  const modelCount = entry.length > 7 ? entry[7] : null
  let factionId = fallbackFaction?.factionId ?? ''
  let factionName = fallbackFaction?.factionName ?? ''
  let selectedOptionsRaw: unknown = []

  if (entry.length > 8) {
    if (typeof entry[8] === 'string') {
      factionId = entry[8]
      if (typeof entry[9] === 'string') {
        factionName = entry[9]
      }
      if (Array.isArray(entry[10])) {
        selectedOptionsRaw = entry[10]
      }
    } else if (Array.isArray(entry[8])) {
      selectedOptionsRaw = entry[8]
    }
  }

  if (typeof unitNo !== 'number' || !Number.isInteger(unitNo) || unitNo <= 0) {
    throw new Error(`${path} has an invalid unit number.`)
  }
  if (typeof unitName !== 'string' || !unitName.trim()) {
    throw new Error(`${path} is missing a unit name.`)
  }
  if (typeof unitType !== 'string' || !unitType.trim()) {
    throw new Error(`${path} is missing a unit type.`)
  }
  if (profileKindCode !== 0 && profileKindCode !== 1) {
    throw new Error(`${path} has an invalid profile kind.`)
  }
  if (typeof profileIndex !== 'number' || !Number.isInteger(profileIndex) || profileIndex < 0) {
    throw new Error(`${path} has an invalid profile index.`)
  }
  if (typeof profileLabel !== 'string' || !profileLabel.trim()) {
    throw new Error(`${path} is missing a profile label.`)
  }
  if (typeof profilePoints !== 'number' || !Number.isFinite(profilePoints) || profilePoints < 0) {
    throw new Error(`${path} has invalid profile points.`)
  }

  const selectedOptions = Array.isArray(selectedOptionsRaw)
    ? selectedOptionsRaw.map((option, optionIndex) =>
        validateSelectedOption(option, `${path} option ${optionIndex + 1}`),
      )
    : []
  const organizeFields = parseOrganizeFields(entry)

  return normalizeRosterEntry({
    id: crypto.randomUUID(),
    factionId,
    factionName,
    unitNo,
    unitName,
    unitType,
    profileKind: profileKindCode === 1 ? 'alt' : 'primary',
    profileIndex,
    profileLabel,
    profilePoints,
    modelCount:
      typeof modelCount === 'string' || typeof modelCount === 'number' || modelCount == null
        ? modelCount
        : null,
    selectedOptions,
    points: profilePoints,
    ...organizeFields,
  })
}

function validateCardEntry(entry: unknown, index: number): ArmyCardEntry {
  const path = `Card entry ${index + 1}`
  if (!Array.isArray(entry) || entry.length < 6) {
    throw new Error(`${path} is malformed.`)
  }

  const cardId = entry[0]
  const name = entry[1]
  const set = entry[2]
  const nm = entry[3]
  const fac = entry[4]
  const cardType = entry[5]
  const subType = entry[6]
  const facNm = entry[7]
  const ability = entry[8]

  if (typeof cardId !== 'string' || !cardId.trim()) {
    throw new Error(`${path} is missing a card id.`)
  }
  if (typeof name !== 'string' || !name.trim()) {
    throw new Error(`${path} is missing a card name.`)
  }
  if (typeof set !== 'string' || !set.trim()) {
    throw new Error(`${path} is missing a card set.`)
  }
  if (typeof nm !== 'number' || !Number.isInteger(nm)) {
    throw new Error(`${path} has an invalid card number.`)
  }
  if (typeof fac !== 'string' || !fac.trim()) {
    throw new Error(`${path} is missing a card faction.`)
  }
  if (typeof cardType !== 'string' || !cardType.trim()) {
    throw new Error(`${path} is missing a card type.`)
  }

  return {
    id: crypto.randomUUID(),
    cardId,
    name,
    set,
    nm,
    fac,
    type: cardType,
    subType: typeof subType === 'string' ? subType : null,
    facNm: typeof facNm === 'number' ? facNm : null,
    ability: typeof ability === 'string' ? ability : '',
  }
}

function decodeCompactPayload(payload: unknown): ImportArmyResult {
  if (!Array.isArray(payload) || payload.length < 6) {
    return { ok: false, error: 'Export payload is malformed.' }
  }

  const version = payload[0]
  const name = payload[1]
  const factionId = payload[2]
  const factionName = payload[3]
  const rosterRaw = payload[4]
  const cardsRaw = payload[5]

  if (version !== ARMY_EXPORT_VERSION) {
    return {
      ok: false,
      error: `Unsupported export version "${String(version)}". Expected version ${ARMY_EXPORT_VERSION}.`,
    }
  }
  if (typeof name !== 'string' || !name.trim()) {
    return { ok: false, error: 'Export payload is missing an army name.' }
  }
  if (typeof factionId !== 'string' || !factionId.trim()) {
    return { ok: false, error: 'Export payload is missing a faction id.' }
  }
  if (typeof factionName !== 'string' || !factionName.trim()) {
    return { ok: false, error: 'Export payload is missing a faction name.' }
  }
  if (!Array.isArray(rosterRaw)) {
    return { ok: false, error: 'Export payload is missing roster data.' }
  }
  if (!Array.isArray(cardsRaw)) {
    return { ok: false, error: 'Export payload is missing card data.' }
  }

  const roster = rosterRaw.map((entry, index) =>
    validateRosterEntry(entry, index, {
      factionId: factionId.trim(),
      factionName: factionName.trim(),
    }),
  )
  const cards = cardsRaw.map(validateCardEntry)

  if (roster.length === 0 && cards.length === 0) {
    return { ok: false, error: 'Army export must include at least one unit or card.' }
  }

  const army = normalizeSavedArmy({
    id: crypto.randomUUID(),
    name: name.trim(),
    factionId: factionId.trim(),
    factionName: factionName.trim(),
    totalPoints: roster.reduce((sum, entry) => sum + entry.points, 0),
    updatedAt: new Date().toISOString(),
    roster,
    cards,
  })

  return { ok: true, army }
}

function decodeArmyCode(text: string): ImportArmyResult {
  const match = text.trim().match(/^AV1\.([A-Za-z0-9_-]+)$/)
  if (!match) {
    return {
      ok: false,
      error: 'Invalid export code. Expected a string starting with "AV1.".',
    }
  }

  try {
    const json = new TextDecoder().decode(base64UrlDecode(match[1]))
    const payload = JSON.parse(json) as unknown
    return decodeCompactPayload(payload)
  } catch {
    return { ok: false, error: 'Export code could not be decoded.' }
  }
}

export function extractArmyCodeFromText(text: string): string | null {
  const labeledMatch = text.match(/\[[^\]\n]+\.\d{4}-\d{2}-\d{2}\]AV1\.[A-Za-z0-9_-]+/)
  if (labeledMatch) {
    return labeledMatch[0]
  }

  const bareMatch = text.match(/AV1\.[A-Za-z0-9_-]+/)
  return bareMatch?.[0] ?? null
}

/** @deprecated Legacy markdown exports from earlier builds. */
function decodeLegacyMarkdown(text: string): ImportArmyResult {
  const frontMatter = /^---\s*\r?\n([\s\S]*?)\r?\n---\s*\r?\n/
  const jsonBlock = /```(?:json|army-json)?\s*\r?\n([\s\S]*?)```/
  const meta: Record<string, string> = {}
  const headerMatch = text.match(frontMatter)
  if (headerMatch) {
    for (const line of headerMatch[1].split('\n')) {
      const colonIndex = line.indexOf(':')
      if (colonIndex > 0) {
        meta[line.slice(0, colonIndex).trim()] = line.slice(colonIndex + 1).trim().replace(/^"|"$/g, '')
      }
    }
  }

  const blockMatch = text.match(jsonBlock)
  if (!blockMatch) {
    return { ok: false, error: 'Legacy export is missing JSON data.' }
  }

  let payload: unknown
  try {
    payload = JSON.parse(blockMatch[1])
  } catch {
    return { ok: false, error: 'Legacy export JSON is invalid.' }
  }

  if (!isRecord(payload) || !Array.isArray(payload.roster) || !Array.isArray(payload.cards)) {
    return { ok: false, error: 'Legacy export JSON is malformed.' }
  }

  const name = meta.name?.trim()
  const factionId = meta.factionId?.trim()
  const factionName = meta.factionName?.trim()
  if (!name || !factionId || !factionName) {
    return { ok: false, error: 'Legacy export is missing army metadata.' }
  }

  const roster = payload.roster.map((entry, index) => {
    if (!isRecord(entry)) {
      throw new Error(`Roster entry ${index + 1} must be an object.`)
    }

    const selectedOptions = Array.isArray(entry.selectedOptions)
      ? entry.selectedOptions.map((option, optionIndex) => {
          if (!isRecord(option)) {
            throw new Error(`Roster entry ${index + 1} option ${optionIndex + 1} must be an object.`)
          }
          if (typeof option.index !== 'number' || typeof option.points !== 'number') {
            throw new Error(`Roster entry ${index + 1} option ${optionIndex + 1} is malformed.`)
          }
          return compactSelectedOption({
            index: option.index,
            points: option.points,
            modelIndex: typeof option.modelIndex === 'number' ? option.modelIndex : undefined,
            slotIndex: typeof option.slotIndex === 'number' ? option.slotIndex : undefined,
            choiceIndex: typeof option.choiceIndex === 'number' ? option.choiceIndex : undefined,
            text: typeof option.text === 'string' ? option.text : undefined,
            label: typeof option.label === 'string' ? option.label : option.label == null ? null : undefined,
          })
        })
      : []

    return validateRosterEntry(
      [
        entry.unitNo,
        entry.unitName,
        entry.unitType,
        entry.profileKind === 'alt' ? 1 : 0,
        entry.profileIndex,
        entry.profileLabel,
        entry.profilePoints,
        entry.modelCount ?? null,
        typeof entry.factionId === 'string' ? entry.factionId : factionId,
        typeof entry.factionName === 'string' ? entry.factionName : factionName,
        selectedOptions,
        ...(typeof entry.cardSlot === 'number' ? [entry.cardSlot, entry.isCommander ? 1 : 0] : []),
      ],
      index,
      { factionId, factionName },
    )
  })

  const cards = payload.cards.map((entry, index) => {
    if (!isRecord(entry)) {
      throw new Error(`Card entry ${index + 1} must be an object.`)
    }
    return validateCardEntry(
      [
        entry.cardId,
        entry.name,
        entry.set,
        entry.nm,
        entry.fac,
        entry.type,
        entry.subType ?? null,
        entry.facNm ?? null,
        entry.ability ?? null,
      ],
      index,
    )
  })

  const army = normalizeSavedArmy({
    id: crypto.randomUUID(),
    name,
    factionId,
    factionName,
    totalPoints: roster.reduce((sum, entry) => sum + entry.points, 0),
    updatedAt: meta.updatedAt ?? new Date().toISOString(),
    roster,
    cards,
  })

  return { ok: true, army }
}

export function importArmyFromCode(text: string): ImportArmyResult {
  const trimmed = text.trim()
  if (!trimmed) {
    return { ok: false, error: 'Paste an army export code before importing.' }
  }

  if (
    trimmed.startsWith('---') ||
    trimmed.startsWith('#') ||
    trimmed.includes('```json') ||
    trimmed.includes('```army-json')
  ) {
    const embeddedCode = extractArmyCodeFromText(trimmed)
    if (embeddedCode) {
      return decodeArmyCode(stripExportLabel(embeddedCode))
    }

    if (trimmed.includes('```json') || trimmed.includes('```army-json')) {
      try {
        return decodeLegacyMarkdown(trimmed)
      } catch (error) {
        const message = error instanceof Error ? error.message : 'Unknown import error.'
        return { ok: false, error: message }
      }
    }

    return {
      ok: false,
      error: 'Markdown export is missing an army export code.',
    }
  }

  const code = stripExportLabel(trimmed)
  return decodeArmyCode(code)
}

export function importAndSaveArmyFromCode(text: string, existingCount?: number): ImportArmyResult {
  const result = importArmyFromCode(text)
  if (!result.ok) {
    return result
  }

  const count = existingCount ?? 0
  if (count >= MAX_SAVED_ARMIES) {
    return {
      ok: false,
      error: `You can only save up to ${MAX_SAVED_ARMIES} armies. Delete one before importing.`,
    }
  }

  const saveResult = saveArmy(result.army)
  if (!saveResult.ok) {
    return { ok: false, error: saveResult.error ?? 'Failed to save imported army.' }
  }

  return { ok: true, army: result.army }
}

/** @deprecated Use generateArmyListMarkdown instead. */
export const exportArmyToMarkdown = encodeArmyExport
/** @deprecated Use importArmyFromCode instead. */
export const importArmyFromMarkdown = importArmyFromCode
/** @deprecated Use importAndSaveArmyFromCode instead. */
export const importAndSaveArmyFromMarkdown = importAndSaveArmyFromCode
