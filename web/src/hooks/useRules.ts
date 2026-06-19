import { useQuery } from '@tanstack/react-query'
import { fetchRules } from '../data/fetchers'
import { queryKeys } from '../queries/keys'

function errorMessage(err: unknown): string {
  return err instanceof Error ? err.message : 'Request failed'
}

export function useRules() {
  const query = useQuery({
    queryKey: queryKeys.rules,
    queryFn: fetchRules,
  })

  return {
    markdown: query.data ?? '',
    loading: query.isLoading,
    error: query.error ? errorMessage(query.error) : null,
  }
}
