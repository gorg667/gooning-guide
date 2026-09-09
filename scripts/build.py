#!/usr/bin/env python3
"""
Build script: concatenates docs/chapters/*.md -> GUIDE.md
and renders a static website into site/.

Usage:  python3 scripts/build.py
Deps:   pip install markdown pymdown-extensions
"""
import glob
import html
import json
import os
import re
import shutil
import sys

import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH_DIR = os.path.join(ROOT, "docs", "chapters")
SITE = os.path.join(ROOT, "site")
TEMPLATE_DIR = os.path.join(ROOT, "scripts", "template")

SITE_TITLE = "The Complete Guide to Male Solo Sexuality"
SITE_TAGLINE = "An evidence-informed handbook on masturbation mastery, pleasure, health, and self-knowledge"

MD_EXT = [
    "tables",
    "fenced_code",
    "toc",
    "attr_list",
    "md_in_html",
    "sane_lists",
    "smarty",
    "pymdownx.superfences",
    "pymdownx.betterem",
]
MD_CFG = {"toc": {"permalink": "#", "toc_depth": "2-3"}}


def slug(s):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s


def load_chapters():
    files = sorted(glob.glob(os.path.join(CH_DIR, "*.md")))
    chapters = []
    for f in files:
        base = os.path.basename(f)
        num = base.split("-")[0]
        with open(f, encoding="utf-8") as fh:
            text = fh.read()
        m = re.search(r"^# (.+)$", text, re.M)
        title = m.group(1).strip() if m else base
        # Strip "Chapter N — " prefix for nav display, keep full for page
        short = re.sub(r"^Chapter \d+ — ", "", title)
        chapters.append(
            {
                "num": num,
                "file": f,
                "title": title,
                "short": short,
                "slug": f"{num}-{slug(short)[:50]}",
                "md": text,
            }
        )
    return chapters


def build_guide_md(chapters):
    parts = []
    for ch in chapters:
        parts.append(ch["md"].rstrip() + "\n")
    out = "\n\n---\n\n".join(parts)
    with open(os.path.join(ROOT, "GUIDE.md"), "w", encoding="utf-8") as fh:
        fh.write(out)
    words = len(re.findall(r"\w+", out))
    return words


def render_md(text):
    md = markdown.Markdown(extensions=MD_EXT, extension_configs=MD_CFG)
    body = md.convert(text)
    toc = md.toc
    # Style evidence emoji tags
    body = body.replace("🟢", '<span class="ev ev-strong" title="Strong evidence">🟢</span>')
    body = body.replace("🟡", '<span class="ev ev-mod" title="Moderate evidence">🟡</span>')
    body = body.replace("🟠", '<span class="ev ev-weak" title="Weak / anecdotal">🟠</span>')
    body = body.replace("🔴", '<span class="ev ev-contra" title="Contradicted">🔴</span>')
    # Cross-reference chapter links: "(Ch. 4, 15)" or "Chapter 12" -> leave as text; simple.
    return body, toc


def read_template(name):
    with open(os.path.join(TEMPLATE_DIR, name), encoding="utf-8") as fh:
        return fh.read()


def nav_html(chapters, current=None):
    items = []
    for ch in chapters:
        cls = ' class="active"' if current and ch["slug"] == current else ""
        label = ch["short"] if ch["num"] != "00" else "Start Here"
        num = "" if ch["num"] == "00" else f'<span class="num">{int(ch["num"])}</span>'
        items.append(f'<li{cls}><a href="{ch["slug"]}.html">{num}{html.escape(label)}</a></li>')
    return "\n".join(items)


