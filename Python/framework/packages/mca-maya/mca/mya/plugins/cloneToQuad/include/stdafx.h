

#include <maya/MStatus.h>
#include <maya/MPxNode.h>
#include <maya/MGlobal.h>

#include <maya/MTypeId.h>
#include <maya/MString.h>
#include <maya/MObject.h>
#include <maya/MDagPath.h>
#include <maya/MPlugArray.h>
#include <maya/MArrayDataHandle.h>

#include <maya/MFnNumericAttribute.h>
#include <maya/MFnTypedAttribute.h>
#include <maya/MFnEnumAttribute.h>
#include <maya/MFnMatrixAttribute.h>

#include <maya/MPointArray.h>
#include <maya/MFloatVectorArray.h>
#include <maya/MFloatPointArray.h>
#include <maya/MVectorArray.h>
#include <maya/MMatrix.h>
#include <maya/MBoundingBox.h>

#include <maya/MFnMesh.h>
#include <maya/MFnMeshData.h>
#include <maya/MItMeshVertex.h>
#include <maya/MItMeshPolygon.h>
#include <maya/MFnSet.h>


#include <vector>
#include <map>

typedef std::vector<int>		intVec ;
typedef std::vector<intVec>		intVecVec ;
typedef std::vector<intVecVec>	intVecVecVec ;

typedef std::vector<bool>		boolVec ;

typedef std::vector<double>		doubleVec ;
typedef std::vector<doubleVec>	doubleVecVec ;
typedef std::vector<doubleVecVec>doubleVecVecVec ;

typedef std::map<intVec, int>	intVec_to_int_map ;

typedef std::vector<MFloatArray>vecMFloatArray ;
typedef std::vector<MIntArray>	vecMIntArray ;

#include <utility> 

typedef std::pair<int, int>			pairII ;
typedef std::pair<double, double>	pairDD ;
typedef std::vector<pairII>			vecPairII ;

#include <iterator> // distance



#include <Eigen/Dense>

typedef Eigen::RowVector4d		RowVector4d ;
typedef Eigen::Vector4d			Vector4d ;
typedef Eigen::Vector2d			Vector2d ;
typedef Eigen::Matrix4d			Matrix4d ;


#include <iso646.h>  // define "not" ( ! ), this shit is used in OpenSubdiv
#include <opensubdiv/far/topologyDescriptor.h>
#include <opensubdiv/far/topologyRefinerFactory.h>
#include <opensubdiv/far/patchTableFactory.h>
#include <opensubdiv/far/stencilTableFactory.h>
#include <opensubdiv/far/ptexIndices.h>

typedef OpenSubdiv::Far::TopologyDescriptor					Descriptor ;
typedef OpenSubdiv::Far::TopologyRefiner					Refiner ;
typedef OpenSubdiv::Far::TopologyRefinerFactory<Descriptor>	RefinerFactory ;

typedef OpenSubdiv::Sdc::Options							RefinerOptions ;

typedef OpenSubdiv::Far::PatchTable							PatchTable ;
typedef OpenSubdiv::Far::PatchTableFactory					PatchTableFactory ;

typedef OpenSubdiv::Far::LimitStencilTable					LimitStencilTable ;
typedef OpenSubdiv::Far::LimitStencilTableFactory			LimitStencilTableFactory ;
typedef LimitStencilTableFactory::LocationArray				LocationArray ;
typedef LimitStencilTableFactory::LocationArrayVec			LocationArrayVec ;

typedef OpenSubdiv::Far::PtexIndices						PtexIndices ;



#define localSpace MSpace::kObject
#define worldSpace MSpace::kWorld

#define epsilon 1e-7

