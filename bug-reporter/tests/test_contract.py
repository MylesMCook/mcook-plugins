import json
import re
import unittest
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PLUGIN_ROOT.parent
SKILL_ROOT = PLUGIN_ROOT / "skills/bug-reporter"


class BugReporterContractTests(unittest.TestCase):
    def test_manifests_share_clean_release_identity(self):
        portable = json.loads((PLUGIN_ROOT / "plugin.json").read_text())
        openai = json.loads(
            (PLUGIN_ROOT / ".codex-plugin/plugin.json").read_text()
        )

        self.assertEqual(portable["name"], "bug-reporter")
        self.assertEqual(openai["name"], portable["name"])
        self.assertEqual(openai["version"], portable["version"])
        self.assertEqual(portable["version"], "0.2.1")
        self.assertNotIn("+", portable["version"])
        self.assertEqual(
            portable["extensions"]["com.openai"]["interface"]["capabilities"],
            ["Read", "Write"],
        )
        self.assertEqual(openai["interface"]["capabilities"], ["Read", "Write"])

    def test_package_remains_skills_only(self):
        portable = json.loads((PLUGIN_ROOT / "plugin.json").read_text())
        openai = json.loads(
            (PLUGIN_ROOT / ".codex-plugin/plugin.json").read_text()
        )

        self.assertNotIn("mcpServers", portable)
        self.assertNotIn("mcpServers", openai)
        self.assertNotIn("apps", openai)
        self.assertFalse((PLUGIN_ROOT / "mcp.json").exists())
        self.assertFalse((PLUGIN_ROOT / ".mcp.json").exists())
        self.assertFalse((PLUGIN_ROOT / ".app.json").exists())
        self.assertFalse((PLUGIN_ROOT / "hooks").exists())

    def test_skill_has_only_supported_frontmatter_fields(self):
        skill = (SKILL_ROOT / "SKILL.md").read_text()
        frontmatter = skill.split("---", 2)[1]
        top_level = {
            line.split(":", 1)[0]
            for line in frontmatter.splitlines()
            if line and not line.startswith(" ") and ":" in line
        }

        self.assertEqual(top_level, {"name", "description"})
        self.assertIn("requested deliverable is a bug report", frontmatter)
        self.assertIn("Do not use when the", frontmatter)
        self.assertIn("only to implement a fix", frontmatter)

    def test_core_contract_covers_fix_ready_handoff(self):
        skill = (SKILL_ROOT / "SKILL.md").read_text()

        required = (
            "Choose the working mode",
            "one independently fixable defect per report",
            "numbered, atomic reproduction steps",
            "reproduction rate",
            "last known good",
            "first known bad",
            "Observed:",
            "Inferred:",
            "Unknown:",
            "acceptance criteria",
            "Never invent versions",
            "Remove every unused heading",
            "Always write the finished report to a Markdown file",
            "Keep causal hypotheses and fix ideas out of the title and summary",
            "Next probe",
        )
        for phrase in required:
            self.assertIn(phrase, skill)

    def test_report_handoff_is_deterministically_file_first(self):
        skill = (SKILL_ROOT / "SKILL.md").read_text()

        for phrase in (
            "Do not print or duplicate",
            "the report body in chat",
            "<workspace-root>/bug-reports/YYYY-MM-DD-<title-slug>.md",
            "host's local date",
            "truncating it to 64 characters",
            "Use `bug-report` if nothing remains",
            "append the lowest available numeric suffix",
            "read the saved file back",
            "Saved: [filename.md](/absolute/path/to/filename.md)",
            "fall back to putting",
            "the report body in chat",
        ):
            self.assertIn(phrase, skill)

        self.assertNotIn("paste-ready Markdown report", skill)

    def test_security_and_mutation_guards_are_explicit(self):
        skill = (SKILL_ROOT / "SKILL.md").read_text()
        evidence = (
            SKILL_ROOT / "references/evidence-by-defect.md"
        ).read_text()

        self.assertIn("private disclosure channel", skill)
        self.assertIn("Never put exploit", skill)
        self.assertIn("Do not reproduce against production", skill)
        self.assertIn("Never\n  retry a non-idempotent operation", skill)
        self.assertIn("Stop public drafting or submission", evidence)

    def test_evidence_guide_covers_major_failure_classes(self):
        evidence = (
            SKILL_ROOT / "references/evidence-by-defect.md"
        ).read_text()

        for heading in (
            "## Crash, panic, or hang",
            "## Performance, resource use, or leak",
            "## Intermittent, timing, or concurrency failure",
            "## Regression",
            "## Build, install, dependency, or test failure",
            "## Incorrect result, data, or state transition",
            "## UI, interaction, or accessibility defect",
            "## API, CLI, integration, or distributed service",
            "## Hardware, operating system, or infrastructure",
            "## Security or privacy vulnerability",
            "## Documentation or usability defect",
        ):
            self.assertIn(heading, evidence)

    def test_template_is_adaptive_and_agent_ready(self):
        template = (SKILL_ROOT / "assets/bug-report.md").read_text()

        for heading in (
            "## Summary",
            "## Environment",
            "## Preconditions",
            "## Steps to reproduce",
            "## Expected behavior",
            "## Actual behavior",
            "## Impact and scope",
            "## Evidence",
            "## Analysis",
            "## Acceptance criteria",
            "## Missing evidence",
        ):
            self.assertIn(heading, template)
        self.assertIn("Delete every unused heading", template)
        self.assertIn("single safest, highest-information action", template)

    def test_concision_gate_blocks_llm_report_bloat(self):
        skill = (SKILL_ROOT / "SKILL.md").read_text()

        for phrase in (
            "There is no minimum section count",
            "Do not add a preamble",
            "State each fact once",
            "Excerpt artifacts to the smallest useful span",
            "Concision does not outrank correctness",
        ):
            self.assertIn(phrase, skill)

    def test_local_markdown_links_resolve(self):
        for path in (
            SKILL_ROOT / "SKILL.md",
            PLUGIN_ROOT / "README.md",
        ):
            text = path.read_text()
            for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", text):
                if (
                    "://" in target
                    or target.startswith("#")
                    or target.startswith("/absolute/")
                ):
                    continue
                self.assertTrue(
                    (path.parent / target).resolve().exists(),
                    f"missing link target {target} in {path}",
                )

    def test_openai_prompts_match_the_skill(self):
        manifest = json.loads(
            (PLUGIN_ROOT / ".codex-plugin/plugin.json").read_text()
        )
        prompts = manifest["interface"]["defaultPrompt"]
        metadata = (SKILL_ROOT / "agents/openai.yaml").read_text()

        self.assertLessEqual(len(prompts), 3)
        self.assertTrue(all(len(prompt) <= 128 for prompt in prompts))
        self.assertIn("$bug-reporter", metadata)
        self.assertIn("evidence-based", metadata)

    def test_marketplace_entry_matches_plugin_root(self):
        catalog_path = REPO_ROOT / ".agents/plugins/marketplace.json"
        if not catalog_path.exists():
            self.skipTest("repository marketplace is not bundled in plugin cache")

        catalog = json.loads(catalog_path.read_text())
        entry = next(
            plugin
            for plugin in catalog["plugins"]
            if plugin["name"] == "bug-reporter"
        )

        self.assertEqual(entry["source"]["path"], "./bug-reporter")
        self.assertEqual(entry["category"], "Developer Tools")


if __name__ == "__main__":
    unittest.main()
