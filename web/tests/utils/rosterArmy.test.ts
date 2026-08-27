import { describe, expect, it } from '@jest/globals'
import type { RosterEntry } from '../../src/types.js'
import {
  deriveSavedArmyFactionMeta,
  rosterHasMultipleFactions,
  sortRosterByFactionAndName,
} from '../../src/utils/rosterArmy.js'

const orksEntry: RosterEntry = {
  id: 'orks-1',
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
  selectedOptions: [],
  points: 5,
}

const eldarEntry: RosterEntry = {
  id: 'eldar-1',
  factionId: 'Apoc40k-Armies-1st - Eldar',
  factionName: 'Eldar',
  unitNo: 6,
  unitName: 'Guardian',
  unitType: 'Troops',
  profileKind: 'primary',
  profileIndex: 0,
  profileLabel: '10 Guardians',
  profilePoints: 6,
  modelCount: '10',
  selectedOptions: [],
  points: 6,
}

describe('sortRosterByFactionAndName', () => {
  it('sorts by faction name then unit name', () => {
    const sorted = sortRosterByFactionAndName([orksEntry, eldarEntry])
    expect(sorted.map((entry) => entry.unitName)).toEqual(['Guardian', 'Boyz'])
  })
})

describe('deriveSavedArmyFactionMeta', () => {
  it('joins multiple faction names for mixed armies', () => {
    expect(
      deriveSavedArmyFactionMeta([orksEntry, eldarEntry], [], {
        factionId: 'Apoc40k-Armies-1st - Orks',
        factionName: 'Orks',
      }),
    ).toEqual({
      factionId: 'Apoc40k-Armies-1st - Eldar',
      factionName: 'Eldar / Orks',
    })
  })
})

describe('rosterHasMultipleFactions', () => {
  it('returns true when roster entries come from different factions', () => {
    expect(rosterHasMultipleFactions([orksEntry, eldarEntry])).toBe(true)
    expect(rosterHasMultipleFactions([orksEntry])).toBe(false)
  })
})
