# Apocalypse Vanguard.

This repo is a modified version of the Warhammer Apocalypse (2019) ruleset, cleaned up, with modifications to rules, strategic asset cards, and most importantly datasheets, with the aim to make the game cleaner to play, more balanced, and more true to the universe.

It also is meant to play at 'Vanguard' scale, which instead of playing at double the size of a normal army, aims to be roughly in line with 40k lists from 3rd edition - representing the vanguards of a much larger apocalyptic battle clashing.

The main data files are markdown, under:
 ArmyLists/Apoc40k-Armies-1st - *.md - Army lists for each faction.
 Cards/Apoc40kCards -cards*.md - List of Command Asset cards.
 Rules/Apocalypse Vanguard.md - Rule set for Apocalypse Vanguard.

This project also contains a web app, used to look at the rules, build lists, and select cards.

It is built using React, Vite, as a front end app, with support scripts run using py.

The app was generated using vibe coding with cursor, so no promises, but it should not run with any security related features, (just static assets, with lists in local Storage) so it should not be a big problem.  But again, no promises.

# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/)

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.
