import adeptusCustodesIcon from '../assets/factions/adeptus-custodes.svg?raw'
import adeptusMechanicusIcon from '../assets/factions/adeptus-mechanicus.svg?raw'
import apocIcon from '../assets/factions/apoc.svg?raw'
import chaosMarinesIcon from '../assets/factions/chaos-marines.svg?raw'
import drukhariIcon from '../assets/factions/drukhari.svg?raw'
import eldarIcon from '../assets/factions/eldar.svg?raw'
import genestealerCultsIcon from '../assets/factions/genestealer-cults.svg?raw'
import harlequinsIcon from '../assets/factions/harlequins.svg?raw'
import imperialGuardIcon from '../assets/factions/imperial-guard.svg?raw'
import knightsIcon from '../assets/factions/knights.svg?raw'
import necronsIcon from '../assets/factions/necrons.svg?raw'
import orksIcon from '../assets/factions/orks.svg?raw'
import sistersOfBattleIcon from '../assets/factions/sisters-of-battle.svg?raw'
import spaceMarinesIcon from '../assets/factions/space-marines.svg?raw'
import tauIcon from '../assets/factions/tau.svg?raw'
import tyranidsIcon from '../assets/factions/tyranids.svg?raw'

const FACTION_ICONS: Record<string, string> = {
  'Adeptus Custodes': adeptusCustodesIcon,
  'Adeptus Mechanicus': adeptusMechanicusIcon,
  Apoc: apocIcon,
  Chaos: chaosMarinesIcon,
  'Chaos Marines': chaosMarinesIcon,
  Drukhari: drukhariIcon,
  Eldar: eldarIcon,
  'Genestealer Cults': genestealerCultsIcon,
  Harlequins: harlequinsIcon,
  'Imperial Guard': imperialGuardIcon,
  'Imperial Knights': knightsIcon,
  Knights: knightsIcon,
  Necrons: necronsIcon,
  Orks: orksIcon,
  'Sisters of Battle': sistersOfBattleIcon,
  'Space Marines': spaceMarinesIcon,
  Tau: tauIcon,
  'Traitor Knights': knightsIcon,
  Tyranids: tyranidsIcon,
}

export function getFactionIconMarkup(name: string): string | null {
  return FACTION_ICONS[name] ?? null
}

export function hasFactionIcon(name: string): boolean {
  return Boolean(FACTION_ICONS[name])
}
