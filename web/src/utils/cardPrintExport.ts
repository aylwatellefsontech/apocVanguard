import { openPrintableInNewTab } from './printExport'
import type { ArmyCardEntry, Card } from '../types'

const CARDS_PER_PAGE = 8
const CARD_WIDTH = '2.5in'
const CARD_HEIGHT = '3.5in'

function escapeHtml(value: string | number | null | undefined): string {
  if (value == null || value === '') {
    return ''
  }

  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
}

export function armyCardEntryToCard(entry: ArmyCardEntry): Card {
  return {
    id: entry.cardId,
    set: entry.set,
    nm: entry.nm,
    fac: entry.fac,
    name: entry.name,
    type: entry.type,
    subType: entry.subType,
    facNm: entry.facNm,
    ability: entry.ability,
  }
}

function chunkCards<T>(items: T[], size: number): T[][] {
  const pages: T[][] = []

  for (let index = 0; index < items.length; index += size) {
    pages.push(items.slice(index, index + size))
  }

  return pages
}

function renderPrintCard(card: Card | null): string {
  if (!card) {
    return '<div class="print-card empty" aria-hidden="true"></div>'
  }

  const subType = card.subType ? `<span class="print-card-subtype">${escapeHtml(card.subType)}</span>` : ''
  const facNm = card.facNm != null ? `<span class="print-card-fac-nm">#${escapeHtml(card.facNm)}</span>` : ''

  return `
    <article class="print-card">
      <div class="print-card-frame">
        <header class="print-card-header">
          <div class="print-card-header-left">
            <span class="print-card-type">${escapeHtml(card.type)}</span>
            ${subType}
          </div>
          <span class="print-card-id">${escapeHtml(card.set)}-${escapeHtml(card.nm)}</span>
        </header>
        <div class="print-card-name-block">
          <h2 class="print-card-name">${escapeHtml(card.name)}</h2>
        </div>
        <p class="print-card-faction">${escapeHtml(card.fac)}${facNm ? ` ${facNm}` : ''}</p>
        <p class="print-card-ability">${escapeHtml(card.ability)}</p>
      </div>
    </article>
  `
}

function renderPrintPage(cards: Array<Card | null>): string {
  const slots = [...cards]
  while (slots.length < CARDS_PER_PAGE) {
    slots.push(null)
  }

  return `
    <section class="print-page">
      <div class="card-grid">
        ${slots.map((card) => renderPrintCard(card)).join('')}
      </div>
    </section>
  `
}

const CARD_PRINT_STYLES = `
  :root {
    color-scheme: light;
  }

  * {
    box-sizing: border-box;
  }

  @page {
    size: 11in 8.5in;
    margin: 0;
  }

  body {
    margin: 0;
    background: #ddd;
    font-family: Arial, Helvetica, sans-serif;
  }

  .print-toolbar {
    position: sticky;
    top: 0;
    z-index: 2;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    padding: 12px 16px;
    border-bottom: 1px solid #bbb;
    background: #fff;
  }

  .print-toolbar h1 {
    margin: 0;
    font-size: 16px;
    font-weight: 600;
  }

  .print-toolbar p {
    margin: 4px 0 0;
    font-size: 12px;
    color: #555;
  }

  .print-btn {
    padding: 10px 16px;
    border: 1px solid #111;
    border-radius: 6px;
    background: #111;
    color: #fff;
    font: 14px Arial, sans-serif;
    cursor: pointer;
  }

  .print-btn:hover {
    background: #333;
  }

  .print-page {
    width: 11in;
    height: 8.5in;
    margin: 16px auto;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #fff;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.12);
    page-break-after: always;
  }

  .card-grid {
    display: grid;
    grid-template-columns: repeat(4, ${CARD_WIDTH});
    grid-template-rows: repeat(2, ${CARD_HEIGHT});
  }

  .print-card {
    width: ${CARD_WIDTH};
    height: ${CARD_HEIGHT};
    padding: 0.07in;
    border: 1px dashed #bbb;
    overflow: hidden;
    background: #fff;
  }

  .print-card.empty {
    border-color: transparent;
    background: transparent;
  }

  .print-card-frame {
    height: 100%;
    padding: 0.08in 0.1in 0.1in;
    border: 1.5px solid #111;
    display: flex;
    flex-direction: column;
    background: linear-gradient(180deg, #faf8f4 0%, #fff 18%);
  }

  .print-card-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 0.08in;
    margin-bottom: 0.05in;
    font-size: 6.5pt;
    line-height: 1.2;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  .print-card-header-left {
    display: flex;
    flex-wrap: wrap;
    gap: 0.04in;
    min-width: 0;
  }

  .print-card-type,
  .print-card-subtype {
    color: #333;
    font-weight: 700;
  }

  .print-card-id {
    flex-shrink: 0;
    color: #666;
    font-family: 'Courier New', Courier, monospace;
    font-size: 6pt;
  }

  .print-card-name-block {
    margin: 0 0 0.07in;
    padding: 0.06in 0.05in;
    border-top: 1px solid #111;
    border-bottom: 1px solid #111;
    background: #ece7dc;
    text-align: center;
  }

  .print-card-name {
    margin: 0;
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 10.5pt;
    line-height: 1.1;
    font-weight: 700;
    letter-spacing: 0.03em;
    text-transform: uppercase;
    color: #111;
  }

  .print-card-faction {
    margin: 0 0 0.07in;
    font-size: 6.5pt;
    line-height: 1.2;
    color: #555;
    text-align: center;
    font-style: italic;
  }

  .print-card-fac-nm {
    font-family: 'Courier New', Courier, monospace;
    font-style: normal;
  }

  .print-card-ability {
    margin: 0;
    flex: 1;
    min-height: 0;
    font-size: 6.75pt;
    line-height: 1.28;
    overflow: hidden;
  }

  @media print {
    body {
      background: #fff;
    }

    .no-print {
      display: none !important;
    }

    .print-page {
      margin: 0;
      box-shadow: none;
    }

    .print-card {
      border: 1px solid #000;
    }

    .print-card.empty {
      border: none;
    }

    .print-card-frame {
      background: #fff;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }

    .print-card-name-block {
      background: #ece7dc;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }
  }
`

export function generateCommandCardsPrintHtml(cards: Card[], title: string): string {
  const pages = chunkCards(cards, CARDS_PER_PAGE)
  const pageMarkup = pages.map((pageCards) => renderPrintPage(pageCards)).join('')

  return `<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>${escapeHtml(title)}</title>
    <style>${CARD_PRINT_STYLES}</style>
  </head>
  <body>
    <header class="print-toolbar no-print">
      <div>
        <h1>${escapeHtml(title)}</h1>
        <p>${cards.length} cards · 8 per page · 2.5&Prime; &times; 3.5&Prime; · landscape letter</p>
      </div>
      <button type="button" class="print-btn" onclick="window.print()">Print</button>
    </header>
    ${pageMarkup}
  </body>
</html>`
}

export function openCommandCardsPrint(cards: Card[], title: string): void {
  openPrintableInNewTab(generateCommandCardsPrintHtml(cards, title), title)
}
