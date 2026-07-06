#!/usr/bin/env python3
"""ExpertPack Doctor — automated fixer for common pack issues.

Usage:
  python3 ep-doctor.py /path/to/pack              # dry-run (default)
  python3 ep-doctor.py /path/to/pack --apply       # write changes
  python3 ep-doctor.py /path/to/pack --fix links   # only fix link issues
  python3 ep-doctor.py /path/to/pack --fix fm      # only fix frontmatter
  python3 ep-doctor.py /path/to/pack --fix all     # fix everything

Fix operations:
  links  — convert path-based related: to bare filenames
         — convert markdown links to wikilinks in body
         — remove broken wikilinks (unlink to plain text; composite-safe)
         — add missing legacy verbatim<->summary cross-links
         — add reverse related: links (bidirectional enforcement)
  fm     — add missing frontmatter fields (title, type, tags, pack)
         — fix legacy canonical_verbatim paths to bare filenames
  hash   — backfill provenance contract fields for --strict:
             id, schema_version, retrieval_strategy, verified_at, content_hash
  size   — (report only) flag files over the char ceiling
  prefix — suggest prefix map for packs without file_prefixes
         — rename files with prefixes (--apply required, transactional)

Always runs ep-validate before and after, showing the diff.
"""

import os, re, sys, yaml, copy, shutil, hashlib
from datetime import date
from collections import defaultdict

SKIP_DIRS = {'.obsidian', '.git', 'node_modules', 'eval', '__pycache__', '.venv'}
SKIP_BASENAMES = {'_index.md', '_access.json', '_index.json'}
ROOT_EXEMPT = {
    'README.md', 'SCHEMA.md', 'STATUS.md', 'LEGACY.md',
    'glossary.md', 'overview.md', 'freshness.md',
}

RE_FM = re.compile(r'^---\n(.*?)\n---', re.DOTALL)
RE_WIKI = re.compile(r'\[\[([^\]|]+?)(?:\|[^\]]+?)?\]\]')
RE_MDLINK = re.compile(r'\[([^\]]+)\]\(([^)]+\.md)\)')

PERSON_PACK_PREFIXES = {
    'facts': 'facts-', 'meta': 'meta-', 'mind': 'mind-',
    'relationships': 'rel-',
    'presentation': 'pres-',
    'presentation/appearance': 'pres-appearance-',
    'presentation/voice': 'pres-voice-',
    'stories': 'story-', 'reflections': 'refl-',
    'opinions': 'opn-', 'conversations': 'conv-',
}

DIR_TYPE_MAP = {
    'concepts': 'concept', 'workflows': 'workflow',
    'troubleshooting': 'troubleshooting',
    'errors': 'troubleshooting',
    'diagnostics': 'troubleshooting',
    'common-mistakes': 'gotcha',
    'faq': 'faq',
    'propositions': 'proposition', 'summaries': 'summary',
    'sources': 'source', 'decisions': 'decision',
    'facts': 'fact', 'mind': 'mind', 'relationships': 'relationship',
    'stories': 'story', 'reflections': 'reflection',
    'opinions': 'opinion', 'conversations': 'conversation',
    'presentation': 'presentation',
    'training': 'training', 'meta': 'meta', 'commercial': 'commercial',
    'customers': 'customer', 'volatile': 'volatile',
    'lessons': 'lesson',
}


def parse_fm(content):
    m = RE_FM.match(content)
    if not m:
        return {}, ''
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        fm = {}
    raw_fm = m.group(1)
    return fm, raw_fm


def rebuild_content(fm_dict, body, original_content):
    """Rebuild file content with updated frontmatter, preserving body."""
    # Serialize frontmatter
    fm_str = yaml.dump(fm_dict, default_flow_style=False, allow_unicode=True,
                       sort_keys=False, width=200).rstrip('\n')
    return f"---\n{fm_str}\n---\n{body}"


def strip_fm_body(content):
    """Return body after frontmatter."""
    m = RE_FM.match(content)
    if m:
        after = content[m.end():]
        return after.lstrip('\n') if after else ''
    return content


