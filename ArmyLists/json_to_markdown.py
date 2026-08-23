#!/usr/bin/env python3
"""Convert Army List JSON files to Markdown."""

import argparse
from pathlib import Path

from army_list_markdown import ARMY_LISTS_DIR, write_markdown_from_json

DEFAULT_GLOB = "Apoc40k-Armies-1st - *.json"


def main():
    parser = argparse.ArgumentParser(description="Convert army list JSON to Markdown")
    parser.add_argument(
        "paths",
        nargs="*",
        help="JSON file paths (default: all Apoc40k-Armies-1st JSON files)",
    )
    args = parser.parse_args()

    if args.paths:
        json_paths = [Path(p) for p in args.paths]
    else:
        json_paths = sorted(ARMY_LISTS_DIR.glob(DEFAULT_GLOB))

    for json_path in json_paths:
        md_path = write_markdown_from_json(json_path)
        print(f"Wrote {md_path.name}")


if __name__ == "__main__":
    main()
