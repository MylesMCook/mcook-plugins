"""Install into a temporary Codex home and inspect supported app-server APIs.

No model, OAuth flow, or Linear mutations are involved.
Run with CODEX_TEST_BINARY to select a second installed Codex binary.
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

ROOT = Path(__file__).resolve().parents[1]
BINARY = os.environ.get('CODEX_TEST_BINARY', 'codex')


class NativeIngestionTests(unittest.TestCase):
    def test_installed_components_are_discoverable(self):
        self.assert_installed_components_are_discoverable(portable_only=False)

    def test_portable_core_components_are_discoverable(self):
        self.assert_installed_components_are_discoverable(portable_only=True)

    def assert_installed_components_are_discoverable(self, *, portable_only):
        with tempfile.TemporaryDirectory(prefix='linear native test ') as tmp:
            scratch = Path(tmp)
            home = scratch / 'home'
            home.mkdir()
            marketplace = scratch / 'marketplace'
            package = marketplace / ROOT.name
            shutil.copytree(ROOT, package, ignore=shutil.ignore_patterns('__pycache__'))
            if portable_only:
                self.assertTrue((package / 'plugin.json').is_file(), 'A portable root manifest is required')
                self.assertTrue((package / 'mcp.json').is_file(), 'Linear must be declared in portable mcp.json')
                shutil.rmtree(package / '.codex-plugin')
                (package / '.mcp.json').unlink()
            catalog = marketplace / '.agents/plugins/marketplace.json'
            catalog.parent.mkdir(parents=True)
            catalog.write_text(json.dumps({
                'name': 'linear-test',
                'plugins': [{'name': ROOT.name, 'source': {'source': 'local', 'path': './' + ROOT.name},
                             'policy': {'installation': 'AVAILABLE', 'authentication': 'ON_INSTALL'},
                             'category': 'Productivity'}],
            }))
            env = {**os.environ, 'CODEX_HOME': str(home)}
            for args in (['marketplace', 'add', str(marketplace)], ['add', ROOT.name + '@linear-test']):
                result = subprocess.run([BINARY, 'plugin', *args, '--json'], env=env,
                                        cwd=scratch, capture_output=True, text=True, timeout=20)
                self.assertEqual(result.returncode, 0, result.stderr)
            installed = Path(json.loads(result.stdout)['installedPath'])
            for source in package.rglob('*'):
                if source.is_file():
                    self.assertEqual(source.read_bytes(), (installed / source.relative_to(package)).read_bytes())
            with (scratch / 'server.log').open('w') as log:
                server = subprocess.Popen([BINARY, 'app-server', '--stdio'], env=env,
                                          cwd=scratch, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                          stderr=log, text=True, bufsize=1)
                responses = queue.Queue()
                def receive():
                    for line in server.stdout:
                        responses.put(json.loads(line))
                reader = threading.Thread(target=receive, daemon=True)
                reader.start()
                def call(number, method, params):
                    server.stdin.write(json.dumps({'id': number, 'method': method, 'params': params}) + '\n')
                    server.stdin.flush()
                    while True:
                        response = responses.get(timeout=15)
                        if response.get('id') == number:
                            self.assertNotIn('error', response, response)
                            return response['result']
                try:
                    call(1, 'initialize', {'clientInfo': {'name': 'linear-test', 'version': '1.0'},
                                           'capabilities': {'experimentalApi': True}})
                    server.stdin.write('{"method":"initialized"}\n')
                    server.stdin.flush()
                    plugin = call(2, 'plugin/read', {'pluginName': ROOT.name,
                                                     'marketplacePath': str(catalog)})['plugin']
                    self.assertTrue(plugin['summary']['installed'])
                    self.assertTrue(plugin['summary']['enabled'])
                    self.assertEqual(plugin['mcpServers'], ['linear'])
                    self.assertEqual(len(plugin['skills']), 1)
                    self.assertEqual(plugin['hooks'], [], 'The plugin must not register hooks')
                    runtime = call(3, 'hooks/list', {'cwds': [str(scratch)]})['data'][0]
                    self.assertEqual(runtime['errors'], [])
                    self.assertEqual(runtime['warnings'], [])
                    self.assertEqual(runtime['hooks'], [], 'No hooks may load from this isolated home')
                    skills = call(4, 'skills/list', {'cwds': [str(scratch)], 'forceReload': True})['data'][0]
                    loaded = [s for s in skills['skills'] if s.get('pluginId') == ROOT.name + '@linear-test']
                    self.assertEqual(len(loaded), 1)
                    self.assertTrue(loaded[0]['enabled'])
                    self.assertTrue(Path(loaded[0]['path']).is_relative_to(installed))
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


if __name__ == '__main__':
    unittest.main()
