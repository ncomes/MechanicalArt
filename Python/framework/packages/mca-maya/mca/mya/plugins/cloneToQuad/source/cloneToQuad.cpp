#include "stdafx.h"
#include "conversion.h"
#include "cloneToQuad.h"
#include "component.h"
#include "bezierPatch.h"
#include "shading.h"

//#pragma optimize( "", off )


CloneToQuad::CloneToQuad(){}
CloneToQuad::~CloneToQuad(){};

MTypeId		CloneToQuad::id(0x0077CBBC);
MString		CloneToQuad::name("cloneToQuad");

MObject		CloneToQuad::clonedMesh;
MObject		CloneToQuad::clonedChanged;
MObject		CloneToQuad::quadMesh;
MObject		CloneToQuad::outMesh;
MObject		CloneToQuad::cloneUVs;
MObject		CloneToQuad::scaleHeight;
MObject		CloneToQuad::offsetHeight;
MObject		CloneToQuad::areaScale;
MObject		CloneToQuad::boundaryInterpolation;
MObject		CloneToQuad::normalInterpolation;
MObject		CloneToQuad::crease;
MObject		CloneToQuad::corner;
MObject		CloneToQuad::relativeMatrix;
MObject		CloneToQuad::shiftIds;

void* CloneToQuad::nodeCreator()
{
	return new CloneToQuad();
}


MStatus CloneToQuad::nodeInitializer()
{
	MFnTypedAttribute		typedAttr;
	MFnNumericAttribute		numAttr;
	MFnEnumAttribute		enumAttr ;
	MFnMatrixAttribute		matAttr ;

	clonedMesh		= typedAttr.create("clonedMesh", "cm", MFnData::kMesh);

	clonedChanged	= numAttr.create("clonedChanged", "cc", MFnNumericData::kBoolean);
	numAttr.setHidden(true);

	quadMesh		= typedAttr.create("quadMesh", "qm", MFnData::kMesh);
	
	cloneUVs		= numAttr.create( "cloneUVs", "cuv", MFnNumericData::kBoolean, true );
	numAttr.setKeyable( true );

	scaleHeight		= numAttr.create("scaleHeight", "sh", MFnNumericData::kDouble, 1.0 );
	numAttr.setKeyable( true );
	numAttr.setMin( .0 ) ;
	numAttr.setMax( 5.0 ) ;
	offsetHeight	= numAttr.create("offsetHeight", "oh", MFnNumericData::kDouble, .0 );
	numAttr.setKeyable( true );
	numAttr.setMin( -5.0 ) ;
	numAttr.setMax( 5.0 ) ;
	areaScale		= numAttr.create("areaScale", "as", MFnNumericData::kDouble, 1.0 );
	numAttr.setKeyable( true );
	numAttr.setMin( .0 ) ;
	numAttr.setMax( 1.0 ) ;

	boundaryInterpolation	= enumAttr.create( "boundaryInterpolation","bi", 1 );
    enumAttr.addField( "Edge" , 0 );
    enumAttr.addField( "Edge and Corner" , 1 );
	enumAttr.setKeyable( true );
	normalInterpolation		= enumAttr.create( "normalInterpolation","ni", 1 );
	enumAttr.addField( "None" , 0 );
    enumAttr.addField( "Phong" , 1 );
    enumAttr.addField( "Derivative" , 2 );
	enumAttr.setKeyable( true );

	crease		= numAttr.create("crease", "cr", MFnNumericData::kFloat, .0f );
	numAttr.setKeyable( true );
	numAttr.setMin( .0 ) ;
	numAttr.setMax( 10.0 ) ;
	corner		= numAttr.create("corner", "co", MFnNumericData::kFloat, .0f );
	numAttr.setKeyable( true );
	numAttr.setMin( .0 ) ;
	numAttr.setMax( 10.0 ) ;

	relativeMatrix		= matAttr.create(  "relativeMatrix", "rm" );

	shiftIds	= numAttr.create( "shiftIds", "si", MFnNumericData::kShort, 0 );
	numAttr.setArray( true ) ;
	

	// output
	outMesh				= typedAttr.create("outMesh", "om", MFnData::kMesh);
	typedAttr.setWritable(false);


	// add
	addAttribute(clonedMesh);
	addAttribute(clonedChanged);
	addAttribute(quadMesh);
	addAttribute(outMesh);
	addAttribute(cloneUVs);
	addAttribute(scaleHeight);
	addAttribute(offsetHeight);
	addAttribute(areaScale);
	addAttribute(boundaryInterpolation);
	addAttribute(normalInterpolation);
	addAttribute(crease);
	addAttribute(corner);
	addAttribute(relativeMatrix);
	addAttribute(shiftIds);
	
	// dependances
	attributeAffects(clonedMesh, clonedChanged);
	attributeAffects(boundaryInterpolation, clonedChanged);
	attributeAffects(crease, clonedChanged);
	attributeAffects(corner, clonedChanged);
	attributeAffects(shiftIds, clonedChanged);

	attributeAffects(clonedMesh, outMesh);
	attributeAffects(boundaryInterpolation, outMesh);
	attributeAffects(crease, outMesh);
	attributeAffects(corner, outMesh);
	attributeAffects(shiftIds, outMesh);
	attributeAffects(normalInterpolation, outMesh);
	attributeAffects(quadMesh, outMesh);
	attributeAffects(scaleHeight, outMesh);
	attributeAffects(offsetHeight, outMesh);
	attributeAffects(areaScale, outMesh);
	attributeAffects(relativeMatrix, outMesh);

	// AE
	init_AETemplate();
	
	return MS::kSuccess;
}


