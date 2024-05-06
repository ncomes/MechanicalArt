

#include "stdafx.h"



void get_average_normals(	MObject& msh, MSpace::Space space,
								MVectorArray& avNormals );


void get_vIds_per_polygon(	MFnMesh& msh,
							MIntArray& polyCounts, MIntArray& polyVertexIds);


void get_smoothEdges(MFnMesh& msh, boolVec& smoothEdges);


void get_edge_vIds( MFnMesh& msh , vecPairII& edgeVertexIds );


void get_polygon_normals( MFnMesh& msh, MSpace::Space space,  MVectorArray& nrms);
void get_vertex_normals( MFnMesh& msh, MSpace::Space space, bool& angleWeighted,   MVectorArray& nrms);


void get_vertex_connectedFaces( MObject& mshObj,  vecMIntArray& adjPolyIds  );

void get_face_areas( MObject& mshObj , MSpace::Space space,  doubleVec& areas ) ;


