
#include "shortestPath.h"


double infinity	= 9999999.0 ;






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




std::vector<std::vector<int>> floyd_warshall( std::vector<std::vector<double>>& dmat  )
// matrix as & to modify it
// return the path matrix of ids
{
	int N = (int)dmat.size() ;



	// init path_matrix to -1
	//std::vector<std::vector<std::vector<int>>> pmat ;
	std::vector<std::vector<int>> pmat ;
	pmat.resize( N );

	for (int ii=0; ii< N; ii++)
	{
		pmat[ii].resize(N);

		//for (int jj=0; jj<N; jj++)
		//{
		//	pmat[ii][jj]	= -1 ;
		//}
	}
	

	
	//original and ONEROUS version  ( O(N3)
	
    for (int kk=0; kk<N; kk++)
    {
		//////////////////////////////////////////////////
		printf("%.6f \n", (double)kk/(double)N);//////// 


        for (int ii=0; ii< N; ii++)
        {
			for (int jj=0; jj<N; jj++)
			// optimize due to symmetric distanceMatrix
            //for (int jj=0; jj<ii; jj++)
            {
				double d	= dmat[ii][kk] + dmat[kk][jj];

				if ( d < dmat[ii][jj] )
				{
                    dmat[ii][jj]	= d ;

				/*
					pmat[ii][jj].clear( );
					pmat[ii][jj].push_back( kk );
				*/
                }
				/*
				else if ((d == dmat[ii][jj]) && (kk != jj) && (kk != ii))
				{
					pmat[ii][jj].push_back( kk );
				}
				*/
            }
        }
	}
	
	/*
	for (int ii=0; ii<N; ii++)
    {
		//////////////////////////////////////////////////
		printf("%.6f \n", (double)ii/(double)N);//////// 


		for (int jj=0; jj<N; jj++)
		{
			if (ii != jj)
			{
				double aji	= (ii < jj) ? dmat[jj][ii] : dmat[ii][jj]; // use only a square matrix
				
				if (aji == infinity) // skip if no path
				{
					continue;
				}


				for (int kk= min(ii,jj)-1 ; kk >= 0; kk--)
				{
					double newjk	= aji + dmat[ii][kk] ;

					if (newjk < dmat[jj][kk])
					{
						dmat[jj][kk]	= newjk;
						//pmat[jj][kk]	= kk ;
					}
				}

				for (int kk= ii + 1 ; kk<jj; kk++)
				{
					double newjk	= aji + dmat[kk][ii];

					if (newjk < dmat[jj][kk])
					{
						dmat[jj][kk]	= newjk;
					}
				}
			}
		}
	}
	*/


	return pmat ;
}





std::vector<int> rebuild_path( int ii, int jj,
					std::vector<std::vector<double>>& dmat,
					std::vector<std::vector<int>>& pmat )
// from i to j
{
	std::vector<int> path_ids ;


	if (dmat[ii][jj]==infinity)
	{
		// no path
		return path_ids ;
	}

	int intermediate = pmat[ii][jj] ;




	return path_ids ;
}




/*
////////////////////////// shortest path

	// build the graph : each point need destinationPoints + distances

	// connected vertices by vertex
	//std::vector<std::vector<int>> connectedVtx	= get_face_connectedVertices( source_Obj, false ) ;
	connectedVtx	= get_face_connectedVertices( source_Obj, false ) ;

	// distances between each connected pairs
	//std::vector<std::vector<double>> distances	= get_connectedDistances( connectedVtx, src_Pnts ) ;

	// Floyd-Warshall algo --> build the adjacent matrix  then  upgrade it  to shortestDistance_matrix

	std::vector<std::vector<double>> distance_matrix	= adjacent_matrix( connectedVtx, src_Pnts ) ;
	printf( "11111111111" ) ;

	std::vector<std::vector<int>> path_matrix	= floyd_warshall( distance_matrix );
	printf( "22222222222" ) ;


	//////////////////////////
*/