MStatus CloneToQuad::init_AETemplate()
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
	AE_cmd += "	editorTemplate -beginLayout \"Height\" -collapse 0;  ";
	//AE_cmd += "		editorTemplate -addSeparator ;  ";
	AE_cmd += "		editorTemplate -addControl  \"areaScale\" ;  ";
	AE_cmd += "		editorTemplate -addControl  \"scaleHeight\" ;  ";
	AE_cmd += "		editorTemplate -addControl  \"offsetHeight\" ;  ";
	AE_cmd += "	editorTemplate -endLayout;  ";

	AE_cmd += "	editorTemplate -beginLayout \"Subdivision\" -collapse 0;  ";
	AE_cmd += "		editorTemplate -addControl  \"boundaryInterpolation\" ;  ";
	AE_cmd += "		editorTemplate -addControl  \"normalInterpolation\" ;  ";
	AE_cmd += "		editorTemplate -addControl  \"crease\" ;  ";
	AE_cmd += "		editorTemplate -addControl  \"corner\" ;  ";
	AE_cmd += "	editorTemplate -endLayout;  ";

	AE_cmd += "	editorTemplate -addExtraControls;  ";
	AE_cmd += "editorTemplate -endScrollLayout;  ";
	AE_cmd += "}  ";

	return MGlobal::executeCommand(AE_cmd);
}



MStatus CloneToQuad::compute(const MPlug& plug, MDataBlock& data)
{

	if (plug != outMesh){
		return MStatus::kSuccess; }

	int nodeState	= data.inputValue( state ).asInt() ;
	if (nodeState==1) {
		return MStatus::kSuccess ; }


	//
	MStatus status ;
	
	bool cloned_changed		= false ;
	if (!data.isClean(clonedChanged))
	{
		status	= update_clonedData( data );  CHECK_MSTATUS(status) ;

		data.setClean(clonedChanged);
		cloned_changed		= true ;
	}


	//
	MObject quad_Obj ;   status = get_quadMesh( data, quad_Obj ) ;  CHECK_MSTATUS(status) ;

	MFnMesh quad_Msh( quad_Obj ) ;  

	int new_quadV			= quad_Msh.numVertices() ;
	int new_quadE			= quad_Msh.numEdges() ;
	int new_quadF			= quad_Msh.numPolygons() ;
	bool quad_topo_changed	= (new_quadV != quadData.V)  ||  (new_quadE != quadData.E)  ||  (new_quadF != quadData.F) ;


	if (cloned_changed  ||  quad_topo_changed)
	{
		MArrayDataHandle shift_Hs( data.inputArrayValue( shiftIds ) );
		update_quadData( quad_Msh, quad_Obj, shift_Hs );

		bool do_UVs		= data.inputValue(cloneUVs).asBool() ;
		update_tessData( do_UVs );

		short boundaryId	= data.inputValue(boundaryInterpolation).asShort() ;
		float crease_value	= data.inputValue(crease).asFloat() ;
		float corner_value	= data.inputValue(corner).asFloat() ;
		update_subdivData( boundaryId, crease_value, corner_value ) ;
	}

	
	// Deformation
	double scale		= data.inputValue( scaleHeight ).asDouble() ;
	double offset		= data.inputValue( offsetHeight ).asDouble() ;
	double area_scale	= data.inputValue( areaScale ).asDouble() ;
	short normal_mode	= data.inputValue( normalInterpolation ).asShort() ;

	create_world_tessMesh( quad_Obj, quad_Msh,  scale, offset, area_scale, normal_mode  );

	// Mult tessMesh by a Matrix
	MMatrix relative_MM		= data.inputValue( relativeMatrix ).asMatrix();
	if ( ! relative_MM.isEquivalent( MMatrix::identity) ) {
		relative_tessMesh( relative_MM ); }
	

	MFnMesh( tessData.mshObj ).setPoints( tessData.pnts  );
	

	//
	data.outputValue( outMesh ).setMObject(  tessData.ownerObj  );
	data.setClean(plug);

	/*
	// shaders,  now the mesh should exist,  so can I assign shaders
	if (cloned_changed  ||  quad_topo_changed) {
		transfer_shaders() ; }
	*/

	return MStatus::kSuccess;
}



