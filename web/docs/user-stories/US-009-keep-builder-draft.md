# US-009 Keep an unfinished list if I leave

**As a** player mid-build  
**I want to** come back to the same roster, cards, name, and selections after I refresh or leave the page  
**So that** I do not lose work before I save

## Acceptance criteria

- The builder writes its current state to a draft in `localStorage` as I work.
- Reopening Build Army without an `armyId` restores that draft.
- Opening a saved army for edit uses that army, not an unrelated draft.
- Starting a confirmed new army or successfully saving clears the stale draft when appropriate.
