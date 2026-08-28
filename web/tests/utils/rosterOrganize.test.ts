import { describe, expect, it } from '@jest/globals'
import type { RosterEntry } from '../../src/types.js'
import {
  assignRosterCardSlot,
  dedupeRosterCommanders,
  getRosterEntriesForCardSlot,
  rosterIsOrganized,
  sortRosterByOrganizeGroup,
  sortRosterForOrganizedArmyView,
  formatPrintRosterEntryMeta,
  toggleRosterCommander,
} from '../../src/utils/rosterOrganize.js'

function makeEntry(id: string, overrides: Partial<RosterEntry> = {}): RosterEntry {
  return {
    id,
    factionId: 'faction-1',
    factionName: 'Orks',
    unitNo: 1,
    unitName: `Unit ${id}`,
    unitType: 'Troops',
    profileKind: 'primary',
    profileIndex: 0,
    profileLabel: 'Primary',
    profilePoints: 5,
    selectedOptions: [],
    points: 5,
    ...overrides,
  }
}

describe('assignRosterCardSlot', () => {
  it('assigns a unit to a card slot', () => {
    const roster = [makeEntry('a')]
    const next = assignRosterCardSlot(roster, 'a', 2)

    expect(next[0]?.cardSlot).toBe(2)
    expect(next[0]?.isCommander).toBe(false)
  })

  it('clears commander status when unassigning', () => {
    const roster = [makeEntry('a', { cardSlot: 3, isCommander: true })]
    const next = assignRosterCardSlot(roster, 'a', null)

    expect(next[0]?.cardSlot).toBeUndefined()
    expect(next[0]?.isCommander).toBe(false)
  })

  it('clears commander status when moving to another card', () => {
    const roster = [makeEntry('a', { cardSlot: 1, isCommander: true })]
    const next = assignRosterCardSlot(roster, 'a', 4)

    expect(next[0]?.cardSlot).toBe(4)
    expect(next[0]?.isCommander).toBe(false)
  })
})

describe('toggleRosterCommander', () => {
  it('marks one commander per card slot and replaces the previous commander', () => {
    const roster = [
      makeEntry('a', { cardSlot: 2 }),
      makeEntry('b', { cardSlot: 2, isCommander: true }),
      makeEntry('c', { cardSlot: 3, isCommander: true }),
    ]

    const next = toggleRosterCommander(roster, 'a')
    expect(next.find((entry) => entry.id === 'a')?.isCommander).toBe(true)
    expect(next.find((entry) => entry.id === 'b')?.isCommander).toBe(false)
    expect(next.find((entry) => entry.id === 'c')?.isCommander).toBe(true)
  })

  it('deselects the commander when toggled again', () => {
    const roster = [makeEntry('a', { cardSlot: 1, isCommander: true })]
    const next = toggleRosterCommander(roster, 'a')

    expect(next[0]?.isCommander).toBe(false)
  })
})

describe('getRosterEntriesForCardSlot', () => {
  it('returns only entries in the requested slot', () => {
    const roster = [
      makeEntry('a', { cardSlot: 1 }),
      makeEntry('b', { cardSlot: 2 }),
      makeEntry('c', { cardSlot: 1 }),
    ]

    expect(getRosterEntriesForCardSlot(roster, 1).map((entry) => entry.id)).toEqual(['a', 'c'])
  })
})

describe('dedupeRosterCommanders', () => {
  it('keeps the first commander per card slot', () => {
    const roster = [
      makeEntry('a', { cardSlot: 1, isCommander: true }),
      makeEntry('b', { cardSlot: 1, isCommander: true }),
    ]

    const next = dedupeRosterCommanders(roster)
    expect(next.find((entry) => entry.id === 'a')?.isCommander).toBe(true)
    expect(next.find((entry) => entry.id === 'b')?.isCommander).toBe(false)
  })
})

describe('sortRosterByOrganizeGroup', () => {
  it('sorts by card slot, faction, commander, then name', () => {
    const roster = [
      makeEntry('z', { unitName: 'Zarbags', factionName: 'Orks', cardSlot: 2 }),
      makeEntry('a', { unitName: 'Alpha', factionName: 'Eldar', cardSlot: 1, isCommander: true }),
      makeEntry('b', { unitName: 'Beta', factionName: 'Eldar', cardSlot: 1 }),
      makeEntry('u', { unitName: 'Unassigned', factionName: 'Orks' }),
    ]

    expect(sortRosterByOrganizeGroup(roster).map((entry) => entry.id)).toEqual([
      'a',
      'b',
      'z',
      'u',
    ])
  })
})

describe('sortRosterForOrganizedArmyView', () => {
  it('sorts by card slot, faction, commander, unit type, then name', () => {
    const roster = [
      makeEntry('troop', { unitName: 'Troopers', unitType: 'Troops', cardSlot: 1 }),
      makeEntry('hq', {
        unitName: 'Boss',
        unitType: 'HQ',
        cardSlot: 1,
        isCommander: true,
        factionName: 'Orks',
      }),
      makeEntry('other', {
        unitName: 'Other',
        unitType: 'Elites',
        cardSlot: 1,
        factionName: 'Eldar',
      }),
    ]

    expect(sortRosterForOrganizedArmyView(roster).map((entry) => entry.id)).toEqual([
      'other',
      'hq',
      'troop',
    ])
  })
})

describe('formatPrintRosterEntryMeta', () => {
  it('includes detachment and commander as text', () => {
    const entry = makeEntry('a', {
      unitName: 'Warboss',
      cardSlot: 2,
      isCommander: true,
      unitType: 'HQ',
      profileLabel: '1 Warboss',
      points: 8,
    })

    expect(formatPrintRosterEntryMeta(entry)).toBe(
      'Detachment 2 · Commander · 1 Warboss · 8 Pt · HQ',
    )
  })

  it('omits organize fields when unassigned', () => {
    const entry = makeEntry('a', {
      unitName: 'Boyz',
      unitType: 'Troops',
      profileLabel: '10 Boys',
      points: 5,
    })

    expect(formatPrintRosterEntryMeta(entry)).toBe('10 Boys · 5 Pt · Troops')
  })
})

describe('rosterIsOrganized', () => {
  it('returns true when any unit has a card slot', () => {
    expect(rosterIsOrganized([makeEntry('a')])).toBe(false)
    expect(rosterIsOrganized([makeEntry('a', { cardSlot: 2 })])).toBe(true)
  })
})