MStatus CloneToQuad::update_clonedData( MDataBlock& data )
{
	MObject cloned_Obj	= data.inputValue(clonedMesh).asMesh();

	if (cloned_Obj.isNull() == true) {
		MGlobal::displayWarning("CloneToQuad : Need a .clonedMesh");
		return MS::kNotFound; }

	// reset
	clonedData	= ClonedData() ;

	// mesh itself
	MFnMesh msh( cloned_Obj );
	msh.getPoints( clonedData.pnts, localSpace);
	clonedData.V	= clonedData.pnts.length() ;

	get_vIds_per_polygon(msh, clonedData.polyCounts, clonedData.polyVertexIds);
	clonedData.F	= clonedData.polyCounts.length() ;

	get_smoothEdges(  msh,  clonedData.smoothEdges  );
	clonedData.E	= (int) clonedData.smoothEdges.size() ;

	get_edge_vIds( msh , clonedData.edgeVertexIds ) ;  // edge vIds in  ascending order.

	msh.getUVSetNames( clonedData.uvSetNames );
	clonedData.S	= clonedData.uvSetNames.length() ;
	clonedData.Us.resize( clonedData.S );
	clonedData.Vs.resize( clonedData.S );
	clonedData.polyUvCounts.resize( clonedData.S );
	clonedData.polyUvIds.resize( clonedData.S );
	for (int ss=0; ss<clonedData.S; ss++) {
		msh.getUVs( clonedData.Us[ss], clonedData.Vs[ss], &clonedData.uvSetNames[ss] ) ;
		msh.getAssignedUVs( clonedData.polyUvCounts[ss], clonedData.polyUvIds[ss], &clonedData.uvSetNames[ss] ); }

	// local BB and deduct parameters in the box
	//clonedData.bb	= msh.boundingBox() ; // does not work
	for (int cv=0; cv<clonedData.V; cv++) { clonedData.bb.expand( clonedData.pnts[cv] );}

	clonedData.u_params.resize( clonedData.V );
	clonedData.v_params.resize( clonedData.V );
	clonedData.heights.resize( clonedData.V );

	MPoint bb_min	= clonedData.bb.min() ;
	MPoint bb_max	= clonedData.bb.max() ;

	for (int cv=0; cv<clonedData.V; cv++ ) {
		clonedData.u_params[cv]		= set_range(  clonedData.pnts[cv].z,  bb_min.z,  bb_max.z,  .0, 1.0 ) ;
		clonedData.v_params[cv]		= set_range(  clonedData.pnts[cv].x,  bb_min.x,  bb_max.x,  .0, 1.0 ) ;
		clonedData.heights[cv]		= clonedData.pnts[cv].y ;   }

	MVector bb_diag			= bb_max - bb_min ;
	clonedData.baseArea		= (bb_max.z-bb_min.z) * (bb_max.x-bb_min.x) ;  // area = dim1*dim2

	return MS::kSuccess ;
}


MStatus CloneToQuad::get_quadMesh( MDataBlock& data, MObject& quad_Obj )
{
	quad_Obj	= data.inputValue(quadMesh).asMesh();

	if (quad_Obj.isNull() == true) {
		MGlobal::displayWarning("CloneToQuad : Need a .quadMesh");
		return MS::kNotFound; }

	return MS::kSuccess ;
}


void CloneToQuad::update_quadData( MFnMesh& quad_Msh, MObject& quad_Obj, MArrayDataHandle& shift_Hs  )
{
	quadData	= QuadData();

	//
	quadData.V	= quad_Msh.numVertices() ;
	quadData.F	= quad_Msh.numPolygons() ;
	
	// shift prepare
	int shiftUsed		= shift_Hs.elementCount() ;
	quadData.shiftIds.resize( quadData.F, 0 );			// default 0 everywhere

	for (int jj=0; jj<shiftUsed; jj++)  {
		shift_Hs.jumpToArrayElement( jj ) ;				// jumpToArrayElement gets the position instead of value
		int fId		= shift_Hs.elementIndex() ;
		if ((fId >= 0) && (fId <quadData.F))     { quadData.shiftIds[fId]  = shift_Hs.inputValue().asInt() ; }  }

	//
	get_vIds_per_polygon( quad_Msh, quadData.polyCounts, quadData.polyVertexIds);

	int ii=0 ;
	for ( int ff=0; ff<quadData.F ; ff++)
	{
		int& polyV	= quadData.polyCounts[ff] ;
		if (polyV==4) { quadData.quadIds.push_back( ff ); }
	
		// shift vIds order
		int& shift	= quadData.shiftIds[ff] ;
		if (shift == 0) {
			ii += polyV ; }
		else  {
			int tmp_ii	= ii ;
			intVec tmp_vIds( polyV );
			for (int vv=0; vv<polyV; vv++)  { tmp_vIds[vv]	= quadData.polyVertexIds[ii++] ; }
			for (int vv=0; vv<polyV; vv++)  { quadData.polyVertexIds[tmp_ii + vv] = tmp_vIds[ (vv+shift)%polyV ] ; }  }
	}

	quadData.Q	= (int) quadData.quadIds.size() ;


	//
	quadData.E	= quad_Msh.numEdges() ;
	quadData.edgeVertices.resize( quadData.E );

	for (int ee=0 ; ee<quadData.E; ee++)  {
		int2 vertices  ;  quad_Msh.getEdgeVertices( ee, vertices );
		quadData.edgeVertices[ee].setLength( 2 );
		quadData.edgeVertices[ee][0]	= vertices[0] ;
		quadData.edgeVertices[ee][1]	= vertices[1] ;  }


	// vertex adjacent_faces needed by areaScale
	get_vertex_connectedFaces( quad_Obj,  quadData.adjPolyIds  );
}


