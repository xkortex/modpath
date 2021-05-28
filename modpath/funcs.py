import os
import re
from typing import Union, Tuple, Optional
from pathlib import Path, PosixPath

# from os.path import expanduser, expandvars, join, normpath, split

from modpath.dtypes import OmniPath, ModpathOptions, Route
from modpath.errors import PathOpError

PAT_SCHEME = re.compile(r"\w+://")  # type: re.Pattern

# todo: datastructure and startswith/endswith for routes

# todo: maybe provide remaps as composable functions e.g. no assumptions about pre-stripping
def remap(op: OmniPath, opts: ModpathOptions) -> OmniPath:
    if opts.ext is not None:
        op.ext = opts.ext

    return op


def remap_base(
    base: str,
    new_base: Optional[str] = None,
    old_base: Optional[str] = None,
    prefix: Optional[str] = None,
    suffix: Optional[str] = None,
    old_prefix: Optional[str] = None,
    old_suffix: Optional[str] = None,
) -> str:
    """
    Remap the parts of a basename/filename (ignoring extension)

    This should be used after dirname and all extensions are stripped.
    todo: check that things work with both suffix and non-multidot
    :param base: The base/stem of a filename, sans dirname and any extension.
    :param new_base:
    :param old_base:
    :param prefix:
    :param suffix:
    :param old_prefix:
    :param old_suffix:
    :return:
    """
    if new_base is not None:
        if old_base is not None:
            if old_base not in base:
                raise PathOpError("could not match 'old_base' to basename '{}'".format(old_base, base))
            base = base.replace(old_base, new_base)
        else:
            base = new_base

    if old_prefix is not None:
        if not base.startswith(old_prefix):
            raise PathOpError("basename '{}' does not start with prefix '{}'".format(base, old_prefix))
        new_prefix = prefix or ""
        base = base.replace(old_prefix, new_prefix)
    else:
        new_prefix = prefix or ""
        base = new_prefix + base

    if old_suffix is not None:
        if not base.endswith(old_suffix):
            raise PathOpError("basename '{}' does not end with suffix '{}'".format(base, old_suffix))
        new_suffix = suffix or ""
        base = base.replace(old_suffix, new_suffix)
    else:
        base += suffix or ""
    return base


def remap_posix_pathstr(pathstr: str, dirname: Optional[str] = None, old_dirname: Optional[str] = None) -> str:
    """

    :param path:
    :param dirname:
    :param old_dirname:
    :return:
    """

    if old_dirname is not None:
        if not pathstr.startswith(old_dirname):
            raise PathOpError("path '{}' does not start with dirname '{}'".format(pathstr, old_dirname))
        new_dirname = dirname or ""
        pathstr = pathstr.replace(old_dirname, new_dirname)
    else:
        if dirname is not None:
            basename = os.path.basename(pathstr)
            pathstr = os.path.join(dirname, basename)

    return pathstr


def segment_uri(opts: ModpathOptions) -> OmniPath:
    from urllib.parse import urlsplit, urlunsplit

    sr = urlsplit(str(opts.path))
    raise NotImplementedError()
    return OmniPath()


def splitext(path: str, multidot=False, old_ext=None) -> Tuple[str, str]:
    if old_ext is not None:
        if not path.endswith(old_ext):
            raise PathOpError("basename '{}' does not end with '{}'".format(path, old_ext))
        base = path.replace(old_ext, "")
        ext = old_ext
    elif multidot:
        base, *extp = path.split(".")
        ext = ".".join(extp)
    else:
        base, *extp = os.path.splitext(path)
        ext = ".".join(extp)
    return base, ext


