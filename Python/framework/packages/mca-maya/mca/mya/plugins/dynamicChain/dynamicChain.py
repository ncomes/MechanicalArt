__author__ = 'Hans Godard'

import math
from maya import OpenMaya, OpenMayaMPx, OpenMayaAnim, OpenMayaRender

try:
	from Qt import QtWidgets, QtGui
except ModuleNotFoundError:
	from PySide2 import QtWidgets, QtGui


# epsilon
e = 10e-04

	
def get_3floats( plug ):
	numData	= OpenMaya.MFnNumericData(plug.asMObject())
	
	triple_util	= [OpenMaya.MScriptUtil() for i in range(3) ]
	triple_ptr	= [triple_util[i].asFloatPtr() for i in range(3)]
	numData.getData3Float( triple_ptr[0], triple_ptr[1], triple_ptr[2] )
	
	triple	= [ OpenMaya.MScriptUtil(triple_ptr[i]).asFloat() for i in range(3) ]
	return triple


def MM_to_FM( mm ):
	valueList	= [
		mm(0,0),mm(0, 1),mm(0, 2),mm(0, 3),
		mm(1,0),mm(1, 1),mm(1, 2),mm(1, 3),
		mm(2,0),mm(2, 1),mm(2, 2),mm(2, 3),
		mm(3,0),mm(3, 1),mm(3, 2),mm(3, 3) ]
	outMat	= OpenMaya.MFloatMatrix()
	OpenMaya.MScriptUtil.createFloatMatrixFromList( valueList , outMat )
	return outMat


def FM_to_MM( fm ):
	valueList	= [
		fm(0,0),fm(0, 1),fm(0, 2),fm(0, 3),
		fm(1,0),fm(1, 1),fm(1, 2),fm(1, 3),
		fm(2,0),fm(2, 1),fm(2, 2),fm(2, 3),
		fm(3,0),fm(3, 1),fm(3, 2),fm(3, 3) ]
	outMat	= OpenMaya.MMatrix()
	OpenMaya.MScriptUtil.createMatrixFromList( valueList , outMat )
	return outMat


def extract_translate( m ):
	t	= [ m(3,i) for i in range(3)]
	return t


def translate_to_FM( t ):
	valueList	= [ 1.0, .0, .0,.0 ,  .0, 1.0, .0, .0,  .0, .0, 1.0, .0,  t[0], t[1], t[2],1.0 ]
	outMat	= OpenMaya.MFloatMatrix()
	OpenMaya.MScriptUtil.createFloatMatrixFromList( valueList , outMat )
	return outMat