void CloneToQuad::update_tessData( bool& do_UVs )
{
	
	tessData	= TesselatedData() ; // reset

	// pnts
	tessData.V	=  quadData.Q * clonedData.V ;
	tessData.pnts.setLength( tessData.V  );
	
	for (int qq=0; qq<quadData.Q; qq++) {
		for (int cv=0; cv<clonedData.V; cv++) {
			tessData.pnts.set(  clonedData.pnts[cv],  clonedData.V*qq + cv  );  }  }

	// polyCounts
	tessData.F	=  quadData.Q * clonedData.F ;
	tessData.polyCounts.setLength( tessData.F );
	
	for (int qq=0; qq<quadData.Q; qq++) {
		for (int cf=0; cf<clonedData.F; cf++) {
			tessData.polyCounts.set( clonedData.polyCounts[cf],  clonedData.F*qq + cf  ) ; } }

	// polyVertexIds
	int c_p_vIds	= clonedData.polyVertexIds.length() ;
	tessData.polyVertexIds.setLength( quadData.Q * c_p_vIds );
	
	for (int qq=0; qq<quadData.Q; qq++) {
		for (int cpv=0; cpv<c_p_vIds; cpv++) {
			int& vId		= clonedData.polyVertexIds[cpv] ;
			int new_vId		= qq*clonedData.V + vId ;
			tessData.polyVertexIds.set(  new_vId,  c_p_vIds*qq + cpv  ) ;  } }


	//
	MFnMesh tess_msh ;
	tessData.ownerObj	= MFnMeshData().create() ;
	tessData.mshObj		= tess_msh.create(	tessData.V, tessData.F, tessData.pnts,
											tessData.polyCounts, tessData.polyVertexIds,
											tessData.ownerObj );

	
	// Edge smoothing
	// The clonedMesh has been edited previously by the user,  so vertexIds and edgeIds  are NOT related anymore.
	// Maya has created a new mesh with same vertexIds but different edgeIds !
	
	intVec clonedEdgeIds( clonedData.E );							// Luckily, the edge order seems consistent per clone :)

	for (int te=0; te<clonedData.E; te++)  {
		int2 vIds ;  tess_msh.getEdgeVertices(te, vIds) ;
		if (vIds[0] > vIds[1])  { std::swap(vIds[0],vIds[1]); }		// ascending order
		clonedEdgeIds[te]	= vecPairII_position( std::make_pair( vIds[0], vIds[1] ), clonedData.edgeVertexIds ) ; }

	for (int qq=0; qq<quadData.Q; qq++) {
		for (int te=0; te<clonedData.E; te++) {
			int& cloned_eId		= clonedEdgeIds[te] ;
			tess_msh.setEdgeSmoothing( clonedData.E*qq + te,  clonedData.smoothEdges[cloned_eId] ); } }


	// UVs
	if (do_UVs)
	{
		for (int ss=0; ss<clonedData.S; ss++)
		{
			// Us Vs
			int cloned_numUV	= clonedData.Us[ss].length() ;
			int tess_numUV		= cloned_numUV * quadData.Q ;
			MFloatArray tess_Us( tess_numUV );
			MFloatArray tess_Vs( tess_numUV );

			for (int qq=0; qq<quadData.Q; qq++) {
				for (int cuv=0; cuv<cloned_numUV; cuv++) {
					tess_Us.set(  clonedData.Us[ss][cuv],  cloned_numUV*qq + cuv  );
					tess_Vs.set(  clonedData.Vs[ss][cuv],  cloned_numUV*qq + cuv  );  }  }

			// polyUvCounts
			MIntArray tess_uvCounts( tessData.F ) ;

			for (int qq=0; qq<quadData.Q; qq++) {
				for (int cf=0; cf<clonedData.F; cf++)  {
					tess_uvCounts.set( clonedData.polyUvCounts[ss][cf],  clonedData.F*qq + cf  ); } }
			
			// polyUvIds
			int c_p_uvIds	= clonedData.polyUvIds[ss].length() ;
			MIntArray tess_uvIds( quadData.Q * c_p_uvIds );
			
			for (int qq=0; qq<quadData.Q; qq++) {
				for (int cpuv=0; cpuv<c_p_uvIds; cpuv++) {
					int& uvId		= clonedData.polyUvIds[ss][cpuv] ;
					int new_uvId	= qq*cloned_numUV + uvId ;
					tess_uvIds.set(  new_uvId,  c_p_uvIds*qq + cpuv  ) ;  } }


			//
			tess_msh.createUVSetWithName(					clonedData.uvSetNames[ss] );
			tess_msh.setUVs(  tess_Us, tess_Vs,				&clonedData.uvSetNames[ss] );
			tess_msh.assignUVs( tess_uvCounts, tess_uvIds,	&clonedData.uvSetNames[ss] );

			// Maya sucks to assign UVs !  if ss > 0   it must have more UVs than the previous uvSet
			// Then if uvSetName != map1  I must assignUV one by one  because assignUVs does not work !
		}
	}
	
}


