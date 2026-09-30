#!/usr/bin/env python3
"""Build static profile artwork or check its offline structural invariants."""

import argparse
from html.parser import HTMLParser
from pathlib import Path
import re
import subprocess
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parent.parent
THEMES = ("light", "dark")


def artwork(theme):
    source = ROOT / "assets" / f"banner-{theme}.svg.source"
    return source, source.with_suffix("")


def generated_text(source):
    return re.sub(r"\s*<!--.*?-->\s*", "\n", source.read_text(), flags=re.S)


class ProfileHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.references = []
        self.details_depth = 0
        self.problems = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "details":
            self.details_depth += 1
        if tag == "img" and not attrs.get("alt"):
            self.problems.append("Image is missing meaningful alt text")
        for name in ("src", "srcset"):
            if name in attrs:
                self.references.append(attrs[name])

    def handle_endtag(self, tag):
        if tag == "details":
            self.details_depth -= 1
            if self.details_depth < 0:
                self.problems.append("Unmatched closing details tag")


def build():
    for theme in THEMES:
        source, target = artwork(theme)
        ET.fromstring(source.read_text())
        target.write_text(generated_text(source))
        print(f"Built {target.relative_to(ROOT)}")


def privacy_errors(history):
    """Use an untracked local Git setting; never print the protected hostname."""
    result = subprocess.run(
        ["git", "config", "--local", "--get", "profile.unlistedHost"],
        cwd=ROOT, capture_output=True, text=True,
    )
    protected = result.stdout.strip().lower()
    if not protected:
        return ["Local unlisted-source privacy guard is not configured"] if history else []
    files = subprocess.run(
        ["git", "ls-files", "-c", "-o", "--exclude-standard", "-z"],
        cwd=ROOT, capture_output=True, check=True,
    ).stdout.decode().split("\0")
    errors = []
    for name in sorted(set(filter(None, files))):
        path = ROOT / name
        if path.is_file() and protected.encode() in path.read_bytes().lower():
            errors.append(f"Unlisted-source reference in {name}")
    if history:
        revisions = subprocess.run(
            ["git", "rev-list", "HEAD"], cwd=ROOT,
            capture_output=True, check=True, text=True,
        ).stdout.splitlines()
        for revision in revisions:
            found = subprocess.run(
                ["git", "grep", "-i", "-F", "-q", "-e", protected, revision],
                cwd=ROOT, capture_output=True,
            )
            if found.returncode == 0:
                errors.append(f"Unlisted-source reference in commit {revision[:10]}")
            elif found.returncode != 1:
                errors.append(f"Could not inspect privacy of commit {revision[:10]}")
    return errors


def check(history=False):
    errors = []
    for theme in THEMES:
        source, target = artwork(theme)
        if not source.is_file() or not target.is_file():
            errors.append(f"Missing artwork source or artifact for {theme}")
            continue
        try:
            tree = ET.fromstring(target.read_text())
            if tree.tag != "{http://www.w3.org/2000/svg}svg":
                errors.append(f"Invalid SVG root: {target.name}")
            if tree.find("{http://www.w3.org/2000/svg}title") is None:
                errors.append(f"Missing SVG title: {target.name}")
            if target.read_text() != generated_text(source):
                errors.append(f"Stale generated artifact: {target.name}")
            for element in tree.iter():
                if element.tag.rsplit("}", 1)[-1] in ("script", "foreignObject"):
                    errors.append(f"Active content in {target.name}")
                if any(key.rsplit("}", 1)[-1] == "href" and not value.startswith("#")
                       for key, value in element.attrib.items()):
                    errors.append(f"External artwork dependency in {target.name}")
        except ET.ParseError as exc:
            errors.append(f"Invalid XML in {target.name}: {exc}")

    readme = (ROOT / "README.md").read_text()
    parser = ProfileHTML()
    parser.feed(readme)
    errors.extend(parser.problems)
    if parser.details_depth != 0:
        errors.append("Unclosed details section")
    references = parser.references + re.findall(r"\]\(([^)]+)\)", readme)
    for reference in references:
        if ":" not in reference and not reference.startswith("#"):
            target = (ROOT / reference.split("#", 1)[0]).resolve()
            if not target.is_relative_to(ROOT) or not target.is_file():
                errors.append(f"Invalid local README reference: {reference}")
    if "SparkyLinux" not in readme:
        errors.append("Required SparkyLinux section missing")
    if "prefers-color-scheme: dark" not in readme:
        errors.append("Dark-theme picture source missing")
    errors.extend(privacy_errors(history))
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("PASS: source/artifact parity, static SVG, local links, alt text, details and required sections")
    if history:
        print("PASS: configured unlisted-source guard across files and Git history")
    print("Offline structural checks only; external links and factual claims require separate review.")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("build", "check"))
    parser.add_argument("--history", action="store_true", help="Check unlisted-source privacy across Git history")
    args = parser.parse_args()
    if args.command == "build":
        if args.history:
            parser.error("--history applies only to check")
        build()
        return 0
    return check(args.history)


if __name__ == "__main__":
    raise SystemExit(main())
