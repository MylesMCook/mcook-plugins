import json
import unittest
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
SKILL_PATH = PLUGIN_ROOT / "skills/product-wrangler/SKILL.md"
EVALS_PATH = PLUGIN_ROOT / "evals/evals.json"


class ProductWranglerContractTests(unittest.TestCase):
    def test_package_is_small_skills_only_and_versioned_consistently(self):
        portable = json.loads((PLUGIN_ROOT / "plugin.json").read_text())
        openai = json.loads(
            (PLUGIN_ROOT / ".codex-plugin/plugin.json").read_text()
        )

        self.assertEqual(portable["name"], "product-wrangler")
        self.assertEqual(portable["version"], "0.2.0")
        self.assertEqual(openai["name"], portable["name"])
        self.assertEqual(openai["version"], portable["version"])
        self.assertEqual(openai["skills"], "./skills/")

        for manifest in (portable, openai):
            for key in ("hooks", "mcpServers", "apps"):
                self.assertNotIn(key, manifest)

        for relative in ("hooks", "mcp", "mcp.json", ".mcp.json", ".app.json"):
            self.assertFalse((PLUGIN_ROOT / relative).exists(), relative)

    def test_skill_is_bounded_and_under_portable_size_limit(self):
        skill = SKILL_PATH.read_text()

        self.assertLessEqual(len(skill.splitlines()), 500)
        for text in (
            "A polished version of the wrong product is a failure",
            "This skill changes execution discipline, not authority",
            "Bound the active product surface",
            "Do not chase every defect in a large application",
            "Do not use for greenfield builds",
            "Do not activate for",
            "review, critique, or report where implementation is not requested",
        ):
            self.assertIn(text, skill)

        self.assertNotIn("fixed iteration", skill.lower())
        self.assertNotIn("frontend-react", skill)

    def test_evidence_hierarchy_and_falsification_are_explicit(self):
        skill = SKILL_PATH.read_text()
        hierarchy = [
            "1. Current user brief and explicit acceptance criteria",
            "2. Current product or domain contracts and business invariants",
            "3. Tests, data model, and functioning workflows",
            "4. Representative content and data",
            "5. Existing interface and styling",
        ]

        positions = [skill.index(item) for item in hierarchy]
        self.assertEqual(positions, sorted(positions))

        for text in (
            "contradictions between sources",
            "assumptions and confidence level",
            "visual-direction rationale based on audience, domain, task density",
            "State the strongest plausible alternative product thesis",
            "Identify evidence that contradicts the selected thesis",
            "Every major change must be traceable",
        ):
            self.assertIn(text, skill)

    def test_workflow_ledger_requires_before_and_after_outcomes(self):
        skill = SKILL_PATH.read_text()

        for text in (
            "Primary user outcome",
            "Baseline behavior or failure",
            "Expected observable result",
            "Selected change",
            "Post-fix evidence from the same journey",
            "Remaining uncertainty",
            "Replay the same journeys",
            "comparable starting state",
            "Cold-start pass",
            "Revisit the thesis",
            "changes only cosmetics",
        ):
            self.assertIn(text, skill)

        self.assertIn("Use exactly one completion state", skill)
        self.assertIn("### COMPLETE", skill)
        self.assertIn("### PARTIAL", skill)
        self.assertIn("### BLOCKED", skill)

    def test_safe_execution_preflight_fails_closed(self):
        skill = SKILL_PATH.read_text()

        for text in (
            "git status --short",
            "rollback boundary",
            "localhost proxies to any shared or production service",
            "Localhost is not proof of a sandbox",
            "Data and outbound effects",
            "email and notifications",
            "billing and payments",
            "queues, jobs, and automations",
            "Safe mutation",
            "Read-only browser",
            "No browser verification",
            "Missing proof means read-only",
            "Do not overwrite, revert, reformat, stage, or absorb unrelated user work",
        ):
            self.assertIn(text, skill)

    def test_metadata_allows_only_precise_implicit_activation(self):
        metadata = (
            PLUGIN_ROOT / "skills/product-wrangler/agents/openai.yaml"
        ).read_text()
        skill = SKILL_PATH.read_text()

        self.assertIn('display_name: "Product Wrangler"', metadata)
        self.assertIn("$product-wrangler", metadata)
        self.assertIn("allow_implicit_invocation: true", metadata)
        self.assertIn("existing runnable web app", skill)
        self.assertIn("narrow isolated UI fixes", skill)
        self.assertIn("review-only audits", skill)

    def test_behavioral_eval_matrix_covers_review_findings(self):
        document = json.loads(EVALS_PATH.read_text())
        names = {case["name"] for case in document["evals"]}
        required = {
            "direct-broad-trigger",
            "indirect-broad-trigger",
            "narrow-ui-non-trigger",
            "greenfield-non-trigger",
            "review-only-non-trigger",
            "conflicting-stale-product-evidence",
            "generic-redesign-is-rejected",
            "real-service-backed-app-stays-read-only",
            "external-effects-require-proof",
            "dirty-worktree-preserves-user-changes",
            "missing-browser-prevents-complete",
            "missing-credentials-prevents-mutating-proof",
            "cosmetic-only-cycle-does-not-count",
            "premature-completion-is-rejected",
            "scope-is-bounded-without-fixed-pass-count",
            "material-ambiguity-does-not-become-confident-invention",
            "authority-does-not-expand",
        }

        self.assertEqual(document["skill_name"], "product-wrangler")
        self.assertTrue(required.issubset(names), required - names)
        self.assertEqual(len(names), len(document["evals"]))

        fixture_required = {
            "conflicting-stale-product-evidence",
            "real-service-backed-app-stays-read-only",
            "external-effects-require-proof",
            "dirty-worktree-preserves-user-changes",
            "scope-is-bounded-without-fixed-pass-count",
            "material-ambiguity-does-not-become-confident-invention",
        }

        for case in document["evals"]:
            self.assertTrue(case["prompt"].strip(), case["name"])
            self.assertTrue(case["expected_output"].strip(), case["name"])
            if case["name"] in fixture_required:
                self.assertTrue(case["files"], case["name"])
            for relative in case["files"]:
                self.assertTrue((PLUGIN_ROOT / relative).is_file(), relative)

    def test_eval_readme_rejects_shape_only_validation(self):
        readme = (PLUGIN_ROOT / "evals/README.md").read_text()

        for text in (
            "Package validators and contract tests do not replace these model runs",
            "at least two materially different model families",
            "real disposable application",
            "service that must remain read-only",
            "returns COMPLETE without before/after journey evidence blocks release",
        ):
            self.assertIn(text, readme)


if __name__ == "__main__":
    unittest.main()
