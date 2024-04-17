import maya.cmds as cmds
from functools import partial
import mca.mya.cinematics.CinematicsArchive.CineClasses as cc
import mca.mya.cinematics.CinematicsArchive.CineSequenceNodes as csn

def playblast(resoH, resoW):
    seqNodes = cmds.ls('*Sequence_Node')
    if seqNodes:
        mayaSeqNode = seqNodes[0]
        cineSeqNode = csn.CineSequenceNode.getCineSeqNode(mayaSeqNode)
        if cineSeqNode.isShot:
            shots = []
            selectedShots = [x for x in cmds.ls(sl=True) if cmds.nodeType(x)=='shot']

            if selectedShots: #if you have selected shots, playblast those
                for sht in selectedShots:
                    shots.append(cc.CineShot.getCineShotFromMayaShot(sht, cineSeqNode))
            elif cmds.ls(type='shot'): #if you haven't selected shots, but there are shots in the sequencer
                for sht in cmds.ls(type='shot'):
                    shots.append(cc.CineShot.getCineShotFromMayaShot(sht, cineSeqNode))
            else:
                shots.append(cc.CineShot.getCineShotFromSeqNode(cineSeqNode))
            for cineShot in shots:
                if cineShot.cam:
                    #print(cineShot.name)
                    playblastShotOrScene(cineShot, cineSeqNode, resoH, resoW)
                else:
                    print('Found no camera to playblast from')
        else:
            sel = cmds.ls(sl=True)
            if sel:
                if cc.CineStaticClass.isShotCam(sel[0]):
                    cam = sel[0]
                    #print('playblasting from this camera: {}'.format(cam))
                    cineScene = cc.CineScene.getCineSceneFromSeqNode(cineSeqNode)
                    cineScene.cam = cam
                    playblastShotOrScene(cineScene, cineSeqNode, resoH, resoW)
                else:
                    print('Select a shot camera to playblast from')
            else:
                print('Select a shot camera to playblast from')

    else:
        print('No Sequence Node in scene')

def playblastShotOrScene(cineClass, cineSeqNode, resoH, resoW):
    shotDirDict = cc.CineStaticClass.getShotDirDict()
    if cineSeqNode.isShot and cineSeqNode.shotNumber==0:
        #if this is a sequence shot file
        blastDir = shotDirDict['previsPlayblast']
        playblastName = '{}_{}_sequence'.format(cineClass.name, cineSeqNode.stageString)
    else:
        blastDir = shotDirDict['playblast']
        playblastName = '{}_{}'.format(cineClass.name, cineSeqNode.stageString)
    a = cmds.ls(type='audio')
    audio = None
    if a:
        audio = a[0]
    p = cmds.sequenceManager(q=1, mp=1)
    cmds.select(cl=True)
    cmds.lookThru(p, cineClass.cam.mayaCam)
    cmds.modelEditor(p, e=1, alo=0)
    cmds.modelEditor(p, e=1, po=('gpuCacheDisplayFilter', 1))
    cmds.modelEditor(p, e=1, pm=1, udm=0, dtx=True, da='smoothShaded')
    cmds.camera(cineClass.cam.mayaCam, e=1, ovr=1, dfg=0, dgm=0)
    try:
        setHud(cineSeqNode)
    except:
        print("hud blocked by other huds")    
    cmds.playblast(
            f="{}\\{}".format(blastDir, playblastName), 
            s=audio, epn=p, fo=1, fmt='qt', c="H.264", st=cineClass.start, 
            et=cineClass.end, v=0, p=100, wh=[resoW, resoH])
    cmds.camera(cineClass.cam.mayaCam, e=1, ovr=1.15, dfg=1, dgm=1)

def getVersionNumber(cineSeqNode):
        return str(cineSeqNode.version)

def setHud(cineSeqNode):
    visibleHuds = [h for h in cmds.headsUpDisplay(listHeadsUpDisplays=True) 
                    if cmds.headsUpDisplay(h, q=True, visible=True)]
    for hud in visibleHuds:
        cmds.headsUpDisplay(hud, edit=True, visible=False)
    playblastHuds = []
    #put focal length in section 5
    playblastHuds.append(cmds.headsUpDisplay( 'HUDFocalLength', 
        edit=True, visible=True, lfs='large', dfs='large', section=5, block=1))
    #put camera name in section 7
    playblastHuds.append(cmds.headsUpDisplay( 'HUDCameraNames', 
        edit=True, visible=True, lfs='large', dfs='large'))
    #put frame count in section 9
    playblastHuds.append(cmds.headsUpDisplay( 'HUDCurrentFrame', 
        edit=True, visible=True, lfs='large', dfs='large'))
    #put version number in section 4
    nextBlock = cmds.headsUpDisplay(nfb=4)
    hudCommand = partial(getVersionNumber, cineSeqNode)
    playblastHuds.append(cmds.headsUpDisplay('HUDversionNumber', 
        label='Version Number: ', command=hudCommand, 
        visible=True, lfs='large', dfs='large', section=4, block=nextBlock))
    
