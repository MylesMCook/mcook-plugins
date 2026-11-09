#!/usr/bin/env python3
"""
ADR linter for the laws-of-software-los skill.

Checks for sections and decision qualities that keep architecture records useful:
context, decision, options, tradeoffs, consequences, validation, ownership,
migration, and revisit triggers.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class Issue:
    severity: str
    title: str
    why: str
    fix: str


REQUIRED_SECTION_GROUPS = [
    ("High", "Missing context/problem section", ["context", "problem"], "Readers need to know the forces and constraints behind the decision.", "Add a Context section with problem, constraints, existing system, and non-goals."),
    ("High", "Missing explicit decision", ["decision", "we will"], "An ADR must record the decision, not just discussion.", "Add a Decision section that states the chosen path and scope."),
    ("Medium", "Missing options considered", ["options", "alternatives", "considered"], "Without alternatives, future readers cannot understand tradeoffs.", "Add 2-4 serious options, including the simplest credible option."),
    ("Medium", "Missing consequences/tradeoffs", ["consequence", "tradeoff", "trade-off", "risk"], "Every architecture decision sacrifices something.", "Add positive and negative consequences plus accepted risks."),
    ("Medium", "Missing validation plan", ["validation", "test", "metric", "success criteria", "slo"], "The team needs evidence that the decision works.", "Add tests, metrics, success criteria, and failure/kill criteria."),
    ("Medium", "Missing owner", ["owner", "team", "responsible"], "Unowned decisions decay and create operational risk.", "Name owning team/person and support/on-call responsibility if applicable."),
    ("Medium", "Missing revisit trigger", ["review trigger", "revisit", "expires", "review date", "superseded"], "Decisions without revisit triggers become stale dogma.", "Add a date, metric, or event that reopens the decision."),
]

OPTIONAL_BUT_IMPORTANT = [
    ("Low", "No status marker found", [r"status:\s*(proposed|accepted|superseded|deprecated)", r"\*\*status:\*\*"], "Status helps readers know whether to follow the ADR.", "Add Status: Proposed/Accepted/Superseded/Deprecated."),
    ("Low", "No date found", [r"\b20\d{2}-\d{2}-\d{2}\b", r"\*\*date:\*\*"], "Date anchors the decision in time and context.", "Add an ISO date."),
]


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower())


def has_any(text: str, terms: list[str]) -> bool:
    return any(term.lower() in text for term in terms)


def has_any_regex(text: str, patterns: list[str]) -> bool:
    return any(re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE) for pattern in patterns)


def lint(text: str) -> list[Issue]:
    t = normalize(text)
    issues: list[Issue] = []

    for severity, title, terms, why, fix in REQUIRED_SECTION_GROUPS:
        if not has_any(t, terms):
            issues.append(Issue(severity, title, why, fix))

    for severity, title, patterns, why, fix in OPTIONAL_BUT_IMPORTANT:
        if not has_any_regex(text, patterns):
            issues.append(Issue(severity, title, why, fix))

    # Higher-risk contextual checks.
    if has_any(t, ["api", "client", "consumer", "sdk", "public"]) and not has_any(t, ["compat", "version", "deprecat", "migration"]):
        issues.append(
            Issue(
                "High",
                "Public/API decision lacks compatibility or migration plan",
                "Observable API behavior becomes a contract in practice.",
                "Add compatibility expectations, versioning/deprecation, migration guide, and contract tests.",
            )
        )

    if has_any(t, ["data", "database", "schema", "migration", "backfill"]) and not has_any(t, ["rollback", "reconcile", "backup", "restore", "source of truth"]):
        issues.append(
            Issue(
                "High",
                "Data decision lacks rollback/reconciliation/source-of-truth detail",
                "Data migrations and schema decisions are difficult to reverse and can corrupt business state.",
                "Add source of truth, backup/restore, reconciliation, and rollback/repair plan.",
            )
        )

    if has_any(t, ["microservice", "distributed", "queue", "event", "kafka", "service"]) and not has_any(t, ["timeout", "retry", "idempot", "observability", "trace", "contract test"]):
        issues.append(
            Issue(
                "High",
                "Distributed decision lacks failure-semantics detail",
                "Remote/service/event boundaries add latency, partial failure, retries, duplication, and operability burden.",
                "Add timeout/retry/idempotency/backpressure/observability/contract-test details.",
            )
        )

    order = {"High": 0, "Medium": 1, "Low": 2}
    return sorted(issues, key=lambda i: (order.get(i.severity, 99), i.title))


def to_markdown(path: Path, issues: list[Issue]) -> str:
    lines = ["# ADR Lint", "", f"Input: `{path}`", ""]
    if not issues:
        lines.append("No major ADR omissions detected by the heuristic scan.")
        return "\n".join(lines)

    lines.append(f"Issues: {len(issues)}")
    lines.append("")
    for idx, issue in enumerate(issues, 1):
        lines.append(f"## {idx}. {issue.severity}: {issue.title}")
        lines.append("")
        lines.append(f"**Why:** {issue.why}")
        lines.append("")
        lines.append(f"**Fix:** {issue.fix}")
        lines.append("")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Lint an Architecture Decision Record.")
    parser.add_argument("--input", "-i", required=True, help="Path to ADR Markdown/text file.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown.")
    args = parser.parse_args(argv)

    path = Path(args.input)
    if not path.exists() or not path.is_file():
        print(f"error: input file not found: {path}", file=sys.stderr)
        return 2

    text = path.read_text(encoding="utf-8", errors="replace")
    issues = lint(text)

    if args.json:
        print(json.dumps({"input": str(path), "issues": [asdict(i) for i in issues]}, indent=2))
    else:
        print(to_markdown(path, issues))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
