from typing import *
import types
from _typeshed import Incomplete
from typing import Any, TypeVar

CallableT = TypeVar('CallableT', bound=Callable)

def decorated(origFunc, newFunc, decoration: Incomplete | None = ...) -> None: ...
def decorator(func): ...
def format_signature(args: Tuple[Any, ...] = ..., varargs: Optional[str] = ..., varkw: Optional[str] = ..., defaults: Optional[Sequence[Any]] = ...) -> str: ...
def interface_wrapper(doer: types.FunctionType, args: Tuple[Any, ...] = ..., varargs: Optional[str] = ..., varkw: Optional[str] = ..., defaults: Optional[Sequence[Any]] = ...) -> Callable: ...