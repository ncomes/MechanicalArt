import subprocess
import mca.mya.cinematics.CinematicsArchive.CineClasses as cc
import mca.mya.cinematics.CinematicsArchive.CineSequenceNodes as csn
import maya.cmds as cmds

def promptExportWindow(*args):
    result = cmds.confirmDialog(title='Batch Break Out Shots', 
        message='WARNING:\n\nThis process will lock your Maya until it is finished.'+
                '\nExport all shots in this Seqeunce?',
        button=['Yes','No'], 
        messageAlign = 'center',
        defaultButton='Yes', 
        cancelButton='No', 
        dismissString='No' )
    if result == 'Yes':
        #print 'clicked yes'
        executeBatchExport()
        
def executeBatchExport():
    mayaSeqNodes = cmds.ls('*Sequence_Node')
    if mayaSeqNodes:
        mayaNode = mayaSeqNodes[0]
        cineSeqNode = csn.CineSequenceNode.getCineSeqNode(mayaNode) 
        fileName = r'{}'.format(cmds.file(q=True, sn=True))
        print(fileName)
        scriptPath = "{}\\{}".format(cc.CineStaticClass.scriptsPath, 'MayaExportStandalone.py')
        command = [cc.CineStaticClass.mayaPyPath, scriptPath, fileName, mayaNode, cineSeqNode.stageString]
        ###
        maya = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = maya.communicate()
        exitcode = maya.returncode
        if str(exitcode) != '0':
            print(err)
            print('error running batch export')
        else:
            print('batch export successful')
        ###
    else:
        nodeUI = csn.MayaSequenceNodeUI()
        nodeUI.mayaCineStartUI(nodeUI)  