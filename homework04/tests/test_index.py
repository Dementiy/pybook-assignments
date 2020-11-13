import io
import pathlib
import unittest
from unittest.mock import patch

from pyfakefs.fake_filesystem_unittest import TestCase

import pyvcs
from pyvcs.index import GitIndexEntry, ls_files, read_index, update_index, write_index
from pyvcs.repo import repo_create


@unittest.skipIf(pyvcs.__version_info__ < (0, 4, 0), "Нужна версия пакета 0.4.0 и выше")
class GitIndexEntryTestCase(TestCase):
    def test_pack(self):
        entry = GitIndexEntry(
            ctime_s=1593379228,
            ctime_n=200331013,
            mtime_s=1593379228,
            mtime_n=200331013,
            dev=16777220,
            ino=8610507,
            mode=33188,
            uid=501,
            gid=20,
            size=4,
            sha1=b"W\x16\xcaY\x87\xcb\xf9}k\xb5I \xbe\xa6\xad\xde$-\x87\xe6",
            flags=7,
            name="bar.txt",
        )
        expected_pack = b"^\xf9\t\x9c\x0b\xf0\xcf\x05^\xf9\t\x9c\x0b\xf0\xcf\x05\x01\x00\x00\x04\x00\x83b\xcb\x00\x00\x81\xa4\x00\x00\x01\xf5\x00\x00\x00\x14\x00\x00\x00\x04W\x16\xcaY\x87\xcb\xf9}k\xb5I \xbe\xa6\xad\xde$-\x87\xe6\x00\x07bar.txt\x00\x00\x00"
        self.assertEqual(expected_pack, entry.pack())

    def test_unpack(self):
        pack = b"^\xf9\t\x9c\x0b\xf0\xcf\x05^\xf9\t\x9c\x0b\xf0\xcf\x05\x01\x00\x00\x04\x00\x83b\xcb\x00\x00\x81\xa4\x00\x00\x01\xf5\x00\x00\x00\x14\x00\x00\x00\x04W\x16\xcaY\x87\xcb\xf9}k\xb5I \xbe\xa6\xad\xde$-\x87\xe6\x00\x07bar.txt\x00\x00\x00"
        expected_entry = GitIndexEntry(
            ctime_s=1593379228,
            ctime_n=200331013,
            mtime_s=1593379228,
            mtime_n=200331013,
            dev=16777220,
            ino=8610507,
            mode=33188,
            uid=501,
            gid=20,
            size=4,
            sha1=b"W\x16\xcaY\x87\xcb\xf9}k\xb5I \xbe\xa6\xad\xde$-\x87\xe6",
            flags=7,
            name="bar.txt",
        )
        self.assertEqual(expected_entry, GitIndexEntry.unpack(pack))


