# US-011 Share a list as a code or markdown

**As a** player  
**I want to** export an army and import it on another device or later  
**So that** I can share lists without a backend

## Acceptance criteria

- Export offers a compact army code (`AV1…`) and a readable markdown list.
- I can copy either format to the clipboard.
- Import accepts either format and saves the result as a new army (subject to the 8-army cap).
- Import reports a clear error if the text is invalid or the save cap is reached.
- Exported organization, options, and cards come back on import.
