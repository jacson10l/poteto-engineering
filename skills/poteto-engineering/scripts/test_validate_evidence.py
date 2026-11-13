import copy
import hashlib
from pathlib import Path
import tempfile
import unittest
from validate_evidence import validate


class EvidenceTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        content = b'one assertion passed\n'
        (self.root / 'run.log').write_bytes(content)
        self.manifest = {
            'schema_version': 1, 'task': 'Fix a CLI boundary',
            'source': {'revision': 'local-test-revision', 'worktree': 'clean'},
            'environment': 'isolated unittest fixture', 'captured_at': '2026-11-13T00:00:00Z',
            'artifacts': [{'id': 'E1', 'type': 'log', 'path': 'run.log',
                           'sha256': hashlib.sha256(content).hexdigest()}],
            'checks': [{'id': 'C1', 'status': 'pass', 'mode': 'command',
                        'procedure': 'python -m unittest', 'source_revision': 'local-test-revision',
                        'exit_code': 0, 'observed': 'one assertion passed', 'artifact_ids': ['E1']}],
            'acceptance': [{'id': 'A1', 'description': 'CLI checks boundary', 'required': True,
                            'requires_visual': False, 'check_ids': ['C1']}],
        }

    def test_valid_manifest(self):
        self.assertEqual(validate(self.manifest, self.root), [])

    def test_missing_artifact(self):
        (self.root / 'run.log').unlink()
        self.assertTrue(validate(self.manifest, self.root))

    def test_tampered_artifact(self):
        (self.root / 'run.log').write_text('different content')
        self.assertTrue(validate(self.manifest, self.root))

    def test_path_escape(self):
        self.manifest['artifacts'][0]['path'] = '../outside.log'
        self.assertTrue(validate(self.manifest, self.root))

    def test_symlink_escape(self):
        (self.root / 'external.log').symlink_to('/etc/hosts')
        self.manifest['artifacts'][0]['path'] = 'external.log'
        self.assertTrue(validate(self.manifest, self.root))

    def test_false_pass_exit(self):
        self.manifest['checks'][0]['exit_code'] = 2
        self.assertTrue(validate(self.manifest, self.root))

    def test_boolean_exit_not_integer_zero(self):
        self.manifest['checks'][0]['exit_code'] = False
        self.assertTrue(validate(self.manifest, self.root))

    def test_stale_revision(self):
        self.manifest['checks'][0]['source_revision'] = 'old'
        self.assertTrue(validate(self.manifest, self.root))

    def test_dirty_snapshot(self):
        self.manifest['source'].update(worktree='dirty', patch_sha256='a' * 64)
        self.assertTrue(validate(self.manifest, self.root))
        self.manifest['checks'][0]['patch_sha256'] = 'a' * 64
        self.assertEqual(validate(self.manifest, self.root), [])

    def test_ui_cannot_use_only_log(self):
        self.manifest['acceptance'][0]['requires_visual'] = True
        self.assertTrue(validate(self.manifest, self.root))

    def test_required_cannot_be_skipped(self):
        self.manifest['checks'][0].update(status='skipped', reason='tool unavailable')
        self.assertTrue(validate(self.manifest, self.root))

    def test_empty_acceptance(self):
        self.manifest['acceptance'] = []
        self.assertTrue(validate(self.manifest, self.root))

    def test_missing_reference(self):
        self.manifest['acceptance'][0]['check_ids'] = ['missing']
        self.assertTrue(validate(self.manifest, self.root))

    def test_duplicate_ids(self):
        self.manifest['checks'].append(copy.deepcopy(self.manifest['checks'][0]))
        self.assertTrue(validate(self.manifest, self.root))

    def test_optional_check_requires_reason(self):
        self.manifest['checks'].append({'id': 'C2', 'status': 'blocked', 'procedure': 'optional check'})
        self.assertTrue(validate(self.manifest, self.root))
        self.manifest['checks'][1]['reason'] = 'Optional environment unavailable'
        self.assertEqual(validate(self.manifest, self.root), [])

    def test_empty_artifact_even_with_correct_hash(self):
        (self.root / 'run.log').write_bytes(b'')
        self.manifest['artifacts'][0]['sha256'] = hashlib.sha256(b'').hexdigest()
        self.assertTrue(validate(self.manifest, self.root))


if __name__ == '__main__':
    unittest.main()
