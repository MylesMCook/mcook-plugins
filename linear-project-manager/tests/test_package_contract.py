"""Keep portable and native packaging aligned without contacting Linear."""

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class PackageContractTests(unittest.TestCase):
    def test_portable_manifests_preserve_linear_connection(self):
        self.assertTrue((ROOT / 'plugin.json').is_file(), 'A portable root manifest is required')
        manifest = json.loads((ROOT / 'plugin.json').read_text())
        native = json.loads((ROOT / '.codex-plugin/plugin.json').read_text())
        self.assertEqual(manifest['$schema'], 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json')
        self.assertEqual(manifest['name'], native['name'])
        self.assertEqual(manifest['version'], native['version'])
        portable = json.loads((ROOT / 'mcp.json').read_text())
        legacy = json.loads((ROOT / '.mcp.json').read_text())
        self.assertEqual(portable['$schema'], 'https://agent-plugins.org/schemas/1.0.0/mcp.schema.json')
        self.assertEqual(portable['mcpServers'], {
            'linear': {'type': 'streamable-http', 'url': 'https://mcp.linear.app/mcp'},
        })
        self.assertEqual(legacy['mcpServers'], {
            'linear': {'type': 'http', 'url': portable['mcpServers']['linear']['url']},
        })


if __name__ == '__main__':
    unittest.main()
