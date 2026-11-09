"""Exercise sync safety and reproducibility using local Git upstreams."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location('frontend_sync', Path(__file__).parents[1] / 'sync_frontend_react.py')
sync = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = sync
SPEC.loader.exec_module(sync)
CONFIGURED_DESTINATIONS = {skill.destination for upstream in sync.UPSTREAMS for skill in upstream.skills}


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], text=True, stderr=subprocess.PIPE).strip()


def commit(root):
    git(root, 'add', '.')
    git(root, '-c', 'user.name=Sync Test', '-c', 'user.email=sync@example.invalid', 'commit', '-qm', 'fixture')


def snapshot(root):
    return {str(p.relative_to(root)): p.read_bytes() for p in root.rglob('*') if p.is_file() and '.git' not in p.parts}


class SyncTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.repo, self.sources = root / 'repo', root / 'sources'
        self.plugin = self.repo / 'frontend-react'
        (self.plugin / 'skills').mkdir(parents=True)
        git(self.repo, 'init', '-q')
        self.upstreams = (
            sync.Upstream('composition', 'composition', 'unused', 'main', (sync.SkillSource('skills/vercel-composition-patterns', 'vercel-composition-patterns'),)),
            sync.Upstream('types', 'types', 'unused', 'main', (sync.SkillSource('skills/typescript-advanced-types', 'typescript-advanced-types'),)),
        )
        for upstream in self.upstreams:
            checkout = self.sources / upstream.checkout
            skill = checkout / upstream.skills[0].source
            (skill / 'agents').mkdir(parents=True)
            (skill / 'SKILL.md').write_text(f'---\nname: {skill.name}\ndescription: Fixture skill.\n---\n\nFixture.\n')
            (skill / 'agents/openai.yaml').write_text('interface:\n  display_name: "Canonical metadata"\n')
            git(checkout, 'init', '-q')
            commit(checkout)
        owned = self.plugin / 'skills/base-ui-stylex'
        owned.mkdir()
        (owned / 'SKILL.md').write_text('Plugin-owned guidance.\n')
        for relative in ['plugin.json', '.codex-plugin/plugin.json']:
            manifest = self.plugin / relative
            manifest.parent.mkdir(exist_ok=True)
            manifest.write_text(json.dumps({'name': 'frontend-react', 'version': '0.2.0'}))
        (self.plugin / 'CHANGELOG.md').write_text('# Changelog\n')
        for key, value in [('REPO_ROOT', self.repo), ('PLUGIN_ROOT', self.plugin), ('UPSTREAMS', self.upstreams)]:
            self.enterContext(patch.object(sync, key, value))
        self.run_sync()
        commit(self.repo)

    def run_sync(self, *args):
        with patch.object(sys, 'argv', ['sync', '--source-root', str(self.sources), *args]):
            return sync.main()

    def test_locked_reproduction_preserves_all_bytes(self):
        before = snapshot(self.plugin)
        self.run_sync('--locked')
        self.assertEqual(before, snapshot(self.plugin))

    def test_version_bump_updates_claude_manifest_and_catalog(self):
        portable = json.loads((self.plugin / 'plugin.json').read_text())
        claude = self.plugin / '.claude-plugin/plugin.json'
        claude.parent.mkdir()
        claude.write_text(json.dumps(portable))
        catalog = self.repo / '.claude-plugin/marketplace.json'
        catalog.parent.mkdir()
        catalog.write_text(json.dumps({'plugins': [
            {'name': 'frontend-react', 'version': portable['version']},
            {'name': 'other', 'version': '7.0.0'},
        ]}))
        version = sync.bump_plugin_version([])
        self.assertEqual(json.loads(claude.read_text())['version'], version)
        entries = json.loads(catalog.read_text())['plugins']
        self.assertEqual(entries[0]['version'], version)
        self.assertEqual(entries[1]['version'], '7.0.0')

    def test_selective_update_preserves_unselected_dirty_files_and_pin(self):
        other = self.plugin / 'skills/typescript-advanced-types/SKILL.md'
        other.write_text(other.read_text() + '\nLocal change.\n')
        before_other = snapshot(other.parent)
        old_lock = json.loads((self.plugin / 'upstreams.lock.json').read_text())
        checkout = self.sources / 'composition'
        (checkout / 'skills/vercel-composition-patterns/reference.md').write_text('New upstream guidance.\n')
        commit(checkout)
        self.run_sync('--upstream', 'composition')
        new_lock = json.loads((self.plugin / 'upstreams.lock.json').read_text())
        self.assertEqual(old_lock['upstreams'][1], new_lock['upstreams'][1])
        self.assertEqual(before_other, snapshot(other.parent))
        self.assertEqual(new_lock['upstreams'][0]['commit'], git(checkout, 'rev-parse', 'HEAD'))
        for relative in ['plugin.json', '.codex-plugin/plugin.json']:
            self.assertEqual(json.loads((self.plugin / relative).read_text())['version'], '0.2.1')

    def test_locked_mismatch_fails_without_changing_destination(self):
        checkout = self.sources / 'composition'
        (checkout / 'note.md').write_text('Later commit.\n')
        commit(checkout)
        before = snapshot(self.plugin)
        with self.assertRaisesRegex(SystemExit, 'does not match locked commit'):
            self.run_sync('--locked')
        self.assertEqual(before, snapshot(self.plugin))

    def test_dirty_selected_destination_is_preserved(self):
        target = self.plugin / 'skills/vercel-composition-patterns/SKILL.md'
        target.write_text(target.read_text() + '\nLocal work.\n')
        before = snapshot(self.plugin)
        with self.assertRaisesRegex(SystemExit, 'Refusing to overwrite'):
            self.run_sync('--upstream', 'composition')
        self.assertEqual(before, snapshot(self.plugin))

    def test_sync_preserves_plugin_owned_committed_and_dirty_edits(self):
        self.assertNotIn('base-ui-stylex', CONFIGURED_DESTINATIONS)
        self.assertNotIn('stylex', CONFIGURED_DESTINATIONS)
        target = self.plugin / 'skills/base-ui-stylex/SKILL.md'
        target.write_text('Committed plugin-owned improvement.\n')
        commit(self.repo)
        self.run_sync('--locked')
        self.assertEqual(target.read_text(), 'Committed plugin-owned improvement.\n')
        target.write_text('Further uncommitted plugin-owned improvement.\n')
        self.run_sync()
        self.assertEqual(target.read_text(), 'Further uncommitted plugin-owned improvement.\n')

    def test_shadcn_overlay_fails_closed_when_routing_anchor_changes(self):
        skill = Path(self.temp.name) / 'shadcn'
        skill.mkdir()
        (skill / 'SKILL.md').write_text('---\nname: shadcn\n---\nChanged upstream trigger.\n')
        with self.assertRaisesRegex(SystemExit, 'shadcn component routing compatibility anchor'):
            sync.adapt_shadcn(skill)

    def test_ui_metadata_overlay_removes_unsupported_version(self):
        skill = Path(self.temp.name) / 'fixing-metadata'
        skill.mkdir()
        source = '---\nname: fixing-metadata\nversion: 1.0.1\nlicense: MIT\n---\n\nGuidance.\n'
        (skill / 'SKILL.md').write_text(source)
        sync.adapt_ui_skills(skill)
        self.assertEqual((skill / 'SKILL.md').read_text(), source.replace('version: 1.0.1\n', ''))

    def test_webapp_overlay_keeps_playwright_cli_default_after_sync(self):
        skill = Path(self.temp.name) / 'webapp-testing'
        skill.mkdir()
        source = (
            '---\nname: webapp-testing\n'
            'description: Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing browser screenshots, and viewing browser logs.\n'
            '---\n\n# Web Application Testing\n\n'
            'To test local web applications, write native Python Playwright scripts.\n\n'
            "page.wait_for_load_state('networkidle')\n"
        )
        (skill / 'SKILL.md').write_text(source)
        examples = skill / 'examples'
        examples.mkdir()
        (examples / 'stale.py').write_text("page.wait_for_timeout(1000)\n")
        bundled = self.plugin / 'skills/webapp-testing'
        for relative in ('references/codex-annotation-csp.md', 'evals/evals.json'):
            path = bundled / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('fixture\n')
        sync.adapt_webapp_testing(skill)
        result = (skill / 'SKILL.md').read_text()
        self.assertIn('use Playwright CLI with an isolated named session', result)
        self.assertIn('repository\'s committed browser-test runner', result)
        self.assertNotIn('agent-browser', result)
        self.assertNotIn("page.wait_for_load_state('networkidle')", result)
        self.assertFalse(examples.exists())
        self.assertTrue((skill / 'references/codex-annotation-csp.md').exists())
        self.assertTrue((skill / 'evals/evals.json').exists())


if __name__ == '__main__':
    unittest.main()