void CloneToQuad::update_subdivData( short& boundaryId, float& crease_value, float& corner_value )
{
	// reset
	subdivData.shut() ;
	subdivData		= SubdivData() ;


	// Refiner Topo
	subdivData.descriptor.numVertices		= quadData.V ;
    subdivData.descriptor.numFaces			= quadData.F ;
    
	int *numVertsPerFace	= new int[quadData.F] ;

	for ( int ff=0; ff<quadData.F ; ff++) {
		numVertsPerFace[ff]		= quadData.polyCounts[ff] ; }


	int numTmp	= quadData.polyVertexIds.length() ;
	int *vertIndicesPerFace	= new int[numTmp] ;

	for ( int ff=0; ff<numTmp ; ff++) {
		vertIndicesPerFace[ff]	= quadData.polyVertexIds[ ff ] ; }

	subdivData.descriptor.numVertsPerFace		= numVertsPerFace ;
    subdivData.descriptor.vertIndicesPerFace	= vertIndicesPerFace ;

	//
	subdivData.intPtrHolder.ptrs.push_back( numVertsPerFace );
	subdivData.intPtrHolder.ptrs.push_back( vertIndicesPerFace );


	// corner , crease ?
	if (corner_value > epsilon)
	{
		subdivData.descriptor.numCorners = quadData.V ;
		int *cornerVertexIndices		= new int[quadData.V] ;
		float *cornerWeights			= new float[quadData.V] ;

		for ( int vv=0; vv<quadData.V ; vv++) {
			cornerVertexIndices[vv]		= vv ;
			cornerWeights[vv]			= corner_value ; }

		subdivData.descriptor.cornerVertexIndices	= cornerVertexIndices ;
		subdivData.descriptor.cornerWeights			= cornerWeights ;

		//
		subdivData.intPtrHolder.ptrs.push_back( cornerVertexIndices );
		subdivData.floatPtrHolder.ptrs.push_back( cornerWeights );
	}

	if (crease_value > epsilon)
	{
		subdivData.descriptor.numCreases	= quadData.E ;
		int *creaseVertexIndexPairs			= new int[quadData.E * 2] ;
		float *creaseWeights				= new float[quadData.E] ;
		
		for ( int ee=0; ee<quadData.E ; ee++) {
			creaseVertexIndexPairs[ee*2+0]		= quadData.edgeVertices[ee][0] ;
			creaseVertexIndexPairs[ee*2+1]		= quadData.edgeVertices[ee][1] ;
			creaseWeights[ee]					= crease_value ; }

		subdivData.descriptor.creaseVertexIndexPairs	= creaseVertexIndexPairs ;
		subdivData.descriptor.creaseWeights				= creaseWeights ;

		//
		subdivData.intPtrHolder.ptrs.push_back( creaseVertexIndexPairs );
		subdivData.floatPtrHolder.ptrs.push_back( creaseWeights );
	}



	// Refiner
	OpenSubdiv::Sdc::SchemeType refiner_type	= OpenSubdiv::Sdc::SCHEME_CATMARK ;

    RefinerOptions refiner_options;
	RefinerOptions::VtxBoundaryInterpolation boundaryModes[]	= {	RefinerOptions::VTX_BOUNDARY_EDGE_ONLY, RefinerOptions::VTX_BOUNDARY_EDGE_AND_CORNER };
    refiner_options.SetVtxBoundaryInterpolation( boundaryModes[ boundaryId ]) ;

	subdivData.refiner_ptr	= RefinerFactory::Create(	subdivData.descriptor,
														RefinerFactory::Options( refiner_type, refiner_options )  ) ;

	int maxLevel	= 10 ;	// only 10 currently allows Crease/Corner to works at value 10.0
	subdivData.refiner_ptr->RefineAdaptive( Refiner::AdaptiveOptions(maxLevel));
	//subdivData.refiner_ptr->RefineUniform( Refiner::UniformOptions( div ));

	/*
	// PatchTable
	PatchTableFactory::Options patchOptions;
    patchOptions.endCapType		= PatchTableFactory::Options::ENDCAP_GREGORY_BASIS ;

	quadData.patchTable_ptr		= PatchTableFactory::Create( *quadData.refiner_ptr, patchOptions) ;
	*/

	// LimitStencil,  only on quads
	PtexIndices	pTex_map	= PtexIndices( *subdivData.refiner_ptr );	// map face to pTex
	LocationArrayVec locationss( quadData.Q ) ;							//  one locationArray can receives all the vertices for this face at once

	for ( int qq=0; qq<quadData.Q ; qq++)
	{
		LocationArray& locations	= locationss[qq] ;
		locations.ptexIdx			= pTex_map.GetFaceId(  quadData.quadIds[qq]  ) ;
		locations.numLocations		= clonedData.V ;

		float *s		= new float[clonedData.V] ;
		float *t		= new float[clonedData.V] ;
		for (int cv=0; cv<clonedData.V; cv++) {
			s[cv]			= (float) clonedData.u_params[cv] ;
			t[cv]			= (float) clonedData.v_params[cv] ; }

		locations.s		= s ;
		locations.t		= t ;

		//
		subdivData.floatPtrHolder.ptrs.push_back( s );
		subdivData.floatPtrHolder.ptrs.push_back( t );
	}

	subdivData.limitTable_ptr	= LimitStencilTableFactory::Create( *subdivData.refiner_ptr,  locationss  );  //  + StencilTable  + patchTable  ?

}



