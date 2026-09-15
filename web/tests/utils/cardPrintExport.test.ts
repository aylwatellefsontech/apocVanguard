import { describe, expect, it } from '@jest/globals'
import type { ArmyCardEntry } from '../../src/types.js'
import type { Card } from '../../src/types.js'
import { armyCardEntryToCard, generateCommandCardsPrintHtml } from '../../src/utils/cardPrintExport.js'

describe('armyCardEntryToCard', () => {
  it('maps an army card entry onto a Card using cardId as id', () => {
    const entry: ArmyCardEntry = {
      id: 'instance-1',
      cardId: 'Core-1-Orks',
      name: 'Waaagh',
      set: 'Core',
      nm: 1,
      fac: 'Orks',
      type: 'Order',
      subType: 'Tactic',
      facNm: 4,
      ability: 'Charge!',
    }

    expect(armyCardEntryToCard(entry)).toEqual({
      id: 'Core-1-Orks',
      set: 'Core',
      nm: 1,
      fac: 'Orks',
      name: 'Waaagh',
      type: 'Order',
      subType: 'Tactic',
      facNm: 4,
      ability: 'Charge!',
    })
  })
})

describe('generateCommandCardsPrintHtml', () => {
  // US-004 / US-013: printable command-card sheet
  it('includes the title and card names', () => {
    const cards: Card[] = [
      {
        id: 'Core-1-Orks',
        set: 'Core',
        nm: 1,
        fac: 'Orks',
        name: 'Waaagh',
        type: 'Order',
        ability: 'Charge!',
      },
    ]

    const html = generateCommandCardsPrintHtml(cards, 'Orks — Command Cards')
    expect(html).toContain('Orks — Command Cards')
    expect(html).toContain('Waaagh')
    expect(html).toContain('1 cards')
  })

  it('still builds a sheet when the card list is empty', () => {
    const html = generateCommandCardsPrintHtml([], 'Empty')
    expect(html).toContain('Empty')
    expect(html).toContain('0 cards')
  })
})
