import { useCallback, useEffect, useState } from 'react'

const MOBILE_PANEL_KEY = '__vanguardMobilePanel'

export type MobilePanelHistoryEntry<T extends string> = {
  scope: string
  panel: T
  data?: Record<string, unknown>
}

type HistoryState = Record<string, unknown> & {
  [MOBILE_PANEL_KEY]?: MobilePanelHistoryEntry<string>
}

export function readMobilePanelFromState<T extends string>(
  scope: string,
  state: HistoryState | null | undefined,
): MobilePanelHistoryEntry<T> | null {
  const entry = state?.[MOBILE_PANEL_KEY]
  if (entry?.scope === scope) {
    return entry as MobilePanelHistoryEntry<T>
  }
  return null
}

export function mergeMobilePanelHistoryState<T extends string>(
  scope: string,
  panel: T,
  data: Record<string, unknown> | undefined,
  currentState: HistoryState | null | undefined,
): HistoryState {
  return {
    ...(currentState ?? {}),
    [MOBILE_PANEL_KEY]: { scope, panel, data },
  }
}

function getMobilePanelFromHistory<T extends string>(
  scope: string,
): MobilePanelHistoryEntry<T> | null {
  return readMobilePanelFromState(scope, window.history.state as HistoryState | null)
}

function mergeHistoryState<T extends string>(
  scope: string,
  panel: T,
  data?: Record<string, unknown>,
): HistoryState {
  return mergeMobilePanelHistoryState(
    scope,
    panel,
    data,
    window.history.state as HistoryState | null,
  )
}

export { MOBILE_PANEL_KEY }

export type SetMobilePanelOptions = {
  data?: Record<string, unknown>
  /** push (default), replace current entry, or skip history update */
  history?: 'push' | 'replace' | 'none'
}

export function useMobilePanelHistory<T extends string>(
  scope: string,
  isMobile: boolean,
  initialPanel: T,
) {
  const [panel, setPanelState] = useState<T>(initialPanel)
  const [panelData, setPanelData] = useState<Record<string, unknown> | undefined>()

  useEffect(() => {
    if (!isMobile) {
      return
    }

    const existing = getMobilePanelFromHistory<T>(scope)
    if (existing) {
      setPanelState(existing.panel)
      setPanelData(existing.data)
    }
  }, [isMobile, scope])

  useEffect(() => {
    if (!isMobile) {
      return
    }

    function handlePopState() {
      const entry = getMobilePanelFromHistory<T>(scope)
      if (entry) {
        setPanelState(entry.panel)
        setPanelData(entry.data)
        return
      }

      setPanelState(initialPanel)
      setPanelData(undefined)
    }

    window.addEventListener('popstate', handlePopState)
    return () => window.removeEventListener('popstate', handlePopState)
  }, [isMobile, scope, initialPanel])

  const setPanel = useCallback(
    (next: T, options?: SetMobilePanelOptions) => {
      const { data, history: historyMode = 'push' } = options ?? {}
      setPanelState(next)
      setPanelData(data)

      if (!isMobile || historyMode === 'none') {
        return
      }

      const merged = mergeHistoryState(scope, next, data)
      if (historyMode === 'replace') {
        window.history.replaceState(merged, '')
      } else {
        window.history.pushState(merged, '')
      }
    },
    [isMobile, scope],
  )

  const goBack = useCallback(() => {
    if (isMobile) {
      window.history.back()
    }
  }, [isMobile])

  return { panel, setPanel, goBack, panelData }
}