void CloneToQuad::create_world_tessMesh( MObject& quad_Obj, MFnMesh& quad_Msh,
											double& scale,
											double& offset,
											double& area_scale,
											short&	normal_mode)
{
	
	// positions,  interp along surface
	MPointArray quad_Pnts  ;	quad_Msh.getPoints( quad_Pnts, worldSpace );	// dont use getRawPoints because it's localSpace
	
	Vertex *quad_pnts	= new Vertex[ quadData.V ] ;
	for (int qv=0; qv<quadData.V; qv++) {
		quad_pnts[qv].point[0]		= quad_Pnts[qv].x ;
		quad_pnts[qv].point[1]		= quad_Pnts[qv].y ;
		quad_pnts[qv].point[2]		= quad_Pnts[qv].z ; }

	Vertex *tess_pnts	= new Vertex[ tessData.V ] ;	// = quadData.Q * clonedData.V
	subdivData.limitTable_ptr->UpdateValues( quad_pnts,  tess_pnts  );

	
	// normals
	// 0 = no interp
	// 1 = Phong interp   (like positions)
	// 2 = Derivative interp
	Vertex *tess_nrms	= new Vertex[ tessData.V ] ;


	if (normal_mode==0)
	{
		MVectorArray quad_Nrms ;	get_polygon_normals( quad_Msh, worldSpace, quad_Nrms) ;

		for (int qq=0; qq<quadData.Q; qq++)  {
			int& quadId		= quadData.quadIds[qq] ;
			for (int cv=0; cv<clonedData.V; cv++) {
				int tv		= clonedData.V*qq + cv ;
				tess_nrms[tv].point[0]	= quad_Nrms[quadId].x ;
				tess_nrms[tv].point[1]	= quad_Nrms[quadId].y ;
				tess_nrms[tv].point[2]	= quad_Nrms[quadId].z ;  }  }

	}
	else if (normal_mode==1) 
	{
		bool angleWeighted	= false ;
		//MVectorArray quad_vNrms ;	get_vertex_normals( quad_Msh, worldSpace, angleWeighted, quad_vNrms) ;
		MFloatVectorArray quad_vNrms  ;   quad_Msh.getVertexNormals( angleWeighted,  quad_vNrms, worldSpace ) ;

		Vertex *quad_nrms	= new Vertex[ quadData.V ] ;
		for (int qv=0; qv<quadData.V; qv++) {
			quad_nrms[qv].point[0]		= quad_vNrms[qv].x ;
			quad_nrms[qv].point[1]		= quad_vNrms[qv].y ;
			quad_nrms[qv].point[2]		= quad_vNrms[qv].z ; }

		subdivData.limitTable_ptr->UpdateValues( quad_nrms,  tess_nrms  );
	}
	else	
	{
		// normal	= tgtU ^ tgtV
		// A ^ B = (a1b2 - a2b1,  a2b0 - a0b2,  a0b1 - a1b0)
		Vertex *tess_tgtUs	= new Vertex[ tessData.V ] ;
		Vertex *tess_tgtVs	= new Vertex[ tessData.V ] ;
		subdivData.limitTable_ptr->UpdateDerivs( quad_pnts,  tess_tgtUs, tess_tgtVs  );

		for (int tv=0; tv<tessData.V; tv++)
		{
			Vertex& nrm		= tess_nrms[tv] ;	
			nrm.point[0]	= tess_tgtUs[tv].point[1] * tess_tgtVs[tv].point[2] - tess_tgtUs[tv].point[2] * tess_tgtVs[tv].point[1] ;
			nrm.point[1]	= tess_tgtUs[tv].point[2] * tess_tgtVs[tv].point[0] - tess_tgtUs[tv].point[0] * tess_tgtVs[tv].point[2] ;
			nrm.point[2]	= tess_tgtUs[tv].point[0] * tess_tgtVs[tv].point[1] - tess_tgtUs[tv].point[1] * tess_tgtVs[tv].point[0] ;

			double norm		= sqrt(  nrm.point[0]*nrm.point[0] + nrm.point[1]*nrm.point[1] +nrm.point[2]*nrm.point[2]  );
			nrm.point[0]	/= norm ;
			nrm.point[1]	/= norm ;
			nrm.point[2]	/= norm ;
		}

		//
		delete tess_tgtUs ;
		delete tess_tgtVs ;
	}

	/*
	/// DEBUG /////
	if ((tess_pnts[0].point[0] > 100.0)  ||  (tess_pnts[0].point[0] < -100.0))
	{
		int bad = 0 ;
	}
	if ((tess_tgtUs[0].point[0] > 100.0)  ||  (tess_tgtUs[0].point[0] < -100.0))
	{
		int bad = 0 ;
	}
	if ((tess_tgtVs[0].point[0] > 100.0)  ||  (tess_tgtVs[0].point[0] < -100.0))
	{
		int bad = 0 ;
	}
	/////////
	*/

	// areaScale
	// relate each quad_vertex to the average of adj face areas   then   interpolate limitTable.
	// finally multiply current normal per the resulting value.
	if ( area_scale > epsilon )
	{
		doubleVec areas	;	get_face_areas( quad_Obj, worldSpace,  areas ) ;

		Scalar *quad_vAreas		= new Scalar[ quadData.V ];
		for (int qv=0; qv<quadData.V; qv++) {
			int numAdj		= quadData.adjPolyIds[ qv ].length();

			quad_vAreas[qv].value	= .0 ;		// without this the default value was .0 most of the time but sometime QAN !

			for (int aa=0; aa<numAdj; aa++) {
				int& fId		= quadData.adjPolyIds[ qv ][aa] ;
				quad_vAreas[qv].value	+= areas[ fId ] ;  }

			quad_vAreas[qv].value	/= numAdj ;  }

		//
		Scalar *tess_areaScales		= new Scalar[ tessData.V ] ;
		subdivData.limitTable_ptr->UpdateValues( quad_vAreas,  tess_areaScales  );

		/*
		/// DEBUG /////
		if ((tess_areaScales[0].value > 100.0)  ||  (tess_areaScales[0].value < -100.0))
		{
			int bad = 0 ;
		}
		/////////
		*/

		for (int tv=0; tv<tessData.V; tv++)  {
			double sq	= sqrt( tess_areaScales[tv].value  / clonedData.baseArea  );  // because area = square(scale)

			//tess_nrms[tv].point[012]	*= sq ;
			tess_nrms[tv].point[0]	= lerp( tess_nrms[tv].point[0], tess_nrms[tv].point[0] * sq,  area_scale ); // I could optimize this but it's ok
			tess_nrms[tv].point[1]	= lerp( tess_nrms[tv].point[1], tess_nrms[tv].point[1] * sq,  area_scale );
			tess_nrms[tv].point[2]	= lerp( tess_nrms[tv].point[2], tess_nrms[tv].point[2] * sq,  area_scale );
		}

		//
		delete quad_vAreas ;
		delete tess_areaScales ;
	}


	// final pnt	+= normal * (height * scale + offset )
	for (int tv=0; tv<tessData.V; tv++)
	{
		double height	= clonedData.heights[tv%clonedData.V] ;
		
		tessData.pnts[ tv ].x		=  tess_pnts[tv].point[0]  +  tess_nrms[tv].point[0] * (height * scale + offset) ;
		tessData.pnts[ tv ].y		=  tess_pnts[tv].point[1]  +  tess_nrms[tv].point[1] * (height * scale + offset) ;
		tessData.pnts[ tv ].z		=  tess_pnts[tv].point[2]  +  tess_nrms[tv].point[2] * (height * scale + offset) ;
	}


	//
	delete quad_pnts ;
	delete tess_pnts ;
	delete tess_nrms ;

	/*
	MPointArray quad_Pnts  ;  quad_Msh.getPoints( quad_Pnts, worldSpace );
	MVectorArray quad_vNrmls ; get_vertex_normals( quad_Msh, worldSpace, angleWeighted, quad_vNrmls) ;
	MVectorArray quad_fNrmls ; get_polygon_normals( quad_Msh, worldSpace, quad_fNrmls) ;

	for (int qf=0; qf<quadData.F; qf++)
	{
		//
		int& v0	= quadData.quadVertices[qf*4  ] ;	MPoint& p00 = quad_Pnts[v0] ;	MVector& vn00 = quad_vNrmls[v0] ;
		int& v1	= quadData.quadVertices[qf*4+1] ;	MPoint& p10 = quad_Pnts[v1] ;	MVector& vn10 = quad_vNrmls[v1] ;
		int& v2	= quadData.quadVertices[qf*4+2] ;	MPoint& p11 = quad_Pnts[v2] ;	MVector& vn11 = quad_vNrmls[v2] ;
		int& v3	= quadData.quadVertices[qf*4+3] ;	MPoint& p01 = quad_Pnts[v3] ;	MVector& vn01 = quad_vNrmls[v3] ;
		
		
		//MVector& fn		= quad_fNrmls[qf] ;

		// get tangents
		// multiply some by -1 because hermite expect sAme directions vectors, opposite of Bezier.
		MVector tu00  ;  get_tangent( p00, p10, n00,  tgt_edge_ratio, curvature_ratio,  tu00 );
		MVector tv00  ;  get_tangent( p00, p01, n00,  tgt_edge_ratio, curvature_ratio,  tv00 );
		
		MVector tu01  ;  get_tangent( p01, p11, n01,  tgt_edge_ratio, curvature_ratio,  tu01 );
		MVector tv01  ;  get_tangent( p01, p00, n01,  tgt_edge_ratio, curvature_ratio,  tv01 );
		tv01	*= -1 ;
		
		MVector tu10  ;  get_tangent( p10, p00, n10,  tgt_edge_ratio, curvature_ratio,  tu10 );
		tu10	*= -1 ;
		MVector tv10  ;  get_tangent( p10, p11, n10,  tgt_edge_ratio, curvature_ratio,  tv10 );

		MVector tu11  ;  get_tangent( p11, p01, n11,  tgt_edge_ratio, curvature_ratio,  tu11 );
		tu11	*= -1 ;
		MVector tv11  ;  get_tangent( p11, p10, n11,  tgt_edge_ratio, curvature_ratio,  tv11 );
		tv11	*= -1 ;
		

		// 

		for (int cv=0; cv<clonedData.V; cv++)
		{
			MPoint& cloned_Pnt	= clonedData.pnts[cv] ;

			double& bary00	= clonedData.barys[4*cv] ;
			double& bary10	= clonedData.barys[4*cv+1] ;
			double& bary11	= clonedData.barys[4*cv+2] ;
			double& bary01	= clonedData.barys[4*cv+3] ;


			MPoint& p	= tessData.pnts[ clonedData.V*qf + cv ];
			
			eval_hermite_patch(	p00, p01, p10, p11,
								n00, n01, n10, n11,
								tu00, tu01, tu10, tu11,
								tv00, tv01, tv10, tv11,
								u, v, w,
								p  );
			eval_nagata_quad_patch(	p00, p01, p10, p11,
									n00, n01, n10, n11,
									u, v, w,
									p  );
			eval_phong(		p00, p10, p11, p01,
							vn00, vn10, vn11, vn01, fn,
							cloned_Pnt,
							bary00, bary10, bary11, bary01,
							p  );
		}
	}
	*/
}


