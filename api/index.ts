import type { Express } from 'express'
import { getCards } from './cards'
import { factionsRouter } from './factions'
import { getRules } from './rules'

export function registerDataApi(app: Express): void {
  app.use('/api/factions', factionsRouter)
  app.get('/api/cards', getCards)
  app.get('/api/rules', getRules)
}
