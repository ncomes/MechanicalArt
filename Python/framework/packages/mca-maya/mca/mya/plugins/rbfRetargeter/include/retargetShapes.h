#ifndef _retargetShapes
#define _retargetShapes

#include <vector>

#include <maya/MPxCommand.h>
#include <maya/MArgList.h>
#include <maya/MSyntax.h>

#include <maya/MObject.h>
#include <maya/MObjectArray.h>
#include <maya/MIntArray.h>

#include <maya/MFnMesh.h>

#include <maya/MPointArray.h>
#include <maya/MStringArray.h>

#include <Eigen/Dense>
#include <Eigen/LU>



#if (!(defined _DEBUG) && (defined _OPENMP))
	#define RELEASE_OPENMP
	#include <maya/MThreadUtils.h>
	#include <omp.h>
#endif




class RetargetShapes : public MPxCommand
{

public:

	// dv
	MStatus			doIt( const MArgList& args );
	MStatus			redoIt();
	MStatus			undoIt();
	bool			isUndoable() const;

	static void*	creator();



	// added
	static MString	name ;
	
	MStatus			get_args( const MArgList& args ) ;

	MStatus			build_solver( MIntArray& pnt_ids, Eigen::MatrixXd& out_X  ) ;

	void	compute_points( MPointArray& shape_Pnts, MIntArray& toVtx_ids ) ;

	Eigen::MatrixXd get_distanceMatrix( MIntArray& ids );

	
	static MSyntax	newSyntax() ;



private:
	// Store the data you will need to undo the command here
	
	// inputs
	MString			sourceName ;
	MString			targetName ;
	MStringArray	sourceShapeNames ;

	bool		static_sphere	;
	//int			growLevel ; // 0 = full,  else growMethod

	MIntArray	fromVtx_ids ;
	MIntArray	toVtx_ids ;


	// store Objs because no need to get them in each redo 
	MObject			source_Obj ;
	MObject			target_Obj ;
	MObjectArray	sourceShape_Objs ;



	// global data
	MPointArray			all_src_Pnts ;
	MPointArray			all_tgt_Pnts ;

	Eigen::MatrixXd		distanceMatrix ;


	// for the full method
	//MPointArray		nKeys ;
	MIntArray			nKeyIds ;
	int					matrixDim ;
	Eigen::MatrixXd		X ;
	/*
	// for the partial method,  same data but array
	//std::vector<MPointArray>		nKeyss ;
	std::vector<MIntArray>			nKeyIdss ;
	std::vector<int>				matrixDims ;
	std::vector<Eigen::MatrixXd>	Xs ;
	*/

	//MString		use_algo ;
	//bool			normalize_b ;
	//double		scale_d ;
	//double		dMax ;

	// output names for undo
	MStringArray	newTr_names ; // for the undo

};

#endif
