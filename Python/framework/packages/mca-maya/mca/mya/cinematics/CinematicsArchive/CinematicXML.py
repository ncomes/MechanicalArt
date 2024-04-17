import xml.etree.ElementTree as et
from xml.dom import minidom
import os
import mca.mya.cinematics.CinematicsArchive.CineClasses as cc

#---------------------------------------------------------------------------
"""
#Test Material
seqPath = r"C:/Users/ctshe/Desktop/pipelineRedux/sequences/TST"
seqName = "TST"
seqTST = cc.CineSequence(seqName, seqPath)
chad = cc.CineCharacter("Chad", 1)
becky = cc.CineCharacter("Becky", 1)
icePick = cc.CineProp("Ice_Pick", 1, 1, chad)
TST_shot_010 = cc.CineShot(seqTST, 10, 10, 100, 1, [chad, becky], [icePick])
TST_shot_020 = cc.CineShot(seqTST, 20, 150, 225, 2, [becky])
"""
#---------------------------------------------------------------------------


class CineXML:
    
    namingConvention = r'{}/{}_sequenceDoc.xml'
    
    def __init__(self, name="writer", rootNode=None, shotsNode=None, path=None):
        self.name = name
        self.rootNode = rootNode
        self.shotsNode = shotsNode
        self.path = path
    
    #Main Function
    
    def exportShotXML(self, cineShot):
        dir = cc.CineStaticClass.getShotDirDict()['sequence']
        path = self.namingConvention.format(dir, cineShot.seq.name)
        cXML = self.getCineXML(path, cineShot)
        self.addShotToXML(cXML, cineShot)    
        self.writeXML(cXML)
        
    def exportElementXML(self, exportElementClass, cineShot):
        #print('writing xml for single element')
        dir = cc.CineStaticClass.getShotDirDict()['sequence']
        path = self.namingConvention.format(dir, cineShot.seq.name)
        nodeParent, elementType, cXML = self.getCineXMLElement(path, cineShot, exportElementClass)
        if cXML:
            self.addElementToShot(nodeParent, elementType, exportElementClass)   
            self.writeXML(cXML)
        
    #---------------------------------------------------------------------------
    
    def writeXML(self, cXML):
        #sort the xml
        cXML.shotsNode[:] = sorted(cXML.shotsNode, key=lambda child: (child.tag,child.get('name')))
        #write the root node to string
        prettyStringXML = self.getPrettyStringXML(cXML)
        #clear the path for the file
        fileXML = open(cXML.path, "w")
        #write the file using the string data
        fileXML.write(prettyStringXML)
        print("finished writing XML")         
        
    def getCineXML(self, path, cineShot):
        if os.path.exists(path):
            print("Found XML doc at {}".format(path))
            cXML = self.getExistingXML(path)
            foundShot, xShot = self.checkForShot(cXML, cineShot)
            if foundShot:
                #print('found existing shot {} in xml doc, removing shot'.format(cineShot.name))
                cXML.shotsNode.remove(xShot)
        else:
            print("No XML document at {}".format(path))
            cXML = self.getNewXML(cineShot.seq, path)
            
        return cXML
    
    def getCineXMLElement(self, path, cineShot, elementClass):
        if os.path.exists(path):
            print("Found XML doc at {}".format(path))
            cXML = self.getExistingXML(path)
            foundShot, xShot = self.checkForShot(cXML, cineShot)
            if foundShot:
                foundElement, nodeParent, elementType, foundNode = self.checkForElement(
                                                                    xShot, elementClass)
                if foundElement:
                    #print('found existing element {} in xml doc, removing element'.format(
                            #elementClass.displayName))
                    nodeParent.remove(foundNode)
                else:
                    print('no shot {} found in xml doc'.format(elementClass.displayName))
            else:
                print('no shot {} found in xml doc'.format(cineShot.name))
        else:
            print("No XML document at {}, cannot write out single element".format(path))
            cXML = None
            
        return nodeParent, elementType, cXML
        
    def getPrettyStringXML(self, cXML):
        #used to make the XML look nicer when opening in text editor
        stringXML = et.tostring(cXML.rootNode, encoding='unicode', method='xml')
        reparsedXML = minidom.parseString(stringXML)
        prettyStringXML = reparsedXML.toprettyxml(indent='  ')
        prettyStringXML = os.linesep.join(
            [s for s in prettyStringXML.splitlines() if s.strip()])
        
        return prettyStringXML
                
    def getNewXML(self, seq, path):
        #makes new CineXML object
        #print("making new CineXML to start new XML file")
        rootNode = et.Element('{}_sequence_information'.format(seq.name), {'name': seq.name})
        shotsNode = et.SubElement(rootNode, 'shots')
        cXML = CineXML(
            "{}_CineXML".format(seq.name), rootNode, shotsNode, path)
        
        return cXML
    
    def getExistingXML(self, path):
        #creates a CineXML object from the existing XML file
        tree = et.parse(path)
        rootNode = tree.getroot()
        seqName = rootNode.get('name')
        #print(seqName)
        shotsNode = rootNode.find('shots')
        cXML = CineXML("{}_cineXML".format(seqName), rootNode, shotsNode, path)
        
        return cXML
        
