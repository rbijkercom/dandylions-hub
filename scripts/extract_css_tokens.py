#!/usr/bin/env python3
"""Extract CSS custom properties from the synced DandyLions stylesheet.

Reads design-system/upstream/styles.css (copied from rbijkercom/dandy-lions,
src/app/(frontend)/styles.css) and writes design-system/upstream/css-tokens.json.
The output is a mechanical snapshot. design-system/tokens.json is the curated
file Claude reads; a maintainer reconciles it by hand when this snapshot changes.
"""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
CSS = ROOT / "design-system" / "upstream" / "styles.css"
OUT = ROOT / "design-system" / "upstream" / "css-tokens.json"

BLOCKS = {
    "theme": r"@theme\s*\{(.*?)\n\}",
    "light": r":root,\s*\[data-theme='light'\],\s*\.tone-light\s*\{(.*?)\n\}",
    "inverted": r"\[data-theme='inverted'\],\s*\.tone-sage\s*\{(.*?)\n\}",
    "layout_base": r"\n:root\s*\{(\s*--page-margin.*?)\n\}",
}
DECL = re.compile(r"(--[\w-]+)\s*:\s*([^;]+);")


def main() -> None:
    css = CSS.read_text(encoding="utf-8")
    out = {"source": "rbijkercom/dandy-lions: src/app/(frontend)/styles.css"}
    for name, pattern in BLOCKS.items():
        match = re.search(pattern, css, re.S)
        out[name] = dict(DECL.findall(match.group(1))) if match else {}
    utilities = {}
    for util, body in re.findall(r"@utility\s+(type-[\w-]+)\s*\{(.*?)\}", css, re.S):
        utilities[util] = {k.strip(): v.strip() for k, v in re.findall(r"([\w-]+)\s*:\s*([^;]+);", body)}
    out["type_utilities"] = utilities
    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
