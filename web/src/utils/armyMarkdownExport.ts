import { STAT_KEYS } from '../constants'
import type { ArmyCardEntry, Card, RosterEntry, Unit, UnitOption, UnitStats, Weapon } from '../types'
import type { ArmyExportSource } from './armyExport'
import { encodeArmyExport } from './armyExport'
import { armyCardEntryToCard } from './cardPrintExport'
import {
  calculateOptionPoints,
  formatOptionBody,
  formatOptionLabel,
} from './formatOption'
import { rosterHasMultipleFactions } from './rosterArmy'
import {
  formatPrintRosterEntryMeta,
  rosterIsOrganized,
  sortRosterForOrganizedArmyView,
} from './rosterOrganize'
import {
  getProfileAbilitySections,
  getProfileKeywordSections,
  getProfileTraitSections,
  getProfileWeaponSections,
  getProfileStatsForEntry,
} from './units'

function escapeMarkdownCell(value: string | number | null | undefined): string {
  if (value == null || value === '') {
    return '—'
  }

  return String(value).replace(/\|/g, '\\|').replace(/\n/g, ' ')
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

function renderMarkdownTable(headers: string[], rows: string[][]): string {
  if (rows.length === 0) {
    return ''
  }

  const headerRow = `| ${headers.join(' | ')} |`
  const divider = `| ${headers.map(() => '---').join(' | ')} |`
  const body = rows.map((row) => `| ${row.join(' | ')} |`).join('\n')

  return `${headerRow}\n${divider}\n${body}`
}

function renderStatsTableMarkdown(stats: UnitStats | null | undefined, label?: string): string {
  if (!stats) {
    return ''
  }

  const headers = [...STAT_KEYS]
  const row = STAT_KEYS.map((key) => escapeMarkdownCell(stats[key]))
  const table = renderMarkdownTable(headers, [row])

  if (!table) {
    return ''
  }

  return label ? `**${label}**\n\n${table}` : table
}

function renderWeaponsTableMarkdown(weapons: Weapon[] | undefined): string {
  if (!weapons?.length) {
    return ''
  }

  const rows = weapons.map((weapon) => {
    const skillAp = weapon.armorPen
      ? `${weapon.skill ?? '—'} / ${weapon.armorPen}`
      : (weapon.skill ?? '—')

    return [
      escapeMarkdownCell(weapon.name),
      escapeMarkdownCell(weapon.type),
      escapeMarkdownCell(weapon.range),
      escapeMarkdownCell(weapon.attacks),
      escapeMarkdownCell(skillAp),
      escapeMarkdownCell(weapon.abilities),
    ]
  })

  return renderMarkdownTable(['Weapon', 'Type', 'Rng', 'A', 'S/AP', 'Abilities'], rows)
}

function renderOptionsMarkdown(
  options: UnitOption[] | undefined,
  profileStats: UnitStats | null,
  selectedOptionIndexes?: number[],
): string {
  if (!options?.length) {
    return ''
  }

  const indexes =
    selectedOptionIndexes != null ? selectedOptionIndexes : options.map((_, index) => index)

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
      const pointsSuffix = points > 0 ? ` (+${points} Pt)` : ''

      return `- **${label}:** ${body}${pointsSuffix}`
    })
    .filter(Boolean)

  if (items.length === 0) {
    return ''
  }

  return `#### Options\n\n${items.join('\n')}`
}

