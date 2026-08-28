import { describe, expect, it } from '@jest/globals'
import { getLocalArmy } from '../../src/data/localArmyLists.js'
import type { SavedArmy } from '../../src/types.js'
import { importArmyFromCode } from '../../src/utils/armyImport.js'
import { generateArmyListMarkdown } from '../../src/utils/armyMarkdownExport.js'
import { buildRosterUnitsByEntryId } from '../../src/utils/rosterUnits.js'

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

const unitsByEntryId = buildRosterUnitsByEntryId(sampleArmy.roster, sampleArmy.factionId)

describe('generateArmyListMarkdown', () => {
  it('includes readable army and card sections plus notes', () => {
    const markdown = generateArmyListMarkdown(sampleArmy, unitsByEntryId, exportDate)
    expect(markdown).toContain('# Waaagh!')
    expect(markdown).toContain('## Army')
    expect(markdown).toContain('### Boyz')
    expect(markdown).toContain('## Command Cards')
    expect(markdown).toContain('### Waaagh!')
    expect(markdown).toContain('## Notes')
    expect(markdown).toContain('10/10, no notes.')
    expect(markdown).not.toContain('## Army Export Code')
    expect(markdown).not.toContain('```json')
  })

  it('includes unit numbers in roster metadata', () => {
    const markdown = generateArmyListMarkdown(sampleArmy, unitsByEntryId, exportDate)
    expect(markdown).toContain('#6')
    expect(getLocalArmy(sampleArmy.factionId)?.units?.some((unit) => unit.no === 6)).toBe(true)
  })
})

describe('importArmyFromCode markdown export', () => {
  it('imports a generated markdown army list', () => {
    const markdown = generateArmyListMarkdown(sampleArmy, unitsByEntryId, exportDate)
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
    expect(result.army.roster[0]?.selectedOptions[0]?.text).toBe(
      'Exchange Sluggas and Choppas for Shootas and Close Combat Weapons.',
    )
  })

  it('imports markdown without unit datasheets in the export', () => {
    const markdown = generateArmyListMarkdown(sampleArmy, new Map(), exportDate)
    expect(markdown).not.toContain('AV1.')
    const result = importArmyFromCode(markdown)
    expect(result.ok).toBe(true)
    if (!result.ok) {
      return
    }

    expect(result.army.name).toBe('Waaagh!')
    expect(result.army.roster).toHaveLength(1)
    expect(result.army.cards).toHaveLength(1)
    expect(result.army.roster[0]?.unitName).toBe('Boyz')
    expect(result.army.roster[0]?.unitNo).toBe(6)
    expect(result.army.roster[0]?.cardSlot).toBe(2)
    expect(result.army.roster[0]?.isCommander).toBe(true)
    expect(result.army.cards[0]?.cardId).toBe('Core-1-Orks')
  })
})
