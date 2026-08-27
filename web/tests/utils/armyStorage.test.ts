import { describe, expect, it } from '@jest/globals'
import type { ArmyCardEntry, Card, RosterEntry, Unit, UnitOption, UnitProfile } from '../../src/types.js'
import {
  createArmyCardEntry,
  createRosterEntry,
  normalizeRosterEntry,
  sortArmyCards,
  toggleRosterOption,
} from '../../src/utils/armyStorage.js'

describe('normalizeRosterEntry', () => {
  it('sums profile points and selected option points', () => {
    const entry: RosterEntry = {
      id: '1',
      unitNo: 1,
      unitName: 'Boyz',
      unitType: 'Troops',
      profileKind: 'primary',
      profileIndex: 0,
      profileLabel: 'Primary Profile',
      profilePoints: 5,
      selectedOptions: [
        { index: 0, points: 2 },
        { index: 1, points: 1 },
      ],
      points: 0,
    }

    expect(normalizeRosterEntry(entry).points).toBe(8)
  })

  it('falls back to points when profilePoints is missing and clears invalid options', () => {
    const entry = {
      id: '1',
      unitNo: 1,
      unitName: 'Boyz',
      unitType: 'Troops',
      profileKind: 'primary' as const,
      profileIndex: 0,
      profileLabel: 'Primary Profile',
      points: 4,
      selectedOptions: null,
    } as unknown as RosterEntry

    const normalized = normalizeRosterEntry(entry)
    expect(normalized.profilePoints).toBe(4)
    expect(normalized.selectedOptions).toEqual([])
    expect(normalized.points).toBe(4)
  })
})

describe('sortArmyCards', () => {
  it('sorts by set then nm without mutating the input', () => {
    const cards: ArmyCardEntry[] = [
      {
        id: 'a',
        cardId: 'Core-2-Orks',
        name: 'B',
        set: 'Core',
        nm: 2,
        fac: 'Orks',
        type: 'Order',
        ability: '',
      },
      {
        id: 'b',
        cardId: 'Alpha-1-Orks',
        name: 'A',
        set: 'Alpha',
        nm: 1,
        fac: 'Orks',
        type: 'Order',
        ability: '',
      },
      {
        id: 'c',
        cardId: 'Core-1-Orks',
        name: 'C',
        set: 'Core',
        nm: 1,
        fac: 'Orks',
        type: 'Order',
        ability: '',
      },
    ]

    const sorted = sortArmyCards(cards)
    expect(sorted.map((card) => card.id)).toEqual(['b', 'c', 'a'])
    expect(cards.map((card) => card.id)).toEqual(['a', 'b', 'c'])
  })
})

describe('createArmyCardEntry', () => {
  it('maps card fields onto an army card entry with a unique id', () => {
    const card: Card = {
      id: 'Core-1-Orks',
      set: 'Core',
      nm: 1,
      fac: 'Orks',
      name: 'Waaagh',
      type: 'Order',
      subType: 'Tactic',
      facNm: 3,
      ability: 'Do the thing',
    }

    const entry = createArmyCardEntry(card)
    expect(entry.cardId).toBe(card.id)
    expect(entry.name).toBe('Waaagh')
    expect(entry.set).toBe('Core')
    expect(entry.nm).toBe(1)
    expect(entry.fac).toBe('Orks')
    expect(entry.type).toBe('Order')
    expect(entry.subType).toBe('Tactic')
    expect(entry.facNm).toBe(3)
    expect(entry.ability).toBe('Do the thing')
    expect(entry.id).toEqual(expect.any(String))
    expect(entry.id).not.toBe(card.id)
  })
})

