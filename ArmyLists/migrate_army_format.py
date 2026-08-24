#!/usr/bin/env python3
"""Migrate army list JSON/MD to Eldar/Orks/Space Marines format conventions."""

from __future__ import annotations

import argparse
import copy
import json
import re
from pathlib import Path

from army_list_markdown import (
    ARMY_LISTS_DIR,
    WEB_ARMY_LISTS_DIR,
    json_to_markdown,
    markdown_to_json,
    normalize_text_fields,
    write_json_from_markdown,
)

MECHANICAL_KEYWORDS = {
    "Light",
    "Heavy",
    "Super-heavy",
    "Infantry",
    "Character",
    "Vehicle",
    "Aircraft",
    "Transport",
    "Psyker",
    "Monster",
    "Beast",
    "Cavalry",
    "Walker",
    "Terminator",
    "Daemon",
    "Daemon Engine",
    "Tech-Priest",
    "Battlesuit",
    "Synapse Creature",
    "Titanic",
    "Biker",
    "Fly",
    "Jet Pack",
    "Jump Pack",
    "Mega Armour",
    "Veterans",
    "Officer",
    "Questoris Class",
    "Armiger Class",
    "Dominus Class",
    "Cerastus Class",
    "Acastus Class",
}

CHOOSE_ONE_PATTERNS = [
    re.compile(
        r"(?:one of the following|equipped with one of the following|"
        r"must be equipped with one of the following|can have one of the following|"
        r"can also be equipped with one of the following|"
        r"must also be equipped with one of the following|"
        r"equipped with four of the following in any combination|"
        r"equipped with two items from the Commander Weapons list)"
        r"(?:\s*\([^)]*\))?\s*:\s*(.+)$",
        re.IGNORECASE,
    ),
    re.compile(r"^Choose 1:\s*(.+)$", re.IGNORECASE),
]

LOADOUT_ONLY = re.compile(
    r"^(?:This unit |It |A |An )?(?:is |can )?(?:a unit that )?contains \d+ model",
    re.IGNORECASE,
)

MOBILITY_PROFILES = {
    "Jump Pack": {
        "M": '12"',
        "pt_delta": 2,
        "keywords": ["Infantry", "Jump Pack", "Fly"],
        "abilities": "Deep Strike",
    },
    "Jump Packs": {
        "M": '12"',
        "pt_delta": 2,
        "keywords": ["Jump Pack", "Fly"],
        "abilities": "Deep Strike",
        "per_models": True,
    },
    "Terminator Armour": {
        "M": '5"',
        "Sv": "4+",
        "pt_delta": 2,
        "keywords": ["Infantry", "Terminator"],
        "abilities": "Deep Strike",
    },
    "Bike": {
        "M": '14"',
        "pt_delta": 1,
        "keywords": ["Biker"],
        "drop_infantry": True,
    },
    "Wings": {
        "M": '16"',
        "pt_delta": 2,
        "keywords": ["Fly"],
        "abilities": "Deep Strike",
    },
    "Hover Drone": {
        "M": '8"',
        "pt_delta": 0,
        "keywords": ["Jet Pack", "Fly"],
    },
    "Skyrunner Jetbike": {
        "M": '17"',
        "pt_delta": 2,
        "keywords": ["Biker", "Fly"],
    },
    "Mega Armour": {
        "M": '4"',
        "Sv": "4+",
        "pt_delta": 0,
        "keywords": ["Mega Armour"],
    },
}

