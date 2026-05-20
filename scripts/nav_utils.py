"""Shared utilities for reading nav.toml and updating nav sections in zensical.toml."""
from __future__ import annotations

import re


def extract_nav_blocks(nav_content: str) -> list[str]:
    """Extract all top-level {…} blocks from nav.toml content.

    Strips TOML line comments before processing to avoid false matches from
    comment text that happens to contain brace characters.
    """
    content = re.sub(r"#[^\n]*", "", nav_content)

    blocks: list[str] = []
    depth = 0
    start: int | None = None
    for i, ch in enumerate(content):
        if ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0 and start is not None:
                blocks.append(content[start : i + 1])
                start = None
    return blocks


def find_nav_section_span(toml_text: str, section_name: str) -> tuple[int, int] | None:
    """Return (start, end) character indices of the {"section_name" = [...]} block.

    The span includes any trailing comma and inline comment on the same line,
    so they are cleanly replaced together with the block.  Returns None when the
    section is not found or the braces are unbalanced.
    """
    pattern = re.compile(r'\{"' + re.escape(section_name) + r'"')
    m = pattern.search(toml_text)
    if m is None:
        return None

    start = m.start()
    depth = 0
    end: int | None = None
    for i in range(start, len(toml_text)):
        ch = toml_text[i]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                end = i + 1
                break

    if end is None:
        return None

    # Consume an optional trailing comma and inline comment (e.g. ", # filled by …")
    m2 = re.match(r",?[ \t]*(?:#[^\n]*)?", toml_text[end:])
    if m2:
        end += m2.end()

    return start, end


def replace_nav_section(toml_text: str, section_name: str, new_block: str) -> tuple[str, bool]:
    """Replace the {"section_name" = [...]} block in toml_text with new_block.

    Uses brace-depth tracking, so it handles arbitrarily nested inline tables.
    The trailing comma and any inline comment after the closing brace are also
    consumed; callers should include a trailing comma in new_block if needed.

    Returns (updated_text, was_replaced).
    """
    span = find_nav_section_span(toml_text, section_name)
    if span is None:
        return toml_text, False
    start, end = span
    return toml_text[:start] + new_block + toml_text[end:], True
