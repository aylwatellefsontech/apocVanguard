import { describe, expect, it } from '@jest/globals'
import { summarizeOption } from '../../src/utils/formatOption.js'

describe('summarizeOption', () => {
  it('summarizes a string option with zero points', () => {
    expect(summarizeOption('May take a Boss Nob', null)).toEqual({
      label: null,
      text: 'May take a Boss Nob',
      points: 0,
    })
  })

  it('summarizes an object option and scales per-model points', () => {
    expect(
      summarizeOption(
        {
          per: 'Per 10 models',
          text: 'Take big shootas (Power Rating +1)',
          Pt: '+1',
        },
        { N: '20' },
      ),
    ).toEqual({
      label: '+1 Power Rating / Per 10 Models',
      text: 'Take big shootas',
      points: 2,
    })
  })

  it('uses title as the bold option label when present', () => {
    expect(
      summarizeOption(
        {
          per: 'Per Unit',
          title: 'Support Weapon',
          text: 'Can be equipped with one of:',
          Pt: '1',
        },
        null,
      ),
    ).toEqual({
      label: 'Support Weapon',
      text: 'Can be equipped with one of:',
      points: 1,
    })
  })

  it('summarizes per-selection points when requested', () => {
    expect(
      summarizeOption(
        {
          per: 'Per 10 models',
          text: 'Take big shootas',
          Pt: '+1',
        },
        { N: '20' },
        true,
      ),
    ).toEqual({
      label: '+1 Power Rating / Per 10 Models',
      text: 'Take big shootas',
      points: 1,
    })
  })
})
