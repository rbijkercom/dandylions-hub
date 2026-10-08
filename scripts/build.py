#!/usr/bin/env python3
"""Build the DandyLions hub pages from manifest.json (stdlib only).

Writes: index.html, templates/index.html, assets/index.html,
design-system/index.html, project-instructions.html, llms.txt, llms-full.txt.
Image sizes and SVG viewBoxes are read from the files themselves.
Run after adding or changing anything in manifest.json, design-system/ or the
image folders, then commit the result. The Pages workflow also runs it.
"""
import html
import json
import pathlib
import re
import struct
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
M = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
BASE = M["base_url"]
RAW = M["raw_base_url"]
TOKENS = json.loads((ROOT / "design-system" / "tokens.json").read_text(encoding="utf-8"))


def info(rel):
    p = ROOT / rel
    if not p.exists():
        sys.exit(f"missing file listed in manifest.json: {rel}")
    data = p.read_bytes()
    ext = p.suffix.lower()
    out = {"bytes": len(data), "format": ext.lstrip(".").upper()}
    if ext == ".png":
        w, h = struct.unpack(">II", data[16:24])
        out["size"] = f"{w} x {h} px"
    elif ext == ".ico":
        w = data[6] or 256
        h = data[7] or 256
        out["size"] = f"{w} x {h} px"
    elif ext == ".svg":
        text = data.decode("utf-8")
        vb = re.search(r'viewBox="([^"]+)"', text)
        out["size"] = f"viewBox {vb.group(1)}" if vb else "no viewBox"
    return out


def esc(s):
    return html.escape(str(s), quote=True)


for sec in M["sections"]:
    for it in sec["items"]:
        it.update(info(it["file"]))
        it["url"] = BASE + it["file"]
        if it["file"].endswith(".svg"):
            it["raw_url"] = RAW + it["file"]

CSS = """
body{margin:0;background:#F5F2EC;color:#2D2D2D;font:16px/1.5 'Hanken Grotesk',Arial,Helvetica,sans-serif}
main{max-width:1200px;margin:0 auto;padding:40px 24px 80px}
h1,h2,h3{font-family:'Cormorant Garamond',Georgia,serif;font-weight:400;line-height:1.15}
h1{font-size:44px;margin:0 0 8px}h2{font-size:30px;margin:48px 0 8px;border-top:1px solid #E3DDCE;padding-top:24px}h3{font-size:20px;margin:0 0 4px}
a{color:#7A663C}code{font-size:13px;background:#E9E8DF;padding:1px 4px;border-radius:4px;word-break:break-all}
nav a{margin-right:16px;text-transform:uppercase;letter-spacing:1.5px;font-size:13px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:20px}
.card{background:#FBF9F4;border:1px solid #E3DDCE;border-radius:12px;padding:12px;font-size:14px}
.card img{width:100%;height:220px;object-fit:contain;background:#E9E8DF;border-radius:8px;margin-bottom:8px}
.card.icon img{height:72px;background:#F5F2EC}
.meta{color:#454340;font-size:13px}
.ph{background:#FBF9F4;border:1px dashed #907948;border-radius:12px;padding:12px;margin:8px 0}
table{border-collapse:collapse;width:100%;font-size:14px}td,th{border-bottom:1px solid #E3DDCE;padding:6px;text-align:left;vertical-align:top}
.sw{display:inline-block;width:28px;height:28px;border-radius:6px;border:1px solid #CFCEC6;vertical-align:middle}
"""


