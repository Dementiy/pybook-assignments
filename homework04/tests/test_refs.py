import unittest

from pyfakefs.fake_filesystem_unittest import TestCase

import pyvcs
from pyvcs.refs import get_ref, is_detached, ref_resolve, resolve_head, update_ref
from pyvcs.repo import repo_create


@unittest.skipIf(pyvcs.__version_info__ < (0, 7, 0), "Нужна версия пакета 0.7.0 и выше")
class ReferencesTestCase(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_ref_resolve(self):
        gitdir = repo_create(".")

        master_sha = "d6ae59694dfec74d7f5ca87608f31c884dc9b0f9"
        master = gitdir / "refs" / "heads" / "master"
        self.fs.create_file(master, contents=master_sha)
        data = ref_resolve(gitdir, "HEAD")
        self.assertEqual(master_sha, data)

        ref = "refs/heads/master"
        data = ref_resolve(gitdir, ref)
        self.assertEqual(master_sha, data)

    def test_resolve_head(self):
        gitdir = repo_create(".")

        data = resolve_head(gitdir)
        self.assertIsNone(data)

        master_sha = "d6ae59694dfec74d7f5ca87608f31c884dc9b0f9"
        master = gitdir / "refs" / "heads" / "master"
        self.fs.create_file(master, contents=master_sha)
        data = resolve_head(gitdir)
        self.assertEqual(master_sha, data)

    def test_get_ref(self):
        gitdir = repo_create(".")
        ref = get_ref(gitdir)
        self.assertEqual("refs/heads/master", ref)

    def test_is_detached(self):
        gitdir = repo_create(".")

        detached = is_detached(gitdir)
        self.assertFalse(detached)

        head = gitdir / "HEAD"
        with head.open(mode="w") as f:
            f.write("d6ae59694dfec74d7f5ca87608f31c884dc9b0f9")
        detached = is_detached(gitdir)
        self.assertTrue(detached)

    def test_update_ref(self):
        gitdir = repo_create(".")

        master_sha = "d6ae59694dfec74d7f5ca87608f31c884dc9b0f9"
        update_ref(gitdir, "refs/heads/master", master_sha)

        master = gitdir / "refs" / "heads" / "master"
        with master.open() as f:
            sha = f.read().strip()

        self.assertEqual(master_sha, sha)
