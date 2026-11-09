from __future__ import annotations

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/build-mcook-plugin/scripts/validate_agent_plugin.py'
spec = importlib.util.spec_from_file_location('sources_validator', SCRIPT)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)
PIN = 'a' * 40


class MarketplaceSourcesTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.catalog = self.root / 'marketplace.json'
        self.entry = {'name': 'advisor', 'source': {'source': 'git-subdir', 'url': 'https://github.com/owner/repo.git', 'path': './plugins/advisor', 'ref': PIN}, 'policy': {'installation': 'AVAILABLE', 'authentication': 'ON_USE'}, 'category': 'Developer Tools'}

    def check(self, plugin_root=None, duplicate=False):
        entries = [self.entry] * (2 if duplicate else 1)
        self.catalog.write_text(json.dumps({'plugins': entries}), encoding='utf-8')
        errors = []
        validator.validate_marketplace(self.catalog, self.root, plugin_root, 'advisor', errors)
        return errors

    def test_pinned_subdirectory_and_root_sources(self):
        self.assertEqual(self.check(), [])
        self.entry['source'] = {'source': 'url', 'url': 'https://github.com/owner/repo', 'sha': PIN}
        self.assertEqual(self.check(), [])

    def test_unsafe_urls_fail_without_echoing_credentials(self):
        for url in ['http://github.com/o/r', 'https://secret:password@github.com/o/r', 'https://github.com/o/r?token=secret', 'https://github.com/o/r#secret', 'file:///tmp/repo', 'https://localhost/o/r', 'https://127.0.0.1/o/r', 'https://example.com/o/r', 'https://github.com:bad/o/r', 'https://github.com/o/r\n', 'https://github.com/o/../r']:
            with self.subTest(url=url):
                self.entry['source']['url'] = url
                errors = self.check()
                self.assertTrue(errors)
                self.assertNotIn('secret', '\n'.join(errors))
                self.assertNotIn('password', '\n'.join(errors))

    def test_pin_is_required_and_unambiguous(self):
        for selector in [{}, {'ref': 'main'}, {'sha': 'abc123'}, {'ref': PIN, 'sha': PIN}, {'ref': None}, {'ref': 'g' * 40}]:
            with self.subTest(selector=selector):
                source = self.entry['source']
                source.pop('ref', None)
                source.pop('sha', None)
                source.update(selector)
                self.assertTrue(self.check())

    def test_path_safety_is_platform_independent(self):
        for path in ['', '.', '..', '../advisor', './plugins/../advisor', '/advisor', '//host/share', 'C:/advisor', 'C:\\advisor', 'plugins\\advisor', './plugins//advisor', 'plugins/%2e%2e/advisor', 'plugins/\x00advisor']:
            with self.subTest(path=path):
                self.entry['source']['path'] = path
                self.assertTrue(self.check())

    def test_existing_local_mapping_and_mismatch(self):
        self.entry['source'] = {'source': 'local', 'path': './advisor'}
        self.assertEqual(self.check(self.root / 'advisor'), [])
        self.assertTrue(self.check(self.root / 'other'))
        self.entry['source']['path'] = '../advisor'
        self.assertTrue(self.check())

    def test_local_symlink_escape(self):
        with tempfile.TemporaryDirectory() as outside:
            try:
                (self.root / 'advisor').symlink_to(outside, target_is_directory=True)
            except OSError:
                self.skipTest('symlink privileges unavailable')
            self.entry['source'] = {'source': 'local', 'path': './advisor'}
            self.assertTrue(self.check())

    def test_duplicate_policy_and_external_package_mode(self):
        self.assertTrue(self.check(duplicate=True))
        self.assertTrue(self.check(self.root / 'advisor'))
        self.entry['policy']['authentication'] = 'NEVER'
        self.assertTrue(self.check())

    def test_metadata_only_cli_and_invalid_combinations(self):
        self.assertEqual(self.check(), [])
        argv = ['validator', '--marketplace-entry', 'advisor', '--marketplace', str(self.catalog), '--marketplace-root', str(self.root)]
        with patch('sys.argv', argv), contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(validator.main(), 0)
            self.assertIn('metadata only', out.getvalue())
        for extra in [['some-plugin'], ['--require-openai-overlay']]:
            with patch('sys.argv', argv + extra), contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit) as raised:
                    validator.main()
                self.assertEqual(raised.exception.code, 2)

    def test_unknown_source_and_root_path_fail(self):
        self.entry['source']['source'] = 'npm'
        self.assertTrue(self.check())
        self.entry['source']['source'] = 'url'
        self.assertTrue(self.check())
