# US-010 Save, edit, and delete lists locally

**As a** player  
**I want to** keep a small set of named armies in this browser  
**So that** I can reuse lists without an account or server

## Acceptance criteria

- I can save the current builder army by name to this browser.
- I can keep at most 8 saved armies; a ninth new save is rejected with a clear error.
- Updating an existing saved army does not count as a new slot.
- My Armies and Build Army can open a saved army for editing.
- I can delete a saved army after confirming.
- Saved armies persist across reloads via `localStorage`.
