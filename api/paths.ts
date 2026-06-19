import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

export const ARMY_LISTS_DIR = path.resolve(__dirname, '../ArmyLists')
export const CARDS_DIR = path.resolve(__dirname, '../Cards')
export const RULES_FILE = path.resolve(__dirname, '../Rules/Apocalypse Vanguard.md')

export const CARD_FILES = [
  'Apoc40kCards - cards.json',
  'Apoc40kCards - cards2.json',
  'Apoc40kCards - cards3.json',
] as const
