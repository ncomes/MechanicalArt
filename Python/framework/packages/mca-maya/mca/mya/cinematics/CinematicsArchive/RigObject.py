#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Creates and includes a shelf with buttons in mya for Cinematics
"""

# mca python imports
import sys
# PySide2 imports
# software specific imports
import maya.cmds as cmds
# mca python imports
from mca.common.modifiers import decorators
import mca.mya.cinematics.CinematicsArchive.CineClasses as cc
import mca.mya.cinematics.CinematicsArchive.MatchObjs as mo


def canBeRigged(obj):
    if cc.CineStaticClass.isShotCam(obj):
        print("Camera object is not suitable for rig")
        return False
    elif cmds.listConnections(obj) and 'Constraint' in cmds.listConnections(obj)[0]:
        print("Some objects in selection are constrained")
        return False
    else:
        return True


def makeRootBone(obj):
    #first item in selection becomes root
    geoBase = cmds.polyCube(name='geoBase'.format(obj))[0]
    cmds.setAttr('{}.sx'.format(geoBase), .01)
    cmds.setAttr('{}.sy'.format(geoBase), .01)
    cmds.setAttr('{}.sz'.format(geoBase), .01)
    cmds.makeIdentity(geoBase, apply=True, s=True)
    cmds.setAttr('{}.visibility'.format(geoBase), 0)
    #make root rig bone
    rootBone = cmds.joint(name='root'.format(obj))
    mo.matchPos(obj, rootBone)
    cmds.parentConstraint(rootBone, obj)

    return rootBone, geoBase


def addRigControllers(rootBone):
    #print('root bone: {}'.format(rootBone))
    if 'root' in rootBone:
        rootCtrl, ctrlsDict = makeRigHierarchy(rootBone)
        constrainCtrlsToBones(rootBone, rootCtrl, ctrlsDict)

    return rootCtrl


def constrainCtrlsToBones(rootBone, rootCtrl, ctrlsDict):
    mo.matchPos(rootBone, rootCtrl)
    cmds.parentConstraint(rootCtrl, rootBone)
    for bone in ctrlsDict:
        mo.matchPos(bone, ctrlsDict[bone])
        cmds.parentConstraint(ctrlsDict[bone], bone)
        
        
def makeRigHierarchy(rootBone):
    colorNumber = 10
    rootCtrl = addController(rootBone, colorNumber)
    boneHierarchy = cmds.listRelatives(rootBone, ad=True)
    ctrlsDict = {}
    if boneHierarchy:
        boneHierarchy.reverse()
        #print("bone heirarchy: {}".format(boneHierarchy))
        for bone in boneHierarchy:
            color = colorNumber+boneHierarchy.index(bone)+2
            if color>31:
                color-=31
            ctrl = addLocatorController(bone, 17)
            ctrlsDict[bone] = ctrl
            #print('controls dictionary {}'.format(ctrlsDict))
            boneParent = cmds.listRelatives(bone, p=True)[0]
            #print(boneParent)
            if boneParent in ctrlsDict:
                cmds.parent(ctrl, ctrlsDict[boneParent])
            else:
                cmds.parent(ctrl, rootCtrl)        

    return rootCtrl, ctrlsDict


def addLocatorController(bone, color):
    name = '{}_ctrl'.format(bone)
    obj = getObjectFromBone(bone)
    scaleX, scaleY, scaleZ = getBoundingInfo(obj)
    loc = cmds.spaceLocator(n=name)[0]
    cmds.xform(loc, a=True,s=(scaleX*1.1,scaleY*1.1,scaleZ*1.1))
    cmds.setAttr("{}.overrideEnabled".format(loc), 1)
    cmds.setAttr("{}.overrideColor".format(loc), color)

    return loc


def addController(bone, color):
    name = '{}_ctrl'.format(bone)
    radius = getRadius(bone)
    ctrl = makeCurve(name, radius, color)

    return ctrl


def getRadius(bone):
    radius=None
    obj = getObjectFromBone(bone)
    #print('object returned from bone: {}'.format(obj))
    if obj:
        scaleX, scaleY, scaleZ = getBoundingInfo(obj)

        axisDict = {
            'x': scaleX,
            'y': scaleY,
            'z': scaleZ
        }

        upAxis = cmds.upAxis(ax=1, q=1)
        axisDict.pop(upAxis)
        scalesList = []
        for a in axisDict:
            #print('axis being processed from axis list: {}'.format(a))
            scalesList.append(axisDict[a])
        radius = max(scalesList)*.8
    #print('scaleReturned from object: {}'.format(radius))

    return radius


def getObjectFromBone(bone):
    obj = None
    cons = [x for x in cmds.listConnections(bone) if 'parentConstraint' in x]
    if cons:
        con = cons[0]
        objectConnections = [c for c in cmds.listConnections(con) if 'bone' not in c
                            and 'Constraint' not in c]
        if objectConnections:
            obj = objectConnections[0]
    #print('{} object constraints: {}'.format(obj, cons))
    return obj


def getBoundingInfo(obj):
    bboxMinX = cmds.getAttr(obj+".boundingBoxMinX")
    bboxMinY = cmds.getAttr(obj+".boundingBoxMinY")
    bboxMinZ = cmds.getAttr(obj+".boundingBoxMinZ")
    bboxMaxX = cmds.getAttr(obj+".boundingBoxMaxX")
    bboxMaxY = cmds.getAttr(obj+".boundingBoxMaxY")
    bboxMaxZ = cmds.getAttr(obj+".boundingBoxMaxZ")
    scaleX =  bboxMaxX - bboxMinX  
    scaleY =  bboxMaxY - bboxMinY
    scaleZ =  bboxMaxZ - bboxMinZ

    return scaleX, scaleY, scaleZ


def makeCurve(name, r, c):
    axisDict = {
        'x':(1,0,0),
        'y':(0,1,0),
        'z':(0,0,1)
    }
    axis = cmds.upAxis(ax=1, q=1)
    normal = axisDict[axis]
    #print('normal axis: {}'.format(normal))    
    radius = .8*r
    color = 17+c*2
    if color>31:
        color-=31
    ctrl = cmds.circle(n=name, nr=normal, r=radius)[0]
    cmds.setAttr("{}.overrideEnabled".format(ctrl), 1)
    cmds.setAttr("{}.overrideColor".format(ctrl), color)

    return ctrl


def cleanUp(geo, geoBase):
    topNode = 'prop_all'
    if not cmds.objExists(topNode):
        topNode = cmds.group(em=True, n=topNode)
    emptyTransforms = cmds.ls('transform*')
    cmds.delete(emptyTransforms)
    if geoBase:
        cmds.parent(geoBase, topNode)
    for each in geo:
        cmds.parent(each, topNode)


@decorators.track_fnc
def rigObject():
    selection = cmds.ls(sl=True)
    rootBone = None
    geoBase = None
    rootCtrl = None
    bones = []
    geo = []
    clean = True
    
    for each in selection:
        if 'root' in each and cmds.objectType(each) == 'joint':
            rootCtrl = addRigControllers(each)
            cmds.parent(rootCtrl, 'prop_all')
            clean=False
        else:
            if canBeRigged(each):
                geo.append(each)
                if selection.index(each) == 0:
                    rootBone, geoBase = makeRootBone(each)
                    bones.append(rootBone)
                else:
                    if rootBone:
                        newBone = cmds.joint(name="bone_{}".format(each, selection.index(each)))
                        cmds.parent(newBone, w=True)
                        cmds.parent(newBone, rootBone)
                        mo.matchPos(each, newBone)
                        cmds.parentConstraint(newBone, each)
                        bones.append(newBone)
    if selection and clean:
        cleanUp(geo, geoBase)

    return bones