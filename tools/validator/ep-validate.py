#!/usr/bin/env python3
"""ExpertPack Validator v2 - comprehensive pack compliance checker.

Usage: python3 ep-validate-v2.py /path/to/pack [--verbose] [--json] [--provenance]

Checks (20):
  1. manifest.yaml exists and has required fields
  2. manifest.yaml field validation (type, slug format, entry_point exists)
  3. Duplicate basenames across the vault
  4. Missing directory prefix on content files
  5. Frontmatter: required fields (title, type, tags, pack)
  6. Frontmatter: type matches directory
  7. _index.md presence for every content directory
  8. Broken related: frontmatter references
  9. Path-based related: entries (should be bare filenames)
 10. Missing verbatim<->summary cross-links
 11. Broken wikilinks in body
 12. Markdown links in body (should be wikilinks for Obsidian)
 13. Broken canonical_verbatim: references
 14. Bidirectional related: check (A->B but not B->A)
 15. Orphaned files (no related: and no incoming links)
 16. File size check (>6000 chars warning)
 17. W-PROV-01: content file missing verified_at (provenance) [--provenance]
 18. W-PROV-02: content_hash present but doesn't match actual file body [--provenance]
 19. W-PROV-04: content file missing id field (provenance) [--provenance]
 20. W-HUB-01: concept-dense hub file detected (high topic count, standard retrieval_strategy)

Provenance checks (17-19) are opt-in via --provenance flag.
"""

import os, re, sys, yaml, json, hashlib
from collections import Counter, defaultdict
from datetime import date, timedelta

SKIP_DIRS = {'.obsidian', '.git', 'node_modules', 'eval', '__pycache__', '.venv'}
SKIP_BASENAMES = {'_index.md', '_access.json', '_index.json'}
ROOT_EXEMPT = {
    'README.md', 'SCHEMA.md', 'STATUS.md', 'LEGACY.md',
    'glossary.md', 'overview.md', 'freshness.md',
}

PERSON_PACK_PREFIXES = {
    'facts': 'facts-', 'meta': 'meta-', 'mind': 'mind-',
    'propositions': 'prop-', 'relationships': 'rel-',
    'presentation': 'pres-',
    'presentation/appearance': 'pres-appearance-',
    'presentation/voice': 'pres-voice-',
    'summaries/stories': 'sum-', 'summaries/reflections': 'sum-',
    'summaries/opinions': 'sum-',
    'verbatim/stories': 'vbt-', 'verbatim/reflections': 'vbt-',
    'verbatim/opinions': 'vbt-',
}

MANIFEST_REQUIRED = {'name', 'slug', 'type', 'version', 'description', 'entry_point'}
VALID_PACK_TYPES = {'person', 'product', 'process', 'composite'}
FM_REQUIRED = {'title', 'type', 'tags', 'pack'}
CHAR_CEILING = 6000

DIR_TYPE_MAP = {
    'concepts': 'concept', 'workflows': 'workflow',
    'troubleshooting': 'troubleshooting', 'faq': 'faq',
    'propositions': 'proposition', 'summaries': 'summary',
    'sources': 'source', 'decisions': 'decision',
    'facts': 'fact', 'mind': 'mind', 'relationships': 'relationship',
    'presentation': 'presentation', 'verbatim': 'verbatim',
    'training': 'training', 'meta': 'meta', 'commercial': 'commercial',
    'customers': 'customer', 'volatile': 'volatile', 'patterns': 'pattern',
}

RE_FM = re.compile(r'^---\n(.*?)\n---', re.DOTALL)
RE_WIKI = re.compile(r'\[\[([^\]|]+?)(?:\|[^\]]+?)?\]\]')
RE_MDLINK = re.compile(r'\[([^\]]+)\]\(([^)]+\.md)\)')

def parse_fm(content):
    m = RE_FM.match(content)
    if not m:
        return {}
    try:
        return yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        return {}

