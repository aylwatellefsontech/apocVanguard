import { useEffect, useState } from 'react'
import type { ArmyList, FactionSummary } from '../types'

function errorMessage(err: unknown): string {
  return err instanceof Error ? err.message : 'Request failed'
}

export function useFactions() {
  const [factions, setFactions] = useState<FactionSummary[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let cancelled = false

    async function loadFactions() {
      setLoading(true)
      setError(null)
      try {
        const response = await fetch('/api/factions')
        if (!response.ok) throw new Error('Failed to load factions')
        const data = (await response.json()) as FactionSummary[]
        if (!cancelled) setFactions(data)
      } catch (err) {
        if (!cancelled) setError(errorMessage(err))
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

interface ArmyQueryResult {
  factionId: string | null
  army: ArmyList | null
  loading: boolean
  error: string | null
}

export function useArmy(factionId: string | null) {
  const [result, setResult] = useState<ArmyQueryResult>({
    factionId: null,
    army: null,
    loading: false,
    error: null,
  })

  useEffect(() => {
    if (!factionId) return undefined

    const activeFactionId = factionId
    let cancelled = false

    async function loadArmy() {
      setResult((current) => ({
        ...current,
        factionId: activeFactionId,
        loading: true,
        error: null,
      }))
      try {
        const response = await fetch(`/api/factions/${encodeURIComponent(activeFactionId)}`)
        if (!response.ok) throw new Error('Failed to load army list')
        const data = (await response.json()) as ArmyList
        if (!cancelled) {
          setResult({
            factionId: activeFactionId,
            army: data,
            loading: false,
            error: null,
          })
        }
      } catch (err) {
        if (!cancelled) {
          setResult({
            factionId: activeFactionId,
            army: null,
            loading: false,
            error: errorMessage(err),
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
