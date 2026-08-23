#!/usr/bin/env python3
"""Convert Army List Markdown files back to JSON (and sync web copies)."""

import argparse
from pathlib import Path

from army_list_markdown import ARMY_LISTS_DIR, write_json_from_markdown

DEFAULT_GLOB = "Apoc40k-Armies-1st - *.md"


def main():
    parser = argparse.ArgumentParser(description="Convert army list Markdown to JSON")
    parser.add_argument(
        "paths",
        nargs="*",
        help="Markdown file paths (default: all Apoc40k-Armies-1st Markdown files)",
    )
    parser.add_argument(
        "--no-sync-web",
        action="store_true",
        help="Do not copy JSON to web/src/ArmyLists",
    )
    args = parser.parse_args()

    if args.paths:
        md_paths = [Path(p) for p in args.paths]
    else:
        md_paths = sorted(ARMY_LISTS_DIR.glob(DEFAULT_GLOB))

    for md_path in md_paths:
        json_path = write_json_from_markdown(md_path, sync_web=not args.no_sync_web)
        print(f"Wrote {json_path.name}")


if __name__ == "__main__":
    main()
