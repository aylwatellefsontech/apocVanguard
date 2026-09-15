import { describe, expect, it } from '@jest/globals'
import { getLocalArmy } from '../data/localArmyLists.js'
import type { SavedArmy } from '../types.js'
import { importArmyFromMarkdownList } from './armyMarkdownImport.js'
import { generateArmyListMarkdown } from './armyMarkdownExport.js'
import { buildRosterUnitsByEntryId } from './rosterUnits.js'

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

describe('importArmyFromMarkdownList', () => {
  // US-011: import a readable markdown list
  it('imports units, cards, and organization from generated markdown', () => {
    const markdown = generateArmyListMarkdown(sampleArmy, unitsByEntryId, new Date('2026-08-27T12:00:00'))
    const result = importArmyFromMarkdownList(markdown)
    expect(result.ok).toBe(true)
    if (!result.ok) {
      return
    }

    expect(result.army.name).toBe('Waaagh!')
    expect(result.army.factionId).toBe('Apoc40k-Armies-1st - Orks')
    expect(result.army.roster).toHaveLength(1)
    expect(result.army.cards).toHaveLength(1)
    expect(result.army.roster[0]?.cardSlot).toBe(2)
    expect(result.army.roster[0]?.isCommander).toBe(true)
    expect(getLocalArmy(sampleArmy.factionId)?.units?.some((unit) => unit.no === 6)).toBe(true)
  })

  it('returns an error when army name or faction metadata is missing', () => {
    const result = importArmyFromMarkdownList('# Untitled\n\n## Army\n\n### Boyz\n')
    expect(result.ok).toBe(false)
    if (result.ok) {
      return
    }
    expect(result.error).toMatch(/missing army name or faction metadata/i)
  })

  it('returns an error when the markdown has no units or cards', () => {
    const result = importArmyFromMarkdownList(`---
format: apoc-vanguard-army
version: 1
name: "Empty"
factionId: Apoc40k-Armies-1st - Orks
factionName: Orks
---

# Empty

## Notes

None.
`)
    expect(result.ok).toBe(false)
    if (result.ok) {
      return
    }
    expect(result.error).toMatch(/does not contain any units or command cards/i)
  })
})
