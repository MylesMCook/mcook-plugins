#!/usr/bin/env python3
"""Run offline structural and contract checks for this skill package."""

from __future__ import annotations

import json
import re
import struct
import sys
from pathlib import Path


NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REF_RE = re.compile(r"`((?:references|scripts|assets|evals)/[^`]+)`")
REQUIRED_SNIPPETS = {
    "SKILL.md": [
        "## Choose one mode",
        "## Hold the truth boundary",
        "## System portrait plan",
        "If the request is ambiguous, use Inkblot-first",
        "assets/inkblot-reference.png",
        "no prop may be larger or more prominent",
        "Never describe or draw an oversized prop",
        "[verified]",
        "[inferred]",
        "[unknown]",
        "one abstraction level",
    ],
    "references/system-portrait-method.md": [
        "Landscape/context",
        "Plumbing/container",
        "Failure/recovery",
        "origin -> destination",
    ],
    "references/qa-checklist.md": [
        "## Pass 1: System truth",
        "## Pass 2: Visual fidelity",
        "**Inkblot-first:**",
        "**System portrait:**",
    ],
    "references/prompt-template.md": [
        "## Inkblot-first prompt",
        "Do not invent components or connections",
        "Exact in-image labels",
    ],
    "references/style-dna.md": [
        "## Mode defaults",
        "no labels by default",
    ],
}


def frontmatter(text: str) -> tuple[str, str, list[str]]:
    errors: list[str] = []
    if not text.startswith("---\n"):
        return "", "", ["SKILL.md must start with YAML frontmatter"]
    end = text.find("\n---", 4)
    if end == -1:
        return "", "", ["SKILL.md is missing closing frontmatter"]
    raw = text[4:end]
    name_match = re.search(r"^name:\s*([^\n]+)$", raw, re.MULTILINE)
    name = name_match.group(1).strip().strip("\"'") if name_match else ""
    description = ""
    lines = raw.splitlines()
    for index, line in enumerate(lines):
        if not line.startswith("description:"):
            continue
        value = line.partition(":")[2].strip()
        if value in {">", ">-", "|", "|-"}:
            folded: list[str] = []
            for continuation in lines[index + 1 :]:
                if continuation and not continuation.startswith((" ", "\t")):
                    break
                if continuation.strip():
                    folded.append(continuation.strip())
            description = " ".join(folded)
        else:
            description = value.strip("\"'")
        break
    return name, description, errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors: list[str] = []
    skill_path = root / "SKILL.md"
    if not skill_path.exists():
        print("ERROR: SKILL.md not found", file=sys.stderr)
        return 1

    text = skill_path.read_text(encoding="utf-8")
    name, description, fm_errors = frontmatter(text)
    errors.extend(fm_errors)
    if name != root.name:
        errors.append(f"frontmatter name {name!r} must match {root.name!r}")
    if not NAME_RE.fullmatch(name):
        errors.append("frontmatter name must be lowercase kebab-case")
    if not description:
        errors.append("frontmatter description is required")
    if len(description) > 1024:
        errors.append("frontmatter description exceeds 1024 characters")
    body = text[text.find("\n---", 4) + 4 :]
    if len(body.splitlines()) > 500:
        errors.append("SKILL.md body exceeds 500 lines")

    for ref in sorted(set(REF_RE.findall(body))):
        if "<" in ref or ">" in ref:
            continue
        if not (root / ref).exists():
            errors.append(f"referenced file does not exist: {ref}")

    for relative, snippets in REQUIRED_SNIPPETS.items():
        path = root / relative
        if not path.exists():
            errors.append(f"missing required file: {relative}")
            continue
        contents = path.read_text(encoding="utf-8")
        for snippet in snippets:
            if snippet not in contents:
                errors.append(f"{relative} missing contract text: {snippet!r}")

    for path in (root / "references").glob("*.md"):
        contents = path.read_text(encoding="utf-8")
        if len(contents.splitlines()) > 100 and "## Contents" not in contents:
            errors.append(f"long reference needs a Contents section: {path.name}")

    reference_image = root / "assets/inkblot-reference.png"
    try:
        data = reference_image.read_bytes()
        if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
            errors.append("assets/inkblot-reference.png must be a valid PNG")
        elif len(data) < 24:
            errors.append("assets/inkblot-reference.png is truncated")
        else:
            width, height = struct.unpack(">II", data[16:24])
            if width < 1000 or height < 500:
                errors.append("assets/inkblot-reference.png is too small")
            ratio = width / height
            if not 1.7 <= ratio <= 1.85:
                errors.append("assets/inkblot-reference.png must be approximately 16:9")
    except OSError as exc:
        errors.append(f"missing Inkblot reference image: {exc}")

    triggers_path = root / "evals/triggers.json"
    evals_path = root / "evals/evals.json"
    try:
        triggers = json.loads(triggers_path.read_text(encoding="utf-8"))
        cases = triggers.get("cases", [])
        positives = [case for case in cases if case.get("should_trigger") is True]
        negatives = [case for case in cases if case.get("should_trigger") is False]
        if triggers.get("skill_name") != name:
            errors.append("triggers.json skill_name must match the skill")
        if triggers.get("runs_per_case", 0) < 3:
            errors.append("triggers.json runs_per_case must be at least 3")
        if len(cases) < 20 or len(positives) < 9 or len(negatives) < 9:
            errors.append("triggers.json needs at least 20 roughly balanced cases")
        if not any("Inkblot-first" in case.get("rationale", "") for case in positives):
            errors.append("triggers.json needs an Inkblot-first positive case")
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid evals/triggers.json: {exc}")

    try:
        eval_data = json.loads(evals_path.read_text(encoding="utf-8"))
        evals = eval_data.get("evals", [])
        if eval_data.get("skill_name") != name:
            errors.append("evals.json skill_name must match the skill")
        if not 10 <= len(evals) <= 20:
            errors.append("evals.json must contain 10-20 cases")
        if not any("Inkblot-first" in case.get("expected_output", "") for case in evals):
            errors.append("evals.json needs an Inkblot-first acceptance case")
        for case in evals:
            for field in ("id", "prompt", "expected_output", "expectations"):
                if field not in case:
                    errors.append(f"eval {case.get('id', '?')} missing {field}")
            for relative in case.get("files", []):
                if not (root / relative).exists():
                    errors.append(f"eval file does not exist: {relative}")
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid evals/evals.json: {exc}")

    plugin_root = root.parents[1]
    manifest_path = plugin_root / ".codex-plugin/plugin.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        plugin_name = manifest.get("name")
        possible_folder_names = {plugin_root.name, plugin_root.parent.name}
        if plugin_name not in possible_folder_names:
            errors.append("plugin manifest name must match the plugin folder or cache namespace")
        if manifest.get("skills") != "./skills/":
            errors.append("plugin manifest skills path must be ./skills/")
        if not manifest.get("version"):
            errors.append("plugin manifest version is required")
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid plugin manifest: {exc}")

    repository_root = plugin_root.parent
    catalog_path = repository_root / ".agents/plugins/marketplace.json"
    if catalog_path.exists():
        try:
            catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
            entries = [
                entry
                for entry in catalog.get("plugins", [])
                if entry.get("name") == plugin_root.name
            ]
            expected_path = f"./{plugin_root.name}"
            if len(entries) != 1:
                errors.append("marketplace must contain exactly one plugin entry")
            elif entries[0].get("source", {}).get("path") != expected_path:
                errors.append(f"marketplace source path must be {expected_path}")
        except json.JSONDecodeError as exc:
            errors.append(f"invalid marketplace catalog: {exc}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("OK: Inkblot skill and detected package contracts passed offline checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
