#!/usr/bin/env python3
"""Validate evidence bookkeeping; never execute commands or certify correctness."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

STATUSES = {'pass', 'fail', 'blocked', 'skipped', 'not-run'}
VISUAL_TYPES = {'image', 'video', 'trace'}


def validate(data, root):
    errors = []
    def need(ok, message):
        if not ok:
            errors.append(message)
        return bool(ok)
    def text(value):
        return isinstance(value, str) and bool(value.strip())
    if not isinstance(data, dict):
        return ['Manifest must be an object']
    need(type(data.get('schema_version')) is int and data['schema_version'] == 1,
         'schema_version must be 1')
    need(text(data.get('task')), 'task is required')
    source = data.get('source', {})
    if not isinstance(source, dict):
        source = {}
    revision = source.get('revision')
    need(text(revision), 'source.revision is required')
    need(source.get('worktree') in {'clean', 'dirty'}, 'source.worktree must be clean or dirty')
    if source.get('worktree') == 'dirty':
        need(isinstance(source.get('patch_sha256'), str) and
             re.fullmatch(r'[0-9a-f]{64}', source['patch_sha256']),
             'Dirty worktree requires patch_sha256 (include relevant untracked files in the snapshot)')
    need(text(data.get('environment')), 'environment is required')
    need(text(data.get('captured_at')), 'captured_at is required')
    def records(key):
        value = data.get(key)
        if not need(isinstance(value, list) and bool(value), key + ' must be a nonempty list'):
            return {}
        result = {}
        for entry in value:
            if not need(isinstance(entry, dict) and text(entry.get('id')), key + ' entries need ids'):
                continue
            ident = entry['id']
            if not need(ident not in result, key + ': duplicate id ' + ident):
                continue
            result[ident] = entry
        return result
    artifacts = records('artifacts')
    checks = records('checks')
    acceptance = records('acceptance')
    root = root.resolve()
    for ident, item in artifacts.items():
        label = 'artifact ' + ident + ': '
        kind = item.get('type')
        need(kind in {'log', 'data', 'image', 'video', 'trace'}, label + 'unsupported type')
        raw = item.get('path')
        if not need(text(raw), label + 'path is required'):
            continue
        rel = Path(raw)
        target = (root / rel).resolve()
        if not need(not rel.is_absolute() and target.is_relative_to(root), label + 'path escapes evidence directory'):
            continue
        if not need(target.is_file(), label + 'file is missing'):
            continue
        try:
            need(target.stat().st_size > 0, label + 'file is empty')
            hasher = hashlib.sha256()
            with target.open('rb') as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                    hasher.update(chunk)
            digest = hasher.hexdigest()
            need(item.get('sha256') == digest, label + 'SHA256 mismatch')
        except OSError as exc:
            errors.append(label + str(exc))
    for ident, check in checks.items():
        label = 'check ' + ident + ': '
        status = check.get('status')
        need(status in STATUSES, label + 'invalid status')
        need(text(check.get('procedure')), label + 'procedure is required')
        if status == 'pass':
            need(check.get('source_revision') == revision, label + 'source revision mismatch')
            if source.get('worktree') == 'dirty':
                need(check.get('patch_sha256') == source.get('patch_sha256'), label + 'patch snapshot mismatch')
            need(text(check.get('observed')), label + 'observed result is required')
            mode = check.get('mode')
            need(mode in {'command', 'observation'}, label + 'mode must be command or observation')
            if mode == 'command':
                need(type(check.get('exit_code')) is int and check['exit_code'] == 0,
                     label + 'passing command needs integer exit_code 0')
            ids = check.get('artifact_ids')
            if need(isinstance(ids, list) and bool(ids), label + 'passing check needs artifacts'):
                need(all(isinstance(a, str) and a in artifacts for a in ids), label + 'unknown artifact id')
        else:
            need(text(check.get('reason')), label + 'non-pass check needs reason')
    required_count = 0
    for ident, criterion in acceptance.items():
        label = 'acceptance ' + ident + ': '
        need(text(criterion.get('description')), label + 'description is required')
        required = criterion.get('required')
        need(type(required) is bool, label + 'required must be boolean')
        if required is not True:
            need(text(criterion.get('reason')), label + 'optional criterion needs reason')
            continue
        required_count += 1
        ids = criterion.get('check_ids')
        if not need(isinstance(ids, list) and bool(ids), label + 'check_ids is required'):
            continue
        for cid in ids:
            if not need(isinstance(cid, str) and cid in checks, label + 'unknown check id'):
                continue
            need(checks[cid].get('status') == 'pass', label + cid + ' is not pass')
        visual = criterion.get('requires_visual')
        need(type(visual) is bool, label + 'requires_visual must be boolean')
        if visual is True:
            evidence_ids = []
            for cid in ids:
                if isinstance(cid, str) and cid in checks and checks[cid].get('status') == 'pass':
                    value = checks[cid].get('artifact_ids')
                    if isinstance(value, list):
                        evidence_ids.extend(value)
            need(any(isinstance(a, str) and artifacts.get(a, {}).get('type') in VISUAL_TYPES
                     for a in evidence_ids), label + 'visual evidence is required')
    need(required_count > 0, 'At least one required acceptance criterion is necessary')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.manifest.read_text(encoding='utf-8'))
        errors = validate(data, args.manifest.parent)
    except (OSError, ValueError, TypeError, KeyError) as exc:
        errors = ['Cannot validate manifest: ' + str(exc)]
    print(json.dumps({'status': 'invalid' if errors else 'manifest-consistent',
                      'errors': errors,
                      'limitation': 'Metadata and file consistency only; does not certify execution, visual content, correctness, or merge authorization.'},
                     ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
