import {
  isRunningAsInstalledApp,
  promptAppInstall,
  INSTALL_FALLBACK_HINT,
  type AppInstallPromptEvent,
} from '../../src/pwa/appInstall'

function matchMediaFor(activeQuery: string | null) {
  return (query: string) => ({ matches: query === activeQuery })
}

describe('isRunningAsInstalledApp', () => {
  it('detects iOS standalone navigator flag', () => {
    expect(isRunningAsInstalledApp({ standalone: true, matchMedia: matchMediaFor(null) })).toBe(
      true,
    )
  })

  it('detects standalone display mode', () => {
    expect(
      isRunningAsInstalledApp({
        standalone: false,
        matchMedia: matchMediaFor('(display-mode: standalone)'),
      }),
    ).toBe(true)
  })

  it('is false in a normal browser tab', () => {
    expect(
      isRunningAsInstalledApp({
        standalone: false,
        matchMedia: matchMediaFor(null),
      }),
    ).toBe(false)
  })
})

describe('promptAppInstall', () => {
  it('returns unavailable when the browser has no install prompt', async () => {
    await expect(promptAppInstall(null)).resolves.toBe('unavailable')
  })

  it('prompts and returns the user choice', async () => {
    let promptCalls = 0
    const event = {
      prompt: async () => {
        promptCalls += 1
      },
      userChoice: Promise.resolve({ outcome: 'accepted', platform: 'web' }),
    } as unknown as AppInstallPromptEvent

    await expect(promptAppInstall(event)).resolves.toBe('accepted')
    expect(promptCalls).toBe(1)
  })
})

describe('INSTALL_FALLBACK_HINT', () => {
  it('tells the user how to install without a native prompt', () => {
    expect(INSTALL_FALLBACK_HINT).toMatch(/Add to Home Screen/i)
  })
})
