#!/usr/bin/env python3
"""
Heuristic architecture/design reviewer for the laws-of-software-los skill.

This script does not replace architectural judgment. It catches common omissions
that map to software-engineering law lenses: simplicity, compatibility,
distributed failure, operability, ownership, metrics, migration, and validation.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable, Optional


SEVERITY_ORDER = {"Blocker": 0, "High": 1, "Medium": 2, "Low": 3}


@dataclass
class Finding:
    severity: str
    title: str
    laws: list[str]
    why: str
    fix: str
    evidence: str


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower())


def has_any(text: str, terms: Iterable[str]) -> bool:
    return any(term.lower() in text for term in terms)


def has_regex(text: str, patterns: Iterable[str]) -> bool:
    return any(re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE) for pattern in patterns)


def missing(text: str, terms: Iterable[str]) -> bool:
    return not has_any(text, terms)


def add_if_missing(
    findings: list[Finding],
    *,
    text: str,
    required_terms: Iterable[str],
    severity: str,
    title: str,
    laws: list[str],
    why: str,
    fix: str,
    evidence: str,
    trigger_terms: Optional[Iterable[str]] = None,
    trigger_regex: Optional[Iterable[str]] = None,
) -> None:
    triggered = True
    if trigger_terms is not None:
        triggered = has_any(text, trigger_terms)
    if trigger_regex is not None:
        triggered = triggered or has_regex(text, trigger_regex)
    if triggered and missing(text, required_terms):
        findings.append(
            Finding(
                severity=severity,
                title=title,
                laws=laws,
                why=why,
                fix=fix,
                evidence=evidence,
            )
        )


def review(text: str) -> list[Finding]:
    t = normalize(text)
    findings: list[Finding] = []

    add_if_missing(
        findings,
        text=t,
        required_terms=["goal", "problem", "requirement", "constraint", "non-goal", "context"],
        severity="High",
        title="Problem framing is underspecified",
        laws=["First Principles", "Map Is Not the Territory"],
        why="A design chosen before the problem and constraints are explicit is likely to optimize the wrong thing.",
        fix="Add a short context section with goals, non-goals, hard constraints, users, workload, and decision horizon.",
        evidence="No clear framing terms such as goal/problem/constraint/non-goal were found.",
    )

    add_if_missing(
        findings,
        text=t,
        required_terms=["metric", "slo", "sla", "success criteria", "measure", "baseline", "target"],
        severity="Medium",
        title="Success metrics or validation criteria are missing",
        laws=["Gilb's Law", "Goodhart's Law"],
        why="Without measurable success and guardrails, the design cannot be validated and incentives can drift.",
        fix="Define outcome metrics plus guardrails, baseline, target, and review cadence.",
        evidence="No metric/SLO/success/measurement language was found.",
    )

    add_if_missing(
        findings,
        text=t,
        required_terms=["option", "alternative", "considered", "tradeoff", "trade-off", "rejected"],
        severity="Medium",
        title="Alternatives and tradeoffs are not explicit",
        laws=["Occam's Razor", "YAGNI", "KISS"],
        why="A single-path proposal hides assumptions and can miss a simpler or safer design.",
        fix="Compare 2-4 options, including the simplest credible option, and state what the recommendation sacrifices.",
        evidence="No alternatives/options/tradeoff language was found.",
    )

    add_if_missing(
        findings,
        text=t,
        required_terms=["owner", "team", "on-call", "runbook", "responsible", "ownership"],
        severity="High",
        title="Ownership and operability are unclear",
        laws=["Conway's Law", "Bus Factor", "Broken Windows"],
        why="Architecture that lacks owners and runbooks tends to fail during incidents and handoffs.",
        fix="Name owning team/person, on-call path, runbook location, support process, and backup owner.",
        evidence="No owner/team/on-call/runbook language was found.",
    )

    add_if_missing(
        findings,
        text=t,
        required_terms=["rollback", "revert", "feature flag", "canary", "blue/green", "roll back", "kill switch"],
        severity="High",
        title="Rollout or rollback plan is missing",
        laws=["Murphy's Law", "Law of Unintended Consequences"],
        why="Complex-system changes produce surprises; safe rollout and rollback reduce blast radius.",
        fix="Add rollout phases, canary/feature-flag strategy, rollback criteria, and data repair path if needed.",
        evidence="No rollback/revert/canary/feature flag language was found.",
    )

    add_if_missing(
        findings,
        text=t,
        required_terms=["log", "metric", "trace", "dashboard", "alert", "observability", "telemetry"],
        severity="High",
        title="Observability is not specified",
        laws=["Murphy's Law", "Map Is Not the Territory"],
        why="If the design cannot be observed, failures will be discovered late or diagnosed by guesswork.",
        fix="Specify logs, metrics, traces, dashboards, alerts, and correlation IDs for critical paths.",
        evidence="No observability/log/metric/trace/dashboard/alert language was found.",
    )

    add_if_missing(
        findings,
        text=t,
        required_terms=["test", "contract test", "integration test", "load test", "e2e", "unit test", "validation"],
        severity="Medium",
        title="Testing and validation plan is thin or absent",
        laws=["Testing Pyramid", "Pesticide Paradox"],
        why="Architecture decisions need executable checks, especially around boundaries and failure modes.",
        fix="Add unit, integration/contract, migration, load, and failure-mode tests proportional to risk.",
        evidence="No test/validation language was found.",
    )

    distributed_terms = [
        "microservice", "service", "rpc", "http", "grpc", "queue", "event", "kafka", "pubsub",
        "distributed", "async", "remote", "network", "stream", "sqs", "rabbitmq"
    ]
    add_if_missing(
        findings,
        text=t,
        trigger_terms=distributed_terms,
        required_terms=["timeout", "retry", "idempotent", "idempotency", "backpressure", "circuit breaker", "dead letter", "dlq"],
        severity="High",
        title="Distributed failure semantics are missing",
        laws=["Fallacies of Distributed Computing", "Murphy's Law"],
        why="Remote calls and async workflows fail through latency, duplication, reordering, partial outage, and retry storms.",
        fix="Document timeout budgets, bounded retries with backoff, idempotency/deduplication, backpressure, DLQ/replay, and circuit breakers.",
        evidence="Distributed terms were found, but timeout/retry/idempotency/backpressure/DLQ terms were not.",
    )

    data_terms = ["database", "db", "table", "schema", "cache", "event", "replica", "transaction", "migration", "data"]
    add_if_missing(
        findings,
        text=t,
        trigger_terms=data_terms,
        required_terms=["source of truth", "consistency", "transaction", "invariant", "reconcile", "reconciliation", "backup", "restore"],
        severity="High",
        title="Data ownership or consistency model is missing",
        laws=["CAP Theorem", "Tesler's Law", "Lehman's Laws"],
        why="Data designs fail when ownership, consistency, invariants, and repair paths are implicit.",
        fix="State source of truth, ownership, invariants, consistency expectations, backup/restore, and reconciliation strategy.",
        evidence="Data terms were found, but source-of-truth/consistency/reconciliation/backup terms were not.",
    )

    api_terms = ["api", "endpoint", "client", "sdk", "public", "consumer", "contract"]
    add_if_missing(
        findings,
        text=t,
        trigger_terms=api_terms,
        required_terms=["version", "deprecation", "backward", "backwards", "compatible", "compatibility", "contract test", "migration guide"],
        severity="High",
        title="API compatibility plan is missing",
        laws=["Hyrum's Law", "Postel's Law", "Least Astonishment"],
        why="Clients may depend on observed behavior even when docs say otherwise.",
        fix="Add versioning, compatibility rules, deprecation window, consumer communication, and contract tests.",
        evidence="API/client/contract terms were found, but compatibility/versioning/deprecation terms were not.",
    )

    security_terms = ["user", "customer", "tenant", "payment", "pii", "personal", "secret", "token", "auth", "permission", "data"]
    add_if_missing(
        findings,
        text=t,
        trigger_terms=security_terms,
        required_terms=["auth", "authorization", "authentication", "encrypt", "privacy", "permission", "least privilege", "audit"],
        severity="Medium",
        title="Security/privacy boundaries are not explicit",
        laws=["Murphy's Law", "Principle of Least Astonishment"],
        why="Systems that handle users, tenants, secrets, or data need explicit trust and access boundaries.",
        fix="Add authentication, authorization, least privilege, audit logging, encryption/privacy, and abuse cases.",
        evidence="Security-relevant terms were found, but auth/privacy/permission/audit terms were thin or absent.",
    )

    perf_terms = ["performance", "latency", "throughput", "scale", "slow", "p95", "p99", "cache", "parallel", "optimize"]
    add_if_missing(
        findings,
        text=t,
        trigger_terms=perf_terms,
        required_terms=["profile", "benchmark", "baseline", "measure", "load test", "slo", "p95", "p99"],
        severity="Medium",
        title="Performance plan lacks measurement",
        laws=["Premature Optimization", "Amdahl's Law", "Pareto Principle"],
        why="Optimization without workload and bottleneck evidence often adds complexity in the wrong place.",
        fix="Define workload/SLO, measure baseline, profile bottlenecks, then optimize and regression-test.",
        evidence="Performance/scale terms were found, but profile/benchmark/baseline/measurement terms were not.",
    )

    rewrite_terms = ["rewrite", "rebuild", "replace legacy", "greenfield", "new platform", "from scratch"]
    add_if_missing(
        findings,
        text=t,
        trigger_terms=rewrite_terms,
        required_terms=["strangler", "incremental", "parallel run", "characterization", "rollback", "migration", "reconcile"],
        severity="High",
        title="Rewrite plan lacks incremental migration controls",
        laws=["Second-System Effect", "Sunk Cost Fallacy", "Gall's Law"],
        why="Rewrites tend to expand scope and discover integration risk late.",
        fix="Add characterization tests, strangler/branch-by-abstraction plan, parallel run, reconciliation, and rollback.",
        evidence="Rewrite/rebuild terms were found, but incremental migration controls were not.",
    )

    plan_terms = ["estimate", "timeline", "deadline", "roadmap", "milestone", "ship", "delivery", "date"]
    add_if_missing(
        findings,
        text=t,
        trigger_terms=plan_terms,
        required_terms=["risk", "buffer", "contingency", "assumption", "scope cut", "dependency", "unknown"],
        severity="Medium",
        title="Plan lacks uncertainty and risk handling",
        laws=["Hofstadter's Law", "Ninety-Ninety Rule", "Brooks's Law"],
        why="Software schedules fail when integration, unknowns, and coordination cost are not represented.",
        fix="Use range estimates, assumptions, risk register, early de-risking milestones, and scope cuts.",
        evidence="Planning/timeline terms were found, but risk/buffer/assumption/scope-cut terms were not.",
    )

    return sorted(findings, key=lambda f: (SEVERITY_ORDER.get(f.severity, 99), f.title))


def to_markdown(input_path: Path, findings: list[Finding]) -> str:
    lines: list[str] = []
    lines.append("# Architecture Law Check")
    lines.append("")
    lines.append(f"Input: `{input_path}`")
    lines.append("")
    if not findings:
        lines.append("No major checklist omissions were detected by the heuristic scan.")
        lines.append("")
        lines.append("Still manually review tradeoffs, failure modes, security, data safety, and team fit.")
        return "\n".join(lines)

    counts: dict[str, int] = {}
    for f in findings:
        counts[f.severity] = counts.get(f.severity, 0) + 1
    summary = ", ".join(f"{severity}: {counts[severity]}" for severity in ["Blocker", "High", "Medium", "Low"] if severity in counts)
    lines.append(f"Findings: {len(findings)} ({summary})")
    lines.append("")
    for idx, finding in enumerate(findings, start=1):
        lines.append(f"## {idx}. {finding.severity}: {finding.title}")
        lines.append("")
        lines.append(f"**Evidence:** {finding.evidence}")
        lines.append("")
        lines.append(f"**Why it matters:** {finding.why}")
        lines.append("")
        lines.append(f"**Laws:** {', '.join(finding.laws)}")
        lines.append("")
        lines.append(f"**Fix:** {finding.fix}")
        lines.append("")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Heuristic architecture/design law checklist.")
    parser.add_argument("--input", "-i", required=True, help="Path to a Markdown/text design document.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown.")
    args = parser.parse_args(argv)

    input_path = Path(args.input)
    if not input_path.exists() or not input_path.is_file():
        print(f"error: input file not found: {input_path}", file=sys.stderr)
        return 2

    text = input_path.read_text(encoding="utf-8", errors="replace")
    findings = review(text)

    if args.json:
        print(json.dumps({"input": str(input_path), "findings": [asdict(f) for f in findings]}, indent=2))
    else:
        print(to_markdown(input_path, findings))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
