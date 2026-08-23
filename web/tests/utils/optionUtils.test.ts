import { describe, expect, it } from '@jest/globals'
import {
  formatPerModelsSlotLegend,
  getChooseInstanceCount,
  getChooseLimit,
  getChooseOneChoices,
  getPerModelsInterval,
  getPerModelsSlotCount,
  isChooseOneOption,
  isPerModelsOption,
  optionUsesSlotIndex,
  parseChooseOneChoices,
} from '../../src/utils/optionUtils.js'

describe('per models options', () => {
  const perTenOption = {
    per: 'per 10 models',
    text: 'Equip with 1 Big Shoota',
    Pt: '+1',
    limit: 'group Exclusive',
    group: 'heavy weapons',
  }

  it('detects per models options', () => {
    expect(isPerModelsOption(perTenOption)).toBe(true)
    expect(isPerModelsOption({ per: 'Per Model', text: 'x' })).toBe(false)
  })

  it('parses the model interval', () => {
    expect(getPerModelsInterval(perTenOption)).toBe(10)
  })

  it('computes slot count from profile N (rounded down)', () => {
    expect(getPerModelsSlotCount(perTenOption, { N: '10' })).toBe(1)
    expect(getPerModelsSlotCount(perTenOption, { N: '20' })).toBe(2)
    expect(getPerModelsSlotCount(perTenOption, { N: '22' })).toBe(2)
    expect(getPerModelsSlotCount(perTenOption, { N: '30' })).toBe(3)
    expect(getPerModelsSlotCount(perTenOption, { N: '9' })).toBe(0)
  })

  it('supports arbitrary per-model intervals', () => {
    const perThree = { per: 'per 3 models', text: 'Upgrade', Pt: '+1' }
    expect(getPerModelsInterval(perThree)).toBe(3)
    expect(getPerModelsSlotCount(perThree, { N: '22' })).toBe(7)
    expect(getPerModelsSlotCount(perThree, { N: '2' })).toBe(0)
  })

  it('formats slot legends', () => {
    expect(formatPerModelsSlotLegend(0, 10, 'heavy weapons')).toBe(
      'heavy weapons (Models 1–10)',
    )
    expect(formatPerModelsSlotLegend(1, 10, 'heavy weapons')).toBe(
      'heavy weapons (Models 11–20)',
    )
  })
})

describe('choose one options', () => {
  const wraithlord = {
    per: 'Per Unit',
    Pt: '1',
    text: 'Can be equipped with one of:',
    chooseOne: [
      '1 Aeldari Missile Launcher',
      '1 Bright Lance',
      '1 Scatter Laser',
      '1 Shuriken Cannon',
      '1 Starcannon',
    ],
  }

  it('parses semicolon-separated choices', () => {
    expect(
      parseChooseOneChoices(
        '1 Aeldari Missile Launcher; 1 Bright Lance; 1 Starcannon.',
      ),
    ).toEqual(['1 Aeldari Missile Launcher', '1 Bright Lance', '1 Starcannon'])
  })

  it('reads chooseOne from an option object', () => {
    expect(isChooseOneOption(wraithlord)).toBe(true)
    expect(getChooseOneChoices(wraithlord)).toEqual(wraithlord.chooseOne)
    expect(getChooseLimit(wraithlord)).toBe(1)
    expect(optionUsesSlotIndex(wraithlord)).toBe(true)
  })

  it('supports numeric choose limits', () => {
    const chooseThree = {
      ...wraithlord,
      chooseLimit: 3,
    }

    expect(getChooseLimit(chooseThree)).toBe(3)
  })

  it('creates one choose group per up-to or per-models slot', () => {
    expect(getChooseInstanceCount({ ...wraithlord, per: 'up to 4' })).toBe(4)
    expect(
      getChooseInstanceCount(
        {
          per: 'Per 10 models',
          chooseOne: ['Bright Lance', 'Scatter Laser'],
        },
        { N: '20' },
      ),
    ).toBe(2)
    expect(
      getChooseInstanceCount(
        {
          per: 'Per 10 models',
          chooseOne: ['Bright Lance'],
        },
        { N: '9' },
      ),
    ).toBe(0)
  })
})
