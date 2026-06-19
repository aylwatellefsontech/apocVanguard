#!/usr/bin/env python3
"""Regenerate faction CSV/JSON from Apocalypse PDF datasheet data."""

from generate_all_faction_lists import (
    FILE_PREFIX,
    OUTPUT_DIR,
    slot,
    u,
    write_csv,
    write_json,
)
from factions.chaos_marines_data import CHAOS_MARINES, CHAOS_MARINES_SLOTS
from factions.imperial_guard_data import IMPERIAL_GUARD_SLOTS
from factions.space_marines_data import SPACE_MARINES_SLOTS
from factions.knights_data import KNIGHTS_SLOTS

FACTION_OUTPUTS = [
    ("Chaos Marines", "Chaos Marines", CHAOS_MARINES_SLOTS),
    ("Imperial Guard", "Imperial Guard", IMPERIAL_GUARD_SLOTS),
    ("Space Marines", "Space Marines", SPACE_MARINES_SLOTS),
    ("Knights", "Knights", KNIGHTS_SLOTS),
]


def main():
    for faction_name, file_label, slots in FACTION_OUTPUTS:
        basename = f"{FILE_PREFIX}{file_label}"
        csv_path = OUTPUT_DIR / f"{basename}.csv"
        json_path = OUTPUT_DIR / f"{basename}.json"
        write_csv(csv_path, slots)
        write_json(json_path, faction_name, f"{basename}.csv", slots)
        print(f"Wrote {csv_path.name} and {json_path.name} ({len(slots)} units)")


if __name__ == "__main__":
    main()
