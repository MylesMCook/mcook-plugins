"""Exercise native package installation/discovery in temporary config homes.

Uses existing Codex and Claude Code CLIs. No model calls, credentials, or live
marketplace changes. Run: uv run python -m unittest discover -s code-comments/tests
"""

import json
import os
from pathlib import Path
import queue
import shutil
import subprocess
import tempfile
import threading
import unittest


PACKAGE = Path(__file__).resolve().parents[1]
NAME = PACKAGE.name


class IngestionTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="code-comments-ingestion-")
        self.addCleanup(temporary.cleanup)
        self.scratch = Path(temporary.name)
        self.marketplace = self.scratch / "marketplace"
        self.package = self.marketplace / NAME
        shutil.copytree(PACKAGE, self.package, ignore=shutil.ignore_patterns("__pycache__"))

    def run_cli(self, args, env):
        result = subprocess.run(
            args, cwd=self.scratch, env=env, capture_output=True, text=True, timeout=30
        )
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        return result.stdout

    def test_codex_installation_and_skill_discovery(self):
        home = self.scratch / "codex-config"
        home.mkdir()
        env = {**os.environ, "CODEX_HOME": str(home)}
        catalog = self.marketplace / ".agents/plugins/marketplace.json"
        catalog.parent.mkdir(parents=True)
        catalog.write_text(json.dumps({
            "name": "comment-test",
            "plugins": [{"name": NAME,
                         "source": {"source": "local", "path": "./" + NAME},
                         "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                         "category": "Developer Tools"}],
        }))
        self.run_cli(["codex", "plugin", "marketplace", "add", str(self.marketplace), "--json"], env)
        result = self.run_cli(["codex", "plugin", "add", NAME + "@comment-test", "--json"], env)
        installed = Path(json.loads(result)["installedPath"])
        for source in self.package.rglob("*"):
            if source.is_file():
                self.assertEqual(source.read_bytes(), (installed / source.relative_to(self.package)).read_bytes())

        with (self.scratch / "server.log").open("w") as log:
            server = subprocess.Popen(
                ["codex", "app-server", "--stdio"], env=env, cwd=self.scratch,
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=log,
                text=True, bufsize=1,
            )
            responses = queue.Queue()

            def receive():
                for line in server.stdout:
                    responses.put(json.loads(line))

            reader = threading.Thread(target=receive, daemon=True)
            reader.start()

            def call(number, method, params):
                server.stdin.write(json.dumps({"id": number, "method": method, "params": params}) + "\n")
                server.stdin.flush()
                while True:
                    response = responses.get(timeout=15)
                    if response.get("id") == number:
                        self.assertNotIn("error", response, response)
                        return response["result"]

            try:
                call(1, "initialize", {"clientInfo": {"name": "comment-test", "version": "1.0"},
                                       "capabilities": {"experimentalApi": True}})
                server.stdin.write('{"method":"initialized"}\n')
                server.stdin.flush()
                plugin = call(2, "plugin/read", {"pluginName": NAME, "marketplacePath": str(catalog)})["plugin"]
                self.assertTrue(plugin["summary"]["installed"])
                self.assertTrue(plugin["summary"]["enabled"])
                self.assertEqual(plugin["mcpServers"], [])
                self.assertEqual(plugin["hooks"], [])
                self.assertEqual(len(plugin["skills"]), 1)
                skills = call(3, "skills/list", {"cwds": [str(self.scratch)], "forceReload": True})["data"][0]
                loaded = [s for s in skills["skills"] if s.get("pluginId") == NAME + "@comment-test"]
                self.assertEqual(len(loaded), 1)
                self.assertTrue(loaded[0]["enabled"])
                self.assertEqual(loaded[0]["name"], NAME + ":" + NAME)
                self.assertTrue(Path(loaded[0]["path"]).is_relative_to(installed))
            finally:
                server.terminate()
                try:
                    server.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    server.kill()
                    server.wait(timeout=5)
                reader.join(timeout=2)
                server.stdin.close()
                server.stdout.close()

    def test_claude_catalog_installation_and_skill_discovery(self):
        config = self.scratch / "claude-config"
        config.mkdir()
        env = {**os.environ, "CLAUDE_CONFIG_DIR": str(config),
               "CLAUDE_CODE_PLUGIN_CACHE_DIR": str(config / "plugins")}
        manifest = json.loads((self.package / "plugin.json").read_text())
        catalog = self.marketplace / ".claude-plugin/marketplace.json"
        catalog.parent.mkdir(parents=True)
        catalog.write_text(json.dumps({
            "name": "comment-test",
            "owner": {"name": "Test"},
            "plugins": [{"name": NAME, "source": "./" + NAME,
                         "description": manifest["description"], "version": manifest["version"]}],
        }))
        self.run_cli(["claude", "plugin", "validate", str(self.marketplace)], env)
        self.run_cli(["claude", "plugin", "marketplace", "add", str(self.marketplace)], env)
        self.run_cli(["claude", "plugin", "install", NAME + "@comment-test", "--json"], env)
        details = self.run_cli(["claude", "plugin", "details", NAME], env)
        self.assertIn("Skills (1)", details)
        self.assertIn(NAME, details)


if __name__ == "__main__":
    unittest.main()
