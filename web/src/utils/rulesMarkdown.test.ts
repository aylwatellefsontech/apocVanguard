import { describe, expect, it } from '@jest/globals'
import {
  extractRulesHeadings,
  parseHeadingLine,
  preprocessRulesMarkdown,
} from './rulesMarkdown.js'

describe('parseHeadingLine', () => {
  // US-015: heading title and optional explicit id
  it('returns the raw title when no id suffix is present', () => {
    expect(parseHeadingLine('Movement')).toEqual({ title: 'Movement', id: undefined })
  })

  it('splits an explicit {#id} suffix from the title', () => {
    expect(parseHeadingLine('Movement {#move}')).toEqual({ title: 'Movement', id: 'move' })
  })
})

describe('preprocessRulesMarkdown', () => {
  it('adds a slug id to a single heading line and keeps an explicit id', () => {
    expect(preprocessRulesMarkdown('# Rules')).toBe('# Rules {#rules}')
    expect(preprocessRulesMarkdown('## Dice {#dice}')).toBe('## Dice {#dice}')
  })

  it('unescapes markdown punctuation used in the rules text', () => {
    expect(preprocessRulesMarkdown('Save 4\\. or 6\\-')).toBe('Save 4. or 6-')
  })
})

describe('extractRulesHeadings', () => {
  it('builds a table of contents from headings that already have ids', () => {
    const source = '# Rules {#rules}\n\n## Movement {#movement}\n\n### Charge\n'
    expect(extractRulesHeadings(source)).toEqual([
      { level: 1, title: 'Rules', id: 'rules' },
      { level: 2, title: 'Movement', id: 'movement' },
    ])
  })

  it('skips headings that have no title or id', () => {
    expect(extractRulesHeadings('## \nnot a heading\n')).toEqual([])
  })
})