TITLE_PATTERNS = [
    (re.compile(r"Jump Pack", re.I), "Jump Pack"),
    (re.compile(r"Jump Packs", re.I), "Jump Packs"),
    (re.compile(r"Terminator Armour", re.I), "Terminator Armour"),
    (re.compile(r"\bBike\b", re.I), "Bike"),
    (re.compile(r"\bWings\b", re.I), "Wings"),
    (re.compile(r"Hover Drone", re.I), "Hover Drone"),
    (re.compile(r"Mega Armour", re.I), "Mega Armour"),
    (re.compile(r"Heavy (?:Weapon|Flamer|Stubber)", re.I), "Heavy Weapon"),
    (re.compile(r"Special Weapon", re.I), "Special Weapon"),
    (re.compile(r"Melee Weapon", re.I), "Melee Weapon"),
    (re.compile(r"Main Weapon", re.I), "Main Weapon"),
    (re.compile(r"Primary Weapon", re.I), "Primary Weapon"),
    (re.compile(r"Secondary Weapon", re.I), "Secondary Weapon"),
    (re.compile(r"Turret Weapon", re.I), "Turret Weapon"),
    (re.compile(r"Sponson", re.I), "Sponson Weapons"),
    (re.compile(r"Regimental Standard", re.I), "Regimental Standard"),
    (re.compile(r"Servo-harness", re.I), "Servo-harness"),
    (re.compile(r"Plasma Exterminators", re.I), "Plasma Exterminators"),
    (re.compile(r"Eviscerator", re.I), "Eviscerator"),
    (re.compile(r"Attack Bike", re.I), "Attack Bike"),
    (re.compile(r"Transonic Cannon", re.I), "Transonic Cannon"),
    (re.compile(r"Close Combat Loadout", re.I), "Close Combat Loadout"),
    (re.compile(r"Warpflamers", re.I), "Warpflamers"),
    (re.compile(r"Soulreaper", re.I), "Soulreaper Cannon"),
    (re.compile(r"Blastmaster", re.I), "Blastmaster"),
    (re.compile(r"Siege Shield", re.I), "Siege Shield"),
    (re.compile(r"Ironstorm|Stormspear|Twin Icarus", re.I), "Carapace Weapon"),
    (re.compile(r"Reaper Chainsword|Thunderstrike", re.I), "Melee Weapon"),
    (re.compile(r"Heavy Stubber.*Meltagun|Meltagun", re.I), "Hull Weapon"),
    (re.compile(r"Special Character|only include one", re.I), "Special Character"),
    (re.compile(r"weapons team", re.I), "Weapons Team"),
    (re.compile(r"10 models", re.I), "10 Models"),
]

FILES = [
    "Apoc40k-Armies-1st - Adeptus Mechanicus.md",
    "Apoc40k-Armies-1st - Chaos Marines.md",
    "Apoc40k-Armies-1st - Drukhari.md",
    "Apoc40k-Armies-1st - Genestealer Cults.md",
    "Apoc40k-Armies-1st - Imperial Guard.md",
    "Apoc40k-Armies-1st - Knights.md",
    "Apoc40k-Armies-1st - Necrons.md",
    "Apoc40k-Armies-1st - Sisters of Battle.md",
    "Apoc40k-Armies-1st - Tau.md",
    "Apoc40k-Armies-1st - Tyranids.md",
]


def extract_preamble(text: str) -> str:
    fm_match = re.match(r"^---\s*\n.*?\n---\s*\n", text, re.DOTALL)
    if not fm_match:
        return ""
    rest = text[fm_match.end():]
    unit_match = re.search(r"^## Unit \d+ —", rest, re.MULTILINE)
    if not unit_match:
        return ""
    preamble = rest[: unit_match.start()].strip()
    preamble = re.sub(r"^---\s*\n.*?\n---\s*\n", "", preamble, flags=re.DOTALL).strip()
    lines: list[str] = []
    seen_list_header = False
    for line in preamble.splitlines():
        if re.match(r"^# .+ Army List$", line.strip()):
            if seen_list_header:
                continue
            seen_list_header = True
        lines.append(line)
    return "\n".join(lines).strip()


def split_keywords_traits(unit: dict) -> None:
    keywords = unit.get("keywords") or []
    if unit.get("traits"):
        mechanical = [k for k in keywords if k in MECHANICAL_KEYWORDS]
        unit["keywords"] = mechanical or keywords
        return

    mechanical: list[str] = []
    traits: list[str] = []
    for tag in keywords:
        if tag in MECHANICAL_KEYWORDS:
            mechanical.append(tag)
        else:
            traits.append(tag)

    if mechanical:
        unit["keywords"] = mechanical
    if traits:
        unit["traits"] = traits

    profile_kw = unit.get("profileKeywords") or []
    if not profile_kw and "Infantry" in (unit.get("keywords") or []):
        unit["profileKeywords"] = ["Infantry"]


def infer_title(text: str, option: dict) -> str | None:
    if option.get("title"):
        return option["title"]
    for pattern, title in TITLE_PATTERNS:
        if pattern.search(text):
            return title
    if option.get("group"):
        return option["group"]
    return None


