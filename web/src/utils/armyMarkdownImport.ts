import { TYPE_ORDER } from '../constants'
import { getLocalArmy, getLocalFactions } from '../data/localArmyLists'
import { getLocalCards } from '../data/localCards'
import type { ArmyCardEntry, RosterEntry, SelectedOption, Unit, UnitProfile, UnitStats } from '../types'
import type { ImportArmyResult } from './armyExport'
import { normalizeSavedArmy, normalizeRosterEntry } from './armyStorage'
import {
  calculateOptionPoints,
  formatOptionBody,
  formatOptionLabel,
} from './formatOption'
import { getUnitProfiles } from './units'

const TYPE_SET = new Set<string>(TYPE_ORDER)
const FRONT_MATTER = /^---\s*\r?\n([\s\S]*?)\r?\n---\s*\r?\n/
const EXPORT_CODE_SECTION = /\n## Army Export Code[\s\S]*$/

interface ParsedFrontMatter {
  name?: string
  factionId?: string
  factionName?: string
  exportedAt?: string
}

interface ParsedEntryMeta {
  cardSlot?: number
  isCommander?: boolean
  factionName?: string
  profileLabel: string
  modelCount?: string | number | null
  points: number
  unitType: string
  unitNo?: number
}

function parseFrontMatter(text: string): ParsedFrontMatter {
  const meta: ParsedFrontMatter = {}
  const match = text.match(FRONT_MATTER)
  if (!match) {
    return meta
  }

  for (const line of match[1].split('\n')) {
    const colonIndex = line.indexOf(':')
    if (colonIndex <= 0) {
      continue
    }

    const key = line.slice(0, colonIndex).trim()
    const value = line.slice(colonIndex + 1).trim().replace(/^"|"$/g, '')
    if (key === 'name') meta.name = value
    if (key === 'factionId') meta.factionId = value
    if (key === 'factionName') meta.factionName = value
    if (key === 'exportedAt') meta.exportedAt = value
  }

  return meta
}

