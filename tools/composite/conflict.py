"""Composite conflict resolver (EP-7).

Pack + consumer contract: given competing claims from constituent packs,
decide use / flag / refuse. Isolation and authority run before strategy.
Markdown in the packs remains canonical; this module does not write packs.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Iterable

CONFIDENCE_RANK = {
    "expert-verified": 3,
    "crawled": 2,
    "inferred": 1,
}

STRATEGIES = ("fail_closed", "flag", "priority")
DEFAULT_ISOLATION = {
    "voice_must_not_assert_knowledge": True,
    "knowledge_must_not_override_voice": True,
    "respect_access_tiers": True,
}


@dataclass(frozen=True)
class Claim:
    pack: str
    role: str  # voice | knowledge
    topic: str
    text: str
    topic_kind: str = "knowledge"  # knowledge | voice
    confidence: str | None = None
    verified_at: str | None = None
    access_tier: str = "public"
    in_authority: bool = True


@dataclass
class Decision:
    action: str  # use | flag | refuse
    winner: Claim | None = None
    considered: list[Claim] = field(default_factory=list)
    dropped: list[tuple[Claim, str]] = field(default_factory=list)
    reason: str = ""


def _parse_day(value: str | None) -> date | None:
    if not value:
        return None
    try:
        return date.fromisoformat(value[:10])
    except ValueError:
        return None


def _tie_key(claim: Claim) -> tuple:
    conf = CONFIDENCE_RANK.get(claim.confidence or "", 0)
    day = _parse_day(claim.verified_at) or date.min
    return (conf, day)


def apply_isolation(
    claims: Iterable[Claim],
    isolation: dict | None,
    allowed_tiers: Iterable[str] | None,
) -> tuple[list[Claim], list[tuple[Claim, str]]]:
    rules = {**DEFAULT_ISOLATION, **(isolation or {})}
    allowed = set(allowed_tiers or ("public",))
    kept: list[Claim] = []
    dropped: list[tuple[Claim, str]] = []
    for claim in claims:
        if rules.get("respect_access_tiers") and claim.access_tier not in allowed:
            dropped.append((claim, f"access_tier {claim.access_tier} not allowed"))
            continue
        if (
            rules.get("voice_must_not_assert_knowledge")
            and claim.role == "voice"
            and claim.topic_kind == "knowledge"
        ):
            dropped.append((claim, "voice pack must not assert knowledge claims"))
            continue
        if (
            rules.get("knowledge_must_not_override_voice")
            and claim.role == "knowledge"
            and claim.topic_kind == "voice"
        ):
            dropped.append((claim, "knowledge pack must not override voice"))
            continue
        kept.append(claim)
    return kept, dropped


def apply_authority(
    claims: Iterable[Claim],
) -> tuple[list[Claim], list[tuple[Claim, str]]]:
    kept: list[Claim] = []
    dropped: list[tuple[Claim, str]] = []
    for claim in claims:
        if not claim.in_authority:
            dropped.append((claim, f"{claim.pack} claim is outside authority_boundary"))
            continue
        kept.append(claim)
    return kept, dropped


def resolve(
    claims: list[Claim],
    *,
    strategy: str = "flag",
    priority: list[str] | None = None,
    isolation: dict | None = None,
    allowed_tiers: Iterable[str] | None = None,
    no_source_no_claim: bool = True,
) -> Decision:
    if strategy not in STRATEGIES:
        raise ValueError(f"unknown strategy {strategy!r}; expected {STRATEGIES}")

    after_iso, dropped = apply_isolation(claims, isolation, allowed_tiers)
    after_auth, dropped_auth = apply_authority(after_iso)
    dropped.extend(dropped_auth)

    if not after_auth:
        reason = "no remaining claim after isolation/authority"
        if no_source_no_claim:
            reason += "; no-source-no-claim"
        return Decision(action="refuse", considered=[], dropped=dropped, reason=reason)

    texts = {c.text.strip().lower() for c in after_auth}
    if len(texts) == 1:
        winner = max(after_auth, key=_tie_key)
        return Decision(
            action="use",
            winner=winner,
            considered=after_auth,
            dropped=dropped,
            reason="claims agree",
        )

    if strategy == "fail_closed":
        return Decision(
            action="refuse",
            considered=after_auth,
            dropped=dropped,
            reason="packs disagree; fail_closed refuses rather than guess",
        )

    if strategy == "flag":
        return Decision(
            action="flag",
            considered=after_auth,
            dropped=dropped,
            reason="packs disagree; present both and ask a human",
        )

    order = {slug: i for i, slug in enumerate(priority or [])}
    ranked = sorted(
        after_auth,
        key=lambda c: (order.get(c.pack, 10_000), -_tie_key(c)[0], -(_tie_key(c)[1].toordinal())),
    )
    return Decision(
        action="use",
        winner=ranked[0],
        considered=after_auth,
        dropped=dropped,
        reason=f"priority winner: {ranked[0].pack}",
    )
