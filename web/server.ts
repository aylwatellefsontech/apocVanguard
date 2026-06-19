import express from 'express'
import fs from 'fs/promises'
import path from 'path'
import { fileURLToPath } from 'url'
import type { Card, CardFactionCount, CardsResponse, FactionSummary } from './src/types'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const ARMY_LISTS_DIR = path.resolve(__dirname, '../ArmyLists')
const CARDS_DIR = path.resolve(__dirname, '../Cards')
const RULES_FILE = path.resolve(__dirname, '../Rules/Apocalypse Vanguard.md')
const CARD_FILES = [
  'Apoc40kCards - cards.json',
  'Apoc40kCards - cards2.json',
  'Apoc40kCards - cards3.json',
]
const isProd = process.env.NODE_ENV === 'production'

function errorMessage(err: unknown): string {
  return err instanceof Error ? err.message : 'Unknown error'
}

function isENOENT(err: unknown): boolean {
  return (
    typeof err === 'object' &&
    err !== null &&
    'code' in err &&
    (err as NodeJS.ErrnoException).code === 'ENOENT'
  )
}

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

async function loadAllCards(): Promise<CardsResponse> {
  const cardsById = new Map<string, Card>()

  for (const file of CARD_FILES) {
    const filePath = path.join(CARDS_DIR, file)
    const raw = await fs.readFile(filePath, 'utf-8')
    const data = JSON.parse(raw) as { cards?: Array<Record<string, unknown>>; source?: string }

    for (const card of data.cards ?? []) {
      const facRaw = typeof card.fac === 'string' ? card.fac.trim() : ''
      if (!facRaw) {
        continue
      }

      const set = String(card.set ?? '?')
      const nm = Number(card.nm ?? 0)
      const id = `${set}-${nm}-${facRaw}`

      if (cardsById.has(id)) {
        continue
      }

      cardsById.set(id, {
        id,
        set,
        nm,
        fac: facRaw,
        name: String(card.name ?? ''),
        type: String(card.type ?? ''),
        subType: (card.subType as string | null | undefined) ?? null,
        facNm: (card.facNm as number | null | undefined) ?? null,
        ability: typeof card.ability === 'string' ? card.ability : undefined,
        source: data.source,
      })
    }
  }

  const cards = [...cardsById.values()]

  cards.sort((a, b) => {
    const setCompare = String(a.set ?? '').localeCompare(String(b.set ?? ''))
    if (setCompare !== 0) return setCompare
    return (a.nm ?? 0) - (b.nm ?? 0)
  })

  const facCounts = new Map<string, number>()
  for (const card of cards) {
    facCounts.set(card.fac, (facCounts.get(card.fac) ?? 0) + 1)
  }

  const factions: CardFactionCount[] = [...facCounts.entries()]
    .map(([fac, count]) => ({ fac, count }))
    .sort((a, b) => a.fac.localeCompare(b.fac))

  return { cards, factions, total: cards.length }
}

async function createApp() {
  const app = express()

  app.get('/api/factions', async (_req, res) => {
    try {
      const files = await listJsonFiles()
      const factions: FactionSummary[] = await Promise.all(
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
      res.json(factions)
    } catch (err) {
      res.status(500).json({ error: errorMessage(err) })
    }
  })

  app.get('/api/factions/:id', async (req, res) => {
    try {
      const filePath = resolveFactionPath(req.params.id)
      if (!filePath) {
        res.status(400).json({ error: 'Invalid faction id' })
        return
      }
      const raw = await fs.readFile(filePath, 'utf-8')
      res.json(JSON.parse(raw))
    } catch (err) {
      if (isENOENT(err)) {
        res.status(404).json({ error: 'Faction not found' })
        return
      }
      res.status(500).json({ error: errorMessage(err) })
    }
  })

  app.get('/api/cards', async (_req, res) => {
    try {
      res.json(await loadAllCards())
    } catch (err) {
      res.status(500).json({ error: errorMessage(err) })
    }
  })

  app.get('/api/rules', async (_req, res) => {
    try {
      const markdown = await fs.readFile(RULES_FILE, 'utf-8')
      res.json({ markdown })
    } catch (err) {
      if (isENOENT(err)) {
        res.status(404).json({ error: 'Rules file not found' })
        return
      }
      res.status(500).json({ error: errorMessage(err) })
    }
  })

  if (isProd) {
    app.use(express.static(path.join(__dirname, 'dist')))
    app.use((req, res, next) => {
      if (req.method !== 'GET' || req.path.startsWith('/api')) {
        next()
        return
      }
      res.sendFile(path.join(__dirname, 'dist', 'index.html'))
    })
  } else {
    const { createServer } = await import('vite')
    const vite = await createServer({
      server: { middlewareMode: true },
      appType: 'spa',
    })
    app.use(vite.middlewares)
  }

  return app
}

const port = Number(process.env.PORT) || 5173

createApp().then((app) => {
  app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`)
  })
})