#---------------------------------------------------------------------------

    def checkForShot(self, cXML, cineShot):
        #print('all shots found in {} XML:'.format(cineShot.seq.name))
        foundShot = False
        xShot = None
        for s in cXML.shotsNode.findall('shot'):
                #print(s.get('name'))
                if cineShot.name == s.get('name'):
                    #print('found {} from XML'.format(cineShot.name))
                    foundShot = True
                    xShot = s
                #print("{} does not equal {}".format(cineShot.name, s.get('name')))
                
        return foundShot, xShot
    
    def checkForElement(self, xShot, elementClass):
        foundElement = False
        nodeParent = None
        if type(elementClass) == cc.CineCamera:
            #print('xml element is camera')
            nodeParent = xShot
            foundNode = xShot.find('camera')
            foundElement = True
            elementType = 'camera'
        else:
            if type(elementClass) == cc.CineProp:
                #print('xml element is prop')
                elementType = 'prop'
            if type(elementClass) == cc.CineCharacter:
                #print('xml element is character')
                elementType = 'character'
            if xShot.find('{}s'.format(elementType)):
                    nodeParent = xShot.find('{}s'.format(elementType))
                    if elementClass.displayName in nodeParent.attrib:
                        #print('found {} {} in xml props node'.format(
                                #elementType, elementClass.displayName))
                        foundNode = nodeParent.find(elementClass.displayName)
                        foundElement = True
                    else:
                        print('{} {} not found in {}'.format(
                            elementType, elementClass.displayName, nodeParent.get('name')))
                
            #for each in xShot.findall('{}s'.format(elementType)):
                #print(each.get('name'))
        
        return foundElement, nodeParent, elementType, foundNode
    
    def addElementToShot(self, nodeParent, elementType, elementClass):
        #print('adding {} to XML'.format(elementClass.displayName))
        if elementType == 'camera':
            e = et.SubElement(nodeParent, elementType, self.getCameraAttributes(elementClass))
        elif elementType == 'character':
            e = et.SubElement(nodeParent, elementType, self.getCharacterAttributes(elementClass))
        elif elementType == 'prop':
            e = et.SubElement(nodeParent, elementType, self.getPropAttributes(elementClass))
    
    def addShotToXML(self, cXML, cineShot):
        #print('adding {} to XML'.format(cineShot.name))
        xShot = et.SubElement(cXML.shotsNode, 'shot', self.getShotAttributes(cineShot))
        shotInfoNode = et.SubElement(xShot, 'shot_info', self.getShotInfoAttributes(cineShot))
        cameraNode = et.SubElement(xShot, 'camera', self.getCameraAttributes(cineShot.cam))
        if cineShot.chars:
            charsNode = et.SubElement(xShot, 'characters')
            self.fillCharacterData(charsNode, cineShot)            
        if cineShot.props:
            propsNode = et.SubElement(xShot, 'props')
            self.fillPropData(propsNode, cineShot)            
    
    def fillCharacterData(self, charsNode, cineShot):
        for char in cineShot.chars:
            #print("shot has character: {}".format(char.displayName))
            c = et.SubElement(
                charsNode, 'character', self.getCharacterAttributes(char))
            
    def fillPropData(self, propsNode, sht):
        for prop in sht.props:
            #print("shot has prop: {}".format(prop.displayName))
            p = et.SubElement(
                propsNode, 'prop', self.getPropAttributes(prop))
    
    #All XML data must be strings!
    def getShotAttributes(self, cineShot):
        #print("Making shot {}".format(cineShot.name))
        attrib = {'name': cineShot.name,
                  'number': str(cineShot.number)}
        
        return attrib
    
    def getShotInfoAttributes(self, sht):
        attrib = {'start_frame': str(sht.start),
                  'end_frame': str(sht.end),
                  'duration': str(sht.end-sht.start+1),
                  'exported_range': str(sht.end-sht.start+2)}
        
        return attrib
    
    def getCameraAttributes(self, cam):
        attrib = {'camera_name': cam.displayName,
                  'camera_focal_length': str(cam.focalLength),
                  'camera_version': str(cam.version)}
        
        return attrib
    
    def getCharacterAttributes(self, char):
        attrib = {'charater_name': char.displayName,
                  'version': str(char.version)}
        
        return attrib
    
    def getPropAttributes(self, prop):
        attrib = {'prop_name': prop.displayName,
                  'attachment': prop.attachment,
                  'version': str(prop.version)}
        
        if prop.char:
            print ('found character associated with prop: {}'.format(prop.char.displayName))
            attrib['character'] = prop.char.displayName
            
        if prop.rigged:
            #print('prop is rigged')
            attrib['rig'] = 'True'
        else:
            #print('prop is not rigged')
            attrib['rig'] = 'False'
        
        return attrib

#---------------------------------------------------------------------------
"""
#Test Material
seqPath = r"C:/Users/ctshe/Desktop/pipelineRedux/sequences/TST"
seqName = "TST"
seqTST = cc.CineSequence(seqName, seqPath)
chad = cc.CineCharacter("Chad", 1)
becky = cc.CineCharacter("Becky", 1)
icePick = cc.CineProp("Ice_Pick", 1, 1, chad)
TST_shot_010 = cc.CineShot(seqTST, 10, 10, 100, 1, [chad, becky], [icePick])
TST_shot_020 = cc.CineShot(seqTST, 20, 150, 225, 2, [becky])
seqTST.shots = [TST_shot_010, TST_shot_020]
"""
#---------------------------------------------------------------------------

#xmlWriter = CineXML()
#xmlWriter.exportShotXML(TST_shot_020)