class DynamicChain(OpenMayaMPx.MPxNode):

	kPluginNodeName = "dynamicChain"
	kPluginNodeId = OpenMaya.MTypeId(0x0D1265)

	@staticmethod
	def blend2( input1 , input2 , wgt ) :
		return (1.0-wgt)*input1 + wgt*input2

	@staticmethod
	def set_range( x, x0, x1, y0, y1 ) :
		y = 1.0*(  y0 + (x-x0)*(y1-y0)/(x1-x0)  )
		return y

	@staticmethod
	def set_Euler_to_Handle3( handles3, euler ):
		for h,angle in zip( handles3, (euler.x,euler.y,euler.z) ) :
			h.setMAngle( OpenMaya.MAngle(angle)  )
	
	@staticmethod
	def set_translate_to_MM( mm, t ):
		for i in range(3):
			OpenMaya.MScriptUtil.setDoubleArray( mm[3], i, t[i]  )
	
	@staticmethod
	def set_translate_to_FM( fm, t ):
		for i in range(3):
			OpenMaya.MScriptUtil.setFloatArray( fm[3], i, t[i]  )

	@staticmethod
	def get_Euler( rotate_H, rotAttrObjs, ro=None ):
		
		rx      = rotate_H.child(rotAttrObjs[0]).asAngle().value()
		ry      = rotate_H.child(rotAttrObjs[1]).asAngle().value()
		rz      = rotate_H.child(rotAttrObjs[2]).asAngle().value()
		
		euler   = OpenMaya.MEulerRotation( rx, ry, rz  )
		
		if ro is not None :
			euler.reorderIt( ro )
			
		return euler

	@staticmethod
	def get_axisAngle( q ):
		mv			= OpenMaya.MVector()
		angle_util		= OpenMaya.MScriptUtil()
		angle_ptr		= angle_util.asDoublePtr()
		
		q.getAxisAngle( mv, angle_ptr  )
		
		angle_rad		= angle_util.getDouble(angle_ptr)
		
		return mv, angle_rad

	@staticmethod
	def slerp_MM(  mmBase, mmMove, wgt, isRelative=False ) :
		
		rel_Q		= OpenMaya.MTransformationMatrix( mmMove * mmBase.inverse() ).rotation()
		
		slerp_Q		= DynamicChain.slerp( OpenMaya.MQuaternion.identity, rel_Q, wgt )
		slerp_MM		= slerp_Q.asMatrix()
		
		if not isRelative :	slerp_MM *=  mmBase
		
		return slerp_MM

	@staticmethod
	def slerp( q1 , q2 , wgt  ):
		'''proc qui slerp entre 2 quaternions'''
		
		q1.normalizeIt()
		q2.normalizeIt()
		
		if q1.isEquivalent( q2 ) :
			return q1
		
		#if dot is None :
		dot	= (q1.x * q2.x) + (q1.y * q2.y) + (q1.z * q2.z) +(q1.w * q2.w)
		
		if dot < 0.0 :
			q2.negateIt()
			dot	*= -1

		# lerp ou slerp
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
	def nodeCreator( cls ):
		return OpenMayaMPx.asMPxPtr( cls() )

	@classmethod
	def nodeInitializer( cls ):
		numAttr 		= OpenMaya.MFnNumericAttribute()
		matrixAttr		= OpenMaya.MFnMatrixAttribute()
		unitAttr		= OpenMaya.MFnUnitAttribute()
		compAttr		= OpenMaya.MFnCompoundAttribute()
		rpAttr			= OpenMaya.MRampAttribute( )
		enumAttr		= OpenMaya.MFnEnumAttribute()
		
		
		cls.inTime		= unitAttr.create(  "inTime", "t", OpenMaya.MFnUnitAttribute.kTime, 1.0)
		unitAttr.setKeyable( True )
		
		# compute all from a startFrame  or  dynamically step by step
		# startFrame is only used when solverMode=1
		cls.solverMode	= enumAttr.create( "solverMode", "svm", 0)
		enumAttr.addField( "Once" , 0 )
		enumAttr.addField( "Iterate from StartTime" , 1 )
		
		cls.startTime		= unitAttr.create(  "startTime", "stm", OpenMaya.MFnUnitAttribute.kTime, 1.0)
		
		# add velocity or directly acceleration ( so when velocity is constant  nothing happens )
		cls.additionMode	= enumAttr.create( "additionMode", "adm", 0)
		enumAttr.addField( "Velocity" , 0 )
		enumAttr.addField( "Acceleration" , 1 )

		# rotationMode with 1 turns on the twist dynamic
		cls.rotationMode		= enumAttr.create( "rotationMode", "rtm", 1 )
		enumAttr.setKeyable( True )
		enumAttr.addField( "Aim", 0 )
		enumAttr.addField( "Aim and Up", 1 )
		
		#
		cls.aimWeight	= numAttr.create( 'aimWeight', 'aw', OpenMaya.MFnNumericData.kFloat, 1.0 )
		numAttr.setKeyable( True )
		numAttr.setMin( .0 )
		numAttr.setMax( 1.0 )
		
		cls.upWeight	= numAttr.create( 'upWeight', 'uw', OpenMaya.MFnNumericData.kFloat, 1.0 )
		numAttr.setKeyable( True )
		numAttr.setMin( .0 )
		numAttr.setMax( 1.0 )
		
		cls.upVector	= numAttr.createPoint( "upVector", "uv",  )
		numAttr.setDefault( .0, 1.0, .0)
		
		cls.mass			= numAttr.create( "mass", "ma", OpenMaya.MFnNumericData.kFloat, 1.0 )
		numAttr.setKeyable( True )
		numAttr.setMin( .0001 )
		cls.stiffness 		= numAttr.create( "stiffness", "s",  OpenMaya.MFnNumericData.kFloat, .5 )
		numAttr.setKeyable( True )
		numAttr.setMin( .0 )
		numAttr.setMax( 2.0 )
		cls.damping 		= numAttr.create( "damping", "d", OpenMaya.MFnNumericData.kFloat, .5 )
		numAttr.setKeyable( True )
		numAttr.setMin( .0 )
		numAttr.setMax( 1.0 )
		
		cls.gravity			= numAttr.create( "gravity", "gr", OpenMaya.MFnNumericData.kFloat, .0 )
		numAttr.setKeyable( True )
		cls.gravityDirection	= numAttr.createPoint( "gravityDirection", "gd",  )
		numAttr.setDefault( .0, -1.0, .0)

		#
		cls.globalRelativeMatrix    = matrixAttr.create( 'globalRelativeMatrix' ,'grm' , OpenMaya.MFnNumericData.kFloat )

		# matrices per level
		cls.inMatrix		= matrixAttr.create( 'inMatrix' ,'im' , OpenMaya.MFnNumericData.kFloat )
		cls.goalMatrix		= matrixAttr.create( 'goalMatrix' ,'gm' , OpenMaya.MFnNumericData.kFloat )
		cls.relativeMatrix	= matrixAttr.create( 'relativeMatrix' ,'rm' , OpenMaya.MFnNumericData.kFloat )
		
		cls.inLevels		= compAttr.create( 'inLevels' , 'ilvs' )
		compAttr.addChild( cls.relativeMatrix )
		compAttr.addChild( cls.inMatrix )
		compAttr.addChild( cls.goalMatrix )
		compAttr.setArray( True )

		# ramps override some attrs
		cls.useAimWeightRamp	= numAttr.create( 'useAimWeightRamp', 'uawrp', OpenMaya.MFnNumericData.kBoolean, False )
		cls.useUpWeightRamp	    = numAttr.create( 'useUpWeightRamp', 'uuwrp', OpenMaya.MFnNumericData.kBoolean, False )
		cls.useMassRamp		    = numAttr.create( 'useMassRamp', 'umrp', OpenMaya.MFnNumericData.kBoolean, False )
		cls.useStiffnessRamp	= numAttr.create( 'useStiffnessRamp', 'usrp', OpenMaya.MFnNumericData.kBoolean, False )
		cls.useDampingRamp		= numAttr.create( 'useDampingRamp', 'udrp', OpenMaya.MFnNumericData.kBoolean, False )
		cls.useGravityRamp		= numAttr.create( 'useGravityRamp', 'ugrp', OpenMaya.MFnNumericData.kBoolean, False )
		
		cls.aimWeightRamp	= rpAttr.createCurveRamp( "aimWeightRamp", "awrp" )
		cls.upWeightRamp	= rpAttr.createCurveRamp( "upWeightRamp", "uwrp" )
		cls.massRamp		= rpAttr.createCurveRamp( "massRamp", "mrp" )
		cls.stiffnessRamp	= rpAttr.createCurveRamp( "stiffnessRamp", "srp" )
		cls.dampingRamp	    = rpAttr.createCurveRamp( "dampingRamp", "drp" )
		cls.gravityRamp		= rpAttr.createCurveRamp( "gravityRamp", "grp" )
		
		# rotateOrders for outRotates
		cls.rotateOrders	= enumAttr.create( "rotateOrders", "ros", 6)
		for k,item in enumerate( ("xyz","yzx","zyx","xzy","yxz","zyx", "None") ):
			enumAttr.addField( item , k )
		enumAttr.setArray( True )
		
		# jo for outRotates
		cls.jointOrientX    = unitAttr.create(  'jointOrientX', 'jox', OpenMaya.MFnUnitAttribute.kAngle, .0)
		cls.jointOrientY    = unitAttr.create(  'jointOrientY', 'joy', OpenMaya.MFnUnitAttribute.kAngle, .0)
		cls.jointOrientZ    = unitAttr.create(  'jointOrientZ', 'joz', OpenMaya.MFnUnitAttribute.kAngle, .0)
		cls.jointOrients    = compAttr.create(  'jointOrients' , 'jos')
		compAttr.addChild( cls.jointOrientX )
		compAttr.addChild( cls.jointOrientY )
		compAttr.addChild( cls.jointOrientZ )
		compAttr.setArray( True )

		#
		cls.stretchPositive      = numAttr.create( "stretchPositive", "stp", OpenMaya.MFnNumericData.kFloat, .0 )
		numAttr.setMin( .0 )
		numAttr.setMax( 1.0 )
		cls.stretchNegative      = numAttr.create( "stretchNegative", "stn", OpenMaya.MFnNumericData.kFloat, .0 )
		numAttr.setMin( .0 )
		numAttr.setMax( 1.0 )
		
		cls.weightPositive  		= numAttr.createPoint( "weightPositive", "wps"  )
		numAttr.setMin( .0,.0,.0 )
		numAttr.setMax( 1.0,1.0,1.0 )
		numAttr.setDefault( 1.0,1.0,1.0 )
		
		cls.weightNegative  		= numAttr.createPoint( "weightNegative", "wns"  )
		numAttr.setMin( .0,.0,.0 )
		numAttr.setMax( 1.0,1.0,1.0 )
		numAttr.setDefault( 1.0,1.0,1.0 )
		
		cls.smooth          = numAttr.createPoint( "smooth", "sth" )
		numAttr.setMin( .0,.0,.0 )
		numAttr.setMax( 1.0,1.0,1.0 )
		numAttr.setDefault( 1.0,1.0,1.0 )
		
		cls.useLimit        = numAttr.create( 'useLimit', 'ul', OpenMaya.MFnNumericData.kBoolean, False )
		cls.limitPositive   = numAttr.createPoint( "limitPositive", "lpv"  )
		numAttr.setMin( e,e,e )
		cls.limitNegative   = numAttr.createPoint( "limitNegative", "lnv"  )
		numAttr.setMax( -e,-e,-e )
		
		cls.limits          = compAttr.create( 'limits' , 'lms' )
		compAttr.addChild( cls.useLimit )
		compAttr.addChild( cls.limitPositive )
		compAttr.addChild( cls.limitNegative )
		compAttr.setArray( True )

		# fake attribute
		cls.refreshStatic   = numAttr.create( 'refreshStatic', 'rfst', OpenMaya.MFnNumericData.kBoolean, False )
		numAttr.setHidden( True )

		#
		cls.outMatrix		= matrixAttr.create( 'outMatrix' ,'om' , OpenMaya.MFnNumericData.kFloat )
		matrixAttr.setWritable( False )
		
		cls.outTranslate	= numAttr.createPoint( "outTranslate", "ot",  )
		numAttr.setWritable( False )
		
		cls.outRotateX		= unitAttr.create(  "outRotateX", "orx", OpenMaya.MFnUnitAttribute.kAngle, .0)
		unitAttr.setWritable( False )
		cls.outRotateY		= unitAttr.create(  "outRotateY", "ory", OpenMaya.MFnUnitAttribute.kAngle, .0)
		unitAttr.setWritable( False )
		cls.outRotateZ		= unitAttr.create(  "outRotateZ", "orz", OpenMaya.MFnUnitAttribute.kAngle, .0)
		unitAttr.setWritable( False )
		cls.outRotate		= compAttr.create( "outRotate" , "or")
		compAttr.addChild( cls.outRotateX )
		compAttr.addChild( cls.outRotateY )
		compAttr.addChild( cls.outRotateZ )
		compAttr.setWritable( False )
		
		cls.outLevels		= compAttr.create( 'outLevels' , 'olvs')
		compAttr.addChild( cls.outMatrix )
		compAttr.addChild( cls.outTranslate )
		compAttr.addChild( cls.outRotate )
		compAttr.setArray( True )
		compAttr.setUsesArrayDataBuilder( True)
		compAttr.setWritable( False )

		#
		for attr in (
					cls.globalRelativeMatrix,
					cls.inTime,
					cls.rotationMode,
					cls.aimWeight,
					cls.upWeight,
					cls.upVector,
					cls.mass, cls.stiffness, cls.damping,
					cls.gravity, cls.gravityDirection,
					
					cls.additionMode,
					cls.inLevels,
					cls.useAimWeightRamp, cls.useUpWeightRamp, cls.useMassRamp, cls.useStiffnessRamp, cls.useDampingRamp, cls.useGravityRamp,
					cls.aimWeightRamp, cls.upWeightRamp, cls.massRamp, cls.stiffnessRamp, cls.dampingRamp, cls.gravityRamp,
					cls.rotateOrders,
					cls.jointOrients,
					
					cls.refreshStatic,
					
					cls.startTime,
					cls.solverMode,	
					
					cls.stretchPositive, cls.stretchNegative,
					cls.weightPositive,
					cls.weightNegative,
					cls.smooth,
					cls.limits,
					
					cls.outLevels,
				):
			cls.addAttribute( attr )

		# static dependencies
		# used for optimization, if one of these attrs changes,
		# refreshStatic is dirtied so I can use it for getting all these attrs just in this case
		for attr in (
					cls.solverMode,
					cls.startTime,
					cls.additionMode,
					cls.rotationMode,
					cls.aimWeight,
					cls.upWeight,
					cls.upVector,
					cls.mass, cls.stiffness, cls.damping,
					cls.gravity, cls.gravityDirection,
					cls.useAimWeightRamp, cls.useUpWeightRamp, cls.useMassRamp, cls.useStiffnessRamp, cls.useDampingRamp, cls.useGravityRamp,
					cls.aimWeightRamp, cls.upWeightRamp, cls.massRamp, cls.stiffnessRamp, cls.dampingRamp, cls.gravityRamp,
					cls.rotateOrders,
					cls.jointOrients,
					cls.stretchPositive, cls.stretchNegative,
					cls.weightPositive,
					cls.weightNegative,
					cls.smooth,
					cls.limits,
				):
			cls.attributeAffects( attr, cls.refreshStatic )
		
		# dynamic dependencies
		for attr in (
					cls.solverMode,
					cls.rotationMode,
					cls.inTime,
					cls.aimWeight,
					cls.upWeight,
					cls.upVector,
					cls.globalRelativeMatrix,
					cls.inLevels,
					cls.rotateOrders,
					cls.jointOrients,
				):
			cls.attributeAffects( attr, cls.outLevels )
			cls.attributeAffects( attr, cls.outMatrix )
			cls.attributeAffects( attr, cls.outTranslate )
			cls.attributeAffects( attr, cls.outRotate )

		#
		cls.init_AETemplate()

	@classmethod
	def init_AETemplate( cls  ):
		AE_cmd = '''
		
		// AE  tool functions
		
		global proc string[] get_inLevelsK_from_selection( )
		{
			string $sel[] = `ls -sl -type "transform" -type "joint"`;
			
			string $node_levelsK[] ;
			
			for ($item in $sel)
			{
				string $outWorldMatrixNodes[]   = `listConnections -d 1 -s 0 ($item+".wm[0]")`;
				string $outWorldMatrixAttrs[]   = `listConnections -d 1 -s 0 -p 1 ($item+".wm[0]")`;
				
				for ($i=0; $i<size($outWorldMatrixNodes); $i++)
				{
					string $nodeType = `nodeType $outWorldMatrixNodes[$i]`;
					
					if (($nodeType=="dynamicChain") && (`match "inMatrix" $outWorldMatrixAttrs[$i]`!=""))
					{
						// remove the .inMatrix
						string $toAdd = `substitute ".inMatrix" $outWorldMatrixAttrs[$i] "" ` ;
						
						$node_levelsK[ size($node_levelsK) ] = $toAdd ;
					}
				}
			}
			
			string $sel[] = `ls -sl -type "dynamicChain"`;
			
			for ($item in $sel)
			{
				int $ids[]	= `getAttr -multiIndices ($item+".inLevels") ` ;
				
				for ($id in $ids)
				{
					string $toAdd   = $item+".inLevels["+$id+"]" ;
					
					$node_levelsK[ size($node_levelsK) ] = $toAdd ;
				}
			}
			
			print $node_levelsK ;
			
			
			return $node_levelsK ;
		}
		
		global proc string[] get_limitsK_from_levelsK( string $node_levelsK[] )
		{
			// extract the id
			
			string $node_limitsK[] ;
			
			
			for ($node_levelK in $node_levelsK )
			{
				//string $token[] ;  tokenize $node_levelK "[0-9]" $token ;
				//string $id      = $token[0]
				
				string $toAdd   = `substitute  (".inLevels")  $node_levelK    (".limits") ` ;
				
				$node_limitsK[size($node_limitsK)]  = $toAdd  ;
			}
			
			print $node_limitsK ;
			
			return $node_limitsK ;
		}
		
		global proc run_dynamicChainLimitCtx( )
		{
			// unselect then select  to refresh
			string $sel[] = `ls -sl`;
			select $sel ;
			
			if (`contextInfo -ex "dynamicChainLimitCtx1"`!=1) { dynamicChainLimitCtx ; }
			if (`currentCtx`!="dynamicChainLimitCtx1")        { setToolTo "dynamicChainLimitCtx1"  ; }
		}
		
		global proc switch_dynamicChain_limits( int $action  )
		{
			// run to visualize
			run_dynamicChainLimitCtx( ) ;
			
			
			// get the attrs to edit from selection
			string $node_attrs[]     = get_inLevelsK_from_selection() ;
			$node_attrs              = get_limitsK_from_levelsK( $node_attrs );
			
			
			for ($node_attr in $node_attrs)
			{ setAttr ($node_attr+".useLimit") $action ; }
		}
		
		global proc set_dynamicChain_dvLimits( )
		{
			// run to visualize
			run_dynamicChainLimitCtx( ) ;
			
			
			// get the attrs to edit from selection
			string $node_levelsK[]     = get_inLevelsK_from_selection() ;
			string $node_limitsK[]     = get_limitsK_from_levelsK( $node_levelsK );
			
			
			for ($i=0; $i<size($node_levelsK); $i++)
			{
				float $inM[]   = `getAttr ($node_levelsK[$i]+".inMatrix" ) ` ;
				float $inT[]   = {$inM[12], $inM[13], $inM[14]};
				
				float $goalM[] = `getAttr ($node_levelsK[$i]+".goalMatrix" ) ` ;
				float $goalT[] = {$goalM[12], $goalM[13], $goalM[14]};
				
				float $d    = sqrt(  pow( ($goalT[0]-$inT[0]),2) +  pow( ($goalT[1]-$inT[1]),2) + pow( ($goalT[2]-$inT[2]),2)  );
				
				setAttr ($node_limitsK[$i]+".limitPositive") $d $d $d ;
				setAttr ($node_limitsK[$i]+".limitNegative") (-$d) (-$d) (-$d) ;
			}
		}
		
		global proc mult_dynamicChain_limits( float $multBy )
		{
			// run to visualize
			run_dynamicChainLimitCtx( ) ;
			
			
			//
			string $node_levelsK[]     = get_inLevelsK_from_selection() ;
			string $node_limitsK[]     = get_limitsK_from_levelsK( $node_levelsK );
			
			
			for ($i=0; $i<size($node_levelsK); $i++)
			{
				float $pos[]    = `getAttr ($node_limitsK[$i]+".limitPositive" ) ` ;
				float $neg[]    = `getAttr ($node_limitsK[$i]+".limitNegative" ) ` ;
				
				float $newPos[] = {$pos[0]*$multBy, $pos[1]*$multBy, $pos[2]*$multBy };
				float $newNeg[] = {$neg[0]*$multBy, $neg[1]*$multBy, $neg[2]*$multBy };
				
				setAttr ($node_limitsK[$i]+".limitPositive" ) $newPos[0] $newPos[1] $newPos[2] ;
				setAttr ($node_limitsK[$i]+".limitNegative") $newNeg[0] $newNeg[1] $newNeg[2] ;
			}
		}
		
		// AE  additive UI
		
		global proc AE_[nodeType]_topAdditive( string $attrName )
		{   
			string $cl = `rowLayout -numberOfColumns 1 -adjustableColumn 1 `;
				
				picture -image ":/node/dynamicChainAE.png" -p $cl;
			setParent..; // because I dont know what is the parent here
			
			
			string $frame = `frameLayout  -label "Limit Tools"
				-borderStyle "etchedIn"
				-collapsable 1 -collapse 1
				-marginWidth 15 -marginHeight 10
				-bgc .16 .16 .16` ;
				
				string $grid  = `gridLayout  -numberOfColumns 7 -cellWidthHeight 45 35 
					-allowEmptyCells 1
					-parent $frame   `;
				
				
				// build button cmds
				//string $tokenizen[] ;  tokenize $attrName "." $tokenizen ;
				
				
				//
				string $ctxCmd  = "run_dynamicChainLimitCtx()" ;
				
    	        button  -l "Ctx"  -ann "Run dynamicChainLimitCtx"
    	            -parent $grid
    	            -c $ctxCmd ;
    	        
    	    text -label "" -parent $grid;   ///////////////// separator
				
    	        
    	        //
				button  -l "ON"  -ann "Turn on all limits"
					-parent $grid
					-c "switch_dynamicChain_limits( 1 )" ;
				
			text -label "" -parent $grid;   ///////////////// separator
				
				//
				button  -l "Set dv"  -ann "Set limit attributes to dv length  (goal-in).length"
					-parent $grid 
					-c "set_dynamicChain_dvLimits( )" ;
				//
				button  -l "x1.1"  -ann "Mult limits by .1"
					-parent $grid
					-c "mult_dynamicChain_limits( 1.1 )" ;
				//
				button  -l "x2"  -ann "Mult limits by 2"
					-parent $grid
					-c "mult_dynamicChain_limits( 2.0 )" ;
				
			text -label "" -parent $grid;   ///////////////// separator
			text -label "" -parent $grid;   ///////////////// separator
	
				//
				button  -l "OFF"  -ann "Turn off all limits"
					-parent $grid
					-c "switch_dynamicChain_limits( 0 )" ;
			
			text -label "" -parent $grid;   ///////////////// separator
			text -label "" -parent $grid;   ///////////////// separator
			
				//
				button  -l "/1.1"  -ann "Divide limits by .1"
					-parent $grid
					-c "mult_dynamicChain_limits( (1.0/1.1) )" ;
				//
				button  -l "/2"  -ann "Mult limits by 2"
					-parent $grid
					-c "mult_dynamicChain_limits(  .5 )" ;
					
    	    setParent..;
    	    
    	    /*
    	    string $parentCol = `rowLayout -q -p $cl`;
    	    string $parentCol2 = `columnLayout -q -p $parentCol`;
    	    print (`columnLayout -q -cw $parentCol2`);
    	    print (`columnLayout -q -rs $parentCol2`);
    	    */
		}
		
		global proc AE_[nodeType]_updateNothing( string $attrName ) {}
		
		// AE
		
		global proc AE[nodeType]Template( string $nodeName )
		{
		editorTemplate -beginScrollLayout;
			
			// first param = build func 2nd=update func,  3rd= attrName
			editorTemplate -callCustom "AE_[nodeType]_topAdditive" "AE_[nodeType]_updateNothing" "";
			
			editorTemplate -beginLayout "Limit Attributes" -collapse 1;
				editorTemplate -addControl "smooth" ;
				editorTemplate -addSeparator ;
				editorTemplate -addControl "stretchPositive" ;
				editorTemplate -addControl "stretchNegative" ;
				editorTemplate -addSeparator ;
				editorTemplate -addControl "weightPositive";
				editorTemplate -addControl "weightNegative" ;
				//editorTemplate -callCustom "AE_[nodeType]_ctx" "AE_[nodeType]_updateNothing" "";
				editorTemplate -addControl "limits";
			editorTemplate -endLayout;
			
			editorTemplate -beginLayout "Solver Attributes" -collapse 0;
				editorTemplate -addControl "nodeState";
				editorTemplate -addSeparator ;
				editorTemplate -addControl "solverMode";
				editorTemplate -addControl "startTime";
				editorTemplate -addSeparator ;
				editorTemplate -addControl "additionMode" ;
				editorTemplate -addControl "rotationMode" ;
				editorTemplate -addControl "inTime";
				editorTemplate -addSeparator ;
				editorTemplate -addControl "aimWeight";
				editorTemplate -addControl "upWeight";
				editorTemplate -addControl "upVector";
				editorTemplate -addSeparator ;
				editorTemplate -addControl "mass";
				editorTemplate -addControl "stiffness";
				editorTemplate -addControl "damping";
				editorTemplate -addSeparator ;
				editorTemplate -addControl "gravity";
				editorTemplate -addControl "gravityDirection";
			editorTemplate -endLayout;
			
			editorTemplate -beginLayout "Ramp Override" -collapse 1;
				editorTemplate -addControl "useAimWeightRamp";
				editorTemplate -addControl "useUpWeightRamp";
				editorTemplate -addControl "useMassRamp";
				editorTemplate -addControl "useStiffnessRamp";
				editorTemplate -addControl "useDampingRamp";
				editorTemplate -addControl "useGravityRamp";
				AEaddRampControl "aimWeightRamp" ;
				AEaddRampControl "upWeightRamp" ;
				AEaddRampControl "massRamp" ;
				AEaddRampControl "stiffnessRamp" ;
				AEaddRampControl "dampingRamp" ;
				AEaddRampControl "gravityRamp" ;
			editorTemplate -endLayout;
			
			editorTemplate -beginLayout "Level Attributes" -collapse 1;
				editorTemplate -addControl "globalRelativeMatrix";
				editorTemplate -addControl "rotateOrders";
				editorTemplate -addControl "jointOrients";
				editorTemplate -addControl "inLevels";
			editorTemplate -endLayout;
			
		editorTemplate -addExtraControls;
		editorTemplate -endScrollLayout;
		}
		'''.replace("[nodeType]", cls.kPluginNodeName )
		OpenMaya.MGlobal.executeCommand( AE_cmd )

	def __init__(self):
		OpenMayaMPx.MPxNode.__init__(self)
		
		self.initialized	= False

		# storage for the static input attrs
		self.thisObj        = None
		self.staticData     = {}

		# 
		self.lastTime		= .0
		
		self.lastGoal		= []
		self.lastGoalVel	= []
		
		self.lastUp1		= []
		self.lastUp2		= []
		self.lastUp1Vel		= []
		self.lastUp2Vel		= []

	def get_rampPositions(self, ids):
		
		num             = len(ids)
		rampPositions	= [.0]
		
		if num>1 :
			rampPositions	= [ float(k)/(num-1)   for k in range(num) ]
		
		return rampPositions
	
	def rampOrValues_to_staticData(self, data, ids):
		
		simples     = ('aw','uw','m','st','dp','g')
		directAttrs = (self.aimWeight, self.upWeight, self.mass, self.stiffness, self.damping, self.gravity)
		rampAttrs   = (self.aimWeightRamp, self.upWeightRamp, self.massRamp, self.stiffnessRamp, self.dampingRamp, self.gravityRamp)
		thisObj		= self.thisMObject()
		rampObjs    = [OpenMaya.MRampAttribute( thisObj, item) for item in rampAttrs]
		rampPoss    = self.get_rampPositions(  ids )
		boolAttrs   = (self.useAimWeightRamp, self.useUpWeightRamp, self.useMassRamp, self.useStiffnessRamp, self.useDampingRamp, self.useGravityRamp )

		for i in ids :
			for simple, boolAttr, rampObj, directAttr in zip(simples, boolAttrs, rampObjs, directAttrs):
				'''
				# use ramp or not
				if data.inputValue(boolAttr).asBool():
					self.staticData[i][simple]   = self.get_rampValue(  rampObj, rampPoss[i] )
				else :
					self.staticData[i][simple]   = data.inputValue(directAttr).asFloat()
				'''
				self.staticData[i][simple]   = data.inputValue(directAttr).asFloat()
				
				# mult by ramp or not
				if data.inputValue(boolAttr).asBool():
					self.staticData[i][simple]  *= self.get_rampValue(  rampObj, rampPoss[i] )
	
	def rotateOrders_to_staticData(self, data,ids):
		
		rotOrders_H     = data.inputArrayValue( self.rotateOrders )
		
		for i in ids :
			try :
				rotOrders_H.jumpToElement( i )
				ro		= rotOrders_H.inputValue().asInt()
			except :
				ro		= 0
				
			self.staticData[i]['ro']   = ro

	def jointOrients_to_staticData( self, data, ids):
		
		jos_H     = data.inputArrayValue( self.jointOrients )
		
		for i in ids :
			try :
				jos_H.jumpToElement( i )
				jo_H        = jos_H.inputValue()
				
				jo_Euler    = self.get_Euler( jo_H, (self.jointOrientX, self.jointOrientY, self.jointOrientZ), None )
				jo_invFM    = MM_to_FM( jo_Euler.asMatrix() ).inverse()
			except :
				jo_invFM    = OpenMaya.MFloatMatrix()
			
			
			self.staticData[i]['jo_im']   = jo_invFM

	def limits_to_staticData(self, data,ids):
		
		limits_H     = data.inputArrayValue( self.limits )
		
		for i in ids :
			try :
				limits_H.jumpToElement( i )
				limit_H		= limits_H.inputValue()
				useIt       = limit_H.child(self.useLimit).asBool()
				pos3        = list( limit_H.child(self.limitPositive).asFloat3() )
				neg3        = list( limit_H.child(self.limitNegative).asFloat3() )
				
				# for the ellipsoid function, we cant have .0
				if pos3[0]<e:  pos3[0]=e
				if pos3[1]<e:  pos3[1]=e
				if pos3[2]<e:  pos3[2]=e
				if neg3[0]>-e:  neg3[0]=-e
				if neg3[1]>-e:  neg3[1]=-e
				if neg3[2]>-e:  neg3[2]=-e
			except :
				useIt       = False
				pos3        = (.0,.0,.0)
				neg3        = (.0,.0,.0)
			
			self.staticData[i]['useLimit']  = useIt
			self.staticData[i]['lpv']       = pos3
			self.staticData[i]['lnv']       = neg3

	def get_staticData(self, data, ids ):
		
		#
		self.thisObj	= self.thisMObject()

		# format staticData
		self.staticData    = {}
		
		for i in ids :
			self.staticData[i]     = {}

		# add  non-ramp attrs  to  staticData
		self.staticData['solverMode']      = data.inputValue(self.solverMode).asInt()
		self.staticData['startTime']       = data.inputValue(self.startTime).asFloat()
		
		self.staticData['additionMode']    = data.inputValue(self.additionMode).asInt()
		self.staticData['rotationMode']    = data.inputValue(self.rotationMode).asInt()
		
		self.staticData['uv1']             = data.inputValue(self.upVector).asFloatVector().normal()
		self.staticData['uv2']             = OpenMaya.MFloatVector(-self.staticData['uv1'].x,-self.staticData['uv1'].y,-self.staticData['uv1'].z)
		self.staticData['gd']              = data.inputValue(self.gravityDirection).asFloatVector().normal()
		
		
		self.staticData['sp']              = data.inputValue(self.stretchPositive).asFloat()
		self.staticData['sn']              = data.inputValue(self.stretchNegative).asFloat()
		self.staticData['wp']              = data.inputValue(self.weightPositive).asFloat3()
		self.staticData['wn']              = data.inputValue(self.weightNegative).asFloat3()
		
		smooths     = data.inputValue(self.smooth).asFloat3()
		self.staticData['sm']              = [ self.set_range( item, .0, 1.0, e, 1.0 )  for item in smooths ]

		# add ramps  to  staticData
		self.rampOrValues_to_staticData( data, ids )

		# add gravity vector  using direction and gravity
		for i in ids :
			self.staticData[i]['gv']       = ( self.staticData[i]['g']*self.staticData['gd'].x,
												self.staticData[i]['g']*self.staticData['gd'].y,
			                                    self.staticData[i]['g']*self.staticData['gd'].z  )
		

		# add rotateOrders and jointOrients  to  staticData
		self.rotateOrders_to_staticData( data, ids)
		self.jointOrients_to_staticData( data, ids)

		# add ellipsoids  to  staticData
		self.limits_to_staticData( data, ids)

		#
		data.outputValue( self.refreshStatic ).setClean()

	def get_ids( self ):
		
		regions_ids	    = OpenMaya.MIntArray()
		regions_Plug	= OpenMaya.MPlug( self.thisMObject(), self.inLevels)
		regions_Plug.getExistingArrayAttributeIndices( regions_ids )
		
		return regions_ids

	def get_all_levelMatrix( self, ids, data=None, ctx=None ):

		relative_FMs,  in_FMs,  goal_FMs, local_FMs		= [],[],[],[]
		
		
		if data :
			# FAST
			globalRelative_FM   = data.inputValue(self.globalRelativeMatrix).asFloatMatrix()
			levels_H            = data.inputArrayValue( self.inLevels )
			
			for i in ids :
				relative_FM,  in_FM,  goal_FM   = self.get_levelMatrix(  i, data, globalRelative_FM, levels_H )
				
				relative_FMs.append(relative_FM)
				in_FMs.append(in_FM)
				goal_FMs.append(goal_FM)
				local_FMs.append( in_FM * relative_FM )

		else :
			# ONEROUS
			levels_Plug         = OpenMaya.MPlug( self.thisObj, self.inLevels )
			
			for i in ids :
				relative_FM,  in_FM,  goal_FM   = self.get_levelMatrix_at_ctx(  i, ctx, levels_Plug  )
				
				relative_FMs.append(relative_FM)
				in_FMs.append(in_FM)
				goal_FMs.append(goal_FM)
				local_FMs.append( in_FM * relative_FM )

		return relative_FMs,  in_FMs,  goal_FMs, local_FMs
	
	def get_levelMatrix( self, i, data,
	                     globalRelative_FM,
	                     levels_H ):
		
		if not globalRelative_FM :
			globalRelative_FM   = data.inputValue(self.globalRelativeMatrix).asFloatMatrix()
		
		if not levels_H:
			levels_H        = data.inputArrayValue( self.inLevels ) 

		#
		levels_H.jumpToElement( i )
		level_H		    = levels_H.inputValue()
		
		relative_FM	    = ( level_H.child(self.relativeMatrix).asFloatMatrix() *globalRelative_FM  ).inverse()
		# (AB-1)-1 = BA-1   I can remove this .inverse()  by having as inputs  globalRelativeMatrix normal   and  relativeMatrices already inversed
		
		in_FM		    = level_H.child(self.inMatrix).asFloatMatrix() *globalRelative_FM
		goal_FM		    = level_H.child(self.goalMatrix).asFloatMatrix() *globalRelative_FM

		return relative_FM,  in_FM,  goal_FM

	def get_levelMatrix_at_ctx( self, i, ctx, levels_Plug ):
		
		globalRelative_Plug = OpenMaya.MPlug( self.thisObj, self.globalRelativeMatrix )
		globalRelative_Obj  = globalRelative_Plug.asMObject( ctx )
		globalRelative_FM   = MM_to_FM( OpenMaya.MFnMatrixData( globalRelative_Obj ).matrix() )
		
		#
		level_Plug          = levels_Plug.elementByLogicalIndex( i )
		
		relative_Plug       = level_Plug.child(self.relativeMatrix)
		in_Plug             = level_Plug.child(self.inMatrix)
		goal_Plug           = level_Plug.child(self.goalMatrix)
		
		relative_Obj        = relative_Plug.asMObject( ctx )
		in_Obj              = in_Plug.asMObject( ctx )
		goal_Obj            = goal_Plug.asMObject( ctx )
		
		relative_FM         = (MM_to_FM( OpenMaya.MFnMatrixData( relative_Obj ).matrix() ) *globalRelative_FM).inverse()
		in_FM               = MM_to_FM( OpenMaya.MFnMatrixData( in_Obj ).matrix() ) *globalRelative_FM
		goal_FM             = MM_to_FM( OpenMaya.MFnMatrixData( goal_Obj ).matrix() ) *globalRelative_FM
		
		
		return relative_FM, in_FM, goal_FM 

	def format_POS_VEL( self, num ):
		
		self.lastGoal		= []
		self.lastGoalVel	= []
		
		self.lastUp1		= []
		self.lastUp1Vel		= []
		self.lastUp2		= []
		self.lastUp2Vel		= []
		
		for i in range(num):
			self.lastGoal.append( [.0,.0,.0] )
			self.lastGoalVel.append( [.0,.0,.0] )
			
			self.lastUp1.append( [.0,.0,.0] )
			self.lastUp1Vel.append( [.0,.0,.0] )
			self.lastUp2.append( [.0,.0,.0] )
			self.lastUp2Vel.append( [.0,.0,.0] )

	def reset_POS_VEL( self, ids, data=None, ctx=None ):
		
		# met les lastGoal en current goal_w
		# up ...
		# set les outMatrices en local
		num  = len(ids)
		self.format_POS_VEL( num )
		
		if data :
			relative_FMs,  in_FMs,  goal_FMs, local_FMs     = self.get_all_levelMatrix( ids, data=data )
		else :
			relative_FMs,  in_FMs,  goal_FMs, local_FMs     = self.get_all_levelMatrix( ids, ctx=ctx )

		for i in range(num) :
			self.lastGoal[ i ]	    = extract_translate( goal_FMs[i] )
			self.lastGoalVel[ i ]	= [.0,.0,.0]
			
			up1_FV                  = (self.staticData['uv1']  *  in_FMs[i]).normal()
			self.lastUp1[ i ]		= [ up1_FV.x, up1_FV.y, up1_FV.z ]
			
			self.lastUp1Vel[ i ]	= [.0,.0,.0]
			up2_FV                  = (self.staticData['uv2']  *  in_FMs[i]).normal()
			self.lastUp2[ i ]		= [ up2_FV.x, up2_FV.y, up2_FV.z ]
			self.lastUp2Vel[ i ]	= [.0,.0,.0]
		
		
		return local_FMs
	
	
	
	def write_outputs( self, ids, out_FMs, data ):
		'''write outMatrices  and  setAllClean '''
		
		outJnts_H		    = data.outputArrayValue( self.outLevels )
		outs_Builder	    = outJnts_H.builder()

		j=0
		for i in ids:
			
			try :
				outJnts_H.jumpToElement( i )
				outJnt_H    = outJnts_H.outputValue()
			except :
				outJnt_H    = outs_Builder.addElement( i )
			
			# inject jo_inverse before rotMatrix
			t_FM        = translate_to_FM( extract_translate( out_FMs[j] ) )
			rot_FM      = OpenMaya.MFloatMatrix( out_FMs[j] )
			self.set_translate_to_FM( rot_FM, (.0,.0,.0) )
			
			rot_FM      = rot_FM * self.staticData[i]['jo_im']
			
			out_FM      = rot_FM * t_FM

			# write matrix,  use jointOrient
			#out_FM      = out_FMs[j]
			outJnt_H.child( self.outMatrix ).setMFloatMatrix( out_FM  )

			# write translate
			outTrans_H	= outJnt_H.child( self.outTranslate )
			translate	= extract_translate( out_FM )
			outTrans_H.set3Float( translate[0], translate[1], translate[2]  )

			# write euler
			euler		= OpenMaya.MTransformationMatrix( FM_to_MM( out_FM )  ).eulerRotation()	# kXYZ
			ro          = self.staticData[i]['ro']
			if ro not in (0,6):
				euler.reorderIt(  ro  )
			
			outR_H		= outJnt_H.child( self.outRotate )
			outRx_H		= outR_H.child( self.outRotateX )
			outRy_H		= outR_H.child( self.outRotateY )
			outRz_H		= outR_H.child( self.outRotateZ )
			self.set_Euler_to_Handle3( (outRx_H, outRy_H, outRz_H), euler )
			
			
			j += 1
		
		outJnts_H.setAllClean( )

	def reset_and_WRITE(self, ids, data ):
		
		local_FMs   = self.reset_POS_VEL( ids, data=data )
		
		self.write_outputs( ids, local_FMs, data  )

	def compute(self, plug, data):

		# default block system for the node attrs
		# refresh  static data  if necessary
		used_ids	= self.get_ids()
		
		if plug not in (self.outLevels, self.outMatrix, self.outTranslate, self.outRotate)   or   not used_ids :
			return
		
		if not data.isClean( self.refreshStatic ):
			self.get_staticData( data, used_ids )

		nodeState       = data.inputValue( self.state).asInt()
		if nodeState==1 :
			return

		# .setAllClean bug,  compute only if plug_id is the first one
		plug_ii     = plug.parent()
		plug_id     = plug_ii.logicalIndex()
		
		if plug_id != used_ids[0] :
			return

		# default block system for dynamic
		currentTime	    = data.inputValue( self.inTime ).asTime().value()
		
		if self.staticData['solverMode']==0 :
			startTime	= OpenMayaAnim.MAnimControl.minTime().value()
		else :
			startTime   = self.staticData['startTime']

		if not self.initialized :
			self.lastTime       = currentTime
			self.reset_and_WRITE( used_ids, data  )
			self.initialized    = True
			return

		if currentTime <= startTime :
			self.lastTime       = startTime
			self.reset_and_WRITE( used_ids, data  )
			return

		# solverMode changes the number of time we launch the compute
		# if==0 run the compute once  from the lastTime  FAST
		# if==1 run the compute for each frame between now and lastTime  --->  SO ONEROUS if user switch between lot of frames
		
		out_FMs		 = []

		if self.staticData['solverMode']==0:
			
			dt		  = currentTime - self.lastTime
			
			# limit it to -1 1  because otherwise I have a floatingPoint problem  when dt is too big
			if dt>1.0:      dt = 1.0
			elif dt <-1.0:  dt = -1.0

			out_FMs   = self.compute_once( used_ids,  dt,  data=data )
		else :
			# start from lastTime or startTime ?
			currentUnit     = OpenMaya.MTime.uiUnit()
			
			if currentTime > self.lastTime :
				time_f     = self.lastTime
				
			else :
				ctx		   = OpenMaya.MDGContext( OpenMaya.MTime( startTime, currentUnit ) )
				
				self.reset_POS_VEL( used_ids, ctx=ctx )
				
				time_f     = startTime

			# get computeNum
			dt              = 1.0
			computeNum_f    = (currentTime - time_f) / dt
			computeNum      = int( computeNum_f )

			#
			for i in range( computeNum ):
				
				time_f     += dt
				ctx		    = OpenMaya.MDGContext( OpenMaya.MTime( time_f, currentUnit ) )
				#print '1 MTime.value = ', OpenMaya.MTime( time_f, currentUnit ).value()
				out_FMs     = self.compute_once( used_ids,  dt,  ctx=ctx )

			# one last using last_dt
			last_dt         = computeNum_f - computeNum
			
			if last_dt > e :
				time_f     += last_dt
				ctx		    = OpenMaya.MDGContext( OpenMaya.MTime( time_f, currentUnit ) )
				#print '2 MTime.value = ', OpenMaya.MTime( time_f, currentUnit ).value()
				out_FMs     = self.compute_once( used_ids,  last_dt,  ctx=ctx )

		#
		self.write_outputs(  used_ids, out_FMs, data )
		
		self.lastTime	= currentTime
		
		data.setClean( plug )

	def compute_once(self, used_ids,  dt,  ctx=None, data=None):
		"""Use relative/in/goal matrices to update pos and vel
		return outMatrices (at this time if specified)"""

		# GET matrices
		# init the matrices relativ/in/goal for jnt[0]
		
		globalRelative_FM, levels_H = None, None # needed only if data
		levels_Plug     = None                   # needed only if ctx

		if data :
			# FAST
			globalRelative_FM   = data.inputValue(self.globalRelativeMatrix).asFloatMatrix()
			levels_H            = data.inputArrayValue( self.inLevels )
			
			relative_FM, in_FM, goal_FM   = self.get_levelMatrix( used_ids[0], data, globalRelative_FM, levels_H )
		
		else :
			# ONEROUS
			levels_Plug     = OpenMaya.MPlug( self.thisObj, self.inLevels )
			
			relative_FM, in_FM, goal_FM   = self.get_levelMatrix_at_ctx( used_ids[0], ctx, levels_Plug )

		# update pos and vel, and iterate relative/in/goal for each jnt[ i ]
		
		out_FMs     = []
		
		for i in range(len(used_ids)) :

			if i !=0 :
				# override  matrices
				
				if data:
					nextRelative_FM, nextIn_FM, nextGoal_FM	 = self.get_levelMatrix( used_ids[i], data, globalRelative_FM, levels_H )
				else :
					nextRelative_FM, nextIn_FM, nextGoal_FM  = self.get_levelMatrix_at_ctx( used_ids[i], ctx, levels_Plug )
					
				
				deltaGoal	= nextGoal_FM * nextIn_FM.inverse()
				deltaIn		= nextIn_FM * nextRelative_FM
				
				relative_FM	= out_wFM.inverse()

				#
				out_pos		= extract_translate( out_wFM )
				vec			= OpenMaya.MFloatVector( self.lastGoal[i-1][0]-out_pos[0], self.lastGoal[i-1][1]-out_pos[1], self.lastGoal[i-1][2]-out_pos[2] )
				vec			= vec * relative_FM
				t_FM		= translate_to_FM( vec )
				
				self.set_translate_to_FM( deltaIn, (.0,.0,.0) )	# it is a rotation matrix now

				#
				in_FM		= deltaIn  *  t_FM  *  out_wFM
				goal_FM		= deltaGoal  *  in_FM

			# rk goal,   velocity or acceleration mode
			in_w		= extract_translate( in_FM )
			goal_w	    = extract_translate( goal_FM )

			if self.staticData['additionMode']==0 :
				self.rk_and_update_vel(  self.fonc1, used_ids[ i ], dt,
				                         goal_w,
				                         self.lastGoal[ i ],
				                         self.lastGoalVel[ i ]  )
			
			elif self.staticData['additionMode']==1:
				self.rk_and_update_acc(  self.fonc1, used_ids[ i ], dt,
				                         goal_w,
				                         self.lastGoal[ i ],
				                         self.lastGoalVel[ i ],)

			# limit
			dvDistance          = OpenMaya.MFloatVector( goal_w[0]-in_w[0], goal_w[1]-in_w[1], goal_w[2]-in_w[2] ).length()
			dir_FV              = OpenMaya.MFloatVector( self.lastGoal[i][0]-goal_w[0], self.lastGoal[i][1]-goal_w[1], self.lastGoal[i][2]-goal_w[2] )
			
			self.lastGoal[ i ]	= self.limit_from_goal(  i, goal_w, in_FM, dvDistance, dir_FV  )
			
			self.lastGoal[ i ]	= self.limit_from_in( self.lastGoal[i], in_w,  dvDistance  )

			# aimWeight = linear wgt between goal and dynGoal
			if self.staticData[used_ids[ i ]]['aw'] < 1.0 :
				self.lastGoal[ i ]	= [ self.blend2( goal_w[k], self.lastGoal[i][k], self.staticData[used_ids[i]]['aw'] )  for k in range(3)  ]


			# calcule aim_matrice en world,  elle aim le goal
			# baseUp_FV = upVector1
			aim_FV      = OpenMaya.MFloatVector( self.lastGoal[ i ][0]-in_w[0], self.lastGoal[ i ][1]-in_w[1], self.lastGoal[ i ][2]-in_w[2] )
			
			goal_l      = extract_translate( goal_FM * in_FM.inverse() )
			baseAim_FV  = OpenMaya.MFloatVector( goal_l[0], goal_l[1], goal_l[2]  )

			if self.staticData['rotationMode']==1 :
				# override up1_FV and up2_FV
				# rk them  and   wgt them
				up1_FV      = (self.staticData['uv1'] * in_FM ).normal()
				up2_FV      = (self.staticData['uv2'] * in_FM ).normal()

				self.rk_and_update_vel( self.fonc2, used_ids[ i ], dt,  up1_FV,  self.lastUp1[ i ],  self.lastUp1Vel[ i ] )
				self.rk_and_update_vel( self.fonc2, used_ids[ i ], dt,  up2_FV,  self.lastUp2[ i ],  self.lastUp2Vel[ i ] )

				if self.staticData[used_ids[ i ]]['uw'] != 1.0 :
					self.lastUp1[ i ]   = [self.blend2( up1_FV[ k ], self.lastUp1[ i ][ k ], self.staticData[used_ids[ i ]]['uw'] )  for k in range(3)  ]
					self.lastUp2[ i ]   = [self.blend2( up2_FV[ k ], self.lastUp2[ i ][ k ], self.staticData[used_ids[ i ]]['uw'] )  for k in range(3)  ]

				# deduct the real upVector    from upVector1 and upVector2
				# up = up1 - up2
				up1_FV  = OpenMaya.MFloatVector( self.lastUp1[ i ][0], self.lastUp1[ i ][1], self.lastUp1[ i ][2] )
				up2_FV  = OpenMaya.MFloatVector( self.lastUp2[ i ][0], self.lastUp2[ i ][1], self.lastUp2[ i ][2] )
				up_FV   = (up1_FV - up2_FV).normal()

				# normalize for next compute
				up1_FV.normalize()
				up2_FV.normalize()
				self.lastUp1[ i ]       = [up1_FV.x, up1_FV.y, up1_FV.z]
				self.lastUp2[ i ]       = [up2_FV.x, up2_FV.y, up2_FV.z]
			else :
				# simply use upVector1
				up_FV   = (self.staticData['uv1'] * in_FM ).normal()

			out_wFM     = self.build_aimFM( aim_FV, baseAim_FV,   up_FV, self.staticData['uv1'] )

			# inject  translate
			self.set_translate_to_FM( out_wFM, in_w )

			out_FM      = out_wFM  *  relative_FM
			
			out_FMs.append(  out_FM  )

		return out_FMs
	
	
	
	
	def limit_from_goal(self, i, goal, in_FM, dvDistance, dir_FV  ):
		
		#** get vector goal->dyn  in  in_FM coordinate system
		local_FV    = dir_FV * in_FM.inverse()
		
		# get each axial limit
		if self.staticData[i]['useLimit']:
			
			if local_FV.x >=.0:     dMaxX   = self.staticData[i]['lpv'][0]
			else :                  dMaxX   = self.staticData[i]['lnv'][0]
			
			if local_FV.y >=.0:     dMaxY   = self.staticData[i]['lpv'][1]
			else :                  dMaxY   = self.staticData[i]['lnv'][1]
			
			if local_FV.z >=.0:     dMaxZ   = self.staticData[i]['lpv'][2]
			else :                  dMaxZ   = self.staticData[i]['lnv'][2]
			
			local_dMaxs     = [ dMaxX, dMaxY, dMaxZ ]
			
		else :
			# if no limit,  use the distance in-goal
			local_dMaxs     = [ dvDistance, dvDistance, dvDistance ]

		# weight axial :
		if local_FV.x >=.0:     local_dMaxs[0]   *= self.staticData['wp'][0]
		else :                  local_dMaxs[0]   *= self.staticData['wn'][0]
		
		if local_FV.y >=.0:     local_dMaxs[1]   *= self.staticData['wp'][1]
		else :                  local_dMaxs[1]   *= self.staticData['wn'][1]
		
		if local_FV.z >=.0:     local_dMaxs[2]   *= self.staticData['wp'][2]
		else :                  local_dMaxs[2]   *= self.staticData['wn'][2]

		# smooth using current distance, dMax, and smooth percent
		# do it in local
		local_dNews       = []
		
		for k in range(3):
			dCurrent		= abs( local_FV[k] )
			dMax            = abs( local_dMaxs[k] )
			
			delta			= self.staticData['sm'][k]  *  dMax
			dStart		    = dMax - delta
			
			if (dCurrent  >= dStart) and delta :
				# delta * (1-exp((dStart-dCurrent)/delta)) + dStart
				local_dNews.append( delta*(1.0-math.exp((dStart-dCurrent)/delta)) + dStart  )
			else :
				local_dNews.append( dCurrent )

		#** build new dir_FV,   same direction but limited/smoothed
		local_FV.normalize()
		
		newLocal_FV     = OpenMaya.MFloatVector( local_FV[0]*local_dNews[0], local_FV[1]*local_dNews[1], local_FV[2]*local_dNews[2]  )
		newDir_FV       = newLocal_FV * in_FM

		# return limitedPos
		return [ goal[0] + newDir_FV[0], goal[1] + newDir_FV[1], goal[2] + newDir_FV[2] ]
	
	def limit_from_in(self, dyn, inPos, dvDistance ):
		
		dir_FV      = OpenMaya.MFloatVector( dyn[0]-inPos[0], dyn[1]-inPos[1], dyn[2]-inPos[2] )
		in_dyn_d    = dir_FV.length()
		
		if in_dyn_d < e:
			in_dyn_d    = e

		# blend between dynDistance and dvDistance  using  strech 
		# use stretchPositive or negative
		
		if in_dyn_d >= dvDistance :
			finalDistance   = (1.0-self.staticData['sp'])*dvDistance + self.staticData['sp']*in_dyn_d
		else :
			finalDistance   = (1.0-self.staticData['sn'])*dvDistance + self.staticData['sn']*in_dyn_d
		
		#
		dir_FVn     = dir_FV.normal()
		
		return [ inPos[0] + dir_FVn[0]*finalDistance, inPos[1] + dir_FVn[1]*finalDistance, inPos[2] + dir_FVn[2]*finalDistance ]

	def build_aimFM( self, aim_FV, baseAim_FV,   up_FV, baseUp_FV ):
		
		# get quat transforming baseAim to desired aim  (aim_Q)
		aim_MV		= OpenMaya.MVector( aim_FV.x, aim_FV.y, aim_FV.z )
		baseAim_MV	= OpenMaya.MVector( baseAim_FV.x, baseAim_FV.y, baseAim_FV.z )
		aim_Q		= OpenMaya.MQuaternion( baseAim_MV.rotateTo( aim_MV  )     )

		# transform baseUp by aim_Q
		# then the tmpUp is crap
		baseLast_FV	= (baseAim_FV ^ baseUp_FV).normal()
		baseUp_FV	= (baseLast_FV ^ baseAim_FV).normal()
		
		baseUp_MV	= OpenMaya.MVector( baseUp_FV.x, baseUp_FV.y, baseUp_FV.z )
		tmpUp_MV	= baseUp_MV.rotateBy( aim_Q )
		

		# get quat transforming tmpUp to desired up  ( up_Q )
		last_FV		= (aim_FV ^ up_FV).normal()
		up_FV		= (last_FV ^ aim_FV).normal()
		
		up_MV		= OpenMaya.MVector( up_FV.x, up_FV.y, up_FV.z )
		up_Q		= OpenMaya.MQuaternion( tmpUp_MV.rotateTo(  up_MV  )     )

		upDot       = tmpUp_MV * up_MV
		
		if upDot < e-1.0 :
			# dot = -1   so twist-quat-axis can be anything !
			# Fix that using aim_vector
			axis, rad   = self.get_axisAngle( up_Q )
			up_Q.setAxisAngle( aim_MV, rad )

		# final : transform an identity by aim_Q then up_Q
		#final_Tr	= OpenMaya.MTransformationMatrix()
		#final_Tr.rotateBy(  aim_Q,  OpenMaya.MSpace.kTransform )
		#final_Tr.rotateBy(  up_Q,  OpenMaya.MSpace.kTransform  )
		
		final_Q     = aim_Q * up_Q
		final_FM    = MM_to_FM(  final_Q.asMatrix()  )

		return final_FM

	def rk_and_update_vel( self, fonc, jntId, dt, newPos, lastPos, lastVel  ):
		'''override lastPost et lastVel    pour chaque compound de la liste/Vec donnEe'''
		
		fonc_kwargs = {'jntId':jntId}

		for i in range(3) :
			
			fonc_kwargs['axisId']= i

			#
			deltaPos		= lastPos[i] - newPos[i]
			
			new_deltaPos, newVel = self.rk4( deltaPos, lastVel[i], dt, fonc, fonc_kwargs )
			
			lastVel[i]		= newVel
			lastPos[i]		= newPos[i]  +  new_deltaPos
			
			# pareil,  sauf quen partant de newPos  on evite les accumulations derreur
			#lastPos[i]		+= lastVel[i]

	def rk_and_update_acc( self, fonc, jntId, dt, newPos, lastPos, lastVel  ):
		
		fonc_kwargs = {'jntId':jntId}
		
		
		for i in range(3) :
			
			fonc_kwargs['axisId']= i

			#
			deltaPos		= lastPos[i] - newPos[i]
			
			new_deltaPos, newVel = self.rk4( deltaPos, lastVel[i], dt, fonc, fonc_kwargs )

			# do this
			#lastPos[i]		+= lastAcc[i]
			# instead of this
			#lastPos[i]		+= lastVel[i]

			# new_deltaVel  = newAcc
			new_deltaVel    = lastVel[i] - newVel
			
			lastVel[i]		= newVel
			lastPos[i]		= newPos[i]  +  new_deltaVel

	def fonc1( self, x, v, fonc_kwargs  ):
		# inDamp = wght du critical damp,   permet de n'avoir aucun ressort lorsque inDamp = 1.0
		# critical damping  =  2m sqrt(k/m)    -------->   realDamp  =  ratio  *  2m sqrt(k/m)
		#realDamp		= self.dampValue *   2.0 * self.massValue* math.sqrt( self.stiffValue/self.massValue  )
		
		# system [mass spring damper] classic :
		# ma + cv + kx = 0    ---->  a = (-cv - kx) /m
		#return (-x*self.stiffValue - v*realDamp ) /self.massValue  + self.gravityValues[axisId]
		
		jntId   = fonc_kwargs['jntId']
		axisId  = fonc_kwargs['axisId']
		
		realDamp = self.staticData[jntId]['dp'] *   2.0 * self.staticData[jntId]['m']* math.sqrt( self.staticData[jntId]['st']/self.staticData[jntId]['m']  )
		return (-x*self.staticData[jntId]['st'] - v*realDamp ) /self.staticData[jntId]['m']  + self.staticData[jntId]['gv'][axisId]

	def fonc2( self, x, v, fonc_kwargs ):
		'''same without gravity'''
		
		#realDamp		= self.dampValue *   2.0 * self.massValue* math.sqrt( self.stiffValue/self.massValue  )
		
		#return (-x*self.stiffValue - v*realDamp ) /self.massValue
	
		jntId   = fonc_kwargs['jntId']
		
		realDamp = self.staticData[jntId]['dp'] *   2.0 * self.staticData[jntId]['m']* math.sqrt( self.staticData[jntId]['st']/self.staticData[jntId]['m']  )
		return (-x*self.staticData[jntId]['st'] - v*realDamp ) /self.staticData[jntId]['m']

	def rk4(self, x, v, dt,  fonc, fonc_kwargs ):
		"""classic rk4 for fake the solve of 4thOrder equation"""
		x1  = x
		v1  = v
		a1  = fonc(x1, v1, fonc_kwargs )
		
		x2  = x + 0.5*v1*dt
		v2  = v + 0.5*a1*dt
		a2  = fonc(x2, v2, fonc_kwargs)
		
		x3  = x + 0.5*v2*dt
		v3  = v + 0.5*a2*dt
		a3  = fonc(x3, v3, fonc_kwargs)
		
		x4  = x + v3*dt
		v4  = v + a3*dt
		a4  = fonc(x4, v4,  fonc_kwargs)
		
		xf  = x + (dt/6.0)*(v1 + 2*v2 + 2*v3 + v4)
		vf  = v + (dt/6.0)*(a1 + 2*a2 + 2*a3 + a4)
		
		return xf, vf


