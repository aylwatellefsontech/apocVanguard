import fs from 'fs/promises'
import path from 'path'
import type { Request, Response } from 'express'
import { mergeCardFiles, type CardFileData } from '../web/src/data/mergeCards'
import type { CardsResponse } from '../web/src/types'
import { errorMessage } from './errors'
import { CARD_FILES, CARDS_DIR } from './paths'

export async function loadAllCards(): Promise<CardsResponse> {
  const sources: CardFileData[] = []

  for (const file of CARD_FILES) {
    const filePath = path.join(CARDS_DIR, file)
    const raw = await fs.readFile(filePath, 'utf-8')
    sources.push(JSON.parse(raw) as CardFileData)
  }

  return mergeCardFiles(sources)
}

export async function getCards(_req: Request, res: Response): Promise<void> {
  try {
    res.json(await loadAllCards())
  } catch (err) {
    res.status(500).json({ error: errorMessage(err) })
  }
}
