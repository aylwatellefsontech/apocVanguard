#!/usr/bin/env python3
"""Bidirectional Army List JSON ↔ Markdown conversion.

Markdown is the human-editable mirror of ArmyLists JSON. Edit `.md` files and run
`markdown_to_json.py` (or `army_list_md.py to-json`) to refresh JSON and web copies.

Format (consistent across all factions):
  - YAML front matter: faction, source
  - ## Unit {no} — {type} — {name}
  - ### Stats / Keywords / Abilities / Options / Weapons / Profiles
"""

import json
import re
from pathlib import Path

from csv_to_json import clean, faction_from_csv_path, sort_units, STAT_FIELDS, TYPE_ORDER

ARMY_LISTS_DIR = Path(__file__).resolve().parent
WEB_ARMY_LISTS_DIR = ARMY_LISTS_DIR.parent / "web" / "src" / "ArmyLists"

STAT_HEADER = "| " + " | ".join(STAT_FIELDS) + " |"
STAT_SEPARATOR = "| " + " | ".join(["---"] * len(STAT_FIELDS)) + " |"
WEAPON_HEADERS = ["Name", "Type", "Range", "A", "SAP", "SAT", "Abilities"]
WEAPON_HEADER_ROW = "| " + " | ".join(WEAPON_HEADERS) + " |"
WEAPON_SEPARATOR = "| " + " | ".join(["---"] * len(WEAPON_HEADERS)) + " |"


def _parse_profile_header(line: str) -> str | None:
    numbered = PROFILE_NUMBER_HEADER.match(line)
    if numbered:
        explicit_name = numbered.group(2)
        if explicit_name:
            return explicit_name.strip()
        return f"Profile {numbered.group(1)}"

    named = PROFILE_NAME_HEADER.match(line)
    if named:
        return named.group(1).strip()

    return None

UNIT_HEADER = re.compile(r"^## Unit (\d+) — (.+?) — (.+)$")
PROFILE_NUMBER_HEADER = re.compile(r"^#### Profile (\d+)(?: — (.+))?$")
PROFILE_NAME_HEADER = re.compile(r"^#### (?!#)(.+)$")
SECTION_HEADERS = {
    "stats": "### Stats",
    "keywords": "### Keywords",
    "profile_keywords": "### Profile Keywords",
    "traits": "### Traits",
    "profile_traits": "### Profile Traits",
    "abilities": "### Abilities",
    "profile_abilities": "### Profile Abilities",
    "options": "### Options",
    "weapons": "### Weapons",
    "profile_weapons": "### Profile Weapons",
    "profiles": "### Profiles",
}
PROFILE_ABILITIES_HEADER = "##### Profile Abilities"
PROFILE_KEYWORDS_HEADER = "##### Profile Keywords"
PROFILE_TRAITS_HEADER = "##### Profile Traits"
PROFILE_WEAPONS_HEADER = "##### Profile Weapons"
FRONT_MATTER = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
FENCE = re.compile(r"^```\s*\n(.*?)```\s*$", re.DOTALL | re.MULTILINE)


def normalize_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")

def _parse_fenced_text(lines: list[str], index: int) -> tuple[str | None, int]:
    if index >= len(lines) or lines[index].strip() != "```":
        return None, index
    fence_start = index + 1
    fence_end = fence_start
    while fence_end < len(lines) and lines[fence_end].strip() != "```":
        fence_end += 1
    text = "\n".join(lines[fence_start:fence_end]).strip()
    return (text or None), fence_end + 1


def _skip_blank_lines(lines: list[str], index: int) -> int:
    while index < len(lines) and not lines[index].strip():
        index += 1
    return index


def _parse_tag_list(lines: list[str], index: int) -> tuple[list[str] | None, int]:
    index = _skip_blank_lines(lines, index)
    if index >= len(lines):
        return None, index
    line = lines[index].strip()
    if not line or line.startswith("#") or line.startswith("|") or line.startswith("```"):
        return None, index
    tags = [part.strip() for part in line.split(",") if part.strip()]
    return (tags or None), index + 1


