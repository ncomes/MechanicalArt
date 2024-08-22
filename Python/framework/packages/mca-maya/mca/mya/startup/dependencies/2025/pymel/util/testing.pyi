from unittest import *
from _typeshed import Incomplete
from collections.abc import Generator
from warnings import warn as warn

TEST_MAIN_FUNC_NAME: str
SUITE_FUNC_NAME: str

def doctestFriendly(func): ...
def doctestobj(*args, **kwargs): ...
def doctestmod(*args, **kwargs): ...

class MayaTestRunner(TextTestRunner):
    def __init__(self, stream=..., descriptions: bool = ..., verbosity: int = ...) -> None: ...
    def run(self, *args, **kwargs) -> None: ...

def addFuncToModule(func, module) -> None: ...
def startsWithDoubleUnderscore(testcase): ...
def setupUnittestModule(moduleName, suiteFuncName=..., testMainName=..., filterTestCases=...): ...

class TestCaseExtended(TestCase):
    DO_NOT_LOAD: bool
    def assertNoError(self, function, *args, **kwargs) -> None: ...
    def assertIteration(self, iterable, expectedResults, orderMatters: bool = ..., onlyMembershipMatters: bool = ...) -> None: ...
    def assertVectorsEqual(self, v1, v2, places: int = ...) -> None: ...

def permutations(sequence, length: Incomplete | None = ...) -> Generator[Incomplete, None, None]: ...
def isOneToOne(dict): ...
def isEquivalenceRelation(inputs, outputs, dict): ...

class SuiteFromModule(TestSuite):
    moduleName: Incomplete
    module: Incomplete
    def __init__(self, module, testImport: bool = ...) -> None: ...

class UnittestSuiteFromModule(SuiteFromModule):
    suiteFuncName: Incomplete
    def __init__(self, moduleName, suiteFuncName=..., **kwargs) -> None: ...

class DoctestSuiteFromModule(SuiteFromModule):
    alreadyRecursed: Incomplete
    packageRecurse: Incomplete
    def __init__(self, moduleName, packageRecurse: bool = ..., alreadyRecursed: Incomplete | None = ..., **kwargs) -> None: ...

def setCompare(iter1, iter2): ...
def suite(): ...
