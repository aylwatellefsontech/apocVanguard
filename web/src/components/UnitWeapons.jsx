export default function UnitWeapons({ weapons }) {
  if (!weapons?.length) return null

  return (
    <section>
      <h3>Weapons</h3>
      <table className="data-table weapons-table">
        <thead>
          <tr>
            <th>Weapon</th>
            <th>Type</th>
            <th>Rng</th>
            <th>A</th>
            <th>S/AP</th>
            <th>Abilities</th>
          </tr>
        </thead>
        <tbody>
          {weapons.map((weapon, index) => (
            <tr key={index}>
              <td>{weapon.name}</td>
              <td>{weapon.type}</td>
              <td>{weapon.range}</td>
              <td>{weapon.attacks}</td>
              <td>
                {weapon.skill}
                {weapon.armorPen ? ` / ${weapon.armorPen}` : ''}
              </td>
              <td>{weapon.abilities || '—'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  )
}
