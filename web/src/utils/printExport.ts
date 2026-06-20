import { STAT_KEYS } from '../constants'
import {
  calculateOptionPoints,
  formatOptionBody,
  formatOptionLabel,
} from './formatOption'
import { getUnitProfiles, groupUnitsByType, getProfileStatsForEntry, sortRosterByType } from './units'
import { formatRosterEntryMeta } from './roster'
import type {
  ArmyList,
  RosterEntry,
  SavedArmy,
  Unit,
  UnitOption,
  UnitStats,
  Weapon,
} from '../types'

function escapeHtml(value: string | number | null | undefined): string {
  if (value == null || value === '') {
    return '—'
  }

  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
}

function renderStatsTable(stats: UnitStats | null | undefined, label?: string): string {
  if (!stats) {
    return ''
  }

  const header = STAT_KEYS.map((key) => `<th>${escapeHtml(key)}</th>`).join('')
  const row = STAT_KEYS.map((key) => `<td>${escapeHtml(stats[key])}</td>`).join('')

  return `
    <div class="stats-block">
      ${label ? `<h4>${escapeHtml(label)}</h4>` : ''}
      <table class="data-table stats-table">
        <thead><tr>${header}</tr></thead>
        <tbody><tr>${row}</tr></tbody>
      </table>
    </div>
  `
}

function renderWeaponsTable(weapons: Weapon[] | undefined): string {
  if (!weapons?.length) {
    return ''
  }

  const rows = weapons
    .map((weapon) => {
      const skillAp = weapon.armorPen
        ? `${weapon.skill ?? '—'} / ${weapon.armorPen}`
        : (weapon.skill ?? '—')

      return `
        <tr>
          <td>${escapeHtml(weapon.name)}</td>
          <td>${escapeHtml(weapon.type)}</td>
          <td>${escapeHtml(weapon.range)}</td>
          <td>${escapeHtml(weapon.attacks)}</td>
          <td>${escapeHtml(skillAp)}</td>
          <td>${escapeHtml(weapon.abilities)}</td>
        </tr>
      `
    })
    .join('')

  return `
    <section>
      <h4>Weapons</h4>
      <table class="data-table weapons-table">
        <thead>
          <tr>
            <th>Weapon</th>
            <th>Type</th>
            <th>Rng</th>
            <th>A</th>
            <th>S/AP</th>
            <th>Abilities</th>
          </tr>
        </thead>
        <tbody>${rows}</tbody>
      </table>
    </section>
  `
}

function renderOptions(
  options: UnitOption[] | undefined,
  profileStats: UnitStats | null,
  selectedOptionIndexes?: number[],
): string {
  if (!options?.length) {
    return ''
  }

  const indexes =
    selectedOptionIndexes != null
      ? selectedOptionIndexes
      : options.map((_, index) => index)

  if (indexes.length === 0) {
    return ''
  }

  const items = indexes
    .map((index) => {
      const option = options[index]
      if (option == null) {
        return ''
      }

      const label = typeof option === 'string' ? 'Option' : formatOptionLabel(option)
      const body = typeof option === 'string' ? option : formatOptionBody(option)
      const points =
        typeof option === 'string' ? 0 : calculateOptionPoints(option, profileStats)
      const labelPrefix = label ? `<strong>${escapeHtml(label)}:</strong> ` : ''
      const pointsSuffix = points > 0 ? ` <span class="option-pts">+${points} Pt</span>` : ''

      return `<li>${labelPrefix}${escapeHtml(body)}${pointsSuffix}</li>`
    })
    .filter(Boolean)
    .join('')

  if (!items) {
    return ''
  }

  return `
    <section>
      <h4>Options</h4>
      <ul class="options-list">${items}</ul>
    </section>
  `
}

function renderUnitSheet(unit: Unit): string {
  const profiles = getUnitProfiles(unit)
  const profileStats = unit.stats ?? null
  const profileBlocks = profiles.map((profile) => renderStatsTable(profile.stats, profile.label)).join('')

  return renderUnitSheetContent({
    unitType: unit.type,
    unitName: unit.name,
    unitNo: unit.no,
    profileBlocks,
    weapons: unit.weapons,
    abilities: unit.abilities,
    keywords: unit.keywords,
    options: unit.options,
    profileStats,
  })
}

interface UnitSheetContent {
  unitType: string
  unitName: string
  unitNo?: number
  entryMeta?: string
  profileBlocks: string
  weapons?: Weapon[]
  abilities?: string
  keywords?: string[]
  options?: UnitOption[]
  profileStats: UnitStats | null
  selectedOptionIndexes?: number[]
  missingMessage?: string
}

