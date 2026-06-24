#!/usr/bin/env python3
"""Normalize unit Type values and sort CSV army lists by battlefield role."""

import csv
from pathlib import Path

from csv_to_json import (
    FIELDNAMES,
    TYPE_RANK,
    is_empty_row,
    is_unit_header,
    norm_type,
)

ARMY_LISTS_DIR = Path(__file__).resolve().parent

CSV_HEADER = [
    "No", "Type", "Name",
    "M", "WS", "BS", "A", "W", "Ld", "Sv", "N", "Pt",
    "Weapon", "Type", "Rng", "A", "SAP", "SAT", "Abilties", "Keywords", "Options",
]


def read_rows(csv_path):
    with open(csv_path, newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        next(reader, None)
        next(reader, None)
        return [
            dict(zip(FIELDNAMES, raw_row + [""] * (len(FIELDNAMES) - len(raw_row))))
            for raw_row in reader
            if not is_empty_row(dict(zip(FIELDNAMES, raw_row + [""] * (len(FIELDNAMES) - len(raw_row)))))
        ]


def group_units(rows):
    units = []
    current = None
    for row in rows:
        if is_unit_header(row):
            if current:
                units.append(current)
            header = dict(row)
            header["Type"] = norm_type(header["Type"])
            current = [header]
        elif current is not None:
            current.append(row)
    if current:
        units.append(current)
    return units


def unit_sort_key(unit_rows):
    header = unit_rows[0]
    unit_type = norm_type(header["Type"])
    unit_no = int(header["No"].strip()) if header["No"].strip() else 0
    return TYPE_RANK.get(unit_type, len(TYPE_RANK)), unit_no


def sort_csv(csv_path):
    rows = read_rows(csv_path)
    units = sorted(group_units(rows), key=unit_sort_key)
    sorted_rows = [row for unit in units for row in unit]

    with open(csv_path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(CSV_HEADER)
        writer.writerow([""] * len(CSV_HEADER))
        for row in sorted_rows:
            writer.writerow([row.get(col, "") for col in FIELDNAMES])


def main():
    csv_files = sorted(ARMY_LISTS_DIR.glob("Apoc40k-Armies-1st - *.csv"))
    for csv_path in csv_files:
        sort_csv(csv_path)
        print(f"Sorted {csv_path.name}")


if __name__ == "__main__":
    main()
