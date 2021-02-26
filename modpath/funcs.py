import os
import re
from typing import Union, Tuple
from pathlib import Path

# from os.path import expanduser, expandvars, join, normpath, split

from modpath.dtypes import OmniPath, ModpathOptions
from modpath.errors import PathOpError

PAT_SCHEME = re.compile(r"\w+\:\/\/")


def remap(op: OmniPath, opts: ModpathOptions) -> OmniPath:
    if opts.ext:
        op.ext = opts.ext

    return op


def segment_uri(opts: ModpathOptions) -> OmniPath:
    ...
    raise NotImplementedError("not ready yet")


def splitext(path: str, multidot=False, old_ext=None) -> Tuple[str, str]:
    if old_ext:
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
    # why is ext handling here but the rest in remap?

    # todo: parsing prefix/suffix here
    if opts.old_dirname:
        raise NotImplementedError("not ready yet")

    if opts.prefix:
        raise NotImplementedError("not ready yet")

    if opts.suffix:
        raise NotImplementedError("not ready yet")

    base, ext = splitext(parts[-1], multidot=opts.multidot, old_ext=opts.old_ext)

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
