__author__ = 'Hans Godard'



import math

from maya import OpenMaya, OpenMayaMPx, OpenMayaAnim






class DynamicConstraint( OpenMayaMPx.MPxConstraint ):
	
	kPluginNodeName     = "hgDynamicConstraint" 	# "dynamicConstraint" already used by Maya
	kPluginNodeId       = OpenMaya.MTypeId(0x0D6845)
	
	
	# epsilon
	e = 10e-06
	
	
	
	@classmethod
	def nodeCreator(cls):
		return OpenMayaMPx.asMPxPtr(cls())
	
	
	
	@classmethod
	def nodeInitializer( cls ):
		unitAttr		= OpenMaya.MFnUnitAttribute()
		numAttr		    = OpenMaya.MFnNumericAttribute()
		matrixAttr	    = OpenMaya.MFnMatrixAttribute()
		compAttr        = OpenMaya.MFnCompoundAttribute()
		enumAttr		= OpenMaya.MFnEnumAttribute()
		
		
		# inputs :
		cls.weight		    = numAttr.create( "weight", "wgt", OpenMaya.MFnNumericData.kFloat, 1.0 )
		numAttr.setKeyable( True )
		numAttr.setMin( .0 )
		numAttr.setMax( 1.0 )
		
		cls.inTime		    = unitAttr.create(  "inTime", "ti", OpenMaya.MFnUnitAttribute.kTime, 1.0)
		unitAttr.setKeyable( True )
		
		cls.inMatrix        = matrixAttr.create( "inMatrix", "inm", OpenMaya.MFnNumericData.kFloat )
		
		cls.relativeMatrix  = matrixAttr.create( "relativeMatrix", "rm", OpenMaya.MFnNumericData.kFloat )
		
		cls.offsetMatrix    = matrixAttr.create( "offsetMatrix", "ofm", OpenMaya.MFnNumericData.kFloat )
		
		
		# solver attrs
		cls.mass		= numAttr.create( "mass", "ma", OpenMaya.MFnNumericData.kFloat, 1.0 )
		numAttr.setKeyable( True )
		numAttr.setMin( .0 )
		
		cls.stiffness	= numAttr.create( "stiffness", "st",  OpenMaya.MFnNumericData.kFloat, .5 )
		numAttr.setKeyable( True )
		numAttr.setMin( .0 )
		numAttr.setMax( 2.0 )
		
		cls.damping	    = numAttr.create( "damping", "dp", OpenMaya.MFnNumericData.kFloat, .5 )
		numAttr.setKeyable( True )
		numAttr.setMin( .0 )
		numAttr.setMax( 1.0 )
		
		
		
		# compute what ? compute what ?!
		cls.solveTranslateX	= numAttr.create( "solveTranslateX", "stx", OpenMaya.MFnNumericData.kBoolean,True )
		numAttr.setKeyable( True )
		cls.solveTranslateY	= numAttr.create( "solveTranslateY", "sty", OpenMaya.MFnNumericData.kBoolean,True )
		numAttr.setKeyable( True )
		cls.solveTranslateZ	= numAttr.create( "solveTranslateZ", "stz", OpenMaya.MFnNumericData.kBoolean,True )
		numAttr.setKeyable( True )
		
		cls.solveRotateX	= numAttr.create( "solveRotateX", "srx", OpenMaya.MFnNumericData.kBoolean,True )
		numAttr.setKeyable( True )
		cls.solveRotateY	= numAttr.create( "solveRotateY", "sry", OpenMaya.MFnNumericData.kBoolean,True )
		numAttr.setKeyable( True )
		cls.solveRotateZ	= numAttr.create( "solveRotateZ", "srz", OpenMaya.MFnNumericData.kBoolean,True )
		numAttr.setKeyable( True )
		
		cls.solveScaleX	= numAttr.create( "solveScaleX", "ssx", OpenMaya.MFnNumericData.kBoolean,True )
		numAttr.setKeyable( True )
		cls.solveScaleY	= numAttr.create( "solveScaleY", "ssy", OpenMaya.MFnNumericData.kBoolean,True )
		numAttr.setKeyable( True )
		cls.solveScaleZ	= numAttr.create( "solveScaleZ", "ssz", OpenMaya.MFnNumericData.kBoolean,True )
		numAttr.setKeyable( True )
		
		
		
		
		# distance max smooth
		cls.limitDistance	= numAttr.create( "limitDistance" , "ld" , OpenMaya.MFnNumericData.kFloat , .0)
		numAttr.setKeyable(True)
		numAttr.setMin( .0 )
		numAttr.setMax( 1.0 )
		
		cls.distanceMax	    = numAttr.create( "distanceMax" , "dm" , OpenMaya.MFnNumericData.kFloat , 3.0)
		numAttr.setKeyable(True)
		numAttr.setMin( .0 )
		
		cls.smoothPercent	= numAttr.create( "smoothPercent" , "smp" , OpenMaya.MFnNumericData.kFloat , 1.0)
		numAttr.setKeyable(True)
		numAttr.setMin( .0 )
		numAttr.setMax( 1.0 )
		
		
		
		
		# output :
		cls.outMatrix	= matrixAttr.create( "outMatrix", "om", OpenMaya.MFnNumericData.kFloat )
		matrixAttr.setWritable( False )
		matrixAttr.setStorable(False )
		
		
		# decomposition
		cls.outJointOrientX  = unitAttr.create(  "outJointOrientX", "ojox", OpenMaya.MFnUnitAttribute.kAngle, .0)
		cls.outJointOrientY  = unitAttr.create(  "outJointOrientY", "ojoy", OpenMaya.MFnUnitAttribute.kAngle, .0)
		cls.outJointOrientZ  = unitAttr.create(  "outJointOrientZ", "ojoz", OpenMaya.MFnUnitAttribute.kAngle, .0)
		cls.outJointOrient   = compAttr.create( "outJointOrient" , "ojo")
		compAttr.addChild( cls.outJointOrientX )
		compAttr.addChild( cls.outJointOrientY )
		compAttr.addChild( cls.outJointOrientZ )
		
		cls.outTranslate    = numAttr.createPoint( "outTranslate", "ot",  )
		numAttr.setWritable( False )
		
		cls.outScale        = numAttr.createPoint( "outScale", "os",  )
		numAttr.setDefault( 1.0,1.0,1.0)
		numAttr.setWritable( False )
		
		cls.outRotateOrder  = enumAttr.create( "outRotateOrder", "oro", 6)
		for k,item in enumerate( ("xyz","yzx","zyx","xzy","yxz","zyx", "None") ):
			enumAttr.addField( item , k )
			
		cls.outRotateX      = unitAttr.create(  "outRotateX", "orx", OpenMaya.MFnUnitAttribute.kAngle, .0)
		unitAttr.setWritable( False )
		cls.outRotateY      = unitAttr.create(  "outRotateY", "ory", OpenMaya.MFnUnitAttribute.kAngle, .0)
		unitAttr.setWritable( False )
		cls.outRotateZ      = unitAttr.create(  "outRotateZ", "orz", OpenMaya.MFnUnitAttribute.kAngle, .0)
		unitAttr.setWritable( False )
		cls.outRotate       = compAttr.create( "outRotate" , "or")
		compAttr.addChild( cls.outRotateX )
		compAttr.addChild( cls.outRotateY )
		compAttr.addChild( cls.outRotateZ )
		compAttr.setWritable( False )
		
		
		
		
		
		
		# add + affect :
		for attr in (
				cls.inTime,
				cls.weight,
				cls.inMatrix,
				cls.mass,
				cls.stiffness,
				cls.damping,
				cls.solveTranslateX, cls.solveTranslateY, cls.solveTranslateZ,
				cls.solveRotateX, cls.solveRotateY, cls.solveRotateZ,
				cls.solveScaleX, cls.solveScaleY, cls.solveScaleZ,
				cls.limitDistance, cls.distanceMax, cls.smoothPercent,
				cls.relativeMatrix,
				cls.offsetMatrix,
					
				cls.outMatrix,
				cls.outTranslate,
				cls.outScale,
				cls.outRotate,
				cls.outRotateOrder,
				cls.outJointOrient,
				) :
			cls.addAttribute( attr )
		
		for attr in (
				cls.inTime,
				cls.inMatrix,
				cls.weight,
				cls.solveTranslateX, cls.solveTranslateY, cls.solveTranslateZ,
				cls.solveRotateX, cls.solveRotateY, cls.solveRotateZ,
				cls.solveScaleX, cls.solveScaleY, cls.solveScaleZ,
				cls.relativeMatrix,
				cls.offsetMatrix,
				cls.outRotateOrder,
				cls.outJointOrient,
				) :
			cls.attributeAffects( attr, cls.outMatrix )
			cls.attributeAffects( attr, cls.outTranslate )
			cls.attributeAffects( attr, cls.outRotate )
			cls.attributeAffects( attr, cls.outRotateX )
			cls.attributeAffects( attr, cls.outRotateY )
			cls.attributeAffects( attr, cls.outRotateZ )
			cls.attributeAffects( attr, cls.outScale )
		
		
		#
		cls.init_AETemplate()
		
		
	@classmethod
	def init_AETemplate( cls  ):
		AE_cmd = '''
		
		global proc AE_[nodeType]_topAdditive( string $attrName )
		{   
			string $cl = `rowLayout -numberOfColumns 1 -adjustableColumn 1 `;
				picture -image ":/node/[nodeType]AE.png" -p $cl;
			setParent..; // because I dont know what is the parent here
		}
		
		global proc AE_[nodeType]_updateNothing( string $attrName ) {}
		
		
		global proc AE[nodeType]Template( string $nodeName )
		{
		editorTemplate -callCustom "AE_[nodeType]_topAdditive" "AE_[nodeType]_updateNothing" "";
		
		editorTemplate -beginScrollLayout;
			
			editorTemplate -beginLayout "Choose what to solve" -collapse 1;
				editorTemplate -addControl "solveTranslateX";
				editorTemplate -addSeparator ;
				editorTemplate -addControl "solveTranslateY";
				editorTemplate -addSeparator ;
				editorTemplate -addControl "solveTranslateZ";
				editorTemplate -addSeparator ;
				editorTemplate -addControl "solveRotateX";
				editorTemplate -addSeparator ;
				editorTemplate -addControl "solveRotateY";
				editorTemplate -addSeparator ;
				editorTemplate -addControl "solveRotateZ";
				editorTemplate -addSeparator ;
				editorTemplate -addControl "solveScaleX";
				editorTemplate -addSeparator ;
				editorTemplate -addControl "solveScaleY";
				editorTemplate -addSeparator ;
				editorTemplate -addControl "solveScaleZ";
			editorTemplate -endLayout;
			
			editorTemplate -beginLayout "Solver Attributes" -collapse 0;
				editorTemplate -addControl "inTime";
				editorTemplate -addSeparator ;
				
				editorTemplate -addControl "weight";
				editorTemplate -addSeparator ;
				
				editorTemplate -addControl "mass";
				editorTemplate -addControl "stiffness";
				editorTemplate -addControl "damping";
			editorTemplate -endLayout;
			
			editorTemplate -beginLayout "Limit Distance Attributes" -collapse 1;
				editorTemplate -addControl "limitDistance";
				editorTemplate -addControl "distanceMax";
				editorTemplate -addControl "smoothPercent";
			editorTemplate -endLayout;
		
			editorTemplate -beginLayout "Matrix Attributes" -collapse 1;
				editorTemplate -addControl "inMatrix";
				editorTemplate -addControl "relativeMatrix";
				editorTemplate -addControl "offsetMatrix";
			editorTemplate -endLayout;
		
		editorTemplate -addExtraControls;
		editorTemplate -endScrollLayout;
		}
		'''.replace("[nodeType]", cls.kPluginNodeName )
		OpenMaya.MGlobal.executeCommand( AE_cmd )
	
	
	@classmethod
	def isPassiveOutput(cls, plug):
		return True
	
	
	
	
	
	def __init__(self):
		OpenMayaMPx.MPxConstraint.__init__(self)
		
		self.initialized    = False
		
		self.lastTime	    = .0
		
		self.massValue	    = .0
		self.stiffValue	    = .0
		self.dampValue	    = .0
		
		#
		self.lastTranslate	= [.0,.0,.0 ]
		self.lastScale	    = [.0,.0,.0 ]
		self.lastQuat	    = [.0,.0,.0,1.0]
		
		self.lastTranslateVel   = [.0,.0,.0 ]
		self.lastScaleVel	    = [.0,.0,.0 ]
		self.lastQuatVel	    = [.0,.0,.0,.0 ]
		
	
		
	def reset_pos_vel( self, inTranslate=None, inQuat=None, inScale=None  ) :
		
		if inTranslate:
			self.lastTranslate      = [inTranslate[0], inTranslate[1], inTranslate[2]]
			self.lastTranslateVel   = [.0,.0,.0 ]
		if inScale:
			self.lastScale		= [inScale[0], inScale[1], inScale[2]]
			self.lastScaleVel	= [.0,.0,.0 ]
		if inQuat:
			#self.lastQuat	    = list( inQuat ) # -> CRASH
			self.lastQuat		= [inQuat[0], inQuat[1], inQuat[2], inQuat[3]]
			self.lastQuatVel	= [.0,.0,.0,.0 ]
	
	
	def get_inComponents( self, data ):
		
		in_FM   = data.inputValue( self.inMatrix ).asFloatMatrix()
		in_Tr	= OpenMaya.MTransformationMatrix( self.FM_to_MM(  in_FM  ) )
		
		t	    = in_Tr.getTranslation( OpenMaya.MSpace.kTransform )
		q		= in_Tr.rotation()
		s		= self.getScale(  in_Tr, OpenMaya.MSpace.kTransform  )
		
		return in_FM, [t[0],t[1],t[2]], [q[0],q[1],q[2],q[3]], s
	
	
	
	
	def compute( self, plug, data  ) :
		
		
		if plug not in (self.outMatrix,
		                self.outTranslate,
		                self.outScale,
		                self.outRotate,self.outRotateX,self.outRotateY,self.outRotateZ ) :
			return
		
		
		
		nodeState       = data.inputValue( self.state).asInt()
		if nodeState == 1 :
			return
		
		
		
		
		#
		in_wFM, inTranslate, inQuat, inScale	= self.get_inComponents( data )
		
		in_Q            = OpenMaya.MQuaternion( inQuat[0],inQuat[1],inQuat[2],inQuat[3]  )
		
		currentTime	    = data.inputValue( self.inTime ).asTime().value()
		startTime		= OpenMayaAnim.MAnimControl.minTime().value()
		
		
		if not self.initialized :
			self.lastTime       = currentTime
			self.reset_pos_vel( inTranslate=inTranslate, inScale=inScale, inQuat=inQuat  )
			self.set_output(  data, plug, inTranslate, in_Q, inScale )
			self.initialized	= True
			return
		
		
		if currentTime <= startTime :
			self.lastTime   = startTime
			self.reset_pos_vel( inTranslate=inTranslate, inScale=inScale, inQuat=inQuat  )
			self.set_output(  data, plug, inTranslate, in_Q, inScale )
			return
		
		
		
		
		# limit deltaTime to one frame
		deltaTime		= currentTime - self.lastTime
		
		if deltaTime > 1.0 :    deltaTime = 1.0
		elif deltaTime < -1.0 : deltaTime = -1.0
			
		self.lastTime   = currentTime
		
		
		
		#
		wgt     = data.inputValue( self.weight ).asFloat()
		
		if wgt < self.e :
			self.reset_pos_vel( inTranslate=inTranslate, inScale=inScale, inQuat=inQuat  )
			self.set_output(  data, plug, inTranslate, in_Q, inScale )
			return
		
		
		
		
		# check the  .dot(current,lastQuat)  to get the reel shortestPath
		dot     = self.lastQuat[0]*in_Q[0] + self.lastQuat[1]*in_Q[1] + self.lastQuat[2]*in_Q[2] + self.lastQuat[3]*in_Q[3]
		
		if dot < 0.0 :
			in_Q.negateIt()
			dot     *= -1.0
			inQuat  = [in_Q[0],in_Q[1],in_Q[2],in_Q[3]]
		
		
		
		
		
		# RK
		self.massValue      = data.inputValue( self.mass ).asFloat()
		if self.massValue < self.e :
			self.massValue      = self.e
		
		self.stiffValue     = data.inputValue( self.stiffness ).asFloat()
		if self.stiffValue < self.e :
			self.stiffValue     = self.e
		
		self.dampValue		= data.inputValue( self.damping ).asFloat()
		
		
		frameIter   = 1.0
		h           = deltaTime / frameIter
		
		
		
		
		# TRANSLATE
		# rk
		# lock local axis
		# limit distance
		doTx    = data.inputValue( self.solveTranslateX ).asBool()
		doTy    = data.inputValue( self.solveTranslateY ).asBool()
		doTz    = data.inputValue( self.solveTranslateZ ).asBool()
		
		
		if doTx or doTy or doTz :
			
			self.rk( 0, inTranslate, self.lastTranslate, self.lastTranslateVel,  h )
			self.rk( 1, inTranslate, self.lastTranslate, self.lastTranslateVel,  h )
			self.rk( 2, inTranslate, self.lastTranslate, self.lastTranslateVel,  h )
			
			
			if (not doTx) or (not doTy) or (not doTz) :
				
				world_FV    = OpenMaya.MFloatVector(self.lastTranslate[0]-inTranslate[0], self.lastTranslate[1]-inTranslate[1],self.lastTranslate[2]-inTranslate[2])
				local_FV    = world_FV * in_wFM.inverse()
				
				local_FV.x  *= int(doTx)
				local_FV.y  *= int(doTy)
				local_FV.z  *= int(doTz)
				
				world_FV    = local_FV * in_wFM
				self.lastTranslate   = [ inTranslate[ii] + world_FV[ii]  for ii in xrange(3) ]
				
				
			limitWgt        = data.inputValue( self.limitDistance ).asFloat()
			if limitWgt >.0:
				self.lastTranslate  = self.get_translateMax( data, inTranslate, self.lastTranslate, limitWgt  )
		
		
		else :
			self.lastTranslate       = inTranslate
			self.lastTranslateVel    = [.0,.0,.0]
		
		
		
		
		# SCALE
		# rk
		doSx    = data.inputValue( self.solveScaleX ).asBool()
		doSy    = data.inputValue( self.solveScaleY ).asBool()
		doSz    = data.inputValue( self.solveScaleZ ).asBool()
		
		
		if doSx :
			self.rk( 0, inScale, self.lastScale, self.lastScaleVel,  h )
		else :
			self.lastScale[0]       = inScale[0]
			self.lastScaleVel[0]    = .0
		if doSy :
			self.rk( 1, inScale, self.lastScale, self.lastScaleVel,  h )
		else :
			self.lastScale[1]       = inScale[1]
			self.lastScaleVel[1]    = .0
		if doSz :
			self.rk( 2, inScale, self.lastScale, self.lastScaleVel,  h )
		else :
			self.lastScale[2]       = inScale[2]
			self.lastScaleVel[2]    = .0
			
			
		
		# ROTATION
		# lock axis
		# rk
		# normalize
		doRx    = data.inputValue( self.solveRotateX ).asBool()
		doRy    = data.inputValue( self.solveRotateY ).asBool()
		doRz    = data.inputValue( self.solveRotateZ ).asBool()
		
		
		if doRx or doRy or doRz :
			
			if (not doRx) or (not doRy) or (not doRz) :
				# if not all axes
				# fake lastQuat before RK
				last_Q      = OpenMaya.MQuaternion(self.lastQuat[0],self.lastQuat[1],self.lastQuat[2],self.lastQuat[3])
				transfo_Q   = last_Q * in_Q.inverse()
				
				axis_MV, angle_rad  = self.getAxisAngle( transfo_Q )
				axis_MV.x   *= int(doRx)
				axis_MV.y   *= int(doRy)
				axis_MV.z   *= int(doRz)
				axis_MV.normalize()
				transfo_Q.setAxisAngle( axis_MV, angle_rad )
				
				last_Q          = transfo_Q * in_Q
				# vel ? -> no need
				self.lastQuat   = [last_Q[0], last_Q[1], last_Q[2], last_Q[3]]
				
			
			self.rk( 0, inQuat, self.lastQuat, self.lastQuatVel,  h )
			self.rk( 1, inQuat, self.lastQuat, self.lastQuatVel,  h )
			self.rk( 2, inQuat, self.lastQuat, self.lastQuatVel,  h )
			self.rk( 3, inQuat, self.lastQuat, self.lastQuatVel,  h )
			
			out_Q   = OpenMaya.MQuaternion(self.lastQuat[0],self.lastQuat[1],self.lastQuat[2],self.lastQuat[3]).normal()
		
		else :
			out_Q               = in_Q
			self.lastQuatVel    = [.0,.0,.0,.0]
		
		
		self.lastQuat   = [out_Q.x, out_Q.y, out_Q.z, out_Q.w]
		
		
		
		
		# WEIGHT all  +  end
		if wgt != 1.0 :
			outTranslate    = [self.blend2( inTranslate[ii], self.lastTranslate[ii], wgt )  for ii in xrange(3)  ]
			outScale        = [self.blend2( inScale[ii], self.lastScale[ii], wgt )  for ii in xrange(3)  ]
			out_Q           = self.quick_slerp( in_Q, out_Q, wgt, dot )
			
		else :
			outTranslate    = self.lastTranslate
			outScale        = self.lastScale
			#out_Q          = out_Q
			
		
		
		self.set_output( data, plug, outTranslate, out_Q, outScale )
	
	
	
	
	
	
	def get_translateMax(self, data, rootPos, movePos, limitWgt ):
		
		
		
		smoothPercent   = data.inputValue( self.smoothPercent ).asFloat()
		if smoothPercent < self.e :
			smoothPercent   = self.e
			
			
			
		invDirection_FV = OpenMaya.MFloatVector( rootPos[0]-movePos[0], rootPos[1]-movePos[1], rootPos[2]-movePos[2] )
		dCurrent        = invDirection_FV.length()
		
		dMax            = data.inputValue( self.distanceMax ).asFloat()
		delta           = smoothPercent  * dMax
		dStart          = dMax - delta
		
		
		
		#
		if (dCurrent  >= dStart) and delta :
			dNew        = delta*(1.0-math.exp((dStart-dCurrent)/delta)) + dStart
		else :
			dNew        = dCurrent
		
		
		
		# weight basic
		dNew        = self.blend2( dCurrent, dNew, limitWgt )
		
		dInv        = dCurrent - dNew
		
		
		
		# final pos		=  movePos  +  ( direction.normalize * invDistance )
		invDirection_FV.normalize()
		outPos      = [	movePos[0]+invDirection_FV[0]*dInv,
						movePos[1]+invDirection_FV[1]*dInv,
						movePos[2]+invDirection_FV[2]*dInv  ]
		return outPos
	
	
	
	
	def rk( self, ii, newPos, lastPos, lastVel, h  ):
		
		deltaPos			= lastPos[ii] - newPos[ii]
			
		newDeltaPos, newVel	= self.rk4( deltaPos, lastVel[ii], h )
		lastVel[ii]			= newVel
		lastPos[ii]			= newPos[ii]  +  newDeltaPos
	
	def accel( self, x, v  ):
		# system [mass spring damper] :
		# critical damping  =  2m sqrt(k/m)    -------->   realDamp  =  ratio  *  2m sqrt(k/m)
		# m(a+g)  +  cv  +  kx  = 0    ---->  a = (-cv - kx) /m  +  g
		criticalDamp    = self.dampValue * 2.0 * self.massValue* math.sqrt( self.stiffValue/self.massValue  )
		
		return (-x*self.stiffValue - v*criticalDamp )/self.massValue
	
	def rk4(self, x, v, h ):
		
		x1	= v
		v1	= self.accel(x, x1)
		
		x2	= v + v1*h*.5
		v2	= self.accel(x + x1*h*.5, x2)
		
		x3	= v + v2*h*.5
		v3	= self.accel(x + x2*h*.5, x3)
		
		x4	= v + v3*h
		v4	= self.accel(x + x3*h, x4)
		
		newX		= x + (x1 + 2.0*x2 + 2.0*x3 + x4)*h/6.0
		newV		= v + (v1 + 2.0*v2 + 2.0*v3 + v4)*h/6.0
		return newX, newV
	
	
	
	
	@staticmethod
	def getAxisAngle(  q):
		axis    = OpenMaya.MVector()
		util    = OpenMaya.MScriptUtil()
		ptr     = util.asDoublePtr()
		q.getAxisAngle(axis,ptr)
		angle_rad   = util.getDouble(ptr)
		return axis, angle_rad
	
	@staticmethod
	def quick_slerp( q1 , q2 , t , dot ):
		
		if q1.isEquivalent( q2 ) :
			return q1
		
		scale1  = 1.0-t
		scale2  = t
		
		if dot < 1.0 :
			theta       = math.acos( dot )
			sinTheta    = math.sin(theta)
			scale1      = math.sin( scale1 *theta) / sinTheta
			scale2      = math.sin( scale2 *theta) / sinTheta
		
		newValues   = [ scale1*q1[kk] + scale2*q2[kk]   for kk in xrange(4) ]
		return OpenMaya.MQuaternion( newValues[0] , newValues[1], newValues[2], newValues[3])
	
	
	
	
	
	def set_output(self, data, plug, outTranslate, out_Q, outScale ):
		
		
		# scale is already local
		# Global scale does not make any sense to deal with
		out_FM, t, r_FM, s		= self.get_outMatrix( data,  outTranslate, out_Q, outScale )
		
		data.outputValue(  self.outMatrix ).setMFloatMatrix( out_FM )
		
		
		
		# set local T
		data.outputValue(  self.outTranslate ).set3Float( t[0], t[1], t[2] )
		
		
		
		# set local S
		data.outputValue(  self.outScale ).set3Float( s[0], s[1], s[2] )
		
		
		
		# decompose to euler
		euler		= OpenMaya.MTransformationMatrix( self.FM_to_MM( r_FM )  ).eulerRotation() # kXYZ
		ro          = data.inputValue(self.outRotateOrder).asInt()
		if ro not in (0,6):     euler.reorderIt(  ro  )
		
		data.outputValue(self.outRotateX).setMAngle( OpenMaya.MAngle(euler.x)  )
		data.outputValue(self.outRotateY).setMAngle( OpenMaya.MAngle(euler.y)  )
		data.outputValue(self.outRotateZ).setMAngle( OpenMaya.MAngle(euler.z)  )
		
		
		#
		data.setClean( plug )
	
	
	
	def get_outMatrix(self, data,  outTranslate, out_Q, outScale ):
		'''Build a clean matrix taking in account jointOrient '''
		
		relative_FM     = data.inputValue( self.relativeMatrix ).asFloatMatrix()
		offset_FM       = data.inputValue( self.offsetMatrix ).asFloatMatrix()
		
		
		# T
		t_world         = OpenMaya.MFloatPoint( outTranslate[0], outTranslate[1], outTranslate[2] )
		t_local         = t_world * relative_FM
		t_FM            = self.translate_to_FM( t_local )
		
		
		# R
		r_FM            = self.MM_to_FM(   out_Q.asMatrix()   )  # = world rotation
		
		jo_Euler        = self.get_Euler( data, (self.outJointOrientX, self.outJointOrientY, self.outJointOrientZ), None )
		jo_FM           = self.MM_to_FM(   jo_Euler.asMatrix()   )
		
		wParent_FM      = relative_FM.inverse()
		
		
		relative_rot_inv    = self.FM( f16=[    wParent_FM(0,0),wParent_FM(0,1),wParent_FM(0,2),.0,
												wParent_FM(1,0),wParent_FM(1,1),wParent_FM(1,2),.0,
												wParent_FM(2,0),wParent_FM(2,1),wParent_FM(2,2),.0,
												.0,.0,.0, 1.0, ] )
		
		jo_wFM          = jo_FM * relative_rot_inv
		deltaRot_FM     = r_FM * jo_wFM.inverse()
		
		
		# S
		scale_FM        = self.FM( f16=[    outScale[0], .0, .0, .0,
											.0, outScale[1], .0, .0 ,
											.0, .0, outScale[2], .0 ,
											.0, .0, .0, 1.0 ] )
		
		
		# final matrix
		# re-extract local data
		out_FM          = offset_FM   *  scale_FM  *  deltaRot_FM  *  t_FM
		
		t, r_FM, s      = self.decompose( out_FM )
		
		
		return out_FM, t, r_FM, s
		
	
	
	
	def decompose( self, out_FM ):
		
		t           = [out_FM(3,0), out_FM(3,1), out_FM(3,2)]
		
		out_Tr      = OpenMaya.MTransformationMatrix( self.FM_to_MM( out_FM)  )
		
		r_FM        = self.MM_to_FM( out_Tr.asRotateMatrix() )
		
		s           = self.getScale(  out_Tr, OpenMaya.MSpace.kTransform  )
		
		return t, r_FM, s
	
		
	
	
	
	@staticmethod
	def FM_to_MM( fm ):
		valueList = [
			fm(0,0),fm(0, 1),fm(0, 2),fm(0, 3),
			fm(1,0),fm(1, 1),fm(1, 2),fm(1, 3),
			fm(2,0),fm(2, 1),fm(2, 2),fm(2, 3),
			fm(3,0),fm(3, 1),fm(3, 2),fm(3, 3) ]
		outMat = OpenMaya.MMatrix()
		OpenMaya.MScriptUtil.createMatrixFromList( valueList , outMat )
		return outMat
	
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
	
	@staticmethod
	def translate_to_FM( t ):
		valueList   = [ 1.0, .0, .0,.0 ,  .0, 1.0, .0, .0,  .0, .0, 1.0, .0,  t[0], t[1], t[2],1.0 ]
		outMat      = OpenMaya.MFloatMatrix()
		OpenMaya.MScriptUtil.createFloatMatrixFromList( valueList , outMat )
		return outMat
	
	@staticmethod
	def FM( f16=[ 1.0,.0,.0,.0, .0,1.0,.0,.0, .0,.0,1.0,.0,  .0,.0,.0,1.0 ] ):
		outMat      = OpenMaya.MFloatMatrix()
		OpenMaya.MScriptUtil.createFloatMatrixFromList( f16 , outMat )
		return outMat
	
	
	@staticmethod
	def blend2( input1 , input2 , wgt ) :
		return (1.0-wgt)*input1 + wgt*input2
	
	@staticmethod
	def getScale( MTransfo, space=OpenMaya.MSpace.kTransform  ):
		scale_util	= OpenMaya.MScriptUtil()
		scale_util.createFromDouble(.0,.0,.0)
		scale_ptr	= scale_util.asDoublePtr()
		MTransfo.getScale( scale_ptr, space )
		inScale	= [ scale_util.getDoubleArrayItem(scale_ptr, i)  for i in xrange(3) ]
		return inScale
	
	
	
	@staticmethod
	def get_Euler( data, attrObjs, ro=None ):
		
		rx      = data.inputValue(attrObjs[0]).asAngle().value()
		ry      = data.inputValue(attrObjs[1]).asAngle().value()
		rz      = data.inputValue(attrObjs[2]).asAngle().value()
		
		euler   = OpenMaya.MEulerRotation( rx, ry, rz  )
		
		if ro != None :
			euler.reorderIt( ro )
			
		return euler
	
	




def initializePlugin(mobject):
	mplugin = OpenMayaMPx.MFnPlugin(mobject, "Hans Godard, zapan669@hotmail.com", "1.0", "Any")
	try:
		mplugin.registerNode(DynamicConstraint.kPluginNodeName, DynamicConstraint.kPluginNodeId, DynamicConstraint.nodeCreator,
		                     DynamicConstraint.nodeInitializer, OpenMayaMPx.MPxNode.kConstraintNode )
	except:
		OpenMaya.MGlobal.displayError("Failed to register node: %s\n" % DynamicConstraint.kPluginNodeName)
		raise


def uninitializePlugin(mobject):
	mplugin = OpenMayaMPx.MFnPlugin(mobject)
	try:
		mplugin.deregisterNode(DynamicConstraint.kPluginNodeId)
	except:
		OpenMaya.MGlobal.displayError("Failed to unregister node: %s\n" % DynamicConstraint.kPluginNodeName)
		raise