def strip_fm(content):
    return RE_FM.sub('', content, count=1).lstrip('\n')

def get_wikilinks(body):
    return RE_WIKI.findall(body)

def get_md_links(body):
    return RE_MDLINK.findall(body)


class Validator:
    def __init__(self, pack_path, verbose=False, check_provenance=False):
        self.pack_path = os.path.abspath(pack_path)
        self.pack_name = os.path.basename(self.pack_path)
        self.verbose = verbose
        self.check_provenance = check_provenance
        self.manifest = {}
        self.pack_type = 'unknown'
        self.pack_slug = ''
        self.files = {}           # rel_path -> content
        self.fm = {}              # rel_path -> frontmatter dict
        self.bodies = {}          # rel_path -> body (post-frontmatter)
        self.basenames = defaultdict(list)  # basename -> [rel_paths]
        self.all_basenames = set()
        self.index_files = set()  # rel_paths of _index.md files
        self.content_dirs = set() # dirs that contain .md content files
        self.issues = []          # (severity, category, file, message)

    def _add(self, sev, cat, f, msg):
        self.issues.append((sev, cat, f, msg))

    def load_manifest(self):
        mp = os.path.join(self.pack_path, 'manifest.yaml')
        if not os.path.exists(mp):
            self._add('ERROR', 'manifest-missing', 'manifest.yaml',
                       'manifest.yaml not found at pack root')
            return
        try:
            with open(mp) as fh:
                self.manifest = yaml.safe_load(fh.read()) or {}
        except yaml.YAMLError as e:
            self._add('ERROR', 'manifest-parse', 'manifest.yaml', f'YAML parse error: {e}')
            return
        self.pack_type = self.manifest.get('type', 'unknown')
        self.pack_slug = self.manifest.get('slug', '')

    def scan(self):
        for root, dirs, files in os.walk(self.pack_path):
            dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
            for f in sorted(files):
                full = os.path.join(root, f)
                rel = os.path.relpath(full, self.pack_path)
                rel_dir = os.path.dirname(rel).replace(os.sep, '/')
                if f == '_index.md':
                    self.index_files.add(rel)
                    if rel_dir:
                        self.content_dirs.add(rel_dir)
                    continue
                if f in SKIP_BASENAMES or not f.endswith('.md'):
                    continue
                content = open(full).read()
                self.files[rel] = content
                self.fm[rel] = parse_fm(content)
                self.bodies[rel] = strip_fm(content)
                self.basenames[f].append(rel)
                self.all_basenames.add(f)
                if rel_dir:
                    self.content_dirs.add(rel_dir)

    # ── Check 1: manifest exists + required fields ───────────────────────
    def check_manifest_fields(self):
        if not self.manifest:
            return  # already flagged in load_manifest
        for field in sorted(MANIFEST_REQUIRED):
            if field not in self.manifest:
                self._add('ERROR', 'manifest-field', 'manifest.yaml',
                           f"Missing required field: '{field}'")

    # ── Check 2: manifest field validation ───────────────────────────────
    def check_manifest_values(self):
        if not self.manifest:
            return
        t = self.manifest.get('type', '')
        if t and t not in VALID_PACK_TYPES:
            self._add('ERROR', 'manifest-type', 'manifest.yaml',
                       f"Invalid type '{t}' - must be one of {sorted(VALID_PACK_TYPES)}")
        slug = self.manifest.get('slug', '')
        if slug and not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', slug):
            self._add('WARN', 'manifest-slug', 'manifest.yaml',
                       f"Slug '{slug}' is not valid kebab-case")
        ep = self.manifest.get('entry_point', '')
        if ep:
            ep_full = os.path.join(self.pack_path, ep)
            if not os.path.exists(ep_full):
                self._add('ERROR', 'manifest-entry', 'manifest.yaml',
                           f"entry_point '{ep}' does not exist")

    # ── Check 3: duplicate basenames ─────────────────────────────────────
    def check_duplicate_basenames(self):
        for bn, paths in self.basenames.items():
            if len(paths) > 1:
                self._add('ERROR', 'duplicate-basename', bn,
                           f"Found in: {', '.join(paths)}")

    # ── Check 4: missing directory prefix ────────────────────────────────
    def check_missing_prefix(self):
        prefixes = {}
        fp = self.manifest.get('file_prefixes')
        if fp and isinstance(fp, dict):
            prefixes = fp
        elif self.pack_type == 'person':
            prefixes = PERSON_PACK_PREFIXES
        else:
            return  # no prefix map available
        for rel in self.files:
            bn = os.path.basename(rel)
            rel_dir = os.path.dirname(rel).replace(os.sep, '/')
            if not rel_dir:
                continue
            prefix = prefixes.get(rel_dir)
            if prefix is None:
                # try parent dir (e.g. summaries/stories -> summaries)
                parent = rel_dir.split('/')[0]
                prefix = prefixes.get(parent)
            if prefix and not bn.startswith(prefix):
                self._add('ERROR', 'missing-prefix', rel,
                           f"Expected prefix '{prefix}' - should be '{prefix}{bn}'")

    # ── Check 5: frontmatter required fields ─────────────────────────────
    def check_frontmatter_required(self):
        for rel, fm in self.fm.items():
            rel_dir = os.path.dirname(rel)
            if not rel_dir:
                continue  # root files exempt
            bn = os.path.basename(rel)
            if bn in ROOT_EXEMPT:
                continue
            if not fm:
                self._add('WARN', 'no-frontmatter', rel, 'No YAML frontmatter found')
                continue
            for field in sorted(FM_REQUIRED):
                if field not in fm:
                    self._add('WARN', 'missing-fm-field', rel,
                               f"Missing frontmatter field: '{field}'")

    # ── Check 6: type-directory consistency ──────────────────────────────
    def check_type_directory(self):
        for rel, fm in self.fm.items():
            if not fm or 'type' not in fm:
                continue
            rel_dir = os.path.dirname(rel).replace(os.sep, '/')
            if not rel_dir:
                continue
            top_dir = rel_dir.split('/')[0]
            expected_type = DIR_TYPE_MAP.get(top_dir)
            if expected_type and fm['type'] != expected_type:
                # Allow close matches (e.g. 'story' in summaries is fine)
                if fm['type'] in ('story', 'reflection', 'opinion') and top_dir in ('summaries', 'verbatim'):
                    continue
                if fm['type'] == 'index':
                    continue
                self._add('WARN', 'type-dir-mismatch', rel,
                           f"type: '{fm['type']}' in directory '{top_dir}/' (expected '{expected_type}')")

    # ── Check 7: _index.md presence ──────────────────────────────────────
    def check_index_files(self):
        for d in self.content_dirs:
            idx_path = os.path.join(d, '_index.md')
            if idx_path not in self.index_files:
                # Only flag directories with actual content files
                has_content = any(
                    os.path.dirname(r).replace(os.sep, '/') == d
                    for r in self.files
                )
                if has_content:
                    self._add('WARN', 'missing-index', d + '/',
                               f"No _index.md in content directory")

    # ── Check 8: broken related: frontmatter references ──────────────────
    def check_broken_related(self):
        for rel, fm in self.fm.items():
            for ref in (fm.get('related') or []):
                ref = str(ref)
                ref_bn = os.path.basename(ref)
                if ref_bn not in self.all_basenames:
                    self._add('ERROR', 'broken-related', rel,
                               f"related: '{ref}' - file not found")

    # ── Check 9: path-based related: entries ─────────────────────────────
    def check_path_in_related(self):
        for rel, fm in self.fm.items():
            for ref in (fm.get('related') or []):
                ref = str(ref)
                if '/' in ref:
                    bn = os.path.basename(ref)
                    self._add('WARN', 'path-in-related', rel,
                               f"related: '{ref}' - should be bare filename '{bn}'")

    # ── Check 10: verbatim<->summary cross-links ────────────────────────
    def check_vbt_sum_links(self):
        vbt_files = {}  # slug -> rel_path
        sum_files = {}  # slug -> rel_path
        for rel in self.files:
            d = os.path.dirname(rel).replace(os.sep, '/')
            bn = os.path.basename(rel)
            if d.startswith('verbatim/'):
                slug = re.sub(r'^vbt-', '', bn)
                vbt_files[slug] = rel
            elif d.startswith('summaries/'):
                slug = re.sub(r'^sum-', '', bn)
                sum_files[slug] = rel
        # Build reverse lookup: summary basename -> summary slug
        sum_by_bn = {os.path.basename(v): k for k, v in sum_files.items()}
        vbt_by_bn = {os.path.basename(v): k for k, v in vbt_files.items()}

        # Check vbt -> sum
        for slug, vbt_rel in vbt_files.items():
            fm = self.fm.get(vbt_rel, {})
            related_bns = [os.path.basename(str(r)) for r in (fm.get('related') or [])]
            # Find matching summary: exact slug match OR via related: frontmatter
            if slug in sum_files:
                matched_sum = sum_files[slug]
            else:
                # Fallback: check if any related: entry points to a known summary
                matched_sum = None
                for r_bn in related_bns:
                    if r_bn in sum_by_bn or r_bn.startswith('sum-'):
                        # Find the sum_rel by basename
                        for sr in sum_files.values():
                            if os.path.basename(sr) == r_bn:
                                matched_sum = sr
                                break
                        if matched_sum:
                            break
            if matched_sum is None:
                self._add('WARN', 'verbatim-no-summary', vbt_rel,
                           f"No matching summary (slug: {slug})")
                continue
            sum_bn = os.path.basename(matched_sum)
            if sum_bn not in related_bns:
                self._add('ERROR', 'missing-vbt-to-sum', vbt_rel,
                           f"Missing related: link to summary '{sum_bn}'")
        # Check sum -> vbt
        for slug, sum_rel in sum_files.items():
            fm = self.fm.get(sum_rel, {})
            related_bns = [os.path.basename(str(r)) for r in (fm.get('related') or [])]
            # Find matching verbatim: exact slug match OR via related: frontmatter
            if slug in vbt_files:
                matched_vbt = vbt_files[slug]
            else:
                matched_vbt = None
                for r_bn in related_bns:
                    if r_bn in vbt_by_bn or r_bn.startswith('vbt-'):
                        for vr in vbt_files.values():
                            if os.path.basename(vr) == r_bn:
                                matched_vbt = vr
                                break
                        if matched_vbt:
                            break
            if matched_vbt is None:
                continue
            vbt_bn = os.path.basename(matched_vbt)
            if vbt_bn not in related_bns:
                self._add('ERROR', 'missing-sum-to-vbt', sum_rel,
                           f"Missing related: link to verbatim '{vbt_bn}'")

    # External spec filenames that are valid cross-pack references (not errors)
    EXTERNAL_SPEC_FILES = {'core.md', 'person.md', 'product.md', 'composite.md'}
    # Root-level meta/doc files to skip for wikilink checking
    WIKILINK_SKIP_FILES = {'README.md', 'SCHEMA.md', 'AGENTS.md'}

    # ── Check 11: broken wikilinks ───────────────────────────────────────
    def check_wikilinks(self):
        for rel in self.files:
            # Skip root-level meta/documentation files
            if os.path.basename(rel) in self.WIKILINK_SKIP_FILES and '/' not in rel:
                continue
            body = self.bodies[rel]
            for target in get_wikilinks(body):
                tb = os.path.basename(target)
                if not tb.endswith('.md'):
                    tb += '.md'
                # Skip known external spec references
                if tb in self.EXTERNAL_SPEC_FILES:
                    continue
                if tb not in self.all_basenames:
                    self._add('ERROR', 'broken-wikilink', rel,
                               f"[[{target}]] - target not found")

    # ── Check 12: markdown links (should be wikilinks) ───────────────────
    def check_md_links(self):
        for rel in self.files:
            body = self.bodies[rel]
            md_links = get_md_links(body)
            if md_links:
                targets = [t for _, t in md_links]
                self._add('WARN', 'markdown-links', rel,
                           f"{len(md_links)} markdown link(s) - should be [[wikilinks]] for Obsidian graph: {', '.join(targets[:3])}" +
                           (f" + {len(targets)-3} more" if len(targets) > 3 else ""))

    # ── Check 13: broken canonical_verbatim ──────────────────────────────
    def check_canonical_verbatim(self):
        for rel, fm in self.fm.items():
            cv = fm.get('canonical_verbatim')
            if not cv:
                continue
            cv_bn = os.path.basename(str(cv))
            if cv_bn not in self.all_basenames:
                self._add('ERROR', 'broken-canonical-verbatim', rel,
                           f"canonical_verbatim: '{cv}' - file not found")

    # ── Check 14: bidirectional related ──────────────────────────────────
    def check_bidirectional_related(self):
        for rel, fm in self.fm.items():
            bn = os.path.basename(rel)
            for ref in (fm.get('related') or []):
                ref_bn = os.path.basename(str(ref))
                if ref_bn not in self.all_basenames:
                    continue  # already flagged in check_broken_related
                # Find the target file and check if it links back
                for target_rel, target_fm in self.fm.items():
                    if os.path.basename(target_rel) != ref_bn:
                        continue
                    target_related_bns = [
                        os.path.basename(str(r))
                        for r in (target_fm.get('related') or [])
                    ]
                    if bn not in target_related_bns:
                        self._add('WARN', 'unidirectional-related', rel,
                                   f"Links to '{ref_bn}' but '{ref_bn}' doesn't link back")
                    break

    # ── Check 15: orphaned files ─────────────────────────────────────────
    def check_orphaned(self):
        incoming = defaultdict(set)
        for rel, fm in self.fm.items():
            for ref in (fm.get('related') or []):
                incoming[os.path.basename(str(ref))].add(rel)
        for rel in self.files:
            body = self.bodies[rel]
            for target in get_wikilinks(body):
                tb = os.path.basename(target)
                if not tb.endswith('.md'):
                    tb += '.md'
                incoming[tb].add(rel)
        for rel, fm in self.fm.items():
            bn = os.path.basename(rel)
            rel_dir = os.path.dirname(rel)
            if not rel_dir:
                continue
            has_outgoing = bool(fm.get('related'))
            has_incoming = bn in incoming
            if not has_outgoing and not has_incoming:
                self._add('WARN', 'orphaned', rel,
                           "No related: frontmatter and no incoming links - orphaned")

    # ── Check 16: file size ──────────────────────────────────────────────
    def check_file_size(self):
        for rel, content in self.files.items():
            chars = len(content)
            if chars > CHAR_CEILING:
                # Check if atomic strategy exempts it
                fm = self.fm.get(rel, {})
                retrieval = fm.get('retrieval', {})
                rs = fm.get('retrieval_strategy', '')
                if (isinstance(retrieval, dict) and retrieval.get('strategy') == 'atomic') \
                        or rs == 'atomic':
                    continue
                self._add('WARN', 'file-too-large', rel,
                           f"{chars} chars (ceiling: {CHAR_CEILING}) — consider splitting")

    # W-HUB-01: concept density check
    HUB_MIN_CONCEPTS = 8   # minimum distinct concept count to trigger
    HUB_MAX_DEPTH    = 15  # words-per-concept threshold (below = hub)
    HUB_SKIP_TYPES   = {'index', 'source', 'proposition', 'summary',
                        'training', 'glossary'}
    HUB_SKIP_RS      = {'atomic', 'navigation'}  # these are intentional
    HUB_SKIP_SCOPE   = {'reference', 'multi', 'navigation'}  # author-declared

    def check_hub_files(self):
        """W-HUB-01: flag files that are concept-dense retrieval hubs.

        A hub file has many distinct topic sections/rows relative to its word
        count, causing its embedding to land in the centroid of all topics and
        rank modestly for everything while answering nothing well.

        Trigger: depth_ratio (words / concept_count) < HUB_MAX_DEPTH
                 AND concept_count >= HUB_MIN_CONCEPTS
                 AND not explicitly declared as reference/multi/navigation.
        """
        for rel, content in self.files.items():
            fm = self.fm.get(rel, {})
            # Skip exempt types
            if fm.get('type', '') in self.HUB_SKIP_TYPES:
                continue
            # Skip exempt retrieval strategies
            rs = fm.get('retrieval_strategy', 'standard')
            if rs in self.HUB_SKIP_RS:
                continue
            # Skip if author declared concept_scope explicitly
            scope = fm.get('concept_scope', '')
            if scope in self.HUB_SKIP_SCOPE:
                continue
            # Strip frontmatter from body for analysis
            body = re.sub(r'^---.*?---\s*', '', content, flags=re.DOTALL)
            body = re.sub(r'<!--.*?-->', '', body, flags=re.DOTALL)
            words = len(body.split())
            if words < 100:
                continue
            # Count H2/H3 headings + non-separator table rows as concept proxy
            h_count = len(re.findall(r'^#{2,3}\s+.+', body, re.MULTILINE))
            row_count = len(re.findall(r'^\|[^-\|].*\|', body, re.MULTILINE))
            concept_count = h_count + row_count
            if concept_count < self.HUB_MIN_CONCEPTS:
                continue
            depth_ratio = words / concept_count
            if depth_ratio < self.HUB_MAX_DEPTH:
                self._add('WARN', 'W-HUB-01', rel,
                           f"{concept_count} concepts, {depth_ratio:.1f} words/concept "
                           f"(threshold: <{self.HUB_MAX_DEPTH} words/concept, "
                           f">={self.HUB_MIN_CONCEPTS} concepts) — "
                           f"consider splitting or setting concept_scope: reference/multi")


    # -- Check: retrieval-first antipattern directories/types ---------------
    def check_retrieval_antipatterns(self):
        """W-RETR-01: warn on directories and file types that harm retrieval quality
        in retrieval-first packs (EP MCP / RAG).

        Antipatterns:
        - Directories named summaries/, propositions/, sources/ at top level
        - Files with type: summary or type: proposition in frontmatter

        These files score broadly on every query and displace specific,
        high-EK files from the result set (Axiom 12). They are only acceptable
        in LLM-reads-all packs where the model ingests full context.

        Suppressed if manifest declares retrieval_model: full-context.
        """
        retrieval_model = self.manifest.get('retrieval_model', 'retrieval-first')
        if retrieval_model == 'full-context':
            return

        # Check for antipattern directory names
        ANTIPATTERN_DIRS = {'summaries', 'propositions', 'sources'}
        found_dirs = set()
        for rel in self.files:
            parts = rel.split('/')
            for part in parts[:-1]:  # exclude filename itself
                if part in ANTIPATTERN_DIRS:
                    found_dirs.add(part)

        for d in sorted(found_dirs):
            self._add('WARN', 'W-RETR-01', f'{d}/',
                      f"Directory '{d}/' is a retrieval-first antipattern "
                      f"(Axiom 12) — files here score broadly on every query "
                      f"and displace specific EK files. "
                      f"Delete or merge content into atomic files. "
                      f"Set manifest retrieval_model: full-context to suppress.")

        # Check for antipattern frontmatter types
        ANTIPATTERN_TYPES = {'summary', 'proposition'}
        for rel, fm in self.fm.items():
            t = fm.get('type', '')
            if t in ANTIPATTERN_TYPES:
                self._add('WARN', 'W-RETR-01', rel,
                          f"type: '{t}' is a retrieval-first antipattern "
                          f"(Axiom 12) — summary/proposition files score broadly "
                          f"and displace atomic EK files. "
                          f"Merge content into the file it describes as a lead sentence. "
                          f"Set manifest retrieval_model: full-context to suppress.")

    # -- Checks 17-19: provenance (opt-in via --provenance) ----------------
    def check_provenance_fields(self):
        """W-PROV-01: missing verified_at; W-PROV-02: hash mismatch;
        W-PROV-03: stale content; W-PROV-04: missing id."""
        refresh_cycle_days = None
        freshness = self.manifest.get('freshness') or {}
        rc = freshness.get('refresh_cycle', '')
        if rc and isinstance(rc, str):
            m = re.match(r'^P(?:(\d+)Y)?(?:(\d+)M)?(?:(\d+)D)?$', rc)
            if m:
                y = int(m.group(1) or 0)
                mo = int(m.group(2) or 0)
                d = int(m.group(3) or 0)
                refresh_cycle_days = y * 365 + mo * 30 + d

        today = date.today()
        PROV_SKIP_TYPES = {'index', 'source', 'proposition', 'summary', 'training'}

        for rel, fm in self.fm.items():
            rel_dir = os.path.dirname(rel)
            if not rel_dir:
                continue  # root-level structural files exempt
            file_type = fm.get('type', '')
            if file_type in PROV_SKIP_TYPES:
                continue

            # W-PROV-04: missing id
            if not fm.get('id'):
                self._add('WARN', 'W-PROV-04', rel,
                           'Missing id field -- add a stable citation ID '
                           '(format: pack-slug/relative-path-no-ext)')

            # W-PROV-01: missing verified_at
            verified_at = fm.get('verified_at')
            if not verified_at:
                self._add('WARN', 'W-PROV-01', rel,
                           'Missing verified_at -- provenance coverage incomplete')
            elif refresh_cycle_days:
                # W-PROV-03: stale content
                try:
                    va_date = date.fromisoformat(str(verified_at))
                    age_days = (today - va_date).days
                    if age_days > refresh_cycle_days:
                        self._add('WARN', 'W-PROV-03', rel,
                                   f'verified_at {verified_at} is {age_days}d old '
                                   f'(refresh_cycle {rc} = {refresh_cycle_days}d)')
                except (ValueError, TypeError):
                    self._add('WARN', 'W-PROV-01', rel,
                               f'verified_at cannot be parsed as a date: {verified_at!r}')

            # W-PROV-02: content_hash mismatch
            stored_hash = fm.get('content_hash', '')
            if stored_hash and isinstance(stored_hash, str):
                body = self.bodies.get(rel, '')
                actual = 'sha256:' + hashlib.sha256(body.encode()).hexdigest()
                if stored_hash != actual:
                    self._add('WARN', 'W-PROV-02', rel,
                               f'content_hash mismatch -- body changed since last hash '
                               f'(stored: {stored_hash[:26]}... actual: {actual[:26]}...)')

    # ── Run all checks ───────────────────────────────────────────────────
    def validate(self):
        self.load_manifest()
        self.scan()
        self.check_manifest_fields()
        self.check_manifest_values()
        self.check_duplicate_basenames()
        self.check_missing_prefix()
        self.check_frontmatter_required()
        self.check_type_directory()
        self.check_index_files()
        self.check_broken_related()
        self.check_path_in_related()
        self.check_vbt_sum_links()
        self.check_wikilinks()
        self.check_md_links()
        self.check_canonical_verbatim()
        self.check_bidirectional_related()
        self.check_orphaned()
        self.check_file_size()
        self.check_hub_files()
        self.check_retrieval_antipatterns()
        if self.check_provenance:
            self.check_provenance_fields()
        return self.issues

    def report(self, as_json=False):
        errors = [i for i in self.issues if i[0] == 'ERROR']
        warns = [i for i in self.issues if i[0] == 'WARN']

        if as_json:
            out = {
                'pack': self.pack_name,
                'files': len(self.files),
                'errors': len(errors),
                'warnings': len(warns),
                'issues': [
                    {'severity': s, 'category': c, 'file': f, 'message': m}
                    for s, c, f, m in self.issues
                ]
            }
            print(json.dumps(out, indent=2))
            return 1 if errors else 0

        if not self.issues:
            print(f"  {self.pack_name}: {len(self.files)} files, 0 errors, 0 warnings")
            return 0

        print(f"\n{'='*60}")
        print(f"Pack: {self.pack_name} ({len(self.files)} files)")
        print(f"{'='*60}")
        by_cat = defaultdict(list)
        for s, c, f, m in self.issues:
            by_cat[c].append((s, f, m))
        for cat in sorted(by_cat):
            items = by_cat[cat]
            sev = items[0][0]
            icon = 'x' if sev == 'ERROR' else '!'
            print(f"\n[{icon}] {cat} ({len(items)})")
            shown = items if self.verbose else items[:5]
            for _, f, m in shown:
                print(f"  {f}")
                print(f"    -> {m}")
            if not self.verbose and len(items) > 5:
                print(f"  ... and {len(items)-5} more (use --verbose)")
        print(f"\n{'='*60}")
        print(f"Total: {len(errors)} errors, {len(warns)} warnings")
        print(f"{'='*60}")
        return 1 if errors else 0


