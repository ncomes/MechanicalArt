#include "retargetShapes.h"

#include "component.h"
#include "shading.h"
#include "object.h"
#include "miscUtil.h"

#include <cmath>
#include <iostream>

#include <maya/MGlobal.h>
#include <maya/MArgDatabase.h>

#include <maya/MPoint.h>
#include <maya/MFloatVectorArray.h>

#include <maya/MFnDagNode.h>

#include <maya/MFnTransform.h>
#include <maya/MTransformationMatrix.h>


MString			RetargetShapes::name(  "retargetShapes" );



void* RetargetShapes::creator()
{
	return new RetargetShapes();
}



bool RetargetShapes::isUndoable() const
{
	return true;
}



MSyntax RetargetShapes::newSyntax()
{
	MSyntax syntax;
	
	syntax.setMinObjects( 3 ) ;
	syntax.setMaxObjects( 5 ) ;

	return syntax ;
}




MStatus RetargetShapes::get_args( const MArgList& args )
{
	MStatus status	= MStatus::kSuccess;

	unsigned int numArgs	= args.length() ;

	if ((numArgs<3) || (numArgs>6))
	{
		MGlobal::displayInfo( "Arguments are : string sourceMesh, stringArray sourceShapes, string targetMesh, \n\tThen optional Arguments are : bool static_sphere, intArray fromVertices, intArray toVertices" );
		return MStatus::kFailure ;
	}



	// set argument order
	unsigned int s_idx		= 0 ;
	unsigned int ss_idx		= 1 ;
	unsigned int t_idx		= 2 ;
	unsigned int volume_idx	= 3 ;
	unsigned int from_idx	= 4 ;
	unsigned int to_idx		= 5 ;



	// Args needed
	MString sourceTmp	= args.asString( s_idx, &status ) ;

	if (status!=MStatus::kSuccess) {
		MGlobal::displayInfo( "First argument must be sourceMesh ( string )" );
		return MStatus::kFailure ; }

	MString targetTmp	= args.asString( t_idx, &status ) ;

	if (status!=MStatus::kSuccess) {
		MGlobal::displayInfo( "Third argument must be target ( string )" );
		return MStatus::kFailure ; }

	MStringArray sourceShapesTmp	= args.asStringArray( ss_idx, &status ) ;

	if (status!=MStatus::kSuccess) {
		MGlobal::displayInfo( "Second argument must be sourceShapes ( stringArray )" );
		return MStatus::kFailure ; }


	// Optionnal Args
	bool volumeTmp	= args.asBool( volume_idx, &status ) ;

	if (status==MStatus::kSuccess)
	{		static_sphere	= volumeTmp ; }
	else {	static_sphere	= false ; }


	MIntArray fromVtxTmp	= args.asIntArray( from_idx, &status ) ;

	if (status==MStatus::kSuccess)
	{		fromVtx_ids	= fromVtxTmp ; }
	//else { }

	MIntArray toVtxTmp		= args.asIntArray( to_idx, &status ) ;

	if (status==MStatus::kSuccess)
	{		toVtx_ids	= toVtxTmp ; }
	//else { }




	// secu : number of shapes
	int numShapes	= sourceShapesTmp.length() ;

	if (numShapes <1) {
		MGlobal::displayInfo( "Second argument (stringArray) must have size >=1" );
		return MStatus::kFailure ; }

	// secu : usedVertices must be 0 (then will be filled with all vertices later  or  >3
	int fromVertices_num	= fromVtx_ids.length() ;
	if ((fromVertices_num >0 ) && (fromVertices_num <3)) {
		MGlobal::displayInfo( "5th argument (intArray) must have size == 0  or > 3" );
		return MStatus::kFailure ; }

	int toVertices_num		= toVtx_ids.length() ;
	if ((toVertices_num >0 ) && (toVertices_num <3)) {
		MGlobal::displayInfo( "6th argument (intArray) must have size == 0  or > 3" );
		return MStatus::kFailure ; }



	// check if all exist  and if all are mesh shapes
	MStringArray checkThem( sourceShapesTmp ) ;
	checkThem.insert( targetTmp, 0 );
	checkThem.insert( sourceTmp, 0 );


	MObjectArray objs ;
	status	= get_Objs_from_names( checkThem, objs, MFn::kMesh ) ;


	if (status!=MStatus::kSuccess)
	{
		return MStatus::kFailure ;
	} 



	// if all is ok,  store names + objs
	sourceName			= sourceTmp ;
	targetName			= targetTmp ;
	sourceShapeNames	= sourceShapesTmp ;

	source_Obj			= objs[0] ;
	target_Obj			= objs[1] ;

	sourceShape_Objs	= MObjectArray( objs ); // copy then remove source and target
	sourceShape_Objs.remove(0);
	sourceShape_Objs.remove(0);



	//
	return status ;
}



