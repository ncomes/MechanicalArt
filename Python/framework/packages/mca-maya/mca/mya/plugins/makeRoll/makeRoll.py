# coding: utf-8

import sys
from maya import OpenMaya, OpenMayaMPx, OpenMayaAnim


class MakeRoll(OpenMayaMPx.MPxNode):
	
	kPluginNodeName = "makeRoll"
	kPluginNodeId = OpenMaya.MTypeId(0x0FE4321)
	
	
	@staticmethod
	def get_3_MAngles( data, attributes ):
		angles = []
		for attr in attributes :
			angles.append( data.inputValue( attr ).asAngle() )
		return angles
	
	@staticmethod
	def set_3_MAngles( data, attributes, angles ):
		for attr,angle in zip( attributes, angles) :
			out_Handle		= data.outputValue(  attr )
			out_Handle.setMAngle( angle )
		
	
	@staticmethod
	def MM_to_FM( mm ):
		valueList = [
			mm(0,0),mm(0, 1),mm(0, 2),mm(0, 3),
			mm(1,0),mm(1, 1),mm(1, 2),mm(1, 3),
			mm(2,0),mm(2, 1),mm(2, 2),mm(2, 3),
			mm(3,0),mm(3, 1),mm(3, 2),mm(3, 3) ]
		outMat = OpenMaya.MFloatMatrix()
		OpenMaya.MScriptUtil.createFloatMatrixFromList( valueList , outMat )
		return outMat
	
	
	
	@classmethod
	def nodeCreator( cls ):
		return OpenMayaMPx.asMPxPtr( cls() )
	
	@classmethod
	def nodeInitializer( cls ):
		numAttr	= OpenMaya.MFnNumericAttribute()
		unitAttr	= OpenMaya.MFnUnitAttribute()
		compAttr	= OpenMaya.MFnCompoundAttribute()
		matrixAttr	= OpenMaya.MFnMatrixAttribute()
		
		cls.inTime	= unitAttr.create(  "inTime", "t", OpenMaya.MFnUnitAttribute.kTime, 1.0)
		unitAttr.setKeyable( True )
		
		cls.computeX	= numAttr.create( "computeX", "cx", OpenMaya.MFnNumericData.kBoolean, True)
		cls.computeY	= numAttr.create( "computeY", "cy", OpenMaya.MFnNumericData.kBoolean, True)
		cls.computeZ	= numAttr.create( "computeZ", "cz", OpenMaya.MFnNumericData.kBoolean, True)
		
		cls.weight	= numAttr.create("weight","w",OpenMaya.MFnNumericData.kFloat, 1.0)
		numAttr.setKeyable( True )
		
		cls.radius	= numAttr.create("radius","r",OpenMaya.MFnNumericData.kFloat, 1.0)
		numAttr.setKeyable( True )
		
		cls.upVector = numAttr.createPoint( "upVector","uv")
		numAttr.setKeyable( True )
		
		cls.inTranslate = numAttr.createPoint( "inTranslate","it")
		numAttr.setKeyable( True )
		
		#cls.resetRotate = numAttr.createPoint( "resetRotate","ir")
		#numAttr.setKeyable( True )
		cls.resetRotateX	= unitAttr.create(  "resetRotateX", "rrx", OpenMaya.MFnUnitAttribute.kAngle, .0)
		cls.resetRotateY	= unitAttr.create(  "resetRotateY", "rry", OpenMaya.MFnUnitAttribute.kAngle, .0)
		cls.resetRotateZ	= unitAttr.create(  "resetRotateZ", "rrz", OpenMaya.MFnUnitAttribute.kAngle, .0)
		cls.resetRotate	= compAttr.create( "resetRotate" , "rr")
		compAttr.addChild( cls.resetRotateX )
		compAttr.addChild( cls.resetRotateY )
		compAttr.addChild( cls.resetRotateZ )
		compAttr.setKeyable( True )
		
		#cls.lastRotate = numAttr.createPoint( "lastRotate","lr")
		#numAttr.setHidden( True )
		#numAttr.setConnectable( False )
		cls.lastRotateX	= unitAttr.create(  "lastRotateX", "lrx", OpenMaya.MFnUnitAttribute.kAngle, .0)
		cls.lastRotateY	= unitAttr.create(  "lastRotateY", "lry", OpenMaya.MFnUnitAttribute.kAngle, .0)
		cls.lastRotateZ	= unitAttr.create(  "lastRotateZ", "lrz", OpenMaya.MFnUnitAttribute.kAngle, .0)
		cls.lastRotate		= compAttr.create( "lastRotate" , "lr")
		compAttr.addChild( cls.lastRotateX )
		compAttr.addChild( cls.lastRotateY )
		compAttr.addChild( cls.lastRotateZ )
		compAttr.setHidden( True )
		compAttr.setConnectable( False )
		
		cls.relativeMatrix = matrixAttr.create( "relativeMatrix" ,"rm" , OpenMaya.MFnNumericData.kFloat )
		
		
		#cls.outRotate = numAttr.createPoint( "outRotate","oeu")
		#numAttr.setWritable( False )
		cls.outRotateX	= unitAttr.create(  "outRotateX", "orx", OpenMaya.MFnUnitAttribute.kAngle, .0)
		cls.outRotateY	= unitAttr.create(  "outRotateY", "ory", OpenMaya.MFnUnitAttribute.kAngle, .0)
		cls.outRotateZ	= unitAttr.create(  "outRotateZ", "orz", OpenMaya.MFnUnitAttribute.kAngle, .0)
		cls.outRotate		= compAttr.create( "outRotate" , "oeu")
		compAttr.addChild( cls.outRotateX )
		compAttr.addChild( cls.outRotateY )
		compAttr.addChild( cls.outRotateZ )
		compAttr.setWritable( False )
		
		cls.outMatrix	= matrixAttr.create( "outMatrix" ,"om" , OpenMaya.MFnNumericData.kFloat )
		matrixAttr.setWritable( False )
		
		
		for attr in (cls.inTime, cls.computeX,cls.computeY,cls.computeZ,
				cls.weight, cls.radius, cls.upVector, cls.inTranslate, cls.resetRotate, cls.relativeMatrix, cls.lastRotate,
				cls.outRotate, cls.outMatrix ):
			cls.addAttribute( attr )
		
		for attr in (cls.inTime, cls.computeX,cls.computeY,cls.computeZ, cls.weight, cls.radius, cls.upVector, cls.inTranslate, cls.relativeMatrix):
			cls.attributeAffects( attr, cls.outRotate )
			cls.attributeAffects( attr, cls.outMatrix )
		
	
	
	def __init__(self):
		OpenMayaMPx.MPxNode.__init__(self)
		self.initialized = False
		self.lastPos = [.0,.0,.0]
		#self.lastRot	= [.0,.0,.0] ---->	inutil car ya besoin d'un attribut de toute facon pour sauver lastEuler
	
	
	
	def initialize( self, data):
		'''prend la derniere rotation sauv�e  et translate = inTranslate'''
		#
		manipPos	= data.inputValue( self.inTranslate ).asFloatVector()
		manipPos	= [manipPos[0],manipPos[1],manipPos[2]]
		self.lastPos	= manipPos
		
		#
		lastRot		= self.get_3_MAngles( data, (self.lastRotateX, self.lastRotateY,self.lastRotateZ) )
		self.set_3_MAngles( data, (self.outRotateX,self.outRotateY,self.outRotateZ), lastRot )
		
		self.initialized = True
	
	
	def reset(self, data, plug):
		'''prend la rotation du resetRotate  et lastTranslate = inTranslate'''
		#
		manipPos	= data.inputValue( self.inTranslate ).asFloatVector()
		manipPos	= [manipPos[0],manipPos[1],manipPos[2]]
		self.lastPos	= manipPos
		
		
		# get resetRotate
		manipRot	= self.get_3_MAngles( data, (self.resetRotateX, self.resetRotateY,self.resetRotateZ) )
		self.set_3_MAngles( data, (self.lastRotateX,self.lastRotateY,self.lastRotateZ), manipRot )
		
		
		# set dans output plug
		if plug in (self.outRotate, self.outRotateX, self.outRotateY, self.outRotateZ,):
			self.set_3_MAngles( data, (self.outRotateX,self.outRotateY,self.outRotateZ), manipRot )
		
		elif plug == self.outMatrix:
			# juste conversion 3 Angles to FM
			manipRot_Euler	= [item.value() for item in manipRot]
			manipRot_Euler	= OpenMaya.MEulerRotation( manipRot_Euler[0], manipRot_Euler[1], manipRot_Euler[2]  )
			out_Tf		= OpenMaya.MTransformationMatrix()
			out_Tf.rotateTo( manipRot_Euler  )
			out_FM		= self.MM_to_FM( out_Tf.asMatrix() )
			
			data.outputValue(self.outMatrix).setMFloatMatrix( out_FM )
		
	
	
	
	def compute(self, plug, data):
		
		
		if not plug in (self.outRotate, self.outRotateX, self.outRotateY, self.outRotateZ, self.outMatrix) :
			return
		
		
		if not self.initialized :
			self.initialize( data )
		
		
		
		# else
		currentTime	= data.inputValue( self.inTime ).asTime().value()
		startTime		= OpenMayaAnim.MAnimControl.minTime().value()
		
		
		
		if  currentTime > startTime :
			manipPos	= data.inputValue( self.inTranslate ).asFloatVector()
			manipPos	= [manipPos[0],manipPos[1],manipPos[2]]
			
			
			wgt	= data.inputValue( self.weight).asFloat()
			if wgt ==.0 :
				self.lastPos	= manipPos
				return
			
			
			
			if self.lastPos !=manipPos  :
				
				
				# trouve pivot de rotation  rot_FV  en local :
				deltaPos	= [ manipPos[i]-self.lastPos[i] for i in range(3)]
				
				aim_FV	= OpenMaya.MFloatVector( deltaPos[0],deltaPos[1],deltaPos[2]  )
				up_FV	= data.inputValue( self.upVector).asFloatVector()
				
				rot_FV	= aim_FV ^ up_FV
				
				
				
				# relative pivot   +   fake pivot (component axis a 0 ou pas ) :
				relativ_FM	= data.inputValue( self.relativeMatrix ).asFloatMatrix()
				rot_FV		= rot_FV * relativ_FM
				
				areComputed	= [ int(data.inputValue( attr).asBool()) for attr in (self.computeX, self.computeY, self.computeZ) ]
				rot_FV		= OpenMaya.MFloatVector( rot_FV[0]*areComputed[0], rot_FV[1]*areComputed[1], rot_FV[2]*areComputed[2])
				
				
				
				# calcul de la distance :  repart de ce nouveau pivot
				#	la distance est celle du projet� de aim sur le plan normalis� par up   donc un dotProduct
				up_FV	= up_FV *  relativ_FM
				aim_FV	= aim_FV *  relativ_FM
				tmp_FV	= up_FV ^ rot_FV
				tmp_FV.normalize()
				distance	= aim_FV.x*tmp_FV.x + aim_FV.y*tmp_FV.y + aim_FV.z*tmp_FV.z
				
				# en fonction de la distance et du radius, trouve l'angle de rotation
				radius	= data.inputValue(self.radius).asFloat()
				angle		= -1.0 * wgt * distance/radius # jai pas trop compris pourquoi multiplier par -1  mais sinon c'est pas bon, peut etre car cest un Right Handed ?
				
				
				
				# incrementes les angles d'euler :
				#last_Euler	= data.inputValue( self.lastRotate ).asFloatVector()
				last_Euler	= self.get_3_MAngles( data, (self.lastRotateX,self.lastRotateY,self.lastRotateZ) )
				last_Euler	= [item.value() for item in last_Euler]
				last_Euler	= OpenMaya.MEulerRotation( last_Euler[0], last_Euler[1], last_Euler[2]  )
				
				#out_Euler	= last_Euler * OpenMaya.MQuaternion( rot_FV[0],rot_FV[1],rot_FV[2], angle  )
				# equivaut a la commande 'rotate' de mel :
				out_Euler		= last_Euler.incrementalRotateBy( OpenMaya.MVector(rot_FV[0],rot_FV[1],rot_FV[2]), angle )
				out_Angles	= [OpenMaya.MAngle( item) for item in [out_Euler[0],out_Euler[1],out_Euler[2]]]
				
				
				
				
				# end :
				self.set_3_MAngles( data, (self.lastRotateX,self.lastRotateY,self.lastRotateZ), out_Angles )
				
				
				if plug in (self.outRotate, self.outRotateX, self.outRotateY, self.outRotateZ,):
					self.set_3_MAngles( data, (self.outRotateX,self.outRotateY,self.outRotateZ), out_Angles )
				
				
				elif plug == self.outMatrix :
					out_Tf	= OpenMaya.MTransformationMatrix()
					out_Tf.rotateTo( out_Euler  )
					
					out_FM	= self.MM_to_FM( out_Tf.asMatrix() )
					data.outputValue(self.outMatrix).setMFloatMatrix( out_FM )
				
			
			
			self.lastPos	= manipPos
		
		
		# reset :
		else :
			self.reset( data, plug )
		
		
		
		data.setClean( plug )
		
	




def initializePlugin(mobject):
	mplugin = OpenMayaMPx.MFnPlugin(mobject, "Hans Godard -- zapan669@hotmail.com", "1.0", "Any")
	try:
		mplugin.registerNode( MakeRoll.kPluginNodeName, MakeRoll.kPluginNodeId, MakeRoll.nodeCreator, MakeRoll.nodeInitializer )
	except:
		sys.stderr.write( "Failed to register command: %s\n" % MakeRoll.kPluginNodeName )
		raise

def uninitializePlugin(mobject):
	mplugin = OpenMayaMPx.MFnPlugin(mobject)
	try:
		mplugin.deregisterNode( MakeRoll.kPluginNodeId )
	except:
		sys.stderr.write( "Failed to unregister node: %s\n" % MakeRoll.kPluginNodeName )
		raise
		
		
