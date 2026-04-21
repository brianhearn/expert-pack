#!/usr/bin/env python3
"""
Batch update frontmatter for v4.1 migration.
- Adds schema_version: "4.1"
- Adds concept_scope: single (unless retrieval_strategy is atomic, in which case skip concept_scope)
- Skips files without frontmatter or _index.md files
- Also handles the 'type: faq' case (concept_scope: single still applies)
"""
import os
import re
import sys

def process_file(filepath, dry_run=False):
    with open(filepath, 'r') as f:
        content = f.read()

    # Must start with frontmatter
    if not content.startswith('---'):
        return False, "no frontmatter"

    # Find end of frontmatter
    end = content.find('\n---', 3)
    if end == -1:
        return False, "unclosed frontmatter"

    frontmatter = content[3:end]
    rest = content[end:]  # starts with \n---

    # Already has schema_version 4.1?
    already_41 = 'schema_version: "4.1"' in frontmatter
    has_concept_scope = 'concept_scope:' in frontmatter
    
    is_atomic = re.search(r'retrieval_strategy:\s*atomic', frontmatter) is not None

    changes = []

    # Update schema_version
    if already_41:
        pass
    elif 'schema_version:' in frontmatter:
        # Update existing
        frontmatter = re.sub(r'schema_version:\s*["\']?[\d.]+["\']?', 'schema_version: "4.1"', frontmatter)
        changes.append('updated schema_version')
    else:
        # Add after verified_by or at end
        if 'verified_by:' in frontmatter:
            frontmatter = re.sub(r'(verified_by:.*)', r'\1\nschema_version: "4.1"', frontmatter)
        else:
            frontmatter = frontmatter.rstrip() + '\nschema_version: "4.1"'
        changes.append('added schema_version')

    # Add concept_scope if missing and not atomic
    if not has_concept_scope and not is_atomic:
        if 'schema_version:' in frontmatter:
            frontmatter = re.sub(r'(schema_version:.*)', r'\1\nconcept_scope: single', frontmatter)
        else:
            frontmatter = frontmatter.rstrip() + '\nconcept_scope: single'
        changes.append('added concept_scope: single')

    if not changes:
        return False, "no changes needed"

    new_content = '---' + frontmatter + rest
    if not dry_run:
        with open(filepath, 'w') as f:
            f.write(new_content)

    return True, ', '.join(changes)


def process_dir(dirpath, dry_run=False):
    updated = []
    skipped = []
    for root, dirs, files in os.walk(dirpath):
        # Skip hidden dirs
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for fname in sorted(files):
            if not fname.endswith('.md'):
                continue
            if fname.startswith('_') or fname == 'OBSIDIAN-SETUP.md':
                continue
            fpath = os.path.join(root, fname)
            changed, reason = process_file(fpath, dry_run=dry_run)
            if changed:
                updated.append((fpath, reason))
            else:
                skipped.append((fpath, reason))
    return updated, skipped


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='Pack directory to process')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    updated, skipped = process_dir(args.path, dry_run=args.dry_run)
    print(f"\n{'DRY RUN - ' if args.dry_run else ''}Updated {len(updated)} files:")
    for f, r in updated:
        print(f"  + {f.replace(args.path+'/', '')} ({r})")
    print(f"\nSkipped {len(skipped)} files:")
    for f, r in skipped:
        print(f"  - {f.replace(args.path+'/', '')} ({r})")