def _try_parse_profile_abilities(lines: list[str], index: int) -> tuple[str | None, int]:
    index = _skip_blank_lines(lines, index)
    if index < len(lines) and lines[index].strip() == PROFILE_ABILITIES_HEADER:
        index += 1
        return _parse_fenced_text(lines, index)
    return None, index


def _parse_profile_extras(lines: list[str], index: int) -> tuple[dict, int]:
    extras: dict = {}
    while True:
        index = _skip_blank_lines(lines, index)
        if index >= len(lines):
            break
        line = lines[index].strip()
        if line == PROFILE_KEYWORDS_HEADER:
            index += 1
            tags, index = _parse_tag_list(lines, index)
            if tags:
                extras["keywords"] = tags
            continue
        if line == PROFILE_TRAITS_HEADER:
            index += 1
            tags, index = _parse_tag_list(lines, index)
            if tags:
                extras["traits"] = tags
            continue
        if line == PROFILE_ABILITIES_HEADER:
            index += 1
            abilities, index = _parse_fenced_text(lines, index)
            if abilities:
                extras["abilities"] = abilities
            continue
        if line == PROFILE_WEAPONS_HEADER:
            index += 1
            index = _skip_blank_lines(lines, index)
            weapons, index = _parse_weapons_table(lines, index)
            if weapons:
                extras["weapons"] = weapons
            continue
        break
    return extras, index


def _append_profile_extras(lines: list[str], extras: dict) -> None:
    keywords = extras.get("keywords") or []
    if keywords:
        lines.append(PROFILE_KEYWORDS_HEADER)
        lines.append(", ".join(keywords))
        lines.append("")
    traits = extras.get("traits") or []
    if traits:
        lines.append(PROFILE_TRAITS_HEADER)
        lines.append(", ".join(traits))
        lines.append("")
    abilities = extras.get("abilities")
    if abilities:
        _append_fenced_section(lines, PROFILE_ABILITIES_HEADER, abilities)
    weapons = extras.get("weapons") or []
    if weapons:
        lines.append(PROFILE_WEAPONS_HEADER)
        lines.extend(_weapons_table(weapons))
        lines.append("")


def _append_fenced_section(lines: list[str], heading: str, text: str) -> None:
    lines.append(heading)
    lines.append("```")
    lines.append(normalize_newlines(text))
    lines.append("```")
    lines.append("")



def normalize_text_fields(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, str):
                obj[key] = normalize_newlines(value)
            else:
                normalize_text_fields(value)
    elif isinstance(obj, list):
        for item in obj:
            normalize_text_fields(item)


def _escape_cell(value: str) -> str:
    return value.replace("|", "\\|")


def _unescape_cell(value: str) -> str:
    return value.replace("\\|", "|")


def _stats_table(stats: dict | None) -> list[str]:
    if not stats:
        return []
    row = "| " + " | ".join(_escape_cell(stats.get(field, "") or "") for field in STAT_FIELDS) + " |"
    return [STAT_HEADER, STAT_SEPARATOR, row]


def _parse_stats_table(lines: list[str], start: int) -> tuple[dict | None, int]:
    if start >= len(lines) or not lines[start].startswith("|"):
        return None, start

    header_cells = [c.strip() for c in lines[start].strip().strip("|").split("|")]
    index = start + 1
    if index < len(lines) and re.match(r"^\|[-:\s|]+\|$", lines[index].strip()):
        index += 1

    if index >= len(lines) or not lines[index].startswith("|"):
        return None, index

    data_cells = [_unescape_cell(c.strip()) for c in lines[index].strip().strip("|").split("|")]
    stats = {}
    for field, value in zip(header_cells, data_cells):
        if field in STAT_FIELDS and value:
            stats[field] = value
    return stats or None, index + 1


def _weapons_table(weapons: list[dict]) -> list[str]:
    if not weapons:
        return []
    lines = [WEAPON_HEADER_ROW, WEAPON_SEPARATOR]
    for weapon in weapons:
        cells = [
            _escape_cell(weapon.get("name", "")),
            _escape_cell(weapon.get("type", "") or ""),
            _escape_cell(weapon.get("range", "") or ""),
            _escape_cell(weapon.get("attacks", "") or ""),
            _escape_cell(weapon.get("skill", "") or ""),
            _escape_cell(weapon.get("armorPen", "") or ""),
            _escape_cell(weapon.get("abilities", "") or ""),
        ]
        lines.append("| " + " | ".join(cells) + " |")
    return lines


