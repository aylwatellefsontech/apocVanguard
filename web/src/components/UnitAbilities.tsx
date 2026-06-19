interface UnitAbilitiesProps {
  abilities?: string
}

export default function UnitAbilities({ abilities }: UnitAbilitiesProps) {
  if (!abilities) return null

  return (
    <section>
      <h3>Abilities</h3>
      <p className="prose">{abilities}</p>
    </section>
  )
}
