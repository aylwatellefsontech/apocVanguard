import { useEffect, useMemo, useRef, useState } from 'react'
import CardDetail from './CardDetail'
import {
  armyCardToDetail,
  cloneHandState,
  createInitialHand,
  discardFromHand,
  drawCardFromDeck,
  drawCardFromDiscard,
  drawFromDeck,
  loadHandState,
  MAX_HAND_UNDO,
  persistHandState,
  reshuffleDiscardIntoDeck,
} from '../utils/handStorage'
import type { HandPile, HandState, SavedArmy } from '../types'

const RESET_CONFIRM_MS = 2500

interface HandModalProps {
  army: SavedArmy
  onClose: () => void
}

export default function HandModal({ army, onClose }: HandModalProps) {
  const [handState, setHandState] = useState<HandState>(() =>
    loadHandState(army.id, army.cards ?? []),
  )
  const [undoStack, setUndoStack] = useState<HandState[]>([])
  const [activePile, setActivePile] = useState<HandPile>('hand')
  const [resetArmed, setResetArmed] = useState(false)
  const resetTimeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null)

  const cardsById = useMemo(() => {
    const map = new Map<string, (typeof army.cards)[number]>()
    for (const card of army.cards ?? []) {
      map.set(card.id, card)
    }
    return map
  }, [army.cards])

  useEffect(() => {
    persistHandState(army.id, handState)
  }, [army.id, handState])

  useEffect(() => {
    function handleKeyDown(event: KeyboardEvent) {
      if (event.key === 'Escape') {
        onClose()
      }
    }

    document.addEventListener('keydown', handleKeyDown)
    return () => {
      document.removeEventListener('keydown', handleKeyDown)
      if (resetTimeoutRef.current) {
        clearTimeout(resetTimeoutRef.current)
      }
    }
  }, [onClose])

  const activeIds = handState[activePile] ?? []
  const piles: { id: HandPile; label: string; count: number }[] = [
    { id: 'deck', label: 'Deck', count: handState.deck.length },
    { id: 'hand', label: 'Hand', count: handState.hand.length },
    { id: 'discard', label: 'Discard', count: handState.discard.length },
  ]

  function applyAction(updater: (state: HandState) => HandState) {
    setHandState((current) => {
      const next = updater(current)
      if (next === current) {
        return current
      }

      setUndoStack((stack) => [...stack, cloneHandState(current)].slice(-MAX_HAND_UNDO))
      return next
    })
  }

  function handleUndo() {
    setUndoStack((stack) => {
      if (stack.length === 0) {
        return stack
      }

      const previous = stack[stack.length - 1]
      setHandState(previous)
      return stack.slice(0, -1)
    })
  }

  function clearResetArm() {
    if (resetTimeoutRef.current) {
      clearTimeout(resetTimeoutRef.current)
      resetTimeoutRef.current = null
    }
    setResetArmed(false)
  }

  function handleResetClick() {
    if (!resetArmed) {
      setResetArmed(true)
      resetTimeoutRef.current = setTimeout(() => {
        setResetArmed(false)
        resetTimeoutRef.current = null
      }, RESET_CONFIRM_MS)
      return
    }

    clearResetArm()
    applyAction(() => createInitialHand(army.cards ?? []))
    setActivePile('deck')
  }

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div
        className="modal-panel hand-modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="hand-modal-title"
        onClick={(event) => event.stopPropagation()}
      >
        <header className="hand-modal-header">
          <div>
            <h2 id="hand-modal-title">Hand Draw</h2>
            <p className="roster-item-meta">{army.name}</p>
          </div>
          <div className="hand-modal-actions">
            <button
              type="button"
              className="secondary-btn"
              disabled={undoStack.length === 0}
              onClick={handleUndo}
            >
              Undo
            </button>
            <button
              type="button"
              className="secondary-btn"
              disabled={handState.deck.length === 0}
              onClick={() => applyAction((state) => drawFromDeck(state, 1))}
            >
              Draw 1
            </button>
            <button
              type="button"
              className="secondary-btn"
              disabled={handState.deck.length === 0}
              onClick={() => applyAction((state) => drawFromDeck(state, 3))}
            >
              Draw 3
            </button>
            <button
              type="button"
              className="secondary-btn"
              disabled={handState.discard.length === 0}
              onClick={() => applyAction(reshuffleDiscardIntoDeck)}
            >
              Reshuffle Discard
            </button>
            <button
              type="button"
              className={resetArmed ? 'secondary-btn hand-reset-armed' : 'secondary-btn'}
              onClick={handleResetClick}
            >
              {resetArmed ? 'Confirm Reset' : 'Reset'}
            </button>
            <button type="button" className="text-btn" onClick={onClose}>
              Close
            </button>
          </div>
        </header>

        <div className="hand-pile-tabs">
          {piles.map((pile) => (
            <button
              key={pile.id}
              type="button"
              className={activePile === pile.id ? 'hand-pile-tab active' : 'hand-pile-tab'}
              onClick={() => setActivePile(pile.id)}
            >
              {pile.label}
              <span className="hand-pile-count">{pile.count}</span>
            </button>
          ))}
        </div>

        <div className="hand-modal-body">
          {activeIds.length === 0 ? (
            <p className="muted panel-message">No cards in this pile.</p>
          ) : (
            <div className="cards-stack hand-card-list">
              {activeIds.map((entryId) => {
                const entry = cardsById.get(entryId)
                if (!entry) {
                  return null
                }

                return (
                  <div key={entryId} className="hand-card-item">
                    <CardDetail
                      card={armyCardToDetail(entry)}
                      headerAction={
                        activePile === 'hand' ? (
                          <button
                            type="button"
                            className="secondary-btn"
                            onClick={() =>
                              applyAction((state) => discardFromHand(state, entryId))
                            }
                          >
                            Discard
                          </button>
                        ) : (
                          <button
                            type="button"
                            className="primary-btn"
                            onClick={() =>
                              applyAction((state) =>
                                activePile === 'deck'
                                  ? drawCardFromDeck(state, entryId)
                                  : drawCardFromDiscard(state, entryId),
                              )
                            }
                          >
                            Draw
                          </button>
                        )
                      }
                    />
                  </div>
                )
              })}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
