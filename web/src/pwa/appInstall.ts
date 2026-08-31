export const INSTALL_FALLBACK_HINT =
  'Use your browser menu to choose Install app or Add to Home Screen.'

export type AppInstallPromptEvent = Event & {
  prompt: () => Promise<void>
  userChoice: Promise<{ outcome: 'accepted' | 'dismissed'; platform: string }>
}

export type InstalledAppEnvironment = {
  matchMedia?: (query: string) => Pick<MediaQueryList, 'matches'>
  standalone?: boolean
}

export type AppInstallOutcome = 'accepted' | 'dismissed' | 'unavailable'

const DISPLAY_MODES = ['standalone', 'fullscreen', 'window-controls-overlay'] as const

let captureStarted = false
let deferredPrompt: AppInstallPromptEvent | null = null
const promptListeners = new Set<(event: AppInstallPromptEvent | null) => void>()

function notifyPromptListeners() {
  for (const listener of promptListeners) {
    listener(deferredPrompt)
  }
}

function onBeforeInstallPrompt(event: Event) {
  event.preventDefault()
  deferredPrompt = event as AppInstallPromptEvent
  notifyPromptListeners()
}

function onAppInstalled() {
  deferredPrompt = null
  notifyPromptListeners()
}

export function isRunningAsInstalledApp(env: InstalledAppEnvironment = {}): boolean {
  if (env.standalone === true) {
    return true
  }

  if (
    env.standalone === undefined &&
    typeof navigator !== 'undefined' &&
    (navigator as Navigator & { standalone?: boolean }).standalone === true
  ) {
    return true
  }

  const matchMedia =
    env.matchMedia ??
    (typeof window !== 'undefined' ? (query: string) => window.matchMedia(query) : undefined)

  if (!matchMedia) {
    return false
  }

  return DISPLAY_MODES.some((mode) => matchMedia(`(display-mode: ${mode})`).matches)
}

export async function promptAppInstall(
  event: AppInstallPromptEvent | null,
): Promise<AppInstallOutcome> {
  if (!event) {
    return 'unavailable'
  }

  await event.prompt()
  const { outcome } = await event.userChoice
  return outcome
}

export function getDeferredInstallPrompt(): AppInstallPromptEvent | null {
  return deferredPrompt
}

export function subscribeInstallPrompt(
  listener: (event: AppInstallPromptEvent | null) => void,
): () => void {
  promptListeners.add(listener)
  listener(deferredPrompt)
  return () => {
    promptListeners.delete(listener)
  }
}

export function ensureAppInstallCapture(): void {
  if (captureStarted || typeof window === 'undefined') {
    return
  }

  captureStarted = true
  window.addEventListener('beforeinstallprompt', onBeforeInstallPrompt)
  window.addEventListener('appinstalled', onAppInstalled)
}

export function resetAppInstallCaptureForTests(): void {
  captureStarted = false
  deferredPrompt = null
  promptListeners.clear()
}
