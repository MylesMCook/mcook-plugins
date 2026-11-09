#!/usr/bin/env python3
"""
Validate a Laws of UX critique against the required output format.

Usage:
    python3 scripts/validate-output.py < critique.md
    python3 scripts/validate-output.py --file critique.md

Exit codes:
    0 - valid
    1 - invalid (errors printed to stderr, one per line)
    2 - usage error

Checks:
    1. Top-level "Laws of UX critique" header present.
    2. "Context read:" and "Selected lenses:" lines present and non-empty.
    3. Exactly 2-4 law sections (### N. lines).
    4. Each law section has all four required bold subsections:
       How it applies here, Recommendation, Why this follows from the law, Watch-out.
    5. "Prioritized next moves" section present with at least 1 numbered item.
    6. No filler phrases (configurable list of vague-UX-advice patterns).
    7. Each "Why this follows from the law" subsection mentions a mechanism, not generic advice
       (heuristic: contains a verb related to perception, decision, memory, attention, or motor action).

If a check seems wrong on a real critique, fix the validator instead of papering over it
in SKILL.md. Pattern misfires should be rare; if you see them often, tighten the patterns.
"""
import argparse
import re
import sys

REQUIRED_SUBSECTIONS = [
    "How it applies here",
    "Recommendation",
    "Why this follows from the law",
    "Watch-out",
]

FILLER_PATTERNS = [
    (re.compile(r"\bbest practices?\b", re.I), "best practices"),
    (re.compile(r"\bconsider improving\b", re.I), "consider improving"),
    (re.compile(r"\bgenerally speaking\b", re.I), "generally speaking"),
    (re.compile(r"\bin general\b", re.I), "in general"),
    (re.compile(r"\bit is important to\b", re.I), "it is important to"),
    (re.compile(r"\bgood UX\b", re.I), "good UX (vague - name the mechanism)"),
    (re.compile(r"\buser-friendly\b", re.I), "user-friendly (vague - name the user task or friction)"),
    (re.compile(r"\bmight want to\b", re.I), "might want to (commit or remove)"),
    (re.compile(r"\bcould potentially\b", re.I), "could potentially (commit or remove)"),
]

# Heuristic: a real "why this follows" should reference a mechanism, not just restate the recommendation.
MECHANISM_VERBS = re.compile(
    r"\b(reduces?|increases?|narrows?|expands?|directs?|breaks?|chunks?|"
    r"recalls?|remembers?|forgets?|notices?|misses?|scans?|"
    r"decides?|chooses?|hesitates?|defaults?|expects?|"
    r"perceives?|groups?|separates?|distinguishes?|"
    r"completes?|abandons?|persists?|resumes?|"
    r"accepts?|translates?|normalizes?|signals?|conveys?|anchors?|"
    r"preserves?|maintains?|establishes?|reinforces?|"
    r"speeds?|slows?|delays?|interrupts?|sustains?|"
    r"matches?|mismatches?|aligns?|conflicts?)\b",
    re.I,
)


def validate(text: str) -> list[str]:
    errors: list[str] = []
    lines = text.split("\n")

    # Check 1: top-level header
    if not re.search(r"^##\s+Laws of UX critique", text, re.MULTILINE):
        errors.append(
            "missing top-level '## Laws of UX critique' header\n"
            "   the output must open with this exact heading"
        )

    # Check 2: Context read and Selected lenses
    if not re.search(r"\*\*Context read:\*\*\s+\S", text):
        errors.append(
            "missing or empty '**Context read:**' line\n"
            "   state the artifact and key assumption in one line"
        )
    if not re.search(r"\*\*Selected lenses:\*\*\s+\S", text):
        errors.append(
            "missing or empty '**Selected lenses:**' line\n"
            "   list the 2-4 law names you applied"
        )

    # Check 3: count law sections
    section_headers = re.findall(r"^###\s+\d+\.\s+(.+)$", text, re.MULTILINE)
    n = len(section_headers)
    if n < 2:
        errors.append(
            f"only {n} law section(s) found; need 2-4\n"
            f"   format: '### 1. Law name - issue/opportunity'"
        )
    elif n > 4:
        errors.append(
            f"{n} law sections found; max is 4\n"
            f"   pick the 2-4 most relevant; drop the rest or merge into prioritized next moves"
        )

    # Check 4: each section has all four required subsections
    sections = re.split(r"^###\s+\d+\.\s+", text, flags=re.MULTILINE)[1:]
    for i, section in enumerate(sections, 1):
        # Cut at the next ### or ## header
        section_body = re.split(r"^(?:###|##)\s+", section, flags=re.MULTILINE)[0]
        for sub in REQUIRED_SUBSECTIONS:
            pattern = re.compile(rf"\*\*{re.escape(sub)}:\*\*\s+\S", re.MULTILINE)
            if not pattern.search(section_body):
                errors.append(
                    f"section {i} missing or empty '**{sub}:**' subsection\n"
                    f"   each law block needs all four: How it applies here, "
                    f"Recommendation, Why this follows from the law, Watch-out"
                )

    # Check 5: prioritized next moves
    if not re.search(r"^##\s+Prioritized next moves", text, re.MULTILINE):
        errors.append(
            "missing '## Prioritized next moves' section\n"
            "   add a numbered list with the highest-impact changes first"
        )
    else:
        next_moves_block = text.split("## Prioritized next moves", 1)[1]
        numbered_items = re.findall(r"^\s*\d+\.\s+\S", next_moves_block, re.MULTILINE)
        if len(numbered_items) < 1:
            errors.append(
                "'Prioritized next moves' section has no numbered items\n"
                "   add at least one prioritized change"
            )

    # Check 6: filler-phrase detection
    for pattern, label in FILLER_PATTERNS:
        if pattern.search(text):
            errors.append(
                f"filler phrase detected: {label}\n"
                f"   replace with a specific, mechanism-grounded statement"
            )

    # Check 7: mechanism check on each "Why this follows" subsection
    why_blocks = re.findall(
        r"\*\*Why this follows from the law:\*\*\s+(.+?)(?=\n\s*-\s+\*\*|\n###|\n##|\Z)",
        text,
        re.DOTALL,
    )
    for i, why in enumerate(why_blocks, 1):
        if not MECHANISM_VERBS.search(why):
            errors.append(
                f"section {i} 'Why this follows from the law' lacks a mechanism verb\n"
                f"   explain HOW the law produces the effect (e.g., 'reduces decision time', "
                f"'narrows attention', 'increases recall'), not just restate the recommendation"
            )

    return errors


def main() -> int:
    p = argparse.ArgumentParser(description="Validate a Laws of UX critique output")
    p.add_argument("--file", help="read critique from file instead of stdin")
    args = p.parse_args()

    if args.file:
        try:
            with open(args.file, encoding="utf-8") as f:
                text = f.read()
        except OSError as e:
            print(f"cannot read {args.file}: {e}", file=sys.stderr)
            return 2
    else:
        text = sys.stdin.read()

    if not text.strip():
        print("empty input - nothing to validate", file=sys.stderr)
        return 1

    errors = validate(text)
    if errors:
        for e in errors:
            print(e, file=sys.stderr)
            print(file=sys.stderr)
        print(f"FAIL: {len(errors)} issue(s)", file=sys.stderr)
        return 1

    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