def find_sub_packs(pack_path):
    """For composite packs, find sub-pack dirs with manifest.yaml."""
    subs = []
    for d in sorted(os.listdir(pack_path)):
        sub = os.path.join(pack_path, d)
        if d in SKIP_DIRS or not os.path.isdir(sub):
            continue
        if os.path.exists(os.path.join(sub, 'manifest.yaml')):
            subs.append(sub)
    # Also check packs/ subdirectory
    packs_dir = os.path.join(pack_path, 'packs')
    if os.path.isdir(packs_dir):
        for d in sorted(os.listdir(packs_dir)):
            sub = os.path.join(packs_dir, d)
            if os.path.isdir(sub) and os.path.exists(os.path.join(sub, 'manifest.yaml')):
                subs.append(sub)
    return subs


def main():
    import argparse
    parser = argparse.ArgumentParser(description='ExpertPack Validator v2')
    parser.add_argument('pack', help='Path to pack directory')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Show all issues (default: max 5 per category)')
    parser.add_argument('--json', action='store_true',
                        help='Output as JSON')
    parser.add_argument('--provenance', action='store_true',
                        help='Enable provenance checks (W-PROV-01 to W-PROV-04): '
                             'missing id, missing verified_at, stale content, hash mismatch')
    args = parser.parse_args()

    if not os.path.isdir(args.pack):
        print(f"Error: {args.pack} is not a directory")
        sys.exit(1)

    pack_path = os.path.abspath(args.pack)

    # Check if composite
    manifest_path = os.path.join(pack_path, 'manifest.yaml')
    is_composite = False
    if os.path.exists(manifest_path):
        try:
            m = yaml.safe_load(open(manifest_path).read()) or {}
            is_composite = m.get('type') == 'composite'
        except:
            pass

    exit_code = 0

    if is_composite:
        print(f"\nComposite pack: {os.path.basename(pack_path)}")
        print(f"{'='*60}")
        subs = find_sub_packs(pack_path)
        if not subs:
            print("  WARNING: No sub-packs found with manifest.yaml")
            sys.exit(1)
        for sub in subs:
            v = Validator(sub, verbose=args.verbose, check_provenance=args.provenance)
            v.validate()
            rc = v.report(as_json=args.json)
            if rc > exit_code:
                exit_code = rc
    else:
        v = Validator(pack_path, verbose=args.verbose, check_provenance=args.provenance)
        v.validate()
        exit_code = v.report(as_json=args.json)

    sys.exit(exit_code)


if __name__ == '__main__':
    main()
