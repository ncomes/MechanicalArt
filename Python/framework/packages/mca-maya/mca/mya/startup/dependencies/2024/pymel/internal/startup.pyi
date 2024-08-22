from . import plogging as plogging
from _typeshed import Incomplete
from pymel.mayautils import getUserPrefsDir as getUserPrefsDir
from pymel.util import subpackages as subpackages

isInitializing: bool
finalizeEnabled: bool

def mayaStartupHasRun(): ...
def mayaStartupHasStarted(): ...
def setupFormatting(): ...
def mayaInit(forversion: Incomplete | None = ...): ...
def initMEL() -> None: ...
def initAE(): ...
def finalize() -> None: ...
def fixMayapySegFault() -> None: ...
def fixMayapy2011SegFault() -> None: ...
def encodeFix() -> None: ...
def getConfigFile(): ...
def parsePymelConfig(): ...

pymel_options: Incomplete