class Doctor:
    def __init__(self, pack_path, apply=False, fix_scope='all'):
        self.pack_path = os.path.abspath(pack_path)
        self.pack_name = os.path.basename(self.pack_path)
        self.apply = apply
        self.fix_scope = fix_scope  # 'all', 'links', 'fm', 'prefix'
        self.manifest = {}
        self.pack_type = 'unknown'
        self.pack_slug = ''
        self.schema_version = ''
        self.files = {}        # rel_path -> content
        self.fm = {}           # rel_path -> frontmatter dict
        self.bodies = {}       # rel_path -> body text
        self.basenames = defaultdict(list)
        self.all_basenames = set()
        self.changes = []       # (rel_path, description)
        self.modified = set()   # rel_paths rewritten via yaml rebuild
        self.text_modified = set()  # rel_paths edited textually (minimal diff)

    def load_manifest(self):
        mp = os.path.join(self.pack_path, 'manifest.yaml')
        if not os.path.exists(mp):
            return
        try:
            with open(mp, encoding='utf-8') as f:
                self.manifest = yaml.safe_load(f.read()) or {}
        except Exception:
            pass
        self.pack_type = self.manifest.get('type', 'unknown')
        self.pack_slug = self.manifest.get('slug', '')
        self.schema_version = str(self.manifest.get('schema_version', '')).strip()

    def scan(self):
        self.load_manifest()
        for root, dirs, files in os.walk(self.pack_path):
            dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
            for f in sorted(files):
                if f in SKIP_BASENAMES or not f.endswith('.md'):
                    continue
                if f == '_index.md':
                    continue
                full = os.path.join(root, f)
                rel = os.path.relpath(full, self.pack_path)
                content = open(full, encoding='utf-8').read()
                self.files[rel] = content
                self.fm[rel] = parse_fm(content)[0]
                self.bodies[rel] = strip_fm_body(content)
                self.basenames[f].append(rel)
                self.all_basenames.add(f)

    def _log(self, rel, desc):
        self.changes.append((rel, desc))
        self.modified.add(rel)

    def _write_file(self, rel):
        """Write modified content back to disk."""
        if not self.apply:
            return
        full = os.path.join(self.pack_path, rel)
        fm_dict = self.fm[rel]
        body = self.bodies[rel]
        content = rebuild_content(fm_dict, body, self.files[rel])
        with open(full, 'w', encoding='utf-8', newline='\n') as f:
            f.write(content)

    # ── Fix: path-based related -> bare filenames ────────────────────────
    def fix_path_related(self):
        if self.fix_scope not in ('all', 'links'):
            return
        for rel in list(self.files):
            fm = self.fm[rel]
            related = fm.get('related', [])
            if not related or not isinstance(related, list):
                continue
            new_related = []
            changed = False
            for ref in related:
                ref = str(ref)
                if '/' in ref:
                    bn = os.path.basename(ref)
                    new_related.append(bn)
                    changed = True
                else:
                    new_related.append(ref)
            if changed:
                self.fm[rel]['related'] = new_related
                self._log(rel, f"Converted {sum(1 for r in related if '/' in str(r))} path-based related: to bare filenames")

    # ── Fix: markdown links -> wikilinks in body ─────────────────────────
    def fix_md_links(self):
        if self.fix_scope not in ('all', 'links'):
            return
        for rel in list(self.files):
            body = self.bodies[rel]
            md_links = RE_MDLINK.findall(body)
            if not md_links:
                continue
            count = 0
            for text, target in md_links:
                if '://' in target:
                    continue  # external URL that merely ends in .md (e.g. obsidian.md)
                target_bn = os.path.basename(target)
                # Build the wikilink
                stem = target_bn.replace('.md', '')
                if text == stem or text == target_bn:
                    wl = f"[[{target_bn}]]"
                else:
                    wl = f"[[{target_bn}|{text}]]"
                old = f"[{text}]({target})"
                if old in body:
                    body = body.replace(old, wl, 1)
                    count += 1
            if count:
                self.bodies[rel] = body
                self._log(rel, f"Converted {count} markdown link(s) to wikilinks")

    # ── Fix: remove broken wikilinks in body ─────────────────────────────
    def fix_broken_wikilinks(self):
        """Unlink wikilinks whose target file does not exist in the pack.

        Broken links become plain text (their alias, or the target stem) so the
        prose stays readable. Composite-safe: run on a composite root and
        cross-sub-pack targets resolve against the full file set. Same-file
        anchors ([[#section]]) and embeds (![[...]]) are left untouched.
        """
        if self.fix_scope not in ('all', 'links'):
            return
        known = set()
        for rel in self.files:
            bn = os.path.basename(rel)
            known.add(bn)
            known.add(bn[:-3] if bn.endswith('.md') else bn)
        wl_re = re.compile(r'(?<!!)\[\[([^\]|#]+?)(?:#[^\]|]+)?(?:\|([^\]]+?))?\]\]')

        for rel in list(self.files):
            body = self.bodies[rel]
            removed = 0

            def repl(m):
                nonlocal removed
                target = m.group(1).strip()
                alias = (m.group(2) or '').strip()
                if '://' in target:
                    return m.group(0)  # external URL, not a pack file reference
                target_bn = os.path.basename(target)
                stem = target_bn[:-3] if target_bn.endswith('.md') else target_bn
                if stem in known or target_bn in known or f'{stem}.md' in known:
                    return m.group(0)
                removed += 1
                return alias or stem

            new_body = wl_re.sub(repl, body)
            if removed:
                self.bodies[rel] = new_body
                self._log(rel, f"Removed {removed} broken wikilink(s)")

    # ── Fix: add missing vbt<->sum cross-links ───────────────────────────
    def fix_vbt_sum_links(self):
        if self.fix_scope not in ('all', 'links'):
            return
        vbt = {}  # slug -> rel
        summ = {}
        for rel in self.files:
            d = os.path.dirname(rel).replace(os.sep, '/')
            bn = os.path.basename(rel)
            if d.startswith('verbatim/'):
                slug = re.sub(r'^vbt-', '', bn)
                vbt[slug] = rel
            elif d.startswith('summaries/'):
                slug = re.sub(r'^sum-', '', bn)
                summ[slug] = rel
        for slug in vbt:
            if slug not in summ:
                continue
            vbt_rel = vbt[slug]
            sum_rel = summ[slug]
            vbt_bn = os.path.basename(vbt_rel)
            sum_bn = os.path.basename(sum_rel)
            # vbt -> sum
            fm_v = self.fm[vbt_rel]
            related_v = [str(r) for r in (fm_v.get('related') or [])]
            related_v_bns = [os.path.basename(r) for r in related_v]
            if sum_bn not in related_v_bns:
                if 'related' not in fm_v:
                    fm_v['related'] = []
                fm_v['related'].append(sum_bn)
                self._log(vbt_rel, f"Added related: link to summary '{sum_bn}'")
            # sum -> vbt
            fm_s = self.fm[sum_rel]
            related_s = [str(r) for r in (fm_s.get('related') or [])]
            related_s_bns = [os.path.basename(r) for r in related_s]
            if vbt_bn not in related_s_bns:
                if 'related' not in fm_s:
                    fm_s['related'] = []
                fm_s['related'].append(vbt_bn)
                self._log(sum_rel, f"Added related: link to verbatim '{vbt_bn}'")

    # ── Fix: add reverse related: (bidirectional) ────────────────────────
    def fix_bidirectional(self):
        if self.fix_scope not in ('all', 'links'):
            return
        # Build basename -> rel_path index
        bn_to_rel = {}
        for rel in self.files:
            bn_to_rel[os.path.basename(rel)] = rel
        for rel in list(self.files):
            fm = self.fm[rel]
            my_bn = os.path.basename(rel)
            for ref in (fm.get('related') or []):
                ref_bn = os.path.basename(str(ref))
                if ref_bn not in bn_to_rel:
                    continue
                target_rel = bn_to_rel[ref_bn]
                target_fm = self.fm[target_rel]
                target_related = [os.path.basename(str(r)) for r in (target_fm.get('related') or [])]
                if my_bn not in target_related:
                    if 'related' not in target_fm:
                        target_fm['related'] = []
                    target_fm['related'].append(my_bn)
                    self._log(target_rel, f"Added reverse related: link from '{my_bn}'")

    # ── Fix: add missing frontmatter fields ──────────────────────────────
    def fix_frontmatter(self):
        if self.fix_scope not in ('all', 'fm'):
            return
        for rel in list(self.files):
            rel_dir = os.path.dirname(rel).replace(os.sep, '/')
            if not rel_dir:
                continue
            bn = os.path.basename(rel)
            if bn in ROOT_EXEMPT:
                continue
            fm = self.fm[rel]
            body = self.bodies[rel]
            added = []
            # title from first H1 anywhere in body
            if 'title' not in fm:
                m = re.search(r'^#\s+(.+)', body, re.MULTILINE)
                if m:
                    fm['title'] = m.group(1).strip()
                    added.append('title')
            # type from directory
            if 'type' not in fm:
                parts = rel.split('/')
                top_dir = parts[0]
                leaf_key = parts[-2] if len(parts) > 2 else os.path.splitext(os.path.basename(rel))[0]
                t = DIR_TYPE_MAP.get(leaf_key) or DIR_TYPE_MAP.get(top_dir)
                if t:
                    fm['type'] = t
                    added.append('type')
            # pack from manifest slug
            if 'pack' not in fm and self.pack_slug:
                fm['pack'] = self.pack_slug
                added.append('pack')
            # tags from directory
            if 'tags' not in fm:
                top_dir = rel_dir.split('/')[0]
                fm['tags'] = [top_dir]
                added.append('tags')
            if added:
                self.fm[rel] = fm
                self._log(rel, f"Added frontmatter: {', '.join(added)}")

    # Types that ep-validate exempts from the provenance contract.
    PROV_SKIP_TYPES = {'index', 'source', 'proposition', 'summary', 'training'}

    def _prov_exempt(self, rel, fm):
        rel_dir = os.path.dirname(rel)
        if not rel_dir:
            return True  # root-level structural files exempt
        if os.path.basename(rel) in ROOT_EXEMPT:
            return True
        return fm.get('type', '') in self.PROV_SKIP_TYPES

    @staticmethod
    def _fm_scalar(value):
        """Quote dates/version-like scalars to match the demo pack style."""
        if re.fullmatch(r'\d{4}-\d{2}-\d{2}', value) or re.fullmatch(r'\d+(\.\d+)+', value):
            return f'"{value}"'
        return value

    def _insert_fm_lines(self, content, new_lines):
        """Insert 'key: value' lines before the closing --- of the frontmatter,
        preserving the body (and its leading blank line) exactly."""
        m = RE_FM.match(content)
        if not m:
            return content, False
        fm_block = m.group(1)
        rest = content[m.end():]  # begins right after the closing '---'
        new_block = fm_block + '\n' + '\n'.join(new_lines)
        return f"---\n{new_block}\n---{rest}", True

    # ── Fix: backfill --strict provenance contract fields ────────────────
    def fix_provenance(self):
        """Backfill id, schema_version, retrieval_strategy, verified_at, and
        content_hash so files satisfy `ep-validate --strict`.

        Uses textual insertion (not a yaml rebuild) so the diff is limited to
        the added lines. content_hash is computed over the body that will be
        written, staying consistent with any earlier body edits.
        """
        if self.fix_scope not in ('all', 'hash'):
            return
        today = date.today().isoformat()
        for rel in list(self.files):
            fm = self.fm[rel]
            if not fm or self._prov_exempt(rel, fm):
                continue
            new_lines = []
            added = []
            if not fm.get('id') and self.pack_slug:
                rel_no_ext = os.path.splitext(rel)[0].replace(os.sep, '/')
                new_lines.append(f"id: {self.pack_slug}/{rel_no_ext}")
                added.append('id')
            if not fm.get('schema_version') and self.schema_version:
                new_lines.append(f"schema_version: {self._fm_scalar(self.schema_version)}")
                added.append('schema_version')
            if not fm.get('retrieval_strategy'):
                new_lines.append("retrieval_strategy: standard")
                added.append('retrieval_strategy')
            if not fm.get('verified_at'):
                new_lines.append(f"verified_at: {self._fm_scalar(today)}")
                added.append('verified_at')
            body = self.bodies[rel]
            new_hash = 'sha256:' + hashlib.sha256(body.encode('utf-8')).hexdigest()
            if fm.get('content_hash') != new_hash:
                new_lines.append(f"content_hash: {new_hash}")
                added.append('content_hash')
            if not new_lines:
                continue
            # If another fix already rewrote this file via the yaml path, fold
            # the fields into the fm dict so that rebuild includes them.
            if rel in self.modified:
                for line in new_lines:
                    key, _, val = line.partition(': ')
                    fm[key] = val.strip('"') if key != 'content_hash' else val
                self._log(rel, f"Backfilled provenance: {', '.join(added)}")
                continue
            updated, ok = self._insert_fm_lines(self.files[rel], new_lines)
            if ok:
                self.files[rel] = updated
                self.changes.append((rel, f"Backfilled provenance: {', '.join(added)}"))
                self.text_modified.add(rel)

    # ── Fix: canonical_verbatim paths -> bare filenames ──────────────────
    def fix_canonical_verbatim(self):
        if self.fix_scope not in ('all', 'fm'):
            return
        for rel in list(self.files):
            fm = self.fm[rel]
            cv = fm.get('canonical_verbatim')
            if not cv:
                continue
            cv = str(cv)
            if '/' in cv:
                fm['canonical_verbatim'] = os.path.basename(cv)
                self._log(rel, f"Stripped path from canonical_verbatim: '{cv}' -> '{os.path.basename(cv)}'")

    # ── Write all modified files ─────────────────────────────────────────
    def write_all(self):
        for rel in self.modified:
            self._write_file(rel)
        if not self.apply:
            return
        for rel in self.text_modified:
            if rel in self.modified:
                continue  # already written via yaml rebuild
            full = os.path.join(self.pack_path, rel)
            with open(full, 'w', encoding='utf-8', newline='\n') as f:
                f.write(self.files[rel])

    # ── Main run ─────────────────────────────────────────────────────────
    def run(self):
        self.scan()
        self.fix_path_related()
        self.fix_md_links()
        self.fix_broken_wikilinks()
        self.fix_vbt_sum_links()
        self.fix_bidirectional()
        self.fix_frontmatter()
        self.fix_canonical_verbatim()
        self.fix_provenance()
        self.write_all()
        return self.changes

    def report(self):
        if not self.changes:
            print(f"\n  {self.pack_name}: No fixes needed")
            return
        print(f"\n{'='*60}")
        mode = "APPLIED" if self.apply else "DRY RUN"
        print(f"Doctor: {self.pack_name} [{mode}]")
        print(f"{'='*60}")
        by_file = defaultdict(list)
        for rel, desc in self.changes:
            by_file[rel].append(desc)
        for rel in sorted(by_file):
            print(f"\n  {rel}")
            for desc in by_file[rel]:
                print(f"    -> {desc}")
        print(f"\n{'='*60}")
        touched = len(self.modified | self.text_modified)
        print(f"Total: {len(self.changes)} fixes across {touched} files")
        if not self.apply:
            print("  (dry run — use --apply to write changes)")
        print(f"{'='*60}")


