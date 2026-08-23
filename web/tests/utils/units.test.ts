import { describe, expect, it } from '@jest/globals'
import type { RosterEntry, Unit } from '../../src/types.js'
import {
  getProfileAbilitySections,
  getProfileKeywordSections,
  getProfileTraitSections,
  getProfileWeaponSections,
  getUnitProfiles,
  getUnitWeightKeyword,
  groupUnitsByType,
  parsePoints,
  sortRosterByType,
  unitHasInfantryKeyword,
} from '../../src/utils/units.js'

function makeUnit(overrides: Partial<Unit> & Pick<Unit, 'no' | 'type' | 'name'>): Unit {
  return { ...overrides }
}

function makeRosterEntry(
  overrides: Partial<RosterEntry> & Pick<RosterEntry, 'id' | 'unitName' | 'unitType'>,
): RosterEntry {
  return {
    unitNo: 1,
    profileKind: 'primary',
    profileIndex: 0,
    profileLabel: 'Primary Profile',
    profilePoints: 0,
    selectedOptions: [],
    points: 0,
    ...overrides,
  }
}

describe('parsePoints', () => {
  it('parses a numeric Pt value', () => {
    expect(parsePoints({ Pt: '12' })).toBe(12)
  })

  it('returns 0 when Pt is missing or invalid', () => {
    expect(parsePoints(undefined)).toBe(0)
    expect(parsePoints({})).toBe(0)
    expect(parsePoints({ Pt: 'abc' })).toBe(0)
  })
})

describe('getUnitProfiles', () => {
  it('returns an empty list for nullish units', () => {
    expect(getUnitProfiles(null)).toEqual([])
    expect(getUnitProfiles(undefined)).toEqual([])
  })

  it('builds primary and alt profiles with points', () => {
    const unit = makeUnit({
      no: 1,
      type: 'Troops',
      name: 'Boyz',
      stats: { Pt: '5', N: '10' },
      profiles: [{ name: '20 Boyz', Pt: '10', N: '20' }],
    })

    expect(getUnitProfiles(unit)).toEqual([
      {
        kind: 'primary',
        index: 0,
        label: 'Primary Profile',
        stats: { Pt: '5', N: '10' },
        points: 5,
      },
      {
        kind: 'alt',
        index: 0,
        label: '20 Boyz',
        stats: { name: '20 Boyz', Pt: '10', N: '20' },
        points: 10,
      },
    ])
  })
})

describe('groupUnitsByType', () => {
  it('groups units in TYPE_ORDER and appends unknown types', () => {
    const units = [
      makeUnit({ no: 1, type: 'Unknown', name: 'Odd' }),
      makeUnit({ no: 2, type: 'Troops', name: 'A' }),
      makeUnit({ no: 3, type: 'HQ', name: 'B' }),
      makeUnit({ no: 4, type: 'Troops', name: 'C' }),
    ]

    const grouped = groupUnitsByType(units)
    expect(grouped.map(([type]) => type)).toEqual(['HQ', 'Troops', 'Unknown'])
    expect(grouped[1]?.[1].map((unit) => unit.name)).toEqual(['A', 'C'])
  })
})

describe('sortRosterByType', () => {
  it('sorts by type order then unit name', () => {
    const roster = [
      makeRosterEntry({ id: '1', unitName: 'Zebra', unitType: 'Troops' }),
      makeRosterEntry({ id: '2', unitName: 'Alpha', unitType: 'Troops' }),
      makeRosterEntry({ id: '3', unitName: 'Boss', unitType: 'HQ' }),
    ]

    expect(sortRosterByType(roster).map((entry) => entry.id)).toEqual(['3', '2', '1'])
  })
})

describe('unitHasInfantryKeyword', () => {
  it('returns true when Infantry is present case-insensitively', () => {
    expect(
      unitHasInfantryKeyword(makeUnit({ no: 1, type: 'Troops', name: 'A', keywords: ['Light', 'Infantry'] })),
    ).toBe(true)
  })

  it('returns false for null units or missing Infantry', () => {
    expect(unitHasInfantryKeyword(null)).toBe(false)
    expect(unitHasInfantryKeyword(makeUnit({ no: 1, type: 'Troops', name: 'A', keywords: ['Vehicle'] }))).toBe(
      false,
    )
  })
})

