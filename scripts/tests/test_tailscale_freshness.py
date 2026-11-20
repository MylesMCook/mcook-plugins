"""Offline tests for the Tailscale freshness checker and skill invariants."""

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "tailscale" / "scripts" / "check_freshness.py"
SKILL = ROOT / "tailscale" / "skills" / "tailscale"

spec = importlib.util.spec_from_file_location("check_freshness", SCRIPT)
freshness = importlib.util.module_from_spec(spec)
spec.loader.exec_module(freshness)

LLMS_SAMPLE = """# Tailscale Documentation

## Features

- [Exit nodes](https://tailscale.com/docs/features/exit-nodes.md): Route traffic.
- [Shiny new thing](https://tailscale.com/docs/features/shiny-new-thing.md): New.
- [Nested](https://tailscale.com/docs/features/oauth-apps/device-provisioning.md): Deep.

## Brand New Section

- [Root](https://tailscale.com/docs/brand-new.md): New.
"""


class FreshnessHelpers(unittest.TestCase):
    def test_normalize(self):
        self.assertEqual(
            freshness.normalize("https://tailscale.com/docs/features/exit-nodes.md#linux"),
            "https://tailscale.com/docs/features/exit-nodes",
        )
        self.assertEqual(
            freshness.normalize("https://tailscale.com/docs/reference/troubleshooting/."),
            "https://tailscale.com/docs/reference/troubleshooting",
        )

    def test_parse_llms_ignores_nested_feature_pages(self):
        sections, features = freshness.parse_llms(LLMS_SAMPLE)
        self.assertEqual(sections, ["Features", "Brand New Section"])
        self.assertEqual(
            features,
            [
                "https://tailscale.com/docs/features/exit-nodes",
                "https://tailscale.com/docs/features/shiny-new-thing",
            ],
        )

    def test_coverage_gaps_reports_new_section_and_feature(self):
        docs_map = "| Features | x |\n| https://tailscale.com/docs/features/exit-nodes | y |"
        gaps = freshness.coverage_gaps(LLMS_SAMPLE, docs_map)
        self.assertEqual(len(gaps), 2)
        self.assertIn("Brand New Section", gaps[0])
        self.assertIn("shiny-new-thing", gaps[1])

    def test_deprecation_marker(self):
        self.assertTrue(freshness.is_deprecated("# Old\n\n**This topic is deprecated.**"))
        self.assertFalse(freshness.is_deprecated("# Current page"))

    def test_skill_urls_are_extracted_with_citations(self):
        urls = freshness.skill_doc_urls()
        self.assertGreater(len(urls), 100)
        self.assertIn("references/pam.md", urls["https://tailscale.com/docs/privileged-access-management"])
        self.assertNotIn("https://tailscale.com/docs/...", urls)


class SkillInvariants(unittest.TestCase):
    def test_every_reference_named_in_skill_exists(self):
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        import re

        for name in set(re.findall(r"references/([a-z0-9-]+\.md)", text)):
            self.assertTrue((SKILL / "references" / name).is_file(), name)

    def test_docs_map_points_to_existing_references(self):
        import re

        text = (SKILL / "references" / "docs-map.md").read_text(encoding="utf-8")
        for name in set(re.findall(r"`([a-z0-9-]+\.md)`", text)):
            self.assertTrue((SKILL / "references" / name).is_file(), name)

    def test_host_neutral_and_current_names(self):
        for path in SKILL.rglob("*.md"):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("WebFetch", text, path.name)
            self.assertNotIn("border0.md", text, path.name)
            self.assertNotIn("https://tailscale.com/docs/border0", text, path.name)


if __name__ == "__main__":
    unittest.main()
