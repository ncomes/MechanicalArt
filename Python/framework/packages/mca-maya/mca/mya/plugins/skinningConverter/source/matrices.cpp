

#include "skinningDecomposition.h"





void SkinningDecomposition::prepare_PART2_PART3( int& it )
{
	// rebuild per-joint  vertexIds
	

	intSetVec joint_vIds_sets( inputs.J ); // vector of sets


	for (int vv=0 ; vv<inputs.V ; vv++)
	{
		int& vId		= inputs.vertexIds[vv] ;

		intVec& jIds	= outputs.vertex_jIds[ vId ] ;
		doubleVec& wgts	= outputs.vertex_wgts[ vId ] ;
		int MI			= (int) jIds.size() ;


		for (int mi=0; mi<MI; mi++ )
		{
			// ignore small weights
			if (wgts[mi] < epsilon_d) {
				continue ;}

			int& jId	= jIds[mi] ;
			joint_vIds_sets[jId].insert( vId );
		}
	}


	// set to vec
	outputs.joint_vIds.resize( inputs.J ) ;
	outputs.joint_poss.resize( inputs.J ) ;


	for (int jj=0; jj<inputs.J; jj++ )
	{
		intVec joint_vIds ;
		intSet_to_intVec( joint_vIds_sets[jj] , joint_vIds  );

		outputs.joint_vIds[jj]	= joint_vIds;


		// store positions of jIds in vertex_jIds
		// because I want to use them later to get wgts.
		int numSkin		= (int) joint_vIds.size() ;

		outputs.joint_poss[jj]	= intVec( numSkin ) ;


		for (int ss=0 ; ss<numSkin; ss++)
		{
			int& vId	= joint_vIds[ss] ;

			// jId = jj
			outputs.joint_poss[jj][ss]	= intVector_position( jj, outputs.vertex_jIds[vId] );
		}
	}
	
}




void SkinningDecomposition::get_centroid_weighted(	int& jId,
													MPointArray& pnts,
													Vector3d& centroid )
{
	double sum_wgts		= .0 ;

	centroid.setZero() ;

	intVec& joint_vIds	= outputs.joint_vIds[jId] ;
	int numSkin			= (int) joint_vIds.size() ;


	for (int ss=0; ss<numSkin; ss++)
	{
		int& vId		= joint_vIds[ss];
		MPoint& pnt		= pnts[ vId ] ;
		
		int& jId_pos	= outputs.joint_poss[jId][ss] ;
		double& wgt		= outputs.vertex_wgts[vId][jId_pos] ;

		Vector3d pnt_V3 ;
		pnt_V3 << pnt.x, pnt.y, pnt.z ;

		centroid	+= ( pnt_V3 * wgt ) ;
		sum_wgts	+= wgt ;
	}

	centroid	/= sum_wgts ;
}



void SkinningDecomposition::update_bindingMMs()
{

	// simply set positions to the middle of their weighted-vertices
	// keep original rotations.
	
	
	if (changed_numCPU) {
		omp_set_dynamic( 0 );
		omp_set_num_threads( numCPU ); }

	#ifdef RELEASE_OPENMP
		Eigen::initParallel();
		# pragma omp parallel for
	#endif
	
	
	for (int jj=0; jj<inputs.J; jj++)
	{

		// if this joint is unused, keep previous matrix
		int numSkin		= (int) outputs.joint_vIds[jj].size() ;

		if (numSkin == 0) {
			continue ;}


		// get weighted mid position   ( jId = jj)
		Vector3d centroid ;
		get_centroid_weighted( jj, inputs.rest_Pnts,  centroid  ) ;


		// override matrix translation
		// normalize at the same time
		MMatrix mm(  outputs.bindingMMs[jj].inverse()  );
		mm[3][0]	= centroid[0] ;
		mm[3][1]	= centroid[1] ;
		mm[3][2]	= centroid[2] ;
		outputs.bindingMMs[jj]	= mm.inverse() ;
	}


	std::cout << "SkinningDecomposition : bindingMatrices updated" << std::endl;
}





