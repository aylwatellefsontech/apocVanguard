import express from 'express'
import fs from 'fs/promises'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const ARMY_LISTS_DIR = path.resolve(__dirname, '../ArmyLists')
const isProd = process.env.NODE_ENV === 'production'

async function listJsonFiles() {
  const entries = await fs.readdir(ARMY_LISTS_DIR)
  return entries.filter((name) => name.endsWith('.json')).sort()
}

function factionIdFromFile(filename) {
  return filename.replace(/\.json$/, '')
}

function resolveFactionPath(id) {
  const filePath = path.resolve(ARMY_LISTS_DIR, `${id}.json`)
  if (!filePath.startsWith(`${ARMY_LISTS_DIR}${path.sep}`)) {
    return null
  }
  return filePath
}

async function createApp() {
  const app = express()

  app.get('/api/factions', async (_req, res) => {
    try {
      const files = await listJsonFiles()
      const factions = await Promise.all(
        files.map(async (file) => {
          const raw = await fs.readFile(path.join(ARMY_LISTS_DIR, file), 'utf-8')
          const data = JSON.parse(raw)
          const id = factionIdFromFile(file)
          return {
            id,
            faction: data.faction,
            source: data.source,
            unitCount: data.units?.length ?? 0,
          }
        }),
      )
      res.json(factions)
    } catch (err) {
      res.status(500).json({ error: err.message })
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
      if (err.code === 'ENOENT') {
        res.status(404).json({ error: 'Faction not found' })
        return
      }
      res.status(500).json({ error: err.message })
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
