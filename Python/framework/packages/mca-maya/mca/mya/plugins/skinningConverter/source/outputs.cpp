
#include "skinningDecomposition.h"




void SkinningDecomposition::output_weights( MFnDependencyNode& storage_Dep )
{

	// elementByLogicalIndex is NOT threadsafe
	//--------------------------------------

	MPlug weightIds_Plug	= storage_Dep.findPlug( "weightIds", true  );
	MPlug weights_Plug		= storage_Dep.findPlug( "weights", true  );



	// weights and weightIds
	for (int vv=0 ; vv<inputs.V ; vv++)
	{
		int& vId	= inputs.vertexIds[vv] ;

		MIntArray vertex_jIds_MI ; // conflict with class object
		intVec_to_MIntArray( outputs.vertex_jIds[ vId ], vertex_jIds_MI );

		MDoubleArray vertex_wgts_MD ;
		doubleVec_to_MDoubleArray( outputs.vertex_wgts[ vId ], vertex_wgts_MD );

		MObject weightIds_obj		= MFnIntArrayData().create( vertex_jIds_MI );
		MObject weights_obj			= MFnDoubleArrayData().create( vertex_wgts_MD  );

		weightIds_Plug.elementByLogicalIndex( vId ).setMObject( weightIds_obj );
		weights_Plug.elementByLogicalIndex( vId ).setMObject( weights_obj );
	}

}



void SkinningDecomposition::output_matrices()
{
	
	// need target dagPaths for frame0 + frames
	MObjectArray targetJoints_Obj ;
	get_Objs( inputs.targetJoints, targetJoints_Obj, MFn::kTransform );

	MDagPathArray targetJoints_Path ;
	targetJoints_Path.setLength( inputs.J );

	MDagPathArray targetParents_Path ; 
	targetParents_Path.setLength( inputs.J );



	// go to frame0
	// store parent path for each target, it can be nothing ( the world path )
	// disconnect  input connections if there are : fill a big Modifier by all the 'disconnectAttr' commands
	
	MTime::Unit uiUnit	= MTime::uiUnit() ;
	MTime time0( inputs.frame0, uiUnit  );
	MAnimControl::setCurrentTime( time0 ) ;

	MDGModifier modifier ;
	MStringArray attrs_to_disconnect	= attribute_strings_to_disconnect() ;


	for (int jj=0; jj<inputs.J; jj++)
	{
		MFnDagNode target_Dag( targetJoints_Obj[jj] );
		target_Dag.getPath( targetJoints_Path[jj] );

		MFnDagNode( target_Dag.parent(0)).getPath( targetParents_Path[jj] );

		disconnect_input_connections( target_Dag, attrs_to_disconnect, modifier );
	}

	modifier.doIt() ;
	


	// store rotateOrders
	// create animCurves
	// set frame0 matrices

	EulerRoVec rotateOrders( inputs.J ) ;
	MObjectVecVec animCurves( inputs.J ) ;														// dim J then 6
	MStringArray attrs_to_animate	= attribute_strings_to_animate( inputs.rigidMatrices ) ;	// dim 6 or 12


	for (int jj=0; jj<inputs.J; jj++)
	{
		MFnTransform target_Tr( targetJoints_Path[jj] ) ;


		TransfoRo ro		= target_Tr.rotationOrder() ;
		rotateOrders[jj]	= TransfoRo_to_EulerRo( ro );

		create_animCurves(  target_Tr, attrs_to_animate, animCurves[jj]  ); // MFnTransform herits from MFnDagNode
		

		MMatrix target_MM	= outputs.bindingMMs[jj].inverse() * targetParents_Path[jj].inclusiveMatrixInverse() ;

		set_animCurves( target_MM, animCurves[jj], rotateOrders[jj], time0 );
	}



	// set framesMMs
	//

	for (int ff=0; ff<inputs.F; ff++)
	{

		MTime time( inputs.frames[ff], uiUnit ) ;
		MAnimControl::setCurrentTime( time ) ;


		for (int jj=0; jj<inputs.J; jj++)
		{
			
			// if no parent, set worldSpace matrix
			// else set  frameMM * parent.inverse
			MMatrix target_MM	= outputs.framesMMs[ff][jj] * targetParents_Path[jj].inclusiveMatrixInverse() ;

			set_animCurves( target_MM, animCurves[jj], rotateOrders[jj], time );
		}
	}


}



void SkinningDecomposition::output_error( MFnDependencyNode& storage_Dep )
{
	MPlug error_Plug	= storage_Dep.findPlug( "error", true  );
	error_Plug.setDouble( outputs.errors.back() );

	MPlug iterDone_Plug	= storage_Dep.findPlug( "iterationDone", true  );
	iterDone_Plug.setInt( outputs.iterationDone );
}


