MStatus RetargetShapes::doIt( const MArgList& args )
//	Return Value:
//		MS::kSuccess - command succeeded
//		MS::kFailure - command failed (returning this value will cause the 
//                     MEL script that is being run to terminate unless the
//                     error is caught using a "catch" statement.
//
{
	// store datas into class
	MStatus status	= get_args( args );

	if (status!=MStatus::kSuccess)
	{
		return status;
	}


	// Typically, the doIt() method only collects the infomation required
	// to do/undo the action and then stores it in class members.  The 
	// redo method is then called to do the actuall work.  This prevents
	// code duplication.
	return redoIt();
}






Eigen::MatrixXd RetargetShapes::get_distanceMatrix( MIntArray& ids )
{
	int dim	= ids.length() ;

	Eigen::MatrixXd MM( dim, dim ) ;


	for (int i=0 ; i<dim; i++)
	{
		for (int j=i ; j<dim; j++)
		{
			if (i==j)
			{
				MM(i,j)	= .0 ;
			}
			else
			{
				MM(i,j)	= sqrt( (all_src_Pnts[ids[j]][0]-all_src_Pnts[ids[i]][0])*(all_src_Pnts[ids[j]][0]-all_src_Pnts[ids[i]][0])+(all_src_Pnts[ids[j]][1]-all_src_Pnts[ids[i]][1])*(all_src_Pnts[ids[j]][1]-all_src_Pnts[ids[i]][1])+(all_src_Pnts[ids[j]][2]-all_src_Pnts[ids[i]][2])*(all_src_Pnts[ids[j]][2]-all_src_Pnts[ids[i]][2])) ;
				MM(j,i)	= MM(i,j) ;
			}
		}
	}

	return MM ;
}




MStatus RetargetShapes::build_solver( MIntArray& ids, Eigen::MatrixXd& out_X  )
// fill mXs
{
	
	int dim	= ids.length() ;


	// LU  +  solve
	Eigen::PartialPivLU<Eigen::MatrixXd> LU	= distanceMatrix.partialPivLu() ;

	Eigen::MatrixXd Y( dim, 3 ) ;


	for (int ii=0 ; ii<dim; ii++)
	{
		Y(ii,0) = all_tgt_Pnts[ids[ii]].x ;
		Y(ii,1) = all_tgt_Pnts[ids[ii]].y ;
		Y(ii,2) = all_tgt_Pnts[ids[ii]].z ;
	}

	out_X	= LU.solve( Y ) ;

	//
	return MStatus::kSuccess ;
}




void RetargetShapes::compute_points( MPointArray& pnts, MIntArray& ids )
{

	int used_shape_numPnt	= ids.length() ;

	
	//// debug

	int ids_len = pnts.length() ;

	/////



	
	for (int jj=0 ; jj<used_shape_numPnt; jj++)
	{

		int jId			= ids[jj] ;
		
		double new3[3]	= {.0,.0,.0};
		

		for (int ii=0 ; ii<matrixDim; ii++)
		{
			// pnts = shape_pnts
			double d	= sqrt( (pnts[jId][0]-all_src_Pnts[nKeyIds[ii]][0])*(pnts[jId][0]-all_src_Pnts[nKeyIds[ii]][0])+(pnts[jId][1]-all_src_Pnts[nKeyIds[ii]][1])*(pnts[jId][1]-all_src_Pnts[nKeyIds[ii]][1])+(pnts[jId][2]-all_src_Pnts[nKeyIds[ii]][2])*(pnts[jId][2]-all_src_Pnts[nKeyIds[ii]][2])) ;
			
			new3[0]    +=  ( d * X(ii,0) ) ;
			new3[1]    +=  ( d * X(ii,1) ) ;
			new3[2]    +=  ( d * X(ii,2) ) ;
		}
		
		pnts.set( jId, new3[0], new3[1], new3[2] ) ;
	}

}




