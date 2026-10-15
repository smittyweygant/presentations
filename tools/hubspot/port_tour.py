#!/usr/bin/env python3
"""Publish the console tour: the akka.io/platform/tour page and the home-page band.

Sources live in website/console-tour/. index.html holds the tour page between its
tour:start/tour:end markers, home-band.html holds the band between band:start/band:end,
and tour.js holds the screen list both of them read. The build inlines tour.js into each,
points the images at the file manager and the band's links at /platform/tour.

    python tools/hubspot/port_tour.py                 # build into scratchpad/hs-out/
    python tools/hubspot/port_tour.py --images        # copy the WebP shots from ai-console, check
                                                      # tour.js against them, upload
    python tools/hubspot/port_tour.py --push          # PUT template + module, publish
                                                      # /platform/tour, re-render home
    python tools/hubspot/port_tour.py --home-layout   # add the band to the home page and
                                                      # set the band order (one time)

Title or caption changes in tour.js need only --push. The token comes from the
gitignored scratchpad/.hs_env.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "website" / "console-tour"
SHOTS_OUT = Path.home() / "ai-console" / "scripts" / "screenshots" / "out"
OUT = ROOT / "scratchpad" / "hs-out"
API = "https://api.hubapi.com"

TOUR_URL = "/platform/tour"
TEMPLATE = "custom-templates/platform-tour.html"
MODULE = "AKKA-2024/modules/Home Tour Band.module"
IMG_FOLDER_PARENT = 180267575306          # file manager /website
IMG_FOLDER = "platform-tour"
IMG_BASE = "https://akka.io/hubfs/website/platform-tour/"
HOME_PAGE_ID = "210655290656"
BAND_WIDGET = "widget_home_tour_band"

PAGE = {
    "slug": "platform/tour",
    "label": "Platform tour",
    "title": "An Integrated Platform | Akka",
    "description": "Orchestration · Guardrails · Evaluations · Routing · Inference · Training · Streaming",
}

# Bands of the home page's first section, top to bottom, by widget name. The four tiles
# and the buttons sit in later sections and stay after these.
HOME_ORDER = [
    "widget_1775678949913",   # hero
    BAND_WIDGET,              # tour band
    "widget_1775684903151",   # Manulife
    "widget_1775685280475",   # Deloitte
    "widget_1775685349763",   # Dojo
    "widget_home_cost_band",  # AI Spend calculator
    "widget_1775685236442",   # Swiggy
    "widget_1775685320626",   # John Deere
    "widget_1775685145617",   # Tubi
]

SHELL = """<!--
    templateType: page
    isAvailableForNewContent: false
    label: {label}
