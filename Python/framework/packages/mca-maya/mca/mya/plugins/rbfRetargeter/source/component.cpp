
#include "component.h"


#include <set>

#include <maya/MFnMeshData.h>
#include <maya/MPoint.h>

#include <maya/MItMeshVertex.h>
#include <maya/MItMeshPolygon.h>
#include <maya/MFnSingleIndexedComponent.h>







MPointArray get_msh_points( const MFnMesh &msh, MSpace::Space space = MSpace::kObject )
{
	MPointArray pnts ;
	msh.getPoints(pnts, space) ;

	return pnts ;
}


MPointArray filter_vertices( MPointArray& all_Pnts, MIntArray& usedVertices )
{
	int num	= usedVertices.length() ;

	MPointArray filtered_Pnts( num ) ;

	for (int ii=0; ii<num; ii++)
	{
		filtered_Pnts[ii]	= all_Pnts[usedVertices[ii]] ;
	}

	return filtered_Pnts ;
}


MIntArray get_vertexIds( const MFnMesh &msh )
{
	MIntArray vertexCount ;
	MIntArray vertexIds ;
	msh.getVertices( vertexCount, vertexIds  );

	return vertexIds ;
}





/*
std::vector<std::vector<double>> get_connectedDistances( std::vector<std::vector<int>>& connectedVtx, MPointArray& pnts )
{

	std::vector<std::vector<double>> distances ;
	int num		= connectedVtx.size() ;
	distances.resize( num  ) ;
	

	for (int ii=0 ; ii<num; ii++)
	{
		std::vector<double> ii_connected_distances ;
		int num2	= connectedVtx[ii].size() ;
		ii_connected_distances.resize( num2  ) ;

		for (int jj=0 ; jj<num2; jj++)
		{
			int jjId	= connectedVtx[ii][jj] ;
			double d	= sqrt( (pnts[jjId][0]-pnts[ii][0])*(pnts[jjId][0]-pnts[ii][0])+(pnts[jjId][1]-pnts[ii][1])*(pnts[jjId][1]-pnts[ii][1])+(pnts[jjId][2]-pnts[ii][2])*(pnts[jjId][2]-pnts[ii][2]));

			distances[ii][jj]	= d ;
			//distances[jj][??]	= d ; // can be optimized here,  we dont need to do the euclidian twice
		}
	}

	return distances ;
}





std::vector<std::vector<double>> adjacent_matrix( std::vector<std::vector<int>>& connectedVtx, MPointArray& pnts )
{

	std::vector<std::vector<double>> adj_matrix ;
	int num		= (int)connectedVtx.size() ;
	adj_matrix.resize( num  ) ;
	

	// init to .0 or infinity

	for (int ii=0 ; ii<num; ii++)
	{
		adj_matrix[ii].resize( num  ) ;

		for (int jj=0 ; jj<num; jj++)
		{
			if (ii==jj)	{ adj_matrix[ii][jj]	= .0 ; }
			else		{ adj_matrix[ii][jj]	= infinity ; }
		}
	}



	for (int ii=0 ; ii<num; ii++)
	{
		int num2	= (int)connectedVtx[ii].size() ;

		for (int jj=0 ; jj<num2; jj++)
		{
			int jjId	= connectedVtx[ii][jj] ;

			//** do it only if it is not already done

			if (adj_matrix[ii][jjId]==infinity)
			{
				double d	= sqrt( (pnts[jjId][0]-pnts[ii][0])*(pnts[jjId][0]-pnts[ii][0])+(pnts[jjId][1]-pnts[ii][1])*(pnts[jjId][1]-pnts[ii][1])+(pnts[jjId][2]-pnts[ii][2])*(pnts[jjId][2]-pnts[ii][2]));

				adj_matrix[ii][jjId]	= d ;
				adj_matrix[jjId][ii]	= d ; //**
			}
		}
	}

	return adj_matrix ;
}


*/



