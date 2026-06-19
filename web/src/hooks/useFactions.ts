import { useQuery } from '@tanstack/react-query'
import { fetchArmy, fetchFactions } from '../data/fetchers'
import { queryKeys } from '../queries/keys'

function errorMessage(err: unknown): string {
  return err instanceof Error ? err.message : 'Request failed'
}

export function useFactions() {
  const query = useQuery({
    queryKey: queryKeys.factions,
    queryFn: fetchFactions,
  })

  return {
    factions: query.data ?? [],
    loading: query.isLoading,
    error: query.error ? errorMessage(query.error) : null,
  }
}

export function useArmy(factionId: string | null) {
  const query = useQuery({
    queryKey: queryKeys.army(factionId ?? ''),
    queryFn: () => fetchArmy(factionId!),
    enabled: Boolean(factionId),
  })

  return {
    army: factionId ? (query.data ?? null) : null,
    loading: Boolean(factionId) && query.isLoading,
    error: factionId && query.error ? errorMessage(query.error) : null,
  }
}