class LimitCtx_cmd( OpenMayaMPx.MPxContextCommand ):
	
	cmdName		= "dynamicChainLimitCtx"

	def __init__(self):
		OpenMayaMPx.MPxContextCommand.__init__(self)
	
	def makeObj(self):
		return OpenMayaMPx.asMPxPtr( LimitCtx() )
	
	@classmethod
	def creator( cls ):
		return OpenMayaMPx.asMPxPtr( cls() )


class LimitCtx( OpenMayaMPx.MPxSelectionContext ):

	def __init__(self):
		OpenMayaMPx.MPxSelectionContext.__init__(self)
		self.callback_id    = None
	
	def toolOnSetup(self,event):
		'''build manipulators and callback'''
		
		self.updateManipulators( self )
		
		#
		self.callback_id    = OpenMaya.MModelMessage.addCallback(OpenMaya.MModelMessage.kActiveListModified, self.updateManipulators, self)
	
	def toolOffCleanup(self):
		'''remove existing manipulators and callback'''
		
		self.deleteManipulators()
		
		#
		OpenMaya.MModelMessage.removeCallback( self.callback_id )

	@staticmethod
	def updateManipulators( ctx ):
		
		ctx.deleteManipulators()
		
		
		sel		        = OpenMaya.MSelectionList()
		OpenMaya.MGlobal.getActiveSelectionList( sel )
		sel_It          = OpenMaya.MItSelectionList( sel  )
		
		
		while not sel_It.isDone():
			# get selected node
			# if it is a DynamicChain
			#       create manips for each joint detected   and  connect them to node
			# if it is a joint/transform
			#       find a connected dynamicChain ( matrix and worldMatrix )
			#           if it is ok   create only one manip to the limitAttr with a specific idx
			
			node        = OpenMaya.MObject()
			sel_It.getDependNode( node )
			
			node_Fn     = OpenMaya.MFnDependencyNode( node )
			nodeType    = node_Fn.typeName()

			if nodeType=='dynamicChain':
				
				levels_Plug     = node_Fn.findPlug('inLevels')
				ids             = OpenMaya.MIntArray()
				levels_Plug.getExistingArrayAttributeIndices( ids )
				
				for inLevel_id in ids :
					ctx.build_manip( node, inLevel_id )

			elif nodeType in ('joint','transform'):
				
				worldMatrix_Plug    = node_Fn.findPlug('worldMatrix')
				worldMatrix0_Plug   = worldMatrix_Plug.elementByLogicalIndex( 0 )
				
				output_Plugs        = OpenMaya.MPlugArray()
				worldMatrix0_Plug.connectedTo( output_Plugs, False, True);
				
				for k in range( output_Plugs.length() ) :
					output_Plug     = output_Plugs[k]
					
					outputNode      = output_Plug.node()
					outpout_Fn      = OpenMaya.MFnDependencyNode( outputNode )
					outputType      = outpout_Fn.typeName()
					outputName      = output_Plug.name()
					
					if (outputType=='dynamicChain')  and  ('inLevels' in outputName)  and  ('inMatrix' in outputName) :
						
						inLevel_id      = output_Plug.parent().logicalIndex()  # parent = inLevels[#]
						
						ctx.build_manip( outputNode, inLevel_id )
				
			sel_It.next()

	def build_manip(self, node, inLevel_id ):
		"""Build a Manip"""
		
		manip_Obj       = OpenMaya.MObject()
		manip_MPx       = OpenMayaMPx.MPxManipulatorNode.newManipulator( LimitManip.kPluginNodeName, manip_Obj)
		
		self.addManipulator( manip_Obj )
		manip_MPx.connectToDependNode( node, inLevel_id=inLevel_id )


