import { describe, expect, it } from '@jest/globals'
import { hasFactionIcon } from './factionIcons.js'

describe('hasFactionIcon', () => {
  // US-001: Home only shows factions that have icons
  it('returns true for a known faction name', () => {
    expect(hasFactionIcon('Orks')).toBe(true)
    expect(hasFactionIcon('Space Marines')).toBe(true)
  })

  it('returns false for an unknown faction name', () => {
    expect(hasFactionIcon('Votann')).toBe(false)
    expect(hasFactionIcon('')).toBe(false)
  })
})
