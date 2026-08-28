import adeptusCustodesIcon from '../assets/factions/adeptus-custodes.svg?raw'
import adeptusMechanicusIcon from '../assets/factions/adeptus-mechanicus.svg?raw'
import chaosDaemonsIcon from '../assets/factions/chaos-daemons.svg?raw'
import chaosIcon from '../assets/factions/chaos.svg?raw'
import chaosMarinesIcon from '../assets/factions/chaos-marines.svg?raw'
import chaosKnightsIcon from '../assets/factions/chaos-knights.svg?raw'
import drukhariIcon from '../assets/factions/drukhari.svg?raw'
import eldarIcon from '../assets/factions/eldar.svg?raw'
import genestealerCultsIcon from '../assets/factions/genestealer-cults.svg?raw'
import harlequinsIcon from '../assets/factions/harlequins.svg?raw'
import imperialAgentsIcon from '../assets/factions/imperial-agents.svg?raw'
import imperialGuardIcon from '../assets/factions/imperial-guard.svg?raw'
import imperialKnightsIcon from '../assets/factions/imperial-knights.svg?raw'
import knightsIcon from '../assets/factions/knights.svg?raw'
import marineChaptersIcon from '../assets/factions/marine-chapters.svg?raw'
import necronsIcon from '../assets/factions/necrons.svg?raw'
import orksIcon from '../assets/factions/orks.svg?raw'
import sistersOfBattleIcon from '../assets/factions/sisters-of-battle.svg?raw'
import spaceMarinesIcon from '../assets/factions/space-marines.svg?raw'
import squatsIcon from '../assets/factions/squats.svg?raw'
import tauIcon from '../assets/factions/tau.svg?raw'
import traitorKnightsIcon from '../assets/factions/traitor-knights.svg?raw'
import tyranidsIcon from '../assets/factions/tyranids.svg?raw'
import vanguardIcon from '../assets/factions/vanguard.svg?raw'
import { normalizeFactionIconSvg } from './normalizeFactionIconSvg'

const RAW_FACTION_ICONS: Record<string, string> = {
  'Adeptus Custodes': adeptusCustodesIcon,
  'Adeptus Mechanicus': adeptusMechanicusIcon,
  Apoc: vanguardIcon,
  Chaos: chaosIcon,
  'Chaos Daemons': chaosDaemonsIcon,
  'Chaos Knights': chaosKnightsIcon,
  'Chaos Marines': chaosMarinesIcon,
  Drukhari: drukhariIcon,
  Eldar: eldarIcon,
  'Genestealer Cults': genestealerCultsIcon,
  Harlequins: harlequinsIcon,
  'Imperial Agents': imperialAgentsIcon,
  'Imperial Guard': imperialGuardIcon,
  'Imperial Knights': imperialKnightsIcon,
  Knights: knightsIcon,
  'Marine Chapters': marineChaptersIcon,
  Necrons: necronsIcon,
  Orks: orksIcon,
  'Sisters of Battle': sistersOfBattleIcon,
  'Space Marines': spaceMarinesIcon,
  Squats: squatsIcon,
  Tau: tauIcon,
  'Traitor Knights': traitorKnightsIcon,
  Tyranids: tyranidsIcon,
}

const FACTION_ICONS = Object.fromEntries(
  Object.entries(RAW_FACTION_ICONS).map(([name, svg]) => [name, normalizeFactionIconSvg(svg)]),
) as Record<string, string>

export function getFactionIconMarkup(name: string): string | null {
  return FACTION_ICONS[name] ?? null
}

export function hasFactionIcon(name: string): boolean {
  return Boolean(FACTION_ICONS[name])
}
