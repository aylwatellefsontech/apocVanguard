import fs from 'fs/promises'
import path from 'path'
import { Router } from 'express'
import type { FactionSummary } from '../web/src/types'
import { errorMessage, isENOENT } from './errors'
import { ARMY_LISTS_DIR } from './paths'

async function listJsonFiles(): Promise<string[]> {
  const entries = await fs.readdir(ARMY_LISTS_DIR)
  return entries.filter((name) => name.endsWith('.json')).sort()
}

function factionIdFromFile(filename: string): string {
  return filename.replace(/\.json$/, '')
}

function resolveFactionPath(id: string): string | null {
  const filePath = path.resolve(ARMY_LISTS_DIR, `${id}.json`)
  if (!filePath.startsWith(`${ARMY_LISTS_DIR}${path.sep}`)) {
    return null
  }
  return filePath
}

export async function loadFactions(): Promise<FactionSummary[]> {
  const files = await listJsonFiles()
  return Promise.all(
    files.map(async (file) => {
      const raw = await fs.readFile(path.join(ARMY_LISTS_DIR, file), 'utf-8')
      const data = JSON.parse(raw) as { faction?: string; source?: string; units?: unknown[] }
      const id = factionIdFromFile(file)
      return {
        id,
        faction: data.faction ?? id,
        source: data.source ?? file,
        unitCount: data.units?.length ?? 0,
      }
    }),
  )
}

export async function loadFactionById(id: string): Promise<unknown> {
  const filePath = resolveFactionPath(id)
  if (!filePath) {
    throw new Error('Invalid faction id')
  }
  const raw = await fs.readFile(filePath, 'utf-8')
  return JSON.parse(raw)
}

export const factionsRouter = Router()

factionsRouter.get('/', async (_req, res) => {
  try {
    res.json(await loadFactions())
  } catch (err) {
    res.status(500).json({ error: errorMessage(err) })
  }
})

factionsRouter.get('/:id', async (req, res) => {
  try {
    res.json(await loadFactionById(req.params.id))
  } catch (err) {
    if (err instanceof Error && err.message === 'Invalid faction id') {
      res.status(400).json({ error: err.message })
      return
    }
    if (isENOENT(err)) {
      res.status(404).json({ error: 'Faction not found' })
      return
    }
    res.status(500).json({ error: errorMessage(err) })
  }
})