def _parse_weapons_table(lines: list[str], start: int) -> tuple[list[dict], int]:
    if start >= len(lines) or not lines[start].startswith("| Name"):
        return [], start

    index = start + 2  # skip header and separator
    weapons: list[dict] = []
    while index < len(lines) and lines[index].startswith("|"):
        cells = [_unescape_cell(c.strip()) for c in lines[index].strip().strip("|").split("|")]
        if len(cells) < len(WEAPON_HEADERS):
            index += 1
            continue
        weapon = {
            "name": cells[0],
            "type": cells[1] or None,
            "range": cells[2] or None,
            "attacks": cells[3] or None,
            "skill": cells[4] or None,
            "armorPen": cells[5] or None,
        }
        if cells[6]:
            weapon["abilities"] = cells[6]
        weapons.append({k: v for k, v in weapon.items() if v is not None})
        index += 1
    return weapons, index


def _format_options(options: list) -> list[str]:
    if not options:
        return []
    lines = []
    for option in options:
        if isinstance(option, str):
            lines.append(f"- per: Per Unit")
            lines.append(f"  text: {option}")
            continue
        per = option.get("per", "Per Unit")
        text = option.get("text", "")
        title = option.get("title")
        pt = option.get("Pt") or option.get("pt")
        limit = option.get("limit")
        group = option.get("group")
        choose_one = option.get("chooseOne") or []
        choose_limit = option.get("chooseLimit", 1)
        lines.append(f"- per: {per}")
        if pt is not None and str(pt).strip():
            lines.append(f"  Pt: {pt}")
        if title and str(title).strip():
            lines.append(f"  title: {str(title).strip()}")
        if limit:
            lines.append(f"  limit: {limit}")
        if group:
            lines.append(f"  group: {group}")
        lines.append(f"  text: {text}")
        if choose_one:
            lines.append(f"  Choose {choose_limit}: {'; '.join(choose_one)}")
    return lines


def _parse_options(lines: list[str], start: int) -> tuple[list[dict], int]:
    options: list[dict] = []
    index = start
    while index < len(lines):
        line = lines[index]
        if line.startswith("## ") or line.startswith("### ") or line.startswith("#### "):
            break
        if line.startswith("- per:"):
            per = line.split(":", 1)[1].strip()
            pt = None
            limit = None
            group = None
            text = ""
            title = None
            choose_one: list[str] | None = None
            choose_limit: int | None = None
            index += 1
            while index < len(lines) and lines[index].startswith("  "):
                sub = lines[index].strip()
                if sub.startswith("Pt:"):
                    pt = sub.split(":", 1)[1].strip()
                elif sub.startswith("title:"):
                    title = sub.split(":", 1)[1].strip()
                elif sub.startswith("limit:"):
                    limit = sub.split(":", 1)[1].strip()
                elif sub.startswith("group:"):
                    group = sub.split(":", 1)[1].strip()
                elif sub.startswith("text:"):
                    text = sub.split(":", 1)[1].strip()
                else:
                    choose_match = re.match(
                        r"^(?:choose|take)\s+(one|[1-9]\d*):\s*(.*)$", sub, re.I
                    )
                    if choose_match:
                        choose_limit = (
                            1 if choose_match.group(1).lower() == "one"
                            else int(choose_match.group(1))
                        )
                        choose_one = [
                            part.strip().rstrip(".,").strip()
                            for part in choose_match.group(2).split(";")
                            if part.strip().rstrip(".,").strip()
                        ]
                index += 1
            option = {"per": per, "text": text}
            if pt is not None:
                option["Pt"] = pt
            if title:
                option["title"] = title
            if limit:
                option["limit"] = limit
            if group:
                option["group"] = group.strip()
            if choose_one:
                option["chooseOne"] = choose_one
                option["chooseLimit"] = choose_limit or 1
            options.append(option)
            continue
        if not line.strip():
            index += 1
            continue
        break
    return options, index


