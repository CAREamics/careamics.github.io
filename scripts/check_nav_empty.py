"""Reset nav entries in zensical.toml that must be left empty at commit time.

Used by pre-commit.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from nav_utils import replace_nav_section

ROOT = Path(__file__).resolve().parent.parent
TOML_PATH = ROOT / "zensical.toml"

# Nav keys whose list value must always be [] in version control.
# These are filled at build time and must never be committed with content.
SHOULD_BE_EMPTY: list[str] = [
    "Using CAREamics",  # filled by scripts/pull_from_repos.sh
    "Tutorials",        # filled by scripts/pull_from_repos.sh
    "Legacy (v0.1)",    # filled by scripts/pull_from_repos.sh
    "API Reference",    # filled by scripts/gen_ref_pages.py
]


def main() -> None:
    content = TOML_PATH.read_text()
    changed: list[str] = []

    for key in SHOULD_BE_EMPTY:
        new_content, replaced = replace_nav_section(content, key, f'{{"{key}" = []}},')
        if replaced and new_content != content:
            content = new_content
            changed.append(key)

    if changed:
        TOML_PATH.write_text(content)
        for key in changed:
            print(
                f'pre-commit: reset nav entry "{key}" to [] in zensical.toml',
                file=sys.stderr,
            )


if __name__ == "__main__":
    main()
