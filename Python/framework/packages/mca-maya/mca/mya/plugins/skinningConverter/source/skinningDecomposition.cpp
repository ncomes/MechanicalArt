

#include "skinningDecomposition.h"




MString		SkinningDecomposition::name( "skinningDecomposition" );




void* SkinningDecomposition::creator()
{
	return new SkinningDecomposition();
}

bool SkinningDecomposition::isUndoable() const
{
	return true;
}




MSyntax SkinningDecomposition::newSyntax()
{
	
	MSyntax syntax;
	

	// args
	syntax.setMinObjects( 1 ) ;
	syntax.setMaxObjects( 1 ) ;

	syntax.addFlag( "sn", "storageNode",  MSyntax::kString  );
	
	return syntax ;
}



MStatus SkinningDecomposition::get_args( const MArgList& args )
{

	MStatus status	= MStatus::kSuccess;


	MArgParser parser( syntax(), args  );


	

	// get storage node
	if (parser.isFlagSet( "storageNode") == false){
		return MS::kNotFound ;}


	MObject storage_Obj ;
	parser.getFlagArgument( "storageNode", 0, storage_name );
	

	if ( get_Obj( storage_name, storage_Obj, MFn::kBase ) != MS::kSuccess ){
		return MS::kUnknownParameter ;}





	//-------------------------------------------------------------------
	// check if all "inputs" needed Attributes  are built and filled
	// and extract datas into "inputs" structure
	
	

	MFnDependencyNode storage_Dep( storage_Obj  );

	

	// frames  ( doubleArray )
	MPlug frames_Plug		= storage_Dep.findPlug( "frames", true, &status );
	if (status!= MS::kSuccess){
		MGlobal::displayError( "Need attribute on storageNode : doubleArray 'frames'" );
		return MS::kFailure; }

	MFnDoubleArrayData frames_DoubleData(  frames_Plug.asMObject() ) ;

	int allFrames_num		= frames_DoubleData.length();

	if (allFrames_num < 2){
		MGlobal::displayError( "numFrame < 2,  need 1 restShape and 1+ shapes" );
		return MS::kFailure; }

	inputs.allFrames	= frames_DoubleData.array( &status );

	if (is_unique_MDoublerray(inputs.allFrames)==false){
		MGlobal::displayError( "Duplicates found in Frames !" );
		return MS::kFailure; }


	inputs.frame0		= inputs.allFrames[0] ;

	inputs.frames		= inputs.allFrames ;
	inputs.frames.remove( 0 ) ;

	inputs.AF			= allFrames_num ;
	inputs.F			= allFrames_num - 1 ;




	// source joints  ( stringArray )
	// they must be animated
	MPlug sourceJoints_Plug	= storage_Dep.findPlug( "sourceJoints", true, &status );
	if (status!= MS::kSuccess){
		MGlobal::displayError( "Need attribute on storageNode : stringArray 'sourceJoints'" );
		return MS::kFailure; }

	MFnStringArrayData sourceJoints_StringData(  sourceJoints_Plug.asMObject() ) ;

	inputs.J		= sourceJoints_StringData.length();

	if (inputs.J<1){
		MGlobal::displayError( "num sourceJoint J < 1" );
		return MS::kFailure; }
	

	MStringArray sourceJoints_MSs	= sourceJoints_StringData.array( &status );

	MStringArray_to_MStringVec( sourceJoints_MSs,  inputs.sourceJoints );


	if (is_unique_MStringArray(sourceJoints_MSs)==false){
		MGlobal::displayError( "Duplicates found in sourceJoints !" );
		return MS::kFailure; }


	MObjectArray sourceJoints_Obj ;
	get_Objs( inputs.sourceJoints, sourceJoints_Obj, MFn::kTransform );




	// iteration max
	MPlug iteration_Plug		= storage_Dep.findPlug( "maxIteration", true, &status );
	if (status!= MS::kSuccess){
		MGlobal::displayError( "Need attribute on storageNode : int 'maxIteration'" );
		return status ;}

	inputs.maxIteration			= iteration_Plug.asInt() ;

	if (inputs.maxIteration <= 0 ) {
		inputs.maxIteration		= 1000 ; }



	// iterationFullSolver  +  updateRestMatrices
	if (inputs.maxIteration == 1)
	{
		// NOT USED
		inputs.iterationFullSolver	= 0 ;
		inputs.updateRestMatrices	= false ;
		inputs.rigidMatrices		= true ;
		inputs.errorPercentBreak	= -1.0 ;
	}
	else
	{
		// iterationFullSolver
		MPlug iterationFullSolver_Plug	= storage_Dep.findPlug( "iterationFullSolver", true, &status );
		if (status!= MS::kSuccess){
			MGlobal::displayError( "Need attribute on storageNode : int 'iterationFullSolver'" );
			return status ;}

		inputs.iterationFullSolver	= iterationFullSolver_Plug.asInt() ;


		if (inputs.iterationFullSolver <= 0) {
			MGlobal::displayError( "iterationFullSolver <= 0, it must be >= 1" ); }

		if (inputs.iterationFullSolver > inputs.maxIteration) {
			MGlobal::displayError( "iterationFullSolver > maxIteration, bad" );
			return MS::kFailure; }


		// updateRestMatrices
		MPlug updateRestMatrices_Plug	= storage_Dep.findPlug( "updateRestMatrices", true, &status );
		if (status!= MS::kSuccess){
			MGlobal::displayError( "Need attribute on storageNode : bool 'updateRestMatrices'" );
			return status ;}

		inputs.updateRestMatrices	= updateRestMatrices_Plug.asBool() ;


		// rigid flexible ?
		MPlug rigid_Plug		= storage_Dep.findPlug( "rigidMatrices", true, &status );
		if (status!= MS::kSuccess){
			MGlobal::displayError( "Need attribute on storageNode : bool 'rigidMatrices'" );
			return status ;}

		inputs.rigidMatrices	= rigid_Plug.asBool() ;


		// errorPercentBreak  ( 1% )
		// usuned if negative, so it means interate until maxIteration
		MPlug errorPercentBreak_Plug	= storage_Dep.findPlug( "errorPercentBreak", true, &status );
		if (status!= MS::kSuccess){
			MGlobal::displayError( "Need attribute on storageNode : double 'errorPercentBreak'" );
			return status ;}

		inputs.errorPercentBreak	= errorPercentBreak_Plug.asDouble() ;
	}
	



	// setMatrices,  set matrices on the target Joints at the end, or not.
	// target joints  ( stringArray ), if they are, check them.
	// they must NOT be animated, anyway I will disconnect the inputs if there are ...


	MPlug setMatrices_Plug	= storage_Dep.findPlug( "setMatrices", true, &status );
	if (status!= MS::kSuccess){
		MGlobal::displayError( "Need attribute on storageNode : bool 'setMatrices'" );
		return MS::kFailure; }

	inputs.setMatrices		= setMatrices_Plug.asBool() ;


	if (inputs.setMatrices)
	{
		MPlug targetJoints_Plug	= storage_Dep.findPlug( "targetJoints", true, &status );
		if (status!= MS::kSuccess){
			MGlobal::displayError( "Need attribute on storageNode : stringArray 'targetJoints'" );
			return MS::kFailure; }

		MFnStringArrayData targetJoints_StringData(  targetJoints_Plug.asMObject() ) ;

		int targetJoints_num	= targetJoints_StringData.length();

		if (inputs.J != targetJoints_num){
			MGlobal::displayError( "num targetJoint != num sourceJoint" );
			return MS::kFailure; }


		MStringArray targetJoints_MSs	= targetJoints_StringData.array( &status );

		MStringArray_to_MStringVec( targetJoints_MSs,  inputs.targetJoints );


		if (is_unique_MStringArray(targetJoints_MSs)==false){
			MGlobal::displayError( "Duplicates found in targetJoints !" );
			return MS::kFailure; }


		MObjectArray targetJoints_Obj ;
		get_Objs( inputs.targetJoints, targetJoints_Obj, MFn::kTransform );
	}
	else
	{
		// unused
		inputs.targetJoints.resize( 0 ) ;
	}




	// vertex ids   ( intArray )
	MPlug vertexIds_Plug		= storage_Dep.findPlug( "vertexIds", true, &status );
	if (status!= MS::kSuccess){
		MGlobal::displayError( "Need attribute on storageNode : intArray 'vertexIds'" );
		return MS::kFailure; }

	MFnIntArrayData vertexIds_IntData(  vertexIds_Plug.asMObject() ) ;

	inputs.V		= vertexIds_IntData.length();

	if (inputs.V<=0){
		MGlobal::displayError( "Used numVertex V <= 0" );
		return MS::kFailure; }

	inputs.vertexIds	= vertexIds_IntData.array( &status );
	//MIntArray vertexIds	= vertexIds_IntData.array( &status );

	if (is_unique_MIntArray(inputs.vertexIds)==false){
		MGlobal::displayError( "Duplicates found in vertexIds !" );
		return MS::kFailure ;}

	//MIntArray_to_intVec( vertexIds, inputs.vertexIds ); // because bug with openMP




	// max influence
	// this will be ignored if an existingSlinCluster is used
	MPlug maxInf_Plug		= storage_Dep.findPlug( "maxInfluence", true, &status );
	if (status!= MS::kSuccess){
		MGlobal::displayError( "Need attribute on storageNode : int 'maxInfluence'" );
		return status ;}

	inputs.MI		= maxInf_Plug.asInt() ;
	
	if ((inputs.MI < 1) || ( inputs.MI > inputs.J )){
		MGlobal::displayError( "maxInfluence < 1 || maxInfluence > J " );
		return MS::kInvalidParameter ;}
	



	// lagragian
	MPlug lagragian_Plug		= storage_Dep.findPlug( "lagragian", true, &status );
	if (status!= MS::kSuccess){
		MGlobal::displayError( "Need attribute on storageNode : double 'lagragian'" );
		return status ;}

	inputs.lagragian	= lagragian_Plug.asDouble();

	if (inputs.lagragian <= .0){
		MGlobal::displayError( "lagragian <= .0" );
		return status ;}
	

	




	// Animated Shape  ( string attr )
	// need dagPath otherwise MFnMesh::getPoints( kWorld ) does not work
	MPlug shape_Plug		= storage_Dep.findPlug( "shape", true, &status );
	if (status!= MS::kSuccess){
		MGlobal::displayError( "Need attribute on storageNode : string 'shape'" );
		return status ;}

	inputs.shape_name		= shape_Plug.asString() ;


	MObject shape_Obj ;
	status		= get_Obj( inputs.shape_name, shape_Obj, MFn::kMesh );
	if ( status != MS::kSuccess ){
		return status ;}


	MDagPath shape_Path ; 
	MFnDagNode( shape_Obj ).getPath( shape_Path );





	// get ALL RestPoints and ALL ShapesPoints
	// because it is faster and easier to deal with vertexIds later

	MTime::Unit uiUnit	= MTime::uiUnit() ;
	startTime			= MAnimControl::currentTime();

	MAnimControl::setCurrentTime( MTime( inputs.frame0, uiUnit ) ) ; // back in outputs functions


	
	// points and bindingMatrices at frame0
	MFnMesh msh_f0( shape_Path );
	msh_f0.getPoints( inputs.rest_Pnts, space );

	MDagPathArray sourceJoints_Path ;
	sourceJoints_Path.setLength( inputs.J );

	outputs.bindingMMs.resize( inputs.J );


	for (int jj=0; jj<inputs.J; jj++)
	{
		MFnDagNode( sourceJoints_Obj[jj] ).getPath( sourceJoints_Path[jj] );
		outputs.bindingMMs[jj]		= sourceJoints_Path[jj].inclusiveMatrixInverse() ;
	}



	// points and matrices at frames
	// boundingBox is needed by the error computation
	inputs.frames_Pnts.resize( inputs.F );
	outputs.framesMMs.resize( inputs.F );

	inputs.boundingBox_diagonal_sum		= .0 ;


	for (int ff=0; ff<inputs.F; ff++)
	{
		double& frame	= inputs.frames[ff] ;
		MAnimControl::setCurrentTime( MTime( frame, uiUnit ) ) ;


		// get mesh points
		inputs.frames_Pnts[ff]	= MPointArray();
		MFnMesh msh_ff( shape_Path );
		msh_ff.getPoints( inputs.frames_Pnts[ff], space ); 

		// boundinBox
		MMatrix msh_ff_wMM		= shape_Path.inclusiveMatrix() ;
		MBoundingBox bb			= msh_ff.boundingBox();
		bb.transformUsing( msh_ff_wMM );
		inputs.boundingBox_diagonal_sum		+= (bb.max() - bb.min()).length() ;

		// get joints matrices
		outputs.framesMMs[ff].resize( inputs.J );
		for (int jj=0; jj<inputs.J; jj++)
		{
			outputs.framesMMs[ff][jj]	= sourceJoints_Path[jj].inclusiveMatrix() ;
		}
	}





	// if an existing SkinCluster name is specified,
	// use the existing jointIds per vertex  to speed up the process.
	// So basically this will build an improved version of this existing skinning.
	MPlug existingSkinCluster_Plug		= storage_Dep.findPlug( "existingSkinCluster", true, &status );
	if (status!= MS::kSuccess){
		MGlobal::displayError( "Need attribute on storageNode : string 'existingSkinCluster'" );
		return status ;}

	MString existingSkinCluster_name	= existingSkinCluster_Plug.asString();


	if (existingSkinCluster_name.length() > 0)
	{
		inputs.useExistingSkinCluster	= true ;

		MObject skinCluster_Obj ;
		status		= get_Obj( existingSkinCluster_name, skinCluster_Obj, MFn::kSkinClusterFilter );
		if ( status != MS::kSuccess ){
			return MS::kFailure ;}
		
		
		// check if the Source_joints are included in the existingSkinCluster
		// they can be in a different order, this is allowed
		MFnSkinCluster skinCluster_Fn( skinCluster_Obj  );

		MDagPathArray existingJoints_Path ;

		int numExisting_inf		= skinCluster_Fn.influenceObjects( existingJoints_Path, &status ) ;
		if ((inputs.J > numExisting_inf) || (status != MS::kSuccess)){
			MGlobal::displayError( "inputs.J > numExisting_inf" );
			return MS::kFailure ;}


		// I want per-vertex jIds,  I need also their weights to choose the biggest inf
		std::map<int, pq_pairDbleInt> qs ;

		for (int vv=0 ; vv<inputs.V ; vv++)
		{
			int& vId	= inputs.vertexIds[vv] ;
			qs[vId]		= pq_pairDbleInt() ;
		}


		for (int jj=0; jj<inputs.J; jj++)
		{
			//
			bool is_present	= false ;
			for (int jj2=0; jj2<numExisting_inf; jj2++) {
				if (sourceJoints_Path[jj] == existingJoints_Path[jj2]) {  is_present=true ; break ; }  }

			if (!is_present){
				MGlobal::displayError( "One (or more sourceJoints) is not in the existingSkinCluster_joints" );
				return MS::kFailure ;}

			//
			MSelectionList components_SL ;  MDoubleArray weights_DA ;
			skinCluster_Fn.getPointsAffectedByInfluence( sourceJoints_Path[jj], components_SL, weights_DA );

			int num_sel		= components_SL.length() ; // should be 1 or 0
			if (num_sel==0) { // joint is unused
				continue ;}

			// get vIds affected by this joint
			MObject comp_Obj ; MDagPath unused_Dag ;
			components_SL.getDagPath( 0, unused_Dag, comp_Obj );
			MIntArray vIds ;  MFnSingleIndexedComponent( comp_Obj ).getElements( vIds ) ;
			
			for (unsigned int vv=0; vv<vIds.length(); vv++) {
				int& vId	= vIds[vv] ;
				qs[vId].push(  pairDbleInt( weights_DA[vv], jj )  );
			}
		}


		// each Vertex is affected by at most MI influences
		for (int vv=0 ; vv<inputs.V ; vv++)
		{
			int& vId		= inputs.vertexIds[vv] ;
			inputs.existing_vertex_jIds[vId]	= intVec() ;

			int numJnt		= (int) qs[vId].size() ;
			if (numJnt == 0) {
				MGlobal::displayError( "Each Vertex needs at least one influence, there's something wrong with the existingSkinCluster" );
				return MS::kFailure ;}

			int numJnt2		= numJnt < inputs.MI ? numJnt : inputs.MI ;
			inputs.existing_vertex_jIds[vId].resize( numJnt2 );

			for (int nn = 0; nn < numJnt2 ; nn++) {
				inputs.existing_vertex_jIds[vId][nn]	= qs[vId].top().second ;
				qs[vId].pop(); }
		}
	}
	else 
	{
		inputs.useExistingSkinCluster	= false ;
		//existing_vertex_jIds is unused
	}




	// multithreading
	//
	MPlug maxCPU_Plug		= storage_Dep.findPlug( "maxCPU", true, &status );

	if (status!= MS::kSuccess){
		MGlobal::displayError( "Need attribute on storageNode : int 'maxCPU'" );
		return status ;}

	

	int inputCPU	= maxCPU_Plug.asInt() ;

	availableCPU	= omp_get_max_threads() ;
	numCPU			= availableCPU ; // default anyway

	if ((inputCPU > 0) && (inputCPU < availableCPU)) {
		changed_numCPU	= true ;
		numCPU		= inputCPU ; }
	else {
		changed_numCPU	= false ; }

	std::cout << "SkinningDecomposition : available CPU = "<< availableCPU << ", used = " << numCPU << std::endl;


	



	//-------------------------------------------------------------------
	// check if all "outputs" needed Attributes  are built
	//
	


	// weightIds
	MPlug weightIds_Plug	= storage_Dep.findPlug( "weightIds", true, &status );

	if (status!= MS::kSuccess){
		MGlobal::displayError( "Need attribute on storageNode : intArray array 'weightIds'" );
		return status ;}

	if (!weightIds_Plug.isArray()){
		MGlobal::displayError( "weightIds attribute must be .setArray( true )" );
		return status ;}



	// weights
	MPlug weights_Plug		= storage_Dep.findPlug( "weights", true, &status );

	if (status!= MS::kSuccess){
		MGlobal::displayError( "Need attribute on storageNode : doubleArray array 'weightIds'" );
		return status ;}

	if (!weights_Plug.isArray()){
		MGlobal::displayError( "weights attribute must be .setArray( true )" );
		return status ;}


	// error
	MPlug error_Plug	= storage_Dep.findPlug( "error", true, &status );

	if (status!= MS::kSuccess){
		MGlobal::displayError( "Need attribute on storageNode : double 'error'" );
		return status ;}

	// iterationDone
	MPlug iterationDone_Plug	= storage_Dep.findPlug( "iterationDone", true, &status );

	if (status!= MS::kSuccess){
		MGlobal::displayError( "Need attribute on storageNode : int 'iterationDone'" );
		return status ;}



	//
	std::cout << "SkinningDecomposition : Arguments Parsed" << std::endl;

	return status ;
}