function renderUnitSheetContent(content: UnitSheetContent): string {
  const keywords = content.keywords?.length
    ? `
      <section>
        <h4>Keywords</h4>
        <p class="keywords">${content.keywords.map((keyword) => escapeHtml(keyword)).join(', ')}</p>
      </section>
    `
    : ''

  const abilities = content.abilities
    ? `
      <section>
        <h4>Abilities</h4>
        <p class="prose">${escapeHtml(content.abilities)}</p>
      </section>
    `
    : ''

  const unitNo = content.unitNo != null
    ? `<span class="unit-no">#${escapeHtml(content.unitNo)}</span>`
    : ''

  const entryMeta = content.entryMeta
    ? `<p class="entry-meta">${escapeHtml(content.entryMeta)}</p>`
    : ''

  const body = content.missingMessage
    ? `<p class="missing-message">${escapeHtml(content.missingMessage)}</p>`
    : `
      ${content.profileBlocks}
      ${renderWeaponsTable(content.weapons)}
      ${abilities}
      ${keywords}
      ${renderOptions(content.options, content.profileStats, content.selectedOptionIndexes)}
    `

  return `
    <article class="unit-sheet">
      <header class="unit-header">
        <div>
          <span class="unit-type">${escapeHtml(content.unitType)}</span>
          <h3>${escapeHtml(content.unitName)}</h3>
          ${entryMeta}
        </div>
        ${unitNo}
      </header>
      ${body}
    </article>
  `
}

function renderRosterEntrySheet(entry: RosterEntry, unit: Unit | null | undefined): string {
  const entryMeta = `${formatRosterEntryMeta(entry)}${entry.unitType ? ` · ${entry.unitType}` : ''}`

  if (!unit) {
    return renderUnitSheetContent({
      unitType: entry.unitType,
      unitName: entry.unitName,
      entryMeta,
      profileBlocks: '',
      profileStats: null,
      missingMessage: 'Unit datasheet not available.',
    })
  }

  const profileStats = getProfileStatsForEntry(unit, entry)
  const selectedOptionIndexes = entry.selectedOptions.map((option) => option.index)

  return renderUnitSheetContent({
    unitType: entry.unitType,
    unitName: entry.unitName,
    unitNo: unit.no,
    entryMeta,
    profileBlocks: renderStatsTable(profileStats, entry.profileLabel),
    weapons: unit.weapons,
    abilities: unit.abilities,
    keywords: unit.keywords,
    options: unit.options,
    profileStats,
    selectedOptionIndexes,
  })
}

const PRINT_STYLES = `
  :root {
    color-scheme: light;
  }

  * {
    box-sizing: border-box;
  }

  body {
    margin: 0;
    padding: 32px;
    font: 14px/1.5 Georgia, 'Times New Roman', serif;
    color: #111;
    background: #fff;
  }

  .doc-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 24px;
    margin-bottom: 32px;
    padding-bottom: 16px;
    border-bottom: 2px solid #111;
  }

  .doc-header h1 {
    margin: 0 0 8px;
    font-size: 28px;
    line-height: 1.2;
  }

  .doc-eyebrow {
    margin: 0 0 4px;
    font: 12px/1.2 Arial, sans-serif;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #555;
  }

  .doc-meta {
    margin: 0;
    color: #444;
    font-size: 13px;
  }

  .print-btn {
    padding: 10px 16px;
    border: 1px solid #111;
    border-radius: 6px;
    background: #111;
    color: #fff;
    font: 14px Arial, sans-serif;
    cursor: pointer;
  }

  .print-btn:hover {
    background: #333;
  }

  .type-section {
    margin-bottom: 28px;
  }

  .type-section > h2 {
    margin: 0 0 16px;
    padding-bottom: 6px;
    border-bottom: 1px solid #ccc;
    font-size: 20px;
    page-break-after: avoid;
  }

  .unit-sheet {
    margin-bottom: 24px;
    padding-bottom: 20px;
    border-bottom: 1px solid #ddd;
    page-break-inside: avoid;
  }

  .unit-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 16px;
    margin-bottom: 12px;
    page-break-after: avoid;
  }

  .unit-type {
    display: inline-block;
    margin-bottom: 4px;
    font: 11px Arial, sans-serif;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #555;
  }

  .unit-header h3 {
    margin: 0;
    font-size: 18px;
  }

  .unit-no {
    font: 12px Arial, sans-serif;
    color: #666;
    white-space: nowrap;
  }

  section,
  .stats-block {
    margin-bottom: 14px;
  }

  h4 {
    margin: 0 0 8px;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 0.04em;
  }

  .data-table {
    width: 100%;
    border-collapse: collapse;
    font: 12px Arial, sans-serif;
  }

  .data-table th,
  .data-table td {
    padding: 6px 8px;
    border: 1px solid #bbb;
    text-align: center;
    vertical-align: top;
  }

  .data-table th {
    background: #f3f3f3;
    font-weight: 600;
  }

  .data-table td:first-child,
  .data-table th:first-child {
    text-align: left;
  }

  .weapons-table td:last-child,
  .weapons-table th:last-child {
    text-align: left;
  }

  .prose,
  .keywords,
  .options-list {
    margin: 0;
  }

  .options-list {
    padding-left: 20px;
  }

  .options-list li + li {
    margin-top: 6px;
  }

  .option-pts {
    font-weight: 600;
  }

  .entry-meta {
    margin: 4px 0 0;
    font: 12px Arial, sans-serif;
    color: #555;
  }

  .missing-message {
    margin: 0;
    color: #666;
    font-style: italic;
  }

  .card-sheet {
    margin-bottom: 20px;
    padding-bottom: 16px;
    border-bottom: 1px solid #ddd;
    page-break-inside: avoid;
  }

  .card-meta-list {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 8px 16px;
    margin: 0 0 14px;
    font: 12px Arial, sans-serif;
  }

  .card-meta-list div {
    margin: 0;
  }

  .card-meta-list dt {
    margin: 0 0 2px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: #555;
    font-size: 11px;
  }

  .card-meta-list dd {
    margin: 0;
  }

  .content-section {
    margin-bottom: 28px;
  }

  .content-section > h2 {
    margin: 0 0 16px;
    padding-bottom: 6px;
    border-bottom: 1px solid #ccc;
    font-size: 20px;
    page-break-after: avoid;
  }

  @media print {
    body {
      padding: 0;
    }

    .no-print {
      display: none !important;
    }

    .doc-header {
      margin-bottom: 20px;
    }

    .unit-sheet {
      break-inside: avoid;
    }

    .type-section > h2 {
      break-after: avoid;
    }

    .content-section > h2 {
      break-after: avoid;
    }

    .card-sheet {
      break-inside: avoid;
    }
  }
`

