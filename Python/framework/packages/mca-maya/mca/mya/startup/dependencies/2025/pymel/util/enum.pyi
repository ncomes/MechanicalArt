from typing import *
from . import utilitytypes as utilitytypes
from _typeshed import Incomplete
from past.builtins import cmp as cmp
from typing import Any

__author_name__: str
__author_email__: str
__date__: str
__url__: str

class EnumException(Exception):
    def __init__(self) -> None: ...

class EnumEmptyError(AssertionError, EnumException): ...

class EnumBadKeyError(TypeError, EnumException):
    key: Incomplete
    def __init__(self, key) -> None: ...

class EnumImmutableError(TypeError, EnumException):
    args: Incomplete
    def __init__(self, *args) -> None: ...

class EnumBadDefaultKeyError(ValueError, EnumException):
    val: Incomplete
    key: Incomplete
    def __init__(self, val, key) -> None: ...

class EnumValue:
    def __init__(self, enumtype, index, key, doc: Incomplete | None = ...) -> None: ...
    enumtype: Incomplete
    key: Incomplete
    def __int__(self) -> int: ...
    index: Incomplete
    def __hash__(self) -> int: ...
    def __eq__(self, other): ...
    def __ne__(self, other): ...
    def __gt__(self, other): ...
    def __lt__(self, other): ...
    def __ge__(self, other): ...
    def __le__(self, other): ...

class Enum:
    def __init__(self, name: str, keys: Union[Dict[str, int], Iterable[str], Iterable[Tuple[str, int]]], **kwargs: Any) -> None: ...
    @property
    def name(self) -> str: ...
    def __eq__(self, other): ...
    def __hash__(self) -> int: ...
    def __ne__(self, other): ...
    def __setattr__(self, name, value) -> None: ...
    def __delattr__(self, name) -> None: ...
    def __len__(self) -> int: ...
    def __getitem__(self, index: str) -> int: ...
    def __setitem__(self, index, value) -> None: ...
    def __delitem__(self, index) -> None: ...
    def __iter__(self) -> Iterable[int]: ...
    def __contains__(self, value: Union[str, int]) -> bool: ...
    def getIndex(self, key: str) -> int: ...
    def getKey(self, index: int) -> str: ...
    def values(self) -> Tuple[int, ...]: ...
    def itervalues(self) -> Iterator[int]: ...
    def keys(self) -> Tuple[str, ...]: ...
EnumType = Enum

class EnumDict(utilitytypes.EquivalencePairs):
    def __init__(self, keys, **kwargs) -> None: ...
    def value(self, key: Union[str, int]) -> int: ...
    def key(self, index: int) -> str: ...
    def values(self) -> List[int]: ...
    def keys(self) -> List[str]: ...
