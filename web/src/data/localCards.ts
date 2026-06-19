import cards1 from '../Cards/Apoc40kCards - cards.json'
import cards2 from '../Cards/Apoc40kCards - cards2.json'
import cards3 from '../Cards/Apoc40kCards - cards3.json'
import { mergeCardFiles, type CardFileData } from './mergeCards'

const CARD_FILES: CardFileData[] = [cards1, cards2, cards3]

export function getLocalCards() {
  return mergeCardFiles(CARD_FILES)
}
