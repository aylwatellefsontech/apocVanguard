import { useEffect, useState } from 'react'
import type { Card, CardFactionCount } from '../types'

function errorMessage(err: unknown): string {
  return err instanceof Error ? err.message : 'Request failed'
}

export function useCards() {
  const [cards, setCards] = useState<Card[]>([])
  const [factions, setFactions] = useState<CardFactionCount[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let cancelled = false

    async function loadCards() {
      setLoading(true)
      setError(null)
      try {
        const response = await fetch('/api/cards')
        const contentType = response.headers.get('content-type') ?? ''
        if (!response.ok) {
          throw new Error('Failed to load cards')
        }
        if (!contentType.includes('application/json')) {
          throw new Error(
            'Cards API returned an invalid response. Restart with npm run dev from the web folder.',
          )
        }
        const data = (await response.json()) as {
          cards?: Card[]
          factions?: CardFactionCount[]
          error?: string
        }
        if (data.error) {
          throw new Error(data.error)
        }
        if (!cancelled) {
          setCards(data.cards ?? [])
          setFactions(data.factions ?? [])
        }
      } catch (err) {
        if (!cancelled) setError(errorMessage(err))
      } finally {
        if (!cancelled) setLoading(false)
      }
    }

    loadCards()
    return () => {
      cancelled = true
    }
  }, [])

  return { cards, factions, loading, error }
}
