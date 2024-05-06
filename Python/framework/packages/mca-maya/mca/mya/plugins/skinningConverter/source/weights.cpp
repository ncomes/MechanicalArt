

#include "skinningDecomposition.h"





void SkinningDecomposition::update_weights( int& it )
{

	
	// for nnls
	int _maxIter1	= 10 * inputs.J ;  // 4to10 times A.numCol
	int _maxIter2	= 10 * inputs.MI ; // 4to10 times A2.numCol
	double _eps		= 1e-10 ;



	// Parallel computation

	// initialize the map data, because it does not like to be filled in multithreading
	if (it == 0)
	{
		for (int vv=0 ; vv<inputs.V ; vv++) {
			int& vId	= inputs.vertexIds[vv] ;
			outputs.vertex_jIds[ vId ]	= intVec() ;
			outputs.vertex_wgts[ vId ]	= doubleVec() ; }
	}

	if (changed_numCPU) {
		omp_set_dynamic( 0 );
		omp_set_num_threads( numCPU ); }

	#ifdef RELEASE_OPENMP
		Eigen::initParallel();
		# pragma omp parallel for
	#endif
	

	for (int vv=0 ; vv<inputs.V ; vv++)
	{
		int& vId	= inputs.vertexIds[vv] ;

		// For ONE vertex :
		// Ax = b
		// A  is (RestPoint * allJoints at allFrames)
		// x  is the weights I want.
		// b  is pointPosition at allFrames
		

		// recompute the points anyway,
		// because  during the iteration   the matrices have been updated
		MatrixXd	A ;
		build_A( vId,  A ) ;		// dim 3AF * J
			
		VectorXd	b ;				// dim 3AF * 1
		build_b( vId, b ) ;
		


		if ((it==0) && (inputs.useExistingSkinCluster==true))
		{
			// I already know a list of jointId per vertex
			outputs.vertex_jIds[ vId ]	= inputs.existing_vertex_jIds[ vId ] ;
		}

		else if ((it==0) || (it < inputs.iterationFullSolver))
		{	
			// NNLS  1st  using all joints
			// this one is slow,  and computed only to get the maxInfluencerIds
			// sum( x[ii] ) = 1.0
			VectorXd x	;									// dim J * 1
			NNLS::solve( A, b, x, _maxIter1, _eps );
			
			//outputs.vertex_jIds[ vId ]	= intVec() ;		// dim MI
			get_maxInfluencerIds( x,  outputs.vertex_jIds[ vId ]  );
		}


		// NNLS  2nd  using max influenced joints only,
		// so lot faster than the 1st NNLS
		// sum( x2[ii] ) = 1.0
		MatrixXd	A2 ;									// dim 3AF * MI
		build_A2( outputs.vertex_jIds[ vId ], A,  A2 ) ;
		
		VectorXd	x2	;									// dim MI * 1
		NNLS::solve( A2, b, x2,  _maxIter2, _eps );
		
		//outputs.vertex_wgts[ vId ]	= doubleVec() ;
		VectorXd_to_doubleVec( x2, epsilon_d, outputs.vertex_wgts[ vId ] ); // dim MI
		
		// weights are clamped and normalized.


		// cout is overlapped by others threaded cout,  use printf + fflush instead
		//std::cout<<"SkinningDecomposition : Iteration "<<it+1<<"/"<<inputs.iteration <<" Solved "<<++vDone<<"/"<<inputs.V<<" (VertexId "<<vId<<")"<<std::endl;
		//printf( "SkinningDecomposition : Iteration %d/%d SkinningSolved %d/%d (VertexId %d) \n", (it+1), inputs.iteration, ++vDone, inputs.V, vId)  ;
		//fflush(  stdout  ); // avoid print overlap
	}


	/*
	///// DEBUG
	if ((outputs.vertex_jIds.size() != inputs.V) || (outputs.vertex_wgts.size() != inputs.V))
	{
		int bad = 0 ;
	}
	///////////////////////////////
	*/
}





void SkinningDecomposition::build_A( int& vId,  MatrixXd& A )
// For ONE vertex,  build the Big Matrix A = "Rest point * allJoints at allPoses"
{

	A.resize(  3*inputs.AF + 1, inputs.J  ); // dim 3AF * J
	

	// for each Frame
	//   for each Joint
	for (int ff=0; ff<inputs.F; ff++)
	{
		for (int jj=0; jj<inputs.J; jj++)
		{
			MPoint transfo_Pnt	= inputs.rest_Pnts[vId] * (outputs.bindingMMs[jj] * outputs.framesMMs[ff][jj]) ;

			A(3*ff+0, jj)	= transfo_Pnt.x ;
			A(3*ff+1, jj)	= transfo_Pnt.y ;
			A(3*ff+2, jj)	= transfo_Pnt.z ;
		}
	}


	// rest pose as last
	for (int jj=0; jj<inputs.J; jj++)
	{
		A(3*inputs.F+0, jj)	= inputs.rest_Pnts[vId].x ;
		A(3*inputs.F+1, jj)	= inputs.rest_Pnts[vId].y ;
		A(3*inputs.F+2, jj)	= inputs.rest_Pnts[vId].z ;
	}


	// last line is lagragian
	A.row( 3*inputs.AF  ).setConstant( inputs.lagragian );

}



