import { Fragment } from 'react'
import type { ProfileWeaponSection, Weapon } from '../types'

interface UnitWeaponsProps {
  weapons?: Weapon[]
  profileSections?: ProfileWeaponSection[]
  embedded?: boolean
}

function formatSkill(weapon: Weapon): string {
  return `${weapon.skill ?? ''}${weapon.armorPen ? ` / ${weapon.armorPen}` : ''}`
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
            <th className="weapon-col-sap">S/AP</th>
            <th className="weapon-col-abilities">Abilities</th>
          </tr>
        </thead>
        <tbody>
          {weapons.map((weapon, index) => (
            <Fragment key={index}>
              <tr className="weapon-main-row">
                <td>{weapon.name}</td>
                <td>{weapon.type}</td>
                <td>{weapon.range}</td>
                <td>{weapon.attacks}</td>
                <td className="weapon-col-sap">{formatSkill(weapon)}</td>
                <td className="weapon-col-abilities">{weapon.abilities || '—'}</td>
              </tr>
              <tr className="weapon-detail-row">
                <td colSpan={4}>
                  <span className="weapon-detail-item">
                    <span className="weapon-detail-label">S/AP</span>
                    {formatSkill(weapon) || '—'}
                  </span>
                  <span className="weapon-detail-item">
                    <span className="weapon-detail-label">Abilities</span>
                    {weapon.abilities || '—'}
                  </span>
                </td>
              </tr>
            </Fragment>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default function UnitWeapons({
  weapons = [],
  profileSections = [],
  embedded = false,
}: UnitWeaponsProps) {
  if (weapons.length === 0 && profileSections.length === 0) return null

  const Wrapper = embedded ? 'div' : 'section'
  const HeadingTag = embedded ? 'h5' : 'h3'

  return (
    <Wrapper className={embedded ? 'profile-details-subsection' : undefined}>
      {!embedded && <HeadingTag>Weapons</HeadingTag>}
      {weapons.length > 0 && (
        embedded ? (
          <>
            <HeadingTag>Weapons</HeadingTag>
            <WeaponsTable weapons={weapons} />
          </>
        ) : (
          <WeaponsTable weapons={weapons} />
        )
      )}
      {profileSections.map((section) => (
        <div key={section.heading} className="profile-extras">
          <h4>{section.heading}</h4>
          <WeaponsTable weapons={section.weapons} />
        </div>
      ))}
    </Wrapper>
  )
}