def page(title, body, depth=0):
    up = "../" * depth
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><link rel="icon" href="{up}assets/logos/favicon.ico"><style>{CSS}</style></head>
<body><main>
<nav><a href="{up}">Hub</a><a href="{up}design-system/">Tokens</a><a href="{up}templates/">Templates</a><a href="{up}assets/">Logos &amp; icons</a><a href="{up}project-instructions.html">Claude setup</a><a href="{up}llms-full.txt">llms-full.txt</a></nav>
{body}
<p class="meta" style="margin-top:64px">DandyLions hub. Read-only reference, maintained by Ruben Bijker. Updated {esc(M['updated'])}.</p>
</main></body></html>
"""


def card(it, depth, icon=False):
    up = "../" * depth
    dark = ' style="background:#748262"' if "ivory" in it["file"] else ""
    lines = [f'<img src="{up}{esc(it["file"])}" alt="{esc(it["title"])}" loading="lazy"{dark}>' if it["format"] != "ICO" else f'<img src="{up}{esc(it["file"])}" alt="favicon">',
             f'<h3>{esc(it["title"])}</h3>',
             f'<div class="meta">{esc(it["format"])} · {esc(it["size"])}' + (f' · {esc(it["format_label"])}' if it.get("format_label") else "") + "</div>"]
    if not icon:
        lines.append(f'<p>{esc(it["description"])}</p>')
        if it.get("background"):
            lines.append(f'<p class="meta">Background: {esc(it["background"])}. Use: {esc(it["use"])}</p>')
    lines.append(f'<p class="meta"><a href="{esc(it["url"])}">{esc(it["url"])}</a>' + (f'<br>Raw text: <a href="{esc(it["raw_url"])}">raw.githubusercontent.com</a>' if it.get("raw_url") else "") + "</p>")
    if not icon:
        lines.append(f'<p class="meta">Source: {esc(it["source"])}</p>')
    return f'<div class="card{" icon" if icon else ""}">' + "".join(lines) + "</div>"


def sections_html(page_id, depth):
    out = []
    for sec in M["sections"]:
        if sec["page"] != page_id:
            continue
        out.append(f'<h2 id="{esc(sec["id"])}">{esc(sec["title"])}</h2>')
        if sec.get("note"):
            out.append(f'<p class="meta">{esc(sec["note"])}</p>')
        if sec["id"] == "icons":
            out.append(f'<p class="meta">Source: {esc(sec["items"][0]["source"])}</p>')
        out.append('<div class="grid">' + "".join(card(it, depth, icon=sec["id"] == "icons") for it in sec["items"]) + "</div>")
    return "\n".join(out)


def placeholders_html():
    return "<h2 id=\"placeholders\">Not included (placeholders)</h2>" + "".join(
        f'<div class="ph"><strong>{esc(p["title"])}</strong><br>{esc(p["note"])}</div>' for p in M["placeholders"])


def counts():
    return {sec["id"]: len(sec["items"]) for sec in M["sections"]}


# ---------- pages ----------
c = counts()
index = f"""<h1>DandyLions hub</h1>
<p>Visual reference for DandyLions: design tokens, real template images and brand assets. Public and read-only. There is no copy or writing guidance here: only how things look.</p>
<ul>
<li><a href="design-system/">Design tokens</a>: <a href="design-system/tokens.json">tokens.json</a> (curated) and <a href="design-system/css-tokens.json">css-tokens.json</a> (raw, synced daily from the website)</li>
<li><a href="templates/">Template images</a>: {c['social']} social, {c['slides']} presentation, {c['email']} email, {c['brand-guide']} brand guide pages</li>
<li><a href="assets/">Logos, icons and graphics</a>: {c['logos']} logo files, {c['icons']} icons, {c['graphics']} graphic devices (SVG served as text)</li>
<li><a href="project-instructions.html">Set up a Claude Project</a> that uses this hub</li>
<li>For AI tools: <a href="llms.txt">llms.txt</a> (index) and <a href="llms-full.txt">llms-full.txt</a> (everything, with absolute URLs); <a href="manifest.json">manifest.json</a> (machine-readable list)</li>
</ul>
<div class="grid">
<div class="card"><img src="templates/social/linkedin-post-01-insight-quote.png" alt=""><h3>Social templates</h3></div>
<div class="card"><img src="templates/slides/slide-01-title-sage.png" alt=""><h3>Presentation layouts</h3></div>
<div class="card"><img src="assets/logos/lockup-charcoal.svg" alt=""><h3>Logos and icons</h3></div>
</div>"""
(ROOT / "index.html").write_text(page("DandyLions hub", index), encoding="utf-8")

tpl = "<h1>Template images</h1><p>Real exports from the DandyLions Figma file, served as PNG. Use them as visual examples of layout, colour, type and graphic devices. The text in them is sample text from the Figma file, not guidance on what to write.</p>" + sections_html("templates/", 1) + placeholders_html()
(ROOT / "templates" / "index.html").write_text(page("Template images · DandyLions hub", tpl, 1), encoding="utf-8")

ast = "<h1>Logos, icons and graphics</h1><p>Real brand files from the Figma file and the website repository. SVGs are plain text: open the URL, or the raw.githubusercontent.com link, to read the markup.</p>" + sections_html("assets/", 1)
(ROOT / "assets" / "index.html").write_text(page("Logos, icons and graphics · DandyLions hub", ast, 1), encoding="utf-8")

# tokens page
rows = []
for name, v in TOKENS["color"]["primitives"].items():
    rows.append(f'<tr><td><span class="sw" style="background:{esc(v["hex"])}"></span></td><td>{esc(name)}</td><td><code>{esc(v["hex"])}</code></td><td>{esc(v.get("role",""))}</td></tr>')
other = {k: v for k, v in TOKENS["color"].items() if k != "primitives"}
fam = TOKENS["typography"]["families"]
typ = "".join(f'<tr><td>{esc(k)}</td><td>{esc(v["name"])}</td><td>{esc(", ".join(v["weights"]))}</td><td>{esc(v["use"])}</td><td>{esc(v["fallback"])}</td></tr>' for k, v in fam.items())
scale = "".join(f'<tr><td>{esc(k)}</td><td>{esc(v.get("family"))}</td><td>{esc(v.get("weight"))}</td><td>{esc(v.get("size"))}</td><td>{esc(v.get("lineHeight",""))}</td><td>{esc(v.get("letterSpacing",""))}</td></tr>' for k, v in TOKENS["typography"]["scale"].items())
ds = f"""<h1>Design tokens</h1>
<p>Machine-readable: <a href="tokens.json">tokens.json</a> (curated, read this first) and <a href="css-tokens.json">css-tokens.json</a> (raw CSS custom properties from the website, refreshed by the daily sync). When the website and Figma disagree, the website wins.</p>
<h2>Colour primitives</h2><table><tr><th></th><th>Name</th><th>Hex</th><th>Role</th></tr>{''.join(rows)}</table>
<p class="meta">Themes, accents and semantic colours: see <code>color</code> and <code>themes</code> in tokens.json.</p>
<h2>Type families</h2><table><tr><th></th><th>Family</th><th>Weights</th><th>Use</th><th>Fallback</th></tr>{typ}</table>
<h2>Type scale</h2><table><tr><th>Style</th><th>Family</th><th>Weight</th><th>Size</th><th>Line height</th><th>Tracking</th></tr>{scale}</table>
<h2>Spacing, radius, effects</h2><pre><code>{esc(json.dumps({k: TOKENS[k] for k in ('spacing','radius','effects','motion')}, indent=2, ensure_ascii=False))}</code></pre>"""
(ROOT / "design-system" / "index.html").write_text(page("Design tokens · DandyLions hub", ds, 1), encoding="utf-8")

INSTR = f"""You have read-only access to the DandyLions hub, a public website with the DandyLions design tokens, template images and brand assets.

