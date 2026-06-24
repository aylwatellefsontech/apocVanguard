#!/usr/bin/env python3
"""Set Pt to half of pre-reduction value (rounded up) for Supersonic-only Air units."""

import shutil
from pathlib import Path

from apply_unit_updates import (
    ARMY_LISTS_DIR,
    WEB_ARMY_LISTS_DIR,
    norm_type,
    read_csv,
    set_stats,
    write_csv,
)
from csv_to_json import write_json

UNIT_TYPES = {"HQ", "Troops", "Elites", "Fast", "Heavy", "Lord", "Transport", "Air"}

# Pre–Supersonic-adjustment power ratings.
SUPERSONIC_ONLY_ORIGINAL_PT = {
    "Raven Strike Fighter": 10,
    "Razorwing Jetfighter": 10,
    "Voidraven Bomber": 10,
    "Crimson Hunter": 11,
    "Hemlock Wraithfighter": 11,
    "Doom Scythe": 17,
    "Night Scythe": 14,
    "Dakka Jet": 7,
    "Bomba": 8,
    "AX3 Razorshark Strike Fighter": 11,
    "AX39 Sun Shark Bomber": 10,
}


def halve_pt_rounded_up(pt: int) -> int:
    return (pt + 1) // 2


def is_supersonic_only(row) -> bool:
    abilities = row.get("Abilities", "")
    return "Supersonic" in abilities and "Harrier" not in abilities


def apply_rows(rows):
    updated = []
    for row in rows:
        unit_type = norm_type(row.get("Type", ""))
        if unit_type not in UNIT_TYPES:
            continue
        if not is_supersonic_only(row):
            continue
        name = row.get("Name", "").strip()
        original = SUPERSONIC_ONLY_ORIGINAL_PT.get(name)
        if original is None:
            continue
        new_pt = halve_pt_rounded_up(original)
        old_pt = row.get("Pt", "").strip()
        set_stats(row, Pt=str(new_pt))
        updated.append(f"{name} ({old_pt} -> {new_pt}, half of {original} rounded up)")
    return updated


def main():
    for csv_path in sorted(ARMY_LISTS_DIR.glob("Apoc40k-Armies-1st - *.csv")):
        rows = read_csv(csv_path)
        changes = apply_rows(rows)
        if changes:
            write_csv(csv_path, rows)
            print(f"{csv_path.name}:")
            for change in changes:
                print(f"  {change}")

    for csv_path in sorted(ARMY_LISTS_DIR.glob("Apoc40k-Armies-1st - *.csv")):
        write_json(csv_path)
        web_path = WEB_ARMY_LISTS_DIR / csv_path.with_suffix(".json").name
        shutil.copy2(csv_path.with_suffix(".json"), web_path)
        print(f"Synced {csv_path.with_suffix('.json').name}")


if __name__ == "__main__":
    main()
