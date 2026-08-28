import { describe, expect, it } from '@jest/globals'
import { encodeArmyExport } from '../../src/utils/armyExport.js'
import type { SavedArmy } from '../../src/types.js'
import { importArmyFromCode } from '../../src/utils/armyExport.js'
import { generateArmyListMarkdown } from '../../src/utils/armyMarkdownExport.js'

const exportDate = new Date('2026-08-27T12:00:00')

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
      cardSlot: 2,
      isCommander: true,
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

describe('generateArmyListMarkdown', () => {
  it('includes readable army and card sections plus embedded army code', () => {
    const exportCode = encodeArmyExport(sampleArmy, exportDate)
    const markdown = generateArmyListMarkdown(sampleArmy, new Map(), exportCode, exportDate)
    expect(markdown).toContain('# Waaagh!')
    expect(markdown).toContain('## Army')
    expect(markdown).toContain('### Boyz')
    expect(markdown).toContain('## Command Cards')
    expect(markdown).toContain('### Waaagh!')
    expect(markdown).toContain('## Army Export Code')
    expect(markdown).toContain(exportCode)
    expect(markdown).not.toContain('```json')
  })
})

describe('importArmyFromCode markdown export', () => {
  it('imports a generated markdown army list from the embedded army code', () => {
    const exportCode = encodeArmyExport(sampleArmy, exportDate)
    const markdown = generateArmyListMarkdown(sampleArmy, new Map(), exportCode, exportDate)
    const result = importArmyFromCode(markdown)
    expect(result.ok).toBe(true)
    if (!result.ok) {
      return
    }

    expect(result.army.name).toBe('Waaagh!')
    expect(result.army.roster).toHaveLength(1)
    expect(result.army.cards).toHaveLength(1)
    expect(result.army.roster[0]?.unitName).toBe('Boyz')
    expect(result.army.roster[0]?.cardSlot).toBe(2)
    expect(result.army.roster[0]?.isCommander).toBe(true)
    expect(result.army.roster[0]?.selectedOptions[0]?.text).toBe('Shootas')
  })
})