1. At the start of a task, fetch {BASE}llms-full.txt. It lists the design tokens and every image and asset with its absolute URL, format, size and a visual description.
2. For colours, fonts, sizes and spacing, use {BASE}design-system/tokens.json.
3. For a social post, slide, newsletter or other visual, the matching template images are a good source of inspiration. Open them by URL and borrow from their layout, colour, type and graphic devices, treating them as reference rather than something to copy exactly.
4. For logos and icons, use the files listed under Logos and Icons. SVGs are plain text: fetch the raw.githubusercontent.com URL to read the markup. Use the charcoal versions on ivory and the ivory versions on sage.
5. Where possible, use the real DandyLions logos, icons and graphics from the hub; they're the best starting point. If something you need isn't there, it helps to mention it, since Ruben looks after the hub and can add it.
6. The hub contains no copywriting guidance. The text inside the template images is sample text only."""

pi = f"""<h1>Set up a Claude Project for the DandyLions hub</h1>
<ol>
<li>In the Claude app, create a Project (for example "DandyLions visuals").</li>
<li>Open the Project's instructions and paste the text below.</li>
<li>Turn on web fetch (web search) for the chat, so Claude can open the hub URLs.</li>
</ol>
<h2>Project instructions</h2>
<pre style="white-space:pre-wrap;background:#FBF9F4;border:1px solid #E3DDCE;border-radius:12px;padding:16px">{esc(INSTR)}</pre>"""
(ROOT / "project-instructions.html").write_text(page("Claude setup · DandyLions hub", pi), encoding="utf-8")

# ---------- llms.txt ----------
L = [f"# DandyLions hub", "",
     "> Visual reference for DandyLions: design tokens, real template images (social posts, presentation slides, newsletter, brand guide pages) and brand assets (logos, icons, graphic devices). Read-only, maintained by Ruben Bijker. No copywriting guidance: only how things look.", "",
     f"Everything in one file: {BASE}llms-full.txt", f"Machine-readable list: {BASE}manifest.json", "",
     "## Design tokens", ""]
for t in M["tokens"]:
    L.append(f"- [{t['title']}]({BASE}{t['file']}): {t['description']}")
for sec in M["sections"]:
    L += ["", f"## {sec['title']}", ""]
    for it in sec["items"]:
        extra = f" Raw text: {it['raw_url']}" if it.get("raw_url") else ""
        L.append(f"- [{it['title']}]({it['url']}): {it['format']}, {it['size']}." + (f" {it['format_label']}." if it.get("format_label") else "") + extra)
L += ["", "## Not included (placeholders)", ""] + [f"- {p['title']}: {p['note']}" for p in M["placeholders"]]
L += ["", "## Optional", "", f"- [Claude Project setup]({BASE}project-instructions.html)", f"- [Template gallery]({BASE}templates/)", f"- [Logos and icons gallery]({BASE}assets/)", ""]
(ROOT / "llms.txt").write_text("\n".join(L), encoding="utf-8")

# ---------- llms-full.txt ----------
F = [f"# DandyLions hub (full)", "",
     f"Source: {BASE} (public, read-only, maintained by Ruben Bijker). Updated {M['updated']}.",
     "Contents: design tokens, template images and brand assets. There is no copywriting guidance in this hub. The text inside template images is sample text from the Figma file.", "",
     "## How to use (for Claude)", "", INSTR, "",
     "## Design tokens: tokens.json (curated)", "", f"URL: {BASE}design-system/tokens.json", "", "```json",
     (ROOT / "design-system" / "tokens.json").read_text(encoding="utf-8").strip(), "```", "",
     "## Design tokens: css-tokens.json (raw snapshot of the website's CSS variables, synced daily)", "", f"URL: {BASE}design-system/css-tokens.json", "", "```json",
     (ROOT / "design-system" / "css-tokens.json").read_text(encoding="utf-8").strip(), "```", ""]
for sec in M["sections"]:
    F += [f"## {sec['title']}", ""]
    if sec.get("note"):
        F += [sec["note"], ""]
    for it in sec["items"]:
        F.append(f"### {it['title']}")
        F.append(f"- URL: {it['url']}")
        if it.get("raw_url"):
            F.append(f"- Raw SVG text: {it['raw_url']}")
        F.append(f"- Format: {it['format']}, {it['size']}" + (f" ({it['format_label']})" if it.get("format_label") else ""))
        if sec["id"] != "icons":
            F.append(f"- Looks like: {it['description']}")
        if it.get("background"):
            F.append(f"- Background: {it['background']}")
            F.append(f"- Use: {it['use']}")
        F.append(f"- Source: {it['source']}")
        if sec["id"] == "icons":
            F += ["", "```svg", (ROOT / it["file"]).read_text(encoding="utf-8").strip(), "```"]
        F.append("")
F += ["## Not included (placeholders)", ""] + [f"- {p['title']}: {p['note']}" for p in M["placeholders"]] + [""]
(ROOT / "llms-full.txt").write_text("\n".join(F), encoding="utf-8")
print("built pages, llms.txt and llms-full.txt for", sum(c.values()), "files")