function parseDocumentTitle(text: string): string | null {
  const match = text.match(/^#\s+(.+)$/m)
  return match?.[1]?.trim() ?? null
}

function stripExportCodeSection(text: string): string {
  return text.replace(EXPORT_CODE_SECTION, '').trim()
}

function extractSection(text: string, heading: string): string {
  const pattern = new RegExp(`## ${heading}\\s*\\n([\\s\\S]*?)(?=\\n## |$)`)
  const match = text.match(pattern)
  return match?.[1]?.trim() ?? ''
}

function splitH3Blocks(section: string): string[] {
  if (!section.trim()) {
    return []
  }

  return section
    .split(/\n(?=### )/)
    .map((block) => block.trim())
    .filter(Boolean)
}

function parseEntryMeta(metaLine: string, knownFactionNames: Set<string>): ParsedEntryMeta {
  const parts = metaLine
    .replace(/^\*|\*$/g, '')
    .split(' · ')
    .map((part) => part.trim())
    .filter(Boolean)

  let cardSlot: number | undefined
  let isCommander = false
  let unitNo: number | undefined
  let unitType = ''
  let points = 0
  let modelCount: string | number | null = null
  let factionName: string | undefined

  if (parts[0]?.startsWith('Detachment ')) {
    const slot = Number.parseInt(parts.shift()!.slice('Detachment '.length), 10)
    if (Number.isFinite(slot)) {
      cardSlot = slot
    }
  }

  if (parts[0] === 'Commander') {
    isCommander = true
    parts.shift()
  }

  if (parts.length > 0 && TYPE_SET.has(parts[parts.length - 1]!)) {
    unitType = parts.pop()!
  }

  if (parts.length > 0 && /^#\d+$/.test(parts[parts.length - 1]!)) {
    const parsedNo = Number.parseInt(parts.pop()!.slice(1), 10)
    if (Number.isFinite(parsedNo)) {
      unitNo = parsedNo
    }
  }

  const pointsIndex = parts.findIndex((part) => /^\d+ Pt$/.test(part))
  if (pointsIndex >= 0) {
    points = Number.parseInt(parts[pointsIndex]!, 10)
    parts.splice(pointsIndex, 1)
  }

  const modelIndex = parts.findIndex((part) => /^N .+/.test(part))
  if (modelIndex >= 0) {
    modelCount = parts[modelIndex]!.slice(2).trim()
    parts.splice(modelIndex, 1)
  }

  if (parts.length > 1 && knownFactionNames.has(parts[0]!)) {
    factionName = parts.shift()
  }

  return {
    cardSlot,
    isCommander,
    factionName,
    profileLabel: parts.join(' · '),
    modelCount,
    points,
    unitType,
    unitNo,
  }
}

function findUnit(
  unitName: string,
  unitNo: number | undefined,
  defaultFactionId: string,
  defaultFactionName: string,
  factionNameHint?: string,
): { unit: Unit; factionId: string; factionName: string } | null {
  if (unitNo != null) {
    for (const faction of getLocalFactions()) {
      const army = getLocalArmy(faction.id)
      const unit = army?.units?.find((candidate) => candidate.no === unitNo && candidate.name === unitName)
      if (unit) {
        return { unit, factionId: faction.id, factionName: faction.faction }
      }
    }
  }

  const tryFaction = (factionId: string, factionName: string) => {
    const army = getLocalArmy(factionId)
    const unit = army?.units?.find((candidate) => candidate.name === unitName)
    return unit ? { unit, factionId, factionName } : null
  }

  const hintedFaction = factionNameHint
    ? getLocalFactions().find((faction) => faction.faction === factionNameHint)
    : null
  if (hintedFaction) {
    const match = tryFaction(hintedFaction.id, hintedFaction.faction)
    if (match) {
      return match
    }
  }

  const primaryMatch = tryFaction(defaultFactionId, defaultFactionName)
  if (primaryMatch) {
    return primaryMatch
  }

  for (const faction of getLocalFactions()) {
    const match = tryFaction(faction.id, faction.faction)
    if (match) {
      return match
    }
  }

  return null
}

function matchProfile(unit: Unit, profileLabel: string, pointsHint: number): UnitProfile | null {
  const profiles = getUnitProfiles(unit)
  if (profiles.length === 0) {
    return null
  }

  const exact = profiles.find((profile) => profile.label === profileLabel)
  if (exact) {
    return exact
  }

  const insensitive = profiles.find(
    (profile) => profile.label.toLowerCase() === profileLabel.toLowerCase(),
  )
  if (insensitive) {
    return insensitive
  }

  if (pointsHint > 0) {
    const byPoints = profiles.find((profile) => profile.points === pointsHint)
    if (byPoints) {
      return byPoints
    }
  }

  return profiles[0] ?? null
}

function extractProfileLabel(block: string, fallback: string): string {
  const match = block.match(/\*\*(.+?)\*\*\s*\n\s*\| M \|/)
  return match?.[1]?.trim() || fallback
}

function extractOptionsSection(block: string): string {
  const match = block.match(/#### Options\s*\n([\s\S]*?)(?=\n#### |\n### |$)/)
  return match?.[1]?.trim() ?? ''
}

function parseSelectedOptions(
  optionsText: string,
  unit: Unit,
  profileStats: UnitStats | null,
): SelectedOption[] {
  if (!optionsText || !unit.options?.length) {
    return []
  }

  const selected: SelectedOption[] = []

  for (const line of optionsText.split('\n')) {
    const match = line.match(/^- \*\*(.*?):\*\* (.+?)(?: \(\+(\d+) Pt\))?\s*$/)
    if (!match) {
      continue
    }

    const [, label, body, pointsText] = match
    const points = pointsText ? Number.parseInt(pointsText, 10) : 0
    const optionIndex = unit.options.findIndex((option) => {
      const optionLabel = formatOptionLabel(option) ?? 'Option'
      const optionBody = formatOptionBody(option)
      return (
        optionLabel === label &&
        (optionBody === body ||
          body.startsWith(optionBody) ||
          optionBody.startsWith(body))
      )
    })

    if (optionIndex < 0) {
      continue
    }

    const option = unit.options[optionIndex]!
    selected.push({
      index: optionIndex,
      points: Number.isFinite(points) ? points : calculateOptionPoints(option, profileStats),
      text: body,
      label: label === 'Option' ? null : label,
    })
  }

  return selected
}

function parseUnitBlock(
  block: string,
  defaults: { factionId: string; factionName: string },
  knownFactionNames: Set<string>,
): RosterEntry | null {
  const lines = block.split('\n')
  const titleMatch = lines[0]?.match(/^### (.+)$/)
  if (!titleMatch) {
    return null
  }

  const unitName = titleMatch[1]!.trim()
  const metaLine = lines.find((line) => line.startsWith('*') && line.endsWith('*'))
  if (!metaLine) {
    throw new Error(`Unit "${unitName}" is missing roster metadata.`)
  }

  const parsedMeta = parseEntryMeta(metaLine, knownFactionNames)
  const unitMatch = findUnit(
    unitName,
    parsedMeta.unitNo,
    defaults.factionId,
    defaults.factionName,
    parsedMeta.factionName,
  )

  if (!unitMatch) {
    throw new Error(`Could not find datasheet data for unit "${unitName}".`)
  }

  const profileLabel = extractProfileLabel(block, parsedMeta.profileLabel)
  const profile = matchProfile(unitMatch.unit, profileLabel, parsedMeta.points)
  if (!profile) {
    throw new Error(`Could not match a profile for unit "${unitName}".`)
  }

  const profileStats = profile.stats ?? null
  const selectedOptions = parseSelectedOptions(
    extractOptionsSection(block),
    unitMatch.unit,
    profileStats,
  )

  return normalizeRosterEntry({
    id: crypto.randomUUID(),
    factionId: unitMatch.factionId,
    factionName: unitMatch.factionName,
    unitNo: unitMatch.unit.no,
    unitName: unitMatch.unit.name,
    unitType: parsedMeta.unitType || unitMatch.unit.type,
    profileKind: profile.kind,
    profileIndex: profile.index,
    profileLabel: profile.label,
    profilePoints: profile.points,
    modelCount: parsedMeta.modelCount ?? profile.stats?.N ?? null,
    selectedOptions,
    points: parsedMeta.points > 0 ? parsedMeta.points : profile.points,
    cardSlot: parsedMeta.cardSlot,
    isCommander: parsedMeta.isCommander,
  })
}

function parseCardMeta(meta: string) {
  const parts = meta.split(' · ').map((part) => part.trim()).filter(Boolean)
  let facNm: number | null = null

  if (parts.length > 0 && /^#\d+$/.test(parts[parts.length - 1]!)) {
    facNm = Number.parseInt(parts.pop()!.slice(1), 10)
  }

  const setNm = parts.pop()
  if (!setNm) {
    throw new Error('Card metadata is missing set and number.')
  }

  const dashIndex = setNm.lastIndexOf('-')
  if (dashIndex <= 0) {
    throw new Error(`Card metadata has invalid set/number "${setNm}".`)
  }

  const set = setNm.slice(0, dashIndex)
  const nm = Number.parseInt(setNm.slice(dashIndex + 1), 10)
  const fac = parts.pop()
  if (!fac || !Number.isFinite(nm)) {
    throw new Error('Card metadata is missing faction or card number.')
  }

  let subType: string | null = null
  let type = parts[0] ?? ''
  if (parts.length === 2) {
    type = parts[0]!
    subType = parts[1]!
  }

  return { type, subType, fac, set, nm, facNm }
}

function extractCardAbility(block: string): string {
  const lines = block.split('\n')
  const metaIndex = lines.findIndex((line) => line.startsWith('*') && line.endsWith('*'))
  if (metaIndex < 0) {
    return ''
  }

  return lines
    .slice(metaIndex + 1)
    .join('\n')
    .trim()
}

function parseCardBlock(block: string): ArmyCardEntry | null {
  const lines = block.split('\n')
  const titleMatch = lines[0]?.match(/^### (.+)$/)
  if (!titleMatch) {
    return null
  }

  const name = titleMatch[1]!.trim()
  const metaLine = lines.find((line) => line.startsWith('*') && line.endsWith('*'))
  const cards = getLocalCards().cards

  if (!metaLine) {
    const fallback = cards.find((card) => card.name === name)
    if (!fallback) {
      throw new Error(`Could not find card data for "${name}".`)
    }

    return {
      id: crypto.randomUUID(),
      cardId: fallback.id,
      name: fallback.name,
      set: fallback.set,
      nm: fallback.nm,
      fac: fallback.fac,
      type: fallback.type,
      subType: fallback.subType ?? null,
      facNm: fallback.facNm ?? null,
      ability: fallback.ability ?? '',
    }
  }

  const parsedMeta = parseCardMeta(metaLine.slice(1, -1))
  const cardId = `${parsedMeta.set}-${parsedMeta.nm}-${parsedMeta.fac}`
  const card =
    cards.find((candidate) => candidate.id === cardId) ??
    cards.find((candidate) => candidate.name === name)

  if (!card) {
    return {
      id: crypto.randomUUID(),
      cardId,
      name,
      set: parsedMeta.set,
      nm: parsedMeta.nm,
      fac: parsedMeta.fac,
      type: parsedMeta.type,
      subType: parsedMeta.subType,
      facNm: parsedMeta.facNm,
      ability: extractCardAbility(block),
    }
  }

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

export function importArmyFromMarkdownList(text: string): ImportArmyResult {
  try {
    const stripped = stripExportCodeSection(text.trim())
    const frontMatter = parseFrontMatter(stripped)
    const name = frontMatter.name ?? parseDocumentTitle(stripped)
    const factionId = frontMatter.factionId
    const factionName = frontMatter.factionName

    if (!name || !factionId || !factionName) {
      return {
        ok: false,
        error: 'Markdown export is missing army name or faction metadata.',
      }
    }

    const armySection = extractSection(stripped, 'Army')
    const cardsSection = extractSection(stripped, 'Command Cards')
    const knownFactionNames = new Set(getLocalFactions().map((faction) => faction.faction))
    const defaults = { factionId, factionName }

    const roster = splitH3Blocks(armySection)
      .map((block) => parseUnitBlock(block, defaults, knownFactionNames))
      .filter((entry): entry is RosterEntry => entry != null)

    const cards = splitH3Blocks(cardsSection)
      .map((block) => parseCardBlock(block))
      .filter((entry): entry is ArmyCardEntry => entry != null)

    if (roster.length === 0 && cards.length === 0) {
      return {
        ok: false,
        error: 'Markdown export does not contain any units or command cards.',
      }
    }

    const army = normalizeSavedArmy({
      id: crypto.randomUUID(),
      name,
      factionId,
      factionName,
      totalPoints: roster.reduce((sum, entry) => sum + entry.points, 0),
      updatedAt: frontMatter.exportedAt ?? new Date().toISOString(),
      roster,
      cards,
    })

    return { ok: true, army }
  } catch (error) {
    const message = error instanceof Error ? error.message : 'Unknown import error.'
    return { ok: false, error: message }
  }
}
