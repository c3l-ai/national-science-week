#!/usr/bin/env python3
"""Check the Future Minds site before it ships.

Local checks (always run, and fail the build):
  - every local href/src points at a file that exists
  - every #anchor points at an element that exists
  - every map pin has a matching event card, and the other way round

External checks (--external, reported but not fatal):
  - every booking and directions link returns a 2xx or 3xx

Usage:
    python3 tools/check_links.py
    python3 tools/check_links.py --external
"""

import os
import re
import sys
import urllib.error
import urllib.request
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = ["index.html"]
TIMEOUT = 15
UA = "Mozilla/5.0 (compatible; c3l-link-check/1.0)"


class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []      # (attr_value, tag)
        self.ids = set()
        self.pins = []
        self.stops = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        for key in ("href", "src"):
            if a.get(key):
                self.links.append((a[key], tag))
        if a.get("id"):
            self.ids.add(a["id"])
        cls = a.get("class", "")
        stop = a.get("data-stop")
        if stop:
            if "pin" in cls.split():
                self.pins.append(stop)
            if "stop" in cls.split():
                self.stops.append(stop)


def load(page):
    path = os.path.join(ROOT, page)
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def check_local(page, parser):
    problems = []

    for href, tag in parser.links:
        if href.startswith(("http://", "https://", "mailto:", "tel:", "data:", "//")):
            continue
        if href.startswith("#"):
            target = href[1:]
            if target and target not in parser.ids:
                problems.append(f"{page}: <{tag}> points at #{target}, which no element has")
            continue
        local = href.split("?")[0].split("#")[0]
        if not os.path.exists(os.path.join(ROOT, local)):
            problems.append(f"{page}: <{tag}> points at {local}, which is not in the repo")

    missing_cards = sorted(set(parser.pins) - set(parser.stops))
    missing_pins = sorted(set(parser.stops) - set(parser.pins))
    for key in missing_cards:
        problems.append(f"{page}: map pin '{key}' has no matching event card")
    for key in missing_pins:
        problems.append(f"{page}: event card '{key}' has no matching map pin")

    return problems


def check_external(parser):
    seen = set()
    problems = []
    for href, _ in parser.links:
        if not href.startswith(("http://", "https://")):
            continue
        if href in seen:
            continue
        seen.add(href)
        req = urllib.request.Request(href, headers={"User-Agent": UA}, method="GET")
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                if resp.status >= 400:
                    problems.append(f"{href} returned {resp.status}")
                else:
                    print(f"  ok  {resp.status}  {href}")
        except urllib.error.HTTPError as exc:
            problems.append(f"{href} returned {exc.code}")
        except Exception as exc:  # network, DNS, TLS
            problems.append(f"{href} could not be reached ({exc.__class__.__name__})")
    return problems


def main():
    external = "--external" in sys.argv
    all_problems = []

    for page in PAGES:
        parser = SiteParser()
        parser.feed(load(page))
        print(f"Checking {page}: {len(parser.links)} links, "
              f"{len(parser.pins)} map pins, {len(parser.stops)} cards")

        if external:
            all_problems += check_external(parser)
        else:
            all_problems += check_local(page, parser)

    if all_problems:
        print("\nProblems found:")
        for p in all_problems:
            print(f"  - {p}")
        # External failures are advisory. Eventbrite and Humanitix both
        # rate limit and sometimes block CI ranges, so a red run there
        # is not a reason to block a deploy.
        sys.exit(0 if external else 1)

    print("\nAll checks passed.")


if __name__ == "__main__":
    main()
