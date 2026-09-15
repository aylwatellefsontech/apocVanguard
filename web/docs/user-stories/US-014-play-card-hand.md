# US-014 Deal and play a command-card hand

**As a** player mid-game  
**I want to** draw, play, and discard the command cards on my saved army  
**So that** I can track my strategic assets without a physical deck

## Acceptance criteria

- Card Hand is available on a saved army that has cards.
- The hand has Deck, Hand, and Discard piles, with counts.
- I can draw from the deck, discard from hand, pull from discard, pin cards to the top of the deck, and reshuffle discard into the deck.
- I can undo a small number of recent hand actions.
- Hand state is stored per army and survives a reload.
- I can reset the hand after a confirm.