class LimitManip( OpenMayaMPx.MPxManipulatorNode ):
	
	
	glRenderer  = OpenMayaRender.MHardwareRenderer.theRenderer()
	glFT        = glRenderer.glFunctionTable()
	
	kPluginNodeName = "dynamicChainLimit"
	kPluginNodeId   = OpenMaya.MTypeId(0x0D1266)

	@staticmethod
	def floatArray_to_ptr(floatArray):
		util	= OpenMaya.MScriptUtil() 
		util.createFromList(floatArray,len(floatArray))
		return util.asFloatPtr()

	@classmethod
	def nodeCreator( cls ):
		return OpenMayaMPx.asMPxPtr( cls() )

	@classmethod
	def nodeInitializer( cls ):
		pass
	
	def __init__(self):
		OpenMayaMPx.MPxManipulatorNode.__init__(self)
		
		self.inLevel_id     = None
		self.node_Fn        = None
		
		self.names      = ( 'xPos','xNeg', 'yPos','yNeg', 'zPos','zNeg' )
		
		self.xPos_id    = None
		self.xNeg_id    = None
		self.yPos_id    = None
		self.yNeg_id    = None
		self.zPos_id    = None
		self.zNeg_id    = None
		
		self.gl_xPos_name   = None
		self.gl_xNeg_name   = None
		self.gl_yPos_name   = None
		self.gl_yNeg_name   = None
		self.gl_zPos_name   = None
		self.gl_zNeg_name   = None
		
		
		self.cursor     = None

	def postConstructor(self ):
		# fill/build the 6 index
		
		tmp_ids     = []
		
		
		for name in self.names:
			
			util        = OpenMaya.MScriptUtil()
			util.createFromInt( 0 )
			int_ptr     = util.asIntPtr()
			
			self.addDoubleValue( name, .0, int_ptr )
			
			tmp_ids.append( util.getInt(int_ptr) )
		
		
		self.xPos_id    = tmp_ids[0]
		self.xNeg_id    = tmp_ids[1]
		self.yPos_id    = tmp_ids[2]
		self.yNeg_id    = tmp_ids[3]
		self.zPos_id    = tmp_ids[4]
		self.zNeg_id    = tmp_ids[5]
	
	def connectToDependNode(self, node, inLevel_id=None ):
		
		
		# stop if it is not the good nodeType
		node_Fn      = OpenMaya.MFnDependencyNode( node )
		
		if not node_Fn.hasAttribute( 'limits' ):
			return
		
		# pos
		limits_plug     = node_Fn.findPlug( 'limits' )
		limit_plug      = limits_plug.elementByLogicalIndex( inLevel_id )
		
		limitPos_plug   = limit_plug.child( 1 )
		
		for i, idx in enumerate( (self.xPos_id, self.yPos_id, self.zPos_id) ):
			pos_plug    = limitPos_plug.child( i )
			util        = OpenMaya.MScriptUtil()
			util.createFromInt( 0 )
			int_ptr     = util.asIntPtr()
			
			self.connectPlugToValue( pos_plug, idx, int_ptr )
		
		# neg
		limitNeg_plug   = limit_plug.child( 2 )
		
		for i, idx in enumerate( (self.xNeg_id, self.yNeg_id, self.zNeg_id) ):
			neg_plug    = limitNeg_plug.child( i )
			util        = OpenMaya.MScriptUtil()
			util.createFromInt( 0 )
			int_ptr     = util.asIntPtr()
			
			self.connectPlugToValue( neg_plug, idx, int_ptr )

		# end
		OpenMayaMPx.MPxManipulatorNode.finishAddingManips(self)
		OpenMayaMPx.MPxManipulatorNode.connectToDependNode(self, node )

		# store for draw
		self.inLevel_id = inLevel_id
		self.node_Fn    = node_Fn

	def draw( self, view, dagPath, displayStyle, displayStatus):

		# get first unused id
		# get active handle  then deduct other names
		util            = OpenMaya.MScriptUtil()
		util.createFromInt( 0 )
		uInt_ptr        = util.asUintPtr()
		
		self.glFirstHandle( uInt_ptr )
		glStartName     = util.getUint( uInt_ptr )
		
		
		self.gl_xPos_name   = glStartName
		self.gl_xNeg_name   = self.gl_xPos_name +1
		self.gl_yPos_name   = self.gl_xNeg_name +1
		self.gl_yNeg_name   = self.gl_yPos_name +1
		self.gl_zPos_name   = self.gl_yNeg_name +1
		self.gl_zNeg_name   = self.gl_zPos_name +1

		#**
		view.beginGL()
		
		self.glFT.glPushAttrib( OpenMayaRender.MGL_ALL_ATTRIB_BITS )

		# remove the light because otherwise the lines receive it !?
		self.glFT.glDisable( OpenMayaRender.MGL_LIGHTING  )

		# load matrix
		self.glFT.glPushMatrix()
		
		in_FM, goal_FM  = self.get_fms()
		dvDistance      = self.get_dvDistance( in_FM, goal_FM )
		useLimit,  xPos, xNeg, yPos, yNeg, zPos, zNeg  = self.get_limitValues(  dvDistance )
		
		matrix_ptr      = self.get_glMatrix( view, in_FM, goal_FM )
		
		self.glFT.glLoadMatrixf(  matrix_ptr  )

		# draw ellipsoid first   then points
		self.draw_ellipsoid( useLimit, xPos, xNeg, yPos, yNeg, zPos, zNeg )
		
		self.draw_points( view, xPos, xNeg, yPos, yNeg, zPos, zNeg )

		#**
		self.glFT.glPopMatrix()
		self.glFT.glPopAttrib()
		
		view.endGL()

	def draw_points(self, view, xPos, xNeg, yPos, yNeg, zPos, zNeg ):
		
		self.glFT.glPointSize( 6.0 )

		# X-POS
		self.colorAndName( view, self.gl_xPos_name, True, self.xColor() )
		self.glFT.glBegin(OpenMayaRender.MGL_POINTS)
		self.glFT.glVertex3f( xPos,0,0 )
		self.glFT.glEnd()
		
		# X-NEG
		self.colorAndName( view, self.gl_xNeg_name, True, self.xColor() )
		self.glFT.glBegin(OpenMayaRender.MGL_POINTS)
		self.glFT.glVertex3f( xNeg,0,0 )
		self.glFT.glEnd()
		
		#  Y-POS
		self.colorAndName( view, self.gl_yPos_name, True, self.yColor() )
		self.glFT.glBegin(OpenMayaRender.MGL_POINTS)
		self.glFT.glVertex3f( 0,yPos,0 )
		self.glFT.glEnd()
		
		# Y-NEG
		self.colorAndName( view, self.gl_yNeg_name, True, self.yColor() )
		self.glFT.glBegin(OpenMayaRender.MGL_POINTS)
		self.glFT.glVertex3f( 0,yNeg,0 )
		self.glFT.glEnd()
		
		#  Z-POS
		self.colorAndName( view, self.gl_zPos_name, True, self.zColor() )
		self.glFT.glBegin(OpenMayaRender.MGL_POINTS)
		self.glFT.glVertex3f( 0,0,zPos )
		self.glFT.glEnd()
		
		# Z-NEG
		self.colorAndName( view, self.gl_zNeg_name, True, self.zColor() )
		self.glFT.glBegin(OpenMayaRender.MGL_POINTS)
		self.glFT.glVertex3f( 0,0,zNeg )
		self.glFT.glEnd()
		
	
	
	
	def draw_ellipsoid(self, useLimit, xPos, xNeg, yPos, yNeg, zPos, zNeg):
		
		self.glFT.glEnable(OpenMayaRender.MGL_BLEND)
		self.glFT.glEnable(OpenMayaRender.MGL_LINE_SMOOTH)

		if useLimit :
			color   = (1.0, .5, .0)
			width   = 1.6
		else :
			color   = (.5, .5, .5)
			width   = 1.4
			
		self.glFT.glColor3f( color[0], color[1], color[2] )
		self.glFT.glLineWidth( width )

		# build the a and b values, the ellipse coordinates
		PI		    = 3.1416
		num     	= 10
		
		cos, sin    = [], []
		
		for i in range( 0, 90+num, num ):
			cos.append( math.cos(i*PI/180) )
			sin.append( math.sin(i*PI/180) )

		# X Y
		self.glFT.glBegin(OpenMayaRender.MGL_LINE_STRIP)
		for i in range( num ):
			#t       = math.sqrt( 1.0/ (cos[i]*cos[i]/(xPos*xPos)+sin[i]*sin[i]/(yPos*yPos)) )
			#self.glFT.glVertex3f( t*cos[i], t*sin[i], 0 )
			self.glFT.glVertex3f( xPos*cos[i], yPos*sin[i], 0 )
		self.glFT.glEnd()
		
		# X -Y
		self.glFT.glBegin(OpenMayaRender.MGL_LINE_STRIP)
		for i in range( num ):
			#t       = math.sqrt( 1.0/ (cos[i]*cos[i]/(xPos*xPos)+sin[i]*sin[i]/(yNeg*yNeg)) )
			self.glFT.glVertex3f( xPos*cos[i], yNeg*sin[i], 0 )
		self.glFT.glEnd()
		
		# X Z
		self.glFT.glBegin(OpenMayaRender.MGL_LINE_STRIP)
		for i in range( num ):
			#t       = math.sqrt( 1.0/ (cos[i]*cos[i]/(xPos*xPos)+sin[i]*sin[i]/(zPos*zPos)) )
			self.glFT.glVertex3f( xPos*cos[i], 0, zPos*sin[i] )
		self.glFT.glEnd()
		
		# X -Z
		self.glFT.glBegin(OpenMayaRender.MGL_LINE_STRIP)
		for i in range( num ):
			#t       = math.sqrt( 1.0/ (cos[i]*cos[i]/(xPos*xPos)+sin[i]*sin[i]/(zNeg*zNeg)) )
			self.glFT.glVertex3f( xPos*cos[i], 0, zNeg*sin[i] )
		self.glFT.glEnd()

		# -X Y
		self.glFT.glBegin(OpenMayaRender.MGL_LINE_STRIP)
		for i in range( num ):
			#t       = math.sqrt( 1.0/ (cos[i]*cos[i]/(xNeg*xNeg)+sin[i]*sin[i]/(yPos*yPos)) )
			self.glFT.glVertex3f( xNeg*cos[i], yPos*sin[i], 0 )
		self.glFT.glEnd()
		
		# -X -Y
		self.glFT.glBegin(OpenMayaRender.MGL_LINE_STRIP)
		for i in range( num ):
			#t       = math.sqrt( 1.0/ (cos[i]*cos[i]/(xNeg*xNeg)+sin[i]*sin[i]/(yNeg*yNeg)) )
			self.glFT.glVertex3f( xNeg*cos[i], yNeg*sin[i], 0 )
		self.glFT.glEnd()
		
		# -X Z
		self.glFT.glBegin(OpenMayaRender.MGL_LINE_STRIP)
		for i in range( num ):
			#t       = math.sqrt( 1.0/ (cos[i]*cos[i]/(xNeg*xNeg)+sin[i]*sin[i]/(zPos*zPos)) )
			self.glFT.glVertex3f( xNeg*cos[i], 0, zPos*sin[i] )
		self.glFT.glEnd()
		
		# -X -Z
		self.glFT.glBegin(OpenMayaRender.MGL_LINE_STRIP)
		for i in range( num ):
			#t       = math.sqrt( 1.0/ (cos[i]*cos[i]/(xNeg*xNeg)+sin[i]*sin[i]/(zNeg*zNeg)) )
			self.glFT.glVertex3f( xNeg*cos[i], 0, zNeg*sin[i] )
		self.glFT.glEnd()
		
		# Y Z
		self.glFT.glBegin(OpenMayaRender.MGL_LINE_STRIP)
		for i in range( num ):
			#t       = math.sqrt( 1.0/ (cos[i]*cos[i]/(yPos*yPos)+sin[i]*sin[i]/(zPos*zPos)) )
			self.glFT.glVertex3f( 0, yPos*cos[i], zPos*sin[i] )
		self.glFT.glEnd()
		
		# Y -Z
		self.glFT.glBegin(OpenMayaRender.MGL_LINE_STRIP)
		for i in range( num ):
			#t       = math.sqrt( 1.0/ (cos[i]*cos[i]/(yPos*yPos)+sin[i]*sin[i]/(zNeg*zNeg)) )
			self.glFT.glVertex3f( 0, yPos*cos[i], zNeg*sin[i] )
		self.glFT.glEnd()
		
		# -Y Z
		self.glFT.glBegin(OpenMayaRender.MGL_LINE_STRIP)
		for i in range( num ):
			#t       = math.sqrt( 1.0/ (cos[i]*cos[i]/(yNeg*yNeg)+sin[i]*sin[i]/(zPos*zPos)) )
			self.glFT.glVertex3f( 0, yNeg*cos[i], zPos*sin[i] )
		self.glFT.glEnd()
		
		# -Y -Z
		self.glFT.glBegin(OpenMayaRender.MGL_LINE_STRIP)
		for i in range( num ):
			#t       = math.sqrt( 1.0/ (cos[i]*cos[i]/(yNeg*yNeg)+sin[i]*sin[i]/(zNeg*zNeg)) )
			self.glFT.glVertex3f( 0, yNeg*cos[i], zNeg*sin[i] )
		self.glFT.glEnd()

	def get_fms(self):
		
		levels_plug     = self.node_Fn.findPlug( 'inLevels' )
		level_plug      = levels_plug.elementByLogicalIndex( self.inLevel_id )
		
		in_FM           = MM_to_FM( OpenMaya.MFnMatrixData(level_plug.child( 1 ).asMObject()).matrix() )
		goal_FM         = MM_to_FM( OpenMaya.MFnMatrixData(level_plug.child( 2 ).asMObject()).matrix() )
		
		return in_FM, goal_FM
	
	def get_dvDistance(self, in_FM, goal_FM):
		
		in_pos, goal_pos    = extract_translate(in_FM), extract_translate(goal_FM)
		distance_in_goal    = OpenMaya.MFloatVector( goal_pos[0]-in_pos[0], goal_pos[1]-in_pos[1], goal_pos[2]-in_pos[2] ).length()
		
		return distance_in_goal

	def get_useLimit(self):
		
		limits_plug     = self.node_Fn.findPlug( 'limits' )
		limit_plug      = limits_plug.elementByLogicalIndex( self.inLevel_id )
		
		useLimit_Plug   = limit_plug.child(0)
		
		return useLimit_Plug.asBool()

	def get_limitValues(self, dv ):
		
		limits_plug     = self.node_Fn.findPlug( 'limits' )
		limit_plug      = limits_plug.elementByLogicalIndex( self.inLevel_id )
		
		useLimit_Plug   = limit_plug.child(0)
		limitPos_Plug   = limit_plug.child(1)
		limitNeg_Plug   = limit_plug.child(2)
		
		useLimit        = useLimit_Plug.asBool()
		
		
		if useLimit:
			xPos, yPos, zPos    = get_3floats( limitPos_Plug )
			xNeg, yNeg, zNeg    = get_3floats( limitNeg_Plug )
		else :
			xPos, yPos, zPos    = dv, dv, dv
			xNeg, yNeg, zNeg    = -dv, -dv, -dv
		
		
		if xPos<e :     xPos=e
		if yPos<e :     yPos=e
		if zPos<e :     zPos=e
		if xNeg>-e :    xNeg=-e
		if yNeg>-e :    yNeg=-e
		if zNeg>-e :    zNeg=-e
		
		return useLimit,  xPos, xNeg, yPos, yNeg, zPos, zNeg
	
	def get_glMatrix(self, view, in_FM, goal_FM ):
		
		cam_DagPath     = OpenMaya.MDagPath()
		view.getCamera( cam_DagPath )
		cam_FM          = MM_to_FM( cam_DagPath.inclusiveMatrix() )
		
		translate_FM    = translate_to_FM( extract_translate( goal_FM * in_FM.inverse() ) )
		
		
		#
		final_FM        = translate_FM * in_FM * cam_FM.inverse()
		
		floatArray_ptr	= self.floatArray_to_ptr(  [ final_FM(i,j) for i in range(4) for j in range(4)]  )
		
		return floatArray_ptr

	"""
	def doPress(self, view ):
		# store screen position
		
		#self.lastXY     = self.get_mousePosition()
		
		pass
	"""

	def doDrag(self, view):

		useLimit    = self.get_useLimit()
		
		if not useLimit :
			return

		#
		activeName          = self.get_activeName()
		
		self.set_activeValue( view, activeName )

		# cursor
		#QtGui.QApplication.overrideCursor() != cursor
		if not self.cursor :
			#self.cursor     = QtGui.QCursor( QtCore.Qt.CrossCursor )
			self.cursor     = QtGui.QCursor( QtGui.QPixmap( ':/cursors/invisibleCursor.png' ), -1, -1 )
			
			QtWidgets.QApplication.setOverrideCursor( self.cursor )

	def doRelease(self, view):
		
		# delete cursor
		
		if self.cursor :
			QtWidgets.QApplication.restoreOverrideCursor()
			
			self.cursor = None

	def get_activeName(self):
		
		util            = OpenMaya.MScriptUtil()
		util.createFromInt( 0 )
		uInt_ptr        = util.asUintPtr()
		
		self.glActiveName( uInt_ptr )
		activeName      = util.getUint( uInt_ptr )
		
		return activeName
	
	def get_camera_wFM(self, view):
		
		cam_DagPath = OpenMaya.MDagPath()
		view.getCamera( cam_DagPath )
		
		cam_wFM     = MM_to_FM( cam_DagPath.inclusiveMatrix() )
		
		return cam_wFM

	def get_active_wPos(self, activeName, in_FM, goal_FM, activeValue ):
		
		translate_FM    = translate_to_FM( extract_translate( goal_FM * in_FM.inverse() ) )
		
		limit_FM        = self.get_activeFM( activeName, activeValue )
		
		
		final_FM        = limit_FM * translate_FM * in_FM
		
		return final_FM(3,0), final_FM(3, 1), final_FM(3, 2)

	def get_activeFM(self, activeName, activeValue ):
		
		if activeName == self.gl_xPos_name:
			return translate_to_FM( (activeValue, .0, .0) )
		
		elif activeName == self.gl_xNeg_name:
			return translate_to_FM( (activeValue, .0, .0) )
			
		elif activeName == self.gl_yPos_name:
			return translate_to_FM( (.0, activeValue, .0) )
		
		elif activeName == self.gl_yNeg_name:
			return translate_to_FM( (.0, activeValue, .0) )
		
		elif activeName == self.gl_zPos_name:
			return translate_to_FM( (.0, .0, activeValue) )
		
		elif activeName == self.gl_zNeg_name:
			return translate_to_FM( (.0, .0, activeValue) )

	def get_activeValue(self, currentId ):
		
		util            = OpenMaya.MScriptUtil()
		util.createFromInt( 0 )
		curr_ptr        = util.asDoublePtr()
		
		self.getDoubleValue( currentId, False, curr_ptr )
		currentValue    = util.getDouble( curr_ptr )
		
		return currentValue

	def set_activeValue(self, view, activeName ):
		
		
		in_FM, goal_FM  = self.get_fms()
		activeId        = self.get_activeId( activeName )
		
		activeValue     = self.get_activeValue(  activeId )

		# build a plan including activePoint   and parallel to cameraXY plan
		
		active_wPos     = self.get_active_wPos( activeName, in_FM, goal_FM, activeValue )
		
		camera_wFM      = self.get_camera_wFM( view  )
		normal_wFV      = OpenMaya.MFloatVector.zNegAxis * camera_wFM
		
		
		# wPlan,  d= -(ax1 + by1 + cz1 )   where x1 y1 z1 are a know point of the plane)
		a, b, c     = normal_wFV.x, normal_wFV.y, normal_wFV.z
		d           = -(a*active_wPos[0] + b*active_wPos[1] + c*active_wPos[2] )

		# now I want the intesection of my mouseRay with this plan
		rayStart_wPnt, ray_wMV    = OpenMaya.MPoint(), OpenMaya.MVector()
		self.mouseRayWorld( rayStart_wPnt, ray_wMV )
		
		# (x0 y0 z0)  is startPnt   and  (x y z) the normalized direction vector
		# solve t-sytem  z' + d = 0
		#                x' = x0 + t*x
		#                y' = y0 + t*y
		#                z' = z0 + t*z
		#   ---->  t =  - (d + ax0 + by0 + cz0) / (ax + by + cz) 
		
		t       = - ( d + a*rayStart_wPnt[0] + b*rayStart_wPnt[1] + c*rayStart_wPnt[2]) / (a*ray_wMV[0] + b*ray_wMV[1] + c*ray_wMV[2])
		
		intersect_wPnt  = OpenMaya.MFloatPoint( rayStart_wPnt.x + t*ray_wMV.x, rayStart_wPnt.y + t*ray_wMV.y, rayStart_wPnt.z + t*ray_wMV.z )

		# get the movement in world 3d,  then in in_FM space
		move_wFV        = OpenMaya.MFloatVector( intersect_wPnt[0]-active_wPos[0], intersect_wPnt[1]-active_wPos[1], intersect_wPnt[2]-active_wPos[2] )
		move_FV         = move_wFV * in_FM.inverse()

		# deduct the value to add to the currentValue   with a dot,   then setValue
		active_FV       = self.get_activeFV(  activeName)
		to_add          = move_FV * active_FV
		
		value           = self.limit_to_epsilon( activeName,  activeValue + to_add  )
		
		
		self.setDoubleValue( activeId, value )

	def get_activeFV( self, activeName):
		
		if activeName == self.gl_xPos_name:
			return OpenMaya.MFloatVector.xAxis
			
		elif activeName == self.gl_xNeg_name:
			return OpenMaya.MFloatVector.xAxis
			
		elif activeName == self.gl_yPos_name:
			return OpenMaya.MFloatVector.yAxis
		
		elif activeName == self.gl_yNeg_name:
			return OpenMaya.MFloatVector.yAxis
		
		elif activeName == self.gl_zPos_name:
			return OpenMaya.MFloatVector.zAxis
		
		elif activeName == self.gl_zNeg_name:
			return OpenMaya.MFloatVector.zAxis

	def get_activeId(self, activeName):
		
		if activeName == self.gl_xPos_name:
			return self.xPos_id
			
		elif activeName == self.gl_xNeg_name:
			return self.xNeg_id
			
		elif activeName == self.gl_yPos_name:
			return self.yPos_id
		
		elif activeName == self.gl_yNeg_name:
			return self.yNeg_id
		
		elif activeName == self.gl_zPos_name:
			return self.zPos_id
		
		elif activeName == self.gl_zNeg_name:
			return self.zNeg_id
		
		else :
			return None

	def limit_to_epsilon(self, activeName, value ):
		
		if (activeName in (self.gl_xPos_name, self.gl_yPos_name, self.gl_zPos_name))  and  (value<e)  :
			return e
		
		elif (activeName in (self.gl_xNeg_name, self.gl_yNeg_name, self.gl_zNeg_name)) and (value>e):
			return e
		
		else :
			return value

	def get_mousePosition(self):
		
		x_util      = OpenMaya.MScriptUtil()
		x_util.createFromInt( 0 )
		x_ptr       = x_util.asShortPtr()
		y_util      = OpenMaya.MScriptUtil()
		y_util.createFromInt( 0 )
		y_ptr       = y_util.asShortPtr()
		
		self.mousePosition( x_ptr, y_ptr )
		
		x       = x_util.getShort( x_ptr )
		y       = y_util.getShort( y_ptr )
		
		return x, y
	

