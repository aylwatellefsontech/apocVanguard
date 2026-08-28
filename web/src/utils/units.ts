import { TYPE_ORDER } from '../constants'
import type {
  ActiveProfileSelection,
  ProfileAbilitySection,
  ProfileTagSection,
  ProfileWeaponSection,
  RosterEntry,
  Unit,
  UnitProfile,
  UnitProfileRecord,
  UnitStats,
} from '../types'

const STAT_FIELDS = ['name', 'M', 'WS', 'BS', 'A', 'W', 'Ld', 'Sv', 'N', 'Pt'] as const

export function parsePoints(stats: UnitStats | undefined): number {
  const value = Number.parseInt(stats?.Pt ?? '', 10)
  return Number.isFinite(value) ? value : 0
}

export function getAltProfileLabel(profile: UnitStats, index: number): string {
  const name = profile.name?.trim()
  return name || `Alt Profile ${index + 1}`
}

export function getProfileDisplayName(profile: UnitProfile): string {
  const name = profile.stats.name?.trim()
  return name || profile.label
}

export function getProfileAnchorId(profile: UnitProfile): string {
  return `profile-detail-${profile.kind}-${profile.index}`
}

export function profileHasExtras(profile: UnitProfile): boolean {
  return Boolean(
    profile.abilities?.trim() ||
      profile.keywords?.length ||
      profile.traits?.length ||
      profile.weapons?.length,
  )
}

export function getProfilesForDetailsSection(unit: Unit | null | undefined): UnitProfile[] {
  const profiles = getUnitProfiles(unit)
  return profiles.length > 1 ? profiles : profiles.filter((profile) => profileHasExtras(profile))
}

export function scrollToProfileDetail(profile: UnitProfile): void {
  document.getElementById(getProfileAnchorId(profile))?.scrollIntoView({
    behavior: 'smooth',
    block: 'start',
  })
}

export function getBlendedKeywords(unit: Unit | null | undefined, profile: UnitProfile | null): string[] {
  const tags = [...(unit?.keywords ?? [])]
  for (const tag of profile?.keywords ?? []) {
    if (!tags.includes(tag)) {
      tags.push(tag)
    }
  }
  return tags
}

export function getBlendedTraits(unit: Unit | null | undefined, profile: UnitProfile | null): string[] {
  const tags = [...(unit?.traits ?? [])]
  for (const tag of profile?.traits ?? []) {
    if (!tags.includes(tag)) {
      tags.push(tag)
    }
  }
  return tags
}

export function getBlendedAbilities(
  unit: Unit | null | undefined,
  profile: UnitProfile | null,
): string | undefined {
  const parts = [unit?.abilities?.trim(), profile?.abilities?.trim()].filter(Boolean)
  return parts.length > 0 ? parts.join('\n\n') : undefined
}

export function getBlendedWeapons(unit: Unit | null | undefined, profile: UnitProfile | null) {
  const weapons = [...(unit?.weapons ?? [])]
  const seen = new Set(weapons.map((weapon) => weapon.name).filter(Boolean))

  for (const weapon of profile?.weapons ?? []) {
    if (weapon.name && seen.has(weapon.name)) {
      continue
    }
    weapons.push(weapon)
    if (weapon.name) {
      seen.add(weapon.name)
    }
  }

  return weapons
}

export function isProfileActive(
  profile: UnitProfile,
  active: ActiveProfileSelection | null | undefined,
): boolean {
  if (!active) {
    return false
  }

  if (profile.kind === active.kind && profile.index === active.index) {
    return true
  }

  if (active.label && profile.label === active.label) {
    return true
  }

  if (
    active.kind === 'primary' &&
    active.index === 0 &&
    active.label === 'Primary Profile' &&
    profile.kind === 'primary'
  ) {
    return true
  }

  return false
}

export function resolveActiveProfile(
  profiles: UnitProfile[],
  active: ActiveProfileSelection | null | undefined,
): UnitProfile | null {
  if (!active) {
    return null
  }

  return profiles.find((profile) => isProfileActive(profile, active)) ?? null
}

function toUnitStats(record: UnitStats): UnitStats {
  const stats: UnitStats = {}
  for (const field of STAT_FIELDS) {
    const value = record[field]
    if (value) {
      stats[field] = value
    }
  }
  return stats
}

function withProfileExtras(
  profile: UnitProfile,
  extras: {
    abilities?: string
    keywords?: string[]
    traits?: string[]
    weapons?: UnitProfile['weapons']
  },
): UnitProfile {
  if (extras.abilities?.trim()) {
    profile.abilities = extras.abilities.trim()
  }
  if (extras.keywords?.length) {
    profile.keywords = extras.keywords
  }
  if (extras.traits?.length) {
    profile.traits = extras.traits
  }
  if (extras.weapons?.length) {
    profile.weapons = extras.weapons
  }
  return profile
}

export function getUnitProfiles(unit: Unit | null | undefined): UnitProfile[] {
  if (!unit) return []

  const profiles: UnitProfile[] = []

  if (unit.stats) {
    const primaryName = unit.stats.name?.trim()
    profiles.push(
      withProfileExtras(
        {
          kind: 'primary',
          index: 0,
          label: primaryName || 'Primary Profile',
          stats: unit.stats,
          points: parsePoints(unit.stats),
        },
        {
          abilities: unit.profileAbilities,
          keywords: unit.profileKeywords,
          traits: unit.profileTraits,
          weapons: unit.profileWeapons,
        },
      ),
    )
  }

  unit.profiles?.forEach((record: UnitProfileRecord, index) => {
    profiles.push(
      withProfileExtras(
        {
          kind: 'alt',
          index,
          label: getAltProfileLabel(record, index),
          stats: toUnitStats(record),
          points: parsePoints(record),
        },
        {
          abilities: record.abilities,
          keywords: record.keywords,
          traits: record.traits,
          weapons: record.weapons,
        },
      ),
    )
  })

  return profiles
}

