


#include <maya/MStatus.h>
#include <maya/MPxDeformerNode.h>
#include <maya/MGlobal.h>

#include <maya/MTypeId.h>
#include <maya/MString.h>
#include <maya/MObject.h>
#include <maya/MDagPath.h>

#include <maya/MFnTypedAttribute.h>
#include <maya/MFnNumericAttribute.h>

#include <maya/MFnMesh.h>
#include <maya/MItGeometry.h>
#include <maya/MItMeshPolygon.h>

#include <maya/MPointArray.h>
#include <maya/MVectorArray.h>

#include <maya/MFnWeightGeometryFilter.h>
#include <maya/MFnSingleIndexedComponent.h>
#include <maya/MMeshIntersector.h>


#include <vector>
#include <map>

#include <math.h>

#include <Eigen/Dense>
#include <Eigen/LU>



#if (!(defined _DEBUG) && (defined _OPENMP))
	#define RELEASE_OPENMP
	#include <maya/MThreadUtils.h>
	#include <omp.h>
#endif



#define oSpace MSpace::kObject
#define wSpace MSpace::kWorld

#define epsilon_d 1e-7


typedef std::vector<MIntArray>		MIntArrayVec;

typedef std::map<int, MIntArray>	MIntArrayMap;
typedef std::map<int, MPointArray>	MPointArrayMap;

typedef std::vector<double>			dVec;
typedef std::vector<dVec>			ddVec;
typedef std::map<int, ddVec>		ddVecMap;

typedef Eigen::Vector4d				EigenV4d;
typedef Eigen::Matrix4d				EigenM4d;




