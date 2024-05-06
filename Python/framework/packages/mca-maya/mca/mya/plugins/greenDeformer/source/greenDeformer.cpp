

#include "greenDeformer.h"
#include "component.h"
#include "conversion.h"
#include "mathUtil.h"



// default
GreenDeformer::GreenDeformer(){}
GreenDeformer::~GreenDeformer(){};

MTypeId		GreenDeformer::id(0xCED2528);
MString		GreenDeformer::name("greenDeformer");



// attrs
MObject		GreenDeformer::cageOrig;
MObject		GreenDeformer::cageDeformed;
MObject		GreenDeformer::cageChanged;
MObject		GreenDeformer::preserveScale;
MObject		GreenDeformer::refresh;



void* GreenDeformer::nodeCreator()
{
	return new GreenDeformer();
}



MStatus GreenDeformer::nodeInitializer()
{
	MFnTypedAttribute	typedAttr;
	MFnNumericAttribute	numAttr;

	
	// assume cage is triangulated
	cageOrig		= typedAttr.create("cageOrig", "co", MFnData::kMesh); // connect .mesh   never .worldMesh
	cageDeformed	= typedAttr.create("cageDeformed", "cd", MFnData::kMesh);

	
	// fake, need this to update cage data
	//cageChanged		= numAttr.create("cageChanged", "cc", MFnNumericData::kBoolean);
	//numAttr.setHidden(true);


	//
	preserveScale	= numAttr.create("preserveScale", "sw", MFnNumericData::kDouble, .0 );
	numAttr.setKeyable( true );
	numAttr.setMin(.0);
	numAttr.setMax(1.0);

	//
	refresh		= numAttr.create("refresh", "rf", MFnNumericData::kBoolean, false);



	
	// add + affect
	addAttribute(cageOrig);
	addAttribute(cageDeformed);
	//addAttribute(cageChanged);
	addAttribute(preserveScale);
	addAttribute(refresh);

	attributeAffects(cageOrig, outputGeom);
	attributeAffects(cageDeformed, outputGeom);
	//attributeAffects(cageChanged, outputGeom);
	attributeAffects(preserveScale, outputGeom);
	attributeAffects(refresh, outputGeom);
	
	//attributeAffects(cageOrig, cageChanged);
	


	// AE
	MStatus AE_status = init_AETemplate();


	// paint
	MString paint_cmd = "makePaintable -attrType \"multiFloat\" -sm \"deformer\" \"" + name + "\" \"weights\" ;";
	MStatus status = MGlobal::executeCommand(paint_cmd);

	return MS::kSuccess;
}



MStatus GreenDeformer::init_AETemplate()
{
	MString AE_cmd = "";

	AE_cmd += "global proc AE_" + name + "_topAdditive( string $attrName )";
	AE_cmd += "{";
	AE_cmd += "	string $cl = `rowLayout -numberOfColumns 1 -adjustableColumn 1 `;";
	AE_cmd += "		picture -image \":/node/" + name + "AE.png\" -p $cl;";
	AE_cmd += "	setParent..;";
	AE_cmd += "}  ";

	AE_cmd += "global proc AE_" + name + "_updateNothing( string $attrName )  {  } ";

	AE_cmd += "global proc AE" + name + "Template( string $kPluginNodeName )";
	AE_cmd += "{";
	AE_cmd += "editorTemplate -callCustom \"AE_" + name + "_topAdditive\" \"AE_" + name + "_updateNothing\" \"\";  ";

	AE_cmd += "editorTemplate -beginScrollLayout;  ";
	AE_cmd += "	editorTemplate -beginLayout \"Green Attributes\" -collapse 0;  ";
	AE_cmd += "		editorTemplate -addControl  \"preserveScale\" ;  ";
	AE_cmd += "	editorTemplate -endLayout;  ";

	AE_cmd += "	editorTemplate -beginLayout \"Advanced Attributes\" -collapse 1;  ";
	AE_cmd += "		editorTemplate -addControl  \"refresh\" ;  ";
	AE_cmd += "	editorTemplate -endLayout;  ";
	
	AE_cmd += "	editorTemplate -beginLayout \"Default Attributes\" -collapse 0;  ";
	AE_cmd += "		editorTemplate -addControl  \"nodeState\" ;  ";
	AE_cmd += "		editorTemplate -addControl  \"envelope\" ;  ";
	AE_cmd += "	editorTemplate -endLayout;  ";

	AE_cmd += "	editorTemplate -addExtraControls;  ";
	AE_cmd += "editorTemplate -endScrollLayout;  ";
	AE_cmd += "}  ";

	return MGlobal::executeCommand(AE_cmd);
}





