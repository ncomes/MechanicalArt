__author__ = 'hgodard'


import math

from maya import OpenMaya, OpenMayaMPx, OpenMayaAnim


class DynamicSlide(OpenMayaMPx.MPxNode):
	kPluginNodeName = "dynamicSlide"
	kPluginNodeId = OpenMaya.MTypeId(0x0D1264)

	# epsilon
	e = 10e-06

	@staticmethod
	def same_sign(  f1, f2 ):
		return (True, False) [f1*f2<.0]

	@staticmethod
	def set_range( x, x0, x1, y0, y1 ) :
		y = 1.0*(  y0 + (x-x0)*(y1-y0)/(x1-x0)  )
		return y

	@staticmethod
	def extract_translate( m ):
		return [ m(3,i) for i in range(3)]
	
	@staticmethod
	def translate_to_FM( t ):
		valueList	= [ 1.0, .0, .0,.0 ,  .0, 1.0, .0, .0,  .0, .0, 1.0, .0,  t[0], t[1], t[2],1.0 ]
		outMat	= OpenMaya.MFloatMatrix()
		OpenMaya.MScriptUtil.createFloatMatrixFromList( valueList , outMat )
		return outMat
	
	@staticmethod
	def set_translate_to_FM( fm, t ):
		for i in range(3):
			OpenMaya.MScriptUtil.setFloatArray( fm[3], i, t[i]  )

	@staticmethod
	def MM_to_FM( mm ):
		valueList	= [
			mm(0,0),mm(0, 1),mm(0, 2),mm(0, 3),
			mm(1,0),mm(1, 1),mm(1, 2),mm(1, 3),
			mm(2,0),mm(2, 1),mm(2, 2),mm(2, 3),
			mm(3,0),mm(3, 1),mm(3, 2),mm(3, 3) ]
		outMat	= OpenMaya.MFloatMatrix()
		OpenMaya.MScriptUtil.createFloatMatrixFromList( valueList , outMat )
		return outMat
	
	@staticmethod
	def FM_to_MM( fm ):
		valueList	= [
			fm(0,0),fm(0, 1),fm(0, 2),fm(0, 3),
			fm(1,0),fm(1, 1),fm(1, 2),fm(1, 3),
			fm(2,0),fm(2, 1),fm(2, 2),fm(2, 3),
			fm(3,0),fm(3, 1),fm(3, 2),fm(3, 3) ]
		outMat	= OpenMaya.MMatrix()
		OpenMaya.MScriptUtil.createMatrixFromList( valueList , outMat )
		return outMat

	def slerp_FM( self, fm0, fm1, wgt, isRelative=False ) :
		
		mm0, mm1  = self.FM_to_MM(fm0), self.FM_to_MM(fm1)
		rel_Q		= OpenMaya.MTransformationMatrix( mm1 * mm0.inverse() ).rotation()
		slerp_Q		= self.slerp( OpenMaya.MQuaternion.identity, rel_Q, wgt )
		slerp_MM	= slerp_Q.asMatrix()
		
		if not isRelative :	slerp_MM *=  mm0
		
		return self.MM_to_FM( slerp_MM )

	@staticmethod
	def slerp( q1 , q2 , wgt  ):
		
		q1.normalizeIt()
		q2.normalizeIt()
		
		if q1.isEquivalent( q2 ) :
			return q1
		
		dot	= (q1.x * q2.x) + (q1.y * q2.y) + (q1.z * q2.z) +(q1.w * q2.w)
		
		if dot < 0.0 :
			q2.negateIt()
			dot	*= -1

		# lerp or slerp
		scale1	= 1.0-wgt
		scale2	= wgt
		
		if dot < 1.0 :
			theta	= math.acos( dot )
			sinTheta	= math.sin(theta)
			
			scale1	= math.sin( scale1 *theta) / sinTheta
			scale2	= math.sin( scale2 *theta) / sinTheta
		
		newValues		= [  scale1 * q1[k]  +  scale2 * q2[k]  for k in range(4) ]
		return OpenMaya.MQuaternion( newValues[0] , newValues[1], newValues[2], newValues[3])
	
	@staticmethod
	def get_rampValue(   rampAttr, rampPosition ):
		
		if rampAttr.getNumEntries():
			
			util		= OpenMaya.MScriptUtil()
			ptr		= util.asFloatPtr()
			rampAttr.getValueAtPosition( rampPosition ,  ptr )
			
			return util.getFloat( ptr )
		else :
			return .0

	@classmethod
	def nodeCreator(cls):
		return OpenMayaMPx.asMPxPtr(cls())
	
	@classmethod
	def nodeInitializer(cls):
		unitAttr		= OpenMaya.MFnUnitAttribute()
		matrixAttr		= OpenMaya.MFnMatrixAttribute()
		numAttr 		= OpenMaya.MFnNumericAttribute()
		rpAttr			= OpenMaya.MRampAttribute()
		enumAttr        = OpenMaya.MFnEnumAttribute()
		
		
		cls.inTime		= unitAttr.create(  "inTime", "t", OpenMaya.MFnUnitAttribute.kTime, 1.0)
		unitAttr.setKeyable( True )
		
		cls.inMatrix0	= matrixAttr.create( 'inMatrix0' ,'im0' , OpenMaya.MFnNumericData.kFloat )
		cls.inMatrix1	= matrixAttr.create( 'inMatrix1' ,'im1' , OpenMaya.MFnNumericData.kFloat )

		cls.gravity		= numAttr.create( "gravity", "gr", OpenMaya.MFnNumericData.kFloat, 9.8 )
		numAttr.setKeyable( True )
		numAttr.setMin( .0 )
		cls.gravityDirection	= numAttr.createPoint( "gravityDirection", "gd",  )
		numAttr.setDefault( .0, -1.0, .0)
		numAttr.setChannelBox( False )

		cls.mass	= numAttr.create( "mass", "ms", OpenMaya.MFnNumericData.kFloat, 1.0 )
		numAttr.setMin( cls.e )
		numAttr.setKeyable( True )
		
		cls.angularFriction	= numAttr.create( "angularFriction", "afc", OpenMaya.MFnNumericData.kFloat, .5 )
		numAttr.setMin( .0 )
		numAttr.setKeyable( True )
		cls.friction	= numAttr.create( "friction", "fc", OpenMaya.MFnNumericData.kFloat, 1.0 )
		numAttr.setMin( .0 )
		numAttr.setKeyable( True )
		
		cls.bounceWeight  = numAttr.create( "bounceWeight", "bw", OpenMaya.MFnNumericData.k2Float )
		numAttr.setDefault(.6, .6)
		numAttr.setMin( .0,.0 )
		#numAttr.setMax( 1.0,1.0 )
		numAttr.setKeyable( True )
		
		cls.distanceWeight	= numAttr.create( "distanceWeight", "dw", OpenMaya.MFnNumericData.kFloat, 1.0 )
		numAttr.setKeyable( True )
		numAttr.setMin( .0 )
		numAttr.setMax( 1.0 )
		
		cls.recoilWeight	= numAttr.create( "recoilWeight", "rw", OpenMaya.MFnNumericData.kFloat, 1.0 )
		numAttr.setMin( .0 )
		numAttr.setMax( 1.0 )
		
		cls.recoilMode      = enumAttr.create( 'recoilMode', 'rmd', 1 )
		enumAttr.addField( 'independant', 0 )
		enumAttr.addField( 'Recoil Weight   =   Distance Weight', 1 )

		cls.uRange  = numAttr.create( "uRange", "ur", OpenMaya.MFnNumericData.k2Float )
		numAttr.setDefault(.0, 1.0)
		
		cls.uBase	= numAttr.create( "uBase", "ubs", OpenMaya.MFnNumericData.kFloat, .0 )
		numAttr.setKeyable( True )
		
		cls.relativeMatrix	= matrixAttr.create( 'relativeMatrix' ,'rm' , OpenMaya.MFnNumericData.kFloat )

		cls.loop            = numAttr.create('loop','lp', OpenMaya.MFnNumericData.kBoolean, False)

		cls.globalWeight    = numAttr.create( "globalWeight", "gw", OpenMaya.MFnNumericData.kFloat, 1.0 )
		numAttr.setKeyable( True )
		numAttr.setMin( .0 )
		numAttr.setMax( 1.0 )

		# ramps
		cls.useGlobalWeightRamp	 = numAttr.create( 'useGlobalWeightRamp', 'ugwrp', OpenMaya.MFnNumericData.kBoolean, False )
		cls.globalWeightRamp	 = rpAttr.createCurveRamp( "globalWeightRamp", "gwrp" )
		
		cls.useMassRamp	 = numAttr.create( 'useMassRamp', 'umrp', OpenMaya.MFnNumericData.kBoolean, False )
		cls.massRamp	 = rpAttr.createCurveRamp( "massRamp", "mrp" )
		
		cls.useAngularFrictionRamp	 = numAttr.create( 'useAngularFrictionRamp', 'uafrp', OpenMaya.MFnNumericData.kBoolean, False )
		cls.angularFrictionRamp	     = rpAttr.createCurveRamp( "angularFrictionRamp", "afrp" )
		
		cls.useFrictionRamp	     = numAttr.create( 'useFrictionRamp', 'ufrp', OpenMaya.MFnNumericData.kBoolean, False )
		cls.frictionRamp	     = rpAttr.createCurveRamp( "frictionRamp", "frp" )
		
		cls.useDistanceWeightRamp	 = numAttr.create( 'useDistanceWeightRamp', 'udwrp', OpenMaya.MFnNumericData.kBoolean, False )
		cls.distanceWeightRamp	     = rpAttr.createCurveRamp( "distanceWeightRamp", "dwrp" )
		
		cls.useGravityRamp	= numAttr.create( 'useGravityRamp', 'ugrp', OpenMaya.MFnNumericData.kBoolean, False )
		cls.gravityRamp	    = rpAttr.createCurveRamp( "gravityRamp", "grp" )
		
		cls.useSlerp	    = numAttr.create( 'useSlerp', 'usl', OpenMaya.MFnNumericData.kBoolean, True )
		cls.slerpRamp       = rpAttr.createCurveRamp( "slerpRamp", "slrp" )

		# fake attribute
		cls.refreshStatic   = numAttr.create( 'refreshStatic', 'rfst', OpenMaya.MFnNumericData.kBoolean, False )
		numAttr.setHidden( True )

		#
		cls.outMatrix	= matrixAttr.create( 'outMatrix' ,'om' , OpenMaya.MFnNumericData.kFloat )
		matrixAttr.setWritable( False )
		
		cls.outU        = numAttr.create( "outU", "ou", OpenMaya.MFnNumericData.kFloat  )
		numAttr.setWritable( False )

		#
		for attr in (
					cls.inTime,
					cls.inMatrix0,
					cls.inMatrix1,
					cls.relativeMatrix,
					
					cls.uRange,
					cls.uBase,
					cls.loop,
					
					cls.globalWeight,
					cls.mass,
					cls.friction,
					cls.angularFriction,	
					cls.bounceWeight,
					
					cls.distanceWeight,
					cls.recoilWeight,
					cls.recoilMode,
					
					cls.gravity,
					cls.gravityDirection,
					
					cls.useGlobalWeightRamp,
					cls.globalWeightRamp,
					cls.useMassRamp,
					cls.massRamp,
					cls.useFrictionRamp,
					cls.frictionRamp,
					cls.useDistanceWeightRamp,
					cls.distanceWeightRamp,
					cls.useGravityRamp,
					cls.gravityRamp,
					cls.useAngularFrictionRamp,
					cls.angularFrictionRamp,
					
					cls.useSlerp,
					cls.slerpRamp,
					
					cls.refreshStatic,
					
					cls.outMatrix,
					cls.outU,
				):
			cls.addAttribute( attr )

		# static dependencies
		# used for optimization, if one of these attrs changes,
		# refreshStatic is dirtied so I can use it for getting all these attrs just in this case
		for attr in (
					cls.uRange,
					cls.uBase,
					cls.loop,
					
					cls.globalWeight,
					cls.mass,
					cls.bounceWeight,
					
					cls.friction,
					cls.distanceWeight,
					cls.recoilWeight,
					cls.recoilMode,
					
					cls.gravity,
					cls.angularFriction,	
					cls.gravityDirection,
					
					cls.useGlobalWeightRamp,
					cls.globalWeightRamp,
					cls.useMassRamp,
					cls.massRamp,
					cls.useFrictionRamp,
					cls.frictionRamp,
					cls.useDistanceWeightRamp,
					cls.distanceWeightRamp,
					cls.useGravityRamp,
					cls.gravityRamp,
					cls.useAngularFrictionRamp,
					cls.angularFrictionRamp,
					
					cls.useSlerp,
					cls.slerpRamp,
				):
			cls.attributeAffects( attr, cls.refreshStatic )

		# dynamic dependencies
		for attr in (
					cls.inTime,
					cls.inMatrix0,
					cls.inMatrix1,
					cls.relativeMatrix,
					cls.uRange,
					cls.uBase,
				):
			cls.attributeAffects( attr, cls.outMatrix )
			cls.attributeAffects( attr, cls.outU )

		#
		cls.init_AETemplate()

	@classmethod
	def init_AETemplate( cls  ):
		AE_cmd = '''
		
		global proc AE_[nodeType]_topAdditive( string $attrName )
		{   
			string $cl = `rowLayout -numberOfColumns 1 -adjustableColumn 1 `;
				
				picture -image ":/node/dynamicSlideAE.png" -p $cl;
			setParent..; // because I dont know what is the parent here
		}
		
		global proc AE_[nodeType]_updateNothing( string $attrName ) {}
		
		
		global proc AE[nodeType]Template( string $nodeName )
		{
		editorTemplate -callCustom "AE_[nodeType]_topAdditive" "AE_[nodeType]_updateNothing" "";
		
		editorTemplate -beginScrollLayout;
			editorTemplate -beginLayout "Matrix Attributes" -collapse 1;
				editorTemplate -addControl "inMatrix0";
				editorTemplate -addControl "inMatrix1";
				editorTemplate -addControl "relativeMatrix";
			editorTemplate -endLayout;
			
			editorTemplate -beginLayout "Solver Attributes" -collapse 0;
				editorTemplate -addControl "nodeState";
				editorTemplate -addControl "inTime";
				editorTemplate -addControl "uRange";
				editorTemplate -addControl "uBase";
				editorTemplate -addControl "loop";
				editorTemplate -addSeparator ;
				
				editorTemplate -addControl "globalWeight";
				editorTemplate -addControl "mass";
				editorTemplate -addControl "friction";
				editorTemplate -addControl "angularFriction";
				editorTemplate -addControl "bounceWeight";
				editorTemplate -addSeparator ;
				
				editorTemplate -addControl "distanceWeight";
				editorTemplate -addControl "recoilMode";
				editorTemplate -addControl "recoilWeight";
				editorTemplate -addSeparator ;
				
				editorTemplate -addControl "gravity";
				editorTemplate -addControl "gravityDirection";
			editorTemplate -endLayout;
			
			editorTemplate -beginLayout "Override Global Weight" -collapse 1;
				editorTemplate -addControl "useGlobalWeightRamp";
				AEaddRampControl "globalWeightRamp" ;
			editorTemplate -endLayout;
			
			editorTemplate -beginLayout "Override Mass" -collapse 1;
				editorTemplate -addControl "useMassRamp";
				AEaddRampControl "massRamp" ;
			editorTemplate -endLayout;
			
			editorTemplate -beginLayout "Override Friction" -collapse 1;
				editorTemplate -addControl "useFrictionRamp";
				AEaddRampControl "frictionRamp" ;
			editorTemplate -endLayout;
			
			editorTemplate -beginLayout "Override Angular Friction" -collapse 1;
				editorTemplate -addControl "useAngularFrictionRamp";
				AEaddRampControl "angularFrictionRamp" ;
			editorTemplate -endLayout;
			
			editorTemplate -beginLayout "Override Distance Weight" -collapse 1;
				editorTemplate -addControl "useDistanceWeightRamp";
				AEaddRampControl "distanceWeightRamp" ;
			editorTemplate -endLayout;
			
			editorTemplate -beginLayout "Override Gravity" -collapse 1;
				editorTemplate -addControl "useGravityRamp";
				AEaddRampControl "gravityRamp" ;
			editorTemplate -endLayout;
			
			editorTemplate -beginLayout "Parametric Rotation" -collapse 1;
				editorTemplate -addControl "useSlerp";
				AEaddRampControl "slerpRamp" ;
			editorTemplate -endLayout;
			
		editorTemplate -addExtraControls;
		editorTemplate -endScrollLayout;
		}
		'''.replace("[nodeType]", cls.kPluginNodeName )
		OpenMaya.MGlobal.executeCommand( AE_cmd )

	def __init__(self):
		OpenMayaMPx.MPxNode.__init__(self)
		
		self.initialized		= False

		# storage for the static input attrs :
		self.staticTmp  = {}
		self.staticData = {}

		#
		self.lastTime	= .0

		self.lastU      = .0
		self.lastU_vel  = .0
		
		self.lastU_pos  = [.0,.0,.0]
		self.last0_pos  = [.0,.0,.0]

	def get_posInfos(self, data):
		
		fm0       = data.inputValue(self.inMatrix0).asFloatMatrix()
		fm1       = data.inputValue(self.inMatrix1).asFloatMatrix()
		
		pos0      = self.extract_translate(fm0)
		pos1      = self.extract_translate(fm1)
		
		parametric_FV   = OpenMaya.MFloatVector( pos1[0]-pos0[0], pos1[1]-pos0[1], pos1[2]-pos0[2] )
		
		return pos0, parametric_FV, fm0, fm1

	def get_staticTmp(self, data ):
		"""Get Ramp objects or values directly"""
		
		thisObj		= self.thisMObject()

		if data.inputValue(self.useGlobalWeightRamp).asBool():
			self.staticTmp['globalWeight']    = OpenMaya.MRampAttribute( thisObj, self.globalWeightRamp )
		else :
			self.staticTmp['globalWeight']    = data.inputValue(self.globalWeight).asFloat()
			
		if data.inputValue(self.useMassRamp).asBool():
			self.staticTmp['m']     = OpenMaya.MRampAttribute( thisObj, self.massRamp )
		else :
			self.staticTmp['m']     = data.inputValue(self.mass).asFloat()
		
		if data.inputValue(self.useFrictionRamp).asBool():
			self.staticTmp['fr']    = OpenMaya.MRampAttribute( thisObj, self.frictionRamp )
		else :
			self.staticTmp['fr']    = data.inputValue(self.friction).asFloat()
		
		if data.inputValue(self.useAngularFrictionRamp).asBool():
			self.staticTmp['aFr']   = OpenMaya.MRampAttribute( thisObj, self.angularFrictionRamp )
		else :
			self.staticTmp['aFr']   = data.inputValue(self.angularFriction).asFloat()
		
		if data.inputValue(self.useDistanceWeightRamp).asBool():
			self.staticTmp['dw']    = OpenMaya.MRampAttribute( thisObj, self.distanceWeightRamp )
		else :
			self.staticTmp['dw']    = data.inputValue(self.distanceWeight).asFloat()
		
		if data.inputValue(self.useGravityRamp).asBool():
			self.staticTmp['g']     = OpenMaya.MRampAttribute( thisObj, self.gravityRamp )
		else :
			self.staticTmp['g']     = data.inputValue(self.gravity).asFloat()

	def staticTmp_to_staticData( self ):
		"""Copy value from staticTmp   or   eval it if it is a ramp
		the result go to staticData """
		
		
		u_to_01     = self.set_range( self.lastU, self.staticData['uStart'], self.staticData['uEnd'], .0, 1.0 )

		for attr in ('globalWeight', 'm', 'fr', 'dw', 'g', 'aFr'):
			
			if isinstance(self.staticTmp[attr], float):
				self.staticData[attr] = self.staticTmp[attr]
			else :
				# ramp  so  get value
				self.staticData[attr] = self.get_rampValue(  self.staticTmp[attr], u_to_01 )

	def get_staticData(self, data):

		# store values or rampObjects
		self.get_staticTmp( data  )

		#
		uStart, uEnd    = data.inputValue(self.uRange).asFloat2()
		
		
		fr0, fr1        = data.inputValue(self.bounceWeight).asFloat2()
		
		#
		dw      = data.inputValue( self.distanceWeight ).asFloat()
		
		recoilMode      = data.inputValue( self.recoilMode ).asInt()
		
		if recoilMode==1:  rw   = float( dw )
		else :             rw   = data.inputValue( self.recoilWeight ).asFloat()
		
		#
		self.staticData    = { 'uStart':    uStart,
		                       'uEnd':      uEnd,
		                       
		                       'fr0':       fr0,
		                       'fr1':       fr1,
		                       
		                       'dw':        dw,
		                       'rw':        rw,
		                       
		                       'loop':      data.inputValue(self.loop).asBool(),
		                       }
		#
		data.outputValue( self.refreshStatic ).setClean()
	
	def get_moveFV(self, pos0, parametric_FV, newU ):
		
		oldUpos     = tuple(self.lastU_pos)
		newUpos     = self.pos_from_U( pos0, parametric_FV, newU )
		
		move_FV     = OpenMaya.MFloatVector(  newUpos[0]- oldUpos[0], newUpos[1]- oldUpos[1], newUpos[2]- oldUpos[2]  )
		d           = abs( move_FV.length() )
		
		if d<self.e :
			return .0, .0, 1.0
		else :
			move_FVn        = move_FV.normal()
			parametric_FVn  = parametric_FV.normal()
			
			dotMove         = move_FVn * parametric_FVn
			
			normale_FVn     = (parametric_FVn ^ move_FVn) ^ parametric_FVn
			dotFrMove       = normale_FVn * move_FVn
			
			return dotMove, d, dotFrMove

	def pos_from_U(self, pos0, parametric_FV, u ):
		# p(u) = p0 + u*vec(p1-p0)
		x   = pos0[0] + u * parametric_FV.x
		y   = pos0[1] + u * parametric_FV.y
		z   = pos0[2] + u * parametric_FV.z
		
		return x,y,z

	def get_slerpFM(self, uStart, uEnd, fm0, fm1 ):
		
		ramp_wgt    = self.set_range( self.lastU, uStart, uEnd, .0, 1.0 )
		
		slerp_Rp    = OpenMaya.MRampAttribute( self.thisMObject(), self.slerpRamp )
		slerp_wgt   = self.get_rampValue(  slerp_Rp, ramp_wgt )
			
		slerp_FM    = self.slerp_FM(  fm0, fm1, slerp_wgt, isRelative=False )
		
		return slerp_FM

	def set_output(self, data, pos0, parametric_FV, fm0, fm1  ):

		# pos,  rot   and merge
		pos         = self.pos_from_U(  pos0, parametric_FV, self.lastU )
		
		rel_FM      = data.inputValue(self.relativeMatrix).asFloatMatrix()

		# slerp or not
		if data.inputValue(self.useSlerp).asBool():
			
			out_FM      = self.get_slerpFM( self.staticData['uStart'], self.staticData['uEnd'], fm0, fm1 )
			
			self.set_translate_to_FM( out_FM, pos )
			
			out_FM      = out_FM * rel_FM
		
		else :
			out_FM      = self.translate_to_FM( pos )
			
			out_FM      = out_FM * rel_FM
			
			# out_FM = only translate
			out_FM      = self.translate_to_FM( self.extract_translate( out_FM ) )

		#
		outMatrix_H     = data.outputValue(self.outMatrix)
		outMatrix_H.setMFloatMatrix( out_FM )
		outMatrix_H.setClean()
		
		outU_H          = data.outputValue(self.outU)
		outU_H.setFloat( self.lastU )
		outU_H.setClean()

	def reset(self, data):
		
		#
		self.lastU      = data.inputValue(self.uBase).asFloat()
		
		if self.lastU < self.staticData['uStart'] : self.lastU = self.staticData['uStart']
		elif self.lastU > self.staticData['uEnd'] : self.lastU = self.staticData['uEnd']

		#
		self.lastU_vel  = .0
		self.isBlocked  = False

		#
		pos0, parametric_FV, fm0, fm1   = self.get_posInfos( data )
		
		self.lastU_pos  = self.pos_from_U(  pos0, parametric_FV, self.lastU )
		self.last0_pos  = self.extract_translate( data.inputValue(self.inMatrix0).asFloatMatrix())

		self.set_output( data, pos0, parametric_FV, fm0, fm1 )

	def compute(self, plug, data):

		if plug not in (self.outMatrix,self.outU) :
			return

		if not data.isClean( self.refreshStatic ):
			self.get_staticData( data )

		# get_and_update time,  or reset
		currentTime	    = data.inputValue( self.inTime ).asTime().value()
		startTime		= OpenMayaAnim.MAnimControl.minTime().value()
		nodeState       = data.inputValue( self.state).asInt()
		
		if (currentTime <= startTime)  or  (nodeState==1)  or  (not self.initialized) :
			
			self.lastTime	= startTime
			
			self.reset( data )
			
			self.initialized	= True
			return

		dt		        = currentTime - self.lastTime
		self.lastTime	= currentTime
		
		# some static may be Ramps,  so rampObjects are stored in staticTmp
		# just evaluate them if they are ramps  and put the result in staticData
		self.staticTmp_to_staticData()

		# Build DYNAMIC DATA
		pos0, parametric_FV, fm0, fm1   = self.get_posInfos( data)

		# gravity data
		# g is static BUT  it must be multiplied by globalWeight  so  there is also g in dynamicData
		gravity_FVn     = data.inputValue( self.gravityDirection ).asFloatVector().normal()
		
		
		parametric_FVn  = parametric_FV.normal()
		normale_FVn     = (parametric_FVn ^ gravity_FVn) ^ parametric_FVn
		
		dotGrav         = parametric_FVn * gravity_FVn
		dotFrGrav       = normale_FVn * gravity_FVn
		
		g     = self.staticData['g'] * self.staticData['globalWeight']

		# move data
		# weight the move amplitudes by globalWeight
		dotMove, d, dotFrMove      = self.get_moveFV( pos0, parametric_FV, self.lastU )
		
		d     *= self.staticData['globalWeight']

		# all is normalized for the moment, divide all the dots by the length of the segment
		# so the result on a short segment and a long are visually the same
		length      = parametric_FV.length()
		
		dotGrav     /= length
		dotFrGrav   /= length
		dotMove     /= length
		dotFrMove   /= length

		# update
		dynData    = { 'dt':        dt,
		               
		               'dotGrav':   dotGrav,
		               'dotMove':   dotMove,
		               'd':         d,
		               'dotFrGrav': dotFrGrav,
		               'dotFrMove': dotFrMove,
		               
		               'g':         g,
		               }
		
		self.apply_rk4(  dynData )

		self.lastU_pos  = self.pos_from_U( pos0, parametric_FV, self.lastU  )
		self.last0_pos  = pos0

		# set output
		self.set_output( data,
		                 pos0, parametric_FV,
		                 fm0, fm1  )

	def apply_rk4(self, dynData ):

		#** store U before fake
		oldU        = float(self.lastU)

		# compute force amplitudes, using angleFriction
		# which are independant of the pos/vel  so compute them here
		dynData['forceMove']  = self.get_forceAmplitude(  dynData['dotMove'], dynData['d'], dynData['dotFrMove'], self.staticData['aFr'] )
		dynData['forceGrav']  = self.get_forceAmplitude(  dynData['dotGrav'], dynData['g'], dynData['dotFrGrav'], self.staticData['aFr'] )

		# weight the forceMove to remove   with  recoilWgt
		# then weight the forceMove to add with distanceWgt
		# this is useful because we can simulate and weight how much is parented the output to the inputs
		# example if recoilWgt=1 and distanceWgt=0  only the collisions affect the system
		self.lastU    -= self.staticData['rw'] * dynData['forceMove']
		
		dynData['forceMove']  *= self.staticData['dw']

		# do it
		self.lastU, self.lastU_vel    = self.rk4(  self.lastU, self.lastU_vel,  self.get_acc_, dynData   )

		#** limit to borders   and  set collision restitution
		reelVel     = self.lastU - oldU
		deltaVel    = reelVel - self.lastU_vel

		if self.lastU < self.staticData['uStart'] + self.e :
			
			if self.staticData['loop']:
				# LOOP  so  no collision
				self.lastU      = self.staticData['uEnd']
			else :
				# COLLISION
				self.lastU      = self.staticData['uStart']
				
				# precision problem  if fr0==.0  we still have a little bound ! ----> BAD
				# if fr0==.0    self.lastU_vel = .0 - deltaVel    != .0
				# so fake it :
				if self.staticData['fr0']==.0:
					# just conserve velocity
					pass
				else :
					# negate and weight the reelVel  then remove the fixed deltaVel to obtain self.lastU_vel
					new_reelVel       = -self.staticData['fr0']  *  reelVel
					self.lastU_vel    = new_reelVel - deltaVel
		
		elif self.lastU > self.staticData['uEnd'] - self.e :
			if self.staticData['loop']:
				self.lastU  = self.staticData['uStart']
			else :
				self.lastU     = self.staticData['uEnd']
				if self.staticData['fr1']==.0:
					pass
				else :
					new_reelVel       = -self.staticData['fr1']  * reelVel
					self.lastU_vel    = new_reelVel - deltaVel
	
	def get_forceAmplitude(self, dotGrav, g, dotFrGrav, gFr ):
		"""If the friction*dotFr > abs( dot )  return .0 """
		
		if gFr*dotFrGrav > abs(dotGrav) :
			return .0
		else :
			# dotFr always >=0
			# set it the opposite sign of dot
			dotFrGrav   = self.adapt_sign( dotGrav, dotFrGrav  )
			return  g* ( dotGrav  +  gFr*dotFrGrav )
	
	def adapt_sign(self, f1, f2):
		
		if   f1 >.0  : return -f2
		elif f1 <=.0 : return f2
	
	def get_acc_(self, x, v, dynData ):
		"""
		forceGrav      = dynData['forceGrav']
		forceMove      = dynData['forceMove']
		
		
		# acc_move is a delta of velocity
		# forceMove    = newVel  -  fr* oldVel 
		forceMove      = dynData['d'] * dynData['dotMove']  -  self.staticData['fr'] * v
		
		# forceSum     = m*a
		forceSum       = forceGrav + forceMove  
		return forceSum  /self.staticData['m']
		"""

		# the damp is the ratio of the oldVel we remove  (=fr*v)
		# we can set fr>1  but  we must be careful,  it cant negate the forceSum   otherwise return .0
		A       = dynData['forceGrav'] + dynData['forceMove']
		B       = self.staticData['fr'] * v
		
		if not self.same_sign(  A, A-B ) :
			# if B change the sign between  A and A-B   it changes the forceSum sign   so BAD
			return .0
			
		else :
			# forceSum     = m*a
			return (A-B) / self.staticData['m']

	def rk4(self, x, v, fonc, dynData  ):
		
		x1  = x
		v1  = v
		a1  = fonc(x1, v1, dynData )
		
		x2  = x + 0.5*v1*dynData['dt']
		v2  = v + 0.5*a1*dynData['dt']
		a2  = fonc(x2, v2, dynData )
		
		x3  = x + 0.5*v2*dynData['dt']
		v3  = v + 0.5*a2*dynData['dt']
		a3  = fonc(x3, v3, dynData )
		
		x4  = x + v3*dynData['dt']
		v4  = v + a3*dynData['dt']
		a4  = fonc(x4, v4, dynData )
		
		xf  = x + (v1 + 2.0*v2 + 2.0*v3 + v4) *dynData['dt']/6.0
		vf  = v + (a1 + 2.0*a2 + 2.0*a3 + a4) *dynData['dt']/6.0
		
		return xf, vf


def initializePlugin(mobject):
	mplugin = OpenMayaMPx.MFnPlugin(mobject, "Hans Godard, zapan669@hotmail.com", "1.0", "Any")
	try:
		mplugin.registerNode(DynamicSlide.kPluginNodeName, DynamicSlide.kPluginNodeId, DynamicSlide.nodeCreator, DynamicSlide.nodeInitializer)
	except:
		OpenMaya.MGlobal.displayError("Failed to register command: %s\n" % DynamicSlide.kPluginNodeName)
		raise


def uninitializePlugin(mobject):
	mplugin = OpenMayaMPx.MFnPlugin(mobject)
	try:
		mplugin.deregisterNode(DynamicSlide.kPluginNodeId)
	except:
		OpenMaya.MGlobal.displayError("Failed to unregister node: %s\n" % DynamicSlide.kPluginNodeName)
		raise
