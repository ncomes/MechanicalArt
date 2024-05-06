


#include "component.h"



void get_average_normals( MObject& msh, MSpace::Space space, MVectorArray& avNormals )
{
	MItMeshVertex iter(msh);
	int vNum	= (int)iter.count();

	avNormals.setLength(vNum);
	int ii = 0;
	for (iter.reset(); !iter.isDone(); iter.next())
	{
		iter.getNormal(avNormals[ii++], space);
	}

}


void get_vIds_per_polygon(MFnMesh& msh, MIntArray& polyCounts, MIntArray& polyVertexIds)
{
	int numF	= msh.numPolygons();

	polyCounts.setLength( numF );
	polyVertexIds.setLength( 0 );

	for (int ff = 0; ff < numF; ff++)
	{
		MIntArray vIds;
		msh.getPolygonVertices( ff, vIds);

		int numV = vIds.length();
		polyCounts.set( numV, ff );

		for (int vv = 0; vv < numV; vv++) {
			polyVertexIds.append( vIds[vv] ); }
	}
}



void get_smoothEdges(MFnMesh& msh, boolVec& smoothEdges)
{
	int numE	= msh.numEdges();
	smoothEdges.resize( numE );

	for (int ee = 0; ee < numE; ee++)
	{
		smoothEdges[ee]	= msh.isEdgeSmooth( ee );
	}
}



void get_edge_vIds( MFnMesh& msh , vecPairII& edgeVertexIds )
// return in ascending order, just to be conistent.
{
	int numE	= msh.numEdges();

	edgeVertexIds.resize( numE );

	for (int ee=0; ee<numE; ee++) {
		int2 vIds ;  msh.getEdgeVertices(ee, vIds) ;
		if (vIds[0] > vIds[1])  { std::swap(vIds[0],vIds[1]); }

		edgeVertexIds[ee]	= std::make_pair( vIds[0], vIds[1] ) ;   }
}



void get_polygon_normals( MFnMesh& msh, MSpace::Space space,  MVectorArray& nrms)
{
	int numF	= msh.numPolygons();
	nrms.setLength( numF );

	for (int ff = 0; ff < numF; ff++)
	{
		msh.getPolygonNormal( ff, nrms[ff], space );
	}

}



void get_vertex_normals( MFnMesh& msh, MSpace::Space space, bool& angleWeighted,   MVectorArray& nrms)
{
	int numV	= msh.numVertices();
	nrms.setLength( numV );

	for (int vv = 0; vv < numV; vv++)
	{
		msh.getVertexNormal( vv, angleWeighted,  nrms[vv], space );
	}

}



/*
void get_points_and_normals_one_by_one( MFnMesh& msh, MSpace::Space space, MPointArray& pnts )
{
	int numV	= msh.numVertices();
	nrms.setLength( numV );

	for (int vv = 0; vv < numV; vv++)
	{
		msh.getVertexNormal( vv, angleWeighted,  nrms[vv], space );
	}

}
*/



void get_vertex_connectedFaces( MObject& mshObj,  vecMIntArray& adjPolyIds  )
{
	MItMeshVertex it( mshObj  );

	adjPolyIds.resize( it.count()  ) ;

	for (it.reset(); !it.isDone(); it.next())
	{
		int vId		= it.index() ;
		MIntArray adj_polys ;   it.getConnectedFaces(  adjPolyIds[vId]  );
	}

}

void get_face_areas( MObject& mshObj, MSpace::Space space,  doubleVec& areas )
{
	MItMeshPolygon it( mshObj  );

	areas.resize( it.count() );
	
	for (it.reset(); !it.isDone(); it.next())
	{
		it.getArea(  areas[it.index()], space );
	}
}