void GreenDeformer::update_orig( int& ii_id, MItGeometry& output_It )
{
	
	// vIds
	int orig_len	= output_It.count() ;

	orig_vIds[ii_id].setLength( orig_len );

	int jj=0;
	for (output_It.reset(); !output_It.isDone(); output_It.next()) {
		orig_vIds[ii_id][jj++]	= output_It.index() ; }


	// positions
	orig_Pnts[ii_id].clear() ;
	output_It.allPositions(orig_Pnts[ii_id], wSpace);
}



void GreenDeformer::update_weights( MDataBlock& data, int& ii_id  )
{
	
	// anyway the following is fast so it is ok  to run it everytime
	MFnWeightGeometryFilter geoFilter( thisMObject()  );

	MFnSingleIndexedComponent sic; 
	MObject components	= sic.create(MFn::kMeshVertComponent); 
	sic.addElements( orig_vIds[ii_id] );

	wgts.clear() ;
	geoFilter.getWeights( ii_id, components,  wgts );
}



void GreenDeformer::update_faceAreas()
{
	int cage_numF	= cageOrig_Nrmls.length() ;

	cageOrig_faceAreas.setLength( cage_numF );


	#ifdef RELEASE_OPENMP
		# pragma omp parallel for
	#endif
	for (int ff=0; ff<cage_numF; ff++)
	{
		MPoint orig0	= cageOrig_Pnts[ cageOrig_vIdsPerFace[ff][0] ];
		MPoint orig1	= cageOrig_Pnts[ cageOrig_vIdsPerFace[ff][1] ];
		MPoint orig2	= cageOrig_Pnts[ cageOrig_vIdsPerFace[ff][2] ];
		
		cageOrig_faceAreas[ff]	= get_triangle_area( orig0, orig1, orig2) ;
	}
}



void GreenDeformer::get_scaleFactors()
{
	int cage_numF	= cageOrig_Nrmls.length() ;

	scaleFactors.setLength( cage_numF );

	/* NOT HERE, it slows down
	#ifdef RELEASE_OPENMP
		# pragma omp parallel for
	#endif
	*/
	for (int ff=0; ff<cage_numF; ff++)
	{
		// Scale Factor S
		MPoint orig0	= cageOrig_Pnts[ cageOrig_vIdsPerFace[ff][0] ];
		MPoint orig1	= cageOrig_Pnts[ cageOrig_vIdsPerFace[ff][1] ];
		MPoint orig2	= cageOrig_Pnts[ cageOrig_vIdsPerFace[ff][2] ];
		MPoint deformed0	= cageDeformed_Pnts[ cageOrig_vIdsPerFace[ff][0] ];
		MPoint deformed1	= cageDeformed_Pnts[ cageOrig_vIdsPerFace[ff][1] ];
		MPoint deformed2	= cageDeformed_Pnts[ cageOrig_vIdsPerFace[ff][2] ];

		MVector u0		= orig1 - orig0;
		MVector u1		= deformed1 - deformed0;
		MVector v0		= orig2 - orig0;
		MVector v1		= deformed2 - deformed0;

		scaleFactors[ff]	= sqrt(u1.length()*u1.length() * v0.length()*v0.length() - 2.0*(u1*v1)*(u0*v0) + v1.length()*v1.length() * u0.length()*u0.length()) / (sqrt(8.0) * cageOrig_faceAreas[ff] );
	}
}