export function groupUnitsByType(units: Unit[]): [string, Unit[]][] {
  const groups = new Map<string, Unit[]>()
  for (const unit of units) {
    const list = groups.get(unit.type) ?? []
    list.push(unit)
    groups.set(unit.type, list)
  }

  const orderedTypes = [
    ...TYPE_ORDER.filter((type) => groups.has(type)),
    ...[...groups.keys()].filter((type) => !TYPE_ORDER.includes(type as (typeof TYPE_ORDER)[number])),
  ]

  return orderedTypes.map((type) => [type, groups.get(type)!])
}

export function sortRosterByType(roster: RosterEntry[]): RosterEntry[] {
  const typeRank = new Map(TYPE_ORDER.map((type, index) => [type, index]))

  return [...roster].sort((a, b) => {
    const rankA = typeRank.get(a.unitType as (typeof TYPE_ORDER)[number]) ?? TYPE_ORDER.length
    const rankB = typeRank.get(b.unitType as (typeof TYPE_ORDER)[number]) ?? TYPE_ORDER.length
    if (rankA !== rankB) {
      return rankA - rankB
    }
    return a.unitName.localeCompare(b.unitName)
  })
}

function matchingProfiles(unit: Unit, selected?: ActiveProfileSelection | null): UnitProfile[] {
  const profiles = getUnitProfiles(unit)
  if (!selected) {
    return profiles
  }
  return profiles.filter((profile) => isProfileActive(profile, selected))
}

export function getProfileSectionHeading(profile: UnitProfile, suffix: string): string {
  const prefix = profile.kind === 'primary' ? 'Base Profile' : profile.label
  return `${prefix} ${suffix}`
}

export function getProfileAbilityHeading(profile: UnitProfile): string {
  return getProfileSectionHeading(profile, 'Abilities')
}

export function getProfileAbilitySections(
  unit: Unit | null | undefined,
  selected?: ActiveProfileSelection | null,
): ProfileAbilitySection[] {
  if (!unit) {
    return []
  }

  return matchingProfiles(unit, selected)
    .filter((profile) => Boolean(profile.abilities))
    .map((profile) => ({
      heading: getProfileAbilityHeading(profile),
      text: profile.abilities as string,
    }))
}

export function getProfileKeywordSections(
  unit: Unit | null | undefined,
  selected?: ActiveProfileSelection | null,
): ProfileTagSection[] {
  if (!unit) {
    return []
  }

  return matchingProfiles(unit, selected)
    .filter((profile) => Boolean(profile.keywords?.length))
    .map((profile) => ({
      heading: getProfileSectionHeading(profile, 'Keywords'),
      items: profile.keywords as string[],
    }))
}

export function getProfileTraitSections(
  unit: Unit | null | undefined,
  selected?: ActiveProfileSelection | null,
): ProfileTagSection[] {
  if (!unit) {
    return []
  }

  return matchingProfiles(unit, selected)
    .filter((profile) => Boolean(profile.traits?.length))
    .map((profile) => ({
      heading: getProfileSectionHeading(profile, 'Traits'),
      items: profile.traits as string[],
    }))
}

export function getProfileWeaponSections(
  unit: Unit | null | undefined,
  selected?: ActiveProfileSelection | null,
): ProfileWeaponSection[] {
  if (!unit) {
    return []
  }

  return matchingProfiles(unit, selected)
    .filter((profile) => Boolean(profile.weapons?.length))
    .map((profile) => ({
      heading: getProfileSectionHeading(profile, 'Weapons'),
      weapons: profile.weapons as NonNullable<UnitProfile['weapons']>,
    }))
}

export function getProfileStatsForEntry(
  unit: Unit | null | undefined,
  entry: RosterEntry | null | undefined,
): UnitStats | null {
  if (!unit || !entry) {
    return null
  }

  if (entry.profileKind === 'primary') {
    return unit.stats ?? null
  }

  const record = unit.profiles?.[entry.profileIndex]
  return record ? toUnitStats(record) : null
}

export function isProfileSelected(profile: UnitProfile, entry: RosterEntry | null | undefined): boolean {
  if (!entry) {
    return false
  }

  return profile.kind === entry.profileKind && profile.index === entry.profileIndex
}

export function unitHasInfantryKeyword(unit: Unit | null | undefined): boolean {
  return unit?.keywords?.some((keyword) => keyword.toLowerCase() === 'infantry') ?? false
}

const WEIGHT_KEYWORDS = new Set(['light', 'heavy'])

export function getUnitWeightKeyword(unit: Unit | null | undefined): string | null {
  for (const keyword of unit?.keywords ?? []) {
    if (WEIGHT_KEYWORDS.has(keyword.toLowerCase())) {
      return keyword
    }
  }

  return null
}

export function getRosterEntryWeightKeyword(
  unit: Unit | null | undefined,
  entry: RosterEntry,
): string | null {
  if (!unit) {
    return null
  }

  const profiles = getUnitProfiles(unit)
  const resolved = resolveActiveProfile(profiles, {
    kind: entry.profileKind,
    index: entry.profileIndex,
    label: entry.profileLabel,
  })

  for (const keyword of getBlendedKeywords(unit, resolved)) {
    if (WEIGHT_KEYWORDS.has(keyword.toLowerCase())) {
      return keyword.charAt(0).toUpperCase() + keyword.slice(1).toLowerCase()
    }
  }

  return null
}

export function formatUnitTypeLabel(type: string, unit?: Unit | null): string {
  if (unitHasInfantryKeyword(unit)) {
    return `${type} - Infantry`
  }

  return type
}
