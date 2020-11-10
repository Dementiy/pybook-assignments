import pathlib
import stat
import unittest
from unittest.mock import patch

from pyfakefs.fake_filesystem_unittest import TestCase

import pyvcs
from pyvcs.porcelain import add, checkout, commit
from pyvcs.repo import repo_create


@unittest.skipIf(pyvcs.__version_info__ < (0, 8, 0), "Нужна версия пакета 0.8.0 и выше")
class CheckoutTestCase(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_checkout(self):
        gitdir = repo_create(".")
        author = "Git User <gituser@example.com>"
        mode100644 = stat.S_IFREG | stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH
        quote = pathlib.Path("quote.txt")
        self.fs.create_file(quote, contents="that's what she said", st_mode=mode100644)
        letters = pathlib.Path("letters.txt")
        self.fs.create_file(letters, contents="abcdefg", st_mode=mode100644)
        digits = pathlib.Path("digits.txt")
        self.fs.create_file(digits, contents="1234567890", st_mode=mode100644)

        add(gitdir, [quote])
        quote_sha = commit(gitdir, "add quote.txt", author)
        add(gitdir, [letters])
        letters_sha = commit(gitdir, "add letters.txt", author)
        add(gitdir, [digits])
        digits_sha = commit(gitdir, "add digits.txt", author)

        checkout(gitdir, digits_sha)
        self.assertTrue(self.fs.exists("quote.txt"))
        self.assertTrue(self.fs.exists("letters.txt"))
        self.assertTrue(self.fs.exists("digits.txt"))

        checkout(gitdir, letters_sha)
        self.assertTrue(self.fs.exists("quote.txt"))
        self.assertTrue(self.fs.exists("letters.txt"))
        self.assertFalse(self.fs.exists("digits.txt"))

        checkout(gitdir, quote_sha)
        self.assertTrue(self.fs.exists("quote.txt"))
        self.assertFalse(self.fs.exists("letters.txt"))
        self.assertFalse(self.fs.exists("digits.txt"))

    def test_checkout_untracked_files_are_not_deleted(self):
        gitdir = repo_create(".")
        author = "Git User <gituser@example.com>"
        mode100644 = stat.S_IFREG | stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH
        quote = pathlib.Path("quote.txt")
        self.fs.create_file(quote, contents="that's what she said", st_mode=mode100644)
        letters = pathlib.Path("letters.txt")
        self.fs.create_file(letters, contents="abcdefg", st_mode=mode100644)
        digits = pathlib.Path("digits.txt")
        self.fs.create_file(digits, contents="1234567890", st_mode=mode100644)
        untracked = pathlib.Path("untracked.txt")
        self.fs.create_file(untracked, contents="don't touch me", st_mode=mode100644)

        add(gitdir, [quote])
        quote_sha = commit(gitdir, "add quote.txt", author)
        add(gitdir, [letters])
        letters_sha = commit(gitdir, "add letters.txt", author)
        add(gitdir, [digits])
        digits_sha = commit(gitdir, "add digits.txt", author)

        checkout(gitdir, digits_sha)
        self.assertTrue(self.fs.exists("quote.txt"))
        self.assertTrue(self.fs.exists("letters.txt"))
        self.assertTrue(self.fs.exists("digits.txt"))
        self.assertTrue(self.fs.exists("untracked.txt"))

        checkout(gitdir, letters_sha)
        self.assertTrue(self.fs.exists("quote.txt"))
        self.assertTrue(self.fs.exists("letters.txt"))
        self.assertFalse(self.fs.exists("digits.txt"))
        self.assertTrue(self.fs.exists("untracked.txt"))

        checkout(gitdir, quote_sha)
        self.assertTrue(self.fs.exists("quote.txt"))
        self.assertFalse(self.fs.exists("letters.txt"))
        self.assertFalse(self.fs.exists("digits.txt"))
        self.assertTrue(self.fs.exists("untracked.txt"))

    def test_checkout_dirs_are_deleted(self):
        gitdir = repo_create(".")
        author = "Git User <gituser@example.com>"
        mode100644 = stat.S_IFREG | stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH
        quote = pathlib.Path("quote.txt")
        self.fs.create_file(quote, contents="that's what she said", st_mode=mode100644)
        add(gitdir, [quote])
        quote_sha = commit(gitdir, "add quote.txt", author)

        letters = pathlib.Path("alphabeta") / "letters.txt"
        self.fs.create_file(letters, contents="abcdefg", st_mode=mode100644)
        add(gitdir, [letters])
        letters_sha = commit(gitdir, "add letters.txt", author)

        digits = pathlib.Path("numbers") / "digits.txt"
        self.fs.create_file(digits, contents="1234567890", st_mode=mode100644)
        add(gitdir, [digits])
        digits_sha = commit(gitdir, "add digits.txt", author)

        checkout(gitdir, digits_sha)
        self.assertTrue(self.fs.exists("quote.txt"))
        self.assertTrue(self.fs.exists(letters.absolute()))
        self.assertTrue(self.fs.exists(digits.absolute()))

        checkout(gitdir, letters_sha)
        self.assertTrue(self.fs.exists("quote.txt"))
        self.assertTrue(self.fs.exists(letters.parent.absolute()))
        self.assertFalse(
            self.fs.exists(digits.parent.absolute()),
            msg=f"Каталога `{digits.parent}` не должно существовать",
        )
        self.assertTrue(self.fs.exists(letters.absolute()))

        checkout(gitdir, quote_sha)
        self.assertTrue(self.fs.exists("quote.txt"))
        self.assertFalse(
            self.fs.exists(letters.parent.absolute()),
            msg=f"Каталога `{letters.parent}` не должно существовать",
        )
        self.assertFalse(
            self.fs.exists(digits.parent.absolute()),
            msg=f"Каталога `{digits.parent}` не должно существовать",
        )