std::vector<std::vector<int>> get_face_connectedVertices( MObject& msh, bool includeItself )
// get connected vertices by faces
{

	MItMeshVertex iter1( msh );
	MItMeshPolygon iter2( msh );

	int vNum	= iter1.count() ;



	//
	std::vector<std::vector<int>> vector_of_vIds ;
	vector_of_vIds.resize( vNum ) ;


	while ( !iter1.isDone() )
	{
		int vId		= iter1.index() ;


		// get connected faces
		MIntArray connectedFaces ;
		iter1.getConnectedFaces( connectedFaces ) ;

		

		// deduct the vertices inside each polygon
		std::set<int> set ;

		for (int ii=0 ; ii<(int)connectedFaces.length(); ii++)
		{
			// go to polygon
			// get its vertices
			// put them in the Set[vId]
			int currIter2Id = iter2.index() ;
			iter2.setIndex( connectedFaces[ii], currIter2Id ) ;


			MIntArray polygonVtxIds ;
			iter2.getVertices( polygonVtxIds ) ;

			for (unsigned int jj=0 ; jj<polygonVtxIds.length(); jj++)
			{
				// ignore vId !?
				if ((polygonVtxIds[jj] == vId) && (includeItself==false))
				{
					continue ;
				}
				else
				{
					set.insert( polygonVtxIds[jj]  ) ;
				}
			}
		}


		// Set to vector
		int set_size	= (int)set.size() ;
		vector_of_vIds[vId].resize( set_size ) ;

		int kk = 0 ;
		for (std::set<int>::iterator it=set.begin(); it!=set.end(); it++) { vector_of_vIds[vId][kk++]	= *it ; }


		//
		iter1.next() ;
	}


	return vector_of_vIds ;
}






MIntArray get_connectedVtxIds( MDagPath &dagPath, int &vtxId  )
// get direct connected vertices by edges
{
	
	// build component
	MFnSingleIndexedComponent compData	;
	MObject comp_Obj = compData.create( MFn::kMeshVertComponent ) ;
	compData.addElement( vtxId ) ;

	MItMeshVertex iter1( dagPath, comp_Obj );

	MIntArray connectedVtx ;
	iter1.getConnectedVertices( connectedVtx ) ;

	return connectedVtx ;
}





std::vector<std::vector<int>> grow_using_existingVector( std::vector<std::vector<int>>& vector_of_connectedIds, int& growLevel  )
{
	
	int vNum	= (int)vector_of_connectedIds.size() ;


	//** vector[ set[ ids ] ]
	// add dv elements
	std::vector<std::set<int>> final_vectorSet ;
	final_vectorSet.resize(vNum) ;

	for (int ii=0 ; ii<vNum; ii++)
	{
		for (int jj=0 ; jj<(int)vector_of_connectedIds[ii].size(); jj++)
		{
			final_vectorSet[ii].insert( vector_of_connectedIds[ii][jj] ) ;
		}
	}
	

	// add new elements
	for (int ii=0 ; ii<vNum; ii++)
	{ 

		std::set<int> set ;
		std::vector<int> lastConnected = vector_of_connectedIds[ii] ;


		for (int ll=1 ; ll<growLevel; ll++)
		{
			std::vector<int> copyConnected =  lastConnected ;
			lastConnected.clear() ;

			for (int jj=0 ; jj<(int)copyConnected.size(); jj++)
			{
				std::vector<int> connecteds = vector_of_connectedIds[copyConnected[jj]]  ;

				for (int kk=0 ; kk<(int)connecteds.size(); kk++)
				{
					lastConnected.push_back( connecteds[kk] ) ;
					set.insert(  connecteds[kk] ) ;
				}
			}
		}


		//int tt = 0 ;
		//finalVector[ii].resize( finalVector[ii].size()+set.size() ) ; { finalVector[finalVector[ii].size()+tt] = *it ; }
		for (auto it=set.begin(); it!=set.end(); it++)    { final_vectorSet[ii].insert( *it ); }
	}


	//** reconvert to vector
	std::vector<std::vector<int>> finalVector ;
	finalVector.resize( vNum ) ;

	for (int ii=0 ; ii<vNum; ii++)
	{
		finalVector[ii].resize( (int)final_vectorSet[ii].size() ) ;

		int tt = 0 ;
		for (auto it=final_vectorSet[ii].begin(); it!=final_vectorSet[ii].end(); it++)
		{
			finalVector[ii][tt++] = *it ;
		}
	}

	return finalVector ;
}
