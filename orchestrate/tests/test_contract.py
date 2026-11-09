import json
import re
import unittest
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PLUGIN_ROOT.parent


class OrchestrateContractTests(unittest.TestCase):
    def test_trigger_is_explicit_and_excludes_external_runtimes(self):
        skill = (PLUGIN_ROOT / "skills/orchestrate/SKILL.md").read_text()
        frontmatter = skill.split("---", 2)[1]
        openai_yaml = (
            PLUGIN_ROOT / "skills/orchestrate/agents/openai.yaml"
        ).read_text()

        self.assertNotRegex(frontmatter, re.compile(r"\b(?:Sol|Terra|Luna|Spark)\b"))
        self.assertIn("the user invokes $orchestrate", frontmatter)
        self.assertIn("Do not trigger merely because", frontmatter)
        self.assertIn("OpenAI Agents SDK services", frontmatter)
        self.assertIn("small sequential tasks", frontmatter)
        self.assertIn("allow_implicit_invocation: false", openai_yaml)
        self.assertNotIn("allow_implicit_invocation: true", openai_yaml)

    def test_routing_contract_records_observed_metadata(self):
        contract = (
            PLUGIN_ROOT / "skills/orchestrate/references/task-contract.md"
        ).read_text()

        for field in (
            "requested_agent_type",
            "requested_model",
            "requested_reasoning_effort",
            "requested_history_mode",
            "configuration_precedence",
            "observed_agent_type",
            "observed_model",
            "observed_reasoning_effort",
            "observed_history_mode",
            "verification_status",
            "metadata_source",
            "fallback_reason",
        ):
            self.assertIn(f"{field}:", contract)

    def test_model_policy_tracks_current_routes_and_keeps_spark_conditional(self):
        policy = (
            PLUGIN_ROOT / "skills/orchestrate/references/routing-policy.md"
        ).read_text()

        self.assertIn("`gpt-5.6`", policy)
        self.assertIn("`gpt-5.6-terra`", policy)
        self.assertIn("`gpt-5.6-luna`", policy)
        self.assertIn("Codex-Spark, only when the host exposes it", policy)
        self.assertIn("Availability varies", policy)
        self.assertNotIn("research-preview option for very fast", policy)

    def test_skill_uses_native_tools_without_an_internal_version_gate(self):
        skill = (PLUGIN_ROOT / "skills/orchestrate/SKILL.md").read_text()
        policy = (
            PLUGIN_ROOT / "skills/orchestrate/references/routing-policy.md"
        ).read_text()
        contract = (
            PLUGIN_ROOT / "skills/orchestrate/references/task-contract.md"
        ).read_text()

        active_contract = (
            skill,
            policy,
            contract,
            (PLUGIN_ROOT / "skills/orchestrate/agents/openai.yaml").read_text(),
            (PLUGIN_ROOT / "plugin.json").read_text(),
            (PLUGIN_ROOT / ".codex-plugin/plugin.json").read_text(),
            (PLUGIN_ROOT / "README.md").read_text(),
            (PLUGIN_ROOT / "evals/evals.json").read_text(),
            (PLUGIN_ROOT / "evals/README.md").read_text(),
        )

        for content in active_contract:
            self.assertNotIn("Subagent V2", content)
            self.assertNotIn("native_subagent_v2", content)

        self.assertIn("native subagent spawn and supervision\ntools", skill)
        self.assertIn("If those tools are unavailable, stay single-agent", skill)
        self.assertIn("native_subagent_tools:", contract)
        self.assertRegex(
            skill, re.compile(r"Responses API multi-agent\s+implementations")
        )
        self.assertIn("Delegation is\ncoordination, not isolation.", skill)

    def test_evals_cover_high_risk_boundaries(self):
        data = json.loads((PLUGIN_ROOT / "evals/evals.json").read_text())
        names = {case["name"] for case in data["evals"]}

        self.assertTrue(
            {
                "small-task-does-not-fan-out",
                "large-uninvoked-task-does-not-trigger",
                "exact-model-fails-closed",
                "external-side-effects-stay-parent-gated",
                "agents-sdk-near-miss",
                "responses-api-multi-agent-near-miss",
            }.issubset(names)
        )

    def test_marketplace_entry_matches_plugin_root(self):
        catalog = json.loads(
            (REPO_ROOT / ".agents/plugins/marketplace.json").read_text()
        )
        entry = next(
            plugin for plugin in catalog["plugins"] if plugin["name"] == "orchestrate"
        )

        self.assertEqual(entry["source"]["path"], "./orchestrate")
        self.assertEqual(entry["category"], "Developer Tools")


if __name__ == "__main__":
    unittest.main()
