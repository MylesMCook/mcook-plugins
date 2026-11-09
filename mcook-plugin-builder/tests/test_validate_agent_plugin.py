from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "build-mcook-plugin"
    / "scripts"
    / "validate_agent_plugin.py"
)
SPEC = importlib.util.spec_from_file_location("validate_agent_plugin", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class AgentPluginValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        self.plugin = self.repo / "demo-plugin"
        (self.plugin / "skills" / "demo").mkdir(parents=True)
        (self.plugin / "skills" / "demo" / "SKILL.md").write_text(
            "---\nname: demo\ndescription: Demonstrate validation.\n---\n",
            encoding="utf-8",
        )
        (self.plugin / "server.py").write_text("print('server')\n", encoding="utf-8")
        self.write_json(
            self.plugin / "plugin.json",
            {
                "$schema": validator.PLUGIN_SCHEMA_ID,
                "name": "demo-plugin",
                "version": "1.0.0",
            },
        )
        self.write_json(
            self.plugin / "mcp.json",
            {
                "$schema": validator.MCP_SCHEMA_ID,
                "mcpServers": {
                    "demo": {
                        "type": "stdio",
                        "command": "uv",
                        "args": ["run", "${PLUGIN_ROOT}/server.py"],
                        "cwd": "${PLUGIN_ROOT}",
                    }
                },
            },
        )

    @staticmethod
    def write_json(path: Path, value: object) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")

    def test_valid_portable_package_and_marketplace(self) -> None:
        marketplace = self.repo / ".agents" / "plugins" / "marketplace.json"
        self.write_json(
            marketplace,
            {
                "name": "test",
                "plugins": [
                    {
                        "name": "demo-plugin",
                        "source": {"source": "local", "path": "./demo-plugin"},
                        "policy": {
                            "installation": "AVAILABLE",
                            "authentication": "ON_INSTALL",
                        },
                        "category": "Developer Tools",
                    }
                ],
            },
        )
        errors, warnings = validator.validate(
            self.plugin,
            marketplace=marketplace,
            marketplace_root=self.repo,
        )
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_versioned_installed_cache_layout_is_valid(self) -> None:
        installed = self.repo / "cache" / "demo-plugin" / "1.0.0"
        installed.parent.mkdir(parents=True)
        self.plugin.rename(installed)

        errors, warnings = validator.validate(installed)

        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_schema_and_containment_failures_are_reported(self) -> None:
        manifest = json.loads((self.plugin / "plugin.json").read_text(encoding="utf-8"))
        manifest["skills"] = "./skills"
        self.write_json(self.plugin / "plugin.json", manifest)
        mcp = json.loads((self.plugin / "mcp.json").read_text(encoding="utf-8"))
        mcp["mcpServers"]["demo"]["command"] = "../server.py"
        self.write_json(self.plugin / "mcp.json", mcp)

        errors, _ = validator.validate(self.plugin)

        self.assertTrue(any("Additional properties" in error for error in errors))
        self.assertTrue(any("one bare executable token" in error for error in errors))

    def test_remote_credentials_and_insecure_origin_fail(self) -> None:
        self.write_json(
            self.plugin / "mcp.json",
            {
                "$schema": validator.MCP_SCHEMA_ID,
                "mcpServers": {
                    "remote": {
                        "type": "streamable-http",
                        "url": "http://example.com/mcp",
                        "headers": {"Authorization": "Bearer nope"},
                    }
                },
            },
        )

        errors, _ = validator.validate(self.plugin)

        self.assertTrue(any("must use HTTPS" in error for error in errors))
        self.assertTrue(any("credential-bearing" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
