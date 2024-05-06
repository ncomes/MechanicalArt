

#include "component.h"




void get_points_and_normals(MObject& mesh_Obj,
							MPointArray& out_Pnts,
							MVectorArray& out_Nrmls,
							MSpace::Space space,

							bool check,
							bool& is_triangular,
							bool& is_holed,
							MIntArrayVec& out_vIdsPerFace )
// checkTriangle is input and output at the same time
// if it is true, check if all polygons are triangles
// if not, checkTriangle becomes false
{


	//
	out_Pnts.clear();
	MFnMesh( mesh_Obj  ).getPoints( out_Pnts, space  );



	//
	out_Nrmls.clear();
	MItMeshPolygon face_It( mesh_Obj );

	int numF	= face_It.count();
	out_Nrmls.setLength( numF );

	for ( face_It.reset() ; !face_It.isDone(); face_It.next() )
	{
		int fId		= face_It.index();
		face_It.getNormal( out_Nrmls[fId], space );
	}



	// triangles ?
	if (check==true)
	{
		out_vIdsPerFace.clear();
		out_vIdsPerFace.resize( numF  );


		for ( face_It.reset() ; !face_It.isDone(); face_It.next() )
		{
			int fId		= face_It.index() ;

			MIntArray f_vIds;
			face_It.getVertices( f_vIds );


			//
			if ( f_vIds.length() != 3 ) {
				MString err = "GreenDeformer : Face[";err+=fId;err+="] not triangular found in cageOrig, please triangulate all cage";
				MGlobal::displayError( err );
				is_triangular	= false ;
				return ; }

			//
			if ( face_It.onBoundary() ) {
				MString err = "GreenDeformer : Hole found near Face[";err+=fId;err+="] in cageOrig, please fill all holes";
				MGlobal::displayError( err );
				is_holed		= true ;
				return ; }

			out_vIdsPerFace[fId]	= f_vIds ;
		}
	}
}












int get_closest_faceId( MPoint& pnt, MMeshIntersector& intersector  )
{
	MPointOnMesh pointInfo ;
	MStatus status	= intersector.getClosestPoint( pnt, pointInfo ) ;

	return pointInfo.faceIndex() ;
}





