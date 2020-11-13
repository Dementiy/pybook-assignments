import pathlib
import stat
import time
import unittest
from unittest.mock import patch

from pyfakefs.fake_filesystem_unittest import TestCase

import pyvcs
from pyvcs.index import read_index, update_index
from pyvcs.repo import repo_create
from pyvcs.tree import commit_tree, write_tree


@unittest.skipIf(pyvcs.__version_info__ < (0, 5, 0), "Нужна версия пакета 0.5.0 и выше")
class WriteTreeTestCase(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_write_tree(self):
        gitdir = repo_create(".")
        animals = pathlib.Path("animals.txt")
        mode100644 = stat.S_IFREG | stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH
        self.fs.create_file(
            animals,
            contents="Big blue basilisks bawl in the basement\n",
            st_mode=mode100644,
        )
        update_index(gitdir, [animals], write=True)
        entries = read_index(gitdir)
        sha = write_tree(gitdir, entries)
        self.assertEqual("dc6b8ea09fb7573a335c5fb953b49b85bb6ca985", sha)

    def test_write_tree_subdirs(self):
        gitdir = repo_create(".")
        mode100644 = stat.S_IFREG | stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH
        quote = pathlib.Path("quote.txt")
        self.fs.create_file(quote, contents="that's what she said", st_mode=mode100644)
        letters = pathlib.Path("alphabeta") / "letters.txt"
        self.fs.create_file(letters, contents="abcdefg", st_mode=mode100644)
        digits = pathlib.Path("numbers") / "digits.txt"
        self.fs.create_file(digits, contents="1234567890", st_mode=mode100644)
        update_index(gitdir, [quote, letters, digits], write=True)
        entries = read_index(gitdir)
        sha = write_tree(gitdir, entries)
        self.assertEqual("a9cde03408c68cbb205b038140b4c3a38aa1d01a", sha)

        alphabeta_tree_sha = "7926bf494dcdb82261e1ca113116610f8d05470b"
        alphabeta_tree_obj = gitdir / "objects" / alphabeta_tree_sha[:2] / alphabeta_tree_sha[2:]
        self.assertTrue(alphabeta_tree_obj.exists())

        numbers_tree_sha = "32ad3641a773ce34816dece1ce63cc24c8a514d0"
        numbers_tree_obj = gitdir / "objects" / numbers_tree_sha[:2] / numbers_tree_sha[2:]
        self.assertTrue(numbers_tree_obj.exists())


@unittest.skipIf(pyvcs.__version_info__ < (0, 6, 0), "Нужна версия пакета 0.6.0 и выше")
class CommitTreeTestCase(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    @patch("time.timezone", -10800)
    @patch("time.localtime", return_value=time.localtime(1593638381))
    def test_commit_tree(self, localtime):
        gitdir = repo_create(".")
        tree_sha = "dc6b8ea09fb7573a335c5fb953b49b85bb6ca985"
        author = "Dmitriy Sorokin <Dementiy@yandex.ru>"
        message = "initial commit"
        commit_sha = commit_tree(gitdir, tree_sha, message, parent=None, author=author)
        self.assertEqual("f60952d53906d8b2e6f8567762f86fbe7ca4ac65", commit_sha)
