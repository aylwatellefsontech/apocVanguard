import { describe, expect, it } from '@jest/globals'
import type { ArmyCardEntry } from '../../src/types.js'
import { armyCardEntryToCard } from '../../src/utils/cardPrintExport.js'

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