-->
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" href="https://akka.io/favicon.ico" type="image/x-icon">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="stylesheet" href="https://akka.io/hubfs/hub_generated/template_assets/1/180483679747/1783700344298/template_Plugin.min.css">
    <link rel="stylesheet" href="https://akka.io/hubfs/hub_generated/template_assets/1/177749484047/1783700345343/template_main.css">
    <link rel="stylesheet" href="https://akka.io/hubfs/hub_generated/template_assets/1/177749412157/1785440087003/template_theme-overrides.css">
    <link rel="stylesheet" href="https://akka.io/hubfs/hub_generated/template_assets/1/177760109709/1783700345998/template_Dev1.min.css">
    {{{{ standard_header_includes }}}}
    <style>
      /* The tour paints black inside its wrapper; the strip behind the header and footer
         takes it here. The header is fixed and the theme clears it with body padding-top. */
      body {{ background: #000000; }}
    </style>
  </head>
  <body>
    {{% global_partial path="AKKA-2024/templates/partials/header-april.html" %}}

{body}

    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script>
    <script src="https://akka.io/hubfs/hub_generated/template_assets/1/177749484049/1783700343576/template_main.min.js"></script>
    {{% global_partial path="AKKA-2024/templates/partials/footer.html" %}}
    {{{{ standard_footer_includes }}}}
  </body>
</html>
"""

MODULE_HEADER = """<!-- Home tour band: the console screenshots playing in order on the home page, with
     links into akka.io/platform/tour. Built by tools/hubspot/port_tour.py from
     website/console-tour/home-band.html and tour.js; edit those and re-run the port
     rather than editing this module. Every class is scoped under #ct-band. -->
"""

MODULE_META = {
    "global": False,
    "content_types": ["LANDING_PAGE", "SITE_PAGE"],
    "host_template_types": ["PAGE"],
    "label": "Home Tour Band",
    "is_available_for_new_content": True,
}


def block(path, start, end):
    s = path.read_text(encoding="utf-8")
    return s[s.index(start):s.index(end)]


def inline_tour(html):
    js = (SRC / "tour.js").read_text(encoding="utf-8")
    script = '<script>\nwindow.TOUR_IMG_BASE = "%s";\n%s</script>' % (IMG_BASE, js)
    if html.count('<script src="tour.js"></script>') != 1:
        sys.exit("expected one tour.js script tag to inline")
    return html.replace('<script src="tour.js"></script>', script)


def no_hubl(name, text):
    # Both outputs are rendered as HubL; a stray delimiter in CSS or JS would be parsed.
    for d in ("{{", "{%", "{#"):
        if d in text:
            sys.exit(f"{name}: HubL delimiter {d!r} in content")


def build():
    page_body = inline_tour(block(SRC / "index.html", "<!-- tour:start", "<!-- tour:end -->"))
    band = inline_tour(block(SRC / "home-band.html", "<!-- band:start", "<!-- band:end -->"))
    band = band.replace('href="index.html', 'href="' + TOUR_URL)
    # The total is in the markup for crawlers; the band script sets the same value from TOUR.screens.
    screens = len(re.findall(r'^\s*\{ id: "', (SRC / "tour.js").read_text(encoding="utf-8"), re.M))
    band, n = re.subn(r'(<span id="ct-total">)\d+(</span>)', rf'\g<1>{screens}\g<2>', band)
    if n != 1:
        sys.exit("expected one ct-total span in the band")
    if 'href="index.html' in band:
        sys.exit("band still links to index.html")
    no_hubl("tour page", page_body)
    no_hubl("band", band)

    OUT.mkdir(parents=True, exist_ok=True)
    tpl = OUT / "platform-tour.html"
    tpl.write_text(SHELL.format(body=page_body, **PAGE), encoding="utf-8")
    mod = OUT / "home-tour-band.module.html"
    mod.write_text(MODULE_HEADER + band, encoding="utf-8")
    print("built", tpl, "and", mod)
    return tpl, mod


_TOKEN = []


def token():
    if not _TOKEN:
        env = (ROOT / "scratchpad" / ".hs_env").read_text(encoding="utf-8")
        for line in env.splitlines():
            if line.startswith("HUBSPOT_TOKEN="):
                _TOKEN.append(line.split("=", 1)[1].strip())
        if not _TOKEN:
            sys.exit("HUBSPOT_TOKEN not found in scratchpad/.hs_env")
    return _TOKEN[0]


def _curl(args):
    r = subprocess.run(["curl", "-s", "-H", "Authorization: Bearer " + token()] + args,
                       capture_output=True)
    return r.stdout.decode("utf-8", errors="strict") if r.stdout else ""


def _json_call(method, path, body):
    # Bodies go through a file: the page description carries middle dots, and a
    # shell-quoted body holding one arrives mojibaked.
    p = ROOT / "scratchpad" / ".hs_body.json"
    p.write_text(json.dumps(body, ensure_ascii=True), encoding="utf-8")
    try:
        return _curl(["-X", method, "-H", "Content-Type: application/json",
                      "--data-binary", "@" + str(p), API + path])
    finally:
        p.unlink()


def put_source(remote, local):
    url_path = remote.replace(" ", "%20")
    for env in ("draft", "published"):
        code = subprocess.run(
            ["curl", "-s", "-o", os.devnull, "-w", "%{http_code}", "-X", "PUT",
             f"{API}/cms/v3/source-code/{env}/content/{url_path}",
             "-H", "Authorization: Bearer " + token(), "-F", f"file=@{local}"],
            capture_output=True, text=True).stdout.strip()
        if code not in ("200", "201"):
            sys.exit(f"PUT {remote} ({env}) returned {code}")
    print("  put", remote)


def put_module(module_html):
    files = {"meta.json": json.dumps(MODULE_META, indent=2), "fields.json": "[]",
             "module.css": "", "module.js": ""}
    for name, text in files.items():
        p = OUT / ("home-tour-band." + name)
        p.write_text(text, encoding="utf-8")
        put_source(f"{MODULE}/{name}", p)
    put_source(f"{MODULE}/module.html", module_html)


def module_id():
    meta = json.loads(_curl([f"{API}/cms/v3/source-code/published/content/"
                             + (MODULE + "/meta.json").replace(" ", "%20")]))
    if not meta.get("module_id"):
        sys.exit(f"{MODULE} has no module_id yet: {meta}")
    return meta["module_id"]


def push_live(pid, label):
    _json_call("POST", f"/cms/v3/pages/site-pages/{pid}/draft/push-live", {})
    print("  pushed live", label, pid)


def publish_page():
    found = json.loads(_curl([API + "/cms/v3/pages/site-pages?limit=5&slug=" + PAGE["slug"]]))
    pid = next((p["id"] for p in found.get("results", []) if p["slug"] == PAGE["slug"]), None)
    body = {"name": PAGE["label"], "slug": PAGE["slug"], "templatePath": TEMPLATE,
            "htmlTitle": PAGE["title"], "metaDescription": PAGE["description"],
            "state": "PUBLISHED", "publishImmediately": True,
            "language": "en", "subcategory": "site_page"}
    if pid:
        r = json.loads(_json_call("PATCH", "/cms/v3/pages/site-pages/" + pid, body))
    else:
        r = json.loads(_json_call("POST", "/cms/v3/pages/site-pages", body))
        pid = r.get("id")
    if not pid:
        sys.exit(f"page publish failed: {str(r)[:300]}")
    push_live(pid, "https://akka.io/" + PAGE["slug"])


def home_draft_matches_live():
    # push-live publishes the whole draft, so an edit someone left unpublished in HubSpot
    # would go live with ours. Stop instead.
    live = json.loads(_curl([f"{API}/cms/v3/pages/site-pages/{HOME_PAGE_ID}"]))
    draft = json.loads(_curl([f"{API}/cms/v3/pages/site-pages/{HOME_PAGE_ID}/draft"]))
    keys = ("layoutSections", "widgets", "widgetContainers", "htmlTitle", "metaDescription", "templatePath")
    differ = [k for k in keys if live.get(k) != draft.get(k)]
    if differ:
        sys.exit(f"home page has unpublished draft changes in {differ}; publish or discard them first")
    return live


def rerender_home():
    # A module change does not reliably invalidate the rendered page. Writing the title
    # back at its current value marks the page dirty, and push-live renders it again.
    page = home_draft_matches_live()
    _json_call("PATCH", f"/cms/v3/pages/site-pages/{HOME_PAGE_ID}", {"htmlTitle": page["htmlTitle"]})
    push_live(HOME_PAGE_ID, "home page")


def sync_shots():
    """Copy the capture run's WebP output into img/ and check every screen tour.js names has both sizes."""
    dest = SRC / "img"
    for f in SHOTS_OUT.glob("*.webp"):
        shutil.copyfile(f, dest / f.name)
    ids = sorted(set(re.findall(r'id:\s*"([^"]+)"', (SRC / "tour.js").read_text(encoding="utf-8"))))
    missing = [f"{i}-{s}.webp" for i in ids for s in ("1280", "2560") if not (dest / f"{i}-{s}.webp").exists()]
    if missing:
        sys.exit(f"tour.js screens without images: {missing}")
    return ids


def upload_images():
    # img/ also holds captures tour.js does not use; those stay local. Uploads are public
    # and indexable, and a screen dropped from tour.js stays in the file manager until
    # deleted there.
    ids = sync_shots()
    found = json.loads(_curl([f"{API}/files/v3/folders/search?path=/website/{IMG_FOLDER}&limit=5"]))
    fid = next((f["id"] for f in found.get("results", []) if f.get("path") == "/website/" + IMG_FOLDER), None)
    if not fid:
        r = json.loads(_json_call("POST", "/files/v3/folders",
                                  {"name": IMG_FOLDER, "parentFolderId": IMG_FOLDER_PARENT}))
        fid = r.get("id") or sys.exit(f"folder create failed: {r}")
    opts = json.dumps({"access": "PUBLIC_INDEXABLE", "overwrite": True})
    files = [SRC / "img" / f"{i}-{s}.webp" for i in ids for s in ("1280", "2560")]
    for f in files:
        r = json.loads(_curl(["-X", "POST", API + "/files/v3/files", "-F", f"file=@{f}",
                              "-F", f"folderId={fid}", "-F", f"fileName={f.stem}",
                              "-F", f"options={opts}"]))
        if not r.get("url"):
            sys.exit(f"upload failed for {f.name}: {str(r)[:300]}")
    print(f"  uploaded {len(files)} images to folder {fid}")


def home_layout():
    home_draft_matches_live()
    draft = json.loads(_curl([f"{API}/cms/v3/pages/site-pages/{HOME_PAGE_ID}/draft"]))
    backup = OUT / time.strftime(f"home-page-{HOME_PAGE_ID}-%Y%m%d-%H%M%S.json")
    OUT.mkdir(parents=True, exist_ok=True)
    backup.write_text(json.dumps(draft, indent=1, ensure_ascii=False), encoding="utf-8")
    print("  backed up the home page draft to", backup)

    sections = draft["layoutSections"]
    cell = sections["dnd_area"]["rows"][0]["0"]
    by_name = {row["0"]["name"]: row for row in cell["rows"]}
    if BAND_WIDGET not in by_name:
        by_name[BAND_WIDGET] = {"0": {
            "cells": [], "cssClass": "", "cssId": "", "cssStyle": "", "label": "Home Tour Band",
            "name": BAND_WIDGET,
            "params": {"css_class": "dnd-module", "module_id": module_id(), "schema_version": 2},
            "rowMetaData": [], "rows": [], "type": "custom_widget", "w": 12, "x": 0}}
    if set(by_name) != set(HOME_ORDER):
        sys.exit(f"home bands differ from HOME_ORDER: {sorted(set(by_name) ^ set(HOME_ORDER))}")
    cell["rows"] = [by_name[n] for n in HOME_ORDER]
    cell["rowMetaData"] = [{"cssClass": "dnd-row"} for _ in HOME_ORDER]

    r = json.loads(_json_call("PATCH", f"/cms/v3/pages/site-pages/{HOME_PAGE_ID}/draft",
                              {"layoutSections": sections}))
    got = [row["0"]["name"] for row in r["layoutSections"]["dnd_area"]["rows"][0]["0"]["rows"]]
    if got != HOME_ORDER:
        sys.exit(f"draft order is {got}")
    push_live(HOME_PAGE_ID, "home page")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--images", action="store_true")
    ap.add_argument("--push", action="store_true")
    ap.add_argument("--home-layout", action="store_true")
    a = ap.parse_args()
    tpl, mod = build()
    if a.images:
        upload_images()
    if a.push:
        put_source(TEMPLATE, tpl)
        put_module(mod)
        publish_page()
        if not a.home_layout:
            rerender_home()
    if a.home_layout:
        home_layout()
