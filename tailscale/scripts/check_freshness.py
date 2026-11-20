#!/usr/bin/env python3
"""Report drift between the Tailscale skill and Tailscale's live docs.

Checks, standard library only:
  1. Every tailscale.com/docs URL in the skill still resolves, without a
     redirect to another page and without a deprecation notice.
  2. Every section and feature page in https://tailscale.com/docs/llms.txt is
     mentioned in references/docs-map.md.
  3. The upstream tailscale/tailscale-skill HEAD still matches the commit
     recorded in ATTRIBUTION.md.

Exits 1 when anything needs review, 2 when a source could not be read.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
SKILL_ROOT = PLUGIN_ROOT / "skills" / "tailscale"
DOCS_MAP = SKILL_ROOT / "references" / "docs-map.md"
ATTRIBUTION = PLUGIN_ROOT / "ATTRIBUTION.md"
LLMS_URL = "https://tailscale.com/docs/llms.txt"
UPSTREAM_REPO = "https://github.com/tailscale/tailscale-skill"
USER_AGENT = "mcook-plugins-tailscale-freshness/1.0"
DEPRECATION_MARKERS = ("this topic is deprecated", "this page is deprecated")

DOC_URL_RE = re.compile(r"https://tailscale\.com/docs[^\s)`>\"'|\]]*")
SECTION_RE = re.compile(r"^## (.+?)\s*$", re.MULTILINE)
FEATURE_RE = re.compile(r"\((https://tailscale\.com/docs/features/[a-z0-9-]+)\.md\)")
COMMIT_RE = re.compile(r"commit \[`([0-9a-f]{40})`\]")


def normalize(url: str) -> str:
    url = url.split("#", 1)[0].rstrip(".,;:*")
    if url.endswith(".md"):
        url = url[: -len(".md")]
    return url.rstrip("/")


def skill_doc_urls(root: Path = SKILL_ROOT) -> dict[str, list[str]]:
    """Map each docs URL to the skill files that cite it."""
    found: dict[str, list[str]] = {}
    for path in sorted(root.rglob("*.md")):
        rel = str(path.relative_to(root))
        for match in DOC_URL_RE.findall(path.read_text(encoding="utf-8")):
            url = normalize(match)
            if url.endswith("/llms.txt") or url == "https://tailscale.com/docs/...":
                continue
            found.setdefault(url, [])
            if rel not in found[url]:
                found[url].append(rel)
    return found


def parse_llms(text: str) -> tuple[list[str], list[str]]:
    sections = [s for s in SECTION_RE.findall(text)]
    features = sorted(set(FEATURE_RE.findall(text)))
    return sections, features


def coverage_gaps(llms_text: str, docs_map_text: str) -> list[str]:
    sections, features = parse_llms(llms_text)
    gaps = [f"docs section not in docs-map.md: {s}" for s in sections if s not in docs_map_text]
    mapped = {normalize(u) for u in DOC_URL_RE.findall(docs_map_text)}
    gaps += [f"feature page not in docs-map.md: {u}" for u in features if u not in mapped]
    return gaps


def is_deprecated(body: str) -> bool:
    head = body[:4000].lower()
    return any(marker in head for marker in DEPRECATION_MARKERS)


def fetch(url: str, timeout: float = 30.0, attempts: int = 3) -> tuple[int, str, str]:
    """Return (status, final URL, body). Status 0 means the network failed."""
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                body = response.read().decode("utf-8", "replace")
                return response.status, response.geturl(), body
        except urllib.error.HTTPError as error:
            if error.code < 500 and error.code != 429:
                return error.code, url, ""
        except (urllib.error.URLError, OSError):
            pass
        time.sleep(2 * (attempt + 1))
    return 0, url, ""


def check_url(url: str) -> str | None:
    status, final, body = fetch(url + ".md")
    if status == 0:
        return "unreachable after retries"
    if status != 200:
        return f"HTTP {status}"
    if normalize(final) != url:
        return f"redirects to {normalize(final)}"
    if is_deprecated(body):
        return "page is marked deprecated"
    return None


def upstream_drift() -> str | None:
    match = COMMIT_RE.search(ATTRIBUTION.read_text(encoding="utf-8"))
    if not match:
        return "no pinned upstream commit found in ATTRIBUTION.md"
    out = subprocess.run(
        ["git", "ls-remote", UPSTREAM_REPO, "HEAD"],
        capture_output=True, text=True, timeout=60, check=True,
    ).stdout.split()
    head = out[0] if out else ""
    if head != match.group(1):
        return f"upstream skill moved: pinned {match.group(1)[:12]}, HEAD {head[:12]} ({UPSTREAM_REPO}/compare/{match.group(1)}...{head})"
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()

    problems: list[str] = []
    try:
        _, _, llms = fetch(LLMS_URL)
        if not llms:
            raise RuntimeError(f"empty response from {LLMS_URL}")
        problems += coverage_gaps(llms, DOCS_MAP.read_text(encoding="utf-8"))

        urls = skill_doc_urls()
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
            for url, issue in zip(urls, pool.map(check_url, urls)):
                if issue:
                    problems.append(f"{url}: {issue} (cited in {', '.join(urls[url])})")

        drift = upstream_drift()
        if drift:
            problems.append(drift)
    except Exception as error:  # network or parse failure is a separate signal
        print(f"freshness check could not run: {error}", file=sys.stderr)
        return 2

    print(f"checked {len(urls)} doc URLs, {LLMS_URL}, and {UPSTREAM_REPO}")
    for problem in problems:
        print(f"- {problem}")
    if problems:
        print(f"{len(problems)} item(s) need review.")
        return 1
    print("No drift found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
