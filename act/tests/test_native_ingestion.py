"""Exercise native discovery in a disposable Codex home, without a model or auth."""

import json
import os
from pathlib import Path
import queue
import shutil
import subprocess
import tempfile
import threading
import unittest


ROOT = Path(__file__).resolve().parents[1]
BINARY = os.environ.get("CODEX_TEST_BINARY", "codex")


class NativeIngestionTests(unittest.TestCase):
    def test_installation_and_skill_discovery(self):
        with tempfile.TemporaryDirectory(prefix="act-native-") as tmp:
            scratch = Path(tmp)
            home = scratch / "home"
            home.mkdir()
            marketplace = scratch / "marketplace"
            package = marketplace / "act"
            shutil.copytree(ROOT, package, ignore=shutil.ignore_patterns("__pycache__"))
            catalog = marketplace / ".agents/plugins/marketplace.json"
            catalog.parent.mkdir(parents=True)
            catalog.write_text(json.dumps({
                "name": "act-test",
                "plugins": [{
                    "name": "act",
                    "source": {"source": "local", "path": "./act"},
                    "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                    "category": "Developer Tools",
                }],
            }))
            env = {**os.environ, "CODEX_HOME": str(home)}
            for args in (["marketplace", "add", str(marketplace)], ["add", "act@act-test"]):
                run = subprocess.run([BINARY, "plugin", *args, "--json"], env=env,
                                     cwd=scratch, capture_output=True, text=True, timeout=30)
                self.assertEqual(run.returncode, 0, run.stderr)
            installed = Path(json.loads(run.stdout)["installedPath"])
            for source in package.rglob("*"):
                if source.is_file():
                    self.assertEqual(source.read_bytes(),
                                     (installed / source.relative_to(package)).read_bytes())

            with (scratch / "server.log").open("w") as log:
                server = subprocess.Popen([BINARY, "app-server", "--stdio"], env=env,
                                          cwd=scratch, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                          stderr=log, text=True, bufsize=1)
                responses = queue.Queue()

                def receive():
                    for line in server.stdout:
                        try:
                            responses.put(json.loads(line))
                        except json.JSONDecodeError:
                            responses.put({"error": "non-JSON app-server output"})

                reader = threading.Thread(target=receive, daemon=True)
                reader.start()

                def call(number, method, params):
                    server.stdin.write(json.dumps({"id": number, "method": method, "params": params}) + "\n")
                    server.stdin.flush()
                    while True:
                        response = responses.get(timeout=15)
                        self.assertNotIn("error", response, response)
                        if response.get("id") == number:
                            return response["result"]

                try:
                    call(1, "initialize", {"clientInfo": {"name": "act-test", "version": "1.0"},
                                           "capabilities": {"experimentalApi": True}})
                    server.stdin.write('{"method":"initialized"}\n')
                    server.stdin.flush()
                    plugin = call(2, "plugin/read", {"pluginName": "act",
                                                     "marketplacePath": str(catalog)})["plugin"]
                    self.assertTrue(plugin["summary"]["installed"])
                    self.assertTrue(plugin["summary"]["enabled"])
                    self.assertEqual(plugin["mcpServers"], [])
                    self.assertEqual(plugin["hooks"], [])
                    self.assertEqual(len(plugin["skills"]), 1)
                    skills = call(3, "skills/list", {"cwds": [str(scratch)], "forceReload": True})["data"][0]
                    loaded = [s for s in skills["skills"] if s.get("pluginId") == "act@act-test"]
                    self.assertEqual(len(loaded), 1)
                    self.assertTrue(loaded[0]["enabled"])
                    self.assertEqual(loaded[0]["name"], "act:act")
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


if __name__ == "__main__":
    unittest.main()
