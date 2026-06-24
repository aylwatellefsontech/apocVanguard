#!/usr/bin/env python3
"""Reduce Pt by 2 for Air units with Supersonic but not Harrier."""

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


def is_supersonic_only(row) -> bool:
    abilities = row.get("Abilities", "")
    if "Supersonic" not in abilities:
        return False
    if "Harrier" in abilities:
        return False
    return True


def apply_rows(rows):
    updated = []
    for row in rows:
        unit_type = norm_type(row.get("Type", ""))
        if unit_type not in UNIT_TYPES:
            continue
        if not is_supersonic_only(row):
            continue
        pt = row.get("Pt", "").strip()
        if not pt.isdigit():
            continue
        new_pt = int(pt) - 2
        set_stats(row, Pt=str(new_pt))
        updated.append(f"{row.get('Name', '').strip()} ({pt} -> {new_pt})")
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