def initializePlugin( mObj ):
	mPlugin = OpenMayaMPx.MFnPlugin(mObj, "Hans Godard -- zapan669@hotmail.com", "3.0", "Any")
	try:
		mPlugin.registerContextCommand( LimitCtx_cmd.cmdName, LimitCtx_cmd.creator )
	except:
		OpenMaya.MGlobal.displayError("Failed to register context command: %s" % LimitCtx_cmd.cmdName )
		raise
	try:
		mPlugin.registerNode( LimitManip.kPluginNodeName, LimitManip.kPluginNodeId, LimitManip.nodeCreator, LimitManip.nodeInitializer, OpenMayaMPx.MPxNode.kManipulatorNode)
	except:
		OpenMaya.MGlobal.displayError( "Failed to register node: %s" % LimitManip.kPluginNodeName )
		raise
	try:
		mPlugin.registerNode( DynamicChain.kPluginNodeName, DynamicChain.kPluginNodeId, DynamicChain.nodeCreator, DynamicChain.nodeInitializer )
	except:
		OpenMaya.MGlobal.displayError( "Failed to register command: %s\n" % DynamicChain.kPluginNodeName )
		raise


def uninitializePlugin( mObj ):
	mPlugin = OpenMayaMPx.MFnPlugin(mObj)
	try:
		mPlugin.deregisterContextCommand(LimitCtx_cmd.cmdName)
	except:
		OpenMaya.MGlobal.displayError("Failed to deregister context command: %s" % LimitCtx_cmd.cmdName )
		raise
	try:
		mPlugin.deregisterNode( LimitManip.kPluginNodeId )
	except:
		OpenMaya.MGlobal.displayError( "Failed to unregister node: %s\n" % LimitManip.kPluginNodeName )
		raise
	try:
		mPlugin.deregisterNode( DynamicChain.kPluginNodeId )
	except:
		OpenMaya.MGlobal.displayError( "Failed to unregister node: %s\n" % DynamicChain.kPluginNodeName )
		raise