void SkinningDecomposition::update_framesMMs( int& it )
{
	// Compute the new bones transformations using the last solved weights.

	int ffDone = 0;

	if (changed_numCPU) {
		omp_set_dynamic( 0 );
		omp_set_num_threads( numCPU ); }

	#ifdef RELEASE_OPENMP
		Eigen::initParallel();
		# pragma omp parallel for
	#endif
	
	
	for (int ff=0; ff<inputs.F; ff++)
	{

		for (int jj=0; jj<inputs.J; jj++)
		{
			// I am simply following the Paper in this part
			// I tried my own ways again and again and I'm sick of that ! F#%K


			intVec& joint_vIds	= outputs.joint_vIds[jj] ;
			intVec& jPoss		= outputs.joint_poss[jj] ;

			int num_vId			= (int) joint_vIds.size() ; // = num affected

			doubleVec joint_wgts( num_vId );
			double sum_wgts		= .0 ;


			for (int ss=0; ss<num_vId; ss++) {
				int& vId			= joint_vIds[ss];
				int& jPos			= outputs.joint_poss[jj][ss] ;
				joint_wgts[ss]		= outputs.vertex_wgts[vId][jPos] ;
				sum_wgts			+= joint_wgts[ss] ;
			}


			if (sum_wgts < epsilon_d )
			{
				// Re-initialize the bone transformation ?
				// for the moment simply dont change it.
				continue ;
			}


			// 6 : get q
			RowVector3d_vec q( num_vId ) ;

			for (int ss=0; ss<num_vId; ss++)
			{

				int& vId		= joint_vIds[ss] ;
				intVec& jIds	= outputs.vertex_jIds[vId] ;
				doubleVec& wgts	= outputs.vertex_wgts[vId] ;
				int MI			= (int) jIds.size() ;

				MPoint& vi		= inputs.frames_Pnts[ff][vId] ;
				RowVector3d vi_R3 ;		vi_R3 << vi.x, vi.y, vi.z ;
				RowVector3d sum_R3 ;	sum_R3.setZero();


				for (int mi=0; mi<MI; mi++)
				{
					int& jjj	= jIds[mi] ;
					if (jj==jjj) {
						continue ; }

					MPoint prev		= inputs.rest_Pnts[vId] * (outputs.bindingMMs[jjj] * outputs.framesMMs[ff][jjj]) ;
					RowVector3d prev_R3 ;	prev_R3 << prev.x, prev.y, prev.z ;

					sum_R3		+= (wgts[mi] * prev_R3) ;
				}

				q[ss]	= vi_R3 - sum_R3 ;
			}


			// 8b : get p* q*
			double sum_w2	= .0 ; 
			RowVector3d w2_by_pis ;	w2_by_pis.setZero();
			RowVector3d w2_by_qis ;	w2_by_qis.setZero();


			for (int ss=0; ss<num_vId; ss++)
			{
				int& vId		= joint_vIds[ss] ;

				MPoint& pi		= inputs.rest_Pnts[vId] ;
				RowVector3d pi_R3 ;		pi_R3 << pi.x, pi.y, pi.z ;

				double& w		= joint_wgts[ss] ;
				double w2		= w*w ;
				sum_w2			+= w2 ;
				w2_by_pis		+= (w2 * pi_R3) ;

				w2_by_qis		+= (w * q[ss]) ;
			}

			RowVector3d p_star	= w2_by_pis / sum_w2 ;
			RowVector3d q_star	= w2_by_qis / sum_w2 ;


			// 8a : get p_bar q_bar  to  P and Q
			Matrix3Xd P ;	P.resize( Eigen::NoChange, num_vId );
			Matrix3Xd Q ;	Q.resize( Eigen::NoChange, num_vId );


			for (int ss=0; ss<num_vId; ss++)
			{
				int& vId		= joint_vIds[ss] ;
				double& w		= joint_wgts[ss] ;

				MPoint& pi		= inputs.rest_Pnts[vId] ;
				RowVector3d pi_R3 ;		pi_R3 << pi.x, pi.y, pi.z ;

				RowVector3d p_bar	= pi_R3 - p_star ;
				P.col(ss)			= w * (p_bar.transpose()) ;

				//
				RowVector3d q_bar	= q[ss] - (w * q_star) ;
				Q.col(ss)			= q_bar.transpose() ;
			}


			// 9 : SVD P*Qt
			//
			MMatrix transfo_MM;

			if (inputs.rigidMatrices==true) {
				get_rigidMatrix( P, Q, p_star, q_star, transfo_MM); }
			else { 
				get_flexibleMatrix( P, Q, p_star, q_star, transfo_MM); }

			outputs.framesMMs[ff][jj]	=  outputs.bindingMMs[jj].inverse() * transfo_MM ;
		}


		//printf( "SkinningDecomposition : Iteration %d/%d BonesSolved at Frame %g \n", (it+1), inputs.iteration, inputs.frames[ff] )  ;
		//fflush(  stdout  ); // avoid print overlap
	}

}



void SkinningDecomposition::get_rigidMatrix( Matrix3Xd& P, Matrix3Xd& Q,
											RowVector3d& p_star,RowVector3d& q_star,
											MMatrix& transfo_MM)
{
	// perform an svd
	// H covarianceMatrix
	MatrixXd H		= P * Q.transpose() ;
	SvdXd svd		= H.jacobiSvd( Eigen::ComputeThinU | Eigen::ComputeThinV ) ;
	Matrix3d Ut		= svd.matrixU().transpose();
	Matrix3d V		= svd.matrixV() ;
	Matrix3d R		= V * Ut;
	
	if (R.determinant() < .0 ) {		
		// R can be left hand, so negate z axis
		R.col(2)	*= -1.0 ;  }
	
	
	// compute translation    t = -R*centroidA.t + centroidB.t
	R.transposeInPlace() ;
	RowVector3d t	=  ( -p_star * R ) + q_star ;
	
	double mm[4][4]	= {	{R(0,0), R(0,1) ,R(0,2), .0},
						{R(1,0), R(1,1), R(1,2), .0},
						{R(2,0), R(2,1), R(2,2), .0},
						{t[0], t[1], t[2], 1.0} };
	
	transfo_MM		= MMatrix( mm );
}



void SkinningDecomposition::get_flexibleMatrix(  Matrix3Xd& P, Matrix3Xd& Q,
											RowVector3d& p_star,RowVector3d& q_star,
											MMatrix& transfo_MM)
{ 
	
	// perform a simple linear least square
	MatrixX3d Pt	= P.transpose() ;
	MatrixX3d Qt	= Q.transpose() ;
	Matrix3d R		= Pt.householderQr().solve( Qt ) ;
	
	// the matrix does not need to be fixed in that case


	RowVector3d t	=  ( -p_star * R ) + q_star ;
	double mm[4][4]	= {	{R(0,0), R(0,1) ,R(0,2), .0},
						{R(1,0), R(1,1), R(1,2), .0},
						{R(2,0), R(2,1), R(2,2), .0},
						{t[0], t[1], t[2], 1.0} };
	
	transfo_MM		= MMatrix( mm );

}































