#!/usr/bin/env python3
"""Extract CSS custom properties (design tokens) from the DandyLions stylesheet.

Usage: python3 scripts/extract_css_tokens.py <path to styles.css>

Reads src/app/(frontend)/styles.css from rbijkercom/dandy-lions (checked out
by the sync workflow) and writes design-system/css-tokens.json. Only token
values are kept; the stylesheet itself is not stored in this repository.
design-system/tokens.json is the curated file; a maintainer reconciles it by
hand when this snapshot changes.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "design-system" / "css-tokens.json"

BLOCKS = {
    "theme": r"@theme\s*\{(.*?)\n\}",
    "light": r":root,\s*\[data-theme='light'\],\s*\.tone-light\s*\{(.*?)\n\}",
    "inverted": r"\[data-theme='inverted'\],\s*\.tone-sage\s*\{(.*?)\n\}",
    "layout_base": r"\n:root\s*\{(\s*--page-margin.*?)\n\}",
}
DECL = re.compile(r"(--[\w-]+)\s*:\s*([^;]+);")


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("usage: extract_css_tokens.py <styles.css>")
    css = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
    out = {"source": "rbijkercom/dandy-lions: src/app/(frontend)/styles.css"}
    for name, pattern in BLOCKS.items():
        match = re.search(pattern, css, re.S)
        out[name] = dict(DECL.findall(match.group(1))) if match else {}
    utilities = {}
    for util, body in re.findall(r"@utility\s+(type-[\w-]+)\s*\{(.*?)\}", css, re.S):
        utilities[util] = {k.strip(): v.strip() for k, v in re.findall(r"([\w-]+)\s*:\s*([^;]+);", body)}
    out["type_utilities"] = utilities
    if not any(out[name] for name in BLOCKS):
        sys.exit("no tokens found: the stylesheet structure changed, update BLOCKS")
    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
