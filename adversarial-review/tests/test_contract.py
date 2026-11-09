import json
import unittest
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PLUGIN_ROOT.parent


class AdversarialReviewContractTests(unittest.TestCase):
    def test_manifest_uses_clean_v2_release(self):
        manifest = json.loads(
            (PLUGIN_ROOT / ".codex-plugin/plugin.json").read_text()
        )

        self.assertEqual(manifest["version"], "0.3.4")
        self.assertNotIn("+", manifest["version"])
        self.assertIn("Subagent V2", manifest["description"])

    def test_skill_is_v2_only_and_never_requires_permission_setup(self):
        skill = (
            PLUGIN_ROOT / "skills/adversarial-review/SKILL.md"
        ).read_text()

        self.assertIn("native Codex Subagent V2", skill)
        self.assertIn("legacy agent interface", skill)
        self.assertIn("Never ask the user to\n  switch permission modes", skill)
        self.assertNotIn("CALLER_MISUSE", skill)
        self.assertNotIn("parent task must already use", skill)

    def test_task_names_are_repeat_safe_v2_identifiers(self):
        files = [
            PLUGIN_ROOT / "skills/adversarial-review/SKILL.md",
            PLUGIN_ROOT
            / "skills/adversarial-review/references/reviewer-lenses.md",
            PLUGIN_ROOT
            / "skills/adversarial-review/references/subagent-review.md",
            PLUGIN_ROOT
            / "skills/adversarial-review/references/verdict-format.md",
        ]
        text = "\n".join(path.read_text() for path in files)

        for task_name_prefix in (
            "skeptic_r",
            "architect_r",
            "minimalist_r",
        ):
            self.assertIn(task_name_prefix, text)
        for example_name in (
            "skeptic_r1",
            "architect_r2",
            "minimalist_r3",
        ):
            self.assertRegex(example_name, r"^[a-z0-9_]+$")
        for invalid_name in (
            "codex_skeptic",
            "codex_architect",
            "codex_minimalist",
            "skeptic-r1",
            "architect-r1",
            "minimalist-r1",
            'task_name: "skeptic_rN"',
            'task_name: "architect_rN"',
            'task_name: "minimalist_rN"',
        ):
            self.assertNotIn(invalid_name, text)

    def test_repeated_invocations_allocate_one_fresh_shared_suffix(self):
        contract = (
            PLUGIN_ROOT
            / "skills/adversarial-review/references/subagent-review.md"
        ).read_text()

        self.assertIn("smallest positive integer `N`", contract)
        self.assertIn("Running, completed, failed, and interrupted", contract)
        self.assertIn("Use one shared run number for the whole trio", contract)
        self.assertIn("advance `N` for all three", contract)
        self.assertIn("partial earlier run", contract)
        self.assertIn("repeated invocations", contract)
        self.assertIn("Never pass a placeholder or uppercase", contract)

    def test_v2_contract_uses_fast_fresh_bounded_children(self):
        contract = (
            PLUGIN_ROOT
            / "skills/adversarial-review/references/subagent-review.md"
        ).read_text()

        self.assertIn('`fork_turns`, use `"none"`', contract)
        self.assertIn("`gpt-5.6-terra` and `high` reasoning", contract)
        self.assertIn("allow three minutes before considering interruption", contract)
        self.assertIn("stop at five total minutes", contract)
        self.assertIn("automatic approval review is active", contract)

    def test_active_contract_has_no_blunt_ninety_second_cap(self):
        active_contract = "\n".join(
            path.read_text()
            for path in (
                PLUGIN_ROOT / "skills/adversarial-review/SKILL.md",
                PLUGIN_ROOT
                / "skills/adversarial-review/references/subagent-review.md",
                PLUGIN_ROOT / "README.md",
                PLUGIN_ROOT / "DESIGN.md",
                PLUGIN_ROOT / "evals/README.md",
                PLUGIN_ROOT / "evals/evals.json",
            )
        )

        self.assertNotIn("90-second", active_contract)
        self.assertNotIn("90 seconds", active_contract)

    def test_reviewers_can_test_but_do_not_implement(self):
        prompt = (
            PLUGIN_ROOT
            / "skills/adversarial-review/references/reviewer-prompt.md"
        ).read_text()

        self.assertIn("run targeted tests, builds,", prompt)
        self.assertIn("Use the inherited approval flow normally.", prompt)
        self.assertIn("Do not implement fixes", prompt)

    def test_scope_defaults_preserve_momentum(self):
        skill = (
            PLUGIN_ROOT / "skills/adversarial-review/SKILL.md"
        ).read_text()

        self.assertIn("## Infer One Exact Scope", skill)
        self.assertIn("Exclude unrelated dirty or untracked state", skill)
        self.assertIn("do not begin a\nclarification loop", skill)
        self.assertIn("Protect the user's momentum", skill)

    def test_active_contract_has_no_permission_gate(self):
        active_contract = "\n".join(
            path.read_text()
            for path in (
                PLUGIN_ROOT / "skills/adversarial-review/SKILL.md",
                PLUGIN_ROOT
                / "skills/adversarial-review/references/subagent-review.md",
                PLUGIN_ROOT
                / "skills/adversarial-review/references/reviewer-prompt.md",
                PLUGIN_ROOT / "evals/evals.json",
            )
        )

        for stale_gate in (
            "CALLER_MISUSE",
            "rerun the review read-only",
            "parent task must already",
            "host-provided read-only child",
        ):
            self.assertNotIn(stale_gate, active_contract)

    def test_default_prompt_requires_no_mechanical_setup(self):
        metadata = (
            PLUGIN_ROOT
            / "skills/adversarial-review/agents/openai.yaml"
        ).read_text()
        manifest = json.loads(
            (PLUGIN_ROOT / ".codex-plugin/plugin.json").read_text()
        )

        self.assertIn("launch all three reviewers immediately", metadata)
        self.assertIn("run useful diagnostics", metadata)
        self.assertIn("without asking me to manage permissions or models", metadata)
        self.assertIn("allow_implicit_invocation: false", metadata)
        self.assertIn(
            "without asking me to configure anything",
            manifest["interface"]["defaultPrompt"][0],
        )

    def test_verdict_is_compact_and_actionable(self):
        verdict = (
            PLUGIN_ROOT
            / "skills/adversarial-review/references/verdict-format.md"
        ).read_text()

        self.assertIn("## Next Action", verdict)
        self.assertIn(
            "Only expand per-reviewer coverage when there is a failure",
            verdict,
        )
        self.assertNotIn("## Lead Judgment", verdict)

    def test_evals_cover_v2_failure_boundaries(self):
        data = json.loads((PLUGIN_ROOT / "evals/evals.json").read_text())
        names = {case["name"] for case in data["evals"]}

        self.assertTrue(
            {
                "codex-v2-trio-runs-exactly-three-children",
                "writable-parent-does-not-block-review",
                "scope-is-inferred-without-back-and-forth",
                "no-legacy-or-outside-reviewer-fallback",
                "standard-review-has-bounded-wait",
                "fast-v2-route-needs-no-user-choice",
                "repeated-review-in-one-parent-uses-fresh-task-names",
            }.issubset(names)
        )

    def test_evals_are_unique_and_complete(self):
        data = json.loads((PLUGIN_ROOT / "evals/evals.json").read_text())
        cases = data["evals"]
        names = [case["name"] for case in cases]

        self.assertGreaterEqual(len(cases), 11)
        self.assertEqual(len(names), len(set(names)))
        for case in cases:
            self.assertTrue(case["prompt"].strip())
            self.assertTrue(case["expected_output"].strip())
            self.assertEqual(case["files"], [])

    def test_release_gate_does_not_require_live_trio(self):
        readme = (PLUGIN_ROOT / "README.md").read_text()
        evals_readme = (PLUGIN_ROOT / "evals/README.md").read_text()

        self.assertIn("## Fast release gate", readme)
        self.assertIn("normal publish acceptance", readme)
        self.assertIn("optional behavioral evals", evals_readme)
        self.assertIn("Run the live cases below only", evals_readme)
        self.assertIn("0\\.3\\.3", readme)

    def test_retirement_routes_marketplace_to_thermos(self):
        catalog_path = REPO_ROOT / ".agents/plugins/marketplace.json"
        if not catalog_path.exists():
            self.skipTest("repository marketplace is not bundled in plugin cache")

        for relative in (".agents/plugins/marketplace.json", ".cursor-plugin/marketplace.json"):
            catalog = json.loads((REPO_ROOT / relative).read_text())
            names = {plugin["name"] for plugin in catalog["plugins"]}
            self.assertNotIn("adversarial-review", names)
            self.assertNotIn("pstack", names)
            self.assertIn("thermos", names)
        self.assertTrue((REPO_ROOT / "thermos/skills/adversarial-review/SKILL.md").is_file())


if __name__ == "__main__":
    unittest.main()
