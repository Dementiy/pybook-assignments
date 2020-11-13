import io
import pathlib
import stat
import unittest
import zlib
from unittest.mock import patch

from pyfakefs.fake_filesystem_unittest import TestCase

import pyvcs
from pyvcs import index, objects, porcelain, repo, tree


@unittest.skipIf(pyvcs.__version_info__ < (0, 2, 0), "Нужна версия пакета 0.2.0 и выше")
class HashObjectTestCase(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_compute_object_id(self):
        contents = "that's what she said"
        data = contents.encode()
        sha = objects.hash_object(data, fmt="blob")
        expected_sha = "7e774cf533c51803125d4659f3488bd9dffc41a6"
        self.assertEqual(expected_sha, sha)

    def test_compute_object_id_and_create_a_blob(self):
        gitdir = repo.repo_create(".")

        contents = "that's what she said"
        data = contents.encode()
        sha = objects.hash_object(data, fmt="blob", write=True)
        expected_sha = "7e774cf533c51803125d4659f3488bd9dffc41a6"
        self.assertEqual(expected_sha, sha)

        obj_path = gitdir / "objects" / "7e" / "774cf533c51803125d4659f3488bd9dffc41a6"
        self.assertTrue(obj_path.exists())

        with obj_path.open(mode="rb") as f:
            content = zlib.decompress(f.read())
        self.assertEqual(b"blob 20\x00that's what she said", content)

    def test_hash_object_twice(self):
        _ = repo.repo_create(".")

        contents = "that's what she said"
        data = contents.encode()
        expected_sha = "7e774cf533c51803125d4659f3488bd9dffc41a6"
        sha = objects.hash_object(data, fmt="blob", write=True)
        self.assertEqual(expected_sha, sha)
        sha = objects.hash_object(data, fmt="blob", write=True)
        self.assertEqual(expected_sha, sha)


@unittest.skipIf(pyvcs.__version_info__ < (0, 3, 0), "Нужна версия пакета 0.3.0 и выше")
class ResolveObjectTestCase(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_resolve_object(self):
        gitdir = repo.repo_create(".")
        blob_path = gitdir / "objects" / "7e" / "774cf533c51803125d4659f3488bd9dffc41a6"
        self.fs.create_file(file_path=blob_path)

        objs = objects.resolve_object("7e774", gitdir)
        self.assertEqual(1, len(objs))

        [sha] = objs
        self.assertEqual("7e774cf533c51803125d4659f3488bd9dffc41a6", sha)

    def test_resolve_many_objects(self):
        gitdir = repo.repo_create(".")

        blob_path = gitdir / "objects" / "7e" / "774cf533c51803125d4659f3488bd9dffc41a1"
        self.fs.create_file(file_path=blob_path)
        blob_path = gitdir / "objects" / "7e" / "774cf533c51803125d4659f3488bd9dffc41a2"
        self.fs.create_file(file_path=blob_path)
        blob_path = gitdir / "objects" / "7e" / "774cf533c51803125d4659f3488bd9dffc41a3"
        self.fs.create_file(file_path=blob_path)

        objs = objects.resolve_object("7e774", gitdir)
        self.assertEqual(3, len(objs))
        self.assertEqual(
            [
                "7e774cf533c51803125d4659f3488bd9dffc41a1",
                "7e774cf533c51803125d4659f3488bd9dffc41a2",
                "7e774cf533c51803125d4659f3488bd9dffc41a3",
            ],
            objs,
        )

    def test_resolve_object_name_ge_4_and_le_40_chars(self):
        gitdir = repo.repo_create(".")
        blob_path = gitdir / "objects" / "7e" / "774cf533c51803125d4659f3488bd9dffc41a1"
        self.fs.create_file(file_path=blob_path)

        obj_name = "7e7"
        with self.assertRaises(Exception) as ctx:
            objects.resolve_object(obj_name, gitdir)
        self.assertEqual(f"Not a valid object name {obj_name}", str(ctx.exception))

        obj_name = "7e7774cf533c51803125d4659f3488bd9dffc41a1e"
        with self.assertRaises(Exception) as ctx:
            objects.resolve_object(obj_name, gitdir)
        self.assertEqual(f"Not a valid object name {obj_name}", str(ctx.exception))

    def test_resolve_object_that_does_not_exists(self):
        gitdir = repo.repo_create(".")
        blob_path = gitdir / "objects" / "7e" / "774cf533c51803125d4659f3488bd9dffc41a1"
        self.fs.create_file(file_path=blob_path)

        obj_name = "7e775"
        with self.assertRaises(Exception) as ctx:
            objects.resolve_object(obj_name, gitdir)
        self.assertEqual(f"Not a valid object name {obj_name}", str(ctx.exception))


@unittest.skipIf(pyvcs.__version_info__ < (0, 3, 0), "Нужна версия пакета 0.3.0 и выше")
class ReadObjectTestCase(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_read_object(self):
        gitdir = repo.repo_create(".")
        blob_path = gitdir / "objects" / "7e" / "774cf533c51803125d4659f3488bd9dffc41a6"
        blob_contents = (
            b"x\x9cK\xca\xc9OR02`(\xc9H,Q/V(\x07R\n\xc5\x19\xa9\n\xc5\x89\x99)\x00\x83:\tb"
        )
        self.fs.create_file(file_path=blob_path, contents=blob_contents)
        fmt, data = objects.read_object("7e774cf533c51803125d4659f3488bd9dffc41a6", gitdir)
        self.assertEqual("blob", fmt)
        self.assertEqual(b"that's what she said", data)


@unittest.skipIf(pyvcs.__version_info__ < (0, 3, 0), "Нужна версия пакета 0.3.0 и выше")
class CatFileTestCase(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_cat_pretty_blob_file(self):
        gitdir = repo.repo_create(".")
        blob_path = gitdir / "objects" / "7e" / "774cf533c51803125d4659f3488bd9dffc41a6"
        blob_contents = (
            b"x\x9cK\xca\xc9OR02`(\xc9H,Q/V(\x07R\n\xc5\x19\xa9\n\xc5\x89\x99)\x00\x83:\tb"
        )
        self.fs.create_file(file_path=blob_path, contents=blob_contents)

        with patch("sys.stdout", new=io.StringIO()) as out:
            objects.cat_file("7e774cf533c51803125d4659f3488bd9dffc41a6", pretty=True)
            self.assertEqual("that's what she said", out.getvalue().strip())

    @unittest.skipIf(pyvcs.__version_info__ < (0, 6, 0), "Нужна версия пакета 0.6.0 и выше")
    def test_cat_tree_file(self):
        gitdir = repo.repo_create(".")
        mode100644 = stat.S_IFREG | stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH
        quote = pathlib.Path("quote.txt")
        self.fs.create_file(quote, contents="that's what she said", st_mode=mode100644)
        letters = pathlib.Path("alphabeta") / "letters.txt"
        self.fs.create_file(letters, contents="abcdefg", st_mode=mode100644)
        digits = pathlib.Path("numbers") / "digits.txt"
        self.fs.create_file(digits, contents="1234567890", st_mode=mode100644)
        index.update_index(gitdir, [quote, letters, digits], write=True)
        entries = index.read_index(gitdir)
        sha = tree.write_tree(gitdir, entries)
        self.assertEqual("a9cde03408c68cbb205b038140b4c3a38aa1d01a", sha)

        expected_output = "\n".join(
            [
                "040000 tree 7926bf494dcdb82261e1ca113116610f8d05470b\talphabeta",
                "040000 tree 32ad3641a773ce34816dece1ce63cc24c8a514d0\tnumbers",
                "100644 blob 7e774cf533c51803125d4659f3488bd9dffc41a6\tquote.txt",
            ]
        )

        with patch("sys.stdout", new=io.StringIO()) as out:
            objects.cat_file(sha, pretty=True)
            self.assertEqual(expected_output, out.getvalue().strip())

    @unittest.skipIf(pyvcs.__version_info__ < (0, 6, 0), "Нужна версия пакета 0.6.0 и выше")
    def test_cat_commit_file(self):
        gitdir = repo.repo_create(".")
        obj = b"x\x9c\x95\x8dA\n\x021\x0c\x00=\xf7\x15\xb9\x0b\x92\x92ljA\xc4\x83\x1fI\xdb,\x16\xec.\x94.\xb8\xbf\x17\x14\x1f\xe0m.3\x93\xd7\xd6\xea\x00\x1f\xe80\xba\x19`&d\x942G5\x9d8\x85\xb9H\xe23\t\xb2\x0f6EMASL\xc9\xe96\x1ek\x87\xbb5[F\xdd\xe1\xf2\xa3\xdb\xaeK\xb1\xd7\xa9oW\xf0\x82\xc4\xc8$\x02G$D\x97?\xbba\x7f\x8b\xae.uT}\xc2\xb7\xe0\xde\xa159\x17"
        sha = "faa73127e7a7b97faf08c147e69130a424c5ddbb"
        obj_path = gitdir / "objects" / sha[:2] / sha[2:]
        self.fs.create_file(obj_path, contents=obj)

        expected_output = "\n".join(
            [
                "tree 0c30406df9aea54b7fd6b48360417e59ab7ab9bb",
                "author Dementiy <Dementiy@yandex.ru> 1603404366 +0300",
                "committer Dementiy <Dementiy@yandex.ru> 1603404366 +0300",
                "",
                "initial commit",
            ]
        )

        with patch("sys.stdout", new=io.StringIO()) as out:
            objects.cat_file(sha, pretty=True)
            self.assertEqual(expected_output, out.getvalue().strip())
