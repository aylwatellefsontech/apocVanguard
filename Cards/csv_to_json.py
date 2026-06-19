#!/usr/bin/env python3
"""Convert Apoc40kCards CSV files in this directory to JSON."""

import csv
import json
from pathlib import Path

CARDS_DIR = Path(__file__).resolve().parent

FIELD_MAP = {
    "Set": "set",
    "Nm": "nm",
    "Fac": "fac",
    "Fac Nm": "facNm",
    "Name": "name",
    "Type": "type",
    "SubType": "subType",
    "Cst": "cst",
    "Atk": "atk",
    "Life": "life",
    "Sh": "sh",
    "Abilities1": "ability",
    "Abilities2": "abilities2",
}

INT_FIELDS = {"nm", "facNm", "cst", "atk", "life", "sh"}


def parse_value(key, value):
    value = value.strip()
    if not value:
        return None
    if key in INT_FIELDS:
        try:
            return int(value)
        except ValueError:
            return value
    return value


def row_to_card(row):
    card = {}
    for csv_key, json_key in FIELD_MAP.items():
        parsed = parse_value(json_key, row.get(csv_key, "") or "")
        if parsed is not None:
            card[json_key] = parsed

    if card.get("abilities2") == "remove":
        card["removed"] = True
        del card["abilities2"]
    elif "abilities2" in card:
        del card["abilities2"]

    return card


def csv_to_json(csv_path):
    with open(csv_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    cards = [row_to_card(row) for row in rows if any(v.strip() for v in row.values() if v)]
    return {"source": csv_path.name, "cards": cards}


def main():
    for csv_path in sorted(CARDS_DIR.glob("*.csv")):
        data = csv_to_json(csv_path)
        json_path = csv_path.with_suffix(".json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
        print(f"Wrote {json_path.name} ({len(data['cards'])} cards)")


if __name__ == "__main__":
    main()
