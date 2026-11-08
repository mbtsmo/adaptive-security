"""Offline checks that the repository installs as a Claude Code plugin."""

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class PluginManifest(unittest.TestCase):
    def setUp(self):
        self.plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
        self.market = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())

    def test_marketplace_lists_this_plugin(self):
        entries = [p for p in self.market["plugins"] if p["name"] == self.plugin["name"]]
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["source"], "./")

    def test_skill_path_resolves_to_skill_md(self):
        skill = ROOT / self.plugin["skills"] / "SKILL.md"
        self.assertTrue(skill.is_file())
        self.assertIn(f"name: {self.plugin['name']}\n", skill.read_text())

    def test_no_pinned_version_so_every_commit_updates(self):
        self.assertNotIn("version", self.plugin)
        self.assertTrue(all("version" not in p for p in self.market["plugins"]))


if __name__ == "__main__":
    unittest.main()
