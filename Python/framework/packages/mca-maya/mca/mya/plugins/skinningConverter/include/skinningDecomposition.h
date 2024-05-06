#ifndef _skinningDecomposition
#define _skinningDecomposition


#include "stdafx.h"
#include "object.h"
#include "conversion.h"





struct Inputs
{
	int				AF ;		// num allFrames
	MDoubleArray	allFrames ;
	int				F ;			// num frames = AF-1
	double			frame0 ;	// rest frame
	MDoubleArray	frames ;	// allFrames - frame0

	int				J ;			// num sourceJoints
	MStringVec		sourceJoints ;
	MStringVec		targetJoints ;
	bool			setMatrices ;	// false if targetJoints is empty

	int			V ;				// num vertices USED
	MIntArray	vertexIds ;		// vertexIds USED,  dim V

	int			MI ;			// maxInfluence
	double		lagragian ;

	int			maxIteration ;			// if maxIteration==1 ignore iterationFullSolver, updateRestMatrices, rigidMatrices.
	int			iterationFullSolver ;	// how much do I run the full joints solving ?
	bool		updateRestMatrices ;	// do I update rest matrices between each iteration ?
	bool		rigidMatrices ;			// output matrices are rigid or flexible(=scale+shear) ?
	double		errorPercentBreak ;		// this stops the iterative process when there is not enought difference with the previous result

	double		boundingBox_diagonal_sum; // needed by the error computation

	bool		useExistingSkinCluster ;// use this existing skinCluster to limit each NNLS to the existing influences
	intVecMap	existing_vertex_jIds ;	// dim V then MIdyn

	MString		shape_name ;

	MPointArray			rest_Pnts ;
	MPointArrayVector	frames_Pnts ;	// dim F  then V
};



struct Outputs
{
	// input and output :
	MMatrixVec		bindingMMs ;	// dim J
	MMatrixVecVec	framesMMs ;		// dim F  then J


	// Returned skinning data,  computed in PART 1
	intVecMap		vertex_jIds ;		// dim V then MI
	doubleVecMap	vertex_wgts ;		// dim V then MI

	// used in PART 2,  computed in PART 1
	intVecVec		joint_vIds ;		// dim J then 'affected V'
	intVecVec		joint_poss ;		// dim J then 'affected V'

	doubleVec		errors ;			// will be dim it
	doubleVec		errorPercents ;		// will be dim it
	int				iterationDone ;
};





class SkinningDecomposition : public MPxCommand
{

public:
	MStatus		doIt( const MArgList& );
	MStatus		redoIt();
	MStatus		undoIt();
	bool		isUndoable() const;

	static		void* creator();


	// added
	static MString	name ;
	
	MStatus			get_args( const MArgList& args ) ;

	static MSyntax	newSyntax() ;



private:
	// too much data to deal with  for a mel command.
	// use a node as only argument to store inputs+outputs datas
	MString		storage_name ;
	MTime		startTime ;

	bool		changed_numCPU ;
	int			availableCPU ;
	int			numCPU ;

	//
	Inputs		inputs ;
	Outputs		outputs ;



	// PART 1 : skinning solver

	void	update_weights( int& iteration ) ;

		void	build_A( int& vId, MatrixXd& out_A ) ;
		void	build_b( int& vId, VectorXd& out_b  ) ;

		void	get_maxInfluencerIds( VectorXd& x, intVec& out_ids  );

		void	build_A2(   intVec& maxInfIds, MatrixXd& A,  MatrixXd& out_A2 ) ;

	void	prepare_PART2_PART3( int& iteration ) ;

	void	get_error( int& iteration ) ;



	// PART 2 and 3 : bones solver

	void	update_bindingMMs() ;
		
		void	get_centroid_weighted( int& jId, MPointArray& pnts,  Vector3d& centroid ) ;
		

	void	update_framesMMs( int& it ) ;

		void	get_rigidMatrix(	Matrix3Xd& P, Matrix3Xd& Q, RowVector3d& p_star,RowVector3d& q_star,  MMatrix& transfo_MM) ;
		void	get_flexibleMatrix( Matrix3Xd& P, Matrix3Xd& Q, RowVector3d& p_star,RowVector3d& q_star,  MMatrix& transfo_MM) ;


	//
	void	output_weights( MFnDependencyNode& storage_Dep );
	void	output_matrices();
	void	output_error( MFnDependencyNode& storage_Dep ) ;
};


#endif

