@unittest.skipIf(pyvcs.__version_info__ < (0, 4, 0), "Нужна версия пакета 0.4.0 и выше")
class ReadIndexTestCase(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_read_index(self):
        gitdir = repo_create(".")
        raw_index = b"DIRC\x00\x00\x00\x02\x00\x00\x00\x03^\xf9\t\x9c\x0b\xf0\xcf\x05^\xf9\t\x9c\x0b\xf0\xcf\x05\x01\x00\x00\x04\x00\x83b\xcb\x00\x00\x81\xa4\x00\x00\x01\xf5\x00\x00\x00\x14\x00\x00\x00\x04W\x16\xcaY\x87\xcb\xf9}k\xb5I \xbe\xa6\xad\xde$-\x87\xe6\x00\x07bar.txt\x00\x00\x00^\xf9\t\xca\x1f\xf0l^^\xf9\t\xca\x1f\xf0l^\x01\x00\x00\x04\x00\x83b\xf6\x00\x00\x81\xa4\x00\x00\x01\xf5\x00\x00\x00\x14\x00\x00\x00\x07\x9f5\x8aJ\xdd\xef\xca\xb2\x94\xb8>B\x82\xbf\xef\x1f\x96%\xa2I\x00\x0fbaz/numbers.txt\x00\x00\x00^\xf9\t\xa18\xd3\xad\xbb^\xf9\t\xa18\xd3\xad\xbb\x01\x00\x00\x04\x00\x83b\xd3\x00\x00\x81\xa4\x00\x00\x01\xf5\x00\x00\x00\x14\x00\x00\x00\x04%|\xc5d,\xb1\xa0T\xf0\x8c\xc8?-\x94>V\xfd>\xbe\x99\x00\x07foo.txt\x00\x00\x00k\xd6q\xa7d\x10\x8e\x80\x93F]\x0c}+\x82\xfb\xc7:\xa8\x11"
        self.fs.create_file(gitdir / "index", contents=raw_index)

        entries = read_index(gitdir)
        self.assertEqual(3, len(entries))
        # TODO: Add sha
        self.assertEqual(
            ["bar.txt", "baz/numbers.txt", "foo.txt"], [e.name for e in entries]
        )

    def test_read_index_when_index_doesnt_exist(self):
        gitdir = repo_create(".")
        entries = read_index(gitdir)
        self.assertEqual(0, len(entries))
        self.assertEqual([], entries)


@unittest.skipIf(pyvcs.__version_info__ < (0, 4, 0), "Нужна версия пакета 0.4.0 и выше")
class LsFilesTestCase(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_ls_files(self):
        gitdir = repo_create(".")
        raw_index = b"DIRC\x00\x00\x00\x02\x00\x00\x00\x03^\xf9\t\x9c\x0b\xf0\xcf\x05^\xf9\t\x9c\x0b\xf0\xcf\x05\x01\x00\x00\x04\x00\x83b\xcb\x00\x00\x81\xa4\x00\x00\x01\xf5\x00\x00\x00\x14\x00\x00\x00\x04W\x16\xcaY\x87\xcb\xf9}k\xb5I \xbe\xa6\xad\xde$-\x87\xe6\x00\x07bar.txt\x00\x00\x00^\xf9\t\xca\x1f\xf0l^^\xf9\t\xca\x1f\xf0l^\x01\x00\x00\x04\x00\x83b\xf6\x00\x00\x81\xa4\x00\x00\x01\xf5\x00\x00\x00\x14\x00\x00\x00\x07\x9f5\x8aJ\xdd\xef\xca\xb2\x94\xb8>B\x82\xbf\xef\x1f\x96%\xa2I\x00\x0fbaz/numbers.txt\x00\x00\x00^\xf9\t\xa18\xd3\xad\xbb^\xf9\t\xa18\xd3\xad\xbb\x01\x00\x00\x04\x00\x83b\xd3\x00\x00\x81\xa4\x00\x00\x01\xf5\x00\x00\x00\x14\x00\x00\x00\x04%|\xc5d,\xb1\xa0T\xf0\x8c\xc8?-\x94>V\xfd>\xbe\x99\x00\x07foo.txt\x00\x00\x00k\xd6q\xa7d\x10\x8e\x80\x93F]\x0c}+\x82\xfb\xc7:\xa8\x11"
        self.fs.create_file(gitdir / "index", contents=raw_index)
        expected_output = "bar.txt\nbaz/numbers.txt\nfoo.txt"
        with patch("sys.stdout", new=io.StringIO()) as out:
            ls_files(gitdir, details=False)
            self.assertEqual(expected_output, out.getvalue().strip())

    def test_ls_files_with_details(self):
        gitdir = repo_create(".")
        raw_index = b"DIRC\x00\x00\x00\x02\x00\x00\x00\x03^\xf9\t\x9c\x0b\xf0\xcf\x05^\xf9\t\x9c\x0b\xf0\xcf\x05\x01\x00\x00\x04\x00\x83b\xcb\x00\x00\x81\xa4\x00\x00\x01\xf5\x00\x00\x00\x14\x00\x00\x00\x04W\x16\xcaY\x87\xcb\xf9}k\xb5I \xbe\xa6\xad\xde$-\x87\xe6\x00\x07bar.txt\x00\x00\x00^\xf9\t\xca\x1f\xf0l^^\xf9\t\xca\x1f\xf0l^\x01\x00\x00\x04\x00\x83b\xf6\x00\x00\x81\xa4\x00\x00\x01\xf5\x00\x00\x00\x14\x00\x00\x00\x07\x9f5\x8aJ\xdd\xef\xca\xb2\x94\xb8>B\x82\xbf\xef\x1f\x96%\xa2I\x00\x0fbaz/numbers.txt\x00\x00\x00^\xf9\t\xa18\xd3\xad\xbb^\xf9\t\xa18\xd3\xad\xbb\x01\x00\x00\x04\x00\x83b\xd3\x00\x00\x81\xa4\x00\x00\x01\xf5\x00\x00\x00\x14\x00\x00\x00\x04%|\xc5d,\xb1\xa0T\xf0\x8c\xc8?-\x94>V\xfd>\xbe\x99\x00\x07foo.txt\x00\x00\x00k\xd6q\xa7d\x10\x8e\x80\x93F]\x0c}+\x82\xfb\xc7:\xa8\x11"
        self.fs.create_file(gitdir / "index", contents=raw_index)
        expected_output = "\n".join(
            [
                "100644 5716ca5987cbf97d6bb54920bea6adde242d87e6 0	bar.txt",
                "100644 9f358a4addefcab294b83e4282bfef1f9625a249 0	baz/numbers.txt",
                "100644 257cc5642cb1a054f08cc83f2d943e56fd3ebe99 0	foo.txt",
            ]
        )
        with patch("sys.stdout", new=io.StringIO()) as out:
            ls_files(gitdir, details=True)
            self.assertEqual(expected_output, out.getvalue().strip())


@unittest.skipIf(pyvcs.__version_info__ < (0, 4, 0), "Нужна версия пакета 0.4.0 и выше")
class WriteIndexTestCase(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_write_index(self):
        gitdir = repo_create(".")
        entries = [
            GitIndexEntry(
                ctime_s=1593379228,
                ctime_n=200331013,
                mtime_s=1593379228,
                mtime_n=200331013,
                dev=16777220,
                ino=8610507,
                mode=33188,
                uid=501,
                gid=20,
                size=4,
                sha1=b"W\x16\xcaY\x87\xcb\xf9}k\xb5I \xbe\xa6\xad\xde$-\x87\xe6",
                flags=7,
                name="bar.txt",
            ),
            GitIndexEntry(
                ctime_s=1593379274,
                ctime_n=535850078,
                mtime_s=1593379274,
                mtime_n=535850078,
                dev=16777220,
                ino=8610550,
                mode=33188,
                uid=501,
                gid=20,
                size=7,
                sha1=b"\x9f5\x8aJ\xdd\xef\xca\xb2\x94\xb8>B\x82\xbf\xef\x1f\x96%\xa2I",
                flags=15,
                name="baz/numbers.txt",
            ),
            GitIndexEntry(
                ctime_s=1593379233,
                ctime_n=953396667,
                mtime_s=1593379233,
                mtime_n=953396667,
                dev=16777220,
                ino=8610515,
                mode=33188,
                uid=501,
                gid=20,
                size=4,
                sha1=b"%|\xc5d,\xb1\xa0T\xf0\x8c\xc8?-\x94>V\xfd>\xbe\x99",
                flags=7,
                name="foo.txt",
            ),
        ]
        write_index(gitdir, entries)

        index = gitdir / "index"
        with index.open(mode="rb") as f:
            index_data = f.read()
        expected_index_data = b"DIRC\x00\x00\x00\x02\x00\x00\x00\x03^\xf9\t\x9c\x0b\xf0\xcf\x05^\xf9\t\x9c\x0b\xf0\xcf\x05\x01\x00\x00\x04\x00\x83b\xcb\x00\x00\x81\xa4\x00\x00\x01\xf5\x00\x00\x00\x14\x00\x00\x00\x04W\x16\xcaY\x87\xcb\xf9}k\xb5I \xbe\xa6\xad\xde$-\x87\xe6\x00\x07bar.txt\x00\x00\x00^\xf9\t\xca\x1f\xf0l^^\xf9\t\xca\x1f\xf0l^\x01\x00\x00\x04\x00\x83b\xf6\x00\x00\x81\xa4\x00\x00\x01\xf5\x00\x00\x00\x14\x00\x00\x00\x07\x9f5\x8aJ\xdd\xef\xca\xb2\x94\xb8>B\x82\xbf\xef\x1f\x96%\xa2I\x00\x0fbaz/numbers.txt\x00\x00\x00^\xf9\t\xa18\xd3\xad\xbb^\xf9\t\xa18\xd3\xad\xbb\x01\x00\x00\x04\x00\x83b\xd3\x00\x00\x81\xa4\x00\x00\x01\xf5\x00\x00\x00\x14\x00\x00\x00\x04%|\xc5d,\xb1\xa0T\xf0\x8c\xc8?-\x94>V\xfd>\xbe\x99\x00\x07foo.txt\x00\x00\x00k\xd6q\xa7d\x10\x8e\x80\x93F]\x0c}+\x82\xfb\xc7:\xa8\x11"
        self.assertEqual(expected_index_data, index_data)


@unittest.skipIf(pyvcs.__version_info__ < (0, 4, 0), "Нужна версия пакета 0.4.0 и выше")
class UpdateIndexTestCase(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_update_index(self):
        gitdir = repo_create(".")
        index = gitdir / "index"
        quote = pathlib.Path("quote.txt")
        self.fs.create_file(quote, contents="that's what she said")

        self.assertFalse(index.exists())
        update_index(gitdir, [quote])
        self.assertTrue(index.exists())
        entries = read_index(gitdir)
        self.assertEqual(1, len(entries))
        expected_sha = "7e774cf533c51803125d4659f3488bd9dffc41a6"
        obj_path = gitdir / "objects" / expected_sha[:2] / expected_sha[2:]
        self.assertTrue(obj_path.exists())

    def test_update_index_many(self):
        gitdir = repo_create(".")
        index = gitdir / "index"
        letters = pathlib.Path("letters.txt")
        self.fs.create_file(letters, contents="abcdefg")
        digits = pathlib.Path("digits.txt")
        self.fs.create_file(digits, contents="1234567890")

        self.assertFalse(index.exists())
        update_index(gitdir, [letters, digits])
        self.assertTrue(index.exists())
        entries = read_index(gitdir)
        self.assertEqual(2, len(entries))

        names = [e.name for e in entries]
        self.assertEqual(["digits.txt", "letters.txt"], names)

    def test_update_index_subdirs(self):
        gitdir = repo_create(".")
        index = gitdir / "index"
        quote = pathlib.Path("quote.txt")
        self.fs.create_file(quote, contents="that's what she said")
        letters = pathlib.Path("alphabeta") / "letters.txt"
        self.fs.create_file(letters, contents="abcdefg")
        digits = pathlib.Path("numbers") / "digits.txt"
        self.fs.create_file(digits, contents="1234567890")

        self.assertFalse(index.exists())
        update_index(gitdir, [quote, letters, digits])
        self.assertTrue(index.exists())
        entries = read_index(gitdir)
        self.assertEqual(3, len(entries))

        names = [e.name for e in entries]
        self.assertEqual(
            ["alphabeta/letters.txt", "numbers/digits.txt", "quote.txt"], names
        )