describe('createRosterEntry', () => {
  it('maps unit and profile fields onto a roster entry', () => {
    const unit: Unit = {
      no: 7,
      type: 'Troops',
      name: 'Boyz',
      stats: { N: '10', Pt: '5' },
    }
    const profile: UnitProfile = {
      kind: 'primary',
      index: 0,
      label: 'Primary Profile',
      stats: unit.stats!,
      points: 5,
    }

    const entry = createRosterEntry(unit, profile, {
      factionId: 'Apoc40k-Armies-1st - Orks',
      factionName: 'Orks',
    })
    expect(entry.factionId).toBe('Apoc40k-Armies-1st - Orks')
    expect(entry.factionName).toBe('Orks')
    expect(entry.unitNo).toBe(7)
    expect(entry.unitName).toBe('Boyz')
    expect(entry.unitType).toBe('Troops')
    expect(entry.profileKind).toBe('primary')
    expect(entry.profileIndex).toBe(0)
    expect(entry.profileLabel).toBe('Primary Profile')
    expect(entry.profilePoints).toBe(5)
    expect(entry.modelCount).toBe('10')
    expect(entry.selectedOptions).toEqual([])
    expect(entry.points).toBe(5)
    expect(entry.id).toEqual(expect.any(String))
  })
})

describe('toggleRosterOption', () => {
  const unitOptions: UnitOption[] = [
    {
      per: 'up to 4',
      limit: 'group Exclusive',
      group: 'weapon',
      text: 'Rokkit Launcha',
      Pt: '+1',
    },
    {
      per: 'up to 4',
      limit: 'group Exclusive',
      group: 'weapon',
      text: 'Killa Klaw',
      Pt: '+1',
    },
  ]

  const baseEntry: RosterEntry = {
    id: '1',
    factionId: 'Apoc40k-Armies-1st - Orks',
    factionName: 'Orks',
    unitNo: 1,
    unitName: 'Deff Dread',
    unitType: 'Walker',
    profileKind: 'primary',
    profileIndex: 0,
    profileLabel: 'Primary Profile',
    profilePoints: 5,
    selectedOptions: [],
    points: 5,
  }

  const summary = { label: '+1 Pt', text: 'Rokkit Launcha', points: 1 }

  it('selects one option in an exclusive group slot', () => {
    const updated = toggleRosterOption(baseEntry, 0, summary, unitOptions, { slotIndex: 0 })
    expect(updated.selectedOptions).toEqual([{ index: 0, slotIndex: 0, ...summary }])
    expect(updated.points).toBe(6)
  })

  it('deselects when clicking the same exclusive radio again', () => {
    const selected: RosterEntry = {
      ...baseEntry,
      selectedOptions: [{ index: 0, slotIndex: 0, ...summary }],
      points: 6,
    }

    const updated = toggleRosterOption(selected, 0, summary, unitOptions, { slotIndex: 0 })
    expect(updated.selectedOptions).toEqual([])
    expect(updated.points).toBe(5)
  })

  it('replaces the selection when choosing a different option in the same slot', () => {
    const selected: RosterEntry = {
      ...baseEntry,
      selectedOptions: [{ index: 0, slotIndex: 0, ...summary }],
      points: 6,
    }
    const otherSummary = { label: '+1 Pt', text: 'Killa Klaw', points: 1 }

    const updated = toggleRosterOption(selected, 1, otherSummary, unitOptions, { slotIndex: 0 })
    expect(updated.selectedOptions).toEqual([{ index: 1, slotIndex: 0, ...otherSummary }])
    expect(updated.points).toBe(6)
  })

  it('selects per-10-models exclusive options in separate slots', () => {
    const perTenOptions: UnitOption[] = [
      {
        per: 'per 10 models',
        limit: 'group Exclusive',
        group: 'heavy weapons',
        text: 'Big Shoota',
        Pt: '+1',
      },
      {
        per: 'per 10 models',
        limit: 'group Exclusive',
        group: 'heavy weapons',
        text: 'Rokkit Launcha',
        Pt: '+1',
      },
    ]
    const bigShoota = { label: '+1 Pt', text: 'Big Shoota', points: 1 }
    const rokkit = { label: '+1 Pt', text: 'Rokkit Launcha', points: 1 }

    const slot0 = toggleRosterOption(baseEntry, 0, bigShoota, perTenOptions, { slotIndex: 0 })
    const slot1 = toggleRosterOption(slot0, 1, rokkit, perTenOptions, { slotIndex: 1 })

    expect(slot1.selectedOptions).toEqual([
      { index: 0, slotIndex: 0, ...bigShoota },
      { index: 1, slotIndex: 1, ...rokkit },
    ])
    expect(slot1.points).toBe(7)
  })

  it('selects one choose-one radio choice', () => {
    const chooseOneOptions: UnitOption[] = [
      {
        per: 'Per Unit',
        text: 'Can be equipped with one of:',
        Pt: '1',
        chooseOne: [
          '1 Aeldari Missile Launcher',
          '1 Bright Lance',
          '1 Scatter Laser',
        ],
      },
    ]
    const summary = { label: '+1 Pt', text: '1 Bright Lance', points: 1 }

    const updated = toggleRosterOption(baseEntry, 0, summary, chooseOneOptions, { choiceIndex: 1 })
    expect(updated.selectedOptions).toEqual([{ index: 0, choiceIndex: 1, ...summary }])
    expect(updated.points).toBe(6)
  })

  it('deselects a choose-one radio when clicking the selected choice', () => {
    const chooseOneOptions: UnitOption[] = [
      {
        per: 'Per Unit',
        text: 'Can be equipped with one of:',
        Pt: '1',
        chooseOne: ['1 Bright Lance', '1 Starcannon'],
      },
    ]
    const summary = { label: '+1 Pt', text: '1 Bright Lance', points: 1 }
    const selected: RosterEntry = {
      ...baseEntry,
      selectedOptions: [{ index: 0, choiceIndex: 0, ...summary }],
      points: 6,
    }

    const updated = toggleRosterOption(selected, 0, summary, chooseOneOptions, { choiceIndex: 0 })
    expect(updated.selectedOptions).toEqual([])
    expect(updated.points).toBe(5)
  })

  it('replaces a choose-one selection when picking a different choice', () => {
    const chooseOneOptions: UnitOption[] = [
      {
        per: 'Per Unit',
        text: 'Can be equipped with one of:',
        Pt: '1',
        chooseOne: ['1 Bright Lance', '1 Starcannon'],
      },
    ]
    const lance = { label: '+1 Pt', text: '1 Bright Lance', points: 1 }
    const star = { label: '+1 Pt', text: '1 Starcannon', points: 1 }
    const selected: RosterEntry = {
      ...baseEntry,
      selectedOptions: [{ index: 0, choiceIndex: 0, ...lance }],
      points: 6,
    }

    const updated = toggleRosterOption(selected, 0, star, chooseOneOptions, { choiceIndex: 1 })
    expect(updated.selectedOptions).toEqual([{ index: 0, choiceIndex: 1, ...star }])
    expect(updated.points).toBe(6)
  })

  it('allows multiple choices up to a numeric choose limit', () => {
    const chooseTwoOptions: UnitOption[] = [
      {
        per: 'Per Unit',
        text: 'Choose two weapons:',
        chooseOne: ['Bright Lance', 'Scatter Laser', 'Starcannon'],
        chooseLimit: 2,
      },
    ]
    const lance = { label: 'Option', text: 'Bright Lance', points: 0 }
    const scatter = { label: 'Option', text: 'Scatter Laser', points: 0 }

    const first = toggleRosterOption(baseEntry, 0, lance, chooseTwoOptions, { choiceIndex: 0 })
    const second = toggleRosterOption(first, 0, scatter, chooseTwoOptions, { choiceIndex: 1 })

    expect(second.selectedOptions).toEqual([
      { index: 0, choiceIndex: 0, ...lance },
      { index: 0, choiceIndex: 1, ...scatter },
    ])
  })

  it('drops the earliest selection when selecting over a numeric choose limit', () => {
    const chooseTwoOptions: UnitOption[] = [
      {
        per: 'Per Unit',
        text: 'Choose two weapons:',
        chooseOne: ['Bright Lance', 'Scatter Laser', 'Starcannon'],
        chooseLimit: 2,
      },
    ]
    const lance = { label: 'Option', text: 'Bright Lance', points: 0 }
    const scatter = { label: 'Option', text: 'Scatter Laser', points: 0 }
    const star = { label: 'Option', text: 'Starcannon', points: 0 }
    const selected: RosterEntry = {
      ...baseEntry,
      selectedOptions: [
        { index: 0, choiceIndex: 0, ...lance },
        { index: 0, choiceIndex: 1, ...scatter },
      ],
    }

    const updated = toggleRosterOption(selected, 0, star, chooseTwoOptions, { choiceIndex: 2 })

    expect(updated.selectedOptions).toEqual([
      { index: 0, choiceIndex: 1, ...scatter },
      { index: 0, choiceIndex: 2, ...star },
    ])
  })

  it('treats up-to slots as separate choose groups', () => {
    const upToChoose: UnitOption[] = [
      {
        per: 'up to 4',
        title: 'Weapon',
        text: 'Exchange 1 Dread Klaw for',
        chooseOne: ['Rokkit Launcha', 'Kustom Mega-Blasta', 'Skorcha', 'Big Shoota'],
      },
    ]
    const rokkit = { label: 'Weapon', text: 'Rokkit Launcha', points: 0 }
    const skorcha = { label: 'Weapon', text: 'Skorcha', points: 0 }

    const first = toggleRosterOption(baseEntry, 0, rokkit, upToChoose, {
      slotIndex: 0,
      choiceIndex: 0,
    })
    const second = toggleRosterOption(first, 0, skorcha, upToChoose, {
      slotIndex: 1,
      choiceIndex: 2,
    })

    expect(second.selectedOptions).toEqual([
      { index: 0, slotIndex: 0, choiceIndex: 0, ...rokkit },
      { index: 0, slotIndex: 1, choiceIndex: 2, ...skorcha },
    ])
  })

  it('replaces the choice in a single up-to slot without clearing other slots', () => {
    const upToChoose: UnitOption[] = [
      {
        per: 'up to 4',
        title: 'Weapon',
        text: 'Exchange 1 Dread Klaw for',
        chooseOne: ['Rokkit Launcha', 'Kustom Mega-Blasta', 'Skorcha'],
      },
    ]
    const rokkit = { label: 'Weapon', text: 'Rokkit Launcha', points: 0 }
    const blasta = { label: 'Weapon', text: 'Kustom Mega-Blasta', points: 0 }
    const skorcha = { label: 'Weapon', text: 'Skorcha', points: 0 }
    const selected: RosterEntry = {
      ...baseEntry,
      selectedOptions: [
        { index: 0, slotIndex: 0, choiceIndex: 0, ...rokkit },
        { index: 0, slotIndex: 1, choiceIndex: 2, ...skorcha },
      ],
    }

    const updated = toggleRosterOption(selected, 0, blasta, upToChoose, {
      slotIndex: 0,
      choiceIndex: 1,
    })

    expect(updated.selectedOptions).toEqual([
      { index: 0, slotIndex: 1, choiceIndex: 2, ...skorcha },
      { index: 0, slotIndex: 0, choiceIndex: 1, ...blasta },
    ])
  })

  it('treats per-10-models slots as separate choose groups', () => {
    const perTenChoose: UnitOption[] = [
      {
        per: 'Per 10 models',
        Pt: '1',
        title: 'Heavy Weapon',
        text: 'May gain a Heavy Weapon Platform Model with',
        chooseOne: ['Bright Lance', 'Scatter Laser', 'Shuriken Cannon'],
      },
    ]
    const lance = { label: '+1 Pt', text: 'Bright Lance', points: 1 }
    const scatter = { label: '+1 Pt', text: 'Scatter Laser', points: 1 }

    const first = toggleRosterOption(baseEntry, 0, lance, perTenChoose, {
      slotIndex: 0,
      choiceIndex: 0,
    })
    const second = toggleRosterOption(first, 0, scatter, perTenChoose, {
      slotIndex: 1,
      choiceIndex: 1,
    })

    expect(second.selectedOptions).toEqual([
      { index: 0, slotIndex: 0, choiceIndex: 0, ...lance },
      { index: 0, slotIndex: 1, choiceIndex: 1, ...scatter },
    ])
    expect(second.points).toBe(7)
  })
})