function wrapPrintDocument(title: string, headerMeta: string, body: string): string {
  return `<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>${escapeHtml(title)}</title>
    <style>${PRINT_STYLES}</style>
  </head>
  <body>
    <header class="doc-header">
      <div>
        <p class="doc-eyebrow">Warhammer 40,000 · Apocalypse Vanguard</p>
        <h1>${escapeHtml(title)}</h1>
        <p class="doc-meta">${headerMeta}</p>
      </div>
      <button type="button" class="print-btn no-print" onclick="window.print()">Print</button>
    </header>
    ${body}
  </body>
</html>`
}

export function generateFactionPrintHtml(army: ArmyList): string {
  const typeSections = groupUnitsByType(army.units)
    .map(
      ([type, units]) => `
        <section class="type-section">
          <h2>${escapeHtml(type)}</h2>
          ${units.map((unit) => renderUnitSheet(unit)).join('')}
        </section>
      `,
    )
    .join('')

  return wrapPrintDocument(
    `${army.faction} — Army List`,
    `Source: ${escapeHtml(army.source)} · ${army.units.length} units`,
    typeSections,
  )
}

function formatArmyUpdatedAt(iso?: string): string {
  if (!iso) {
    return ''
  }

  try {
    return new Date(iso).toLocaleDateString(undefined, {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    })
  } catch {
    return ''
  }
}

export function generateArmyPrintHtml(
  army: SavedArmy,
  unitsByNo: Map<number, Unit>,
): string {
  const metaParts = [
    `Faction: ${escapeHtml(army.factionName)}`,
    `${army.totalPoints} Pt total`,
  ]

  if (army.roster.length > 0) {
    metaParts.push(`${army.roster.length} units`)
  }

  const updated = formatArmyUpdatedAt(army.updatedAt)
  if (updated) {
    metaParts.push(`Updated ${updated}`)
  }

  const sections: string[] = []

  if (army.roster.length > 0) {
    const rosterSheets = sortRosterByType(army.roster)
      .map((entry) => renderRosterEntrySheet(entry, unitsByNo.get(entry.unitNo)))
      .join('')

    sections.push(`
      <section class="content-section">
        <h2>Army</h2>
        ${rosterSheets}
      </section>
    `)
  }

  return wrapPrintDocument(army.name, metaParts.join(' · '), sections.join(''))
}

export function openPrintableInNewTab(html: string, title: string): void {
  const blob = new Blob([html], { type: 'text/html;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const tab = window.open(url, '_blank', 'noopener,noreferrer')

  if (!tab) {
    URL.revokeObjectURL(url)
    return
  }

  tab.document.title = title
  window.setTimeout(() => URL.revokeObjectURL(url), 60_000)
}
