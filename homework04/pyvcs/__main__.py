import argparse
import pathlib

from pyvcs.cli import (
    cmd_cat_file,
    cmd_checkout,
    cmd_commit_tree,
    cmd_hash_object,
    cmd_init,
    cmd_ls_files,
    cmd_rev_parse,
    cmd_symbolic_ref,
    cmd_update_index,
    cmd_update_ref,
    cmd_write_tree,
)


def add_init_subparser(subparsers) -> None:
    init_subparser = subparsers.add_parser("init", help="Create a new repository.")
    init_subparser.add_argument(
        "path",
        metavar="directory",
        type=pathlib.Path,
        nargs="?",
        default=".",
        help="Where to create the repository.",
    )
    init_subparser.set_defaults(func=cmd_init)


def add_hash_object_subparser(subparsers) -> None:
    hash_object_subparser = subparsers.add_parser(
        "hash-object",
        help="Compute object ID and optionally creates a blob from a file.",
    )
    hash_object_subparser.add_argument(
        "-t",
        metavar="<type>",
        dest="type",
        choices=["blob", "commit", "tag", "tree"],
        default="blob",
        help="Specify the type (default: 'blob')",
    )
    hash_object_subparser.add_argument(
        "-w",
        dest="write",
        action="store_true",
        help="Actually write the object into the database",
    )
    hash_object_subparser.add_argument("path", type=pathlib.Path, help="Read object from <file>")
    hash_object_subparser.set_defaults(func=cmd_hash_object)


def add_cat_file_subparser(subparsers) -> None:
    cat_file_subparser = subparsers.add_parser(
        "cat-file", help="Provide content of repository objects."
    )

    group = cat_file_subparser.add_mutually_exclusive_group(required=True)
    # NOTE: Mutually exclusive arguments must be optional
    # group.add_argument(
    #     "type",
    #     metavar="<type>",
    #     choices=["blob", "commit", "tag", "tree"],
    #     default="blob",
    #     nargs="?",
    #     help="Specify the type",
    # )
    group.add_argument(
        "-p",
        dest="pretty",
        action="store_true",
        help="Pretty-print the contents of <object> based on its type",
    )
    cat_file_subparser.add_argument(
        "object", metavar="object", help="The name of the object to show"
    )
    cat_file_subparser.set_defaults(func=cmd_cat_file)


def add_ls_files_subparser(subparsers) -> None:
    ls_files_subparser = subparsers.add_parser(
        "ls-files", help="Show information about files in the index."
    )
    ls_files_subparser.add_argument(
        "-s",
        dest="stage",
        action="store_true",
        help="Show staged contents' mode bits, object name and stage number in the output",
    )
    ls_files_subparser.set_defaults(func=cmd_ls_files)


def add_update_index_subparser(subparsers) -> None:
    update_index_subparser = subparsers.add_parser(
        "update-index", help="Add file contents to the index."
    )
    update_index_subparser.add_argument(
        "paths", nargs="+", metavar="path", type=pathlib.Path, help="path(s) of files to add"
    )
    update_index_subparser.add_argument(
        "--add",
        dest="add",
        action="store_true",
        help="If a specified file isn't in the index already then it's added.",
    )
    update_index_subparser.set_defaults(func=cmd_update_index)


def add_write_tree_subparser(subparsers) -> None:
    write_tree_subparser = subparsers.add_parser(
        "write-tree", help="Create a tree object from the current index."
    )
    write_tree_subparser.set_defaults(func=cmd_write_tree)


def add_commit_tree_subparser(subparsers) -> None:
    # FIXME: Add author
    commit_tree_subparser = subparsers.add_parser("commit-tree", help="Create a new commit object.")
    commit_tree_subparser.add_argument("tree", help="An existing tree object")
    commit_tree_subparser.add_argument("-p", dest="parent", help="Id of a parent commit object")
    commit_tree_subparser.add_argument(
        "-m", dest="message", help="A paragraph in the commit log message"
    )
    commit_tree_subparser.set_defaults(func=cmd_commit_tree)


def add_update_ref_subparser(subparsers) -> None:
    # FIXME: Добавить описание для аргументов
    update_ref_subparser = subparsers.add_parser(
        "update-ref", help="Update the object name stored in a ref safely."
    )
    update_ref_subparser.add_argument("ref", help="")
    update_ref_subparser.add_argument("newvalue", help="")
    update_ref_subparser.set_defaults(func=cmd_update_ref)


def add_rev_parse_subparser(subparsers) -> None:
    # FIXME: Добавить описание для аргументов
    rev_parse_subparser = subparsers.add_parser("rev-parse", help="")
    rev_parse_subparser.add_argument("rev", help="")
    rev_parse_subparser.set_defaults(func=cmd_rev_parse)


def add_symbolic_ref_subparser(subparsers) -> None:
    # FIXME: Добавить описание для аргументов
    symbolic_ref_subparser = subparsers.add_parser("symbolic-ref", help="Modify symbolic refs.")
    symbolic_ref_subparser.add_argument("name", help="")
    symbolic_ref_subparser.add_argument("ref", help="")
    symbolic_ref_subparser.set_defaults(func=cmd_symbolic_ref)


def add_checkout_subparser(subparsers) -> None:
    # FIXME: Добавить описание для аргументов
    checkout_subparser = subparsers.add_parser("checkout", help="")
    checkout_subparser.add_argument("obj_name", help="")
    checkout_subparser.set_defaults(func=cmd_checkout)


def parse_args() -> argparse.Namespace:
    argparser = argparse.ArgumentParser(description="The stupid content tracker")
    subparsers = argparser.add_subparsers(title="Commands", dest="command")
    subparsers.required = True
    add_init_subparser(subparsers)
    add_hash_object_subparser(subparsers)
    add_cat_file_subparser(subparsers)
    add_ls_files_subparser(subparsers)
    add_update_index_subparser(subparsers)
    add_write_tree_subparser(subparsers)
    add_commit_tree_subparser(subparsers)
    add_update_ref_subparser(subparsers)
    add_rev_parse_subparser(subparsers)
    add_symbolic_ref_subparser(subparsers)
    add_checkout_subparser(subparsers)
    return argparser.parse_args()


def main() -> None:
    args = parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
