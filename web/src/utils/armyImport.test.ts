import { beforeEach, describe, expect, it } from '@jest/globals'
import { MAX_SAVED_ARMIES, SAVED_ARMIES_KEY } from '../constants.js'
import type { SavedArmy } from '../types.js'
import { encodeArmyExport } from './armyExport.js'
import { importAndSaveArmyFromCode } from './armyImport.js'
import { loadSavedArmies } from './armyStorage.js'

const sampleArmy: SavedArmy = {
  id: 'army-1',
  name: 'Waaagh!',
  factionId: 'Apoc40k-Armies-1st - Orks',
  factionName: 'Orks',
  totalPoints: 5,
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
      selectedOptions: [],
      points: 5,
    },
  ],
  cards: [],
}

function installMemoryLocalStorage() {
  const store = new Map<string, string>()
  Object.defineProperty(globalThis, 'localStorage', {
    configurable: true,
    value: {
      getItem: (key: string) => store.get(key) ?? null,
      setItem: (key: string, value: string) => {
        store.set(key, value)
      },
      removeItem: (key: string) => {
        store.delete(key)
      },
      clear: () => store.clear(),
    },
  })
}

describe('importAndSaveArmyFromCode', () => {
  // US-011: import a code and save it, subject to the 8-army cap
  beforeEach(() => {
    installMemoryLocalStorage()
  })

  it('returns an error when the paste is empty', () => {
    const result = importAndSaveArmyFromCode('   ')
    expect(result.ok).toBe(false)
    if (result.ok) {
      return
    }
    expect(result.error).toMatch(/paste an army export code/i)
  })

  it('returns an error for invalid text', () => {
    const result = importAndSaveArmyFromCode('not-an-army')
    expect(result.ok).toBe(false)
    if (result.ok) {
      return
    }
    expect(result.error.length).toBeGreaterThan(0)
  })

  it('rejects import when the saved-army cap is already reached', () => {
    const code = encodeArmyExport(sampleArmy, new Date('2026-08-27T12:00:00'))
    const result = importAndSaveArmyFromCode(code, MAX_SAVED_ARMIES)
    expect(result.ok).toBe(false)
    if (result.ok) {
      return
    }
    expect(result.error).toMatch(/only save up to 8 armies/i)
    expect(localStorage.getItem(SAVED_ARMIES_KEY)).toBeNull()
  })

  it('saves a valid export code as a new army', () => {
    const code = encodeArmyExport(sampleArmy, new Date('2026-08-27T12:00:00'))
    const result = importAndSaveArmyFromCode(code, 0)
    expect(result.ok).toBe(true)
    if (!result.ok) {
      return
    }

    expect(result.army.name).toBe('Waaagh!')
    expect(loadSavedArmies()).toHaveLength(1)
    expect(loadSavedArmies()[0]?.name).toBe('Waaagh!')
  })
})