MStatus GreenDeformer::compute(const MPlug& plug, MDataBlock& data)
{
	///////////////
	//MString debuug =  plug.info();
	////////////

	


	#ifdef RELEASE_OPENMP
		MThreadUtils::syncNumOpenMPThreads();
	#endif

		
	// dv
	if ((plug != outputGeom) || (plug.isArray()) ) {
		return MStatus::kSuccess; }


	int nodeState = data.inputValue(state).asInt();
	if (nodeState == 1) {
		return MStatus::kSuccess; }



	//
	int plug_id		= plug.logicalIndex() ;
	MIntArray all_ids ;  MPlug(plug.array()).getExistingArrayAttributeIndices( all_ids );

	if (plug_id != all_ids[0]) {
		return MStatus::kSuccess; }




	//
	MStatus mStatus;

	double envelope_d		= (double)data.inputValue(envelope).asFloat();

	double preserveScale_d	= data.inputValue( preserveScale ).asDouble() ;
	bool refresh_b			= data.inputValue( refresh ).asBool() ;



	// stop if nothing plugged to cage Meshes
	MObject cageOrig_Obj		= data.inputValue( cageOrig ).asMesh();
	MObject cageDeformed_Obj	= data.inputValue( cageDeformed ).asMesh();

	if (cageOrig_Obj.isNull() || cageDeformed_Obj.isNull()) {
		MGlobal::displayWarning("GreenDeformer : Nothing connected to .cageOrig or .cageDeformed" );
		return MS::kInvalidParameter; }

	


	// get cageOrig pnts/nrmls
	//bool cageChanged_b	= ! data.isClean(cageChanged) ;


	//if  ((refresh_b)  ||  (cageChanged_b))
	if ((cageOrig_Pnts.length()==0)
			||  (refresh_b)  )
	{

		// I NEED a cage triangular with no hole
		bool is_triangular	= true ;
		bool is_holed		= false ;
		get_points_and_normals( cageOrig_Obj, cageOrig_Pnts, cageOrig_Nrmls, wSpace, true, is_triangular, is_holed, cageOrig_vIdsPerFace );


		if (( !is_triangular ) || (is_holed)){
			return MS::kInvalidParameter; }


		// store triangles areas
		update_faceAreas() ;


		// need a meshIntersector for outside cage points
		cageOrig_Intersector.create( cageOrig_Obj );
		

		//
		//data.setClean( cageChanged );
		MGlobal::displayInfo("GreenDeformer : Cage Updated");
	}



	

	// get cageDeformed pnts/nrmls
	// check if cageOrig and cageDeformed same topo
	bool		not_used1, not_used2 ;
	MIntArrayVec not_used3 ;
	get_points_and_normals(cageDeformed_Obj, cageDeformed_Pnts, cageDeformed_Nrmls, wSpace,  false, not_used1, not_used2, not_used3 );


	if ( (cageOrig_Pnts.length() != cageDeformed_Pnts.length())
		|| (cageOrig_Nrmls.length() != cageDeformed_Nrmls.length()) )
	{
		MGlobal::displayWarning("GreenDeformer : cageOrig and cageDeformed don't share same topology");
		return MS::kInvalidParameter;
	}

	

	// deduct scaleFactor per face
	//
	get_scaleFactors() ;

	
	


	//
	MArrayDataHandle inputs_H	= data.inputArrayValue(input);
	MArrayDataHandle outputs_H	= data.outputArrayValue(outputGeom);



	for (int ii = 0; ii < (int)outputs_H.elementCount(); ii++)
	{
		
		//
		int ii_id = outputs_H.elementIndex();

		mStatus = inputs_H.jumpToElement(ii_id);
		if (mStatus != MStatus::kSuccess) {
			outputs_H.next(); continue; }


		// get inputGeometry,  stop if not a mesh ...
		MDataHandle input_H		= inputs_H.inputValue();
		MDataHandle inputGeo_H	= input_H.child(inputGeom);

		if (inputGeo_H.type() != MFnData::kMesh){
			outputs_H.next(); continue; }

		MObject input_Obj	= input_H.asMesh();


		//  ... else copy inputGeometry data  to outputGeometry[ii]
		// it is faster than mesh.copy() + output_H.setMObject( newMesh )
		MDataHandle outputGeo_H		= outputs_H.outputValue();
		outputGeo_H.copy(inputGeo_H);

		if (envelope_d < epsilon_d){
			outputs_H.next(); continue; }


		// use MItGeometry to get affected_vIds  ( once )
		unsigned int groupId_int = input_H.child(groupId).asInt();
		MItGeometry output_It(outputGeo_H, groupId_int, false); // false = readOnly

		int deformed_len = output_It.count();

		if (deformed_len == 0) {
			// No vertices in the deformerSet
			outputs_H.next(); continue; }


		

		// update weights only if :
		//	
		//	- cage changed
		//	- force refresh using attribute 'refresh'

		//if ((!is_int_in_mapFirst( ii_id, orig_vIds))
		//	||  (refresh_b) 
		//	||	(cageChanged_b) )
		if ((!is_int_in_mapFirst( ii_id, orig_vIds))
			||  (refresh_b)  )
		{
			// dv
			orig_vIds[ii_id]	= MIntArray() ;
			orig_Pnts[ii_id]	= MPointArray() ;
			phis[ii_id]			= ddVec() ;
			psis[ii_id]			= ddVec() ;

			//
			update_orig( ii_id, output_It );
			update_green( ii_id );

			//
			MString mess	= "GreenDeformer : Coordinates("; mess+=ii_id; mess+=") Updated" ;
			MGlobal::displayInfo(mess);
		}



		
		// Get scaleFactor  then  Apply ( fast )
		//
		MPointArray green_Pnts	= apply_green( ii_id, preserveScale_d  );





		// final points
		// blend between orig and green  using weight*envelope

		update_weights( data, ii_id ) ;

		MPointArray newIt_Pnts(deformed_len); // dim deformed,   because set output_It


		//#ifdef RELEASE_OPENMP
		//	# pragma omp parallel for
		//#endif
		for (int vv = 0; vv < deformed_len; vv++)
		{
			newIt_Pnts[vv] = blend_2_MPoints( orig_Pnts[ii_id][vv], green_Pnts[vv], envelope_d*wgts[vv]);
		}
		


		//
		output_It.setAllPositions(newIt_Pnts, wSpace);

		outputs_H.next();
	}

	


	// end
	mStatus		= outputs_H.setAllClean(); // ignored ???
	//data.setClean(plug);

	return MS::kSuccess;
}