def parse_choose_one(text: str) -> tuple[str, list[str]] | None:
    for pattern in CHOOSE_ONE_PATTERNS:
        match = pattern.search(text.strip())
        if not match:
            continue
        choices_raw = match.group(1)
        choices = [
            part.strip().rstrip(".,").strip()
            for part in re.split(r";", choices_raw)
            if part.strip().rstrip(".,").strip()
        ]
        if not choices:
            continue
        prefix = text[: match.start()].strip().rstrip(".")
        prefix = re.sub(r"\s*\(Power Rating[^)]*\)", "", prefix).strip()
        prefix = prefix.lstrip("•").strip()
        return prefix or "Can be equipped with", choices
    return None


def migrate_option(option: dict) -> dict | None:
    if isinstance(option, str):
        return None
    text = (option.get("text") or "").strip()
    if not text:
        return None

    text = text.lstrip("•").strip()
    option = copy.deepcopy(option)
    option["text"] = text

    if option.get("chooseOne"):
        if len(option.get("text") or "") < 20:
            option["text"] = "Can also be equipped with one of the following"
        if not option.get("title"):
            title = infer_title(text, option)
            if title:
                option["title"] = title
        return option

    parsed = parse_choose_one(text)
    if parsed:
        prefix, choices = parsed
        prefix = re.sub(r"\s*\(Power Rating[^)]*\)", "", prefix).strip()
        prefix = prefix.rstrip(":").strip()
        if prefix.lower().endswith("with"):
            prefix = f"{prefix} one of the following"
        option["text"] = prefix or "Can be equipped with"
        option["chooseOne"] = choices
        option["chooseLimit"] = option.get("chooseLimit") or 1
    else:
        option["text"] = re.sub(r"\s*\(Power Rating[^)]*\)", "", text).strip()

    title = infer_title(text, option)
    if title:
        option["title"] = title

    if LOADOUT_ONLY.match(text) and not option.get("chooseOne"):
        return None

    boilerplate = {
        "this unit can have one of the following",
        "this unit can have one of:",
        "this model can have one of the following",
    }
    if text.lower().rstrip(".:") in boilerplate or text.lower() == "this unit can have one of the following:":
        return None

    return option


def parse_pt(value) -> int:
    if value is None:
        return 0
    match = re.search(r"\+?(\d+)", str(value))
    return int(match.group(1)) if match else 0


STAT_FIELDS = ["M", "WS", "BS", "A", "W", "Ld", "Sv", "N", "Pt"]


def squad_had_jump_packs(unit: dict) -> bool:
    for opt in unit.get("options") or []:
        if not isinstance(opt, dict):
            continue
        title = (opt.get("title") or infer_title(opt.get("text", ""), opt) or "").lower()
        text = (opt.get("text") or "").lower()
        if "jump pack" in title or "jump pack" in text:
            return True
    return False


