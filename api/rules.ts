import fs from 'fs/promises'
import type { Request, Response } from 'express'
import { errorMessage, isENOENT } from './errors'
import { RULES_FILE } from './paths'

export async function loadRules(): Promise<string> {
  return fs.readFile(RULES_FILE, 'utf-8')
}

export async function getRules(_req: Request, res: Response): Promise<void> {
  try {
    res.json({ markdown: await loadRules() })
  } catch (err) {
    if (isENOENT(err)) {
      res.status(404).json({ error: 'Rules file not found' })
      return
    }
    res.status(500).json({ error: errorMessage(err) })
  }
}
