#!/usr/bin/env python3
"""Apply June unit updates: Eldar Phoenix Lords, aircraft, Orks Ghazghkull, etc."""

import re
import shutil
from pathlib import Path

from apply_unit_updates import (
    ARMY_LISTS_DIR,
    FIELDNAMES,
    WEB_ARMY_LISTS_DIR,
    add_ability,
    header_row,
    read_csv,
    set_stats,
    update_weapon,
    write_csv,
)
from csv_to_json import write_json


def blank(no):
    return {col: "" for col in FIELDNAMES} | {"No": str(no)}


def weapon_row(no, name, wtype, rng, attacks, sap, sat, abilities=""):
    row = blank(no)
    row.update({
        "Weapon": name,
        "WeaponType": wtype,
        "Rng": rng,
        "WeaponA": attacks,
        "SAP": sap,
        "SAT": sat,
        "Abilities": abilities,
    })
    return row


def replace_unit_block(rows, no, block):
    rows[:] = [r for r in rows if r["No"].strip() != str(no)]
    insert_at = len(rows)
    for i, r in enumerate(rows):
        if r["No"].strip().isdigit() and int(r["No"].strip()) > int(no):
            insert_at = i
            break
    rows[insert_at:insert_at] = block


def strip_ability(row, fragment):
    if not row:
        return
    text = row.get("Abilities", "")
    text = text.replace(fragment, "")
    text = text.replace(fragment.rstrip("\n"), "")
    text = re.sub(r"\n{2,}", "\n", text).strip()
    row["Abilities"] = text


PHOENIX_ABILITIES = (
    'You can only include one Phoenix Lord in your army.\n'
    'Lord of <Aspect>: <Aspect> units within 6" of this unit and this unit re-roll failed attacks.'
)

PHOENIX_OPTIONS = [
    'Asurmen - equipped with Sword of Asur & Avenger Shuriken catapults. Hand of Asuryan. Improve saving throws of Aspect Warriors within 6" by 1. Lord of <Dire Avengers>.',
    'Baharoth - equipped with Hawks Talon and Shining Blade. Deep strike. Harrier. Brilliant sun. Add 1 to leadership to aspect warriors within 6". Lord of <Swooping Hawks>.',
    'Feugan - equipped with Fire Pike and Fire Axe. Ignore Damage (6+). Assured Destruction. Fire Dragons within 6" of this unit and this unit re-roll wound rolls of 1 against Heavy or Super-heavy units. Lord of <Fire Dragons>.',
    'Karandras - equipped with Lord Weapon and Scorpion\'s Bite. Deep strike. Infiltrators. A thousand stings: for each attack against a Light non-character unit, add 1 A. Lord of <Striking Scorpions>.',
    'Jain Zar - equipped with Lord Ranged Weapon and Blade of Destruction. Terror Troops. Cry of War: enemy units within 2" of this unit subtract 1 from hit rolls with melee weapons. Lord of <Howling Banshees>.',
    'Maugan Ra - equipped with Maugetar. Legacy of Altansar: this unit and Dark Reapers within 6" reroll wound rolls of 1 against Chaos units. Lord of <Dark Reapers>.',
    'Lhykhis - equipped with Lord Weapon and Weaveender. Deep strike. Infiltrators. Perfect Warp Jump: instead of a Move action, this unit can perform a warp jump and set up anywhere more than 9" from enemy units. Whispering Web: Warp Spiders within 6" of this unit gain Perfect Warp Jump and Infiltrators. Lord of <Warp Spiders>.',
]

PHOENIX_WEAPONS = [
    ("Lord Weapon", "Melee", "Melee", "User", "6+", "8+"),
    ("Lord Ranged Weapon", "Small Arms", '12"', "1", "7+", "8+"),
    ("Avenger Shuriken Catapults", "Small Arms", '18"', "User", "7+", "8+"),
    ("Sword of Asur", "Melee", "Melee", "User", "6+", "8+"),
    ("Hawk's Talon", "Small Arms", '24"', "User", "9+", "10+"),
    ("Shining Blade", "Melee", "Melee", "User", "7+", "8+"),
    ("Fire Pike", "Heavy", '6"', "1", "11+", "4+", "Destroyer"),
    ("Fire Axe", "Melee", "Melee", "User", "8+", "4+"),
    ("Blade of Destruction", "Melee", "Melee", "x2", "6+", "8+"),
    ("Scorpion's Bite", "Melee", "Melee", "1", "4+", "10+", "Inferno"),
    ("Maugetar (Melee)", "Melee", "Melee", "1", "7+", "9+"),
    ("Maugetar (Ranged)", "Small Arms", '36"', "User", "6+", "8+", "Inferno"),
    ("Weaveender", "Small Arms", '12"', "User", "6+", "8+"),
]


