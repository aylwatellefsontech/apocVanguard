# Web app architecture

The app is a client-only React + TypeScript site built with Vite. It is served under the `/apocVanguard` base path.

## Stack

| Piece | Role |
| --- | --- |
| React 19 | UI |
| Vite 8 | Dev server and static build |
| TanStack Router | Pages and search params (`faction`, `cards`, `armyId`) |
| TanStack Query | Cached reads of bundled factions, army lists, cards, and rules |
| Jest | Unit tests under `web/tests/` |
| `localStorage` | Saved armies, build drafts, and per-army card hands |

There is no backend. `src/data/fetchers.ts` reads bundled JSON and markdown the same way a remote API would, so the UI hooks stay fetch-shaped.

## Routes

Defined in `src/router.tsx`:

| Path | Page | Purpose |
| --- | --- | --- |
| `/` | `HomePage` | Intro, faction grid, PWA install prompt |
| `/browse` | `BrowsePage` | Datasheets (`?faction=`) or command cards (`?cards=`) |
| `/build` | `BuildArmyPage` | List builder; `?armyId=` opens a saved army for edit |
| `/armies` | `ViewArmiesPage` | Saved lists, print, export, card hand |
| `/rules` | `RulesPage` | Rendered rules markdown with a heading nav |

`AppNav` is shared on every page.

## Bundled game data

| Source | Loaded by | Contents |
| --- | --- | --- |
| `src/ArmyLists/*.json` | `localArmyLists.ts` | Faction datasheets (13 factions) |
| `src/Cards/Apoc40kCards - cards*.json` | `localCards.ts` | Command / strategic asset cards, merged across files |
| `src/Rules/Apocalypse Vanguard.md` | `localRules.ts` | Full rules text |

Unit types are shown in a fixed order: HQ, Troops, Elites, Fast, Heavy, Transport, Air, Lord.

## Browser storage

| Key | Module | Data |
| --- | --- | --- |
| `40kvanguard-saved-armies` | `armyStorage.ts` | Up to 8 named lists (roster + cards + points) |
| `40kvanguard-build-army-draft` | `buildArmyDraftStorage.ts` | In-progress builder state so a refresh does not wipe work |
| `40kvanguard-hands` | `handStorage.ts` | Deck / hand / discard per saved army |

Import and export share two formats: a compact `AV1` army code and a readable markdown list. Either can be pasted back into Build Army → Import.

Print helpers open a new tab with printable HTML for a faction list, a saved army, or a command-card sheet.

## Folder layout

```
web/
  src/
    pages/          Route screens
    components/     Shared UI (unit detail, roster, modals, nav)
    hooks/          Data, media query, mobile panel history, PWA install
    data/           Bundled JSON/markdown loaders
    utils/          Roster math, options, export/import, print, hands
    ArmyLists/      Faction datasheet JSON
    Cards/          Command card JSON
    Rules/          Rules markdown
    assets/         Faction and unit-type icons
  tests/            Jest tests colocated by concern
  docs/             This documentation
```

## Mobile

Browse, Build, My Armies, and Rules use a stacked panel layout on small viewports (`useMediaQuery` + `useMobilePanelHistory`). The browser back button steps through panels (factions → list → detail, and so on) instead of leaving the page.

## Install

`src/pwa/appInstall.ts` captures the browser install prompt. Home offers “Install this as a Progressive Web App” when the app is not already running installed.
