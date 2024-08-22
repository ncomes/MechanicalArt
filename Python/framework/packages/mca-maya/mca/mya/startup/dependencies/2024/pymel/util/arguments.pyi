from typing import *
from .utilitytypes import ProxyUnicode as ProxyUnicode
from _typeshed import Incomplete
from collections.abc import Generator
from typing import Any, TypeVar

T = TypeVar('T')

def isIterable(obj: Any) -> bool: ...
def isScalar(obj: Any) -> bool: ...
def isNumeric(obj: Any) -> bool: ...
def isSequence(obj: Any) -> bool: ...
def isMapping(obj: Any) -> bool: ...

clsname: Incomplete

def convertListArgs(args): ...
def expandArgs(*args, **kwargs): ...
def preorderArgs(limit=..., testFn=..., *args): ...
def postorderArgs(limit=..., testFn=..., *args): ...
def breadthArgs(limit=..., testFn=..., *args): ...
def iterateArgs(*args, **kwargs) -> Generator[Incomplete, None, Incomplete]: ...
def preorderIterArgs(limit=..., testFn=..., *args) -> Generator[Incomplete, None, None]: ...
def postorderIterArgs(limit=..., testFn=..., *args) -> Generator[Incomplete, None, None]: ...
def breadthIterArgs(limit=..., testFn=..., *args) -> Generator[Incomplete, None, None]: ...
def preorder(iterable, testFn=..., limit=...) -> Generator[Incomplete, None, None]: ...
def postorder(iterable, testFn=..., limit=...) -> Generator[Incomplete, None, None]: ...
def breadth(iterable, testFn=..., limit=...) -> Generator[Incomplete, None, None]: ...
def listForNone(res: Optional[List[T]]) -> List[T]: ...
def pairIter(sequence: Iterable[Any]) -> Iterator[Tuple[Any, Any]]: ...
def reorder(x, indexList=..., indexDict=...): ...

class RemovedKey:
    oldVal: Incomplete
    def __init__(self, oldVal) -> None: ...
    def __eq__(self, other): ...
    def __ne__(self, other): ...
    def __hash__(self): ...

class AddedKey:
    newVal: Incomplete
    def __init__(self, newVal) -> None: ...
    def __eq__(self, other): ...
    def __ne__(self, other): ...
    def __hash__(self): ...

class ChangedKey:
    oldVal: Incomplete
    newVal: Incomplete
    def __init__(self, oldVal, newVal) -> None: ...
    def __eq__(self, other): ...
    def __ne__(self, other): ...
    def __hash__(self): ...

def compareCascadingDicts(dict1: Union[dict, list, tuple], dict2: Union[dict, list, tuple], encoding: Union[str, bool, None] = ..., useAddedKeys: bool = ..., useChangedKeys: bool = ...) -> Tuple[set, set, set, dict]: ...
def mergeCascadingDicts(from_dict, to_dict, allowDictToListMerging: bool = ..., allowNewListMembers: bool = ...): ...
def setCascadingDictItem(dict, keys, value) -> None: ...
def getCascadingDictItem(dict, keys, default=...): ...
def deepPatch(input, predicate, changer): ...
def deepPatchAltered(input, predicate, changer): ...
def sequenceToSlices(intList, sort: bool = ...): ...
def izip_longest(*args, **kwds) -> Generator[Incomplete, None, None]: ...
def getImportableObject(importableName): ...
def getImportableName(obj): ...
