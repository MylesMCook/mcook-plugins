"""Verify upstream refresh preserves both React discovery and framework scope."""
import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location(
    "frontend_framework_sync", Path(__file__).parents[1] / "sync_frontend_react.py"
)
sync = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = sync
SPEC.loader.exec_module(sync)


class FrameworkOverlayTest(unittest.TestCase):
    def test_upstream_refresh_and_repeat_preserve_frontmatter_and_body(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            upstream = "---\nname: react-best-practices\ndescription: React performance\n---\n\n# Upstream\n\nOriginal advice.\n"
            (root / "SKILL.md").write_text(upstream)
            (root / "AGENTS.md").write_text("# Upstream compiled rules\n")
            sync.adapt_react_framework(root)
            first = {p.name: p.read_text() for p in root.iterdir()}
            self.assertTrue(first["SKILL.md"].startswith(upstream.split("---", 2)[0] + "---\nname:"))
            self.assertIn("description: React performance\n---", first["SKILL.md"])
            self.assertTrue(first["SKILL.md"].endswith("# Upstream\n\nOriginal advice.\n"))
            self.assertTrue(first["AGENTS.md"].endswith("# Upstream compiled rules\n"))
            for text in first.values():
                self.assertEqual(text.count(sync.REACT_FRAMEWORK_GUIDANCE), 1)
            sync.adapt_react_framework(root)
            self.assertEqual(first, {p.name: p.read_text() for p in root.iterdir()})

    def test_missing_frontmatter_fails_before_rewriting_skill(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "SKILL.md"
            path.write_text("# Missing metadata\n")
            with self.assertRaises(SystemExit):
                sync.adapt_react_framework(path.parent)
            self.assertEqual(path.read_text(), "# Missing metadata\n")
