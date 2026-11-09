#!/usr/bin/env python3
"""Refresh the vendored skills in the frontend-react plugin.

The script copies exact upstream snapshots, applies the small Codex compatibility
overlay documented in frontend-react/ATTRIBUTION.md, and records every source
commit. Installed plugin caches are intentionally never modified.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
PLUGIN_ROOT = REPO_ROOT / "frontend-react"


@dataclass(frozen=True)
class SkillSource:
    source: str
    destination: str


@dataclass(frozen=True)
class Upstream:
    name: str
    checkout: str
    repository: str
    ref: str
    skills: tuple[SkillSource, ...]
    license_file: str | None = None
    bundled_license: str | None = None


UPSTREAMS = (
    Upstream(
        name="vercel-labs-agent-skills",
        checkout="vercel-agent-skills",
        repository="https://github.com/vercel-labs/agent-skills.git",
        ref="main",
        skills=(
            SkillSource("skills/react-best-practices", "vercel-react-best-practices"),
            SkillSource("skills/composition-patterns", "vercel-composition-patterns"),
        ),
    ),
    Upstream(
        name="shadcn-ui",
        checkout="shadcn-ui",
        repository="https://github.com/shadcn-ui/ui.git",
        ref="main",
        skills=(SkillSource("skills/shadcn", "shadcn"),),
        license_file="LICENSE.md",
        bundled_license="shadcn-ui-MIT.txt",
    ),
    Upstream(
        name="anthropic-skills",
        checkout="anthropic-skills",
        repository="https://github.com/anthropics/skills.git",
        ref="main",
        skills=(SkillSource("skills/webapp-testing", "webapp-testing"),),
    ),
    Upstream(
        name="wshobson-agents",
        checkout="wshobson-agents",
        repository="https://github.com/wshobson/agents.git",
        ref="main",
        skills=(
            SkillSource(
                "plugins/javascript-typescript/skills/typescript-advanced-types",
                "typescript-advanced-types",
            ),
        ),
        license_file="LICENSE",
        bundled_license="wshobson-agents-MIT.txt",
    ),
    Upstream(
        name="ui-skills",
        checkout="ui-skills",
        repository="https://github.com/ibelick/ui-skills.git",
        ref="main",
        skills=(
            SkillSource("skills/fixing-accessibility", "fixing-accessibility"),
            SkillSource("skills/fixing-motion-performance", "fixing-motion-performance"),
            SkillSource("skills/fixing-metadata", "fixing-metadata"),
        ),
        license_file="LICENSE",
        bundled_license="ui-skills-MIT.txt",
    ),
)


OPENAI_INTERFACES = {
    "vercel-react-best-practices": (
        "Vercel React Best Practices",
        "Optimize React and Next.js performance.",
        "Use $vercel-react-best-practices to review this React code for the highest-impact performance improvements.",
    ),
    "vercel-composition-patterns": (
        "Vercel Composition Patterns",
        "Design scalable React component APIs.",
        "Use $vercel-composition-patterns to refactor this component API around composition.",
    ),
    "shadcn": (
        "shadcn/ui",
        "Manage and compose shadcn/ui components.",
        "Use $shadcn to add or refine these components using the project's existing shadcn setup.",
    ),
    "webapp-testing": (
        "Web App Testing",
        "Verify web apps with Playwright CLI.",
        "Use $webapp-testing to inspect this local web app with Playwright CLI and add a repository-native regression when needed.",
    ),
    "typescript-advanced-types": (
        "TypeScript Advanced Types",
        "Build safe advanced TypeScript types.",
        "Use $typescript-advanced-types to design a precise type-safe solution for this API.",
    ),
    "fixing-accessibility": (
        "Fixing Accessibility",
        "Repair web accessibility issues.",
        "Use $fixing-accessibility to audit and fix the accessibility of this interface.",
    ),
    "fixing-motion-performance": (
        "Fixing Motion Performance",
        "Repair janky UI animations.",
        "Use $fixing-motion-performance to diagnose and fix this animation's performance.",
    ),
    "fixing-metadata": (
        "Fixing Metadata",
        "Repair page and social metadata.",
        "Use $fixing-metadata to check and fix this page's metadata.",
    ),
}


def run(*args: str, cwd: Path | None = None) -> str:
    result = subprocess.run(
        args,
        cwd=cwd,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout.strip()


def ensure_clean_destinations(upstreams: tuple[Upstream, ...]) -> None:
    paths = [f"frontend-react/skills/{item.destination}" for repo in upstreams for item in repo.skills]
    status = run("git", "status", "--porcelain", "--", *paths, cwd=REPO_ROOT)
    if status:
        raise SystemExit(
            "Refusing to overwrite local edits in vendored skill directories:\n" + status
        )


def checkout_upstream(
    upstream: Upstream, source_root: Path | None, temp_root: Path, commit: str | None = None
) -> Path:
    if source_root is not None:
        checkout = source_root / upstream.checkout
        if not (checkout / ".git").exists():
            raise SystemExit(f"Missing upstream checkout: {checkout}")
        status = run("git", "status", "--porcelain", cwd=checkout)
        if status:
            raise SystemExit(f"Refusing dirty upstream checkout {checkout}:\n{status}")
        if commit and run("git", "rev-parse", "HEAD", cwd=checkout) != commit:
            raise SystemExit(f"Upstream checkout does not match locked commit: {checkout}")
        return checkout

    checkout = temp_root / upstream.checkout
    run(
        "git",
        "clone",
        "--depth",
        "1",
        "--filter=blob:none",
        "--sparse",
        "--branch",
        upstream.ref,
        upstream.repository,
        str(checkout),
    )
    run(
        "git",
        "sparse-checkout",
        "set",
        *(skill.source for skill in upstream.skills),
        cwd=checkout,
    )
    if commit:
        run("git", "fetch", "--depth", "1", "origin", commit, cwd=checkout)
        run("git", "checkout", "--detach", commit, cwd=checkout)
    return checkout


def copy_skill(source: Path, destination: Path) -> None:
    if not (source / "SKILL.md").is_file():
        raise SystemExit(f"Upstream skill is missing SKILL.md: {source}")
    symlinks = [path for path in source.rglob("*") if path.is_symlink()]
    if symlinks:
        names = "\n".join(str(path) for path in symlinks)
        raise SystemExit(f"Refusing upstream symlinks:\n{names}")
    shutil.copytree(source, destination)


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"Expected one {label} compatibility anchor, found {count}")
    return text.replace(old, new)


REACT_FRAMEWORK_GUIDANCE = """## Framework ownership

