# coding: utf-8

import sys , math
from maya import OpenMaya, OpenMayaMPx





class zapanSmoothDistance(OpenMayaMPx.MPxNode):
	'''Branchement obligatoire dans les 2 matrix + distanceMax'''
	
	kPluginNodeName = "zapanSmoothDistance"
	kPluginNodeId = OpenMaya.MTypeId(0x0077AA7A)
	
	
	
	@staticmethod
	def FMatrix_to_MMatrix(fm):
		mat = OpenMaya.MMatrix()
		OpenMaya.MScriptUtil.createMatrixFromList ([
			fm(0,0),fm(0, 1),fm(0, 2),fm(0, 3),
			fm(1,0),fm(1, 1),fm(1, 2),fm(1, 3),
			fm(2,0),fm(2, 1),fm(2, 2),fm(2, 3),
			fm(3,0),fm(3, 1),fm(3, 2),fm(3, 3)], mat)
		return mat
	
	
	
	@classmethod
	def nodeCreator( cls ):
		return OpenMayaMPx.asMPxPtr( cls() )
	
	
	@classmethod
	def nodeInitializer( cls ):
		
		# matric necessaire pour chopper les worldTranslate :
		matrixAttr = OpenMaya.MFnMatrixAttribute()
		numAttr = OpenMaya.MFnNumericAttribute()
		
		
		# input :
		cls.rootMatrix	= matrixAttr.create( "rootMatrix" , "rm" , OpenMaya.MFnNumericData.kFloat )
		matrixAttr.setReadable( False )
		cls.moveMatrix	= matrixAttr.create( "moveMatrix" , "mm" , OpenMaya.MFnNumericData.kFloat  )
		matrixAttr.setReadable( False )
		
		cls.distanceMax	= numAttr.create( "distanceMax" , "dm" , OpenMaya.MFnNumericData.kFloat , 1.0)
		numAttr.setHidden(False)
		numAttr.setKeyable(True)
		numAttr.setStorable(True)
		numAttr.setMin( 0.0 )
		cls.smoothPercent	= numAttr.create( "smoothPercent" , "sp" , OpenMaya.MFnNumericData.kFloat , 0.05)
		numAttr.setHidden(False)
		numAttr.setKeyable(True)
		numAttr.setStorable(True)
		numAttr.setMin( 0.0001 )
		numAttr.setMax( 0.2 )
		cls.smoothWeight	= numAttr.create( "smoothWeight" , "smw" , OpenMaya.MFnNumericData.kFloat , 0.0)
		numAttr.setHidden(False)
		numAttr.setKeyable(True)
		numAttr.setStorable(True)
		numAttr.setMin( 0.0)
		numAttr.setMax( 1.0 )
		cls.strechWeight	= numAttr.create( "strechWeight" , "stw" , OpenMaya.MFnNumericData.kFloat , 0.0)
		numAttr.setHidden(False)
		numAttr.setKeyable(True)
		numAttr.setStorable(True)
		numAttr.setMin( 0.0)
		numAttr.setMax( 1.0 )
		
		#cls.moveRelative = numAttr.create( "moveRelative" , "mr" , OpenMaya.MFnNumericData.kBoolean , 0)
		#numAttr.setHidden(False)
		#numAttr.setKeyable(False)
		#numAttr.setStorable(True)
		cls.relativeMatrix = matrixAttr.create( "relativeMatrix" ,"relm" , OpenMaya.MFnNumericData.kFloat )
		
		
		# output :
		cls.outTranslateX = numAttr.create( "outTranslateX" , "otx" , OpenMaya.MFnNumericData.kFloat )
		cls.outTranslateY = numAttr.create( "outTranslateY" , "oty" , OpenMaya.MFnNumericData.kFloat  )
		cls.outTranslateZ = numAttr.create( "outTranslateZ" , "otz" , OpenMaya.MFnNumericData.kFloat  )
		cls.outTranslate = numAttr.create( "outTranslate","ot", cls.outTranslateX , cls.outTranslateY,  cls.outTranslateZ )
		numAttr.setWritable(False)
		numAttr.setStorable(False)
		
		
		cls.outDistance = numAttr.create( "outDistance" , "od" , OpenMaya.MFnNumericData.kFloat )
		numAttr.setWritable(False)
		numAttr.setStorable(False)
		numAttr.setHidden(False)
		numAttr.setChannelBox(True)
		
		cls.outDistanceSmooth = numAttr.create( "outDistanceSmooth" , "odm" , OpenMaya.MFnNumericData.kFloat )
		numAttr.setWritable(False)
		numAttr.setStorable(False)
		numAttr.setHidden(False)
		numAttr.setChannelBox(True)
		
		
		# creation  :
		cls.addAttribute( cls.rootMatrix )
		cls.addAttribute( cls.moveMatrix )
		#cls.addAttribute( cls.moveRelative )
		cls.addAttribute( cls.relativeMatrix )
		cls.addAttribute( cls.distanceMax )
		cls.addAttribute( cls.smoothPercent )
		cls.addAttribute( cls.smoothWeight )
		cls.addAttribute( cls.strechWeight )
		
		cls.addAttribute( cls.outTranslate )
		cls.addAttribute( cls.outDistance )
		cls.addAttribute( cls.outDistanceSmooth )
		
		
		# dependance :
		cls.attributeAffects( cls.rootMatrix , cls.outDistance )
		cls.attributeAffects( cls.moveMatrix , cls.outDistance )
		cls.attributeAffects( cls.relativeMatrix , cls.outDistance )
		
		cls.attributeAffects( cls.rootMatrix , cls.outDistanceSmooth )
		cls.attributeAffects( cls.moveMatrix , cls.outDistanceSmooth )
		cls.attributeAffects( cls.distanceMax , cls.outDistanceSmooth )
		cls.attributeAffects( cls.smoothPercent , cls.outDistanceSmooth )
		cls.attributeAffects( cls.smoothWeight , cls.outDistanceSmooth )
		cls.attributeAffects( cls.relativeMatrix , cls.outDistanceSmooth )
		
		cls.attributeAffects( cls.rootMatrix , cls.outTranslate )
		cls.attributeAffects( cls.moveMatrix , cls.outTranslate )
		cls.attributeAffects( cls.distanceMax , cls.outTranslate )
		cls.attributeAffects( cls.smoothPercent , cls.outTranslate )
		cls.attributeAffects( cls.smoothWeight , cls.outTranslate )
		cls.attributeAffects( cls.strechWeight , cls.outTranslate )
		cls.attributeAffects( cls.relativeMatrix , cls.outTranslate )
	
	
	
	
	def __init__(self):
		OpenMayaMPx.MPxNode.__init__(self)
	
	
	def compute( self , plug , data ) :
		
		# si le output va quelque part le node se calcule, sinon rien :
		plugList = [self.outTranslate , self.outDistanceSmooth , self.outDistance]
		if plug  in  plugList :
			
			
			# asMatrix()  ne marche pas car il cherche des doubles !!!  Donc passage oblig� par FMatrix :
			root_MM	= self.FMatrix_to_MMatrix(data.inputValue( self.rootMatrix ).asFloatMatrix())
			move_MM	= self.FMatrix_to_MMatrix(data.inputValue( self.moveMatrix ).asFloatMatrix())
			
			
			# calcul de la distance entre eux  (vecteur invers� pour optimiser outTranslate):
			rootPosition_MV	= OpenMaya.MTransformationMatrix(root_MM).getTranslation( OpenMaya.MSpace.kWorld )
			movePosition_MV	= OpenMaya.MTransformationMatrix(move_MM).getTranslation( OpenMaya.MSpace.kWorld )
			
			direction_FV	= OpenMaya.MFloatVector( rootPosition_MV[0]-movePosition_MV[0] , rootPosition_MV[1]-movePosition_MV[1],rootPosition_MV[2]-movePosition_MV[2] )
			
			# la longueur reste la meme
			distance	= direction_FV.length()
			
			
			# outDistance output :
			if plug == plugList[2] :
				outDistance_Handle = data.outputValue( self.outDistance )
				outDistance_Handle.setFloat( distance )
			
			
			
			###############################
			# Calcul de la nouvelle distance   :
			else :
				
				dMax		= data.inputValue( self.distanceMax ).asFloat()
				dSmooth		= data.inputValue( self.smoothPercent ).asFloat()
				smWgt		= data.inputValue( self.smoothWeight ).asFloat()
				
				# update de dSmooth pour que ca soit une vrai longueur  et jamais < 0  (sinon expression divide 0):
				if dSmooth < .0 :	dSmooth = .0
				
				dSmooth		= dSmooth * dMax
				
				
				# calcule la new distance  et la met dans outDistanceSmooth :
				newDistance	= distance
				delta			= dMax - dSmooth
				
				
				if (delta <= distance)   and  (dSmooth != .0) :
					
					newDistance = dSmooth*(1.0-math.exp(-(distance-delta)/dSmooth)) + delta
					
					# si smWgt=0   newDistance= dMax :
					'''
					if smWgt <1.0 :
						newDistance = smWgt*newDistance + (1.0-smWgt)*dMax
					'''
				
				
				if plug == plugList[1] :
					outDistanceSmooth_Handle = data.outputValue( self.outDistanceSmooth )
					outDistanceSmooth_Handle.setFloat( newDistance )
				
				
				
				#######################################
				# calcul  du outTranslate :
				# recuperer le point de fin   et le vecteur de destination normalis� :
				# fait tout avec des MFloatType  car jarrive pas a faire des float--> double.
				
				else :
					# distance inverse  = la nouvelle norme du vecteur  inverse:
					invDistance = distance-newDistance
					
					# plutot que weighter les position finale , weighter invDistance  avec 0 :
					if smWgt <1.0 :
						invDistance	= smWgt*invDistance
						
					# re-blender avec 0  si ya le strech :
					stWgt	= data.inputValue( self.strechWeight ).asFloat()
					stWgtRev = 1.0- stWgt
					
					if stWgtRev <1.0 :
						invDistance	= stWgtRev*invDistance
					
					
					# vecteur direction  a normaliser :
					direction_FV.normalize()
					
					new_FV = direction_FV  * invDistance
					
					
					# get movePoint position   (on part de la):
					new_FPnt = OpenMaya.MFloatPoint( movePosition_MV[0] , movePosition_MV[1] ,movePosition_MV[2] )
					
					# ajout du vecteur qui place le point au smooth  (en partant du move) :
					new_FPnt += new_FV
					
					
					
					# ... relative au PERE du move :
					relative_FM = data.inputValue( self.relativeMatrix ).asFloatMatrix()
					new_FPnt *= relative_FM
					
					
					# ce MPoint va dans le outTranslate :
					out_Handle = data.outputValue( self.outTranslate )
					out_Handle.set3Float( new_FPnt[0] , new_FPnt[1], new_FPnt[2] )
			
			
			# refresh la connection  pour boucler l'evaluation du node :
			data.setClean( plug )
			
			
		
		
	
	





def initializePlugin(mobject):
	mplugin = OpenMayaMPx.MFnPlugin(mobject, "Hans Godard -- zapan669@hotmail.com", "1.0", "Any")
	try:
		mplugin.registerNode( zapanSmoothDistance.kPluginNodeName, zapanSmoothDistance.kPluginNodeId, zapanSmoothDistance.nodeCreator, zapanSmoothDistance.nodeInitializer )
	except:
		sys.stderr.write( "Failed to register command: %s\n" % zapanSmoothDistance.kPluginNodeName )
		raise

def uninitializePlugin(mobject):
	mplugin = OpenMayaMPx.MFnPlugin(mobject)
	try:
		mplugin.deregisterNode( zapanSmoothDistance.kPluginNodeId )
	except:
		sys.stderr.write( "Failed to unregister node: %s\n" % zapanSmoothDistance.kPluginNodeName )
		raise