def json_to_markdown(data: dict, md_path: Path | None = None) -> str:
    faction = data.get("faction", "Unknown")
    source = data.get("source", "")
    if md_path and source.endswith(".csv"):
        source = md_path.name

    lines = [
        "---",
        f"faction: {faction}",
        f"source: {source}",
        "---",
        "",
        f"# {faction} Army List",
        "",
    ]

    for unit in data.get("units", []):
        lines.append(f"## Unit {unit['no']} — {unit['type']} — {unit['name']}")
        lines.append("")

        stats_lines = _stats_table(unit.get("stats"))
        if stats_lines:
            lines.append("### Stats")
            lines.extend(stats_lines)
            lines.append("")

        keywords = unit.get("keywords") or []
        if keywords:
            lines.append("### Keywords")
            lines.append(", ".join(keywords))
            lines.append("")

        profile_keywords = unit.get("profileKeywords") or []
        if profile_keywords:
            lines.append("### Profile Keywords")
            lines.append(", ".join(profile_keywords))
            lines.append("")

        traits = unit.get("traits") or []
        if traits:
            lines.append("### Traits")
            lines.append(", ".join(traits))
            lines.append("")

        profile_traits = unit.get("profileTraits") or []
        if profile_traits:
            lines.append("### Profile Traits")
            lines.append(", ".join(profile_traits))
            lines.append("")

        abilities = unit.get("abilities")
        if abilities:
            _append_fenced_section(lines, "### Abilities", abilities)

        profile_abilities = unit.get("profileAbilities")
        if profile_abilities:
            _append_fenced_section(lines, "### Profile Abilities", profile_abilities)

        option_lines = _format_options(unit.get("options") or [])
        if option_lines:
            lines.append("### Options")
            lines.extend(option_lines)
            lines.append("")

        weapon_lines = _weapons_table(unit.get("weapons") or [])
        if weapon_lines:
            lines.append("### Weapons")
            lines.extend(weapon_lines)
            lines.append("")

        profile_weapons = unit.get("profileWeapons") or []
        if profile_weapons:
            lines.append("### Profile Weapons")
            lines.extend(_weapons_table(profile_weapons))
            lines.append("")

        profiles = unit.get("profiles") or []
        if profiles:
            lines.append("### Profiles")
            for profile in profiles:
                name = profile.get("name")
                title = name.strip() if isinstance(name, str) and name.strip() else "Profile"
                lines.append(f"#### {title}")
                stat_fields = {k: v for k, v in profile.items() if k in STAT_FIELDS}
                profile_lines = _stats_table(stat_fields)
                if profile_lines:
                    lines.extend(profile_lines)
                lines.append("")
                _append_profile_extras(lines, profile)

    return "\n".join(lines).rstrip() + "\n"


def _parse_front_matter(text: str) -> tuple[dict, str]:
    match = FRONT_MATTER.match(text)
    if not match:
        return {}, text

    meta: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            meta[key.strip()] = value.strip()
    return meta, text[match.end():]