def jump_profile_variants(unit: dict) -> list[dict]:
    """When Jump Packs option removed from squads, add jump versions of size profiles."""
    base = unit.get("stats") or {}
    profiles = unit.get("profiles") or []
    if not base or not profiles:
        return []

    variants: list[dict] = []
    spec = MOBILITY_PROFILES["Jump Packs"]
    unit_name = unit.get("name", "Models")

    def make_jump(source: dict, label: str) -> dict:
        jump = {"name": label}
        for field in STAT_FIELDS:
            if field in source:
                jump[field] = source[field]
        jump["M"] = spec["M"]
        n = parse_pt(source.get("N")) or 5
        jump["Pt"] = str(parse_pt(source.get("Pt")) + max(2, (n // 5) * 2))
        jump["keywords"] = list(spec["keywords"])
        jump["abilities"] = spec["abilities"]
        return jump

    base_n = str(base.get("N", ""))
    if base_n:
        variants.append(make_jump(base, f"{base_n} Jump {unit_name}"))

    for profile in profiles:
        n = profile.get("N")
        if not n:
            continue
        pname = profile.get("name", "")
        if "jump" in pname.lower():
            continue
        variants.append(make_jump(profile, f"{n} Jump {unit_name}"))

    return variants


def build_mobility_profile(
    unit: dict,
    title: str,
    spec: dict,
    option: dict,
    *,
    per_models: bool = False,
) -> dict:
    base = unit.get("stats") or {}
    profile = {"name": title}
    for field in ("WS", "BS", "A", "W", "Ld", "N"):
        if field in base:
            profile[field] = base[field]

    profile["M"] = spec["M"]
    if "Sv" in spec:
        profile["Sv"] = spec["Sv"]
    else:
        profile["Sv"] = base.get("Sv", "")

    base_pt = parse_pt(base.get("Pt"))
    delta = spec.get("pt_delta", 0)
    if per_models and option.get("per", "").lower().startswith("per 5"):
        delta = parse_pt(option.get("Pt")) or delta
    profile["Pt"] = str(base_pt + delta)
    profile["N"] = base.get("N", "1")

    if spec.get("keywords"):
        profile["keywords"] = list(spec["keywords"])
    if spec.get("abilities"):
        profile["abilities"] = spec["abilities"]
    return profile


def extract_mobility_profiles(unit: dict) -> list[dict]:
    options = unit.get("options") or []
    if not options:
        return []

    profiles: list[dict] = []
    kept: list[dict] = []

    mobility_groups: dict[str, list[dict]] = {}
    for opt in options:
        if not isinstance(opt, dict):
            continue
        group = (opt.get("group") or "").strip()
        title = (opt.get("title") or infer_title(opt.get("text", ""), opt) or "").strip()
        if group.lower() == "mobility" or title in MOBILITY_PROFILES:
            mobility_groups.setdefault(group or "Mobility", []).append(opt)
        else:
            kept.append(opt)

    def consume_mobility(opt: dict) -> None:
        title = (opt.get("title") or infer_title(opt.get("text", ""), opt) or "").strip()
        spec = MOBILITY_PROFILES.get(title)
        if not spec:
            kept.append(opt)
            return
        if title == "Jump Packs" and (unit.get("profiles") or []):
            return
        per = (opt.get("per") or "").lower()
        per_models = spec.get("per_models") or per.startswith("per 5") or per.startswith("per unit")
        profiles.append(
            build_mobility_profile(
                unit,
                title,
                spec,
                opt,
                per_models=per_models and title == "Jump Packs",
            )
        )

    for group_opts in mobility_groups.values():
        if len(group_opts) >= 2 or any(
            (o.get("title") or infer_title(o.get("text", ""), o)) in MOBILITY_PROFILES
            for o in group_opts
        ):
            for opt in group_opts:
                consume_mobility(opt)
        else:
            kept.extend(group_opts)

    for opt in list(kept):
        title = (opt.get("title") or infer_title(opt.get("text", ""), opt) or "").strip()
        spec = MOBILITY_PROFILES.get(title)
        if not spec:
            continue
        text = (opt.get("text") or "").lower()
        if title == "Jump Packs" and (unit.get("profiles") or []):
            kept.remove(opt)
            continue
        if "move becomes" in text or "move characteristic" in text or title in MOBILITY_PROFILES:
            kept.remove(opt)
            profiles.append(build_mobility_profile(unit, title, spec, opt))

    unit["options"] = kept or None
    if unit["options"] is None:
        unit.pop("options", None)
    return profiles


def rename_profiles(unit: dict) -> None:
    profiles = unit.get("profiles") or []
    base_n = (unit.get("stats") or {}).get("N", "")
    unit_name = unit.get("name", "Models")

    for profile in profiles:
        name = profile.get("name", "")
        if not re.match(r"^Profile \d+$", name):
            continue
        n = profile.get("N") or base_n
        short = unit_name
        if n and str(n) != str(base_n):
            profile["name"] = f"{n} {short}"
        elif n:
            profile["name"] = f"{n} {short}"
        else:
            profile["name"] = f"{name.replace('Profile ', '')} {short}"


def strip_duplicate_abilities(unit: dict) -> None:
    abilities = unit.get("abilities")
    if not abilities:
        return

    profile_names = {p.get("name") for p in (unit.get("profiles") or [])}
    mobility_names = {"Jump Pack", "Jump Packs", "Terminator Armour", "Bike", "Wings", "Hover Drone"}
    if profile_names & mobility_names:
        abilities = re.sub(
            r"This unit can have one of the following:\s*\n.*?(?=\n[A-Z][a-z]|$)",
            "",
            abilities,
            flags=re.DOTALL,
        )
        lines = abilities.splitlines()
        kept = []
        for line in lines:
            lower = line.strip().lower()
            if not lower:
                kept.append(line)
                continue
            if lower.startswith("this unit can have one of the following"):
                continue
            if any(
                name.lower() in lower and ("move" in lower or "power rating" in lower or "save" in lower)
                for name in mobility_names
            ):
                continue
            if any(n.lower() == "wings" for n in profile_names) and (
                "move characteristic of 16" in lower
                or "additional keywords: fly" in lower
                or "additional abilities: deep strike" in lower
            ):
                continue
            kept.append(line)
        abilities = "\n".join(kept).strip()

    options = unit.get("options") or []
    if not options:
        if abilities:
            unit["abilities"] = abilities
        else:
            unit.pop("abilities", None)
        return

    option_snippets = []
    for opt in options:
        if isinstance(opt, dict):
            text = (opt.get("text") or "").strip()
            if text:
                option_snippets.append(text.lower())
            for choice in opt.get("chooseOne") or []:
                option_snippets.append(choice.lower())

    lines = abilities.splitlines()
    kept_lines = []
    for line in lines:
        stripped = line.strip().lstrip("•").strip()
        lower = stripped.lower()
        if any(snippet and snippet in lower for snippet in option_snippets if len(snippet) > 20):
            continue
        if re.search(r"one of the following:", lower) and any(
            re.search(r"one of the following:", s) for s in option_snippets
        ):
            continue
        if re.search(r"instead of 1 .+, this unit can be equipped", lower):
            if any("instead of" in s for s in option_snippets):
                continue
        kept_lines.append(line)

    cleaned = "\n".join(kept_lines).strip()
    unit["abilities"] = cleaned or None
    if not unit["abilities"]:
        unit.pop("abilities", None)


def extract_commander_battlesuit_profiles(unit: dict) -> list[dict]:
    if unit.get("name") != "Commander":
        return []
    base = unit.get("stats") or {}
    return [
        {
            "name": "XV8-02 Iridium",
            "M": base.get("M"),
            "WS": base.get("WS"),
            "BS": base.get("BS"),
            "A": base.get("A"),
            "W": base.get("W"),
            "Ld": base.get("Ld"),
            "Sv": "5+",
            "N": base.get("N"),
            "Pt": str(parse_pt(base.get("Pt")) + 1),
            "keywords": ["Battlesuit", "Fly", "Jet Pack"],
            "traits": ["XV8-02 Iridium"],
        },
        {
            "name": "XV85 Enforcer",
            "M": base.get("M"),
            "WS": base.get("WS"),
            "BS": base.get("BS"),
            "A": base.get("A"),
            "W": base.get("W"),
            "Ld": base.get("Ld"),
            "Sv": base.get("Sv"),
            "N": base.get("N"),
            "Pt": str(parse_pt(base.get("Pt")) + 1),
            "keywords": ["Battlesuit", "Fly", "Jet Pack"],
            "traits": ["XV85 Enforcer"],
            "abilities": (
                "Enforcer Battlesuit: At the start of the Damage phase, you can remove one "
                "blast marker from this unit. Small blast markers must be removed before large blast markers."
            ),
        },
        {
            "name": "XV86 Coldstar",
            "M": '20"',
            "WS": base.get("WS"),
            "BS": base.get("BS"),
            "A": base.get("A"),
            "W": base.get("W"),
            "Ld": base.get("Ld"),
            "Sv": base.get("Sv"),
            "N": base.get("N"),
            "Pt": str(parse_pt(base.get("Pt")) + 1),
            "keywords": ["Battlesuit", "Fly", "Jet Pack"],
            "traits": ["XV86 Coldstar"],
            "abilities": (
                "Equipped with 1 High-output Burst Cannon instead of one item from the Commander Weapons list."
            ),
        },
    ]


def remove_commander_battlesuit_options(unit: dict) -> None:
    if unit.get("name") != "Commander":
        return
    kept = []
    for opt in unit.get("options") or []:
        if not isinstance(opt, dict):
            continue
        text = (opt.get("text") or "").lower()
        if "xv85 enforcer" in text or "xv86 coldstar" in text:
            continue
        if "this model can have one of the following" in text:
            continue
        kept.append(opt)
    if kept:
        unit["options"] = kept
    else:
        unit.pop("options", None)


def migrate_unit(unit: dict) -> None:
    split_keywords_traits(unit)

    had_jump_packs = squad_had_jump_packs(unit)
    mobility_profiles = extract_mobility_profiles(unit)

    options = unit.get("options") or []
    migrated: list[dict] = []
    for opt in options:
        if isinstance(opt, str):
            continue
        updated = migrate_option(opt)
        if updated:
            migrated.append(updated)
    if migrated:
        unit["options"] = migrated
    elif "options" in unit:
        unit.pop("options")

    rename_profiles(unit)

    if mobility_profiles:
        existing = unit.get("profiles") or []
        existing_names = {p.get("name") for p in existing}
        for profile in mobility_profiles:
            if profile["name"] not in existing_names:
                existing.append(profile)
        unit["profiles"] = existing
    elif had_jump_packs:
        existing = unit.get("profiles") or []
        existing_names = {p.get("name") for p in existing}
        for profile in jump_profile_variants(unit):
            if profile["name"] not in existing_names:
                existing.append(profile)
        unit["profiles"] = existing

    if unit.get("name") == "Commander":
        remove_commander_battlesuit_options(unit)
        existing = unit.get("profiles") or []
        existing_names = {p.get("name") for p in existing}
        for profile in extract_commander_battlesuit_profiles(unit):
            if profile["name"] not in existing_names:
                existing.append(profile)
        unit["profiles"] = existing
        abilities = unit.get("abilities")
        if abilities:
            lines = abilities.splitlines()
            kept = []
            profile_name_set = {p.get("name") for p in unit.get("profiles") or []}
            for line in lines:
                lower = line.strip().lower()
                if "xv8-02" in lower and "XV8-02 Iridium" in profile_name_set:
                    continue
                if "enforcer battlesuit" in lower and "XV85 Enforcer" in profile_name_set:
                    continue
                kept.append(line)
            unit["abilities"] = "\n".join(kept).strip() or None
            if not unit["abilities"]:
                unit.pop("abilities", None)

    strip_duplicate_abilities(unit)


def migrate_data(data: dict) -> dict:
    data = copy.deepcopy(data)
    for unit in data.get("units", []):
        migrate_unit(unit)
    normalize_text_fields(data)
    return data


def write_markdown(data: dict, md_path: Path, preamble: str) -> None:
    body = json_to_markdown(data, md_path)
    fm_match = re.match(r"^(---\s*\n.*?\n---\s*\n)", body, re.DOTALL)
    if not fm_match:
        md_path.write_text(body, encoding="utf-8")
        return
    front = fm_match.group(1)
    rest = body[fm_match.end():]
    unit_match = re.search(r"^## Unit \d+ —", rest, re.MULTILINE)
    if unit_match is None or not preamble.strip():
        md_path.write_text(body, encoding="utf-8")
        return
    units = rest[unit_match.start():]
    md_path.write_text(f"{front}{preamble.rstrip()}\n\n{units}", encoding="utf-8")


def write_json_outputs(data: dict, json_path: Path, sync_web: bool) -> None:
    with open(json_path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    if sync_web and WEB_ARMY_LISTS_DIR.is_dir():
        web_path = WEB_ARMY_LISTS_DIR / json_path.name
        with open(web_path, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2, ensure_ascii=False)
            handle.write("\n")


def migrate_file(md_path: Path, sync_web: bool = True) -> None:
    text = md_path.read_text(encoding="utf-8")
    preamble = extract_preamble(text)
    json_path = md_path.with_suffix(".json")
    if json_path.exists():
        data = json.loads(json_path.read_text(encoding="utf-8"))
    else:
        data = markdown_to_json(text, md_path)
    migrated = migrate_data(data)
    write_markdown(migrated, md_path, preamble)
    write_json_outputs(migrated, json_path, sync_web)
    print(f"Migrated {md_path.name}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Migrate army list MD/JSON to reference format")
    parser.add_argument("paths", nargs="*", help="Markdown paths (default: 10 faction files)")
    parser.add_argument("--no-sync-web", action="store_true")
    args = parser.parse_args()

    paths = [Path(p) for p in args.paths] if args.paths else [ARMY_LISTS_DIR / name for name in FILES]
    for path in paths:
        migrate_file(path, sync_web=not args.no_sync_web)


if __name__ == "__main__":
    main()
