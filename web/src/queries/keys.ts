export const queryKeys = {
  factions: ['factions'] as const,
  army: (factionId: string) => ['armies', factionId] as const,
  cards: ['cards'] as const,
  rules: ['rules'] as const,
}
