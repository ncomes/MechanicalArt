


#include "stdafx.h"





void get_points_and_normals(MObject& mesh_Obj,
							MPointArray& out_Pnts,
							MVectorArray& out_Nrmls,
							MSpace::Space space,

							bool check,
							bool& is_triangular,
							bool& is_holed,
							MIntArrayVec& out_vIdsPerFace );



//int get_closest_faceId( MPoint& pnt, MFnMesh& msh  );

int get_closest_faceId( MPoint& pnt, MMeshIntersector& intersector ) ;