void GreenDeformer::update_green( int& ii_id )
{
	int cage_numV	= cageOrig_Pnts.length() ;
	int cage_numF	= cageOrig_Nrmls.length() ;
	int numV		= orig_Pnts[ii_id].length() ;

	phis[ii_id].resize( numV, dVec( cage_numV, .0 ) );
	psis[ii_id].resize( numV, dVec( cage_numF, .0 ) );


	#ifdef RELEASE_OPENMP
		# pragma omp parallel for
	#endif
	for (int vv=0; vv<numV; vv++)
	{
		MPoint vPnt		= orig_Pnts[ii_id][vv] ;


		for (int ff=0; ff<cage_numF; ff++)
		{
			MVectorArray vf( 3 );

			for (int kk=0; kk<3; kk++)
			{
				int tri_vId		= cageOrig_vIdsPerFace[ff][kk];
				MPoint tri_vPnt	= cageOrig_Pnts[tri_vId] ;

				vf[kk]	= tri_vPnt - vPnt ;
			}


			MVector p	= cageOrig_Nrmls[ff] * ( vf[0]*cageOrig_Nrmls[ff] );

			double s3[3], I3[3], II3[3] ;
			MVectorArray N3( 3 );

			for (int kk=0; kk<3; kk++)
			{
				int next	= (kk+1)%3 ;

				double sl_val	=  ( (vf[kk] - p)^(vf[next] - p) ) * cageOrig_Nrmls[ff] ;
				s3[kk]		= sl_val < 0.0 ? -1.0 : 1.0;  // Sign

				MVector zero_MV(.0,.0,.0);
				I3[kk]		= GCTriInt( p, vf[kk], vf[next], zero_MV  );
				II3[kk]		= GCTriInt( zero_MV, vf[next], vf[kk], zero_MV );

				N3[kk]		= (vf[next] ^ vf[kk]).normal() ;
			}


			// psi
			psis[ii_id][vv][ff]	= abs( s3[0]*I3[0] + s3[1]*I3[1] + s3[2]*I3[2]  ) ;

			MVector w	= (cageOrig_Nrmls[ff]*(-psis[ii_id][vv][ff])) + (N3[0]*II3[0] + N3[1]*II3[1] + N3[2]*II3[2]) ;

			// phi
			if (w.length() > epsilon_d)
			{
				for (int kk=0; kk<3; kk++)
				{
					int tri_vId		= cageOrig_vIdsPerFace[ff][kk];
					int next		= (kk+1)%3 ;

					phis[ii_id][vv][tri_vId] +=  (N3[next]*w)/(N3[next]*vf[kk])  ;
				}
			}
		}


		
		// outside cage if phi_sum<1/2 ?
		double phi_sum	= .0 ;
		
		for (int cvv=0; cvv<cage_numV; cvv++) {
			phi_sum	+= phis[ii_id][vv][cvv] ; }


		EigenV4d vPnt2 ;	vPnt2 << vPnt.x, vPnt.y, vPnt.z, 1.0;

		if (phi_sum < .5)
		{
			// find closest face/triangle
			// use MFnMesh::getClosestPoint with arg closestPolygon
			// get triangle_vertex_ids   and their positions  ( I know them already )
			int closest_fId			= get_closest_faceId( vPnt, cageOrig_Intersector  );

			MIntArray closest_vIds	= cageOrig_vIdsPerFace[ closest_fId ] ;


			// A  =  eigenMatrix4*4  with  each column = triangle-Vertex_position   with 4th element=1.0
			// last .col(3) = cageNormalOrig and 4th = 0.0
			EigenM4d A;
			for (int kk=0; kk<3; kk++)
			{
				MPoint closest_Pnt		= cageOrig_Pnts[ closest_vIds[kk] ] ;
				EigenV4d p4 ;	p4 << closest_Pnt.x, closest_Pnt.y, closest_Pnt.z, 1.0;
				A.col(kk)	= p4;
			}

			MVector closest_Nrm		= cageOrig_Nrmls[ closest_fId ] ;
			EigenV4d n4; n4 << closest_Nrm.x, closest_Nrm.y, closest_Nrm.z, 0.0;
			A.col(3)	= n4;


			// solve alpha(0,1,2) and betas(3)
			// add alphas  to  phi
			// add beta  to  psi
			EigenV4d x	= A.fullPivLu().solve( vPnt2 );

			for (int kk=0; kk<3; kk++)
			{
				int tri_vId		= closest_vIds[kk];

				phis[ii_id][vv][tri_vId]	+= x[kk];
			}

			psis[ii_id][vv][closest_fId]	+= x[3];
		}
		


		// normalize phi only
		phi_sum	= .0 ;
		
		for (int cvv=0; cvv<cage_numV; cvv++) {
			phi_sum	+= phis[ii_id][vv][cvv] ; }

		for (int cvv=0; cvv<cage_numV; cvv++) {
			phis[ii_id][vv][cvv]	/= phi_sum ; }
		
	}
}



