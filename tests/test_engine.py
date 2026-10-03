from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

# Ensure scripts module is accessible
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import update_contributions as engine


class TestPrShowcaseEngine(unittest.TestCase):
    def setUp(self):
        fixture_path = (
            Path(__file__).resolve().parent / "fixtures" / "graphql_response.json"
        )
        with open(fixture_path, encoding="utf-8") as f:
            self.graphql_data = json.load(f)

    def test_parse_graphql_prs_and_repos(self):
        nodes = self.graphql_data["data"]["search"]["nodes"]
        prs, repos = engine.parse_graphql_nodes(nodes)

        self.assertEqual(len(prs), 2)

        merged_pr = next(p for p in prs if p["state"] == "merged")
        self.assertEqual(merged_pr["number"], 101)
        self.assertEqual(merged_pr["repo"], "octocat/super-engine")
        self.assertEqual(merged_pr["title"], "feat(core): add async event dispatcher")

        open_pr = next(p for p in prs if p["state"] == "open")
        self.assertEqual(open_pr["number"], 42)
        self.assertEqual(open_pr["repo"], "dev-org/code-parser")

        self.assertIn("octocat/super-engine", repos)
        repo_info = repos["octocat/super-engine"]
        self.assertEqual(repo_info["stars"], 14200)
        self.assertEqual(
            repo_info["owner_avatar"], "https://github.com/octocat.png?size=64"
        )

    def test_render_contains_key_elements(self):
        nodes = self.graphql_data["data"]["search"]["nodes"]
        prs, repos = engine.parse_graphql_nodes(nodes)
        config = engine.get_default_config()
        config["show_stars"] = True

        rendered = engine.render(prs, repos, config)

        # Check headline metrics
        self.assertIn("pull_requests-2", rendered)
        self.assertIn("merged-1", rendered)
        self.assertIn("in_review-1", rendered)
        self.assertIn("projects-2", rendered)

        # Check repository header and PR titles
        self.assertIn("octocat/super-engine", rendered)
        self.assertIn("feat(core): add async event dispatcher", rendered)
        self.assertIn("dev-org/code-parser", rendered)
        self.assertIn("fix(parser): resolve token stream overflow", rendered)

        # Check star badge in cloud
        self.assertIn("img.shields.io/github/stars/octocat/super-engine", rendered)

    def test_inject_markers_existing(self):
        nodes = self.graphql_data["data"]["search"]["nodes"]
        prs, repos = engine.parse_graphql_nodes(nodes)
        initial = (
            "# My Profile\n\n"
            "<!-- CONTRIB:START -->\n"
            "old content\n"
            "<!-- CONTRIB:END -->\n\n"
            "Footer"
        )
        updated = engine.inject_content(initial, prs, repos)
        self.assertIn("<!-- CONTRIB:START -->", updated)
        self.assertIn("pull_requests-2", updated)
        self.assertIn("<!-- CONTRIB:END -->", updated)
        self.assertTrue(updated.startswith("# My Profile\n\n"))
        self.assertTrue(updated.endswith("\n\nFooter"))

    def test_inject_modular_sub_markers_claimed(self):
        nodes = self.graphql_data["data"]["search"]["nodes"]
        prs, repos = engine.parse_graphql_nodes(nodes)
        initial = (
            "# My Profile\n\n"
            "<!-- CONTRIB:METRICS:START -->\n<!-- CONTRIB:METRICS:END -->\n\n"
            "Some content in between.\n\n"
            "<!-- CONTRIB:START -->\n<!-- CONTRIB:END -->\n"
        )
        updated = engine.inject_content(initial, prs, repos)
        # Metrics injected into SUB_MARKER
        self.assertIn('<!-- CONTRIB:METRICS:START -->\n<p align="center">', updated)
        # Global block should NOT duplicate metrics (Claimed Section Principle)
        global_block = updated.split("<!-- CONTRIB:START -->")[1].split(
            "<!-- CONTRIB:END -->"
        )[0]
        self.assertNotIn("pull_requests-2", global_block)
        self.assertIn("### Merged upstream", global_block)

    def test_idempotent_injection(self):
        nodes = self.graphql_data["data"]["search"]["nodes"]
        prs, repos = engine.parse_graphql_nodes(nodes)
        initial = "# My Profile\n"
        first = engine.inject_content(initial, prs, repos)
        second = engine.inject_content(first, prs, repos)
        self.assertEqual(first, second)
        self.assertEqual(second.count("<!-- CONTRIB:START -->"), 1)
        self.assertEqual(second.count("<!-- CONTRIB:END -->"), 1)

    def test_alignment_options(self):
        nodes = self.graphql_data["data"]["search"]["nodes"]
        prs, repos = engine.parse_graphql_nodes(nodes)

        # Default alignment: badge_alignment="center", contributed_to_alignment="left"
        cfg_default = engine.get_default_config()
        rendered_default = engine.render(prs, repos, cfg_default)
        self.assertIn('<p align="center">', rendered_default)
        self.assertIn('<p align="left">', rendered_default)

        # Custom alignment: badge_alignment="left", contributed_to_alignment="center"
        cfg_custom = engine.get_default_config()
        cfg_custom["badge_alignment"] = "left"
        cfg_custom["contributed_to_alignment"] = "center"
        metrics_block = engine.render_metrics_section(prs, repos, cfg_custom)
        projects_block = engine.render_projects_section(prs, repos, cfg_custom)
        self.assertTrue(metrics_block.startswith('<p align="left">'))
        self.assertIn('<p align="center">', projects_block)


if __name__ == "__main__":
    unittest.main()
