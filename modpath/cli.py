from typing import List, Optional
from modpath.dtypes import ModpathOptions
from modpath.funcs import segment, recombine
from modpath.errors import ArgumentError, PathOpError


def check_args(args):
    if args.old_ext and args.multidot:
        raise ArgumentError("Cannot use --old-ext with --multidot option")


def modpath_argparse():
    import argparse

    pr = argparse.ArgumentParser(
        description="""Modify paths. A tool to manipulate paths, extensions, directories, 
    and structured filenames. A path looks like this: 
    [SCHEME://][HOST][DIRNAME]/[BASENAME][.EXT]"""
    )
    pr.add_argument("path", nargs="+", help="The path(s) to be modified")
    pr.add_argument("-s", "--suffix", default=None, help="placed between the basename and extension")
    pr.add_argument("-S", "--old-suffix", default=None, help="if specified, use this as the suffix")
    pr.add_argument("-p", "--prefix", default=None, help="placed in front of the basename")
    pr.add_argument("-P", "--old-prefix", default=None, help="if specified, use this as the prefix")
    pr.add_argument("-e", "--ext", default=None, help="if specified, replaces the extension")
    pr.add_argument("-E", "--old-ext", default=None, help="if specified, treat this as the extension")
    pr.add_argument(
        "-b",
        "--base",
        default=None,
        help="if specified, replaces the basename without extension",
    )
    pr.add_argument("-d", "--dirname", default=None, help="if specified, replaces the dirname")
    pr.add_argument("-D", "--old-dirname", default=None, help="if specified, treat this as the dirname")
    pr.add_argument("-r", "--rel", default=None, help="determine relpath to")
    pr.add_argument(
        "-m",
        "--multidot",
        action="store_true",
        help="Treat all dotted components in base as the extension",
    )
    pr.add_argument("-g", "--glob", action="store_true", help="Allows globbing in [PATH]")
    pr.add_argument("-a", "--abs", action="store_true", help="Get absolute path")
    pr.add_argument("-R", "--real", "--realpath", action="store_true", help="Get realpath")
    return pr


def args_to_opts(args) -> List[ModpathOptions]:
    argdict = vars(args).copy()  # otherwise this mutates args
    paths = argdict.pop("path")
    out = []
    for p in paths:
        argdict["path"] = p
        out.append(ModpathOptions(**argdict))
    return out


def modpath_cli():
    parser = modpath_argparse()
    args = parser.parse_args()
    check_args(args)
    opts = args_to_opts(args)
    # print(opts)
    for opt in opts:
        try:
            print(recombine(segment(opt)))
        except PathOpError as exc:
            print("{}: {}".format(exc.__class__.__name__, exc))
            exit(1)
