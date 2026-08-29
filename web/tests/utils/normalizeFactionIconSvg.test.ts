import { describe, expect, it } from '@jest/globals'
import { readFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'
import { normalizeFactionIconSvg } from '../../src/utils/normalizeFactionIconSvg.js'

const testDir = dirname(fileURLToPath(import.meta.url))
const factionsDir = join(testDir, '../../src/assets/factions')

function loadIcon(name: string): string {
  return readFileSync(join(factionsDir, name), 'utf8')
}

describe('normalizeFactionIconSvg', () => {
  it('adds fill currentColor to filled paths missing an explicit fill', () => {
    const svg =
      '<svg><path style="stroke: currentColor; stroke-width: 20px;" d="M0 0 L10 0 L5 10 Z"/></svg>'
    const normalized = normalizeFactionIconSvg(svg)

    expect(normalized).toContain('fill: currentColor')
    expect(normalized).not.toMatch(/fill:\s*rgb\(0,\s*0,\s*0\)/i)
  })

  it('keeps outline shapes transparent', () => {
    const svg =
      '<svg><path style="fill: none; stroke: currentColor;" d="M0 0 L10 0 L5 10 Z"/></svg>'
    const normalized = normalizeFactionIconSvg(svg)

    expect(normalized).toContain('fill: none')
    expect(normalized).not.toContain('fill: currentColor; fill: none')
  })

  it('normalizes fill-only layers used by Space Marines skulls', () => {
    const svg =
      '<svg><path style="stroke: rgb(0, 0, 0); stroke-width: 0px;" d="M0 0 L10 0 L5 10 Z"/></svg>'
    const normalized = normalizeFactionIconSvg(svg)

    expect(normalized).toContain('fill: currentColor')
    expect(normalized).toContain('stroke: none')
  })

  it('uses fill none for stroked ellipses with a visible stroke width', () => {
    const svg =
      '<svg><ellipse style="stroke: currentColor; stroke-width: 20px;" cx="10" cy="10" rx="5" ry="5"/></svg>'
    const normalized = normalizeFactionIconSvg(svg)

    expect(normalized).toContain('fill: none')
  })

  it('fills thin stroked ellipses without a visible stroke width', () => {
    const svg = '<svg><ellipse style="stroke: rgb(0, 0, 0);" cx="10" cy="10" rx="5" ry="5"/></svg>'
    const normalized = normalizeFactionIconSvg(svg)

    expect(normalized).toContain('fill: currentColor')
    expect(normalized).toContain('stroke: none')
  })

  it('normalizes the affected faction icons without default black fills', () => {
    for (const file of [
      'knights.svg',
      'orks.svg',
      'imperial-guard.svg',
      'sisters-of-battle.svg',
      'space-marines.svg',
      'tyranids.svg',
    ]) {
      const normalized = normalizeFactionIconSvg(loadIcon(file))

      expect(normalized).not.toMatch(/fill:\s*rgb\(0,\s*0,\s*0\)/i)
      expect(normalized).not.toMatch(/\bfill="#(?:000000|000)"/i)
      expect(normalized).toMatch(/fill: currentColor/)
    }
  })
})