void CloneToQuad::relative_tessMesh( MMatrix& relative_MM ) 
{

	for (int vv=0; vv<tessData.V; vv++)
	{
		tessData.pnts[vv]	*= relative_MM ;
	}

}

/*
void CloneToQuad::transfer_shaders()
{

	// get shaders from cloned_mesh

	MObject this_Obj	= thisMObject() ;
	MFnDependencyNode this_Dep(  this_Obj  );

	MPlug this_cloned_Plug	= this_Dep.findPlug( clonedMesh, false );				// false = wantNetworkedPlug

	MPlugArray tmp_Plugs ;
	bool connected_b	= this_cloned_Plug.connectedTo( tmp_Plugs, true, false  );	// this_cloned_plug is destination

	MObject cloned_Obj	= tmp_Plugs[0].node() ;

	MFnDagNode cloned_DagNode( cloned_Obj );
	MDagPath cloned_Path  ;  cloned_DagNode.getPath( cloned_Path ) ;

	MObjectArray	shader_Objs ;		// sets
	MIntArray		shaderPerPoly ;		// dim F,  id in shaders
	MFnMesh( cloned_Path ).getConnectedShaders( 0, shader_Objs, shaderPerPoly );	// 0 = instanceNumber

	
	
	// assign shaders to tess_mesh(es)
	
	int numShader	= shader_Objs.length() ;

	if (numShader > 0)
	{
		//
		MPlug this_tess_Plug	= this_Dep.findPlug( outMesh, false );				// false = wantNetworkedPlug

		tmp_Plugs.setLength( 0 ); ;
		connected_b		= this_tess_Plug.connectedTo( tmp_Plugs, false, true  );	// this_tess_Plug is source

		int numTess		= tmp_Plugs.length() ;

		//
		if (numShader==1)
		{
			MFnSet shader_Set( shader_Objs[0] ) ;
			
			for (int tt=0 ; tt<numTess; tt++)
			{
				MPlug& tess_Plug	= tmp_Plugs[tt] ;
				//MObject tess_Obj	= tess_Plug.node() ;
				//MFnDagNode tess_DagNode( tess_Obj );
				//MDagPath tess_Path  ;  tess_DagNode.getPath( tess_Path ) ;
				shader_Set.addMember( tess_Plug );
				//shader_Set.addMember( tess_Obj );
			}
		}

		else  // >=2
		{
			intVec tess_face_shaderId(  tessData.F  );

			for (int qq=0; qq<quadData.Q; qq++) {
				for (int cf=0; cf<clonedData.F; cf++) {
					int tess_fId	= clonedData.F*qq + cf ;
					tess_face_shaderId[ tess_fId ]	= shaderPerPoly[ cf ] ;  }  }

			for (int tt=0 ; tt<numTess; tt++)
			{
				MPlug& tess_Plug	= tmp_Plugs[tt] ;
				MObject tess_Obj	= tess_Plug.node() ;
				MFnDagNode tess_DagNode( tess_Obj );

				MDagPath tess_Path  ;  tess_DagNode.getPath( tess_Path ) ;

				MItMeshPolygon iter( tess_Path );

				////// DEBUG
				int numPoly		= iter.count() ;
				///////

				for (int ss=0; ss<numShader; ss++)
				{
					MFnSet shader_Set( shader_Objs[ss] ) ;

					for (iter.reset(); !iter.isDone(); iter.next() )
					{
						int idx			= iter.index() ;
						int& shaderId	= tess_face_shaderId[idx] ;


						if (shaderId == ss)
						{
							shader_Set.addMember( tess_Path, iter.currentItem() ) ; 
						}

					}
				}
				
			}

		}

	}
	
}
*/



//#pragma optimize( "", on )

