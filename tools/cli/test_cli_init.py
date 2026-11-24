#!/usr/bin/env python3
"""Tests verifying `expertpack init` scaffolds all 4 pack types cleanly under --strict."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CLI = REPO_ROOT / "tools" / "cli" / "expertpack.py"


class TestCliInit(unittest.TestCase):
    def test_init_all_pack_types_pass_strict(self):
        with tempfile.TemporaryDirectory(prefix="ep-init-test-") as tmp:
            for pack_type in ("product", "person", "process", "composite"):
                slug = f"sample-{pack_type}"
                proc = subprocess.run(
                    [sys.executable, str(CLI), "init", slug, "--type", pack_type, "--output", tmp],
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                )
                self.assertEqual(
                    proc.returncode,
                    0,
                    msg=f"init --type {pack_type} failed:\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}",
                )
                pack_root = Path(tmp) / slug
                self.assertTrue((pack_root / "manifest.yaml").is_file())
                if pack_type == "person":
                    self.assertTrue((pack_root / "stories" / "story-example.md").is_file())
                    self.assertTrue((pack_root / "meta" / "meta-source-coverage.md").is_file())
                elif pack_type == "process":
                    self.assertTrue((pack_root / "phases" / "01-getting-started.md").is_file())
                elif pack_type == "composite":
                    self.assertTrue((pack_root / "product" / "manifest.yaml").is_file())
                    self.assertTrue((pack_root / "process" / "manifest.yaml").is_file())


if __name__ == "__main__":
    unittest.main()
