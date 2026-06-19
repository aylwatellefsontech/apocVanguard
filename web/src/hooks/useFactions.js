import { useEffect, useState } from 'react'

export function useFactions() {
  const [factions, setFactions] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    let cancelled = false

    async function loadFactions() {
      setLoading(true)
      setError(null)
      try {
        const response = await fetch('/api/factions')
        if (!response.ok) throw new Error('Failed to load factions')
        const data = await response.json()
        if (!cancelled) setFactions(data)
      } catch (err) {
        if (!cancelled) setError(err.message)
      } finally {
        if (!cancelled) setLoading(false)
      }
    }

    loadFactions()
    return () => {
      cancelled = true
    }
  }, [])

  return { factions, loading, error }
}

export function useArmy(factionId) {
  const [result, setResult] = useState({
    factionId: null,
    army: null,
    loading: false,
    error: null,
  })

  useEffect(() => {
    if (!factionId) return undefined

    let cancelled = false

    async function loadArmy() {
      setResult((current) => ({
        ...current,
        factionId,
        loading: true,
        error: null,
      }))
      try {
        const response = await fetch(
          `/api/factions/${encodeURIComponent(factionId)}`,
        )
        if (!response.ok) throw new Error('Failed to load army list')
        const data = await response.json()
        if (!cancelled) {
          setResult({
            factionId,
            army: data,
            loading: false,
            error: null,
          })
        }
      } catch (err) {
        if (!cancelled) {
          setResult({
            factionId,
            army: null,
            loading: false,
            error: err.message,
          })
        }
      }
    }

    loadArmy()
    return () => {
      cancelled = true
    }
  }, [factionId])

  const isCurrent = result.factionId === factionId

  return {
    army: factionId && isCurrent ? result.army : null,
    loading: factionId ? isCurrent && result.loading : false,
    error: factionId && isCurrent ? result.error : null,
  }
}
