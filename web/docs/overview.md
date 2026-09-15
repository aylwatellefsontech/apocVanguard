# What the web folder does

`web/` is the Apocalypse Vanguard companion app. It is a static front end: no server, no accounts, and no live game engine. Players use it to read the rules, look up datasheets and command cards, build lists, and run a command-card hand during a game.

The game itself is a cleaned-up fan version of Warhammer 40,000 Apocalypse (2019), scaled to Vanguard size — roughly a 3rd-edition 40k list, representing the leading edge of a larger apocalyptic battle. The source rules, army lists, and cards live as markdown and JSON in this repo; the web app packages those files so they can be used in a browser or as an installed Progressive Web App.

## What players can do

- **Home** — see what Vanguard is, jump to the rules, and pick a faction to browse.
- **Browse** — look up faction army lists and unit datasheets, or scan command cards by faction. Print a faction list or a card set.
- **Build Army** — pick units and command cards, choose profiles and options, organize detachments and commanders, then save the list locally. Unfinished work is kept as a draft. Lists can be imported or exported as a compact army code or readable markdown.
- **My Armies** — open saved lists, edit or delete them, print the roster or cards, and deal a command-card hand (deck / hand / discard) for play.
- **Rules** — read the bundled Apocalypse Vanguard rules with a section table of contents.

All saved lists, in-progress drafts, and card hands stay in the browser's `localStorage`. A player can keep up to 8 saved armies.

## What this folder is not

The web app does not host a multiplayer game, sync lists across devices, or enforce army-construction rules beyond what the builder UI already does (points totals, option selections, detachment slots, and the 8-army save cap). Datasheet design guidance lives in [UNITDESIGN.md](./UNITDESIGN.md); the game-content backlog lives in [`../TODO.md`](../TODO.md).
