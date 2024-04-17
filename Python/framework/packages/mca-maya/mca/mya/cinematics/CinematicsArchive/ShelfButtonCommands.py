import importlib
import imp


importDict = {
'mca.mya.cinematics.CreateShot' : 'makeNewShot',
'mca.mya.cinematics.RenameShot' : 'renameShot',
'mca.mya.cinematics.DuplicateShot' : 'duplicateShot',
'mca.mya.cinematics.CameraController' : 'addCameraController',
'mca.mya.cinematics.RigObject' : 'rigObject',
'mca.mya.cinematics.RigObjectDouble' : 'rigObjectDouble',
'mca.mya.cinematics.SceneMover' : 'makeSceneMoverButtonClick',
'mca.mya.cinematics.CopyCamera' : 'copyCamera',
'mca.mya.cinematics.GrandParent' : 'parentMultiple',
'mca.mya.cinematics.MatchObjs' : 'matchObjs',
'mca.mya.cinematics.AddLocator' : 'addLocators',
'mca.mya.cinematics.BakeLocator' : 'bakeLocToSelection',
'mca.mya.cinematics.BreakoutSelectedShot' : 'breakOutSelectedShot',
'mca.mya.cinematics.SendLayoutToAnim' : 'layoutToAnim',
'mca.mya.cinematics.PlayblastSingleClick': 'playblastSingle',
'mca.mya.cinematics.PlayblastDoubleClick': 'playblastDouble',
'mca.mya.cinematics.SaveButton' : 'saveButtonPress',
'mca.mya.cinematics.CineSequenceNodes' : 'seqNodeButtonPress',
'mca.mya.cinematics.OpenCineFile' : 'openMayaFile',
'mca.mya.cinematics.ExecuteBatchBreakout' : 'promptBreakoutWindow'
}

def getCommand(key):
	mod = importlib.import_module(key)
	imp.reload(mod)
	c = getattr(mod, importDict[key])

	return c

def _null(*args):
	print("nothing here")
	pass

#
newShot = getCommand('mca.mya.cinematics.CreateShot')
renameShot = getCommand('mca.mya.cinematics.RenameShot')
duplicateShot = getCommand('mca.mya.cinematics.DuplicateShot')
#
camControl = getCommand('mca.mya.cinematics.CameraController')
rigObj = getCommand('mca.mya.cinematics.RigObject')
rigObjDouble = getCommand('mca.mya.cinematics.RigObjectDouble')
sceneMover = getCommand('mca.mya.cinematics.SceneMover')
copyCam = getCommand('mca.mya.cinematics.CopyCamera')
grandP = getCommand('mca.mya.cinematics.GrandParent')
match = getCommand('mca.mya.cinematics.MatchObjs')
loc = getCommand('mca.mya.cinematics.AddLocator')
bakeLoc = getCommand('mca.mya.cinematics.BakeLocator')
#
breakOutShot = getCommand('mca.mya.cinematics.BreakoutSelectedShot')
batchBreakOut = getCommand('mca.mya.cinematics.ExecuteBatchBreakout')
layoutToAnim = getCommand('mca.mya.cinematics.SendLayoutToAnim')
editSeqNode = getCommand('mca.mya.cinematics.CineSequenceNodes')
#
playblastSingle = getCommand('mca.mya.cinematics.PlayblastSingleClick')
playblastDouble = getCommand('mca.mya.cinematics.PlayblastDoubleClick')
#
save = getCommand('mca.mya.cinematics.SaveButton')
openFile = getCommand('mca.mya.cinematics.OpenCineFile')

