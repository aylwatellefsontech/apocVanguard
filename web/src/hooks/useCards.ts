import { useQuery } from '@tanstack/react-query'
import { fetchCards } from '../data/fetchers'
import { queryKeys } from '../queries/keys'

function errorMessage(err: unknown): string {
  return err instanceof Error ? err.message : 'Request failed'
}

export function useCards() {
  const query = useQuery({
    queryKey: queryKeys.cards,
    queryFn: fetchCards,
  })

  return {
    cards: query.data?.cards ?? [],
    factions: query.data?.factions ?? [],
    loading: query.isLoading,
    error: query.error ? errorMessage(query.error) : null,
  }
}
