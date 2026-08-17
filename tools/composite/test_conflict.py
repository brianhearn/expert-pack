"""Fail-closed tests for composite conflict resolution (EP-7)."""
from __future__ import annotations

import unittest

from conflict import Claim, resolve


def _c(**kwargs) -> Claim:
    defaults = dict(
        pack="acme",
        role="knowledge",
        topic="feature-x",
        text="Feature X is supported",
        topic_kind="knowledge",
        confidence="crawled",
        verified_at="2026-01-01",
        access_tier="public",
        in_authority=True,
    )
    defaults.update(kwargs)
    return Claim(**defaults)


class IsolationTests(unittest.TestCase):
    def test_private_claim_never_leaks(self):
        private = _c(pack="grandpa", role="voice", access_tier="family",
                     text="SSN is 000-00-0000", topic="identity")
        public = _c(pack="product", text="Feature X is supported")
        d = resolve([private, public], strategy="priority",
                    priority=["grandpa", "product"],
                    allowed_tiers=["public"])
        self.assertEqual(d.action, "use")
        self.assertEqual(d.winner.pack, "product")
        self.assertTrue(any("access_tier" in why for _, why in d.dropped))

    def test_voice_must_not_assert_knowledge(self):
        voice_fact = _c(pack="founder", role="voice", topic_kind="knowledge",
                        text="We shipped Feature X yesterday")
        d = resolve([voice_fact], strategy="fail_closed",
                    no_source_no_claim=True)
        self.assertEqual(d.action, "refuse")
        self.assertTrue(any("voice pack" in why for _, why in d.dropped))

    def test_knowledge_must_not_override_voice(self):
        voice = _c(pack="founder", role="voice", topic="tone", topic_kind="voice",
                   text="Speak casually")
        product = _c(pack="docs", role="knowledge", topic="tone", topic_kind="voice",
                     text="Speak in formal support voice")
        d = resolve([voice, product], strategy="priority",
                    priority=["docs", "founder"])
        self.assertEqual(d.action, "use")
        self.assertEqual(d.winner.pack, "founder")
        self.assertTrue(any("must not override voice" in why for _, why in d.dropped))


class AuthorityTests(unittest.TestCase):
    def test_out_of_authority_refused(self):
        claim = _c(in_authority=False, text="Take this medication twice daily")
        d = resolve([claim], strategy="flag")
        self.assertEqual(d.action, "refuse")
        self.assertIn("no-source-no-claim", d.reason)

    def test_empty_after_filters_is_refuse(self):
        d = resolve([], strategy="priority", priority=["acme"])
        self.assertEqual(d.action, "refuse")


class StrategyTests(unittest.TestCase):
    def test_agreeing_claims_use(self):
        a = _c(pack="a", text="Feature X is supported", confidence="inferred")
        b = _c(pack="b", text="Feature X is supported", confidence="expert-verified",
               verified_at="2026-06-01")
        d = resolve([a, b], strategy="fail_closed")
        self.assertEqual(d.action, "use")
        self.assertEqual(d.winner.pack, "b")

    def test_fail_closed_on_disagreement(self):
        a = _c(pack="person", text="Feature X was deprecated last quarter")
        b = _c(pack="product", text="Feature X is fully supported")
        d = resolve([a, b], strategy="fail_closed")
        self.assertEqual(d.action, "refuse")
        self.assertIn("fail_closed", d.reason)
        self.assertIsNone(d.winner)

    def test_flag_returns_both(self):
        a = _c(pack="person", text="Deprecated")
        b = _c(pack="product", text="Supported")
        d = resolve([a, b], strategy="flag")
        self.assertEqual(d.action, "flag")
        self.assertEqual({c.pack for c in d.considered}, {"person", "product"})

    def test_priority_picks_first_listed(self):
        a = _c(pack="person", text="Deprecated")
        b = _c(pack="product", text="Supported")
        d = resolve([a, b], strategy="priority", priority=["person", "product"])
        self.assertEqual(d.action, "use")
        self.assertEqual(d.winner.pack, "person")

    def test_confidence_breaks_same_priority_rank(self):
        old = _c(pack="a", text="Yes", confidence="inferred", verified_at="2024-01-01")
        new = _c(pack="a", text="Yes", confidence="expert-verified", verified_at="2026-08-01")
        d = resolve([old, new], strategy="fail_closed")
        self.assertEqual(d.action, "use")
        self.assertEqual(d.winner.confidence, "expert-verified")


class WorkedExampleTests(unittest.TestCase):
    """The three examples in schemas/composite.md must fail closed or isolate."""

    def test_example_deprecation_flag(self):
        person = _c(pack="jane-doe", role="knowledge",
                    text="Feature X was deprecated last quarter")
        product = _c(pack="acme-widget", text="Feature X is documented as current")
        d = resolve([person, product], strategy="flag")
        self.assertEqual(d.action, "flag")

    def test_example_shared_term_fail_closed(self):
        a = _c(pack="product-a", topic="territory", text="A territory is a zip cluster")
        b = _c(pack="product-b", topic="territory", text="A territory is a sales team")
        d = resolve([a, b], strategy="fail_closed")
        self.assertEqual(d.action, "refuse")

    def test_example_family_fact_isolated(self):
        family = _c(pack="grandpa-bob", role="voice", topic="health",
                    access_tier="family", text="Grandpa's diagnosis is X")
        public = _c(pack="family-history", text="The family emigrated in 1912")
        d = resolve(
            [family, public],
            strategy="priority",
            priority=["grandpa-bob", "family-history"],
            allowed_tiers=["public"],
        )
        self.assertEqual(d.action, "use")
        self.assertEqual(d.winner.pack, "family-history")
        self.assertTrue(any(c.pack == "grandpa-bob" for c, _ in d.dropped))


if __name__ == "__main__":
    unittest.main()