double clamp( double minVal, double val, double maxVal  )
{
	if (val <minVal){
		return minVal;}
	else if (val > maxVal){
		return maxVal;}
	return val ;
}



double GreenDeformer::GCTriInt( MVector& p, MVector& v1, MVector& v2, MVector& n  )
{

	double alpha	= acos( clamp( -1.0, ((v2 - v1).normal())*((p - v1).normal()), 1.0)  );
	if (alpha <= .0) {
		return .0 ;}

	double beta		= acos( clamp( -1.0, ((v1 - p).normal())*((v2 - p).normal()), 1.0)  );

	double lambda	= (p-v1).length()*(p-v1).length()   *  sin(alpha)*sin(alpha) ;
	double c		= (p-n).length()*(p-n).length();

	double thetas[2]	= {M_PI-alpha, M_PI-alpha-beta} ;
	double Ithetas[2]	= {.0,.0};

	for (int ii=0; ii<2; ii++)
	{
		double S	= sin( thetas[ii] );
		/*
		if ((-epsilon_d < S)  &&  ( S < epsilon_d)) {
			return .0 ;}
		*/
		double C	= cos( thetas[ii] );

		double Ssign	= S / abs(S) ;

		Ithetas[ii]	= (-Ssign/2.0) * (2.0*sqrt(c)*atan( sqrt(c)*C / (sqrt(lambda+S*S*c)))  +  sqrt(lambda)*log( 2.0*sqrt(lambda)*S*S/((1.0-C)*(1.0-C))  * (1.0- 2.0*c*C/(c*(1.0+C)+lambda+sqrt(lambda*lambda+lambda*c*S*S)) )  ) );
	}

	return (-1.0/(4.0*M_PI) * abs(Ithetas[0]-Ithetas[1]-sqrt(c)*beta)) ;
}




