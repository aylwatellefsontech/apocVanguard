import {
  mergeMobilePanelHistoryState,
  MOBILE_PANEL_KEY,
  readMobilePanelFromState,
} from '../../src/hooks/useMobilePanelHistory'

describe('useMobilePanelHistory helpers', () => {
  it('merges mobile panel into existing history state', () => {
    const merged = mergeMobilePanelHistoryState('browse', 'list', { unitNo: 3 }, { router: true })

    expect(merged).toEqual({
      router: true,
      [MOBILE_PANEL_KEY]: { scope: 'browse', panel: 'list', data: { unitNo: 3 } },
    })
  })

  it('reads mobile panel for matching scope', () => {
    const state = {
      [MOBILE_PANEL_KEY]: { scope: 'browse', panel: 'detail', data: { unitNo: 5 } },
    }

    expect(readMobilePanelFromState('browse', state)).toEqual({
      scope: 'browse',
      panel: 'detail',
      data: { unitNo: 5 },
    })
    expect(readMobilePanelFromState('build', state)).toBeNull()
  })
})
