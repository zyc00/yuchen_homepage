#!/usr/bin/env python3
"""Generate the static homepage from its templates and publication data.

Uses only Python's standard library. Run from any directory:
  python3 scripts/build.py
  python3 scripts/build.py --check
"""

import argparse
from html import escape
import json
import math
from pathlib import Path
import re
from string import Template
from textwrap import indent
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parent.parent
OWNER_NAME = "Yuchen Zhou"


def text(value, field):
    """Require plain text; HTML is escaped when rendered."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be a nonempty string")
    return value.strip()


def url(value, field):
    value = text(value, field)
    parsed = urlsplit(value)
    if parsed.scheme:
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError(f"{field} must be an HTTP(S) URL or a local file")
    else:
        candidate = (ROOT / unquote(parsed.path)).resolve()
        if parsed.netloc or not candidate.is_relative_to(ROOT) or not candidate.is_file():
            raise ValueError(f"{field} points to a missing or invalid local file: {value}")
    return escape(value, quote=True)


def render_authors(authors):
    if not isinstance(authors, list) or not authors:
        raise ValueError("authors must be a nonempty list of names")
    rendered = []
    for author in authors:
        author = text(author, "author")
        equal = author.endswith("*")
        name = text(author[:-1] if equal else author, "author name")
        label = escape(name)
        if name == OWNER_NAME:
            label = f"<strong>{label}</strong>"
        rendered.append(label + ("<sup>*</sup>" if equal else ""))
    return ", ".join(rendered)


def render_media(media, name):
    if media is None:
        return ""
    if not isinstance(media, dict):
        raise ValueError("media must be an object")
    src = url(media.get("src"), "media.src")
    alt = escape(text(media.get("alt"), "media.alt"), quote=True)
    if media.get("type") == "image":
        dimensions = ""
        for key in ("width", "height"):
            if key in media:
                if type(media[key]) is not int or media[key] <= 0:
                    raise ValueError(f"media.{key} must be a positive integer")
                dimensions += f' {key}="{media[key]}"'
        label = escape(text(media.get("label", f"View the full {name} figure"), "media.label"))
        return (
            f'<a class="publication-figure" href="{src}" aria-label="{label}">\n'
            f'  <img src="{src}"{dimensions} loading="lazy" decoding="async" alt="{alt}" />\n'
            '</a>'
        )
    if media.get("type") == "video":
        start = media.get("start", 0)
        if type(start) not in (int, float) or not math.isfinite(start) or start < 0:
            raise ValueError("media.start must be a nonnegative number of seconds")
        video_src = f"{src}#t={start:g}" if start else src
        return (
            '<div class="publication-figure publication-video">\n'
            f'  <video autoplay muted loop playsinline preload="metadata" aria-label="{alt}">\n'
            f'    <source src="{video_src}" type="video/mp4" />\n'
            f'    <a href="{src}">Watch the {escape(name)} demo</a>.\n'
            '  </video>\n'
            '</div>'
        )
    raise ValueError("media.type must be 'image' or 'video'")


def render_publications(papers):
    if not isinstance(papers, list):
        raise ValueError("publications.json must contain a list of papers")
    template = Template((ROOT / "templates/publication.html").read_text(encoding="utf-8"))
    articles = []
    ids = set()
    equal_contribution = False
    for number, paper in enumerate(papers, start=1):
        try:
            if not isinstance(paper, dict):
                raise ValueError("each paper must be an object")
            paper_id = text(paper.get("id"), "id")
            if not re.fullmatch(r"[a-z][a-z0-9-]*", paper_id) or paper_id in ids:
                raise ValueError("id must be unique, using lowercase letters, digits, and hyphens")
            ids.add(paper_id)
            name = text(paper.get("name"), "name")
            title = text(paper.get("title"), "title")
            authors = render_authors(paper.get("authors"))
            equal_contribution |= "<sup>*</sup>" in authors

            links = paper.get("links")
            if not isinstance(links, dict) or not links.get("Paper"):
                raise ValueError("links must contain a Paper URL")
            resources = [
                f'<li><a href="{url(href, f"links.{label}")}">{escape(text(label, "link label"))}</a></li>'
                for label, href in links.items()
            ]
            venue = paper.get("venue")
            if not isinstance(venue, dict):
                raise ValueError("venue must contain a name and an optional URL")
            venue_html = escape(text(venue.get("name"), "venue.name"))
            if venue.get("url"):
                venue_html = f'<a href="{url(venue["url"], "venue.url")}">{venue_html}</a>'

            media = render_media(paper.get("media"), name)
            articles.append(template.substitute(
                classes="publication" if media else "publication publication-text-only",
                id=paper_id,
                name=escape(name),
                title=escape(title),
                title_url=url(links.get("Project", links["Paper"]), "title link"),
                authors=authors,
                venue=venue_html,
                media=media.replace("\n", "\n  "),
                links="\n      ".join(resources),
            ).strip())
        except ValueError as error:
            raise ValueError(f"Paper {number}: {error}") from error

    note = '<p class="publication-note">* Equal contribution.</p>' if equal_contribution else ""
    return "\n\n".join(articles), note


def render_site(papers):
    page = (ROOT / "templates/index.html").read_text(encoding="utf-8")
    publications, note = render_publications(papers)
    for marker, content, spaces in (
        ("<!-- PUBLICATIONS -->", publications, 12),
        ("<!-- CONTRIBUTION_NOTE -->", note, 10),
    ):
        if page.count(marker) != 1:
            raise ValueError(f"templates/index.html must contain exactly one {marker}")
        page = page.replace(marker, indent(content, " " * spaces))
    return page


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="check whether index.html is up to date without writing it")
    args = parser.parse_args()
    try:
        papers = json.loads((ROOT / "data/publications.json").read_text(encoding="utf-8"))
        rendered = render_site(papers)
    except (ValueError, OSError) as error:
        parser.exit(1, f"Build failed: {error}\n")
    output = ROOT / "index.html"
    current = output.read_text(encoding="utf-8") if output.exists() else None
    if args.check:
        if current != rendered:
            parser.exit(1, "index.html is out of date. Run: python3 scripts/build.py\n")
        print("index.html is up to date.")
    else:
        if current != rendered:
            output.write_text(rendered, encoding="utf-8")
        print(f"Built index.html with {len(papers)} publications.")


if __name__ == "__main__":
    main()
