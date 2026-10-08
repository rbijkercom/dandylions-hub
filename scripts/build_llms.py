#!/usr/bin/env python3
"""Build llms.txt (index) and llms-full.txt (all content) for the DandyLions hub.

Run from anywhere: python3 scripts/build_llms.py
Both files are written to the repository root and served by GitHub Pages.
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://rbijkercom.github.io/dandylions-hub"

# (path, one-line description). Order is the reading order in llms-full.txt.
SECTIONS = {
    "Start here": [
        ("README.md", "What the hub is and its rules"),
        ("project-instructions.md", "Instructions for Claude: sources, voice, LinkedIn and Instagram, output format"),
    ],
    "Voice": [
        ("voice/voice-and-tone.md", "Who speaks (I vs we), tone, vocabulary, style rules"),
        ("voice/multilingual-glossary.md", "Official EN / IT / NL terms"),
    ],
    "Design system": [
        ("design-system/brand-rules.md", "Name, tagline, logo and lion mark, graphic devices, imagery, do and don't"),
        ("design-system/social-formats.md", "LinkedIn and Instagram sizes, safe zones, Figma templates"),
        ("design-system/tokens.json", "Colours, themes, typography, spacing, radius, grain"),
    ],
    "Sources": [
        ("sources/README.md", "What each source holds and its status; placeholder rules"),
        ("sources/about.md", "Fabio, archetypes, vision and mission, track record, testimonials, contact"),
        ("sources/offerings/insights.md", "Insights (Clarity): formats and newsletter"),
        ("sources/offerings/educational-events.md", "Educational Events: five topics"),
        ("sources/offerings/consulting.md", "Consulting (Impact): Ready/Set/Go, services, Team Alignment"),
        ("sources/offerings/project-coaching.md", "Project Coaching"),
        ("sources/offerings/policy-compass.md", "Policy Compass"),
        ("sources/offerings/collaborative-kitchen.md", "Collaborative Kitchen"),
        ("sources/offerings/the-story-beneath.md", "The Story Beneath"),
        ("sources/offerings/pattern-weaver-approach.md", "Pattern Weaver Approach: technical vs adaptive, four loyalties"),
        ("sources/articles.md", "Field notes: titles and deks"),
        ("sources/linkedin/README.md", "How to write LinkedIn posts"),
        ("sources/linkedin/post-template.md", "LinkedIn draft template"),
        ("sources/instagram/README.md", "How to write Instagram posts"),
        ("sources/instagram/post-template.md", "Instagram draft template"),
    ],
}


def page_url(path: str) -> str:
    if path.endswith(".md"):
        return f"{BASE}/{path[:-3]}.html"
    return f"{BASE}/{path}"


def main() -> None:
    index = [
        "# DandyLions hub",
        "",
        "> Single source of truth for DandyLions (founder Fabio Bortolazzi): design system, voice and published source material for LinkedIn and Instagram content. Read-only reference maintained by Ruben Bijker. Never invent facts or quotes; gaps are marked [TO BE SUPPLIED BY RUBEN: ...].",
        "",
        f"Everything in one file: {BASE}/llms-full.txt",
        "",
    ]
    full = [
        "# DandyLions hub: full content",
        "",
        f"Source: {BASE}/ . This file concatenates every hub file. Each file starts with a line '===== FILE: <path> ====='. Cite those paths as sources.",
        "Read-only reference maintained by Ruben Bijker. Never invent facts, figures, events or quotes. Gaps are marked [TO BE SUPPLIED BY RUBEN: ...].",
        "",
    ]
    for section, files in SECTIONS.items():
        index += [f"## {section}", ""]
        for path, desc in files:
            index.append(f"- [{path}]({page_url(path)}): {desc}")
            text = (ROOT / path).read_text(encoding="utf-8").strip()
            full += [f"===== FILE: {path} =====", "", text, ""]
        index.append("")
    (ROOT / "llms.txt").write_text("\n".join(index).rstrip() + "\n", encoding="utf-8")
    (ROOT / "llms-full.txt").write_text("\n".join(full).rstrip() + "\n", encoding="utf-8")
    size = (ROOT / "llms-full.txt").stat().st_size
    print(f"wrote llms.txt and llms-full.txt ({size:,} bytes)")


if __name__ == "__main__":
    main()