MPointArray GreenDeformer::apply_green(  int& ii_id, double& preserveScale_d )
{
	int numV		= orig_vIds[ii_id].length();
	int cage_numV	= cageDeformed_Pnts.length() ;
	int cage_numF	= cageDeformed_Nrmls.length() ;

	MPointArray new_Pnts( numV  );

	
	#ifdef RELEASE_OPENMP
		# pragma omp parallel for
	#endif
	for (int ii=0; ii<numV; ii++ )
	{

		// add weighted(phi) cage points
		for (int vv=0; vv<cage_numV; vv++)
		{
			new_Pnts[ii]	+=  MVector(cageDeformed_Pnts[vv]) * phis[ii_id][ii][vv] ;
		}


		// add weighted(psi) cage normals
		for (int ff=0; ff<cage_numF; ff++)
		{
			double noScaleFactor	= 1.0 ;
			double finalScaleFactor	= blend2( noScaleFactor, scaleFactors[ff],  preserveScale_d ) ;

			new_Pnts[ii]	+=  cageDeformed_Nrmls[ff] * psis[ii_id][ii][ff] * finalScaleFactor ;
		}
	}
	
	/*
	/////////// Alternativ
	#ifdef RELEASE_OPENMP
		# pragma omp parallel for
	#endif
	for (int iivv=0; iivv<numV*cage_numV; iivv++ )
	{
		int ii	= iivv / cage_numV  ;
		int vv	= iivv % cage_numV ;

		new_Pnts[ii]	+=  MVector(cageDeformed_Pnts[vv]) * phis[ii_id][ii][vv] ;
	}

	#ifdef RELEASE_OPENMP
		# pragma omp parallel for
	#endif
	for (int iiff=0; iiff<numV*cage_numF; iiff++ )
	{
		int ii	= iiff / cage_numF  ;
		int ff	= iiff % cage_numF ;

		double noScaleFactor	= 1.0 ;
		double finalScaleFactor	= blend2( noScaleFactor, scaleFactors[ff],  preserveScale_d ) ;

		new_Pnts[ii]	+=  cageDeformed_Nrmls[ff] * psis[ii_id][ii][ff] * finalScaleFactor ;
	}
	*/


	return new_Pnts ;
}













