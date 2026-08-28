import { MAX_SAVED_ARMIES } from '../constants'
import type { ImportArmyResult } from './armyExport'
import {
  decodeArmyCode,
  decodeLegacyMarkdown,
  extractArmyCodeFromText,
  stripExportLabel,
} from './armyExport'
import { importArmyFromMarkdownList } from './armyMarkdownImport'
import { saveArmy } from './armyStorage'

export type { ImportArmyResult } from './armyExport'

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

    return importArmyFromMarkdownList(trimmed)
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

export const importArmyFromMarkdown = importArmyFromCode
export const importAndSaveArmyFromMarkdown = importAndSaveArmyFromCode
