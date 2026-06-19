import type { ReactNode } from 'react'

export type AppPage = 'browse' | 'build' | 'armies' | 'rules'

export type BrowseMode = 'army' | 'cards'

export type ViewMode = 'army' | 'cards' | 'all'

export type HandPile = 'deck' | 'hand' | 'discard'

export type UnitStats = {
  M?: string
  WS?: string
  BS?: string
  A?: string
  W?: string
  Ld?: string
  Sv?: string
  N?: string
  Pt?: string
  [key: string]: string | undefined
}

export interface Weapon {
  name?: string
  type?: string
  range?: string
  attacks?: string
  skill?: string
  armorPen?: string
  abilities?: string
}

export interface UnitOptionObject {
  per?: string
  text?: string
  name?: string
  Pt?: string | number
  pt?: string | number
}

export type UnitOption = string | UnitOptionObject

export interface Unit {
  no: number
  type: string
  name: string
  stats?: UnitStats
  profiles?: UnitStats[]
  abilities?: string
  keywords?: string[]
  options?: UnitOption[]
  weapons?: Weapon[]
}

export interface FactionSummary {
  id: string
  faction: string
  source: string
  unitCount: number
}

export interface ArmyList {
  faction: string
  source: string
  units: Unit[]
}

export interface Card {
  id: string
  set: string
  nm: number
  fac: string
  name: string
  type: string
  subType?: string | null
  facNm?: number | null
  ability?: string
  source?: string
}

export interface CardFactionCount {
  fac: string
  count: number
}

export interface CardsResponse {
  cards: Card[]
  factions: CardFactionCount[]
  total: number
}

export interface SelectedOption {
  index: number
  label?: string | null
  text?: string
  points: number
}

export interface RosterEntry {
  id: string
  unitNo: number
  unitName: string
  unitType: string
  profileKind: 'primary' | 'alt'
  profileIndex: number
  profileLabel: string
  profilePoints: number
  modelCount?: string | number | null
  selectedOptions: SelectedOption[]
  points: number
}

export interface ArmyCardEntry {
  id: string
  cardId: string
  name: string
  set: string
  nm: number
  fac: string
  type: string
  subType?: string | null
  facNm?: number | null
  ability: string
}

export interface SavedArmy {
  id: string
  name: string
  factionId: string
  factionName: string
  totalPoints: number
  updatedAt?: string
  roster: RosterEntry[]
  cards: ArmyCardEntry[]
}

export interface UnitProfile {
  kind: 'primary' | 'alt'
  index: number
  label: string
  stats: UnitStats
  points: number
}

export interface HandState {
  deck: string[]
  hand: string[]
  discard: string[]
}

export interface RulesHeading {
  level: number
  title: string
  id: string
}

export interface SaveMessage {
  type: 'error' | 'success'
  text: string
}

export interface SaveArmyResult {
  ok: boolean
  error?: string
  armies?: SavedArmy[]
}

export interface OptionSummary {
  label: string | null
  text: string
  points: number
}

export type OptionScope =
  | { type: 'unit' }
  | { type: 'models'; count: number }

export type CardDetailProps = {
  card: Card | null | undefined
  emptyMessage?: string
  headerAction?: ReactNode
}
