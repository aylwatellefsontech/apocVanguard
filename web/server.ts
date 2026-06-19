import express from 'express'
import path from 'path'
import { fileURLToPath } from 'url'
import { registerDataApi } from '../api/index'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const isProd = process.env.NODE_ENV === 'production'

async function createApp() {
  const app = express()

  registerDataApi(app)

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
