
#include <vector>
#include <map>
#include <set>
#include <queue>
#include <cassert>

#include <maya/MPxCommand.h>
#include <maya/MSyntax.h>
#include <maya/MArgParser.h>
#include <maya/MArgList.h>
#include <maya/MGlobal.h>
#include <maya/MTime.h>
#include <maya/MAnimControl.h>

#include <maya/MObjectArray.h>
#include <maya/MSelectionList.h>
#include <maya/MFnSingleIndexedComponent.h>
#include <maya/MPlug.h>
#include <maya/MPlugArray.h>
#include <maya/MFnAttribute.h>
#include <maya/MFnTypedAttribute.h>

#include <maya/MStringArray.h>
#include <maya/MMatrixArray.h>
#include <maya/MPointArray.h>
#include <maya/MDoubleArray.h>

#include <maya/MFnIntArrayData.h>
#include <maya/MFnStringArrayData.h>
#include <maya/MFnMatrixData.h>
#include <maya/MFnDoubleArrayData.h>

#include <maya/MFnMesh.h>
#include <maya/MFnSkinCluster.h>
#include <maya/MFnTransform.h>
#include <maya/MTransformationMatrix.h>
#include <maya/MEulerRotation.h>
#include <maya/MQuaternion.h>
#include <maya/MBoundingBox.h>

#include <maya/MDagPath.h>
#include <maya/MDagPathArray.h>
#include <maya/MFnDagNode.h>

#include <Eigen/Dense>
#include <Eigen/QR>

#include "nnls.h"



// multithreading
//
#include <maya/MThreadUtils.h>
#include <omp.h>


#if (!(defined _DEBUG) && (defined _OPENMP))
	#define RELEASE_OPENMP
	#define EIGEN_DONT_PARALLELIZE
#endif




#define space MSpace::kWorld

#define epsilon_d 1e-7


//
typedef std::map<int, MObject>		MObjectMap ;
typedef std::vector<MObject>		MObjectVec ;
typedef std::vector<MObjectVec>		MObjectVecVec ;

typedef std::map<int, MString>		MStringMap ;
typedef std::vector<MString>		MStringVec ;

typedef std::vector<MMatrix>		MMatrixVec ;
typedef std::vector<MMatrixVec>		MMatrixVecVec ;

typedef std::map<int, MMatrix>		MMatrixMap ;
typedef std::map<int, MMatrixMap>	MMatrixMapMap ;

typedef std::map<int, MPointArray>	MPointArrayMap ;
typedef std::vector<MPointArray>	MPointArrayVector ;
typedef std::vector<MPoint>			MPointVec ;
//typedef std::map<int, MPointVec>	MPointVecMap ;

typedef std::map<int, MIntArray>	MIntArrayMap ;
typedef std::map<int, MDoubleArray>	MDoubleArrayMap ;

typedef std::vector<int>			intVec ;
typedef std::vector<intVec>			intVecVec ;
typedef std::map<int, intVec>		intVecMap ;

typedef std::vector<double>			doubleVec ;
typedef std::vector<doubleVec>		doubleVecVec ;
typedef std::map<int, doubleVec>	doubleVecMap ;

typedef std::set<int>				intSet ;
typedef std::vector<intSet>			intSetVec ;
typedef std::map<int, intSet>		intSetMap ;

typedef std::map<int,int>			intIntMap ;

typedef std::pair<double, int>		pairDbleInt ;
typedef std::priority_queue<pairDbleInt>	pq_pairDbleInt ;

typedef MEulerRotation::RotationOrder			EulerRo ;
typedef std::vector<EulerRo>					EulerRoVec ;
typedef MTransformationMatrix::RotationOrder	TransfoRo ;


//
typedef Eigen::MatrixXd		MatrixXd ;

typedef Eigen::MatrixX3d	MatrixX3d ;
typedef Eigen::Matrix3Xd	Matrix3Xd ;
typedef Eigen::Matrix3d		Matrix3d ; // 3*3
typedef Eigen::Matrix<double,2,3>					Matrix23d ; // 2*3
typedef Eigen::Matrix<double,2,Eigen::Dynamic>		Matrix2Xd ; // 2*x

typedef std::map<int, MatrixX3d>	MatrixX3d_map ;

typedef Eigen::Vector3d		Vector3d ;
typedef Eigen::VectorXd		VectorXd ;

typedef Eigen::RowVector3d			RowVector3d ;
typedef Eigen::RowVectorXd			RowVectorXd ;
typedef std::vector<RowVector3d>	RowVector3d_vec ;


typedef Eigen::HouseholderQR<MatrixXd>	QR ;
typedef Eigen::NNLS<MatrixXd>			NNLS ;
typedef Eigen::JacobiSVD<MatrixXd>		SvdXd ;	// svd works only with Xd matrices, crashing otherwise







