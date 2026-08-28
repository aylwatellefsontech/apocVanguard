import hqIcon from '../assets/unitTypes/hq.svg?raw'
import troopsIcon from '../assets/unitTypes/troops.svg?raw'
import elitesIcon from '../assets/unitTypes/elites.svg?raw'
import fastIcon from '../assets/unitTypes/fast.svg?raw'
import heavyIcon from '../assets/unitTypes/heavy.svg?raw'
import transportIcon from '../assets/unitTypes/transport.svg?raw'
import airIcon from '../assets/unitTypes/air.svg?raw'
import lordIcon from '../assets/unitTypes/lord.svg?raw'
import { TYPE_ORDER } from '../constants'
import { normalizeFactionIconSvg } from './normalizeFactionIconSvg'

const RAW_UNIT_TYPE_ICONS: Record<(typeof TYPE_ORDER)[number], string> = {
  HQ: hqIcon,
  Troops: troopsIcon,
  Elites: elitesIcon,
  Fast: fastIcon,
  Heavy: heavyIcon,
  Transport: transportIcon,
  Air: airIcon,
  Lord: lordIcon,
}

const UNIT_TYPE_ICONS = Object.fromEntries(
  Object.entries(RAW_UNIT_TYPE_ICONS).map(([type, svg]) => [type, normalizeFactionIconSvg(svg)]),
) as Record<(typeof TYPE_ORDER)[number], string>

export function getUnitTypeIconMarkup(type: string): string | null {
  return UNIT_TYPE_ICONS[type as (typeof TYPE_ORDER)[number]] ?? null
}

export function hasUnitTypeIcon(type: string): boolean {
  return type in UNIT_TYPE_ICONS
}