describe('getUnitWeightKeyword', () => {
  it('returns the first light or heavy keyword', () => {
    expect(
      getUnitWeightKeyword(makeUnit({ no: 1, type: 'Troops', name: 'A', keywords: ['Infantry', 'Heavy'] })),
    ).toBe('Heavy')
  })

  it('returns null when no weight keyword is present', () => {
    expect(getUnitWeightKeyword(makeUnit({ no: 1, type: 'Troops', name: 'A', keywords: ['Infantry'] }))).toBe(
      null,
    )
    expect(getUnitWeightKeyword(null)).toBe(null)
  })
})

describe('getProfileAbilitySections', () => {
  const unit = makeUnit({
    no: 3,
    type: 'HQ',
    name: 'Big Mek',
    stats: { Pt: '5' },
    abilities: 'Kustom Force Field.',
    profileAbilities: 'It is equipped with: Shokk Attack Gun; Mek Weapons.',
    profiles: [
      {
        name: 'Mega Armour',
        Pt: '5',
        abilities: 'It is equipped with Mek Mega Weapons instead of 1 Shokk Attack Gun and Mek Weapons.',
      },
    ],
  })

  it('returns every profile ability section when no profile is selected', () => {
    expect(getProfileAbilitySections(unit)).toEqual([
      {
        heading: 'Base Profile Abilities',
        text: 'It is equipped with: Shokk Attack Gun; Mek Weapons.',
      },
      {
        heading: 'Mega Armour Abilities',
        text: 'It is equipped with Mek Mega Weapons instead of 1 Shokk Attack Gun and Mek Weapons.',
      },
    ])
  })

  it('returns only the selected profile ability section', () => {
    expect(getProfileAbilitySections(unit, 'Mega Armour')).toEqual([
      {
        heading: 'Mega Armour Abilities',
        text: 'It is equipped with Mek Mega Weapons instead of 1 Shokk Attack Gun and Mek Weapons.',
      },
    ])
  })

  it('returns an empty list when no profile abilities exist', () => {
    expect(getProfileAbilitySections(makeUnit({ no: 1, type: 'HQ', name: 'Warboss', abilities: 'Waaagh!' }))).toEqual([])
    expect(getProfileAbilitySections(null)).toEqual([])
  })
})

describe('profile keyword, trait, and weapon sections', () => {
  const unit = makeUnit({
    no: 1,
    type: 'HQ',
    name: 'Farseer',
    stats: { Pt: '4' },
    keywords: ['Aeldari'],
    profileKeywords: ['Infantry'],
    traits: ['Psyker'],
    profileTraits: ['Character'],
    weapons: [{ name: 'Witchblade', type: 'Melee' }],
    profileWeapons: [{ name: 'Shuriken Pistol', type: 'Pistol' }],
    profiles: [
      {
        name: 'Sky Runner',
        Pt: '6',
        keywords: ['Biker', 'Fly'],
        traits: ['Jetbike'],
        weapons: [{ name: 'Twin Shuriken Catapult', type: 'Assault' }],
      },
    ],
  })

  it('returns every profile extra section when no profile is selected', () => {
    expect(getProfileKeywordSections(unit)).toEqual([
      { heading: 'Base Profile Keywords', items: ['Infantry'] },
      { heading: 'Sky Runner Keywords', items: ['Biker', 'Fly'] },
    ])
    expect(getProfileTraitSections(unit)).toEqual([
      { heading: 'Base Profile Traits', items: ['Character'] },
      { heading: 'Sky Runner Traits', items: ['Jetbike'] },
    ])
    expect(getProfileWeaponSections(unit).map((section) => section.heading)).toEqual([
      'Base Profile Weapons',
      'Sky Runner Weapons',
    ])
  })

  it('returns only the selected profile extra sections', () => {
    expect(getProfileKeywordSections(unit, 'Sky Runner')).toEqual([
      { heading: 'Sky Runner Keywords', items: ['Biker', 'Fly'] },
    ])
    expect(getProfileTraitSections(unit, 'Primary Profile')).toEqual([
      { heading: 'Base Profile Traits', items: ['Character'] },
    ])
  })
})
