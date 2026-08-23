import type { ProfileWeaponSection, Weapon } from '../types'

interface UnitWeaponsProps {
  weapons?: Weapon[]
  profileSections?: ProfileWeaponSection[]
}

function WeaponsTable({ weapons }: { weapons: Weapon[] }) {
  return (
    <div className="table-scroll">
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
    </div>
  )
}

export default function UnitWeapons({ weapons = [], profileSections = [] }: UnitWeaponsProps) {
  if (weapons.length === 0 && profileSections.length === 0) return null

  return (
    <section>
      <h3>Weapons</h3>
      {weapons.length > 0 && <WeaponsTable weapons={weapons} />}
      {profileSections.map((section) => (
        <div key={section.heading} className="profile-extras">
          <h4>{section.heading}</h4>
          <WeaponsTable weapons={section.weapons} />
        </div>
      ))}
    </section>
  )
}
