import { useEffect, useState } from 'react'

export function useCards() {
  const [cards, setCards] = useState([])
  const [factions, setFactions] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

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
        const data = await response.json()
        if (data.error) {
          throw new Error(data.error)
        }
        if (!cancelled) {
          setCards(data.cards ?? [])
          setFactions(data.factions ?? [])
        }
      } catch (err) {
        if (!cancelled) setError(err.message)
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
