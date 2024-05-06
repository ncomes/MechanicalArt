


#include <vector>

#include <maya/MPointArray.h>





std::vector<std::vector<double>> adjacent_matrix( std::vector<std::vector<int>>& connectedVtx, MPointArray& pnts ) ;


std::vector<std::vector<int>> floyd_warshall( std::vector<std::vector<double>>& dmat  ) ;


std::vector<int> rebuild_path( int ii, int jj,
					std::vector<std::vector<double>>& dmat,
					std::vector<std::vector<int>>& pmat ) ;




