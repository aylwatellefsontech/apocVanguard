#!/usr/bin/env python3
"""Add Options column to all army list CSVs from wargear option rows."""

import csv
from pathlib import Path

from army_list_options import format_options_from_texts

ARMY_LISTS_DIR = Path(__file__).resolve().parent
UNIT_TYPES = {
    "hq", "troops", "elites", "elite", "fast", "heavy", "lord", "transport", "air",
}
STAT_FIELDS = {"M", "WS", "BS", "A", "W", "Ld", "Sv", "N", "Pt"}
OPTIONS_COL = "Options"


def is_unit_header(row, header):
    type_idx = header.index("Type")
    return row[type_idx].strip().lower() in UNIT_TYPES


def has_stats(row, header):
    for field in STAT_FIELDS:
        if field in header and row[header.index(field)].strip():
            return True
    return False


def has_weapon(row, header):
    weapon_idx = header.index("Weapon")
    return row[weapon_idx].strip()


def get_cell(row, header, name):
    if name not in header:
        return ""
    idx = header.index(name)
    return row[idx].strip() if idx < len(row) else ""


def set_cell(row, header, name, value):
    if name not in header:
        header.append(name)
        row.append(value)
        return
    idx = header.index(name)
    while len(row) <= idx:
        row.append("")
    row[idx] = value


def pad_row(row, length):
    while len(row) < length:
        row.append("")
    return row[:length]


def process_csv(path):
    with open(path, newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        rows = list(reader)

    if len(rows) < 2:
        return False

    header = rows[0]
    if OPTIONS_COL not in header:
        header = header + [OPTIONS_COL]

    header_len = len(header)
    abilities_col = "Abilties" if "Abilties" in header else "Abilities"
    out_rows = [header, pad_row(rows[1], header_len)]

    i = 2
    while i < len(rows):
        row = pad_row(rows[i], header_len)
        if not any(cell.strip() for cell in row):
            out_rows.append(row)
            i += 1
            continue

        if not is_unit_header(row, header):
            out_rows.append(row)
            i += 1
            continue

        unit_rows = [row]
        i += 1
        while i < len(rows):
            next_row = pad_row(rows[i], header_len)
            if not any(cell.strip() for cell in next_row):
                break
            if is_unit_header(next_row, header):
                break
            unit_rows.append(next_row)
            i += 1

        option_texts = []
        for unit_row in unit_rows:
            if has_weapon(unit_row, header) or (
                has_stats(unit_row, header) and not is_unit_header(unit_row, header)
            ):
                continue
            text = get_cell(unit_row, header, abilities_col)
            if text:
                option_texts.append(text)

        set_cell(unit_rows[0], header, OPTIONS_COL, format_options_from_texts(option_texts))
        out_rows.extend(unit_rows)

    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, quoting=csv.QUOTE_MINIMAL)
        writer.writerows(out_rows)
    return True


def main():
    csv_files = sorted(ARMY_LISTS_DIR.glob("Apoc40k-Armies-1st - *.csv"))
    for path in csv_files:
        process_csv(path)
        print(f"Updated {path.name}")


if __name__ == "__main__":
    main()
