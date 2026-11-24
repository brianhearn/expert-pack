#!/usr/bin/env python3
"""Unit tests for Agent Skill folder export and strict shared-profile validation (E1)."""

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[1]
SCRIPT_PATH = HERE / "ep-skill-export.py"


def _load_mod():
    spec = importlib.util.spec_from_file_location("ep_skill_export", str(SCRIPT_PATH))
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


skill_export = _load_mod()


class TestSkillExport(unittest.TestCase):
    def test_export_public_composite_pack_solar_diy(self):
        with tempfile.TemporaryDirectory(prefix="ep-skill-solar-") as tmp:
            out = skill_export.export_skill(REPO_ROOT / "packs" / "solar-diy", tmp)
            self.assertEqual(out.name, "solar-diy")
            skill_md = (out / "SKILL.md").read_text(encoding="utf-8")
            self.assertTrue(skill_md.startswith("---\n"))
            self.assertEqual(skill_export.validate_skill_folder(out), [])

            fm, body = skill_export._split_frontmatter(skill_md)
            self.assertEqual(fm["name"], "solar-diy")
            self.assertEqual(fm["license"], "CC-BY-4.0")
            self.assertEqual(fm["metadata"]["pack_version"], "2.0.0")
            self.assertIn("canonical_url", fm["metadata"])
            self.assertIn("pack_digest", fm["metadata"])
            self.assertLessEqual(len(body), 10_000)
            self.assertLessEqual(len(fm["description"]), 1024)
            self.assertIn("## Common Gotchas", body)
            self.assertTrue((out / "evals" / "evals.json").is_file())
            eval_data = json.loads((out / "evals" / "evals.json").read_text(encoding="utf-8"))
            self.assertEqual(eval_data["pack_version"], "2.0.0")

    def test_export_public_product_pack_blender_3d(self):
        with tempfile.TemporaryDirectory(prefix="ep-skill-blender-") as tmp:
            out = skill_export.export_skill(REPO_ROOT / "packs" / "blender-3d", tmp)
            self.assertEqual(skill_export.validate_skill_folder(out), [])
            fm, body = skill_export._split_frontmatter((out / "SKILL.md").read_text(encoding="utf-8"))
            self.assertEqual(fm["metadata"]["applies_to"], "blender@>=4.2")
            self.assertLessEqual(len(body), 10_000)

    def test_strict_validator_rejects_profile_violations(self):
        with tempfile.TemporaryDirectory(prefix="ep-skill-bad-") as tmp:
            root = Path(tmp) / "bad-skill"
            root.mkdir()

            # 1. Content above frontmatter ---
            (root / "SKILL.md").write_text(
                "<!-- Apache-2.0 -->\n---\nname: bad-skill\ndescription: ok\n---\n\nBody\n",
                encoding="utf-8",
            )
            errs = skill_export.validate_skill_folder(root)
            self.assertTrue(any("start immediately" in e for e in errs))

            # 2. Uppercase name + overlong description + non-string metadata + overlong body
            (root / "SKILL.md").write_text(
                "---\n"
                "name: Bad_Skill\n"
                f"description: {'x' * 1100}\n"
                "metadata:\n"
                "  version: 123\n"
                "---\n\n"
                + ("a" * 10_100),
                encoding="utf-8",
            )
            errs = skill_export.validate_skill_folder(root)
            self.assertTrue(any("kebab-case" in e for e in errs))
            self.assertTrue(any("1024" in e for e in errs))
            self.assertTrue(any("must be a string" in e for e in errs))
            self.assertTrue(any("10000" in e for e in errs))

            # 3. Broken relative link + executable script in script-free mode
            (root / "SKILL.md").write_text(
                "---\nname: bad-skill\ndescription: valid desc\n---\n\nSee [x](references/missing.md)\n",
                encoding="utf-8",
            )
            (root / "run.sh").write_text("echo hi\n", encoding="utf-8")
            errs = skill_export.validate_skill_folder(root)
            self.assertTrue(any("Broken relative link" in e for e in errs))
            self.assertTrue(any("Executable script" in e for e in errs))


if __name__ == "__main__":
    unittest.main()
