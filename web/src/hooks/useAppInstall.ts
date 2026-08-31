import { useCallback, useEffect, useState } from 'react'
import {
  ensureAppInstallCapture,
  getDeferredInstallPrompt,
  INSTALL_FALLBACK_HINT,
  isRunningAsInstalledApp,
  promptAppInstall,
  subscribeInstallPrompt,
  type AppInstallPromptEvent,
} from '../pwa/appInstall'

export function useAppInstall() {
  const [installed, setInstalled] = useState(isRunningAsInstalledApp)
  const [promptEvent, setPromptEvent] = useState<AppInstallPromptEvent | null>(
    getDeferredInstallPrompt,
  )
  const [showHint, setShowHint] = useState(false)

  useEffect(() => {
    ensureAppInstallCapture()
    setInstalled(isRunningAsInstalledApp())
    return subscribeInstallPrompt(setPromptEvent)
  }, [])

  useEffect(() => {
    const onInstalled = () => setInstalled(true)
    window.addEventListener('appinstalled', onInstalled)
    return () => window.removeEventListener('appinstalled', onInstalled)
  }, [])

  const install = useCallback(async () => {
    const outcome = await promptAppInstall(promptEvent)
    if (outcome === 'unavailable') {
      setShowHint(true)
      return
    }
    setShowHint(false)
    if (outcome === 'accepted') {
      setInstalled(true)
    }
  }, [promptEvent])

  return {
    installed,
    showHint,
    hint: INSTALL_FALLBACK_HINT,
    install,
  }
}
