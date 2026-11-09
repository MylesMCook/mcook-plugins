"""Check the documented claude.ai import rules without provider credentials.

Source: https://platform.claude.com/docs/en/manage-claude/plugins-api#upload-requirements
These checks do not replace Anthropic's authenticated server-side validation.
"""

import json
from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[2]


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


class ClaudeMarketplaceTests(unittest.TestCase):
    def test_each_entry_is_a_complete_cloud_package(self):
        catalog = read_json(ROOT / ".claude-plugin/marketplace.json")
        names = [entry["name"] for entry in catalog["plugins"]]
        self.assertEqual(len(names), len(set(names)))
        for entry in catalog["plugins"]:
            with self.subTest(plugin=entry["name"]):
                package = (ROOT / entry["source"]).resolve()
                self.assertTrue(package.is_relative_to(ROOT))
                manifest = read_json(package / ".claude-plugin/plugin.json")
                portable = read_json(package / "plugin.json")
                codex = read_json(package / ".codex-plugin/plugin.json")
                for key in ("name", "version", "description"):
                    self.assertEqual(entry[key], manifest[key])
                    self.assertEqual(portable[key], manifest[key])
                    if key in ("name", "version"):
                        self.assertEqual(codex[key], manifest[key])
                self.assertRegex(manifest["name"], r"^[a-z0-9-]{1,64}$")
                self.assertLessEqual(len(manifest["description"]), 500)
                self.assertLessEqual(len(manifest.get("displayName", "")), 64)
                self.assertFalse((package / "bin").exists())
                self.assertFalse((package / "hooks/hooks.json").exists())
                files = [path for path in package.rglob("*") if path.is_file()]
                self.assertLessEqual(len(files), 5000)
                self.assertLessEqual(sum(path.stat().st_size for path in files), 200_000_000)
                for path in package.rglob("*"):
                    relative = path.relative_to(package)
                    self.assertFalse(path.is_symlink(), str(path))
                    self.assertRegex(relative.as_posix(), r"^[A-Za-z0-9_ .\-/(),]+$")
                    self.assertNotIn("..", relative.parts)
                    self.assertLessEqual(len(relative.parts), 12)
                    self.assertLessEqual(len(relative.as_posix()), 472)
                    self.assertTrue(all(len(part) <= 255 for part in relative.parts))
                    self.assertNotEqual(path.suffix.lower(), ".zip")
                # Only the canonical Claude manifest counts; portable and Codex
                # manifests remain alongside it for the other clients.
                self.assertEqual(len(list(package.rglob(".claude-plugin/plugin.json"))), 1)
                skill_names = []
                for path in package.rglob("SKILL.md"):
                    text = path.read_text(encoding="utf-8")
                    self.assertTrue(text.startswith("---\n"), str(path))
                    metadata = yaml.safe_load(text.split("---", 2)[1])
                    for key in ("name", "description"):
                        self.assertIsInstance(metadata[key], str)
                        self.assertNotRegex(metadata[key], r"</?[A-Za-z][^>]*>")
                    skill_names.append(metadata["name"])
                self.assertEqual(len(skill_names), len(set(skill_names)))

    def test_components_live_in_the_plugin_manifest(self):
        for entry in read_json(ROOT / ".claude-plugin/marketplace.json")["plugins"]:
            package = ROOT / entry["source"]
            manifest = read_json(package / ".claude-plugin/plugin.json")
            self.assertNotIn("agents", entry)
            self.assertNotIn("mcpServers", entry)
            for agent in manifest.get("agents", []):
                path = (package / agent).resolve()
                self.assertTrue(path.is_relative_to(package.resolve()))
                self.assertTrue(path.is_file())
        assistant = read_json(ROOT / "assistant-ui/.claude-plugin/plugin.json")
        self.assertEqual(assistant["mcpServers"]["assistant-ui"]["type"], "http")
        explainer = read_json(ROOT / "explainer/.claude-plugin/plugin.json")
        self.assertEqual(explainer["mcpServers"]["explainer"]["command"], "node")

    def test_fabric_stays_available_in_codex_and_cursor(self):
        for catalog in (".agents/plugins/marketplace.json", ".cursor-plugin/marketplace.json"):
            self.assertIn("fabric-mcp-server", [entry["name"] for entry in read_json(ROOT / catalog)["plugins"]])
        self.assertNotIn("fabric-mcp-server", [entry["name"] for entry in read_json(ROOT / ".claude-plugin/marketplace.json")["plugins"]])
        self.assertTrue((ROOT / "fabric-mcp-server/bin/fabric-mcp-server.exe").is_file())


if __name__ == "__main__":
    unittest.main()
