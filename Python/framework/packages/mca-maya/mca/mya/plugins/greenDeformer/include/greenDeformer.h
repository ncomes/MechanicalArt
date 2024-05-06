#ifndef _greenDeformer
#define _greenDeformer

#include "stdafx.h"






class GreenDeformer : public MPxDeformerNode
{
public:
	GreenDeformer();
	virtual				~GreenDeformer();

	static  MTypeId		id;
	static  MString		name;

	static  void*		nodeCreator();

	static  MStatus     nodeInitializer();
	static	MStatus		init_AETemplate();


	// attributes
	// assume cage is triangulated
	static  MObject     cageOrig ;		// connect .mesh   never .worldMesh
	static  MObject     cageDeformed ;
	static  MObject     cageChanged;	// fake
	static  MObject     preserveScale ;
	static  MObject     refresh ;		// force refresh

	//
	virtual MStatus		compute(const MPlug& plug, MDataBlock& data);


private:
	MMeshIntersector cageOrig_Intersector ;	// static
	MPointArray		cageOrig_Pnts;			// static
	MVectorArray	cageOrig_Nrmls;			// static
	MIntArrayVec	cageOrig_vIdsPerFace;	// static
	
	MPointArray		cageDeformed_Pnts;		// dynamic
	MVectorArray	cageDeformed_Nrmls;		// dynamic

	MDoubleArray	cageOrig_faceAreas;		// static
	void	update_faceAreas();

	MDoubleArray	scaleFactors ;	// dim cage_face
	void	get_scaleFactors();		// compute once when cage is deformed


	MIntArrayMap	orig_vIds;		// [inputGeometry_id] [geoIt vId]
	MPointArrayMap	orig_Pnts;		// [inputGeometry_id] [geoIt pnt]
	void	update_orig( int& ii_id, MItGeometry& output_It);

	ddVecMap		phis;			// cageVertexWeight dim  [inputGeometry_id] [geoIt vId] [cage_vId] 
	ddVecMap		psis;			// cageFaceWeight   dim  [inputGeometry_id] [geoIt vId] [cage_fId] 
	void	update_green( int& ii_id );
	double	GCTriInt( MVector& p, MVector& v1, MVector& v2, MVector& n  );

	MPointArray		apply_green(  int& ii_id, double& preserveShape_d );

	MFloatArray		wgts ;				// dim geoIt_vId
	void	update_weights( MDataBlock& data,  int& ii_id  );

	

};

#endif






