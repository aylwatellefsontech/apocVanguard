import {
  buildArmyDraftFromSaved,
  clearBuildArmyDraft,
  emptyBuildArmyDraft,
  loadBuildArmyDraft,
  resolveBuildArmyInitialState,
  saveBuildArmyDraft,
} from '../../src/utils/buildArmyDraftStorage'
import type { SavedArmy } from '../../src/types'

const savedArmy: SavedArmy = {
  id: 'army-1',
  name: 'Test',
  factionId: 'orks',
  factionName: 'Orks',
  totalPoints: 100,
  updatedAt: '2026-01-01T00:00:00.000Z',
  roster: [
    {
      id: 'entry-1',
      unitNo: 1,
      unitName: 'Warboss',
      factionId: 'orks',
      factionName: 'Orks',
      profilePoints: 100,
      points: 100,
      selectedOptions: [],
    },
  ],
  cards: [],
}

describe('buildArmyDraftStorage', () => {
  beforeEach(() => {
    clearBuildArmyDraft()
  })

  it('restores draft when routeArmyId matches', () => {
    saveBuildArmyDraft({
      ...emptyBuildArmyDraft(null),
      armyName: 'WIP',
      roster: savedArmy.roster,
    })

    const resolved = resolveBuildArmyInitialState(undefined, null)
    expect(resolved.armyName).toBe('WIP')
    expect(resolved.roster).toHaveLength(1)
  })

  it('uses saved army when draft is for a different route', () => {
    saveBuildArmyDraft({
      ...emptyBuildArmyDraft(null),
      armyName: 'Stale draft',
    })

    const resolved = resolveBuildArmyInitialState('army-1', savedArmy)
    expect(resolved.armyName).toBe('Test')
    expect(resolved.editingArmyId).toBe('army-1')
  })

  it('round-trips through sessionStorage', () => {
    saveBuildArmyDraft(buildArmyDraftFromSaved(savedArmy, null))
    expect(loadBuildArmyDraft()?.editingArmyId).toBe('army-1')
  })
})