def _parse_unit_block(lines: list[str], start: int) -> tuple[dict | None, int]:
    match = UNIT_HEADER.match(lines[start].strip())
    if not match:
        return None, start + 1

    unit_no = int(match.group(1))
    unit_type = match.group(2).strip()
    unit_name = match.group(3).strip()
    unit: dict = {"no": unit_no, "type": unit_type, "name": unit_name}

    index = start + 1
    while index < len(lines):
        line = lines[index].strip()

        if line.startswith("## Unit "):
            break

        if line == SECTION_HEADERS["stats"]:
            stats, index = _parse_stats_table(lines, index + 1)
            if stats:
                unit["stats"] = stats
            continue

        if line == SECTION_HEADERS["keywords"]:
            index += 1
            tags, index = _parse_tag_list(lines, index)
            if tags:
                unit["keywords"] = tags
            continue

        if line == SECTION_HEADERS["profile_keywords"]:
            index += 1
            tags, index = _parse_tag_list(lines, index)
            if tags:
                unit["profileKeywords"] = tags
            continue

        if line == SECTION_HEADERS["traits"]:
            index += 1
            tags, index = _parse_tag_list(lines, index)
            if tags:
                unit["traits"] = tags
            continue

        if line == SECTION_HEADERS["profile_traits"]:
            index += 1
            tags, index = _parse_tag_list(lines, index)
            if tags:
                unit["profileTraits"] = tags
            continue

        if line == SECTION_HEADERS["abilities"]:
            index += 1
            abilities, index = _parse_fenced_text(lines, index)
            if abilities:
                unit["abilities"] = abilities
            continue

        if line == SECTION_HEADERS["profile_abilities"]:
            index += 1
            profile_abilities, index = _parse_fenced_text(lines, index)
            if profile_abilities:
                unit["profileAbilities"] = profile_abilities
            continue

        if line == SECTION_HEADERS["options"]:
            options, index = _parse_options(lines, index + 1)
            if options:
                unit["options"] = options
            continue

        if line == SECTION_HEADERS["weapons"]:
            weapons, index = _parse_weapons_table(lines, index + 1)
            if weapons:
                unit["weapons"] = weapons
            continue

        if line == SECTION_HEADERS["profile_weapons"]:
            index = _skip_blank_lines(lines, index + 1)
            weapons, index = _parse_weapons_table(lines, index)
            if weapons:
                unit["profileWeapons"] = weapons
            continue

        if line == SECTION_HEADERS["profiles"]:
            index += 1
            profiles: list[dict] = []
            while index < len(lines):
                profile_line = lines[index].strip()
                if profile_line.startswith("## Unit "):
                    break
                profile_name = _parse_profile_header(profile_line)
                if profile_name:
                    profile: dict = {"name": profile_name}
                    stats, next_index = _parse_stats_table(lines, index + 1)
                    if stats:
                        profile.update(stats)
                    extras, next_index = _parse_profile_extras(lines, next_index)
                    profile.update(extras)
                    profiles.append(profile)
                    index = next_index
                    continue
                if profile_line in {
                    PROFILE_ABILITIES_HEADER,
                    PROFILE_KEYWORDS_HEADER,
                    PROFILE_TRAITS_HEADER,
                    PROFILE_WEAPONS_HEADER,
                }:
                    index += 1
                    continue
                if profile_line.startswith("### ") and profile_line != SECTION_HEADERS["profiles"]:
                    break
                index += 1
            if profiles:
                unit["profiles"] = profiles
            continue

        index += 1

    return unit, index


def markdown_to_json(text: str, md_path: Path | None = None) -> dict:
    meta, body = _parse_front_matter(text)
    faction = meta.get("faction", "")
    source = meta.get("source", "")
    if md_path and not source:
        source = md_path.name

    lines = body.splitlines()
    units: list[dict] = []
    index = 0
    while index < len(lines):
        if UNIT_HEADER.match(lines[index].strip()):
            unit, index = _parse_unit_block(lines, index)
            if unit:
                units.append(unit)
        else:
            index += 1

    if not faction and md_path:
        faction = faction_from_csv_path(md_path.with_suffix(".csv"))

    data = clean(
        {
            "faction": faction,
            "source": source,
            "units": sort_units(units),
        }
    )
    normalize_text_fields(data)
    return data


def write_markdown_from_json(json_path: Path, md_path: Path | None = None) -> Path:
    md_path = md_path or json_path.with_suffix(".md")
    data = json.loads(json_path.read_text(encoding="utf-8"))
    normalize_text_fields(data)
    md_path.write_text(json_to_markdown(data, md_path), encoding="utf-8")
    return md_path


def write_json_from_markdown(md_path: Path, json_path: Path | None = None, sync_web: bool = True) -> Path:
    json_path = json_path or md_path.with_suffix(".json")
    text = md_path.read_text(encoding="utf-8")
    data = markdown_to_json(text, md_path)
    with open(json_path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
        handle.write("\n")

    if sync_web and WEB_ARMY_LISTS_DIR.is_dir():
        web_path = WEB_ARMY_LISTS_DIR / json_path.name
        with open(web_path, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2, ensure_ascii=False)
            handle.write("\n")

    return json_path


def round_trip_equal(original: dict, restored: dict) -> bool:
    return json.dumps(original, sort_keys=True) == json.dumps(restored, sort_keys=True)