MStatus RetargetShapes::redoIt()
//	No arguments are passed in as all of the necessary information is cached by the doIt method.
//	Return Value: MS::kSuccess  or  MS::kFailure
{

	#ifdef RELEASE_OPENMP
		MThreadUtils::syncNumOpenMPThreads();
	#endif


	MStatus status		= MStatus::kSuccess;
	MSpace::Space space	= MSpace::kObject ;



	// get objs
	MObject source_Obj ;
	status			= get_Obj_from_name( sourceName, source_Obj, MFn::kMesh );


	int numShape	= sourceShapeNames.length() ;

	MObjectArray shape_Objs ;
	status			= get_Objs_from_names( sourceShapeNames, shape_Objs, MFn::kMesh ) ;

	newTr_names.setLength( numShape ) ;


	
	// get ALL source+target points    and  used source+target points
	MFnMesh source_Msh( source_Obj ) ;
	MFnMesh target_Msh( target_Obj ) ;

	all_src_Pnts	= get_msh_points( source_Msh, space );
	all_tgt_Pnts	= get_msh_points( target_Msh, space );
	
	int src_len		= all_src_Pnts.length() ;
	int tgt_len		= all_tgt_Pnts.length() ;


	int	fromVtx_len ;

	if (fromVtx_ids.length() ==0) {
		fromVtx_len		= src_len ;
		fromVtx_ids		= range( src_len ) ; }
	else {
		fromVtx_len		= fromVtx_ids.length() ; }



	// secu
	if (src_len != tgt_len) {
		MGlobal::displayError( "RetargetShapes failed : Source and Target dont have the same vertexNum" ) ;
		return MStatus::kFailure ; }

	std::cout << "RetargetShapes : " << fromVtx_len << "/" << src_len << " Vertices used" << std::endl ;



	// add sphere points in the all_ containers
	// and update all_ dimensions
	
	if (static_sphere==true)
	{
		int sphere_len		= 300 ;
		build_spheres(	all_src_Pnts, all_tgt_Pnts,  source_Obj, shape_Objs, target_Obj, sphere_len  ) ;

		//
		fromVtx_ids.setLength( fromVtx_len + sphere_len );

		for (int ii=0; ii<sphere_len; ii++) {
			fromVtx_ids[fromVtx_len+ii]	= src_len + ii ;  }

		fromVtx_len		+= sphere_len ;
	}
	

	matrixDim	= fromVtx_len ;
	nKeyIds.copy( fromVtx_ids );


	// distance between all src elements
	distanceMatrix		= get_distanceMatrix( fromVtx_ids ) ;


	//
	std::cout<<"RetargetShapes : Solving "<<sourceName<<" / "<<targetName<< " ..." << std::endl ;
	DWORD dwTickCount = GetTickCount();

	build_solver( fromVtx_ids, X ) ;
	
	std::cout << "RetargetShapes : Done in " <<  (double)(GetTickCount() - dwTickCount)/1000.0 << " sec" << std::endl ;



	for (int ss=0 ; ss<numShape; ss++)
	{

		// get shape as Mesh
		MFnMesh shape_Msh( shape_Objs[ss] ) ;
		MPointArray shape_Pnts	= get_msh_points( shape_Msh, space );
		

		// build new points,  override shape_pnts because ne need to do a copy here

		if (toVtx_ids.length() ==0)
		{
			compute_points( shape_Pnts, range( shape_Msh.numVertices() ) ) ; }
		else
		{	compute_points( shape_Pnts, toVtx_ids ) ; }

		
		
		// copy shape, a transform is automatically built  during the copy  because no data is specified
		// ( cant copy from target because if shape doesnt have same topology ?  so copy from shape )
		MFnMesh new_Msh ;
		MObject tr_Obj	= new_Msh.copy( shape_Objs[ss] ) ;


		// set new points  ( +  set normal if same topo ) 
		new_Msh.setPoints(  shape_Pnts, MSpace::kObject   ) ;

		
		
		// same local matrix as the input shape
		MFnDagNode shape_DagNode( shape_Objs[ss] ) ;

		MFnTransform shape_Tr( shape_DagNode.parent( 0 )  ) ;
		MTransformationMatrix shape_Transfo = shape_Tr.transformation() ;

		MFnTransform tr_Tr( tr_Obj );
		tr_Tr.set( shape_Transfo  ) ;


		// store new transform.name for returnCmd
		newTr_names[ss]	= MFnDependencyNode( tr_Obj ).name();


		//printf( "RetargetShapes : Shape built %d/%d\n", (ss+1), numShape ) ;
		std::cout << "RetargetShapes : Shape built " <<  (ss+1) << "/" << numShape << std::endl ;
	}



	// returnCmd + print
	setResult(  newTr_names  ) ;

	MGlobal::displayInfo( "RetargetShapes : Done" );

	return MS::kSuccess;
}







MStatus RetargetShapes::undoIt()
//
//	Description:
//		implements undo for the MEL RetargetShapes command.  
//
//		This method is called to undo a previous command of this type.  The 
//		system should be returned to the exact state that it was it previous 
//		to this command being executed.  That includes the selection state.
//
//	Return Value:
//		MS::kSuccess - command succeeded
//		MS::kFailure - redoIt failed.  this is a serious problem that will
//                     likely cause the undo queue to be purged
//
{

	// get trs objects
	MObjectArray tr_Objs ;
	MStatus status		= get_Objs_from_names( newTr_names, tr_Objs, MFn::kTransform ) ;



	// simply delete all the new transforms
	for (unsigned int ii=0 ; ii<tr_Objs.length(); ii++)
	{
		MGlobal::deleteNode( tr_Objs[ii] );
	}



	//
    MGlobal::displayInfo( "RetargetShapes : Undone\n" );

	return MS::kSuccess;
}



