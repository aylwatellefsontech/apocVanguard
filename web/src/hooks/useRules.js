import { useEffect, useState } from 'react'

export function useRules() {
  const [markdown, setMarkdown] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    let cancelled = false

    async function loadRules() {
      setLoading(true)
      setError(null)
      try {
        const response = await fetch('/api/rules')
        const contentType = response.headers.get('content-type') ?? ''
        if (!response.ok) {
          throw new Error('Failed to load rules')
        }
        if (!contentType.includes('application/json')) {
          throw new Error(
            'Rules API returned an invalid response. Restart with npm run dev from the web folder.',
          )
        }
        const data = await response.json()
        if (data.error) {
          throw new Error(data.error)
        }
        if (!cancelled) {
          setMarkdown(data.markdown ?? '')
        }
      } catch (err) {
        if (!cancelled) setError(err.message)
      } finally {
        if (!cancelled) setLoading(false)
      }
    }

    loadRules()
    return () => {
      cancelled = true
    }
  }, [])

  return { markdown, loading, error }
}