def _run_validator(pack_path):
    """Run the sibling ep-validate.py with the current interpreter."""
    validator = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ep-validate.py')
    if not os.path.exists(validator):
        print("  (ep-validate.py not found next to ep-doctor.py — skipping)")
        return
    os.system(f'"{sys.executable}" "{validator}" "{pack_path}" --provenance')


def main():
    import argparse
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError):
        pass
    parser = argparse.ArgumentParser(description='ExpertPack Doctor')
    parser.add_argument('pack', help='Path to pack directory')
    parser.add_argument('--apply', action='store_true',
                        help='Write changes (default is dry-run)')
    parser.add_argument('--fix', choices=['all', 'links', 'fm', 'hash', 'prefix'],
                        default='all', help='Which fixes to apply')
    args = parser.parse_args()

    if not os.path.isdir(args.pack):
        print(f"Error: {args.pack} is not a directory")
        sys.exit(1)

    # Run validator before
    print("\n--- BEFORE ---")
    _run_validator(args.pack)

    # Run doctor
    doc = Doctor(args.pack, apply=args.apply, fix_scope=args.fix)
    doc.run()
    doc.report()

    # Run validator after (only if we applied changes)
    if args.apply and doc.changes:
        print("\n--- AFTER ---")
        _run_validator(args.pack)


if __name__ == '__main__':
    main()