MStatus SkinningDecomposition::doIt( const MArgList& args )
{
	// store datas into class
	MStatus status	= get_args( args );

	if (status!=MStatus::kSuccess) {
		return status; }


	// REDO
	return redoIt();
}





MStatus SkinningDecomposition::redoIt()
//	No arguments are passed in as all of the necessary information is cached by the doIt method.
//	Return Value: MS::kSuccess  or  MS::kFailure
{

	DWORD dwTickCount		= GetTickCount();

	outputs.iterationDone	= 0 ;

	


	#ifdef RELEASE_OPENMP
		MThreadUtils::syncNumOpenMPThreads();
	#endif


	for (int it=0; it<inputs.maxIteration; it++)
	{
		outputs.iterationDone++ ;


		if (it != 0)
		{
			// PART 2
			// Update Rest matrices   using previous skinning
			if (inputs.updateRestMatrices)
			{
				update_bindingMMs() ;
			}


			// PART 3
			// Update Shapes matrices   using previous skinning
			std::cout<<"SkinningDecomposition : Iteration "<<it+1 <<" Solving Bones"<<std::endl;		

			update_framesMMs( it ) ;
		}


		// PART 1
		// compute skinningMap using  Rest matrices, Shapes matrices.
		std::cout<<"SkinningDecomposition : Iteration "<<it+1<<" Solving Skinning"<<std::endl;

		update_weights( it ) ;
		get_error( it );

		std::cout<<"SkinningDecomposition : Iteration "<<it+1<<" Error = "<<outputs.errors.back()<<std::endl;
		
		
		
		if ( inputs.maxIteration > 1 )
		{
			// BREAK if last errorRatio < 1%  (errorPercentBreak negative means unused)
			if (inputs.errorPercentBreak > .0)
			{
				if ( outputs.errorPercents.back() < inputs.errorPercentBreak ) {
					std::cout<<"SkinningDecomposition : Result not improved by "<<inputs.errorPercentBreak<<" %, break"<<std::endl;
					break ;}
			}

			// update per-joint datas, needed by PART 2 and PART 3
			if ( (it==0)  ||  (it < inputs.iterationFullSolver)  ) {
				prepare_PART2_PART3( it ); }
		}

	}
	


	
	// set final data to the storage node
	std::cout<<"SkinningDecomposition : Setting Outputs"<<std::endl;

	MObject storage_Obj ;  get_Obj( storage_name, storage_Obj, MFn::kBase );
	MFnDependencyNode storage_Dep( storage_Obj  );

	output_weights( storage_Dep ) ;

	if ( inputs.setMatrices ) {
		output_matrices() ;}

	output_error( storage_Dep ) ;




	// I dont want to store anything in the undo queue, it is too big
	inputs		= Inputs() ;
	outputs		= Outputs() ;



	//
	if (changed_numCPU) {
		omp_set_dynamic( 1 );
		omp_set_num_threads( availableCPU ); }



	//
	MAnimControl::setCurrentTime( startTime ) ;

	std::cout << "SkinningDecomposition : TimeElapsed " << ((double)(GetTickCount() - dwTickCount) / 1000.0) << " sec"<< std::endl;

	return MS::kSuccess ;
}






MStatus SkinningDecomposition::undoIt()
{

	// I dont care about undo because the storageNode will be deleted in the python undo ...

    MGlobal::displayInfo( "SkinningDecomposition : Undone\n" );

	return MS::kSuccess;
}







