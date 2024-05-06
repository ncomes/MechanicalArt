# coding: utf-8

import sys
from maya import OpenMaya, OpenMayaMPx, OpenMayaAnim


class DynamicTime(OpenMayaMPx.MPxNode):
	
	kPluginNodeName = "dynamicTime"
	kPluginNodeId = OpenMaya.MTypeId(0x0C46121)

	def __init__(self):
		OpenMayaMPx.MPxNode.__init__(self)
		
		self.initialized	= False
		
		
		self.depNode		= None
		
		
		self.last_dirtied	= None
		self.matrixDirtieds 	= []
		
		dvTimeValue		= OpenMayaAnim.MAnimControl.currentTime().value()
		self.lastTimeValue	= float(dvTimeValue)
		self.outTimeValue	= float(dvTimeValue)
		
		self.lastMMatrix	= OpenMaya.MMatrix.identity

	@classmethod
	def nodeCreator( cls ):
		return OpenMayaMPx.asMPxPtr( cls() )

	@classmethod
	def nodeInitializer( cls ):
		unitAttr	= OpenMaya.MFnUnitAttribute()
		matrixAttr	= OpenMaya.MFnMatrixAttribute()

		# baseTime
		cls.inTime	= unitAttr.create(  "inTime", "t", OpenMaya.MFnUnitAttribute.kTime, 1.0)
		unitAttr.setKeyable( True )

		cls.inMatrices	= matrixAttr.create( "inMatrices" ,"ims" , OpenMaya.MFnNumericData.kFloat )
		matrixAttr.setArray( True )

		cls.outTime	= unitAttr.create(  "outTime", "ot", OpenMaya.MFnUnitAttribute.kTime, 1.0)
		unitAttr.setWritable( False )
		unitAttr.setStorable( False )


		for attr in (cls.inTime, cls.inMatrices, cls.outTime ) :
			cls.addAttribute( attr)

	# voir dependances dans setDependentsDirty

	def check_depNode( self ):
		if not self.depNode :
			self.depNode		= OpenMaya.MFnDependencyNode(  self.thisMObject() )
		return self.depNode

	def setDependentsDirty( self ,plugDirtied , affectedPlugs) :
		#print "\n----------------",plugDirtied.info()
		
		
		dNode		= self.check_depNode()
		
		
		if plugDirtied == self.inTime  :
			
			self.matrixDirtieds 	= []
			affectedPlugs.append(   dNode.findPlug( "outTime" )   )

		elif ( plugDirtied == self.inMatrices
			and plugDirtied.isElement()  ):
			
			self.matrixDirtieds.append( plugDirtied  )
			affectedPlugs.append(   dNode.findPlug( "outTime" )   )
		
		# sauve le dernier plug dirtied name
		self.last_dirtied	= plugDirtied.partialName(False,False,False,False,False,True)
	
	def compute( self, plug, data  ) :
		
		# refresh + get time :
		data.inputValue( self.inMatrices )
		
		current_Time		= data.inputValue( self.inTime ).asTime()
		current		= current_Time.value()

		# init
		if not self.initialized :
			
			self.outTimeValue	= float(current)
			self.lastTimeValue	= float(current)
			data.outputValue(  self.outTime ).setMTime( current_Time )
			
			data.setClean( plug )
			
			self.initialized = True
			return

		# check
		dNode			= self.check_depNode()
		connected_num	= dNode.findPlug("inMatrices").numConnectedElements()
		
		if  ((self.last_dirtied == "inTime"  and  current!=self.lastTimeValue)
			or len( self.matrixDirtieds ) > connected_num ):
			pass
			
		else  :
			return

		# reset ou increment
		if current == OpenMayaAnim.MAnimControl.minTime().value()  :
			
			self.outTimeValue	= current
			data.outputValue(  self.outTime ).setMTime( current_Time )
		else :
			#units	= ( OpenMaya.MTime.kNTSCFrame, OpenMaya.MTime.kSeconds, OpenMaya.MTime.kMinutes, OpenMaya.MTime.kHours )
			currentUnit	= OpenMaya.MTime.uiUnit()
			
			
			self.outTimeValue	+= 1.0
			time			= OpenMaya.MTime(self.outTimeValue, currentUnit )
			
			data.outputValue(  self.outTime ).setMTime( time )

		#
		self.lastTimeValue	= current
		
		data.setClean( plug )
		

def initializePlugin(mobject):
	mplugin = OpenMayaMPx.MFnPlugin(mobject, "Hans Godard -- zapan669@hotmail.com", "1.0", "Any")
	try:
		mplugin.registerNode( DynamicTime.kPluginNodeName, DynamicTime.kPluginNodeId, DynamicTime.nodeCreator, DynamicTime.nodeInitializer )
	except:
		sys.stderr.write( "Failed to register command: %s\n" % DynamicTime.kPluginNodeName )
		raise


def uninitializePlugin(mobject):
	mplugin = OpenMayaMPx.MFnPlugin(mobject)
	try:
		mplugin.deregisterNode( DynamicTime.kPluginNodeId )
	except:
		sys.stderr.write( "Failed to unregister node: %s\n" % DynamicTime.kPluginNodeName )
		raise
