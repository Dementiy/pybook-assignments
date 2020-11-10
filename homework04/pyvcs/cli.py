import argparse

from pyvcs.index import ls_files, read_index, update_index
from pyvcs.objects import cat_file, hash_object
from pyvcs.porcelain import checkout, commit
from pyvcs.refs import ref_resolve, symbolic_ref, update_ref
from pyvcs.repo import repo_create, repo_find
from pyvcs.tree import commit_tree, write_tree


def cmd_init(args: argparse.Namespace) -> None:
    # TODO: Reinitialized existing pyvcs repository
    gitdir = repo_create(args.path)
    print(f"Initialized empty pyvcs repository in {gitdir.absolute()}")


def cmd_hash_object(args: argparse.Namespace) -> None:
    with args.path.open(mode="rb") as f:
        data = f.read()

    sha = hash_object(data, args.type, args.write)
    print(sha)


def cmd_cat_file(args: argparse.Namespace) -> None:
    cat_file(args.object, args.pretty)


def cmd_ls_files(args: argparse.Namespace) -> None:
    gitdir = repo_find()
    ls_files(gitdir, details=args.stage)


def cmd_update_index(args: argparse.Namespace) -> None:
    gitdir = repo_find()
    update_index(gitdir, args.paths, write=args.add)


def cmd_write_tree(args: argparse.Namespace) -> None:
    gitdir = repo_find()
    entries = read_index(gitdir)
    sha = write_tree(gitdir, entries)
    print(sha)


def cmd_commit_tree(args: argparse.Namespace) -> None:
    gitdir = repo_find()
    sha = commit_tree(gitdir, args.tree, args.message, args.parent)
    print(sha)


def cmd_update_ref(args: argparse.Namespace) -> None:
    gitdir = repo_find()
    update_ref(gitdir, args.ref, args.newvalue)


def cmd_rev_parse(args: argparse.Namespace) -> None:
    gitdir = repo_find()
    sha = ref_resolve(gitdir, args.rev)
    print(sha)


def cmd_symbolic_ref(args: argparse.Namespace) -> None:
    gitdir = repo_find()
    symbolic_ref(gitdir, args.name, args.ref)


def cmd_commit(args: argparse.Namespace) -> None:
    gitdir = repo_find()
    sha = commit(gitdir, args.message, args.author)
    print(sha)


def cmd_checkout(args: argparse.Namespace) -> None:
    gitdir = repo_find()
    checkout(gitdir, args.obj_name)