Apply general React guidance to the installed React version. Next.js-specific
APIs, routing, caching, and server lifecycle examples apply only to Next.js.
Do not introduce `next/dynamic`, `next/server`, `after()`, or a Next.js cache
contract into another framework. Verify runtime-specific behavior against the
target framework's current docs and installed exports before adapting examples.

For RedwoodSDK apps, Redwood Web Apps owns routing, RSC/server-function
semantics, and Cloudflare deployment; Frontend / React owns UI components,
StyleX, and browser verification. Use the Redwood skill when available, or
consult https://docs.rwsdk.com/llms.txt and the relevant current pages directly.
Preserve the existing framework and styling. This guide does not select a new
app framework, mandate SWR, or authorize migration.

"""


def adapt_react_framework(skill_dir: Path) -> None:
    """Keep framework boundaries present after refreshing Vercel snapshots."""
    for name in ("SKILL.md", "AGENTS.md"):
        path = skill_dir / name
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        if REACT_FRAMEWORK_GUIDANCE in text:
            continue
        if name == "SKILL.md":
            parts = text.split("---", 2)
            if len(parts) != 3 or parts[0].strip():
                raise SystemExit("React skill is missing YAML frontmatter")
            text = "---" + parts[1] + "---\n\n" + REACT_FRAMEWORK_GUIDANCE + parts[2].lstrip()
        else:
            text = REACT_FRAMEWORK_GUIDANCE + text
        path.write_text(text, encoding="utf-8")


def adapt_shadcn(skill_dir: Path) -> None:
    skill_file = skill_dir / "SKILL.md"
    text = skill_file.read_text(encoding="utf-8")
    text = re.sub(r"(?m)^user-invocable:.*\n", "", text)
    text = re.sub(r"(?m)^allowed-tools:.*\n", "", text)
    text = replace_once(
        text,
        "or any project with a components.json file.",
        "or explicit shadcn requests. A components.json file alone does not select this skill for unrelated components; Base UI + StyleX components use base-ui-stylex.",
        "shadcn component routing",
    )
    text = replace_once(
        text,
        "## Current Project Context",
        "Read [stack routing](references/stack-routing.md) in mixed projects before applying the conventions below.\n\n## Current Project Context",
        "shadcn routing reference",
    )
    text = replace_once(
        text,
        "> **IMPORTANT:** Run all CLI commands using the project's package runner: `npx shadcn@latest`, `pnpm dlx shadcn@latest`, or `bunx --bun shadcn@latest` — based on the project's `packageManager`. Examples below use `npx shadcn@latest` but substitute the correct runner for the project.\n",
        "> **Codex compatibility:** Inspect the nearest `AGENTS.md`, `package.json`, lockfile, and `components.json` first. Prefer an already-installed project-local shadcn CLI through the repository's package manager. Treat the `@latest` commands in this upstream guide as examples, not permission to download packages. Ask before an ephemeral install, and run mutating commands only when the user requested the change.\n",
        "shadcn package-runner",
    )
    text = replace_once(
        text,
        "```json\n!`npx shadcn@latest info --json`\n```\n\nThe JSON above contains the project config and installed components. Use `npx shadcn@latest docs <component>` to get documentation and example URLs for any component.\n",
        "Read `components.json`, the package manifest, and installed component files. When a compatible local shadcn CLI is available, run its `info --json` command to confirm the project config and installed components. Use its `docs <component>` command when current component documentation is needed.\n",
        "shadcn inline-command",
    )
    skill_file.write_text(text, encoding="utf-8")

    mcp_file = skill_dir / "mcp.md"
    mcp_text = mcp_file.read_text(encoding="utf-8")
    mcp_text = re.sub(r"(?m)^\| Claude Code \|.*\n", "", mcp_text)
    mcp_file.write_text(mcp_text, encoding="utf-8")

    legacy_metadata = skill_dir / "agents" / "openai.yml"
    legacy_metadata.unlink(missing_ok=True)
    references = skill_dir / "references"
    references.mkdir(exist_ok=True)
    (references / "stack-routing.md").write_text(
        "# Component routing\n\n"
        "Apply shadcn conventions to existing shadcn components or explicit shadcn requests. "
        "Inspect the target component's imports, implementation, and styling contract; components.json "
        "does not make every component in a mixed project a shadcn component.\n\n"
        "Base UI + StyleX components use base-ui-stylex for behavior and integration, with stylex "
        "supporting general styling and compiler work. Tailwind, cn(), shadcn variants, and component "
        "conventions in this skill do not govern those components. Existing shadcn components may "
        "use Base UI internally; preserve their actual styling contract unless migration is requested.\n\n"
        "Plain React performance work uses relevant performance guidance without adding a Base UI workflow.\n",
        encoding="utf-8",
    )


def adapt_webapp_testing(skill_dir: Path) -> None:
    skill_file = skill_dir / "SKILL.md"
    text = skill_file.read_text(encoding="utf-8")
    text = replace_once(
        text,
        "description: Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing browser screenshots, and viewing browser logs.",
        "description: Verify local web applications with Playwright CLI for live browser work and the repository's existing test runner for durable regressions. Use for UI flows, screenshots, console errors, accessibility checks, and browser debugging.",
        "webapp-testing description",
    )
    compatibility = (
        "# Web Application Testing\n\n"
        "## Codex compatibility\n\n"
        "Honor the target repository's instructions and existing test stack. For live browser work, use the installed official Playwright skill and its `playwright-cli` workflow. Do not install browser tooling or dependencies without authorization. Use another browser tool only when the user requests it or Playwright CLI lacks a required capability.\n\n"
        "### Choose the browser path\n\n"
        "Use the smallest path that produces the evidence the user needs:\n\n"
        "- **Live verification or exploratory debugging:** use Playwright CLI with an isolated named session. Take a snapshot before using element references and refresh it after navigation or meaningful UI changes. Capture screenshots, traces, and console evidence when they answer the task. Close the session you own.\n"
        "- **Durable regression or CI coverage:** use the repository's committed browser-test runner, configuration, language, and dependencies. Extend an existing Playwright suite when it fits; do not introduce a parallel Python harness.\n"
        "- **React runtime diagnosis:** reproduce the affected flow in Playwright CLI, then use the project's existing profiling or diagnostic tools for render counts and Web Vitals. Report measurements only when observed; a screenshot does not establish runtime performance.\n"
        "- **Formal QA handoff:** use Playwright CLI to collect reproducible steps, targeted screenshots or traces, and a concise issue report. Verify each issue in the running app before reporting it.\n\n"
        "Keep exploration and committed regression tests distinct: a successful browser click does not replace an assertion in the project's test suite.\n\n"
        "### Annotation-mode check\n\n"
        "Playwright can verify the application, but it does not prove that Codex annotation mode works in the in-app browser. If annotation mode hides the pointer, shows a small black box, or cannot select an element while ordinary interaction still works, check for a collision between the page's style CSP and Codex's injected annotation stylesheet before clearing browser state or changing application CSS. Read [Diagnose Codex annotation CSP failures](references/codex-annotation-csp.md). When annotation mode works normally, do not change the application's CSP.\n"
    )
    text = replace_once(
        text,
        "# Web Application Testing\n",
        compatibility,
        "webapp-testing heading",
    )
    legacy_start = "To test local web applications, write native Python Playwright scripts."
    if text.count(legacy_start) != 1:
        raise SystemExit("Expected one webapp-testing legacy Python anchor")
    text = text.split(legacy_start, 1)[0] + (
        "## Bundled legacy helper\n\n"
        "The upstream Python examples and `scripts/with_server.py` remain in the package for existing consumers. "
        "Use them only when explicitly requested or when Playwright CLI cannot provide a required capability. "
        "Inspect the helper's `--help` before use. Wait for the specific UI state or assertion needed; "
        "do not treat `networkidle` or fixed timeouts as proof that a page is ready.\n"
    )
    skill_file.write_text(text.rstrip() + "\n", encoding="utf-8")
    shutil.rmtree(skill_dir / "examples", ignore_errors=True)

    source_reference = (
        PLUGIN_ROOT
        / "skills"
        / "webapp-testing"
        / "references"
        / "codex-annotation-csp.md"
    )
    destination_reference = skill_dir / "references" / "codex-annotation-csp.md"
    destination_reference.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_reference, destination_reference)

    source_evals = (
        PLUGIN_ROOT / "skills" / "webapp-testing" / "evals" / "evals.json"
    )
    destination_evals = skill_dir / "evals" / "evals.json"
    destination_evals.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_evals, destination_evals)


def adapt_ui_skills(skill_dir: Path) -> None:
    if skill_dir.name != "fixing-metadata":
        return
    skill_file = skill_dir / "SKILL.md"
    text = skill_file.read_text(encoding="utf-8")
    text, count = re.subn(r"(?m)^version: [^\n]+\n", "", text, count=1)
    if count != 1:
        raise SystemExit("Expected one UI Skills metadata version compatibility anchor")
    skill_file.write_text(text, encoding="utf-8")


def write_openai_metadata(skill_dir: Path) -> None:
    display_name, short_description, default_prompt = OPENAI_INTERFACES[skill_dir.name]
    lines = [
        "interface:",
        f"  display_name: {json.dumps(display_name)}",
        f"  short_description: {json.dumps(short_description)}",
    ]
    if skill_dir.name == "shadcn":
        lines.extend(
            [
                '  icon_small: "./assets/shadcn-small.png"',
                '  icon_large: "./assets/shadcn.png"',
            ]
        )
    lines.append(f"  default_prompt: {json.dumps(default_prompt)}")
    agents = skill_dir / "agents"
    agents.mkdir(exist_ok=True)
    (agents / "openai.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def normalize_text_files(root: Path) -> None:
    text_suffixes = {".json", ".md", ".py", ".txt", ".yaml", ".yml"}
    for path in root.rglob("*"):
        if path.is_file() and path.suffix in text_suffixes:
            content = path.read_text(encoding="utf-8")
            path.write_text(re.sub(r"[ \t]+(?=\n|$)", "", content), encoding="utf-8")


def validate_skill(skill_dir: Path) -> None:
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    match = re.search(r"(?m)^name:\s*['\"]?([^'\"\n]+)", text)
    if match is None or match.group(1).strip() != skill_dir.name:
        found = match.group(1).strip() if match else "missing"
        raise SystemExit(
            f"Skill identity mismatch for {skill_dir}: expected {skill_dir.name}, found {found}"
        )
    if re.search(r"(?i)claude(?: code)?", text):
        raise SystemExit(f"Claude-specific instructions remain in {skill_dir / 'SKILL.md'}")
    if "!`" in text or "allowed-tools:" in text or "user-invocable:" in text:
        raise SystemExit(f"Non-portable skill metadata remains in {skill_dir / 'SKILL.md'}")
    if not (skill_dir / "agents" / "openai.yaml").is_file():
        raise SystemExit(f"Missing Codex metadata: {skill_dir / 'agents' / 'openai.yaml'}")


def parse_version(value: str) -> tuple[int, int, int]:
    match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)", value)
    if match is None:
        raise SystemExit(f"Cannot automatically bump non-SemVer version: {value}")
    return tuple(int(part) for part in match.groups())


def bump_plugin_version(changed: list[tuple[str, str, str]]) -> str:
    manifest_paths = [PLUGIN_ROOT / "plugin.json", PLUGIN_ROOT / ".codex-plugin" / "plugin.json"]
    claude_manifest = PLUGIN_ROOT / ".claude-plugin" / "plugin.json"
    if claude_manifest.exists():
        manifest_paths.append(claude_manifest)
    documents = [json.loads(path.read_text(encoding="utf-8")) for path in manifest_paths]
    versions = {document["version"] for document in documents}
    if len(versions) != 1:
        raise SystemExit(f"Plugin manifests disagree on version: {sorted(versions)}")
    major, minor, patch = parse_version(versions.pop())
    version = f"{major}.{minor}.{patch + 1}"
    for path, document in zip(manifest_paths, documents):
        document["version"] = version
        path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")

    catalog_path = PLUGIN_ROOT.parent / ".claude-plugin" / "marketplace.json"
    if catalog_path.exists():
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        for plugin in catalog["plugins"]:
            if plugin["name"] == PLUGIN_ROOT.name:
                plugin["version"] = version
        catalog_path.write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")

    changelog = PLUGIN_ROOT / "CHANGELOG.md"
    old = changelog.read_text(encoding="utf-8")
    details = "\n".join(
        f"- Refreshed `{name}` from `{before[:12]}` to `{after[:12]}`."
        for name, before, after in changed
    )
    entry = f"\n## {version}\n\n{details}\n"
    changelog.write_text(replace_once(old, "# Changelog\n", "# Changelog\n" + entry, "changelog"), encoding="utf-8")
    return version


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--upstream", action="append", choices=[upstream.name for upstream in UPSTREAMS],
        help="Refresh only this upstream (repeatable); preserve all other pins and bytes.",
    )
    parser.add_argument(
        "--locked", action="store_true",
        help="Reproduce the recorded commits instead of advancing upstream refs.",
    )
    parser.add_argument(
        "--source-root",
        type=Path,
        help="Use existing checkouts below this directory instead of cloning.",
    )
    parser.add_argument(
        "--no-bump-version",
        action="store_true",
        help="Do not bump plugin SemVer when an existing lock changes (initial import only).",
    )
    args = parser.parse_args()

    selected = tuple(u for u in UPSTREAMS if not args.upstream or u.name in args.upstream)
    ensure_clean_destinations(selected)
    old_lock_path = PLUGIN_ROOT / "upstreams.lock.json"
    old_lock = json.loads(old_lock_path.read_text(encoding="utf-8")) if old_lock_path.exists() else None
    old_entries = {item["name"]: item for item in old_lock.get("upstreams", [])} if old_lock else {}
    if args.locked and any(u.name not in old_entries for u in selected):
        raise SystemExit("Cannot reproduce an upstream without a recorded commit")
    if any(u.name not in old_entries and u not in selected for u in UPSTREAMS):
        raise SystemExit("Initial import must include every upstream without a recorded commit")

    temp_parent = Path(tempfile.mkdtemp(prefix="frontend-react-sync."))
    stage_root = Path(tempfile.mkdtemp(prefix=".sync-", dir=PLUGIN_ROOT))
    commits: dict[str, str] = {}
    try:
        staged_skills = stage_root / "skills"
        staged_licenses = stage_root / "licenses"
        staged_skills.mkdir()
        staged_licenses.mkdir()

        for upstream in selected:
            commit = old_entries[upstream.name]["commit"] if args.locked else None
            checkout = checkout_upstream(upstream, args.source_root, temp_parent, commit)
            commits[upstream.name] = run("git", "rev-parse", "HEAD", cwd=checkout)
            for skill in upstream.skills:
                copy_skill(checkout / skill.source, staged_skills / skill.destination)
            if upstream.license_file and upstream.bundled_license:
                shutil.copy2(
                    checkout / upstream.license_file,
                    staged_licenses / upstream.bundled_license,
                )

        if (staged_skills / "vercel-react-best-practices").exists():
            adapt_react_framework(staged_skills / "vercel-react-best-practices")
        if (staged_skills / "shadcn").exists():
            adapt_shadcn(staged_skills / "shadcn")
        if (staged_skills / "webapp-testing").exists():
            adapt_webapp_testing(staged_skills / "webapp-testing")
        for skill_dir in staged_skills.iterdir():
            if skill_dir.name in {"fixing-accessibility", "fixing-motion-performance", "fixing-metadata"}:
                adapt_ui_skills(skill_dir)
        for skill_dir in sorted(staged_skills.iterdir()):
            write_openai_metadata(skill_dir)
        normalize_text_files(staged_skills)
        normalize_text_files(staged_licenses)
        for skill_dir in sorted(staged_skills.iterdir()):
            validate_skill(skill_dir)

        backup_root = stage_root / "backups"
        backup_root.mkdir()
        replaced: list[tuple[Path, Path | None]] = []
        try:
            for staged in sorted(staged_skills.iterdir()):
                destination = PLUGIN_ROOT / "skills" / staged.name
                backup = backup_root / staged.name if destination.exists() else None
                if backup is not None:
                    os.replace(destination, backup)
                os.replace(staged, destination)
                replaced.append((destination, backup))
        except Exception:
            for destination, backup in reversed(replaced):
                if destination.exists():
                    shutil.rmtree(destination)
                if backup is not None and backup.exists():
                    os.replace(backup, destination)
            raise

        licenses = PLUGIN_ROOT / "licenses"
        licenses.mkdir(exist_ok=True)
        for staged_license in staged_licenses.iterdir():
            shutil.copy2(staged_license, licenses / staged_license.name)

        lock = {
            "schema_version": 1,
            "upstreams": [
                {
                    "name": upstream.name,
                    "repository": upstream.repository.removesuffix(".git"),
                    "ref": upstream.ref,
                    "commit": commits[upstream.name],
                    "skills": [
                        {"source": skill.source, "destination": f"skills/{skill.destination}"}
                        for skill in upstream.skills
                    ],
                } if upstream in selected else old_entries[upstream.name]
                for upstream in UPSTREAMS
            ],
        }
        old_commits = {
            item["name"]: item["commit"] for item in old_lock.get("upstreams", [])
        } if old_lock else {}
        changed = [
            (upstream.name, old_commits[upstream.name], commits[upstream.name])
            for upstream in selected
            if upstream.name in old_commits and old_commits[upstream.name] != commits[upstream.name]
        ]
        old_lock_path.write_text(json.dumps(lock, indent=2) + "\n", encoding="utf-8")

        version = None
        if changed and not args.no_bump_version:
            version = bump_plugin_version(changed)

        print("Synced frontend-react upstreams:")
        for upstream in selected:
            print(f"- {upstream.name}: {commits[upstream.name]}")
        if version:
            print(f"Bumped plugin version to {version}")
        elif changed:
            print("Upstream commits changed; version bump was explicitly disabled")
        return 0
    finally:
        shutil.rmtree(stage_root, ignore_errors=True)
        shutil.rmtree(temp_parent, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
