"""Merge nav.toml entries from the careamics repo into zensical.toml.

Reads the top-level {…} blocks from nav.toml and replaces the matching
section in zensical.toml (identified by the section name as the key).  The
replacement is idempotent: running the script multiple times always produces
the same result regardless of the current state of zensical.toml.

Usage:
    python scripts/update_nav.py                  # print merged nav to stdout (dry-run)
    python scripts/update_nav.py --write           # apply changes to zensical.toml
    python scripts/update_nav.py --nav path/to/nav.toml --toml path/to/zensical.toml --write
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Ensure the scripts directory is on the path so nav_utils can be imported
# both when run directly and when invoked from another directory.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from nav_utils import extract_nav_blocks, replace_nav_section  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_NAV = ROOT / "from_git" / "careamics" / "docs" / "nav.toml"
DEFAULT_TOML = ROOT / "zensical.toml"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Merge nav.toml entries into zensical.toml."
    )
    parser.add_argument(
        "--nav",
        type=Path,
        default=DEFAULT_NAV,
        help="Path to nav.toml (default: from_git/careamics/docs/nav.toml)",
    )
    parser.add_argument(
        "--toml",
        type=Path,
        default=DEFAULT_TOML,
        help="Path to zensical.toml (default: zensical.toml at repo root)",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write changes into zensical.toml. Without this flag the merged nav is printed to stdout.",
    )
    args = parser.parse_args()

    if not args.nav.exists():
        print(f"Warning: {args.nav} not found, skipping nav merge.", file=sys.stderr)
        sys.exit(0)

    nav_content = args.nav.read_text()
    toml_text = args.toml.read_text()

    blocks = extract_nav_blocks(nav_content)
    replaced = 0
    for block in blocks:
        m = re.match(r'\{"([^"]+)"\s*=', block)
        if not m:
            continue
        name = m.group(1)
        new_text, ok = replace_nav_section(toml_text, name, block + ",")
        if ok:
            toml_text = new_text
            replaced += 1
            if args.write:
                print(f"  Replaced: {name!r}")
            else:
                print(f"=== {name} ===")
                print(block)
                print()
        else:
            print(
                f"  Warning: no placeholder found for {name!r}, skipping.",
                file=sys.stderr,
            )

    if args.write and replaced:
        args.toml.write_text(toml_text)
        print(f"  Wrote {args.toml}")


if __name__ == "__main__":
    main()
