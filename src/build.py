"""Build otownwc.com.

    python3 src/build.py

Regenerates the six HTML pages at the repo root from the sources in src/.
Commit and push the result; the GitHub Pages workflow deploys main.

Sources
    src/home.html       the home page, and the <style> block every page shares
    src/build_pages.py  the five sub-pages (about, contact, sponsors, store,
                        handbook) and the shared nav and footer
    src/practices.json  reference copy of the practice calendar data, which is
                        embedded in home.html as the PRACTICES object

Do not hand-edit the HTML at the repo root - it is generated and any change
there is lost on the next build.

Why the sources look like fragments
    src/home.html starts at <meta charset> with no <!doctype>, <html> or
    <body>. The site began life as Claude Artifacts, whose runtime supplies
    that skeleton itself. GitHub Pages serves files raw, so wrap_document()
    below adds the skeleton. Without it the live site rendered in quirks mode
    with no viewport meta, which made phones lay the page out at ~980px and
    scale the whole thing down.

Cross-page links
    Written in the sources as {{ABOUT_URL}} / {ABOUT_URL} placeholders and
    resolved here to plain filenames. Both spellings occur because
    build_pages.py emits some templates from f-strings, which eat one level
    of braces.
"""
import pathlib
import re
import subprocess
import sys

SRC = pathlib.Path(__file__).parent
REPO = SRC.parent

URLS = {
    "HOME_URL": "index.html",
    "ABOUT_URL": "about.html",
    "SPONSORS_URL": "sponsors.html",
    "STORE_URL": "store.html",
    "CONTACT_URL": "contact.html",
    "HANDBOOK_URL": "handbook.html",
}

# placeholder in the sources -> shared asset file
IMAGES = {
    "BGTEX_B64": "bg-texture.webp",
    "STEEL2_B64": "steel-texture.webp",
    "BADGE_B64": "badge.webp",
    "MASCOT_B64": "mascot.webp",
}

PAGES = {
    "home.html": "index.html",
    "pages/about.html": "about.html",
    "pages/contact.html": "contact.html",
    "pages/sponsors.html": "sponsors.html",
    "pages/store.html": "store.html",
    "pages/handbook.html": "handbook.html",
}


def sub_urls(html):
    # double braces first: replacing {TOKEN} first would corrupt {{TOKEN}}
    for token, value in URLS.items():
        html = html.replace("{{" + token + "}}", value)
    for token, value in URLS.items():
        html = html.replace("{" + token + "}", value)
    return html


def wrap_document(html):
    """Give the fragment a real document shell. See the module docstring."""
    marker = "</style>"
    idx = html.index(marker) + len(marker)
    head, body = html[:idx].strip(), html[idx:].strip()
    if 'name="viewport"' not in head:
        viewport = ('<meta name="viewport" content="width=device-width, '
                    'initial-scale=1">')
        charset = '<meta charset="UTF-8">'
        if head.startswith(charset):           # charset stays first in the head
            head = charset + "\n" + viewport + head[len(charset):]
        else:
            head = viewport + "\n" + head
    return ("<!DOCTYPE html>\n"
            '<html lang="en">\n'
            "<head>\n" + head + "\n</head>\n"
            "<body>\n" + body + "\n</body>\n"
            "</html>\n")


def check(name, html):
    leftover = re.findall(r"__[A-Z0-9_]+__|\{\{?[A-Z_]+\}\}?", html)
    if leftover:
        sys.exit(f"ERROR: {name} has unresolved placeholders: {sorted(set(leftover))}")
    if 'href="#"' in html:
        sys.exit(f"ERROR: {name} has a dead href='#' - use pending_link() instead")
    if not html.lstrip().lower().startswith("<!doctype html>"):
        sys.exit(f"ERROR: {name} has no doctype - it would render in quirks mode")
    if 'name="viewport"' not in html:
        sys.exit(f"ERROR: {name} has no viewport meta - mobile would render shrunken")


def main():
    subprocess.run([sys.executable, "build_pages.py"], cwd=SRC, check=True)

    for src_name, out_name in PAGES.items():
        html = (SRC / src_name).read_text(encoding="utf-8")
        html = sub_urls(html)
        for token, fname in IMAGES.items():
            html = html.replace(f"data:image/webp;base64,__{token}__", f"assets/{fname}")
        html = wrap_document(html)
        check(out_name, html)
        (REPO / out_name).write_text(html, encoding="utf-8")
        print(f"  {out_name:15s} {len(html):>7,} bytes")

    print("build ok")


if __name__ == "__main__":
    main()
