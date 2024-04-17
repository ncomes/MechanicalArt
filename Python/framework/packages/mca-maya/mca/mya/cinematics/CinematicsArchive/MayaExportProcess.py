import maya.cmds as cmds
import mca.mya.cinematics.CinematicsArchive.CineClasses as cc
import maya.mel as mm
import os
from mca.mya.cinematics.CinematicsArchive.CinematicXML import CineXML
from mca.mya.cinematics.CinematicsArchive.AddLocator import makeLoc

class MayaExporter:
                    
    def getCameraTransform(self, cam):
        #print(cmds.objectType(cam))
        if cmds.objectType(cam) != 'transform':
            #print('getting camera transform')
            camT = cmds.listRelatives(cam, p=True)
        else:
            #print('have camera transform')
            camT = cam
            
        return camT
            
    def processCameraRig(self, cineShot):
        atList = ["rx","ry","rz","tx","ty","tz"]
        camT = self.getCameraTransform(cineShot.cam.mayaCam)
        #print 'unlocking camera {}'.format(cam)
        cmds.lockNode(camT, l=False)
        cmds.camera(camT, e=True, lt=False)
        
        if cmds.keyframe(camT, q=True, kc=True, s=False):
            #print('animation directly on camera')
            loc = makeLoc(camT, 'camera_rig_export_locator')
            cmds.parentConstraint(camT, loc, mo=False)
            #bake locator onto camera
            cmds.bakeResults(loc, sm=True, t=(cineShot.start, cineShot.end), at=atList)
            #clear animation on camera
            cmds.cutKey(camT, s=False, cl=True)
            #parent camera to world
            cmds.parent(camT, w=True)
            #constrain camera to locator
            cmds.parentConstraint(loc, camT, mo=False)
            
        elif cmds.parentConstraint(camT, q=True, tl=True):
            #print('camera constrained properly')
            pass
        
        else:
            if cmds.listRelatives(camT, p=True):
                #print('camera directly parented to foreign object, no animation')
                #mark camera locaiton
                loc = makeLoc(camT, 'camera_rig_export_locator')
                #parent camera to the world
                cmds.parent(camT, w=True)
                #constrain camera to locator
                cmds.parentConstraint(loc, camT, mo=False)
            else:
                #print('camera parented to world, no animation')
                pass

    def processCamera(self, cineShot):
        camT = self.getCameraTransform(cineShot.cam.mayaCam)
        self.processCameraRig(cineShot)
        cmds.bakeResults(camT, sm=True, mr=True, s=True, t=(cineShot.start, cineShot.end+1))
        try:
            cmds.parent(camT, w=True)
        except RuntimeError as e:
            print(e)
            
        removeAttr = ["focusDistance", "centerOfInterest", "fStop"]
        camShape = cmds.listRelatives(camT, s=True)[0]
        for each in removeAttr:
            cmds.cutKey("{}.{}".format(camShape, each), time=(cineShot.start, cineShot.end+1), cl=True)

        #print('baked cam {}'.format(camT))
    
    def getExportName(self, cineClass, cineShot):
        #naming convention: A_SEQ_010_Object
        exportDir = cc.CineStaticClass.getShotDirDict()['exports']
        if not os.path.exists(exportDir):
            os.mkdir(exportDir)
        if isinstance(cineClass, cc.CineCamera):
            name = 'cam'
        else:
            name = cineClass.displayName
        saveAs = "A_{}_{}_{}".format(cineShot.seq.name, '{0:0=3d}'.format(cineShot.number), name)
        exportName = "{}/{}".format(exportDir, saveAs)
        
        return exportName
    
    def getSingleBoneProps(self):
        propGrpName = 'props_grp'
        singleBoneProps = []
        if cmds.objExists(propGrpName):
            for each in cmds.listRelatives(propGrpName, c=True):
                if not cmds.getAttr('{}.visibility'.format(each))==0:
                    shapes = cmds.listRelatives(each, s=True)
                    if shapes:
                        for s in shapes:
                            if cmds.objectType(s) =='mesh':
                                singleBoneProps.append(each)
                            
        return singleBoneProps
    
    def fillCineShot(self, cineShot):
        #print('filling cineShot: {}'.format(cineShot.name))
        cineShot.chars = []
        cineShot.props = []
        singleBoneProps = self.getSingleBoneProps()
        for each in singleBoneProps:
            #unrigged props
            #print('found unrigged prop: {}'.format(each))
            prop = cc.CineProp.getCinePropFromElementName(each, cineShot)
            cineShot.props.append(prop)
        exportElements = cmds.ls("*:root")
        for each in exportElements:
            #prop
            p = cmds.listRelatives(each, p=True)
            #print(p)
            if p and 'geoBase' in p[0]:
                #print('found prop: {}'.format(each))
                prop = cc.CineProp.getCinePropFromElementName(each, cineShot)
                cineShot.props.append(prop)
            else:
                #character
                #print('found character: {}'.format(each))
                char = cc.CineCharacter(each, cineShot.version)
                cineShot.chars.append(char)          
        
    def offsetAnimation(self, obj, cineShot):
        #offset animation to frame 0
        try:
            cmds.keyframe(obj, hi='below', edit=True, r=True, iub=True, option='over', 
                          timeChange=(-cineShot.start))
            #print ('moving keys back to 0 for {}'.format(obj))
        except RuntimeError as e:
            print('cannot move keys for some stupid reason')
            print(e)
            pass
    
    def setMayaTimeline(self, cineShot):
        #set anim tangents
        cmds.keyTangent(g=True, itt='auto')
        cmds.keyTangent(g=True, ott='auto')
        cmds.playbackOptions(min=cineShot.start-cineShot.start)
        cmds.playbackOptions(ast=cineShot.start-cineShot.start)
        cmds.playbackOptions(max=cineShot.end-cineShot.start+1)
        cmds.playbackOptions(aet=cineShot.end-cineShot.start+1)    
                
    def exportFBX(self, obj, exportName):
        #print('exports an fbx to a location defined by exportName')
        fbxName = r'{}.fbx'.format(exportName)
        cmds.setAttr("{}.visibility".format(obj), 1)
        cmds.select(cl=True)
        cmds.select(obj)
        #print(obj)
        #print(exportName)
        shapes = cmds.listRelatives(obj, s=True)
        if shapes:      
            if shapes[0] in cmds.listCameras():
                #print('making fbx settings for camera export')
                mm.eval("FBXExportCameras -v true")
        mm.eval("FBXExportUpAxis z")
        mm.eval("FBXExportBakeComplexAnimation -v true")
        mm.eval('FBXExportInputConnections -v false')
        #print('fbx settings made, attempting export')
        mm.eval('FBXExport -f "{}" -s'.format(fbxName))
    
    def exportXML(self, cineShot, exportSelect):
        xmlExporter = CineXML()
        if exportSelect:
            xmlExporter.exportElementXML(exportSelect, cineShot)
        else:
            xmlExporter.exportShotXML(cineShot)
    
    def exportShot(self, cineShot):
        #camera
        self.processCamera(cineShot)
        self.exportFBX(cineShot.cam.mayaCam, self.getExportName(cineShot.cam, cineShot))
        #prop
        for prop in cineShot.props:
            self.exportFBX(prop.name, self.getExportName(prop, cineShot))
        #character
        for char in cineShot.chars:
            #INSERT CHARACTER EXPORTER HERE
            exportName = self.getExportName(char, cineShot)
            print('currently not exporting character: {}'.format(char.displayName))
    
    def exportElement(self, cineShot, exportElement):
        if type(exportElement) == cc.CineCamera:
                #camera
                #print('selected export element is a camera: {}'.format(exportElement.displayName))
                self.processCamera(cineShot)
                self.exportFBX(cineShot.cam.mayaCam, self.getExportName(cineShot.cam, cineShot))
        elif type(exportElement) == cc.CineCharacter:
            #character
            #print('selected export element is a character: {}'.format(exportElement.displayName))
            #INSERT CHARACTER EXPORTER HERE
            exportName = self.getExportName(exportElement, cineShot)
            print('currently not exporting character: {}'.format(exportElement.displayName))
        elif type(exportElement) == cc.CineProp:
            #prop
            #print('selected export element is a prop: {}'.format(exportElement.displayName))
            self.exportFBX(exportElement.name, self.getExportName(exportElement, cineShot))
                
    def exportAnimation(self, cineShot, exportElement=None):
        #export element must be a cineclass object
        #
        self.setMayaTimeline(cineShot)        
        if exportElement:
            self.exportElement(cineShot, exportElement)
        else:
            #gather characters and prop information into the shot for xml data here
            self.fillCineShot(cineShot)
            self.exportShot(cineShot)
        #write xml doc
        self.exportXML(cineShot, exportElement)
        cmds.file(rn=cc.CineStaticClass.doNotSaveName)
        
        
        
        