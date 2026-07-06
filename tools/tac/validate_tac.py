#!/usr/bin/env python3
"""validate_tac.py — validate a Typed Answer Contract (TAC) envelope.

Checks an agent's JSON answer against the TAC v1 contract
(schemas/registry/typed-answer.spec.yaml + typed-answer.schema.json): structural
shape plus the semantic rules a plain JSON Schema cannot express:

  - every claim has at least one source,
  - every claim has at least one source with support "supported"
    (or the answer carries an unsupported_note),
  - retrieval_mode "reconstruct" requires each source to carry a fragment_id,
  - content_hash values are well-formed.

If the `jsonschema` package is installed it is also used for full 2020-12
validation; otherwise the built-in structural checks run standalone.

Usage (Windows: use `python`):
    python tools/tac/validate_tac.py answer.json
    python tools/tac/validate_tac.py answer.json --json
    cat answer.json | python tools/tac/validate_tac.py -
"""

import argparse
import json
import os
import re
import sys

SCHEMA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    '..', 'schemas', 'registry', 'typed-answer.schema.json',
)
SHA256_RE = re.compile(r'^sha256:[a-f0-9]{64}$')
VALID_SUPPORT = {'supported', 'partial', 'unsupported'}
VALID_MODE = {'standard', 'reconstruct'}
VALID_CONFIDENCE = {'expert-verified', 'crawled', 'inferred'}


def structural_errors(tac):
    """Return a list of contract-violation strings ([] means valid)."""
    errs = []
    if not isinstance(tac, dict):
        return ["top-level value is not a JSON object"]

    if tac.get('schema') != 'expertpack.typed_answer.v1':
        errs.append("schema must be 'expertpack.typed_answer.v1'")
    for field in ('answer_id', 'pack'):
        if not tac.get(field):
            errs.append(f"missing required field: {field}")

    mode = tac.get('retrieval_mode')
    if mode not in VALID_MODE:
        errs.append(f"retrieval_mode must be one of {sorted(VALID_MODE)}")

    claims = tac.get('claims')
    if not isinstance(claims, list) or not claims:
        errs.append("claims must be a non-empty array")
        return errs

    has_unsupported_note = bool(tac.get('unsupported_note'))
    seen_ids = set()
    for i, claim in enumerate(claims):
        where = f"claims[{i}]"
        if not isinstance(claim, dict):
            errs.append(f"{where} is not an object")
            continue
        cid = claim.get('claim_id')
        if not cid:
            errs.append(f"{where} missing claim_id")
        elif cid in seen_ids:
            errs.append(f"{where} duplicate claim_id '{cid}'")
        else:
            seen_ids.add(cid)
        if not claim.get('text'):
            errs.append(f"{where} missing text")
        conf = claim.get('confidence')
        if conf is not None and conf not in VALID_CONFIDENCE:
            errs.append(f"{where} confidence '{conf}' invalid")

        sources = claim.get('sources')
        if not isinstance(sources, list) or not sources:
            errs.append(f"{where} must have at least one source")
            continue

        has_supported = False
        for j, src in enumerate(sources):
            sw = f"{where}.sources[{j}]"
            if not isinstance(src, dict):
                errs.append(f"{sw} is not an object")
                continue
            support = src.get('support')
            if support not in VALID_SUPPORT:
                errs.append(f"{sw} support must be one of {sorted(VALID_SUPPORT)}")
            if support == 'supported':
                has_supported = True
            ch = src.get('content_hash')
            if ch is not None and not SHA256_RE.match(str(ch)):
                errs.append(f"{sw} content_hash is not a valid sha256:… value")
            if mode == 'reconstruct' and not src.get('fragment_id'):
                errs.append(f"{sw} retrieval_mode=reconstruct requires fragment_id")
            if not (src.get('fragment_id') or src.get('id') or src.get('source_file')):
                errs.append(f"{sw} needs one of fragment_id / id / source_file")

        if not has_supported and not has_unsupported_note:
            errs.append(
                f"{where} has no 'supported' source — every claim must be grounded "
                f"or the answer must carry an unsupported_note")
    return errs


def jsonschema_errors(tac):
    """Optional full JSON Schema validation. Returns [] if jsonschema missing."""
    try:
        import jsonschema  # type: ignore
    except ImportError:
        return []
    try:
        with open(SCHEMA_PATH, encoding='utf-8') as f:
            schema = json.load(f)
    except OSError:
        return []
    validator = jsonschema.Draft202012Validator(schema)
    return [f"{'/'.join(map(str, e.path))}: {e.message}" for e in validator.iter_errors(tac)]


def validate(tac):
    errs = structural_errors(tac)
    # Only add schema errors that the structural pass did not already surface.
    for e in jsonschema_errors(tac):
        errs.append(f"[schema] {e}")
    # Deduplicate while preserving order.
    seen = set()
    out = []
    for e in errs:
        if e not in seen:
            seen.add(e)
            out.append(e)
    return out


def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass
    parser = argparse.ArgumentParser(description='Validate a Typed Answer Contract (TAC) JSON')
    parser.add_argument('path', help="Path to TAC JSON, or '-' for stdin")
    parser.add_argument('--json', action='store_true', help='Emit a JSON report')
    args = parser.parse_args()

    raw = sys.stdin.read() if args.path == '-' else open(args.path, encoding='utf-8').read()
    try:
        tac = json.loads(raw)
    except json.JSONDecodeError as e:
        msg = f"invalid JSON: {e}"
        print(json.dumps({'valid': False, 'errors': [msg]}) if args.json else f"INVALID: {msg}")
        return 1

    errors = validate(tac)
    if args.json:
        print(json.dumps({'valid': not errors, 'errors': errors}, indent=2))
    elif errors:
        print(f"INVALID TAC ({len(errors)} issue(s)):")
        for e in errors:
            print(f"  - {e}")
    else:
        n = len(tac.get('claims', []))
        print(f"VALID TAC: {n} claim(s), retrieval_mode={tac.get('retrieval_mode')}")
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