def segment_path(opts: ModpathOptions) -> OmniPath:
    path = opts.path
    if opts.real:
        path = os.path.realpath(path)
    if opts.abs:
        path = os.path.abspath(path)

    # todo: remove redundant splitting and joining
    path = remap_posix_pathstr(str(path), opts.dirname, opts.old_dirname)

    # parts = Route.frum.string(path) # todo: wip, breaks leading / conventions
    parts = Path(path).parts
    base = parts[-1]
    route = parts[:-1]

    base, ext = splitext(base, multidot=opts.multidot, old_ext=opts.old_ext)

    # todo: add old_base
    base = remap_base(
        base,
        new_base=opts.base,
        old_base=None,
        prefix=opts.prefix,
        suffix=opts.suffix,
        old_prefix=opts.old_prefix,
        old_suffix=opts.old_suffix,
    )

    op = OmniPath(route=route, base=base, ext=ext, scheme=None)
    return remap(op, opts)


def segment(opts: ModpathOptions) -> OmniPath:
    """Segment a (file)path or URI"""
    path = opts.path
    if re.search(PAT_SCHEME, path):
        return segment_uri(opts)
    return segment_path(opts)


def recombine(op: OmniPath) -> Union[os.PathLike, str]:
    base = (op.base or "") + (op.ext or "")
    return os.path.join(*op.route, base)


def modpath_opt(opts: ModpathOptions) -> Union[os.PathLike, str]:
    segs = segment(opts)
    return recombine(segs)


def modpath(
    path: Union[os.PathLike, str],
    base: Optional[str] = None,
    dirname: Optional[str] = None,
    ext: Optional[str] = None,
    prefix: Optional[str] = None,
    suffix: Optional[str] = None,
    old_ext: Optional[str] = None,
    old_dirname: Optional[str] = None,
    old_prefix: Optional[str] = None,
    old_suffix: Optional[str] = None,
    rel: Optional[str] = None,
    multidot: bool = False,
    glob: bool = False,
    abs: bool = False,
    real: bool = False,
    expand: bool = False,
    collapse: bool = False,
) -> Union[os.PathLike, str]:
    """
    Modify a path by modifying its individual components.
    A typical path looks like this:
    A path looks like this:

         file://localhost/home/me/myfile.txt
        //        ||         ||       \\      \\
    file        localhost /home/me/  myfile   .txt
    [SCHEME://][HOSTNAME][DIRNAME]/[BASENAME][.EXT]

    Prefix/Suffix are applied to basename.

    # todo: dotted paths are problematic. Route class should handle this once that comes online. 

    :param path: Path to be manipulated
    :param base: Replace the basename
    :param dirname: Replace the dirname
    :param ext: Replace the extension
    :param prefix: Add a prefix to the start of the basename
    :param suffix: Add a suffix to the end of the basename
    :param old_ext: If provided, treat this string as the extension, rather than the last dotted component
    :param old_dirname: If provided, treat this string as dirname, rather than the leading directory
    :param old_prefix: If provided, treat this string as the prefix to replace in the basename
    :param old_suffix: If provided, treat this string as the suffix to replace in the basename
    :param rel: If provided, compute the relpath (relative path) to the target path
    :param multidot: Treat all dotted components in the basename as extension
    :param glob: Use glob notation. In old_FOO, capture a wildcard pattern.
    :param abs: Resolve the absolute path. Resolve location, but do not follow symbolic links
    :param real: Resolve the real path, resolving any symbolic links, then returning the absolute path
        (see also: https://stackoverflow.com/a/40311142/)
    :param expand: Expand ~
    :param collapse: Collapse $HOME to ~
    :return: Modified path

    Examples:
    >>> modpath("foo/bar/spam.tar.gz", ext='')
    foo/bar/spam.tar
    >>> modpath("./foo/bar/spam.tar.gz", ext='', multidot=True)
    foo/bar/spam
    >>> modpath("/home/mike.m/bar/spam.tar.gz", ext='.jpg', prefix='pr_', suffix='_suf',  multidot=True)
    /home/mike.m/bar/pr_spam_suf.jpg
    >>> modpath("~/foo/bar/pr_spam_suf", ext='.tar.gz', old_prefix='pr_', old_suffix='_suf')
    ~/foo/bar/spam.tar.gz

    Examples:
    >>> modpath("foo/bar/spam.tar", dirname='/spam/eggs')
    /spam/eggs/spam.tar
    """
    opts = ModpathOptions(**locals())
    return modpath_opt(opts)
