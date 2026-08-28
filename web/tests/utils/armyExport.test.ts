import { describe, expect, it } from '@jest/globals'
import type { SavedArmy } from '../../src/types.js'
import {
  ARMY_CODE_PREFIX,
  encodeArmyExport,
  formatExportLabel,
  importArmyFromCode,
  stripExportLabel,
} from '../../src/utils/armyExport.js'

const sampleArmy: SavedArmy = {
  id: 'army-1',
  name: 'Waaagh!',
  factionId: 'Apoc40k-Armies-1st - Orks',
  factionName: 'Orks',
  totalPoints: 12,
  roster: [
    {
      id: 'entry-1',
      factionId: 'Apoc40k-Armies-1st - Orks',
      factionName: 'Orks',
      unitNo: 6,
      unitName: 'Boyz',
      unitType: 'Troops',
      profileKind: 'primary',
      profileIndex: 0,
      profileLabel: '10 Boys',
      profilePoints: 5,
      modelCount: '10',
      selectedOptions: [{ index: 0, points: 0, text: 'Shootas' }],
      points: 5,
    },
  ],
  cards: [
    {
      id: 'card-1',
      cardId: 'Core-1-Orks',
      name: 'Waaagh!',
      set: 'Core',
      nm: 1,
      fac: 'Orks',
      type: 'Order',
      ability: 'Fight.',
    },
  ],
}

const exportDate = new Date('2026-08-27T12:00:00')

describe('formatExportLabel', () => {
  it('formats army name and export date', () => {
    expect(formatExportLabel('Waaagh!', exportDate)).toBe('[Waaagh!.2026-08-27]')
  })
})

describe('encodeArmyExport', () => {
  it('produces a compact AV1 code with a readable label prefix', () => {
    const code = encodeArmyExport(sampleArmy, exportDate)
    expect(code.startsWith('[Waaagh!.2026-08-27]')).toBe(true)
    expect(code).toContain(`${ARMY_CODE_PREFIX}.`)
    expect(code).not.toContain('\n')
    expect(code.length).toBeLessThan(550)
  })
})

describe('importArmyFromCode', () => {
  it('rehydrates a valid export with label prefix', () => {
    const code = encodeArmyExport(sampleArmy, exportDate)
    const result = importArmyFromCode(code)
    expect(result.ok).toBe(true)
    if (!result.ok) {
      return
    }

    expect(result.army.name).toBe('Waaagh!')
    expect(result.army.factionId).toBe('Apoc40k-Armies-1st - Orks')
    expect(result.army.roster).toHaveLength(1)
    expect(result.army.cards).toHaveLength(1)
    expect(result.army.roster[0]?.unitName).toBe('Boyz')
    expect(result.army.roster[0]?.selectedOptions[0]?.text).toBe('Shootas')
  })

  it('ignores a mismatched label prefix and uses encoded army data', () => {
    const code = encodeArmyExport(sampleArmy, exportDate)
    const relabeled = code.replace('[Waaagh!.2026-08-27]', '[Different Name.1999-01-01]')
    const result = importArmyFromCode(relabeled)
    expect(result.ok).toBe(true)
    if (!result.ok) {
      return
    }
    expect(result.army.name).toBe('Waaagh!')
  })

  it('still imports bare AV1 codes without a label prefix', () => {
    const code = stripExportLabel(encodeArmyExport(sampleArmy, exportDate))
    const result = importArmyFromCode(code)
    expect(result.ok).toBe(true)
  })

  it('returns a helpful error for invalid codes', () => {
    const result = importArmyFromCode('not-a-valid-code')
    expect(result).toEqual({
      ok: false,
      error: 'Invalid export code. Expected a string starting with "AV1.".',
    })
  })

  it('returns a helpful error for corrupted payloads', () => {
    const result = importArmyFromCode(`${ARMY_CODE_PREFIX}.AAAA`)
    expect(result).toEqual({
      ok: false,
      error: 'Export code could not be decoded.',
    })
  })

  it('returns a helpful error when roster is missing', () => {
    const brokenPayload = btoa(JSON.stringify([1, 'Broken', 'test', 'Test', 'not-an-array', []]))
      .replace(/\+/g, '-')
      .replace(/\//g, '_')
      .replace(/=+$/, '')
    const result = importArmyFromCode(
      `[Broken.2026-08-27]${ARMY_CODE_PREFIX}.${brokenPayload}`,
    )
    expect(result).toEqual({
      ok: false,
      error: 'Export payload is missing roster data.',
    })
  })

  it('round-trips card slot and commander metadata', () => {
    const organizedArmy: SavedArmy = {
      ...sampleArmy,
      roster: [
        {
          ...sampleArmy.roster[0]!,
          cardSlot: 3,
          isCommander: true,
        },
      ],
    }

    const code = encodeArmyExport(organizedArmy, exportDate)
    const result = importArmyFromCode(code)
    expect(result.ok).toBe(true)
    if (!result.ok) {
      return
    }

    expect(result.army.roster[0]?.cardSlot).toBe(3)
    expect(result.army.roster[0]?.isCommander).toBe(true)
  })

  it('still imports legacy markdown exports', () => {
    const legacy = `---
format: apoc-vanguard-army
version: 1
name: "Waaagh!"
factionId: Apoc40k-Armies-1st - Orks
factionName: Orks
---

\`\`\`json
${JSON.stringify({ roster: sampleArmy.roster, cards: sampleArmy.cards }, null, 2)}
\`\`\``
    const result = importArmyFromCode(legacy)
    expect(result.ok).toBe(true)
    if (!result.ok) {
      return
    }
    expect(result.army.name).toBe('Waaagh!')
    expect(result.army.roster).toHaveLength(1)
  })
})
