#!/usr/bin/env python3
"""Generate Rules/ApocalypseVanguardUnits.md from ArmyLists JSON files."""

import json
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ARMY_LISTS_DIR = Path(__file__).resolve().parent
OUTPUT_FILE = REPO_ROOT / "Rules" / "ApocalypseVanguardUnits.md"

TYPE_ORDER = [
    "HQ",
    "Troops",
    "Elites",
    "Fast Attack",
    "Heavy Support",
    "Flyer",
    "Dedicated Transport",
    "Lord of War",
]

TYPE_NORMALIZE = {
    "HQ": "HQ",
    "Troops": "Troops",
    "Elites": "Elites",
    "Elite": "Elites",
    "Fast": "Fast Attack",
    "Heavy": "Heavy Support",
    "Air": "Flyer",
    "air": "Flyer",
    "Transport": "Dedicated Transport",
    "transport": "Dedicated Transport",
    "Lord": "Lord of War",
}


def normalize_type(raw_type: str | None) -> str:
    if not raw_type:
        return "Other"
    return TYPE_NORMALIZE.get(raw_type, raw_type)


def format_profile(stats: dict) -> str:
    points = stats.get("Pt", "—")
    models = stats.get("N", "—")
    return f"{points} Pt · N {models}"


def format_unit_line(unit: dict) -> str:
    name = unit.get("name", "Unknown")
    profile_parts: list[str] = []

    if unit.get("stats"):
        profile_parts.append(format_profile(unit["stats"]))

    for index, profile in enumerate(unit.get("profiles") or [], start=1):
        profile_parts.append(f"Alt {index}: {format_profile(profile)}")

    if len(profile_parts) == 1:
        return f"- **{name}** — {profile_parts[0]}"

    joined = "; ".join(profile_parts)
    return f"- **{name}** — {joined}"


def load_army_lists() -> list[tuple[str, list[dict]]]:
    armies: list[tuple[str, list[dict]]] = []
    for file_path in sorted(ARMY_LISTS_DIR.glob("*.json")):
        data = json.loads(file_path.read_text(encoding="utf-8"))
        faction = data.get("faction") or file_path.stem
        units = data.get("units") or []
        armies.append((faction, units))
    return armies


def build_markdown(armies: list[tuple[str, list[dict]]]) -> str:
    lines = [
        "# Apocalypse Vanguard Units",
        "",
        "Complete unit reference for all army lists. Units are grouped by faction and",
        "battlefield role. Points and model counts (N) are listed for each profile.",
        "",
    ]

    for faction, units in armies:
        by_type: dict[str, list[dict]] = defaultdict(list)
        for unit in units:
            by_type[normalize_type(unit.get("type"))].append(unit)

        lines.append(f"## {faction}")
        lines.append("")

        ordered_types = [t for t in TYPE_ORDER if t in by_type]
        extra_types = sorted(t for t in by_type if t not in TYPE_ORDER)
        for unit_type in ordered_types + extra_types:
            type_units = sorted(by_type[unit_type], key=lambda unit: unit.get("name", "").lower())
            lines.append(f"### {unit_type}")
            lines.append("")
            for unit in type_units:
                lines.append(format_unit_line(unit))
            lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    markdown = build_markdown(load_army_lists())
    OUTPUT_FILE.write_text(markdown, encoding="utf-8")
    print(f"Wrote {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
