

#include <vector>

#include <maya/MObject.h>
#include <maya/MDagPath.h>
#include <maya/MIntArray.h>
#include <maya/MPointArray.h>
#include <maya/MFnMesh.h>


MPointArray get_msh_points( const MFnMesh &msh, MSpace::Space space );

MPointArray filter_vertices( MPointArray& all_Pnts, MIntArray& usedVertices ) ;

MIntArray get_vertexIds( const MFnMesh &msh );

std::vector<std::vector<int>> get_face_connectedVertices( MObject &msh, bool includeItself   ) ;

MIntArray get_connectedVtxIds( MDagPath &dagPath, int &vtxId  ) ;

std::vector<std::vector<int>> grow_using_existingVector( std::vector<std::vector<int>>& vector_of_connectedIds, int& levelIds  ) ;

