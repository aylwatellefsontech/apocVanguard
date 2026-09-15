import { describe, expect, it } from '@jest/globals'
import type { ArmyList, SavedArmy, Unit } from '../types.js'
import { generateArmyPrintHtml, generateFactionPrintHtml } from './printExport.js'

const boyz: Unit = {
  no: 6,
  name: 'Boyz',
  type: 'Troops',
  stats: { Pt: '5' },
}

const factionList: ArmyList = {
  faction: 'Orks',
  source: 'Apoc40k-Armies-1st',
  units: [boyz],
}

const savedArmy: SavedArmy = {
  id: 'army-1',
  name: 'Waaagh!',
  factionId: 'Apoc40k-Armies-1st - Orks',
  factionName: 'Orks',
  totalPoints: 7,
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
      selectedOptions: [{ index: 0, points: 2, text: 'Big Shoota' }],
      points: 7,
    },
  ],
  cards: [],
}

describe('generateFactionPrintHtml', () => {
  // US-004: printable faction army list
  it('includes the faction name and unit datasheets', () => {
    const html = generateFactionPrintHtml(factionList)
    expect(html).toContain('Orks — Army List')
    expect(html).toContain('Boyz')
    expect(html).toContain('Troops')
  })

  it('still wraps an empty faction list without throwing', () => {
    const html = generateFactionPrintHtml({ faction: 'Orks', source: 'test', units: [] })
    expect(html).toContain('Orks — Army List')
    expect(html).toContain('0 units')
  })
})

describe('generateArmyPrintHtml', () => {
  // US-013: printable saved roster with options and points
  it('includes the saved army name, points, and selected options', () => {
    const html = generateArmyPrintHtml(savedArmy, new Map([['entry-1', boyz]]))
    expect(html).toContain('Waaagh!')
    expect(html).toContain('7 Pt total')
    expect(html).toContain('Boyz')
    expect(html).toContain('10 Boys · 7 Pt')
  })
})