function renderRosterEntryMarkdown(
  entry: RosterEntry,
  unit: Unit | null | undefined,
  showFaction: boolean,
): string {
  const meta = formatPrintRosterEntryMeta(entry, showFaction)
  const lines: string[] = [`### ${entry.unitName}`, '', `*${meta}*`]

  if (!unit) {
    lines.push('', '_Unit datasheet not available._')
    return lines.join('\n')
  }

  const profileStats = getProfileStatsForEntry(unit, entry)
  const activeProfile = {
    kind: entry.profileKind,
    index: entry.profileIndex,
    label: entry.profileLabel,
  }
  const selectedOptionIndexes = entry.selectedOptions.map((option) => option.index)

  const statsBlock = renderStatsTableMarkdown(profileStats, entry.profileLabel)
  if (statsBlock) {
    lines.push('', statsBlock)
  }

  const weapons = renderWeaponsTableMarkdown(unit.weapons)
  const profileWeaponSections = getProfileWeaponSections(unit, activeProfile)
  if (weapons || profileWeaponSections.length > 0) {
    lines.push('', '#### Weapons')
    if (weapons) {
      lines.push('', weapons)
    }
    for (const section of profileWeaponSections) {
      lines.push('', `**${section.heading}**`, '')
      lines.push(renderWeaponsTableMarkdown(section.weapons))
    }
  }

  const profileAbilitySections = getProfileAbilitySections(unit, activeProfile)
  if (unit.abilities || profileAbilitySections.length > 0) {
    lines.push('', '#### Abilities')
    if (unit.abilities) {
      lines.push('', unit.abilities)
    }
    for (const section of profileAbilitySections) {
      lines.push('', `**${section.heading}**`, '', section.text)
    }
  }

  const keywordSections = getProfileKeywordSections(unit, activeProfile)
  if (unit.keywords?.length || keywordSections.length > 0) {
    lines.push('', '#### Keywords')
    if (unit.keywords?.length) {
      lines.push('', unit.keywords.join(', '))
    }
    for (const section of keywordSections) {
      lines.push('', `**${section.heading}:** ${section.items.join(', ')}`)
    }
  }

  const traitSections = getProfileTraitSections(unit, activeProfile)
  if (unit.traits?.length || traitSections.length > 0) {
    lines.push('', '#### Traits')
    if (unit.traits?.length) {
      lines.push('', unit.traits.join(', '))
    }
    for (const section of traitSections) {
      lines.push('', `**${section.heading}:** ${section.items.join(', ')}`)
    }
  }

  const optionsBlock = renderOptionsMarkdown(
    unit.options,
    profileStats,
    selectedOptionIndexes,
  )
  if (optionsBlock) {
    lines.push('', optionsBlock)
  }

  return lines.join('\n')
}

function renderCardMarkdown(card: Card): string {
  const metaParts = [card.type]
  if (card.subType) {
    metaParts.push(card.subType)
  }
  metaParts.push(card.fac)
  metaParts.push(`${card.set}-${card.nm}`)
  if (card.facNm != null) {
    metaParts.push(`#${card.facNm}`)
  }

  return [`### ${card.name}`, '', `*${metaParts.join(' · ')}*`, '', card.ability ?? ''].join('\n')
}

export function generateArmyListMarkdown(
  army: ArmyExportSource,
  unitsByEntryId: Map<string, Unit> = new Map(),
  exportCode?: string,
  exportedAt: Date = new Date(),
): string {
  const armyCode = exportCode ?? encodeArmyExport(army, exportedAt)
  const metaParts = [
    `Faction: ${army.factionName}`,
    `${army.totalPoints} Pt total`,
  ]

  if (army.roster.length > 0) {
    metaParts.push(`${army.roster.length} units`)
  }

  if (army.cards.length > 0) {
    metaParts.push(`${army.cards.length} cards`)
  }

  const updated = formatArmyUpdatedAt(army.updatedAt ?? exportedAt.toISOString())
  if (updated) {
    metaParts.push(`Updated ${updated}`)
  }

  const sections: string[] = [
    '---',
    'format: apoc-vanguard-army',
    'version: 1',
    `name: "${army.name.replace(/"/g, '\\"')}"`,
    `factionId: ${army.factionId}`,
    `factionName: ${army.factionName}`,
    `exportedAt: ${exportedAt.toISOString()}`,
    '---',
    '',
    `# ${army.name}`,
    '',
    '_Warhammer 40,000 · Apocalypse Vanguard_',
    '',
    metaParts.join(' · '),
  ]

  if (army.roster.length > 0) {
    const showFaction = rosterHasMultipleFactions(army.roster)
    const roster = rosterIsOrganized(army.roster)
      ? sortRosterForOrganizedArmyView(army.roster)
      : army.roster

    sections.push('', '## Army', '')
    sections.push(
      roster
        .map((entry: RosterEntry) => renderRosterEntryMarkdown(entry, unitsByEntryId.get(entry.id), showFaction))
        .join('\n\n'),
    )
  }

  if (army.cards.length > 0) {
    sections.push('', '## Command Cards', '')
    sections.push(
      army.cards
        .map((entry: ArmyCardEntry) => renderCardMarkdown(armyCardEntryToCard(entry)))
        .join('\n\n'),
    )
  }

  sections.push('', '## Army Export Code', '', '```', armyCode, '```')

  return sections.join('\n')
}