def build_site(chapters):
    os.makedirs(SITE, exist_ok=True)
    # static assets
    for asset in ("style.css", "app.js"):
        shutil.copy(os.path.join(TEMPLATE_DIR, asset), os.path.join(SITE, asset))
    page_t = read_template("page.html")
    index_t = read_template("index.html")

    search_index = []
    for i, ch in enumerate(chapters):
        body, toc = render_md(ch["md"])
        prev_ch = chapters[i - 1] if i > 0 else None
        next_ch = chapters[i + 1] if i < len(chapters) - 1 else None
        prev_html = (
            f'<a class="pager prev" href="{prev_ch["slug"]}.html">← {html.escape(prev_ch["short"])}</a>'
            if prev_ch
            else "<span></span>"
        )
        next_html = (
            f'<a class="pager next" href="{next_ch["slug"]}.html">{html.escape(next_ch["short"])} →</a>'
            if next_ch
            else "<span></span>"
        )
        page = (
            page_t.replace("{{SITE_TITLE}}", html.escape(SITE_TITLE))
            .replace("{{TITLE}}", html.escape(ch["title"]))
            .replace("{{NAV}}", nav_html(chapters, ch["slug"]))
            .replace("{{TOC}}", toc)
            .replace("{{BODY}}", body)
            .replace("{{PREV}}", prev_html)
            .replace("{{NEXT}}", next_html)
        )
        with open(os.path.join(SITE, ch["slug"] + ".html"), "w", encoding="utf-8") as fh:
            fh.write(page)

        # search index: split by h2 sections
        plain = re.sub(r"<[^>]+>", " ", body)
        plain = html.unescape(re.sub(r"\s+", " ", plain))
        sections = re.split(r"(?=<h2 )", body)
        for sec in sections:
            hm = re.search(r'<h2 id="([^"]+)">(.*?)</h2>', sec, re.S)
            if not hm:
                continue
            hid = hm.group(1)
            htitle = re.sub(r"<[^>]+>", "", hm.group(2)).replace("#", "").strip()
            stext = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", sec)))
            search_index.append(
                {
                    "c": ch["short"],
                    "u": f'{ch["slug"]}.html#{hid}',
                    "t": htitle,
                    "x": stext[:600],
                }
            )

    with open(os.path.join(SITE, "search.json"), "w", encoding="utf-8") as fh:
        json.dump(search_index, fh, ensure_ascii=False)

    # index page: chapter cards
    cards = []
    for ch in chapters:
        if ch["num"] == "00":
            continue
        # first paragraph after title as blurb
        paras = [p for p in ch["md"].split("\n\n") if p and not p.startswith("#")]
        blurb = paras[0] if paras else ""
        blurb = re.sub(r"[*_`\[\]]", "", blurb)
        blurb = re.sub(r"\(http[^)]*\)", "", blurb)
        if len(blurb) > 220:
            blurb = blurb[:217].rsplit(" ", 1)[0] + "…"
        cards.append(
            f'<a class="card" href="{ch["slug"]}.html"><div class="card-num">{int(ch["num"])}</div>'
            f'<h3>{html.escape(ch["short"])}</h3><p>{html.escape(blurb)}</p></a>'
        )
    total_words = sum(len(re.findall(r"\w+", c["md"])) for c in chapters)
    index = (
        index_t.replace("{{SITE_TITLE}}", html.escape(SITE_TITLE))
        .replace("{{TAGLINE}}", html.escape(SITE_TAGLINE))
        .replace("{{NAV}}", nav_html(chapters))
        .replace("{{CARDS}}", "\n".join(cards))
        .replace("{{WORDS}}", f"{total_words:,}")
        .replace("{{NCHAPTERS}}", str(len(chapters) - 1))
        .replace("{{FIRST}}", chapters[0]["slug"] + ".html")
    )
    with open(os.path.join(SITE, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(index)
    # copy the single-file guide into the site for download
    shutil.copy(os.path.join(ROOT, "GUIDE.md"), os.path.join(SITE, "GUIDE.md"))
    # .nojekyll for GitHub Pages
    open(os.path.join(SITE, ".nojekyll"), "w").close()


def main():
    chapters = load_chapters()
    words = build_guide_md(chapters)
    build_site(chapters)
    print(f"Built GUIDE.md ({words:,} words) and site/ ({len(chapters)} pages)")


if __name__ == "__main__":
    main()
