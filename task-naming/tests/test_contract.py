import json
import unittest
from pathlib import Path


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PLUGIN_ROOT.parent


class TaskNamingContractTests(unittest.TestCase):
    def test_package_is_explicit_skills_only(self):
        manifest = json.loads(
            (PLUGIN_ROOT / ".codex-plugin/plugin.json").read_text()
        )

        self.assertEqual(manifest["name"], "task-naming")
        self.assertEqual(manifest["version"], "0.5.4")
        self.assertEqual(manifest["skills"], "./skills/")
        self.assertNotIn("hooks", manifest)
        self.assertNotIn("mcpServers", manifest)
        self.assertNotIn("apps", manifest)

        for relative in ("hooks", "mcp", "evals", ".mcp.json", ".app.json"):
            self.assertFalse((PLUGIN_ROOT / relative).exists(), relative)

    def test_package_contains_only_the_small_manual_surface(self):
        files = {
            path.relative_to(PLUGIN_ROOT).as_posix()
            for path in PLUGIN_ROOT.rglob("*")
            if path.is_file() and "__pycache__" not in path.parts
        }
        self.assertEqual(
            files,
            {
                ".claude-plugin/plugin.json",
                ".codex-plugin/plugin.json",
                "CHANGELOG.md",
                "LICENSE",
                "README.md",
                "plugin.json",
                "skills/task-naming/SKILL.md",
                "skills/task-naming/agents/openai.yaml",
                "tests/test_contract.py",
            },
        )

    def test_skill_owns_exactly_three_manual_scopes(self):
        skill = (PLUGIN_ROOT / "skills/task-naming/SKILL.md").read_text()

        for text in (
            "$task-naming",
            "Current task",
            "Project folder",
            "Machine",
            "Verb object — Context",
            "25–45 characters",
            "dominant objective",
            "quick detours",
            "native task operations",
            "/rename <title>",
            "eligible",
            "changed",
            "unchanged",
            "deferred",
            "failed",
        ):
            self.assertIn(text, skill)

        for text in (
            "UserPromptSubmit",
            "codex app-server",
            "thread/name/set",
            "Automatic mode",
        ):
            self.assertNotIn(text, skill)

    def test_active_docs_use_the_action_first_contract(self):
        active_paths = (
            PLUGIN_ROOT / ".codex-plugin/plugin.json",
            PLUGIN_ROOT / "README.md",
            PLUGIN_ROOT / "skills/task-naming/SKILL.md",
        )
        active_text = "\n".join(path.read_text() for path in active_paths)

        self.assertIn("Verb object", active_text)
        self.assertIn("optional", active_text)
        self.assertNotIn("Subject — Outcome", active_text)

    def test_skill_requires_explicit_invocation(self):
        metadata = (
            PLUGIN_ROOT / "skills/task-naming/agents/openai.yaml"
        ).read_text()

        self.assertIn('display_name: "Task Naming"', metadata)
        self.assertIn("$task-naming", metadata)
        self.assertIn("allow_implicit_invocation: false", metadata)

    def test_marketplace_entry_still_points_to_plugin(self):
        catalog_path = REPO_ROOT / ".agents/plugins/marketplace.json"
        if not catalog_path.is_file():
            self.skipTest("marketplace catalog is external to installed cache")

        catalog = json.loads(catalog_path.read_text())
        entry = next(
            plugin
            for plugin in catalog["plugins"]
            if plugin["name"] == "task-naming"
        )

        self.assertEqual(entry["source"]["path"], "./task-naming")
        self.assertEqual(entry["category"], "Productivity")


if __name__ == "__main__":
    unittest.main()
