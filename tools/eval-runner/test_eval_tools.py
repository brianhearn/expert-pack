#!/usr/bin/env python3
"""Unit tests for v4.1 EK proposition extraction, pack_version pinning, and local RAG retrieval."""

import importlib.util
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
EVAL_EK_PATH = REPO_ROOT / "tools" / "eval-ek.py"
RUN_EVAL_PATH = REPO_ROOT / "tools" / "eval-runner" / "run_eval.py"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


eval_ek = _load("eval_ek_mod", EVAL_EK_PATH)
run_eval = _load("run_eval_mod", RUN_EVAL_PATH)


class TestEvalTools(unittest.TestCase):
    def test_eval_ek_extracts_from_v41_public_packs_and_skips_volatile(self):
        blender_props = eval_ek.extract_all_propositions(REPO_ROOT / "packs" / "blender-3d")
        solar_props = eval_ek.extract_all_propositions(REPO_ROOT / "packs" / "solar-diy")
        self.assertGreater(len(blender_props), 50)
        self.assertGreater(len(solar_props), 20)

        # Ensure volatile/ content is never included (Axiom 6d)
        with tempfile.TemporaryDirectory(prefix="ep-ek-vol-") as tmp:
            p = Path(tmp) / "p"
            (p / "concepts").mkdir(parents=True)
            (p / "volatile" / "concepts").mkdir(parents=True)
            (p / "concepts" / "core.md").write_text(
                "---\ntitle: Core\ntype: concept\n---\n# Core\n\nDurable rule: always apply scale before physics.\n",
                encoding="utf-8",
            )
            (p / "volatile" / "concepts" / "pricing.md").write_text(
                "---\ntitle: Pricing\ntype: volatile\n---\n# Pricing\n\nCurrent price is $99 per month right now.\n",
                encoding="utf-8",
            )
            props = eval_ek.extract_all_propositions(p)
            self.assertEqual(len(props), 1)
            self.assertIn("Durable rule", props[0]["text"])

    def test_version_pinning_detects_drift(self):
        manifest = {"slug": "demo", "version": "2.0.0"}
        eval_ok = {
            "pack_version": "2.0.0",
            "questions": [{"id": "q1", "pack_version": "2.0.0"}],
        }
        self.assertEqual(run_eval.check_version_pinning(manifest, eval_ok), [])

        eval_drift = {
            "pack_version": "1.0.0",
            "questions": [{"id": "q1", "pack_version": "1.5.0"}],
        }
        mismatches = run_eval.check_version_pinning(manifest, eval_drift)
        self.assertEqual(len(mismatches), 2)

    def test_local_bm25_retriever_finds_relevant_blender_atoms(self):
        ret = run_eval.LocalBM25Retriever(REPO_ROOT / "packs" / "blender-3d")
        try:
            self.assertGreater(ret.doc_count, 50)
            hits = ret.retrieve("What is a field in Geometry Nodes?", top_k=5)
            self.assertGreaterEqual(len(hits), 1)
            self.assertTrue(
                any("geometry-nodes" in h["source_file"] for h in hits),
                msg=f"Expected geometry-nodes hit, got {[h['source_file'] for h in hits]}",
            )
        finally:
            ret.close()


if __name__ == "__main__":
    unittest.main()
