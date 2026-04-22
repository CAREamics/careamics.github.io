"""Generate API reference markdown pages and navigation for zensical.

This script walks the careamics source tree, generates one .md file per public
module containing the mkdocstrings identifier (`::: package.module`), and builds
a navigation sub-tree compatible with zensical.toml.

Usage:
    python scripts/gen_ref_pages.py           # generate files + print nav block
    python scripts/gen_ref_pages.py --check   # also compare nav with zensical.toml
    python scripts/gen_ref_pages.py --write   # write generated nav into zensical.toml
    python scripts/gen_ref_pages.py --write --local # use local files in from_git dir.

To use a local careamics repo, run pull_from_repos.sh --local <path> first.
Then 
This creates a symlink at from_git/careamics so this script works transparently.
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

# nav_utils lives alongside this script; make it importable regardless of cwd.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from nav_utils import replace_nav_section  # noqa: E402

if sys.version_info >= (3, 11):
    import tomllib
else:
    try:
        import tomllib
    except ImportError:
        import tomli as tomllib  # type: ignore[no-redef]

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT / "from_git" / "careamics" / "src"
PACKAGE_NAME = "careamics"
PACKAGE_DIR = SRC_DIR / PACKAGE_NAME
OUT_DIR = ROOT / "docs" / "reference"
TOML_PATH = ROOT / "zensical.toml"
GITHUB_SOURCE_URL = "https://github.com/CAREamics/careamics/blob/main/src"

SKIP_FILES = {"__main__.py", "conftest.py", "py.typed"}
SKIP_MODULES = {}
SKIP_PREFIXES = ()
SKIP_DIRS = {}


def is_private(name: str) -> bool:
    """Return True for private names (single-underscore prefix), but not dunders."""
    return name.startswith("_") and not name.startswith("__")


# ---------------------------------------------------------------------------
# Phase 1 — Generate reference .md files
# ---------------------------------------------------------------------------
def generate_md_files(source: str) -> dict:
    """Walk the source tree and write .md files. Returns the nav tree."""
    if not PACKAGE_DIR.exists():
        print(f"Error: source directory {PACKAGE_DIR} not found.", file=sys.stderr)
        sys.exit(1)

    # Clean output directory
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir(parents=True)

    # Collect the navigation tree (nested dict/list structure)
    nav_tree = _walk_package(PACKAGE_DIR, PACKAGE_NAME, source)

    # Write top-level reference index with grid cards linking to subpackages
    _write_reference_index()

    return nav_tree


def _walk_package(package_path: Path, dotted_path: str, source: str) -> list:
    """Recursively walk a package directory, generate .md files, return nav entries."""
    entries = []

    # Collect subpackages and modules
    children = sorted(package_path.iterdir())
    subpackages = []
    modules = []

    for child in children:
        if child.name in SKIP_FILES or child.name == "__pycache__":
            continue

        if child.is_dir():
            if is_private(child.name):
                continue
            if child.name in SKIP_DIRS:
                continue
            if any(child.name.startswith(p) for p in SKIP_PREFIXES):
                continue
            if (child / "__init__.py").exists():
                subpackages.append(child)
        elif child.is_file() and child.suffix == ".py":
            if is_private(child.name):
                continue
            if child.stem in SKIP_MODULES:
                continue
            if any(child.stem.startswith(p) for p in SKIP_PREFIXES):
                continue
            modules.append(child)

    # Process __init__.py → index.md for this package
    init_file = package_path / "__init__.py"
    if init_file.exists():
        rel_md = _dotted_to_md_path(dotted_path, is_init=True)
        _write_md(rel_md, dotted_path, source)
        entries.append(f"reference/{rel_md}")

    # Process regular modules (non-__init__)
    for mod in modules:
        if mod.name == "__init__.py":
            continue
        mod_name = mod.stem
        mod_dotted = f"{dotted_path}.{mod_name}"
        rel_md = _dotted_to_md_path(mod_dotted, is_init=False)
        _write_md(rel_md, mod_dotted, source)
        entries.append(f"reference/{rel_md}")

    # Process subpackages recursively
    for subpkg in subpackages:
        sub_dotted = f"{dotted_path}.{subpkg.name}"
        sub_entries = _walk_package(subpkg, sub_dotted, source)
        if sub_entries:
            entries.append({_format_nav_title(subpkg.name): sub_entries})

    return entries


def _dotted_to_md_path(dotted: str, is_init: bool) -> str:
    """Convert 'careamics.config.algorithms' to 'careamics/config/algorithms/index.md'
    or 'careamics.config.algorithms.care' to 'careamics/config/algorithms/care.md'."""
    parts = dotted.split(".")
    if is_init:
        return "/".join(parts) + "/index.md"
    else:
        return "/".join(parts[:-1]) + f"/{parts[-1]}.md"


def _dotted_to_source_url(dotted_path: str, is_init: bool, source: str) -> str:
    """Convert a dotted path to a GitHub source URL."""
    parts = dotted_path.split(".")
    if is_init:
        return f"{source}/{'/'.join(parts)}/__init__.py"
    else:
        return f"{source}/{'/'.join(parts[:-1])}/{parts[-1]}.py"


def _write_md(rel_md: str, dotted_path: str, source: str) -> None:
    """Write a single .md file with a GitHub source link and mkdocstrings identifier."""
    out_path = OUT_DIR / rel_md
    out_path.parent.mkdir(parents=True, exist_ok=True)
    is_init = rel_md.endswith("index.md")
    source_url = _dotted_to_source_url(dotted_path, is_init, source)
    # Derive title from the last component of the dotted path
    name = dotted_path.rsplit(".", 1)[-1]
    title = _format_nav_title(name)
    out_path.write_text(
        f"---\ntitle: {title}\n---\n\n"
        f"[:fontawesome-brands-github: Source]({source_url})\n"
        f"\n"
        f"::: {dotted_path}\n"
    )


def _format_nav_title(name: str) -> str:
    """Format a module/package name for navigation display."""
    import re

    # Acronyms that should be fully uppercased.
    # Words followed by \b match as whole words; those marked with (?=\s|$)
    # only match when followed by a space or end-of-string.
    _ACRONYMS = {
        "n2v": "N2V",
        "fcn": "FCN",
        "lvae": "LVAE",
        "xy": "XY",
        "tta": "TTA",
        "io": "IO",
        "care": "CARE",
        "hdn": "HDN",
        "pn2v": "PN2V",
        "vae": "VAE",
        "unet": "UNet",
    }
    # Acronyms that must only match before a space or end-of-string
    _SPACE_ONLY = {"xy", "tta", "io", "care", "unet"}

    title = name.replace("_", " ").title()

    for lower, upper in _ACRONYMS.items():
        if lower in _SPACE_ONLY:
            title = re.sub(
                rf"\b{re.escape(lower)}\b(?=\s|$)",
                upper,
                title,
                flags=re.IGNORECASE,
            )
        else:
            title = re.sub(
                rf"\b{re.escape(lower)}\b",
                upper,
                title,
                flags=re.IGNORECASE,
            )

    return title


def _write_reference_index() -> None:
    """Write the top-level reference/index.md with grid cards."""
    subpackages = sorted(
        p.name
        for p in PACKAGE_DIR.iterdir()
        if p.is_dir()
        and (p / "__init__.py").exists()
        and not is_private(p.name)
        and p.name != "__pycache__"
        and p.name not in SKIP_DIRS
        and not any(p.name.startswith(pr) for pr in SKIP_PREFIXES)
    )

    lines = [
        "---",
        "icon: octicons/code-24",
        "description: API Reference",
        "---",
        "",
        "# API Reference",
        "",
        "Use the navigation on the left to explore the code reference, or pick a "
        "subpackage below.",
        "",
        '<div class="grid cards" markdown>',
        "",
    ]

    for pkg in subpackages:
        title = _format_nav_title(pkg)
        lines.append(f"-   :octicons-package-24:{{ .lg .middle }} __{title}__")
        lines.append("")
        lines.append("    ---")
        lines.append("")
        lines.append(f"    [:octicons-arrow-right-24: {title}](careamics/{pkg}/)")
        lines.append("")

    lines.append("</div>")
    lines.append("")

    (OUT_DIR / "index.md").write_text("\n".join(lines))


# ---------------------------------------------------------------------------
# Phase 2 — Build navigation list (TOML-ready)
# ---------------------------------------------------------------------------
def nav_to_toml_lines(nav: list, indent: int = 0) -> list[str]:
    """Convert the nav tree to TOML-formatted lines for pasting into zensical.toml."""
    lines = []
    prefix = "    " * indent
    for entry in nav:
        if isinstance(entry, str):
            lines.append(f'{prefix}"{entry}",')
        elif isinstance(entry, dict):
            for key, value in entry.items():
                lines.append(f'{prefix}{{"{key}" = [')
                lines.extend(nav_to_toml_lines(value, indent + 1))
                lines.append(f"{prefix}]}},")
    return lines


def print_nav_block(nav: list) -> None:
    """Print the full nav entry for zensical.toml to stdout."""
    print('{"API Reference" = [')
    print('    "reference/index.md",')
    # The nav tree starts with the careamics package entries
    # We wrap them under a "careamics" section
    inner_lines = nav_to_toml_lines(nav, indent=1)
    for line in inner_lines:
        print(line)
    print("]},")


# ---------------------------------------------------------------------------
# Phase 3 — Compare with zensical.toml
# ---------------------------------------------------------------------------
def check_nav(nav: list) -> bool:
    """Compare generated nav with the 'API Reference' entry in zensical.toml.
    Returns True if they match, False otherwise."""
    with open(TOML_PATH, "rb") as f:
        config = tomllib.load(f)

    existing_nav = config.get("project", {}).get("nav", config.get("nav", []))

    # Find the "API Reference" entry
    api_ref_entry = None
    for entry in existing_nav:
        if isinstance(entry, dict) and "API Reference" in entry:
            api_ref_entry = entry["API Reference"]
            break

    if api_ref_entry is None:
        print(
            "No 'API Reference' entry found in zensical.toml nav.",
            file=sys.stderr,
        )
        print("Add the following block to the nav list:\n", file=sys.stderr)
        print_nav_block(nav)
        return False

    # Build the expected nav (with reference/index.md at the top)
    expected = ["reference/index.md"] + nav

    if api_ref_entry != expected:
        print("Nav mismatch! Expected:\n", file=sys.stderr)
        print_nav_block(nav)
        print(
            "\nUpdate the 'API Reference' entry in zensical.toml to match.",
            file=sys.stderr,
        )
        return False

    return True


def write_nav_to_toml(nav: list) -> None:
    """Replace the API Reference nav block in zensical.toml with the generated nav."""
    toml_text = TOML_PATH.read_text()

    # Build the replacement TOML block
    inner_lines = ['    "reference/index.md",']
    inner_lines.extend(nav_to_toml_lines(nav, indent=1))
    new_block = '{"API Reference" = [\n' + "\n".join(inner_lines) + "\n  ]},"

    new_text, ok = replace_nav_section(toml_text, "API Reference", new_block)
    if not ok:
        print(
            "Error: could not find 'API Reference' block in zensical.toml.",
            file=sys.stderr,
        )
        sys.exit(1)

    TOML_PATH.write_text(new_text)
    print(f"Updated API Reference nav in {TOML_PATH}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate API reference .md files for zensical."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Compare generated nav with zensical.toml and exit non-zero on mismatch.",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write the generated nav directly into zensical.toml.",
    )
    parser.add_argument(
        "--local",
        action="store_true",
        help=(
            "Whether to use local files as the API reference source. (These have to be "
            "in the from_git directory)"
        ),
    )
    args = parser.parse_args()
    if args.local:
        ref_source = "from_git"
    else:
        ref_source = GITHUB_SOURCE_URL

    nav = generate_md_files(ref_source)
    print(f"Generated reference pages in {OUT_DIR}")
    print()
    print("=== Nav block for zensical.toml ===")
    print_nav_block(nav)

    if args.write:
        write_nav_to_toml(nav)

    if args.check:
        if not check_nav(nav):
            sys.exit(1)
        else:
            print("\nNav is up to date.", file=sys.stderr)


if __name__ == "__main__":
    main()
