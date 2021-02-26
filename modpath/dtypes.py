from typing import List, Tuple, Union, Optional
from dataclasses import dataclass


@dataclass
class ModpathOptions:
    path: str
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


@dataclass
class OmniPath:
    route: Tuple[str]
    base: str
    ext: Optional[str] = None
    scheme: Optional[str] = None