void SkinningDecomposition::build_b( int& vId, VectorXd& b )
// For ONE vertex,  build the vertical vector "this vertex at all poses"
{
	b.resize( 3*inputs.AF +1 );
	

	for (int ff=0; ff<inputs.F; ff++)
	{
		b(3*ff+0)	= inputs.frames_Pnts[ff][vId].x ;
		b(3*ff+1)	= inputs.frames_Pnts[ff][vId].y ;
		b(3*ff+2)	= inputs.frames_Pnts[ff][vId].z ;
	}

	b(3*inputs.F+0)	= inputs.rest_Pnts[vId].x ;
	b(3*inputs.F+1)	= inputs.rest_Pnts[vId].y ;
	b(3*inputs.F+2)	= inputs.rest_Pnts[vId].z ;

	b(3*inputs.AF)	= inputs.lagragian ;
}



void SkinningDecomposition::get_maxInfluencerIds( VectorXd& x,  intVec& jnt_ids )
{
	
	// convert to priority_queue
	// order 'double' then 'int' DOES matter because containers are ordered using keys
	pq_pairDbleInt q;

	for (int jj = 0; jj < inputs.J; jj++)
	{
		q.push( pairDbleInt(x(jj), jj )  );
	}


	// get ::top  and  ::pop it
	jnt_ids.resize( inputs.MI );

	for (int ii = 0; ii < inputs.MI ; ++ii) {
		jnt_ids[ii]		= q.top().second ;
		q.pop();
	}

}



void SkinningDecomposition::build_A2(  intVec& vertex_jIds, MatrixXd& A, MatrixXd& A2  )
{
	int MI	= (int) vertex_jIds.size() ;

	A2.resize( 3*inputs.AF +1, MI ); // dim 3AF * MI

	// Dont need to set lagragian values, because I copy full A columns 
	// ( therefore including lagragian at bottom )
	
	for (int jj=0; jj<MI; jj++)
	{
		int& jId	= vertex_jIds[jj];
		
		A2.col(jj)	= A.col( jId  );
	}
}




void SkinningDecomposition::get_error( int& it )
{
	// compare final points and inputPoints
	// error = 1000* sqrt((sum the delta length at each frame) /3*V*F)  in the paper

	double error	= .0 ;


	if (changed_numCPU) {
		omp_set_dynamic( 0 );
		omp_set_num_threads( numCPU ); }

	#ifdef RELEASE_OPENMP
		Eigen::initParallel();
		# pragma omp parallel for
	#endif
	

	for (int ff=0; ff<inputs.F; ff++)
	{
		for (int vv=0; vv<inputs.V; vv++)
		{
			int& vId			= inputs.vertexIds[vv];

			intVec& vertex_jIds		= outputs.vertex_jIds[vId] ;
			doubleVec& vertex_wgts	= outputs.vertex_wgts[vId] ;

			MPoint skinned_Pnt( .0,.0,.0 ) ;
			int MI		= (int) vertex_jIds.size() ;
			
			for (int mi=0; mi<MI; mi++)
			{
				int& jId		= vertex_jIds[mi] ;
				double& wgt		= vertex_wgts[mi] ;

				MPoint pnt		= inputs.rest_Pnts[vId] * (outputs.bindingMMs[jId] * outputs.framesMMs[ff][jId]) ;
				skinned_Pnt.x	+= wgt * pnt.x ;
				skinned_Pnt.y	+= wgt * pnt.y ;
				skinned_Pnt.z	+= wgt * pnt.z ;
			}

			double d	= (skinned_Pnt - inputs.frames_Pnts[ff][vId]).length() ;
			error		+= d*d ;
			//error		+= d  ;
		}
	}

	error	= 1000.0 * sqrt( error/(3.0*inputs.V*inputs.F) ) ; // = paper
	error	/= inputs.boundingBox_diagonal_sum ;	// = me ;) this allows to get a ratio



	//
	double errorPercent ;
	if (outputs.errorPercents.size()==0) {
		errorPercent	= 1.0 ;}
	else {
		// 100 * abs( 1 - error/prevError ) ~= 1% ...
		errorPercent	= 100.0 * abs(1.0-error/outputs.errors.back()) ;}


	//
	outputs.errors.push_back( error );
	outputs.errorPercents.push_back( errorPercent );
}







