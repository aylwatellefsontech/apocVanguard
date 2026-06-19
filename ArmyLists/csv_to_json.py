#!/usr/bin/env python3
"""Convert Apoc40k-Armies-1st CSV army lists to JSON."""

import csv
import json
import re
from pathlib import Path

ARMY_LISTS_DIR = Path(__file__).resolve().parent

STAT_FIELDS = ["M", "WS", "BS", "A", "W", "Ld", "Sv", "N", "Pt"]
CANONICAL_TYPES = {
    "hq": "HQ",
    "troops": "Troops",
    "elites": "Elites",
    "elite": "Elites",
    "fast": "Fast",
    "heavy": "Heavy",
    "lord": "Lord",
    "transport": "Transport",
    "air": "Air",
}
UNIT_TYPES = set(CANONICAL_TYPES.values())

FIELDNAMES = [
    "No", "Type", "Name",
    "M", "WS", "BS", "A", "W", "Ld", "Sv", "N", "Pt",
    "Weapon", "WeaponType", "Rng", "WeaponA", "SAP", "SAT", "Abilities",
    "Keywords",
]

WEAPON_SAT = re.compile(r"^(-|\d+\+|[A-Za-z ]{1,20})$")


def norm_type(value):
    return CANONICAL_TYPES.get(value.strip().lower(), value.strip())


def parse_keywords(text):
    if not text or not text.strip():
        return []
    result = []
    for line in text.strip().split("\n"):
        for part in line.split(","):
            part = part.strip()
            if part:
                result.append(part)
    return result


def get_stats(row):
    stats = {}
    for field in STAT_FIELDS:
        value = row.get(field, "").strip()
        if value:
            stats[field] = value
    return stats or None


def get_weapon(row):
    if not row.get("Weapon", "").strip():
        return None

    weapon = {
        "name": row["Weapon"].strip(),
        "type": row.get("WeaponType", "").strip() or None,
        "range": row.get("Rng", "").strip() or None,
        "attacks": row.get("WeaponA", "").strip() or None,
        "skill": row.get("SAP", "").strip() or None,
        "armorPen": row.get("SAT", "").strip() or None,
    }
    abilities = row.get("Abilities", "").strip()
    if abilities and abilities != "-":
        weapon["abilities"] = abilities
    return {key: value for key, value in weapon.items() if value is not None}


def get_option_text(row):
    abilities = row.get("Abilities", "").strip()
    if abilities:
        return abilities

    sat = row.get("SAT", "").strip()
    if sat and not WEAPON_SAT.match(sat):
        return sat
    return None


def is_empty_row(row):
    return not any(value.strip() for value in row.values() if value)


def is_unit_header(row):
    return norm_type(row.get("Type", "")) in UNIT_TYPES


def clean(obj):
    if isinstance(obj, dict):
        return {
            key: clean(value)
            for key, value in obj.items()
            if value is not None and value != [] and value != {}
        }
    if isinstance(obj, list):
        return [clean(item) for item in obj]
    return obj


def faction_from_csv_path(csv_path):
    name = csv_path.name
    prefix = "Apoc40k-Armies-1st - "
    if name.startswith(prefix) and name.endswith(".csv"):
        return name[len(prefix):-4]
    return csv_path.stem


def csv_to_json(csv_path):
    units = []
    current = None

    with open(csv_path, newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        next(reader, None)
        next(reader, None)

        for raw_row in reader:
            while len(raw_row) < len(FIELDNAMES):
                raw_row.append("")
            row = dict(zip(FIELDNAMES, raw_row))

            if is_empty_row(row):
                continue

            if is_unit_header(row):
                if current:
                    units.append(current)

                current = {
                    "no": int(row["No"].strip()),
                    "type": norm_type(row["Type"]),
                    "name": row["Name"].strip(),
                }

                stats = get_stats(row)
                if stats:
                    current["stats"] = stats

                abilities = row["Abilities"].strip()
                if abilities:
                    current["abilities"] = abilities

                keywords = row["Keywords"].strip()
                if keywords:
                    current["keywords"] = parse_keywords(keywords)

                current["profiles"] = []
                current["options"] = []
                current["weapons"] = []

                weapon = get_weapon(row)
                if weapon:
                    current["weapons"].append(weapon)
                continue

            if not current:
                continue

            weapon = get_weapon(row)
            if weapon:
                current["weapons"].append(weapon)
                if row["Keywords"].strip():
                    current.setdefault("keywords", []).extend(parse_keywords(row["Keywords"]))
                continue

            stats = get_stats(row)
            option_text = get_option_text(row)

            if stats:
                profile = stats
                name = row["Name"].strip()
                if name:
                    profile["name"] = name
                current["profiles"].append(profile)
            elif option_text:
                current["options"].append(option_text)
            elif row["Keywords"].strip():
                current.setdefault("keywords", []).extend(parse_keywords(row["Keywords"]))

    if current:
        units.append(current)

    return {
        "faction": faction_from_csv_path(csv_path),
        "source": csv_path.name,
        "units": [clean(unit) for unit in units],
    }


def write_json(csv_path):
    data = csv_to_json(csv_path)
    json_path = csv_path.with_suffix(".json")
    with open(json_path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    return json_path, data


def main():
    csv_files = sorted(ARMY_LISTS_DIR.glob("Apoc40k-Armies-1st - *.csv"))
    for csv_path in csv_files:
        json_path, data = write_json(csv_path)
        print(f"Wrote {json_path.name} ({len(data['units'])} units)")


if __name__ == "__main__":
    main()
