import os
import re
from typing import Union, Tuple
from pathlib import Path

# from os.path import expanduser, expandvars, join, normpath, split

from modpath.dtypes import OmniPath, ModpathOptions
from modpath.errors import PathOpError

PAT_SCHEME = re.compile(r"\w+\:\/\/")


def remap(op: OmniPath, opts: ModpathOptions) -> OmniPath:
    if opts.ext is not None:
        op.ext = opts.ext

    return op


def segment_uri(opts: ModpathOptions) -> OmniPath:
    ...
    raise NotImplementedError("not ready yet")


def splitext(path: str, multidot=False, old_ext=None) -> Tuple[str, str]:
    if old_ext is not None:
        if not path.endswith(old_ext):
            raise PathOpError("basename '{}' does not end with '{}'".format(path, old_ext))
        base = path.replace(old_ext, "")
        ext = old_ext
    elif multidot:
        base, *extp = path.split('.')
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
    parts = Path(path).parts
    base = parts[-1]

    base, ext = splitext(base, multidot=opts.multidot, old_ext=opts.old_ext)

    # todo: parsing prefix/suffix here
    if opts.old_dirname is not None:
        raise NotImplementedError("not ready yet")

    if opts.old_prefix is not None:
        if not base.startswith(opts.old_prefix):
            raise PathOpError("basename '{}' does not start with prefix '{}'".format(base, opts.old_prefix))
        new_prefix = opts.prefix or ''
        base = base.replace(opts.old_prefix, new_prefix)
    else:
        new_prefix = opts.prefix or ''
        base = new_prefix + base

    if opts.old_suffix is not None:
        if not base.endswith(opts.old_suffix):
            raise PathOpError("basename '{}' does not end with suffix '{}'".format(base, opts.old_suffix))
        new_suffix = opts.suffix or ''
        base = base.replace(opts.old_suffix, new_suffix)
    else:
        base += opts.suffix or ''



    op = OmniPath(route=parts[:-1], base=base, ext=ext, scheme=None)
    return remap(op, opts)


def segment(opts: ModpathOptions) -> OmniPath:
    """Segment a (file)path or URI"""
    path = opts.path
    if re.search(PAT_SCHEME, path):
        return segment_uri(opts)
    return segment_path(opts)


def recombine(op: OmniPath):
    base = op.base + op.ext
    return os.path.join(*op.route, base)
