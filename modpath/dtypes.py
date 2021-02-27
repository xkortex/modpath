import os
import abc
import _collections_abc as cabc  # type: ignore
from typing import List, Tuple, Union, Optional, TypeVar
from dataclasses import dataclass

K = TypeVar("K")
ST = TypeVar("ST", str, bytes)


class NonStringIterable(cabc.Iterable, metaclass=abc.ABCMeta):
    """Any iterable which isn't string/bytes"""

    __slots__ = ()

    @abc.abstractmethod
    def __iter__(self):
        """
            Examples:
        >>> from pathlib import PosixPath
        >>> ok_types = [iter('abc'), list(['a', 'b']), dict(a='b'), tuple(('a','b')), {'a', 'b'}, ]
        >>> bad_types = ['string', b'bytes', PosixPath('foo/bar'), 5, 3.14, object()]
        >>> all([isinstance(t, NonStringIterable) for t in ok_types])
        True
        >>> any([isinstance(t, NonStringIterable) for t in bad_types])
        False
        """
        while False:
            yield None

    @classmethod
    def __subclasshook__(cls, c):

        if cls is NonStringIterable:
            if issubclass(c, (str, bytes)):
                return False
            return cabc._check_methods(c, "__iter__")
        return NotImplemented


@dataclass
class ModpathOptions:
    path: Union[os.PathLike, str]
    base: Optional[str] = None
    dirname: Optional[str] = None
    ext: Optional[str] = None
    prefix: Optional[str] = None
    suffix: Optional[str] = None
    old_ext: Optional[str] = None
    old_dirname: Optional[str] = None
    old_prefix: Optional[str] = None
    old_suffix: Optional[str] = None
    rel: Optional[str] = None
    multidot: bool = False
    glob: bool = False
    abs: bool = False
    real: bool = False
    expand: bool = False
    collapse: bool = False


@dataclass
class OmniPath:
    # todo: modpath/funcs.py:126: error: Argument "route" to "OmniPath" has incompatible type "Tuple[str, ...]"; expected "NonStringIterable"  [arg-type]
    route: Union[NonStringIterable, Tuple]
    base: str
    ext: Optional[str] = None
    scheme: Optional[str] = None
    netloc: Optional[str] = None


class Route(NonStringIterable):
    """A representation of a path, without path separators"""

    def __init__(self, it: Union[NonStringIterable, List[str], str], *args):
        """
        Accepts "it" as a str in order to get end-to-end __repr__() to work.
        May disable this in the future, or munge the type checks.
        :param it:
        :param args:
        """
        if isinstance(it, NonStringIterable):
            frst = list(it)
        else:
            frst = [it]

        self._it = frst + list(args)

    def __iter__(self):
        yield from self._it

    def __str__(self) -> str:
        return self.join()

    def __repr__(self) -> str:
        parts = ["'" + str(el) + "'" for el in self._it]
        return "Route({})".format(", ".join(parts))

    def __fspath__(self):
        return self.join()

    def __getitem__(self, item):
        return self._it.__getitem__(item)

    class frum:
        @staticmethod
        def string(s: str, sep=os.path.sep) -> 'Route':
            return Route(s.split(sep))

    def join(self, sep=os.path.sep):
        return sep.join(self._it)
