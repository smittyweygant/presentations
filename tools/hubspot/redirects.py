#!/usr/bin/env python3
"""Create the akka.io 301s for retired paths: the old get-started pages go to /install, and the
listing pages of the unpublished benchmark and staging blogs go to /blog, and an old
customer-story post with no story page goes to /customers.

    python tools/hubspot/redirects.py          # list each route, the redirect HubSpot has for it, and what it serves
    python tools/hubspot/redirects.py --push   # create the redirects that are missing

Each redirect matches the full URL, so /get-started/contact and /get-started/learn are not
affected. isOnlyAfterNotFound is false because live pages still sit at these paths and the
redirect has to win over them. The token comes from the gitignored scratchpad/.hs_env.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from port_tour import _json_call, _curl, API  # noqa: E402

INSTALL = "https://akka.io/install"
BUILD_COPIES = ["371439950605", "371466225041", "371497059511", "371500019502", "385085886788",
                "385091434243", "407568999561", "430650522387", "440048776232", "440050064267",
                "441074622623", "443838715056"]
ROUTES = {
    "/get-started": INSTALL,
    "/get-started/build": INSTALL,
    **{f"/get-started/build/{n}": INSTALL for n in BUILD_COPIES},
    "/llms-all.txt": "https://akka.io/llms-full.txt",
    "/akka-performance-benchmark": "https://akka.io/blog",
    "/akka-blog-staging": "https://akka.io/blog",
    "/customer-stories/scalable-real-time-event-manager-based-on-akka-streams-and-a-highly-reliable-scalable-and-unified-interface-for-payment-products":
        "https://akka.io/customers",
}


def existing():
    found, after = {}, None
    while True:
        q = "?limit=100" + (f"&after={after}" if after else "")
        r = json.loads(_curl([f"{API}/cms/v3/url-redirects{q}"]))
        for x in r.get("results", []):
            path = x["routePrefix"].split("akka.io", 1)[-1] if "akka.io" in x["routePrefix"] else None
            if path in ROUTES:
                found[path] = x
        after = (r.get("paging") or {}).get("next", {}).get("after")
        if not after:
            return found


def served(path):
    # One HEAD per route without following redirects; akka.io rate-limits bursts.
    out = subprocess.run(["curl", "-s", "-o", "/dev/null", "-I", "-A", "Mozilla/5.0",
                          "-w", "%{http_code} %{redirect_url}", "https://akka.io" + path],
                         capture_output=True, text=True).stdout
    return out.strip()


def report(found):
    for path, dest in ROUTES.items():
        have = found.get(path)
        state = (f"redirect {have['redirectStyle']} -> {have['destination']}" if have else "no redirect")
        print(f"{path:<36} want 301 -> {dest:<32} {state:<52} serves {served(path)}")


def push(found):
    for path, dest in ROUTES.items():
        if path in found:
            if found[path]["destination"] != dest:
                print(f"  {path} already redirects to {found[path]['destination']}; left as is")
            continue
        body = {"routePrefix": "http://akka.io" + path, "destination": dest, "redirectStyle": 301,
                "isOnlyAfterNotFound": False, "isMatchFullUrl": True, "isMatchQueryString": False,
                "isPattern": False, "isTrailingSlashOptional": True, "isProtocolAgnostic": True}
        r = json.loads(_json_call("POST", "/cms/v3/url-redirects", body))
        if not r.get("id"):
            sys.exit(f"redirect for {path} failed: {str(r)[:300]}")
        print(f"  {path} -> {dest} (id {r['id']})")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--push", action="store_true")
    a = ap.parse_args()
    found = existing()
    if a.push:
        push(found)
    else:
        report(found)
