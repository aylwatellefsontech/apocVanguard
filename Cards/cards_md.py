#!/usr/bin/env python3
"""Apoc40k Cards JSON ↔ Markdown utilities."""

import argparse
import json
from pathlib import Path

from cards_markdown import (
    CARDS_DIR,
    json_to_markdown,
    markdown_to_json,
    round_trip_equal,
    write_json_from_markdown,
    write_markdown_from_json,
)

DEFAULT_JSON_GLOB = "Apoc40kCards - cards*.json"


def cmd_to_md(paths: list[str]) -> None:
    json_paths = [Path(p) for p in paths] if paths else sorted(CARDS_DIR.glob(DEFAULT_JSON_GLOB))
    for json_path in json_paths:
        md_path = write_markdown_from_json(json_path)
        print(f"Wrote {md_path.name}")


def cmd_to_json(paths: list[str], sync_web: bool) -> None:
    md_paths = [Path(p) for p in paths] if paths else sorted(CARDS_DIR.glob("Apoc40kCards - cards*.md"))
    for md_path in md_paths:
        json_path = write_json_from_markdown(md_path, sync_web=sync_web)
        print(f"Wrote {json_path.name}")


def cmd_verify(paths: list[str]) -> None:
    json_paths = [Path(p) for p in paths] if paths else sorted(CARDS_DIR.glob(DEFAULT_JSON_GLOB))
    failed = []
    for json_path in json_paths:
        original = json.loads(json_path.read_text(encoding="utf-8"))
        md_text = json_to_markdown(original, json_path)
        restored = markdown_to_json(md_text, json_path)
        if not round_trip_equal(original, restored):
            failed.append(json_path.name)
            print(f"FAIL {json_path.name}")
        else:
            print(f"OK   {json_path.name}")
    if failed:
        raise SystemExit(f"Round-trip failed for {len(failed)} file(s)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Apoc40k Cards JSON ↔ Markdown conversion")
    sub = parser.add_subparsers(dest="command", required=True)

    to_md = sub.add_parser("to-md", help="Convert JSON to Markdown")
    to_md.add_argument("paths", nargs="*")

    to_json = sub.add_parser("to-json", help="Convert Markdown to JSON")
    to_json.add_argument("paths", nargs="*")
    to_json.add_argument("--no-sync-web", action="store_true")

    verify = sub.add_parser("verify", help="Verify JSON round-trip through Markdown")
    verify.add_argument("paths", nargs="*")

    args = parser.parse_args()
    if args.command == "to-md":
        cmd_to_md(args.paths)
    elif args.command == "to-json":
        cmd_to_json(args.paths, sync_web=not args.no_sync_web)
    elif args.command == "verify":
        cmd_verify(args.paths)


if __name__ == "__main__":
    main()