def apply_eldar(rows):
    update_weapon(rows, 1, "Witchblade", Abilities="Witchfire")
    update_weapon(rows, 5, "Witchblades & Singing Spears", Abilities="Witchfire")

    phoenix_block = [
        {
            **blank(3),
            "Type": "HQ",
            "Name": "Phoenix Lord",
            "M": '7"',
            "WS": "2+",
            "BS": "2+",
            "A": "2",
            "W": "1",
            "Ld": "7",
            "Sv": "4+",
            "N": "1",
            "Pt": "9",
            "Abilities": PHOENIX_ABILITIES,
            "Keywords": "Aeldari, Asuryani, Aspect Warrior\nLight, Infantry, Character, Phoenix Lord",
            "Options": "; ".join(f"per Unit: {opt}" for opt in PHOENIX_OPTIONS),
        },
    ]
    for entry in PHOENIX_WEAPONS:
        ab = entry[6] if len(entry) > 6 else ""
        phoenix_block.append(weapon_row(3, entry[0], entry[1], entry[2], entry[3], entry[4], entry[5], ab))
    replace_unit_block(rows, 3, phoenix_block)

    set_stats(header_row(rows, 4), A="4", W="3", Pt="16")

    h18 = header_row(rows, 18)
    if h18:
        h18["Abilities"] = "Deep Strike\nHarrier"
        h18["Options"] = "per Unit: Deep Strike"
    for r in rows:
        if r["No"].strip() == "18" and "Skyleap" in r.get("Options", ""):
            r["Options"] = "per Unit: Deep Strike"

    return rows


def apply_aircraft_move(rows, no, move, hover_fragment):
    h = header_row(rows, no)
    if not h:
        return
    set_stats(h, M=move)
    strip_ability(h, hover_fragment)
    add_ability(h, "Harrier")


def apply_eldar_aircraft(rows):
    return rows


def apply_imperial_guard_air(rows):
    apply_aircraft_move(
        rows,
        25,
        '14"',
        'Hover Jet: At the start of the Action phase, you can declare that this unit will hover. If it does, then until the end of the phase, its Move characteristic changes to 20" but it loses the Supersonic ability.\n',
    )
    return rows


def apply_space_marines_air(rows):
    apply_aircraft_move(
        rows,
        28,
        '14"',
        'Hover Jet: At the start of the Action phase, you can declare that this unit will hover. If it does, Move becomes 20" but it loses Supersonic.\n',
    )
    return rows


def apply_admech_air(rows):
    for no in (30, 31):
        h = header_row(rows, no)
        if not h:
            continue
        set_stats(h, M='14"')
        strip_ability(h, "Hover")
        add_ability(h, "Harrier")
    return rows


def apply_chaos_air(rows):
    h = header_row(rows, 25)
    if h:
        set_stats(h, M='6"-20"')
    return rows


def apply_orks(rows):
    h = header_row(rows, 1)
    if h:
        h["Name"] = "Gazzghkull Thraka"
        kw = h.get("Keywords", "")
        kw = kw.replace("Light", "Heavy")
        h["Keywords"] = kw
    return rows


def main():
    updates = {
        "Eldar": apply_eldar,
        "Imperial Guard": apply_imperial_guard_air,
        "Space Marines": apply_space_marines_air,
        "Adeptus Mechanicus": apply_admech_air,
        "Chaos Marines": apply_chaos_air,
        "Orks": apply_orks,
    }
    for faction, fn in updates.items():
        path = ARMY_LISTS_DIR / f"Apoc40k-Armies-1st - {faction}.csv"
        rows = read_csv(path)
        fn(rows)
        write_csv(path, rows)
        print(f"Updated {path.name}")

    for csv_path in sorted(ARMY_LISTS_DIR.glob("Apoc40k-Armies-1st - *.csv")):
        write_json(csv_path)
        web_path = WEB_ARMY_LISTS_DIR / csv_path.with_suffix(".json").name
        shutil.copy2(csv_path.with_suffix(".json"), web_path)
        print(f"Wrote {csv_path.with_suffix('.json').name}")


if __name__ == "__main__":
    main()
