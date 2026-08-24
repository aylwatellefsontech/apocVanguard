#!/usr/bin/env python3
"""Bidirectional Apoc40k Cards JSON ↔ Markdown conversion."""

from __future__ import annotations

import json
import re
from pathlib import Path

CARDS_DIR = Path(__file__).resolve().parent
WEB_CARDS_DIR = CARDS_DIR.parent / "web" / "src" / "Cards"

FIELD_ORDER = [
    "set",
    "nm",
    "fac",
    "facNm",
    "type",
    "subType",
    "cst",
    "atk",
    "life",
    "sh",
    "removed",
]

CARD_HEADER = re.compile(r"^## Card (\d+)(?: — (.+))?$")
FRONT_MATTER = re.compile(r"^---\s*\n.*?\n---\s*\n", re.DOTALL)
FIELD_LINE = re.compile(r"^- ([a-zA-Z]+): (.+)$")


def _format_field_value(value) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def _parse_field_value(raw: str):
    text = raw.strip()
    if text == "true":
        return True
    if text == "false":
        return False
    try:
        return int(text)
    except ValueError:
        return text


def json_to_markdown(data: dict, json_path: Path | None = None) -> str:
    source = data.get("source") or (json_path.name if json_path else "")
    lines = ["---", f"source: {source}", "---", ""]

    title = json_path.stem if json_path else "Apoc40k Cards"
    lines.append(f"# {title}")
    lines.append("")

    for card in data.get("cards") or []:
        nm = card.get("nm", "?")
        name = card.get("name")
        if name:
            lines.append(f"## Card {nm} — {name}")
        else:
            lines.append(f"## Card {nm}")
        lines.append("")
        lines.append("### Fields")
        for key in FIELD_ORDER:
            if key not in card:
                continue
            value = card.get(key)
            if value is None:
                continue
            lines.append(f"- {key}: {_format_field_value(value)}")
        lines.append("")

        ability = card.get("ability")
        if ability:
            lines.append("### Ability")
            lines.append("```")
            lines.append(ability.strip())
            lines.append("```")
            lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def markdown_to_json(text: str, md_path: Path | None = None) -> dict:
    meta: dict[str, str] = {}
    body = text
    match = FRONT_MATTER.match(text)
    if match:
        body = text[match.end() :]
        for line in match.group(0).splitlines():
            if line.strip() == "---" or not line.strip():
                continue
            if ":" in line:
                key, value = line.split(":", 1)
                meta[key.strip()] = value.strip()

    cards: list[dict] = []
    blocks = re.split(r"(?m)^(?=## Card \d+)", body)

    for block in blocks:
        block = block.strip()
        if not block.startswith("## Card "):
            continue

        header_end = block.find("\n")
        header = block[:header_end].strip()
        rest = block[header_end + 1 :].strip()

        header_match = CARD_HEADER.match(header)
        if not header_match:
            continue

        card: dict = {"nm": int(header_match.group(1))}
        if header_match.group(2):
            card["name"] = header_match.group(2).strip()

        ability_match = re.search(
            r"### Ability\s*\n```\n(.*?)\n```", rest, flags=re.DOTALL
        )
        if ability_match:
            card["ability"] = ability_match.group(1).strip()
            rest = rest[: ability_match.start()].strip()

        fields_match = re.search(
            r"### Fields\s*\n(.*?)(?:\n### |\n## Card |\Z)", rest, flags=re.DOTALL
        )
        if fields_match:
            for line in fields_match.group(1).splitlines():
                field_match = FIELD_LINE.match(line.strip())
                if not field_match:
                    continue
                key = field_match.group(1)
                if key == "nm":
                    continue
                card[key] = _parse_field_value(field_match.group(2))

        cards.append(card)

    source = meta.get("source") or (md_path.name.replace(".md", ".json") if md_path else "")
    return {"source": source, "cards": cards}


def round_trip_equal(original: dict, restored: dict) -> bool:
    return original == restored


def write_markdown_from_json(json_path: Path) -> Path:
    data = json.loads(json_path.read_text(encoding="utf-8"))
    md_path = json_path.with_suffix(".md")
    md_path.write_text(json_to_markdown(data, json_path), encoding="utf-8")
    return md_path


def write_json_from_markdown(md_path: Path, *, sync_web: bool = True) -> Path:
    text = md_path.read_text(encoding="utf-8")
    data = markdown_to_json(text, md_path)
    json_path = md_path.with_suffix(".json")
    with open(json_path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    if sync_web and WEB_CARDS_DIR.is_dir():
        web_path = WEB_CARDS_DIR / json_path.name
        with open(web_path, "w", encoding="utf-8") as handle:
            json.dump(data, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
    return json_path
