import os
import pathlib

from pyfakefs.fake_filesystem_unittest import TestCase

from pyvcs import repo


class RepoCreateTestCase(TestCase):
    def setUp(self):
        os.environ["GIT_DIR"] = ".git"
        self.setUpPyfakefs()

    def test_created_repo_has_the_correct_structure(self):
        workdir = pathlib.Path(".")
        gitdir = repo.repo_create(workdir)

        expected_gitdir = workdir / ".git"
        self.assertEqual(expected_gitdir, gitdir)
        self.assertTrue(gitdir.exists())
        self.assertTrue((gitdir / "refs" / "heads").exists())
        self.assertTrue((gitdir / "refs" / "tags").exists())
        self.assertTrue((gitdir / "objects").exists())

        head = gitdir / "HEAD"
        self.assertTrue(head.exists())
        with head.open() as f:
            self.assertEqual("ref: refs/heads/master\n", f.read())

        config = gitdir / "config"
        self.assertTrue(config.exists())
        with config.open() as f:
            self.assertEqual(
                "[core]\n\trepositoryformatversion = 0\n\tfilemode = true\n\tbare = false\n\tlogallrefupdates = false\n",
                f.read(),
            )

        description = gitdir / "description"
        self.assertTrue(description.exists())
        with description.open() as f:
            self.assertEqual(
                "Unnamed pyvcs repository.\n", f.read(),
            )

    def test_cant_create_repo_if_workdir_is_a_file(self):
        filename = "test"
        workdir = pathlib.Path(filename)
        self.fs.create_file(workdir, contents="test")
        with self.assertRaises(Exception) as ctx:
            repo.repo_create(workdir)
        self.assertEqual(f"{filename} is not a directory", str(ctx.exception))

    def test_git_dir(self):
        dir_name = ".pyvcs"
        os.environ["GIT_DIR"] = dir_name
        workdir = pathlib.Path(".")
        actual_gitdir = repo.repo_create(workdir)
        expected_gitdir = workdir / dir_name
        self.assertEqual(expected_gitdir, actual_gitdir)
        self.assertTrue(expected_gitdir.exists())


class RepoFindTestCase(TestCase):
    def setUp(self):
        os.environ["GIT_DIR"] = ".git"
        self.setUpPyfakefs()

    def test_repo_find(self):
        workdir = pathlib.Path(".")
        workdir = workdir.absolute()
        expected_gitdir = workdir / ".git"
        self.fs.create_dir(expected_gitdir)
        gitdir = repo.repo_find(workdir)
        self.assertEqual(expected_gitdir, gitdir)

    def test_repo_find_in_a_given_dir(self):
        expected_gitdir = pathlib.Path("dir1") / ".git"
        expected_gitdir = expected_gitdir.absolute()
        current_dir = expected_gitdir / "dir2"
        self.fs.create_dir(current_dir)
        gitdir = repo.repo_find(current_dir)
        self.assertEqual(expected_gitdir, gitdir)

    def test_repo_not_found(self):
        with self.assertRaises(Exception) as ctx:
            _ = repo.repo_find()
        self.assertEqual("Not a git repository", str(ctx.exception))
