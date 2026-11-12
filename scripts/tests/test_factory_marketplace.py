"""Check the Factory (Droid) catalog against the documented plugin rules.

Source: https://docs.factory.com/harness/plugins
Droid reads `.factory-plugin/marketplace.json`, translates `.claude-plugin/`
packages at install time, loads MCP servers from `.mcp.json` when the root
`mcp.json` is an Agent Plugins file, and loads subagents from `droids/`. It
ignores components declared inside `plugin.json`.
"""

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def body(path):
    return path.read_text(encoding="utf-8").split("---", 2)[2]


class FactoryMarketplaceTests(unittest.TestCase):
    def setUp(self):
        self.factory = read_json(ROOT / ".factory-plugin/marketplace.json")
        self.claude = read_json(ROOT / ".claude-plugin/marketplace.json")

    def test_catalog_mirrors_the_claude_catalog(self):
        self.assertEqual(self.factory["name"], self.claude["name"])
        claude = {entry["name"]: entry for entry in self.claude["plugins"]}
        self.assertEqual([e["name"] for e in self.factory["plugins"]], list(claude))
        for entry in self.factory["plugins"]:
            with self.subTest(plugin=entry["name"]):
                self.assertEqual(entry["source"], claude[entry["name"]]["source"])
                self.assertEqual(entry["description"], claude[entry["name"]]["description"])
                package = (ROOT / entry["source"]).resolve()
                self.assertTrue(package.is_relative_to(ROOT))
                self.assertTrue((package / ".claude-plugin/plugin.json").is_file())

    def test_cursor_catalog_covers_the_claude_catalog(self):
        cursor = read_json(ROOT / ".cursor-plugin/marketplace.json")["plugins"]
        cursor = {entry["name"]: entry["source"] for entry in cursor}
        for entry in self.claude["plugins"]:
            self.assertEqual(cursor.get(entry["name"]), entry["source"], entry["name"])

    def test_manifest_components_are_also_on_disk_for_droid(self):
        for entry in self.factory["plugins"]:
            package = ROOT / entry["source"]
            manifest = read_json(package / ".claude-plugin/plugin.json")
            with self.subTest(plugin=entry["name"]):
                if "mcpServers" in manifest:
                    self.assertEqual(
                        read_json(package / ".mcp.json")["mcpServers"], manifest["mcpServers"]
                    )
                    for server in manifest["mcpServers"].values():
                        self.assertIn(server.get("type", "stdio"), ("stdio", "http", "sse"))
                for agent in manifest.get("agents", []):
                    source = package / agent
                    droid = package / "droids" / source.name
                    self.assertTrue(droid.is_file(), str(droid))
                    self.assertEqual(body(droid), body(source))


if __name__ == "__main__":
    unittest.main()
